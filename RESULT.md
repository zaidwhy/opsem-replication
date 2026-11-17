# Result: could not be run

Paper: Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval (arXiv 2606.04194), repo Chrislysen/opsem at 68186a45882dd85ea66fcc70ee38ba28f6de9a90.

Claim (paper.tex, abstract and Table of fusion results): BM25 + max-sim fusion reaches LoCoMo Hit@1 0.752 with e5-large-v2 (BM25 0.640, max-sim 0.664), +8.8 to +17.2 pp over late interaction alone across six encoders.

| Quantity | Paper | Mine | Difference |
|---|---|---|---|
| e5-large-v2 fusion Hit@1 | 0.752 | not produced | n/a |

Verdict: could not be run.

Why: the 6 GB free-disk floor set for this task was crossed. C: had 12G free at start, 2.7G after installing CPU torch, and 288M minutes later, with other jobs consuming the space. Encoder weights (e5-large-v2 is about 1.3 GB) were never downloaded and no embedding or evaluation script was executed. No number was produced.

What was done: paper and code verified to exist (arXiv abs/HTML fetched; headline numbers cross-checked against upstream/opsem/paper/paper.tex), LoCoMo licence checked (CC BY-NC 4.0), plan committed, repo cloned, venv created with CPU torch 2.15.0 and numpy 2.5.5 (Python 3.14.6).

Not verified: everything about replication. Also not done: DEVIATIONS.md (no changes made to upstream code), determinism run, requirements.lock.txt (install unfinished).

What this does not show: nothing about whether the paper's numbers are right or wrong.

To resume once at least 6 GB is free: finish `pip install sentence-transformers scipy matplotlib datasets` in .venv, place locomo10.json at upstream/opsem/data/locomo/, run embed_locomo.py, embed_turns.py, embed_turns_multi.py for the other five encoders with their prefixes (e5: "query: " / "passage: "), then tune13_interaction.py and tune13b_fusion_vs_late.py.
