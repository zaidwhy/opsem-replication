# opsem replication

A one-session attempt to reproduce the headline number of *Training-Free Lexical-Dense Fusion for
Conversational-Memory Retrieval* (Christian Lysenstoen, [arXiv 2606.04194](https://arxiv.org/abs/2606.04194),
code at [Chrislysen/opsem](https://github.com/Chrislysen/opsem), commit `68186a45`).

**Verdict: it replicates.** The tolerance (1 point of Hit@1) was written into `PLAN.md` before any run.

| LoCoMo, session-level gold, n = 1978, e5-large-v2 | Paper | Here |
|---|---|---|
| BM25 Hit@1 | 0.640 | 0.6395 |
| Dense max-sim Hit@1 | 0.664 | 0.6638 |
| BM25 + max-sim fusion Hit@1 | 0.752 | 0.7518 |
| Fusion NDCG@5 | 0.829 | 0.8292 |
| Fusion over max-sim alone | +8.8 pp | +8.80 pp, 95% interval [+6.52, +11.21] |

The full write-up, with what was and was not checked, is [`RESULT.md`](RESULT.md).

## What was run

The authors' code, unchanged except for one edit: the evaluator's encoder list was cut to
e5-large-v2, because the other five encoders were out of scope (`upstream_changes.patch`,
`DEVIATIONS.md`). CPU only, library versions in `requirements.lock.txt`.

```
git clone https://github.com/Chrislysen/opsem upstream/opsem
cd upstream/opsem && git checkout 68186a45 && git apply ../../upstream_changes.patch
# place LoCoMo's locomo10.json at data/locomo/ (sha256 79fa87e9...ea698ff4, from snap-research/locomo)
python embed_turns_multi.py intfloat/e5-large-v2 "query: " "passage: "
python tune13_interaction.py
python tune13b_fusion_vs_late.py
```

The two evaluators were run twice on one embedding cache; every point value is identical across
runs. Logs and result tables are in `runs/`.

## A second route to the baseline

`tools/bm25_second_route.py` uses none of the authors' code: its own LoCoMo parse, a plain
word tokenizer and textbook Okapi BM25. It gets Hit@1 0.6332 on 1,982 questions against 0.6395 on
1,978. Part of the gap is traced: the authors' gold parser matches each evidence entry with an anchored
pattern, so it drops 4 questions whose evidence field holds several references in one string
(conversation 0 question 37; conversation 8 questions 31, 38 and 46). The rest is attributed to
the tokenizer (theirs removes stopwords and short tokens) and was not isolated here. Neither
changes the verdict.

## What this does not show

- Only the e5-large-v2 row. The other five encoders, the LongMemEval table, the reranking table,
  the end-to-end QA numbers and the latency claims were not attempted.
- A reproduction with the authors' code and data confirms the number follows from the released
  artefacts. It does not test whether the method holds on other data; the fusion weight is chosen
  by leave-one-conversation-out on the same 10 conversations.
- The embedding pass was computed once, on one machine.

## Licences

Code in this repository is MIT. The opsem code is MIT and is not copied here. LoCoMo is
CC BY-NC 4.0 and is not redistributed here.
