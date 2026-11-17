import json, sys, time
from sentence_transformers import SentenceTransformer
d = json.load(open("upstream/opsem/data/locomo/locomo10.json", encoding="utf-8"))
n = 0; texts = []
for rec in d:
    c = rec["conversation"]
    for k in c:
        if k.startswith("session_") and not k.endswith("_date_time"):
            texts += ["passage: " + f"{t.get('speaker','?')}: {t.get('text','') or ''}" for t in c[k]]
print("total turns", len(texts), flush=True)
m = SentenceTransformer("intfloat/e5-large-v2")
t = time.time(); m.encode(texts[:200], batch_size=64, show_progress_bar=False); dt = time.time() - t
print(f"200 turns {dt:.1f}s -> est total {dt/200*len(texts)/60:.1f} min", flush=True)
