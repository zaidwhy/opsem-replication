# Deviations from the authors' code

One change to the authors' code was needed for the run reported in RESULT.md.

1. upstream/opsem/tune13_interaction.py : ENCODERS list cut to e5-large-v2 only, because the evaluator crashes on the bge-base entry when its caches (locomo_turn_cache.npz) are absent and the scope was cut to one encoder. Diff in upstream_changes.patch (5 deleted lines). Could not change the number: it only removes encoders from the loop.
2. Library versions are today's pip resolution (requirements.lock.txt), unpinned by the authors.
3. Timing helper tools/time200.py is mine, not the authors'.
