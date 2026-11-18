## tune13b: does BM25 fusion add OVER late-interaction (max-sim) alone? (LoCoMo)

n_eval = 1978, 10 conversations, conversation-cluster bootstrap (n_boot=4000). Dense term fixed at max-sim; only BM25 fusion (LOCO-CV α) added.

| encoder | dense max-sim Hit@1 | +BM25 fusion Hit@1 | Δ pp | 95% CI | p |
|---|---|---|---|---|---|
| e5-large-v2 | 0.6638 | 0.7518 | +8.80 | [+6.58, +11.36] | 0.0000 |

Raw: `tune13b.json`.
