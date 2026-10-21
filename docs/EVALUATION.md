# Evaluating Kinetic

Three proof layers, each with its own limits. None alone certifies design quality.

## 1. Engine correctness (automated)
`python3 -m unittest discover -s tests -v` (add `KINETIC_SLOW=1` to compile
Flutter exports). Covers the KDL parser (structures, errors, line numbers),
color science against APCA/WCAG reference values, role derivation for 12
seeds, validator on a golden record and a slop record, scanner on slop
fixtures for Flutter / SwiftUI / Compose / React Native and on a clean
fixture (no false positives), DNA proposal, exports compiled with
`swiftc` (iOS + macOS), `tsc` and `flutter analyze`, the SVG linter on
hand-built icons and hostile files (XXE), state matrices, score gates, CLI
exit codes and non-destructive writes, and the edit hook.

## 2. Discoverability (manual, per host)
`evals/triggers.json` lists direct, broad and negative prompts. Run each in a
fresh session with the plugin installed; record host, model, selected skill,
errors and outcome. Keyword overlap in descriptions does not prove selection.

## 3. Design outcome (A/B)
Protocol used for v1 (`evals/ab-courant/`):
1. One brief (`BRIEF.md`), one stack (SwiftUI), one render harness
   (`harness/Render.swift`: every gallery state at 393×852pt, light and dark).
2. Arm A: the same model with no design plugin and no skills. Arm B: the same
   model following Kinetic. Both can render and iterate as much as they like.
3. Measured: `kinetic scan` on both outputs (same command, same config).
4. Judged: the `kinetic-critic` rubric applied **blind** — the critic gets the
   brief and renders labelled X/Y in random order, never the arm names or the
   KDL, so the record cannot bias it toward Kinetic.
5. Report per-dimension scores with evidence, the measured findings, the time
   and the feedback the Kinetic arm logged about the plugin.
Limits: N = 1 brief, one model, one critic; macOS `ImageRenderer` cannot show
Dynamic Type scaling (XXL needs the iOS Simulator); a blind critic is still a
model. Treat a result as evidence about this brief, not a universal ranking.
