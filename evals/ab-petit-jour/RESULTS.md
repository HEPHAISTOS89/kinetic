# A/B round 4b — "Petit Jour" (daycare, French UI), React Native, Kinetic v1.4

Single pass per arm. A = the model alone, K = the model with Kinetic v1.4 (create, D2).
Renders: react-native-web in Chromium, 393×852, safe areas, light + dark (harness in `harness/`).
Judged blind by three new critics (X = A, Y = K). Motion unjudged. Raw scores: `../round4-tally.tsv`.

| Dimension | C1 A / K | C2 A / K | C3 A / K |
|---|---|---|---|
| product_fit | 4 / 4 | 4 / 4 | 4 / 4 |
| hierarchy | 4 / 4 | 4 / 4 | 4 / 4 |
| distinctiveness | **4** / 3 | **4** / 3 | **4** / 3 |
| typography | 4 / 4 | 4 / 4 | 4 / 4 |
| color | 4 / 4 | 4 / 4 | 4 / 4 |
| layout_craft | 4 / 4 | 3 / **4** | 4 / 4 |
| native_fidelity | 3 / **4** | 3 / **4** | 3 / **4** |
| anticipation | 4 / **5** | 3 / **4** | 4 / **5** |
| copy | 4 / 4 | 4 / 4 | 4 / 4 |
| **mean** | 3.89 / **4.00** | 3.67 / **3.89** | 3.89 / **4.00** |
| verdict | tie | K slight | tie |

Pooled: A 3.81, K 3.96 — a tie leaning Kinetic.
Measured (`kinetic scan`, v1.5 engine): A 1 F08 (6 animations, no reduce-motion) + 8 D (11 radii, 42/71 spacings
off-grid, 14 font sizes, …); K 0.

All three critics agree:
- **Kinetic better**: loading, server error with "Appeler la crèche", offline in the imperfect tense
  ("Léa faisait la sieste…") with a queued signature, offline photo placeholder, large text; correct French
  typography (13 h 05, 38,4 °C); native inset lists and segmented control; one accent with one meaning.
- **Baseline better**: identity — a mark per child state (moon napping, sun in the garden, house at home);
  the fever moment as an event (missed call at 14h22, the number on the button, the hero re-answering
  "en attendant votre appel"); the child switcher showing each child's live state; warmer carer copy.
- **Kinetic misses**: the hero under the fever alert talks about the nap; "Sieste : Pas encore" during a
  logging lag states a fact the app doesn't have; the alert copy reads like a rule; "Départ prévu" is the
  daycare's word, not the parent's.

Changes (v1.5): domain vocabulary and per-state marks (kinetic-direct §4b); high-stakes moments —
alert takeover, alerts as events, unknown ≠ didn't happen, live state in switchers (states.md §3c);
fear test in self-critique; French time formats and "user's side of the verb" (copy.md);
"Childcare / family logistics" sector; RN core-Animated, no-haptics and text-scale preview notes;
the engine fixes listed in `K-feedback.md` (RN export now typed as `TextStyle`, data colours in
`useTokens()`, per-platform families, fixture folders, `exceptions`).
