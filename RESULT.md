# Result: replicates

Paper: Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval, arXiv 2606.04194. Repo Chrislysen/opsem, commit 68186a45882dd85ea66fcc70ee38ba28f6de9a90.

Claim (paper.tex, checked against the source): on LoCoMo (n=1978), e5-large-v2, BM25 Hit@1 0.640, dense max-sim 0.664, BM25 + max-sim fusion Hit@1 0.752, NDCG@5 0.829.

Scope: the e5-large-v2 row only. The "+8.8 to +17.2 pp across six encoders" range was not attempted.

| Quantity (LoCoMo, session-level gold, n = 1978) | Paper | Here | Difference |
|---|---|---|---|
| BM25 Hit@1 | 0.640 | 0.6395 | -0.0005 |
| dense max-sim Hit@1, e5-large-v2 | 0.664 | 0.6638 | -0.0002 |
| BM25 + max-sim fusion Hit@1 | 0.752 | 0.7518 | -0.0002 |
| fusion NDCG@5 | 0.829 | 0.8292 | +0.0002 |
| fusion over max-sim alone | +8.8 pp | +8.80 pp, 95% interval [+6.52, +11.21] | 0 |

**Verdict: replicates.** All four numbers round to the paper's figures, inside the 1-point tolerance fixed in PLAN.md before any run. The fusion gain over the dense scorer alone is positive with an interval clear of zero (conversation-cluster bootstrap, 4,000 resamples, the authors' code).

How it was run (2026-11-18, from `upstream/opsem`, CPU, torch 2.15.0+cpu, versions in `requirements.lock.txt`):

```
HF_HOME=.hf python embed_turns_multi.py intfloat/e5-large-v2 "query: " "passage: "
python tune13_interaction.py          # with upstream_changes.patch applied
python tune13b_fusion_vs_late.py
```

The two evaluators were each run twice on the one embedding cache. Every point value is identical across the two runs (`runs/results/tune13_run1.md` and `tune13_run2.md` are byte-identical). The bootstrap interval is not seeded upstream and moves in the second decimal: [+6.52, +11.21] and [+6.58, +11.36] here, [+6.62, +11.19] in the authors' committed output. Logs: `runs/embed_e5_large_run2.log`, `runs/tune13_interaction_{1,2}.log`, `runs/tune13b_{1,2}.log`.

The e5-large-v2 rows of the authors' committed result file (`results/tune13-interaction-20260601T170200/tune13.md`) match this run to all four decimals in every column.

Deviations (full list in DEVIATIONS.md): the evaluator's encoder list was cut to e5-large-v2 because the other five caches were not built; nothing else in the authors' code was changed.

What this does not show:
- Nothing about the other five encoders, the LongMemEval results, the end-to-end QA numbers or the latency claims.
- The embedding was computed once. Embedding determinism across machines was not tested; the evaluators were repeated, the encoder pass was not.
- It is a reproduction with the authors' code and data, so it confirms the number follows from the released artefacts, not that the method generalises. The fusion weight is chosen by leave-one-conversation-out on the same 10 conversations.
- The authors' gold parser drops 4 questions whose evidence field holds several references in one string (1,978 against 1,982); all four are BM25 misses in the independent route below, so the effect on Hit@1 is under 0.2 points.
- An earlier attempt the same night stopped at 788 of 5,882 turns because the CPU was shared; no number came from it.

## Earlier partial result, 2026-11-18: the BM25 row alone

The BM25 baseline needs no encoder, so it was run on its own with the authors' tokenizer, scorer and metric functions imported unchanged (`tools/bm25_row.py` repeats the BM25 half of upstream `tune13_interaction.build_signals`).

| row (LoCoMo, session-level gold) | paper | here | difference |
|---|---|---|---|
| examples | 1978 | 1978 | 0 |
| BM25 Hit@1 | 0.640 | 0.6395 | -0.0005 (rounds to the paper's figure) |
| dense max-sim Hit@1, e5-large-v2 | 0.664 | not run | - |
| BM25 + max-sim fusion Hit@1 | 0.752 | not run | - |
| fusion NDCG@5 | 0.829 | not run | - |

Command: `.venv/Scripts/python.exe tools/bm25_row.py`. Run twice, byte-identical output (`runs/bm25_row_1.log`, `runs/bm25_row_2.log`). Within the 1-point tolerance set in PLAN.md.

At that point only the baseline row and the example count were confirmed; the table at the top of this file has the full row.

### Second route to the same row

`tools/bm25_second_route.py` uses none of the authors' code: its own LoCoMo parse, its own tokenizer (lowercase word characters) and textbook Okapi BM25 (k1 1.5, b 0.75). Result: Hit@1 0.6332 on 1,982 questions (`runs/bm25_second_route.log`), against 0.6395 on 1,978 through the authors' functions and 0.640 in the paper. The 4 extra questions are traced: the authors' parser matches each evidence entry with an anchored pattern and drops entries that hold several references in one string (conversation 0 question 37; conversation 8 questions 31, 38, 46). The rest of the 0.6-point gap is attributed to the tokenizer and was not isolated here. The baseline row does not depend on anything particular to the authors' loader or scorer.

Deviations from the paper's setup for the rows run so far: none for `tools/bm25_row.py` (authors' functions, same data file, sha256 in PLAN.md); library versions are whatever `requirements.lock.txt` records, not the authors' unpinned environment.
