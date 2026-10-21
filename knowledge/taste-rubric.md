# Taste rubric (judged dimensions)

Used by the `kinetic-critic` agent and by `kinetic score --judged`. Ten
dimensions, each scored 1–5 **against anchors**, each score backed by
evidence (a screenshot reference, a file:line, or a KDL path) and a fix.
A score without evidence is discarded by the engine.

Calibration: **3 is competent and forgettable** — what a good template
produces. 4 is designed. 5 is what a design lead would show as reference work.
Most first drafts are 2–3. Don't grade on effort; grade the artefact.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **product_fit** | Could be any app; contradicts the thesis or the user moment | Serves the task; thesis visible only in copy | Every element traceable to the thesis and moment; the design *argues* for the product |
| **hierarchy** | No primary element; everything competes | Primary element clear; secondary/tertiary muddled | One primary, one second, calm rest on every screen; squint test passes |
| **distinctiveness** | Fails the swap test; stock patterns everywhere | Competent but familiar; recognisable only by logo | Unmistakable without the logo; one signature idea carried consistently, not decoration |
| **typography** | Many sizes, wrong leading, default tracking at display sizes | Coherent ramp; generic choices; some rhythm issues | Ramp, leading, tracking, numerals and measure tuned; type carries hierarchy and voice |
| **color** | Default palette, contrast failures, inverted dark mode | Role-based, passes contrast; generic greys or accent overuse | Tinted neutrals, accent with meaning, both themes designed; atmosphere matches thesis |
| **layout_craft** | Off-grid, misaligned, inconsistent radii/padding | Grid mostly respected; a few optical misses | Exact grid, optical alignment, concentric radii, consistent rhythm; nothing accidental |
| **motion** | Decorative or absent where needed; bounce/linear; no reduce-motion | Purposeful transitions, platform defaults | Physics with personality, continuity across screens, interruptible, reduce-motion designed |
| **native_fidelity** | Web-on-a-phone or wrong-platform idioms | Native components, little adaptation | Feels made for each platform where it helps; identity shared, chrome native |
| **anticipation** | Happy path only | Main states designed; edge cases thin | Every state, long content, XXL text, errors with recovery, offline — designed, not defaulted |
| **copy** | Marketing slop, vague labels, "Oops!" | Clear and correct; generic voice | Specific, human, short; voice derived from thesis; errors explain and recover |

## Gates (engine-enforced in `kinetic score`)
- Any F(block) finding → **blocked**, whatever the judged scores.
- product_fit ≤ 2 or distinctiveness ≤ 2 or mean < 3 → **rethink** (direction problem, not polish).
- **ship** requires: an independent critic, every dimension judged, mean ≥ 4.0, none < 3, product_fit ≥ 4, all measured scores ≥ 70.
- **ship-pending**: the same gates, but self-judged or with dimensions declared unjudgeable (with a reason) — verify before shipping.
- A judgment older than the current renders/code cannot decide (re-judge).
- Otherwise **iterate**, fixing the lowest dimensions first.

## Known critic variance
Independent blind critics disagree: across three A/B rounds the two critics
picked different winners in two rounds, with means within ±0.25. Treat a
difference under ~0.3 between two designs as a tie, use at least two critics for
decisions, and act on what they *agree* on rather than on either verdict.

## How to judge (critic procedure)
1. Read the thesis, expression level and chosen direction in KDL first; judge
   against *them*, not your own preferred style. A precise level-1 instrument
   should not be marked down for being quiet.
2. Look at renders: each key screen in light and dark, at default and largest
   text size, on the smallest and largest supported phone. No render → say so;
   judge code only for the dimensions code can show and mark the rest unjudged.
3. Run the deeper tests from anti-slop.md (swap, squint, silence, thumb, night, XXL, thesis).
4. For each dimension: score, 1–3 evidence items, the single most valuable fix.
5. Name the one change that would raise the overall design most.
