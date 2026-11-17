"""The paper's BM25 row on LoCoMo, with the authors' own tokenizer, scorer and metric code.

It repeats the BM25 half of upstream `tune13_interaction.build_signals` and nothing else, so it
needs no encoder. Usage: python tools/bm25_row.py   (from the repo root, inside .venv)
"""

import sys
from pathlib import Path

import numpy as np

UPSTREAM = Path(__file__).resolve().parents[1] / "upstream" / "opsem"
sys.path.insert(0, str(UPSTREAM))

import locomo  # noqa: E402
from tune7_bm25 import ConvStats, _tokenize_text, score_classic  # noqa: E402
from tune13_interaction import LOCOMO, METRIC_KEYS, metrics_from_scores  # noqa: E402

examples = [e for e in locomo.iter_examples(LOCOMO) if e["gold_session_ids"]]
stats, per_example = {}, []
for e in examples:
    conv = e["conv_idx"]
    if conv not in stats:
        stats[conv] = ConvStats([_tokenize_text(s) for s in e["haystack_sessions"]])
    scores = score_classic(stats[conv], set(_tokenize_text(e["question"])), 1.5, 0.75)
    position = {s: j for j, s in enumerate(e["session_ids"])}
    gold = {position[g] for g in e["gold_session_ids"] if g in position}
    per_example.append(metrics_from_scores(np.asarray(scores, float), gold))

print(f"examples {len(examples)} conversations {len(stats)}")
for key in METRIC_KEYS:
    print(f"BM25 {key} {np.mean([m[key] for m in per_example]):.4f}")
