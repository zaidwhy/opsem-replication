# Replication plan

Written and committed before any experiment script was run (environment setup and data download came first; no embedding or evaluation had been executed when this was committed).

## Paper
- Title: Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval
- Author: Christian Lysenstoen (single author)
- arXiv: 2606.04194 (v1, submitted 2 June 2026). Abstract page and HTML version (arxiv.org/html/2606.04194) were fetched; the tables below came from the HTML version via a fetch tool summary and must be re-checked against the paper PDF in `upstream/opsem/paper/paper.pdf` (done before RESULT.md is written).
- Repo: https://github.com/Chrislysen/opsem (MIT, 2 stars at time of check)
- Commit cloned: 68186a45882dd85ea66fcc70ee38ba28f6de9a90 (2 June 2026)

## Candidates considered (3)
1. opsem / arXiv 2606.04194 (chosen). Retrieval only, CPU only, no LLM, LoCoMo + small encoders, ships result receipts. Feasible. Downside: obscure (2 stars).
2. ConvMemory, arXiv 2605.28062. No code repo found on the abstract page; author says numbers are single-seed. Infeasible as a replication.
3. rohitg00/agentmemory LongMemEval-S retrieval file (all-MiniLM-L6-v2, R@5 95.2 hybrid). Not a paper, vendor self-report; would be a repo claim, not a paper claim. Not chosen.
Also seen and rejected: arXiv 2605.04897 (vendor report, needs LLM reader for headline), Hindsight 2512.12818 (2025, LLM), memory-probe 2603.02473 (LLM answers), MemMachine 2604.04853 (GPT-5-mini).

## Headline claim (README "Headline result" and paper abstract)
"fusion adds +8.8 to +17.2 points of LoCoMo Hit@1 over late interaction alone across six encoders". Deployable recipe: e5-large-v2, BM25 + max-sim fusion, LoCoMo Hit@1 0.752 (NDCG@5 0.829), versus BM25 0.640, dense mean-pool 0.427, dense max-sim 0.664 (same encoder). n = 1978 QA examples, session-level gold, leave-one-conversation-out alpha.

## Numbers to reproduce
Primary: e5-large-v2 on LoCoMo: Hit@1 of BM25 (0.640), mean-pool (0.427), max-sim (0.664), BM25+max-sim fusion (0.752); fusion NDCG@5 0.829.
Secondary: fusion Hit@1 for the other five encoders (gte-base 0.691, bge-base 0.699, e5-base-v2 0.702, mxbai-large 0.713, bge-large 0.721) and the fusion-minus-max-sim delta range (+8.8 to +17.2 pp).
Not attempted: LongMemEval-S table, cross-encoder reranking table, e2e QA (needs a paid LLM API).

## Method
Authors' scripts, unmodified where possible: `embed_locomo.py`, `embed_turns.py` (bge-base), `embed_turns_multi.py <model> <qpref> <ppref>` (others), `tune13_interaction.py`, `tune13b_fusion_vs_late.py`. Data: LoCoMo `locomo10.json` from snap-research/locomo (licence CC BY-NC 4.0, non-commercial research use; this is non-commercial, local-only, not redistributed). Encoder weights from the Hugging Face Hub. To fit the 3 GB budget, each encoder's HF cache is deleted after its embeddings are cached.

## Tolerance
Deterministic retrieval metric on the full 1978-question set with the authors' scoring code: replicates if each Hit@1 is within 1.0 absolute point of the paper (0.010). The bootstrap CIs/p-values are seeded via Python `hash()` (randomised per process), so they are not compared exactly; only their sign and rough magnitude. The range claim replicates if every delta over max-sim is positive and within 1 point of the quoted endpoints.
"Does not replicate": primary fusion Hit@1 differs by more than 2 points, or fusion fails to beat max-sim alone for any encoder, or the ordering BM25 < max-sim < fusion changes.
Between 1 and 2 points: "partially replicates".

## Known deviations
- CPU torch, library versions are whatever pip resolves today (recorded in requirements.lock.txt); authors did not pin versions. Embeddings can differ slightly across versions/hardware.
- Batch size is the authors' (64); no change.
- Set HF_HOME inside the project and delete model caches after use.
- If a script needs changes to run, each goes in DEVIATIONS.md.

## Run plan
Run the headline pipeline twice (second run from freshly rebuilt embeddings for e5-large-v2, plus a rerun of the evaluation scripts for all) to check determinism.

## Change log
(none yet)

## Change log
- 2026-11-18: Stopped before running any experiment. Free space on C: was 12G at start, 2.7G after the CPU torch install (venv about 0.7G, pip cache about 0.13G, i.e. under 1G is mine), then 288M a few minutes later. The brief says stop if free space would drop under 6G. The drop is from other jobs on the machine, not from this task. No encoder weights were downloaded. The pending `pip install sentence-transformers ...` was still running at that point and may leave a partial venv.
