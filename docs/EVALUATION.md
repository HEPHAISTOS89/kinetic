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

## 4. Results so far (six blind rounds, eight briefs, 30 critic reads)
| Round | Brief | Stack | Arms | Critics | Judged mean (baseline / Kinetic) | Clean (baseline / Kinetic) | Verdicts |
|---|---|---|---|---|---|---|---|
| 1 | Courant (transit) | SwiftUI | model vs v1.0 | 2 | 3.67 / 3.78 | — | split |
| 2 | Courant (transit) | SwiftUI | model vs v1.1 | 2 | 3.78 / 3.56 | — | split |
| 3 | Tally (shared money) | SwiftUI | model + critic vs v1.3 + critic | 2 | 3.83 / 3.83 | — | split |
| 4a | Prise (bouldering gym) | Flutter | model vs v1.4 | 3 | 4.26 / 4.22 | — | K slight, tie, A slight |
| 4b | Petit Jour (daycare, FR) | React Native | model vs v1.4 | 3 | 3.81 / 3.96 | — | K slight, tie, tie |
| 5a | Prise (re-run) | Flutter | same baseline vs v1.5 | 3 | 4.04 / 4.22 | — | K slight ×3 |
| 5b | Petit Jour (re-run) | React Native | same baseline vs v1.5 | 3 | 3.74 / 4.11 | — | K clear ×3 |
| 6a | Officine (pharmacy) — fresh | Flutter | model vs v1.6 | 3 | **4.00 / 3.44** | 4.0 / 3.0 | A clear ×3 |
| 6b | The Rialto (cinema) — fresh | React Native | model vs v1.6 | 3 | **4.11 / 3.74** | 3.7 / 2.7 | A clear ×2, A slight |

Honest reading, round by round:
- **Rounds 1–4**: Kinetic matched a strong frontier model (pooled 3.90 / 3.91). Stable trade: Kinetic more
  complete, native and rigorous; the bare model more distinctive (6/6 reads in round 4).
- **Round 5 (v1.5, the identity-as-vocabulary rule)**: Kinetic won all 6 reads (pooled 4.17 / 3.89) and
  closed the identity gap on Petit Jour (3 → 4). **Caveat**: same briefs as round 4, and v1.5's knowledge
  was written after seeing them (brief-specific examples were neutralised before the run; a few traces
  remained). Encouraging, not proof.
- **Round 6 (v1.6, directions dealt from a library)** — the clean test on fresh briefs — Kinetic **lost all
  6 reads** (pooled 3.59 / 4.06; cleanness 2.85 / 3.83). It tied or led on distinctiveness (4.0 / 3.83) and
  anticipation, and lost on typography, colour, layout craft and calm. Cause, from the critics' evidence:
  the dealt slots were adopted whole and fought the briefs — a cool navy for "a warm local shop" and
  "a warm cinephile cinema", engraved 9pt capitals, a ruled line under every line of text, staggered
  two-up cards, a permanent CTA competing with each state's action. The bare model chose warm paper,
  serif voices and one loud object per screen — exactly what those briefs asked for. Kinetic's
  self-judgment was 0.5 too high.
- What v1.7 changes because of it: directions are **authored first** from the thesis, the deal supplies
  two **challengers** (tone-weighted, redrawn when they contradict the thesis), priors are spent only as
  defaults, decorative faces need the brief's world, ruled engines rule between entries, a measured
  **clarity** gate (`kinetic clarity`: words, lines, sizes, quiet space, loud colour areas — it ranks round
  6's pair the way the critics did), and the **studio**: three directors, a rival, an editor and a
  three-critic panel in separate contexts. Measured next in round 7 against the bare model *and*
  ui-ux-pro-max.
- Measured rigor still holds: baselines keep shipping engine-detectable defects; Kinetic arms ship none
  (caveat: Kinetic's own engine).
