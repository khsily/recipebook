from __future__ import annotations

import json
import math
import os
import platform
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sentence_transformers import SentenceTransformer

from run_experiment import (
    ONTO,
    SEED,
    ARTICLE,
    bm25,
    char,
    concepts,
    dtext,
    evaluate,
    load,
    ontology_scores,
    qtext,
    ranks,
    rrf,
)

MODEL_NAME = os.getenv("MODEL_NAME", "intfloat/multilingual-e5-small")
RESULT_DIR = Path(os.getenv("RESULT_DIR", "research/ontology_korean_qa/results"))
RESULT_DIR.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(SEED)


@dataclass(frozen=True)
class BaseConfig:
    rrf_k: int
    char_weight: float
    dense_weight: float


@dataclass(frozen=True)
class OntologyConfig:
    mode: str
    weight: float
    top_n: int = 0
    gate_threshold: float = -math.inf


def normalize_rows(values: np.ndarray) -> np.ndarray:
    lo = values.min(axis=1, keepdims=True)
    hi = values.max(axis=1, keepdims=True)
    return (values - lo) / np.maximum(hi - lo, 1e-12)


def split_indices(qdf: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    meta = qdf["meta"].astype(str)
    dev = np.flatnonzero(meta.str.contains("13회차", regex=False).to_numpy())
    test = np.flatnonzero(meta.str.contains("14회차", regex=False).to_numpy())
    if len(dev) == 0 or len(test) == 0:
        raise RuntimeError("Expected both 13회차 and 14회차 examples in KCL-MCQA metadata.")
    if set(dev).intersection(test):
        raise RuntimeError("Development and test indices overlap.")
    return dev, test


def subset_gold(gold: list[set[str]], indices: np.ndarray) -> list[set[str]]:
    return [gold[int(i)] for i in indices]


def metric_row(rank: np.ndarray, gold: list[set[str]], doc_ids: list[str]) -> dict[str, float]:
    frame, _ = evaluate({"candidate": rank}, gold, doc_ids)
    return frame.iloc[0].to_dict()


def objective(row: dict[str, float]) -> tuple[float, float, float]:
    return (float(row["nDCG@10"]), float(row["MRR@10"]), float(row["Recall@10"]))


def tune_base(component_ranks, dev_idx, dev_gold, doc_ids):
    records = []
    best_cfg = None
    best_obj = (-1.0, -1.0, -1.0)
    for k in (10, 20, 40, 60, 100):
        for char_weight in (0.5, 1.0, 1.5, 2.0):
            for dense_weight in (0.25, 0.5, 0.75, 1.0):
                score = rrf(
                    [component_ranks["BM25"], component_ranks["CharTFIDF"], component_ranks["Dense-E5"]],
                    [1.0, char_weight, dense_weight],
                    k,
                )
                rank = ranks(score)[dev_idx]
                row = metric_row(rank, dev_gold, doc_ids)
                record = {"rrf_k": k, "char_weight": char_weight, "dense_weight": dense_weight, **row}
                records.append(record)
                if objective(row) > best_obj:
                    best_obj = objective(row)
                    best_cfg = BaseConfig(k, char_weight, dense_weight)
    assert best_cfg is not None
    return best_cfg, pd.DataFrame(records).sort_values(["nDCG@10", "MRR@10", "Recall@10"], ascending=False)


def base_scores(component_ranks, cfg):
    return rrf(
        [component_ranks["BM25"], component_ranks["CharTFIDF"], component_ranks["Dense-E5"]],
        [1.0, cfg.char_weight, cfg.dense_weight],
        cfg.rrf_k,
    )


def ontology_confidence(onto_score):
    sorted_score = np.sort(onto_score, axis=1)[:, ::-1]
    top = sorted_score[:, 0]
    top10_mean = sorted_score[:, : min(10, sorted_score.shape[1])].mean(axis=1)
    return top - top10_mean


def rerank_top_n(base_score, onto_score, alpha, top_n):
    base_rank = ranks(base_score)
    base_norm = normalize_rows(base_score)
    onto_norm = normalize_rows(onto_score)
    out = np.empty_like(base_rank)
    for i in range(base_rank.shape[0]):
        candidates = base_rank[i, :top_n]
        candidate_score = base_norm[i, candidates] + alpha * onto_norm[i, candidates]
        order = candidates[np.argsort(-candidate_score, kind="mergesort")]
        out[i, :top_n] = order
        out[i, top_n:] = base_rank[i, top_n:]
    return out


def gated_rrf(base_score, onto_rank, weight, k, confidence, threshold):
    base_rank = ranks(base_score)
    candidate_score = rrf([base_rank, onto_rank], [1.0, weight], k)
    candidate_rank = ranks(candidate_score)
    return np.where((confidence >= threshold)[:, None], candidate_rank, base_rank)


def tune_ontology(base_score, onto_score, dev_idx, dev_gold, doc_ids, k):
    onto_rank = ranks(onto_score)
    conf = ontology_confidence(onto_score)
    records = []
    best_cfg = OntologyConfig("none", 0.0)
    best_obj = objective(metric_row(ranks(base_score)[dev_idx], dev_gold, doc_ids))

    for weight in (0.025, 0.05, 0.1, 0.2, 0.3, 0.5):
        rank = ranks(rrf([ranks(base_score), onto_rank], [1.0, weight], k))
        row = metric_row(rank[dev_idx], dev_gold, doc_ids)
        records.append({"mode": "rrf", "weight": weight, "top_n": 0, "gate_threshold": -1.0, **row})
        if objective(row) > best_obj:
            best_obj = objective(row)
            best_cfg = OntologyConfig("rrf", weight)

    for top_n in (10, 20, 50, 100):
        for alpha in (0.01, 0.025, 0.05, 0.1, 0.2):
            rank = rerank_top_n(base_score, onto_score, alpha, top_n)
            row = metric_row(rank[dev_idx], dev_gold, doc_ids)
            records.append({"mode": "rerank", "weight": alpha, "top_n": top_n, "gate_threshold": -1.0, **row})
            if objective(row) > best_obj:
                best_obj = objective(row)
                best_cfg = OntologyConfig("rerank", alpha, top_n)

    thresholds = sorted(set(float(x) for x in np.quantile(conf[dev_idx], [0.0, 0.25, 0.5, 0.75, 0.9])))
    for threshold in thresholds:
        for weight in (0.05, 0.1, 0.2, 0.3, 0.5):
            rank = gated_rrf(base_score, onto_rank, weight, k, conf, threshold)
            row = metric_row(rank[dev_idx], dev_gold, doc_ids)
            records.append({"mode": "gated_rrf", "weight": weight, "top_n": 0, "gate_threshold": threshold, **row})
            if objective(row) > best_obj:
                best_obj = objective(row)
                best_cfg = OntologyConfig("gated_rrf", weight, 0, threshold)

    return best_cfg, pd.DataFrame(records).sort_values(["nDCG@10", "MRR@10", "Recall@10"], ascending=False)


def apply_ontology_config(base_score, onto_score, cfg, k):
    if cfg.mode == "none":
        return ranks(base_score)
    if cfg.mode == "rrf":
        return ranks(rrf([ranks(base_score), ranks(onto_score)], [1.0, cfg.weight], k))
    if cfg.mode == "rerank":
        return rerank_top_n(base_score, onto_score, cfg.weight, cfg.top_n)
    if cfg.mode == "gated_rrf":
        return gated_rrf(base_score, ranks(onto_score), cfg.weight, k, ontology_confidence(onto_score), cfg.gate_threshold)
    raise ValueError(f"Unsupported ontology mode: {cfg.mode}")


def per_query_metrics(methods, gold, doc_ids, indices, qdf, ddf):
    _, per = evaluate({name: rank[indices] for name, rank in methods.items()}, subset_gold(gold, indices), doc_ids)
    mapping = {local: int(global_id) for local, global_id in enumerate(indices)}
    per["global_qid"] = per["qid"].map(mapping)
    meta = qdf.reset_index().rename(columns={"index": "global_qid"})[["global_qid", "meta", "question", "n_gold"]]
    per = per.merge(meta, on="global_qid", how="left")
    per["top_title"] = per["top_doc"].map(ddf.set_index("doc_id")["title"].to_dict())
    return per


def paired_bootstrap(a, b, n_samples=20000):
    delta = b - a
    draws = []
    batch = 500
    for _ in range(math.ceil(n_samples / batch)):
        sample_index = RNG.integers(0, len(delta), size=(batch, len(delta)))
        draws.extend(delta[sample_index].mean(axis=1).tolist())
    draws = np.asarray(draws[:n_samples])
    return {
        "mean_difference": float(delta.mean()),
        "ci_low": float(np.quantile(draws, 0.025)),
        "ci_high": float(np.quantile(draws, 0.975)),
        "p_bootstrap_two_sided": float(2 * min((draws <= 0).mean(), (draws >= 0).mean())),
    }


def domain_from_meta(meta):
    if "민사법" in meta:
        return "민사법"
    if "형사법" in meta:
        return "형사법"
    if "공법" in meta:
        return "공법"
    return "기타"


def encode_queries(model, query_texts):
    return np.asarray(model.encode(["query: " + text for text in query_texts], batch_size=32, normalize_embeddings=True, show_progress_bar=True), dtype=np.float32)


def build_variant_scores(variant_queries, doc_texts, doc_embeddings, model):
    bm25_score = bm25(variant_queries, doc_texts)
    char_score = char(variant_queries, doc_texts)
    dense_score = np.asarray(encode_queries(model, variant_queries) @ doc_embeddings.T, dtype=np.float32)
    onto_score = ontology_scores(variant_queries, doc_texts)
    return {"BM25": bm25_score, "CharTFIDF": char_score, "Dense-E5": dense_score, "Ontology": onto_score}


def main():
    started = time.time()
    qdf, ddf, gold = load()
    doc_ids = ddf["doc_id"].tolist()
    query_texts = [qtext(row) for _, row in qdf.iterrows()]
    question_only = [qtext(row, False) for _, row in qdf.iterrows()]
    doc_texts = [dtext(row) for _, row in ddf.iterrows()]
    dev_idx, test_idx = split_indices(qdf)
    dev_gold = subset_gold(gold, dev_idx)
    test_gold = subset_gold(gold, test_idx)

    timings = {}
    t = time.perf_counter()
    bm25_score = bm25(query_texts, doc_texts)
    timings["bm25_s"] = time.perf_counter() - t
    t = time.perf_counter()
    char_score = char(query_texts, doc_texts)
    timings["char_tfidf_s"] = time.perf_counter() - t

    t = time.perf_counter()
    model = SentenceTransformer(MODEL_NAME, device="cpu")
    doc_embeddings = np.asarray(model.encode(["passage: " + text for text in doc_texts], batch_size=32, normalize_embeddings=True, show_progress_bar=True), dtype=np.float32)
    query_embeddings = encode_queries(model, query_texts)
    dense_score = np.asarray(query_embeddings @ doc_embeddings.T, dtype=np.float32)
    timings["dense_encoding_s"] = time.perf_counter() - t

    t = time.perf_counter()
    onto_score = ontology_scores(query_texts, doc_texts)
    timings["ontology_scoring_s"] = time.perf_counter() - t

    component_score = {"BM25": bm25_score, "CharTFIDF": char_score, "Dense-E5": dense_score}
    component_rank = {name: ranks(score) for name, score in component_score.items()}

    base_cfg, base_grid = tune_base(component_rank, dev_idx, dev_gold, doc_ids)
    base_score = base_scores(component_rank, base_cfg)
    base_rank = ranks(base_score)
    ontology_cfg, ontology_grid = tune_ontology(base_score, onto_score, dev_idx, dev_gold, doc_ids, base_cfg.rrf_k)
    selected_rank = apply_ontology_config(base_score, onto_score, ontology_cfg, base_cfg.rrf_k)
    naive_rank = ranks(rrf([base_rank, ranks(onto_score)], [1.0, 0.75], base_cfg.rrf_k))

    methods = {
        "BM25": component_rank["BM25"],
        "CharTFIDF": component_rank["CharTFIDF"],
        "Dense-E5": component_rank["Dense-E5"],
        "Strong-Hybrid": base_rank,
        "Naive-Ontology": naive_rank,
        "Dev-Tuned-Ontology": selected_rank,
    }
    dev_metrics, _ = evaluate({name: rank[dev_idx] for name, rank in methods.items()}, dev_gold, doc_ids)
    test_metrics, _ = evaluate({name: rank[test_idx] for name, rank in methods.items()}, test_gold, doc_ids)
    dev_metrics.to_csv(RESULT_DIR / "holdout_metrics_dev.csv", index=False)
    test_metrics.to_csv(RESULT_DIR / "holdout_metrics_test.csv", index=False)
    base_grid.to_csv(RESULT_DIR / "holdout_base_tuning.csv", index=False)
    ontology_grid.to_csv(RESULT_DIR / "holdout_ontology_tuning.csv", index=False)

    per = per_query_metrics(methods, gold, doc_ids, test_idx, qdf, ddf)
    per["domain"] = per["meta"].map(domain_from_meta)
    per.to_csv(RESULT_DIR / "holdout_per_query.csv", index=False)
    per.groupby(["method", "domain"])[["Recall@1", "Recall@5", "Recall@10", "MRR@10", "nDCG@10", "MAP@10"]].mean().reset_index().to_csv(RESULT_DIR / "holdout_metrics_by_domain.csv", index=False)

    pivot = per.pivot(index="global_qid", columns="method", values=["MRR@10", "nDCG@10", "Recall@5"])
    significance = {}
    for metric in ("MRR@10", "nDCG@10", "Recall@5"):
        a = pivot[metric]["Strong-Hybrid"].to_numpy()
        b = pivot[metric]["Dev-Tuned-Ontology"].to_numpy()
        result = paired_bootstrap(a, b)
        stat, p_value = wilcoxon(b, a, zero_method="pratt")
        result.update({"wilcoxon_stat": float(stat), "wilcoxon_p": float(p_value)})
        significance[metric] = result
    (RESULT_DIR / "holdout_significance.json").write_text(json.dumps(significance, ensure_ascii=False, indent=2), encoding="utf-8")

    confidence = ontology_confidence(onto_score)
    q_concept_count = np.asarray([len(concepts(text)) for text in query_texts])
    test_analysis = qdf.iloc[test_idx][["qid", "meta", "question", "n_gold"]].copy()
    test_analysis["ontology_confidence"] = confidence[test_idx]
    test_analysis["ontology_concept_count"] = q_concept_count[test_idx]
    test_analysis["confidence_group"] = pd.qcut(test_analysis["ontology_confidence"], q=4, labels=["Q1-low", "Q2", "Q3", "Q4-high"], duplicates="drop")
    selected_per = per[per["method"].isin(["Strong-Hybrid", "Dev-Tuned-Ontology"])].copy()
    selected_per = selected_per.merge(test_analysis[["qid", "ontology_confidence", "ontology_concept_count", "confidence_group"]], left_on="global_qid", right_on="qid", how="left", suffixes=("", "_analysis"))
    selected_per.groupby(["method", "confidence_group"], observed=True)[["Recall@5", "Recall@10", "MRR@10", "nDCG@10"]].mean().reset_index().to_csv(RESULT_DIR / "holdout_metrics_by_confidence.csv", index=False)

    wide = selected_per.pivot(index="global_qid", columns="method", values=["MRR@10", "nDCG@10"])
    delta = pd.DataFrame(index=wide.index)
    delta["mrr_gain"] = wide["MRR@10"]["Dev-Tuned-Ontology"] - wide["MRR@10"]["Strong-Hybrid"]
    delta["ndcg_gain"] = wide["nDCG@10"]["Dev-Tuned-Ontology"] - wide["nDCG@10"]["Strong-Hybrid"]
    cases = test_analysis.set_index("qid").join(delta, how="left").reset_index()
    cases.nlargest(15, "ndcg_gain").to_csv(RESULT_DIR / "holdout_largest_gains.csv", index=False)
    cases.nsmallest(15, "ndcg_gain").to_csv(RESULT_DIR / "holdout_largest_losses.csv", index=False)

    variants = {
        "Full item": query_texts,
        "Question only": question_only,
        "Article masked": [ARTICLE.sub("[조문]", text) for text in query_texts],
    }
    robustness_records = []
    for variant_name, variant_queries in variants.items():
        if variant_name == "Full item":
            variant_component = component_score
            variant_onto = onto_score
        else:
            scores = build_variant_scores(variant_queries, doc_texts, doc_embeddings, model)
            variant_component = {name: scores[name] for name in ("BM25", "CharTFIDF", "Dense-E5")}
            variant_onto = scores["Ontology"]
        variant_ranks = {name: ranks(score) for name, score in variant_component.items()}
        variant_base_score = base_scores(variant_ranks, base_cfg)
        variant_methods = {
            "Strong-Hybrid": ranks(variant_base_score),
            "Dev-Tuned-Ontology": apply_ontology_config(variant_base_score, variant_onto, ontology_cfg, base_cfg.rrf_k),
        }
        frame, _ = evaluate({name: rank[test_idx] for name, rank in variant_methods.items()}, test_gold, doc_ids)
        frame.insert(0, "variant", variant_name)
        robustness_records.append(frame)
    pd.concat(robustness_records, ignore_index=True).to_csv(RESULT_DIR / "holdout_robustness.csv", index=False)

    tuning = {
        "development_cohort": "13회차 변호사시험",
        "held_out_test_cohort": "14회차 변호사시험",
        "n_dev": int(len(dev_idx)),
        "n_test": int(len(test_idx)),
        "base_config": base_cfg.__dict__,
        "ontology_config": ontology_cfg.__dict__,
        "selection_objective": ["nDCG@10", "MRR@10", "Recall@10"],
        "dense_model": MODEL_NAME,
        "ontology_nodes": len(ONTO),
    }
    (RESULT_DIR / "holdout_tuning.json").write_text(json.dumps(tuning, ensure_ascii=False, indent=2), encoding="utf-8")
    (RESULT_DIR / "holdout_run_metadata.json").write_text(json.dumps({**tuning, "seed": SEED, "python": platform.python_version(), "platform": platform.platform(), "timings": timings, "elapsed_total_s": time.time() - started}, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Selected base configuration:", base_cfg)
    print("Selected ontology configuration:", ontology_cfg)
    print("\nHeld-out test results")
    print(test_metrics.to_string(index=False))
    print("\nSignificance")
    print(json.dumps(significance, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
