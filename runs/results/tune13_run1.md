## tune13: the lever is the INTERACTION FUNCTION, not the unit (LoCoMo)

n_eval = 1978 across 10 conversations. Retrieval unit is held fixed at *session*; only the query<->session scoring operator varies, over the SAME cached turn vectors. Field-standard metrics; conversation-cluster bootstrap (n_boot=4000). CPU, no training.

BM25 baseline: hit@1 0.6395, recall@3 0.7788, recall@5 0.8325, mrr 0.7504, ndcg@5 0.7456

### Dense-alone: early (mean-pool) vs late (max-sim) interaction

| encoder | pooler | Hit@1 | R@3 | R@5 | MRR | NDCG@5 |
|---|---|---|---|---|---|---|
| e5-large-v2 | mean(early) | 0.4267 | 0.6006 | 0.7125 | 0.5760 | 0.5732 |
| e5-large-v2 | max-sim(late) | 0.6638 | 0.7919 | 0.8631 | 0.7669 | 0.7694 |
| e5-large-v2 | top3(late) | 0.6365 | 0.7786 | 0.8471 | 0.7478 | 0.7483 |
| e5-large-v2 | lse10(late) | 0.1269 | 0.2781 | 0.3842 | 0.2870 | 0.2573 |

### BM25-fused (LOCO-CV alpha): same pooler sweep

| encoder | pooler | Hit@1 | R@3 | R@5 | MRR | NDCG@5 |
|---|---|---|---|---|---|---|
| e5-large-v2 | mean(early) | 0.6658 | 0.7967 | 0.8512 | 0.7722 | 0.7656 |
| e5-large-v2 | max-sim(late) | 0.7518 | 0.8464 | 0.8943 | 0.8347 | 0.8292 |
| e5-large-v2 | top3(late) | 0.7240 | 0.8293 | 0.8905 | 0.8148 | 0.8125 |
| e5-large-v2 | lse10(late) | 0.6461 | 0.7790 | 0.8439 | 0.7556 | 0.7528 |

### The control contrast: late minus early interaction
(identical turn vectors; only the pooling operator differs)

| encoder | dense Δ(late-early) pp | p | fusion Δ(late-early) pp | p | fusion-late vs BM25 pp | p |
|---|---|---|---|---|---|---|
| e5-large-v2 | +23.71 | 0.0000 | +8.59 | 0.0000 | +11.22 | 0.0000 |

Raw: `tune13.json`.
