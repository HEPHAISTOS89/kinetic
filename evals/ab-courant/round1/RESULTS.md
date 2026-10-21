# A/B round 1 — "Courant" home screen (SwiftUI), Kinetic v1.0

Protocol: docs/EVALUATION.md §3. Same model for both arms; A = no plugin/skills, B = Kinetic v1.0.
Both arms could render and iterate freely. Two independent critics judged renders blind
(X = A, Y = B, random assignment sealed until both verdicts were in). Motion unjudged (stills).

## Judged (rubric 1–5, 3 = competent and forgettable)
| Dimension | Critic 1: A / B | Critic 2: A / B |
|---|---|---|
| product_fit | 4 / 4 | 4 / 4 |
| hierarchy | 3 / 4 | 4 / 4 |
| distinctiveness | 3 / **4** | 3 / **4** |
| typography | 3 / **4** | 3 / **4** |
| color | **4** / 3 | **4** / 3 |
| layout_craft | 3 / 4 | 4 / 3 |
| native_fidelity | **4** / 3 | **4** / 3 |
| anticipation | 4 / 4 | 4 / 4 |
| copy | 4 / 5 | 4 / 4 |
| **mean** | 3.56 / **3.89** | **3.78** / 3.67 |
| verdict | B, clear | A, slight |

Pooled mean: A 3.67, B 3.78 — a split decision.
B's self-judged mean was 4.11 — more lenient than both independent critics (evidence for `ship-pending`).

## Measured (`kinetic scan`, same engine version)
A: 3 major D (16 neutrals, 23/30 spacings off-grid, text shrink-to-fit), 14 literal font sizes and no text styles.
B: 0 findings at the time; integrity, state coverage, accessibility, motion hygiene 100; system coherence 84.

## Consistent signal (both critics agree)
- Kinetic better: distinctiveness, typography (condensed board numerals), anticipation breadth
  (server error keeping structure, long text, accessibility layout, late night), honest degraded states, copy.
- Kinetic worse: brief coverage (saved stops below the fold), no search/map in the thumb zone,
  native chrome, white canvas with an achromatic accent.

## Changes made in response (v1.1)
- KDL `requirements` + screen `serves` + validator K21 (must-have served by no screen / not above the fold).
- `thumb` per screen + K22; K23 white canvas; K24 achromatic accent.
- "Completeness before cleverness" in the router, think and critique (structure pass before taste).
- From B's feedback log: inferred findings never gate; `ship-pending`; states code follows components;
  motion `kind` (only signature budgeted); font width (condensed) in KDL/export; data colors; transit playbook;
  macOS render-harness notes; locale formatting; minimum reading list per depth.
