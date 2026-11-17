"""Second route to the BM25 row: none of the authors' code.

Own LoCoMo parse (sessions from `session_N`, gold sessions from the `D<session>:<turn>` evidence ids),
own tokenizer (lowercase word characters) and textbook Okapi BM25 (k1 1.5, b 0.75, query terms as a set).
If the authors' 0.640 depended on something particular to their loader or scorer, this would not land near it.
Usage: python tools/bm25_second_route.py
"""

import json
import math
import re
from collections import Counter
from pathlib import Path

LOCOMO = Path(__file__).resolve().parents[1] / "upstream" / "opsem" / "data" / "locomo" / "locomo10.json"
K1, B = 1.5, 0.75


def words(text):
    return re.findall(r"\w+", text.lower())


def sessions_of(conversation):
    """session number -> the session as one string, in the file's order."""
    numbers = sorted(int(k.split("_")[1]) for k, v in conversation.items()
                     if re.fullmatch(r"session_\d+", k) and isinstance(v, list))
    return {n: " ".join(f"{t.get('speaker', '')}: {t.get('text', '')}" for t in conversation[f"session_{n}"])
            for n in numbers}


def bm25_scores(docs, query_terms):
    lengths = [len(d) for d in docs]
    mean_length = sum(lengths) / len(docs)
    counts = [Counter(d) for d in docs]
    scores = [0.0] * len(docs)
    for term in query_terms:
        df = sum(1 for c in counts if term in c)
        if not df:
            continue
        idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
        for i, c in enumerate(counts):
            tf = c[term]
            if tf:
                scores[i] += idf * tf * (K1 + 1) / (tf + K1 * (1 - B + B * lengths[i] / mean_length))
    return scores


hits = total = skipped = 0
for sample in json.loads(LOCOMO.read_text(encoding="utf-8")):
    sessions = sessions_of(sample["conversation"])
    order = list(sessions)
    docs = [words(sessions[n]) for n in order]
    for qa in sample["qa"]:
        gold = {int(m.group(1)) for e in qa.get("evidence", []) for m in re.finditer(r"D(\d+):\d+", str(e))}
        gold &= set(order)
        if not gold:
            skipped += 1
            continue
        scores = bm25_scores(docs, set(words(str(qa["question"]))))
        best = max(range(len(docs)), key=lambda i: (scores[i], -i))
        hits += order[best] in gold
        total += 1

print(f"questions with gold {total}, without {skipped}")
print(f"BM25 hit@1 {hits / total:.4f}")
