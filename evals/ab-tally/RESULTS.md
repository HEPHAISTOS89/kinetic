# A/B round 3 — new brief "Tally" (shared expenses), Kinetic v1.3, both arms with a critic loop

Controlled design: both arms produced v1, received one independent critique, and iterated once.
- A = the model alone + a generic senior design-director critique (no Kinetic knowledge).
- K = the model with Kinetic + the `kinetic-critic` agent (rubric, KDL, protocol JSON).
Final renders judged blind by two new critics (X = K, Y = A). Motion unjudged.

| Dimension | Critic 1: A / K | Critic 2: A / K |
|---|---|---|
| product_fit | 4 / 4 | 4 / 4 |
| hierarchy | 4 / 4 | 3 / **4** |
| distinctiveness | **4** / 3 | **4** / 3 |
| typography | **4** / 3 | 4 / 4 |
| color | 4 / 4 | 3 / **4** |
| layout_craft | **4** / 3 | 3 / **4** |
| native_fidelity | 4 / 4 | **4** / 3 |
| anticipation | 4 / 4 | 4 / 4 |
| copy | 4 / **5** | 4 / **5** |
| **mean** | **4.00** / 3.78 | 3.67 / **3.89** |
| verdict | A, clear | K, slight |

Pooled: A 3.83, K 3.83. A tie.

Measured (`kinetic scan`, same engine): K 0 findings; A 1 F (animation without reduce-motion) + 6 D
(28/34 spacings off-grid, 6 hue families, …).

Both critics agree:
- **Kinetic better**: copy and tone ("to put in / to get back"; errors give cause, consequence and recovery),
  faithfulness to "never a debt collector", the post-logging moment (Added · Undo), loading and per-row sync states.
- **Baseline better**: identity (New York serif title, tally motif, tuned numerals with dimmed decimals),
  compact secondary chart keeping settle-up in the first viewport.

Changes (v1.4): identity floor at every expression level; "system text, owned voice" replaces
"system first"; secondary blocks stay compact; critic variance documented (use ≥2 critics, a gap under 0.3 is a tie).
