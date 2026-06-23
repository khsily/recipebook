# Korean Legal QA Evidence-Retrieval Experiment

This isolated research directory reproduces a closed-corpus evidence-precedent retrieval study on the public KCL-MCQA benchmark. It does not modify the application code in the surrounding repository.

Run:

```bash
python -m pip install -r research/ontology_korean_qa/requirements.txt
python research/ontology_korean_qa/run_experiment.py
```

The script downloads `lbox/kcl` (`kcl_mcqa`, test split), constructs a deduplicated precedent corpus, evaluates lexical, dense, hybrid, and ontology-enhanced retrieval, and writes aggregate, per-query, ablation, robustness, significance, and provenance files under `results/`.

KCL data are not redistributed. KCL is licensed CC BY-NC 4.0; use the upstream dataset and citation provided by its authors.
