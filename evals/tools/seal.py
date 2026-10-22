"""Seal one brief's arms into blind folders: seal.py <round_dir> <brief> <arm,arm,arm>.
Copies each arm's shots/*.png into <brief>/judge/blind/{X,Y,Z} in random order and writes keys/<brief>_key.json."""
import json, os, random, shutil, sys
root, brief, arms = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
random.shuffle(arms)
blind = os.path.join(root, brief, 'judge', 'blind')
shutil.rmtree(blind, ignore_errors=True)
for label, arm in zip('XYZ', arms):
    dst = os.path.join(blind, label)
    os.makedirs(dst)
    src = os.path.join(root, brief, arm, 'shots')
    for f in sorted(os.listdir(src)):
        if f.endswith('.png'):
            shutil.copy(os.path.join(src, f), dst)
    print(label, len(os.listdir(dst)), 'images')
os.makedirs(os.path.join(root, 'keys'), exist_ok=True)
json.dump(dict(zip('XYZ', arms)), open(os.path.join(root, 'keys', f'{brief}_key.json'), 'w'))
