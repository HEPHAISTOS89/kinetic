# A/B round 4a — "Prise" (bouldering gym), Flutter, Kinetic v1.4

Single pass per arm (each arm rendered and self-iterated; no external critique loop).
- A = the model alone. K = the model with Kinetic v1.4 (create, D2).
Renders: Flutter test renderer, 393×852, safe areas, light + dark (harness in `harness/`).
Judged blind by three new critics (X = K, Y = A). Motion unjudged. Raw scores: `../round4-tally.tsv`.

| Dimension | C1 A / K | C2 A / K | C3 A / K |
|---|---|---|---|
| product_fit | 4 / **5** | 4 / **5** | 4 / **5** |
| hierarchy | **5** / 4 | 4 / 4 | **5** / 4 |
| distinctiveness | **5** / 4 | **5** / 4 | **5** / 4 |
| typography | **5** / 4 | 4 / 4 | 4 / 4 |
| color | **5** / 4 | 4 / 4 | 4 / 4 |
| layout_craft | **4** / 3 | **4** / 3 | **4** / 3 |
| native_fidelity | 3 / **4** | 3 / **4** | 3 / **4** |
| anticipation | 4 / **5** | 4 / **5** | 4 / **5** |
| copy | 5 / 5 | 5 / 5 | 5 / 5 |
| **mean** | **4.44** / 4.22 | 4.11 / **4.22** | 4.22 / 4.22 |
| verdict | A slight | K slight | tie |

Pooled: A 4.26, K 4.22 — a tie.
Measured (`kinetic scan`, v1.5 engine): A 1 F08 (7 animations, no reduce-motion) + 4 F02 (`onTap: () {}`) + 6 D
(10 radii, 53/134 spacings off-grid, …); K 1 minor (D09 FAB, deliberate on Android).

All three critics agree:
- **Kinetic better**: an in-session home (one-tap "+1 go / Topped", Undo) for the 30-second rest; loading,
  stale "~34", unreachable-server and true XXL states; Android chrome actually rendered; community copy
  ("Nobody has topped Black 2 yet").
- **Baseline better**: a drawn domain vocabulary — pegboard illustration, hold-shaped tokens, chalk tallies,
  queued sends as outlined holds, a punch-card entry meter — and a display-size verdict sentence
  ("Busy, not packed.") as the hero; a log action reachable in every state.
- **Kinetic misses**: the tape grid is the loudest mass and competes with the answer; the pinned CTA hides
  the last row; the log sheet has a dead band; "Flash" offered on a boulder with logged goes.

Changes (v1.5): identity as a domain vocabulary with an ownable-hero gate (kinetic-direct §4b); verdict-first
heroes and one loud mass per viewport (layout.md); craft checks for sticky CTAs, sheets, the core action in
every mode, scaling numerals (kinetic-craft); domain-logic validity per state (states.md §3c);
"Community venue" sector; Flutter sheet/golden notes; the engine fixes listed in `K-feedback.md`.
