from __future__ import annotations

import json
import math
import os
import platform
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

from run_experiment import (
    ONTO,
    SEED,
    bm25,
    char,
    concepts,
    dtext,
    evaluate,
    expand,
    load,
    ontology_scores,
    qtext,
    ranks,
    statutes,
)

RESULT_DIR = Path(os.getenv("RESULT_DIR", "research/ontology_korean_qa/results"))
RESULT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_NAME = os.getenv("MODEL_NAME", "intfloat/multilingual-e5-small")
RNG = np.random.default_rng(SEED)


def normalize_rows(x):
    lo = x.min(axis=1, keepdims=True)
    hi = x.max(axis=1, keepdims=True)
    return (x - lo) / np.maximum(hi - lo, 1e-12)


def reciprocal_rank_feature(score, offset=10.0):
    order = ranks(score)
    inv = np.empty_like(order)
    inv[np.arange(order.shape[0])[:, None], order] = np.arange(order.shape[1])[None, :]
    return 1.0 / (offset + inv.astype(np.float32) + 1.0)


def split_indices(qdf):
    meta = qdf.meta.astype(str)
    dev = np.flatnonzero(meta.str.contains("13회차", regex=False).to_numpy())
    test = np.flatnonzero(meta.str.contains("14회차", regex=False).to_numpy())
    if len(dev) != 142 or len(test) != 141:
        raise RuntimeError(f"Unexpected temporal split: dev={len(dev)}, test={len(test)}")
    return dev, test


def concept_features(query_texts, doc_texts):
    q_concepts = [expand(concepts(x), True, True) for x in query_texts]
    d_concepts = [expand(concepts(x), True, True) for x in doc_texts]
    q_statutes = [statutes(x) for x in query_texts]
    d_statutes = [statutes(x) for x in doc_texts]
    nq, nd = len(query_texts), len(doc_texts)
    jaccard = np.zeros((nq, nd), dtype=np.float32)
    overlap = np.zeros((nq, nd), dtype=np.float32)
    statute_overlap = np.zeros((nq, nd), dtype=np.float32)
    query_coverage = np.zeros((nq, nd), dtype=np.float32)
    for i, q in enumerate(q_concepts):
        qset = set(q)
        for j, d in enumerate(d_concepts):
            dset = set(d)
            common = qset & dset
            union = qset | dset
            if union:
                jaccard[i, j] = len(common) / len(union)
            if common:
                overlap[i, j] = sum(min(q[c], d[c]) for c in common)
            if qset:
                query_coverage[i, j] = len(common) / len(qset)
            if q_statutes[i] and d_statutes[j]:
                statute_overlap[i, j] = min(len(q_statutes[i] & d_statutes[j]), 3) / 3.0
    return jaccard, overlap, query_coverage, statute_overlap


def build_feature_tensor(scores, ontology_extra):
    base_names = ["bm25", "char", "dense"]
    base = []
    base_labels = []
    for name in base_names:
        base.append(normalize_rows(scores[name]))
        base_labels.append(f"{name}_score")
        base.append(reciprocal_rank_feature(scores[name]))
        base_labels.append(f"{name}_rr")
    base_tensor = np.stack(base, axis=2)

    ontology = [normalize_rows(scores["ontology"]), reciprocal_rank_feature(scores["ontology"])]
    ontology_labels = ["ontology_score", "ontology_rr"]
    for label, value in zip(["concept_jaccard", "concept_overlap", "query_concept_coverage", "statute_overlap"], ontology_extra):
        ontology.append(value)
        ontology_labels.append(label)
    ontology_tensor = np.stack(ontology, axis=2)
    return base_tensor, ontology_tensor, base_labels, ontology_labels


def gold_indices(gold, doc_ids):
    mapping = {doc_id: i for i, doc_id in enumerate(doc_ids)}
    return [{mapping[x] for x in items} for items in gold]


def candidate_negatives(base_score, positive, limit=30):
    order = np.argsort(-base_score, kind="mergesort")
    negatives = [int(x) for x in order if int(x) not in positive]
    return negatives[:limit]


def pairwise_rows(features, query_ids, gold_idx, candidate_score, max_neg=30):
    xs = []
    ys = []
    groups = []
    for qid in query_ids:
        positive = gold_idx[int(qid)]
        if not positive:
            continue
        negatives = candidate_negatives(candidate_score[int(qid)], positive, max_neg)
        for pos in positive:
            for neg in negatives:
                delta = features[int(qid), int(pos)] - features[int(qid), int(neg)]
                xs.append(delta)
                ys.append(1)
                groups.append(int(qid))
                xs.append(-delta)
                ys.append(0)
                groups.append(int(qid))
    return np.asarray(xs, dtype=np.float32), np.asarray(ys, dtype=np.int8), np.asarray(groups, dtype=np.int32)


def fit_ranker(features, train_qids, gold_idx, candidate_score, c_value):
    x, y, _ = pairwise_rows(features, train_qids, gold_idx, candidate_score)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    model = LogisticRegression(C=c_value, penalty="l2", fit_intercept=False, solver="liblinear", max_iter=3000, random_state=SEED)
    model.fit(x_scaled, y)
    effective_weight = model.coef_[0] / np.maximum(scaler.scale_, 1e-12)
    return model, scaler, effective_weight, len(y)


def score_ranker(features, model, scaler):
    nq, nd, nf = features.shape
    score = model.decision_function(scaler.transform(features.reshape(-1, nf))).reshape(nq, nd)
    return score.astype(np.float32)


def objective(metric_row):
    return float(metric_row["nDCG@10"]), float(metric_row["MRR@10"]), float(metric_row["Recall@10"])


def tune_c(features, dev_idx, gold_idx, candidate_score, doc_ids):
    c_values = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    kfold = KFold(n_splits=5, shuffle=True, random_state=SEED)
    records = []
    best_c = None
    best_obj = (-1.0, -1.0, -1.0)
    dev_idx = np.asarray(dev_idx)
    for c_value in c_values:
        fold_rows = []
        for fold, (train_local, valid_local) in enumerate(kfold.split(dev_idx), 1):
            train_qids = dev_idx[train_local]
            valid_qids = dev_idx[valid_local]
            model, scaler, _, n_pairs = fit_ranker(features, train_qids, gold_idx, candidate_score, c_value)
            rank = ranks(score_ranker(features[valid_qids], model, scaler))
            frame, _ = evaluate({"ranker": rank}, [gold[int(i)] for i in valid_qids], doc_ids)
            row = frame.iloc[0].to_dict()
            fold_rows.append(row)
            records.append({"C": c_value, "fold": fold, "n_train_pair_rows": n_pairs, **row})
        mean = pd.DataFrame(fold_rows).mean(numeric_only=True).to_dict()
        obj = objective(mean)
        if obj > best_obj:
            best_obj = obj
            best_c = c_value
    return best_c, pd.DataFrame(records)


def paired_bootstrap(a, b, n=20000):
    delta = b - a
    samples = []
    for _ in range(math.ceil(n / 500)):
        index = RNG.integers(0, len(delta), size=(500, len(delta)))
        samples.extend(delta[index].mean(axis=1).tolist())
    samples = np.asarray(samples[:n])
    p = 2 * min((samples <= 0).mean(), (samples >= 0).mean())
    return {"mean_difference": float(delta.mean()), "ci_low": float(np.quantile(samples, 0.025)), "ci_high": float(np.quantile(samples, 0.975)), "p_bootstrap_two_sided": float(min(p, 1.0))}


def main():
    started = time.time()
    qdf, ddf, gold_data = load()
    global gold
    gold = gold_data
    doc_ids = ddf.doc_id.tolist()
    gold_idx = gold_indices(gold, doc_ids)
    query_texts = [qtext(row) for _, row in qdf.iterrows()]
    doc_texts = [dtext(row) for _, row in ddf.iterrows()]
    dev_idx, test_idx = split_indices(qdf)

    timings = {}
    t = time.perf_counter()
    bm25_score = bm25(query_texts, doc_texts)
    char_score = char(query_texts, doc_texts)
    timings["lexical_s"] = time.perf_counter() - t

    t = time.perf_counter()
    encoder = SentenceTransformer(MODEL_NAME, device="cpu")
    q_embeddings = encoder.encode(["query: " + x for x in query_texts], batch_size=32, normalize_embeddings=True, show_progress_bar=True)
    d_embeddings = encoder.encode(["passage: " + x for x in doc_texts], batch_size=32, normalize_embeddings=True, show_progress_bar=True)
    dense_score = np.asarray(q_embeddings @ d_embeddings.T, dtype=np.float32)
    timings["dense_s"] = time.perf_counter() - t

    t = time.perf_counter()
    ontology_score = ontology_scores(query_texts, doc_texts)
    extra = concept_features(query_texts, doc_texts)
    timings["ontology_s"] = time.perf_counter() - t

    score_map = {"bm25": bm25_score, "char": char_score, "dense": dense_score, "ontology": ontology_score}
    base_features, ontology_features, base_labels, ontology_labels = build_feature_tensor(score_map, extra)
    full_features = np.concatenate([base_features, ontology_features], axis=2)

    candidate_score = normalize_rows(char_score) + 0.5 * normalize_rows(bm25_score) + 0.25 * normalize_rows(dense_score)
    best_c_base, cv_base = tune_c(base_features, dev_idx, gold_idx, candidate_score, doc_ids)
    best_c_full, cv_full = tune_c(full_features, dev_idx, gold_idx, candidate_score, doc_ids)
    cv_base.insert(0, "feature_set", "retrieval_only")
    cv_full.insert(0, "feature_set", "retrieval_plus_ontology")
    pd.concat([cv_base, cv_full], ignore_index=True).to_csv(RESULT_DIR / "ltr_cross_validation.csv", index=False)

    base_model, base_scaler, base_weight, n_base_pairs = fit_ranker(base_features, dev_idx, gold_idx, candidate_score, best_c_base)
    full_model, full_scaler, full_weight, n_full_pairs = fit_ranker(full_features, dev_idx, gold_idx, candidate_score, best_c_full)
    base_rank = ranks(score_ranker(base_features, base_model, base_scaler))
    full_rank = ranks(score_ranker(full_features, full_model, full_scaler))

    baseline_rank = ranks(candidate_score)
    methods = {"Fixed-Fusion": baseline_rank, "LTR-Retrieval": base_rank, "LTR-Ontology": full_rank}
    dev_metrics, _ = evaluate({name: rank[dev_idx] for name, rank in methods.items()}, [gold[int(i)] for i in dev_idx], doc_ids)
    test_metrics, per = evaluate({name: rank[test_idx] for name, rank in methods.items()}, [gold[int(i)] for i in test_idx], doc_ids)
    dev_metrics.to_csv(RESULT_DIR / "ltr_metrics_dev.csv", index=False)
    test_metrics.to_csv(RESULT_DIR / "ltr_metrics_test.csv", index=False)

    q_meta = qdf.iloc[test_idx][["qid", "meta", "question", "n_gold"]].reset_index(drop=True)
    per = per.merge(q_meta, on="qid", how="left")
    per["domain"] = per.meta.apply(lambda x: "민사법" if "민사법" in x else ("형사법" if "형사법" in x else ("공법" if "공법" in x else "기타")))
    per.to_csv(RESULT_DIR / "ltr_per_query.csv", index=False)
    per.groupby(["method", "domain"])[["Recall@1", "Recall@5", "Recall@10", "MRR@10", "nDCG@10", "MAP@10"]].mean().reset_index().to_csv(RESULT_DIR / "ltr_metrics_by_domain.csv", index=False)

    coefficient_rows = []
    for label, value in zip(base_labels, base_weight):
        coefficient_rows.append({"model": "LTR-Retrieval", "feature": label, "effective_weight": float(value)})
    for label, value in zip(base_labels + ontology_labels, full_weight):
        coefficient_rows.append({"model": "LTR-Ontology", "feature": label, "effective_weight": float(value)})
    pd.DataFrame(coefficient_rows).to_csv(RESULT_DIR / "ltr_coefficients.csv", index=False)

    pivot = per.pivot(index="qid", columns="method", values=["MRR@10", "nDCG@10", "Recall@5"])
    significance = {}
    for metric in ("MRR@10", "nDCG@10", "Recall@5"):
        a = pivot[metric]["LTR-Retrieval"].to_numpy()
        b = pivot[metric]["LTR-Ontology"].to_numpy()
        result = paired_bootstrap(a, b)
        try:
            stat, p = wilcoxon(b, a, zero_method="pratt")
            result.update({"wilcoxon_stat": float(stat), "wilcoxon_p": float(p)})
        except ValueError:
            result.update({"wilcoxon_stat": 0.0, "wilcoxon_p": 1.0})
        significance[metric] = result
    (RESULT_DIR / "ltr_significance.json").write_text(json.dumps(significance, ensure_ascii=False, indent=2), encoding="utf-8")

    config = {
        "development_cohort": "13회차 변호사시험",
        "held_out_test_cohort": "14회차 변호사시험",
        "n_dev": int(len(dev_idx)),
        "n_test": int(len(test_idx)),
        "best_C_retrieval": best_c_base,
        "best_C_ontology": best_c_full,
        "n_pair_rows_retrieval": n_base_pairs,
        "n_pair_rows_ontology": n_full_pairs,
        "base_features": base_labels,
        "ontology_features": ontology_labels,
        "dense_model": MODEL_NAME,
        "seed": SEED,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "timings": timings,
        "elapsed_total_s": time.time() - started,
    }
    (RESULT_DIR / "ltr_run_metadata.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(config, ensure_ascii=False, indent=2))
    print("\nHeld-out test results")
    print(test_metrics.to_string(index=False))
    print("\nOntology feature significance")
    print(json.dumps(significance, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
