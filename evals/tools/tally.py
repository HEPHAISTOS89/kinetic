"""Unblind and average a round: tally.py <round_dir>. Reads results/<brief>-cN.json and keys/<brief>_key.json."""
import glob, json, os, statistics as st, sys
from collections import defaultdict
root = sys.argv[1]
DIMS = "product_fit hierarchy distinctiveness typography color layout_craft native_fidelity anticipation copy".split()
pooled = defaultdict(list)
for keyf in sorted(glob.glob(os.path.join(root, "keys", "*_key.json"))):
    brief = os.path.basename(keyf)[:-9]
    key = json.load(open(keyf))
    files = sorted(glob.glob(os.path.join(root, "results", f"{brief}-c*.json")))
    if not files:
        continue
    print("==", brief)
    for arm in sorted(set(key.values())):
        L = [l for l, a in key.items() if a == arm][0]
        reads = [json.load(open(f)) for f in files]
        means = [round(st.mean(r[L]["scores"]), 2) for r in reads]
        ranks = [r["ranking"].index(L) + 1 for r in reads]
        clean = round(st.mean(r[L]["clean"] for r in reads), 2)
        dims = [round(st.mean(r[L]["scores"][i] for r in reads), 2) for i in range(len(DIMS))]
        pooled[arm] += means
        print(f"  {arm}: mean {round(st.mean(means), 2)} {means}  clean {clean}  ranks {ranks}")
        print("     " + "  ".join(f"{d[:5]} {v:.2f}" for d, v in zip(DIMS, dims)))
for arm, v in pooled.items():
    print(f"pooled {arm}: {round(st.mean(v), 2)}")
