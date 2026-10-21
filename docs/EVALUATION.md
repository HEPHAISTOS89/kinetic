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

## 4. Results so far (four blind A/B rounds, four briefs, five comparisons, twelve critic reads)
| Round | Brief | Stack | Arms | Critics | Pooled judged mean (baseline / Kinetic) | Measured findings (baseline / Kinetic) |
|---|---|---|---|---|---|---|
| 1 | Courant (transit) | SwiftUI | model vs Kinetic v1.0 | 2 | 3.67 / 3.78 | 3 major / 0 |
| 2 | Courant (transit) | SwiftUI | model vs Kinetic v1.1 | 2 | 3.78 / 3.56 | 3 major / 0 |
| 3 | Tally (shared money) | SwiftUI | model + critic vs Kinetic v1.3 + Kinetic critic | 2 | 3.83 / 3.83 | 1 F + 6 D / 0 |
| 4a | Prise (bouldering gym) | Flutter | model vs Kinetic v1.4 | 3 | 4.26 / 4.22 | 5 F (reduce-motion, 4 empty handlers) + 6 D / 1 minor |
| 4b | Petit Jour (daycare, French UI) | React Native | model vs Kinetic v1.4 | 3 | 3.81 / 3.96 | 1 F (reduce-motion) + 8 D / 0 |

Round 4 verdicts: Prise — Kinetic slight, tie, baseline slight; Petit Jour — Kinetic slight, tie, tie.
Per dimension, the six critics agreed completely (round-4 means, baseline → Kinetic):
- **Kinetic ahead**: anticipation (Prise 4.0 → 5.0, Petit Jour 3.7 → 4.7: loading, unreachable server,
  queued offline actions, true XXL, an in-session mode), native fidelity (3.0 → 4.0 on both: platform
  chrome rendered per OS), product fit on Prise (4.0 → 5.0), layout craft on Petit Jour.
- **Baseline ahead**: distinctiveness in **6 of 6** reads (Prise 5.0 → 4.0, Petit Jour 4.0 → 3.0),
  hierarchy on Prise (a display-size verdict sentence, "Busy, not packed.", over a numeral), and the
  frightening moment on Petit Jour (fever alert as an event with the missed call and the number).

Honest reading:
- On blind judged design quality, Kinetic **matches** a strong frontier model (pooled over the 12 reads:
  baseline 3.90, Kinetic 3.91); it does not beat it. Every gap is inside critic variance.
- The **trade is stable across 4 briefs and 3 stacks**: Kinetic is more complete, more native and more
  rigorous; the bare model is more distinctive. The v1.4 identity floor ("at least one ownable element")
  did **not** close the gap. Round 4 shows why: the winning designs build a drawn *vocabulary* from the
  domain's real material (holds, tape, tally marks, pegboard; moon/sun/house per child state) and use it in
  place of generic parts, where Kinetic asked for one signature detail. v1.5 rewrites the rule accordingly
  (kinetic-direct §4b: domain vocabulary, ownable-hero gate) and adds verdict-first heroes, high-stakes
  moment rules and craft checks — **not yet re-measured**.
- Measured rigor: the baselines shipped real defects in every round (3 major D findings in rounds 1–2,
  no reduce-motion path in rounds 3 and 4, four `onTap: () {}` handlers in round 4); Kinetic arms shipped none. Caveat unchanged: the engine is
  Kinetic's own and the arms could run it, so this gap is partly by construction.
- Self-critique calibration improved: round-4 self-judged means were within 0.1 of the critics' (4.11 vs
  4.22; 4.0 vs 3.96), but self-judged distinctiveness was still +1 on Petit Jour. `ship` still requires an
  independent critic.
- The round-4 arms also found 20 engine/knowledge issues (false positives on data palettes and theme
  accessors, an RN export that failed strict TypeScript, no place for accepted exceptions…); all fixed
  in v1.5 with regression tests.

Next evaluation step: re-run two briefs with v1.5 against the same baselines (renders already archived)
to test the vocabulary rule on distinctiveness specifically, with ≥ 3 critics.
