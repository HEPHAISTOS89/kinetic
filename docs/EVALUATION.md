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

## 4. Results so far (three blind A/B rounds, six independent critics)
| Round | Brief | Arms | Pooled judged mean (baseline / Kinetic) | Measured findings (baseline / Kinetic) |
|---|---|---|---|---|
| 1 | Courant (transit) | model vs Kinetic v1.0 | 3.67 / 3.78 | 3 major / 0 |
| 2 | Courant (transit) | model vs Kinetic v1.1 | 3.78 / 3.56 | 3 major / 0 |
| 3 | Tally (shared money) | model + critic vs Kinetic v1.3 + Kinetic critic | 3.83 / 3.83 | 1 F + 6 D / 0 |

Honest reading:
- On blind judged design quality, Kinetic currently **matches** a strong frontier model; it does not beat it.
  Differences are within critic variance: in two of three rounds the two critics picked different winners.
- Kinetic **robustly** wins on what the engine measures (system coherence, grid, contrast, reduce-motion,
  state coverage: 0 findings in every round) and on copy/tone faithful to the brief.
- Its recurring weakness was identity, traced to our own guidance favouring quiet system typography; fixed in v1.4
  but **not yet re-measured**.
- Self-critique was more lenient than independent critics every time (+0.3 to +0.6): `ship` therefore requires an
  independent critic.
- Each round's arm feedback produced concrete engine and knowledge fixes (logged in each round's folder).

Next evaluation step: ≥3 new briefs across sectors and stacks, ≥3 critics each, to separate signal from variance.
