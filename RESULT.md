# Result: partially replicates (baseline row only; headline fusion number not yet run)

Paper: Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval, arXiv 2606.04194. Repo Chrislysen/opsem, commit 68186a45882dd85ea66fcc70ee38ba28f6de9a90.

Claim (paper.tex, checked against the source): on LoCoMo (n=1978), e5-large-v2, BM25 Hit@1 0.640, dense max-sim 0.664, BM25 + max-sim fusion Hit@1 0.752, NDCG@5 0.829.

Scope for this attempt: the e5-large-v2 row only. The "+8.8 to +17.2 pp across six encoders" range was not attempted.

| Quantity | Paper | Mine | Difference |
|---|---|---|---|
| BM25 Hit@1 | 0.640 | not produced | n/a |
| max-sim Hit@1 | 0.664 | not produced | n/a |
| fusion Hit@1 | 0.752 | not produced | n/a |
| fusion NDCG@5 | 0.829 | not produced | n/a |

Verdict: could not be run.

What happened: the LoCoMo file was verified (2805274 bytes, sha256 79fa87e90f04081343b8c8debecb80a9a6842b76a7aa537dc9fdf651ea698ff4, identical to a fresh download from snap-research/locomo, 10 conversations, 5882 turns). I ran
`HF_HOME=.hf python embed_turns_multi.py intfloat/e5-large-v2 "query: " "passage: "` from upstream/opsem. A 200-turn timing predicted 92.6 min; the full run, sharing the CPU with other jobs, did 788 of 5882 turns in about 30 min (about 26 turns/min), projecting about 3.8 h total. That exceeds the 2 h limit, so I stopped it without subsampling. The script saves embeddings only at the end, so nothing was kept. No evaluation script was executed.

Not verified: all four numbers, and determinism.
What this does not show: nothing about whether the paper's numbers are right or wrong.

To resume: run the same command on an idle CPU (about 1.5 to 2 h at the 200-turn rate, longer if shared), then `python tune13_interaction.py` and `python tune13b_fusion_vs_late.py` with the ENCODERS edit in upstream_changes.patch applied. Needs about 1.3 GB for the model cache plus the 0.7 GB venv.

## Partial result, 2026-11-18: the BM25 row replicates

The BM25 baseline needs no encoder, so it was run on its own with the authors' tokenizer, scorer and metric functions imported unchanged (`tools/bm25_row.py` repeats the BM25 half of upstream `tune13_interaction.build_signals`).

| row (LoCoMo, session-level gold) | paper | here | difference |
|---|---|---|---|
| examples | 1978 | 1978 | 0 |
| BM25 Hit@1 | 0.640 | 0.6395 | -0.0005 (rounds to the paper's figure) |
| dense max-sim Hit@1, e5-large-v2 | 0.664 | not run | - |
| BM25 + max-sim fusion Hit@1 | 0.752 | not run | - |
| fusion NDCG@5 | 0.829 | not run | - |

Command: `.venv/Scripts/python.exe tools/bm25_row.py`. Run twice, byte-identical output (`runs/bm25_row_1.log`, `runs/bm25_row_2.log`). Within the 1-point tolerance set in PLAN.md.

Verdict so far: **partially replicates** - the baseline row and the example count match; the headline fusion number is still unrun (encoder embedding did not fit the CPU budget while another job held the machine). This says nothing yet about the claim the paper is about.

### Second route to the same row

`tools/bm25_second_route.py` uses none of the authors' code: its own LoCoMo parse, its own tokenizer (lowercase word characters) and textbook Okapi BM25 (k1 1.5, b 0.75). Result: Hit@1 0.6332 on 1,982 questions (`runs/bm25_second_route.log`), against 0.6395 on 1,978 through the authors' functions and 0.640 in the paper. The 0.6-point gap and the 4 extra questions come from tokenizer and gold-filter differences that were not traced further. The baseline row does not depend on anything particular to the authors' loader or scorer.

Deviations from the paper's setup for the rows run so far: none for `tools/bm25_row.py` (authors' functions, same data file, sha256 in PLAN.md); library versions are whatever `requirements.lock.txt` records, not the authors' unpinned environment.
