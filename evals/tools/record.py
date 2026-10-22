"""Record one blind critic: record.py <round_dir> <brief-cN> "X 9 scores" "Y 9" "Z 9" "cleanX cleanY cleanZ" "rank1 rank2 rank3".
Scores in rubric order: product_fit hierarchy distinctiveness typography color layout_craft native_fidelity anticipation copy."""
import json, os, sys
root, name, x, y, z, cl, rk = sys.argv[1:8]
c = [int(v) for v in cl.split()]
out = {L: {"scores": [int(v) for v in s.split()], "clean": c[i]} for i, (L, s) in enumerate(zip("XYZ", (x, y, z)))}
out["ranking"] = rk.split()
os.makedirs(os.path.join(root, "results"), exist_ok=True)
json.dump(out, open(os.path.join(root, "results", name + ".json"), "w"))
