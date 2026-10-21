# Kinetic communication protocol

How Kinetic's modules, agents and engine talk to each other and to the user.
It is optimised for models: fixed shapes, explicit evidence, no prose where a
field will do, and nothing that has to be re-derived later.

## 1. Evidence vocabulary (everywhere)
| Level | Means | Example |
|---|---|---|
| `observed` | read directly from a source or render | `Color(0xFF7C3AED)` at home.dart:16 |
| `derived` | computed from observed facts | "12 distinct font sizes" |
| `inferred` | heuristic about intent; needs confirmation | "IconButton without tooltip" (may be wrapped in Semantics elsewhere) |
| `judged` | a critic's assessment of a render, with anchors | "hierarchy 2/5: three elements compete at the top (shot-2)" |
| `unknown` | not examined | a file not scanned, a state not rendered |

Rules: missing coverage is `unknown`, never "clean". An `inferred` finding is
never reported to the user as a fact. A `judged` score without evidence is discarded.

## 2. Finding (engine → model)
```json
{"rule": "D17", "tier": "D", "severity": "major", "evidence": "derived",
 "file": "lib/home.dart", "line": 19, "path": "system.space.scale",
 "message": "4/4 spacing values off the 4pt grid (13, 14, 17, 23)",
 "fix": "snap to the spacing scale (multiples of 4)"}
```
`tier`: F refuse · D reject by default · C conditional · I info.
`severity`: block · major · minor · info. Rule IDs: knowledge/anti-slop.md
(F/D/C), docs/KDL.md (K), knowledge/iconography-svg.md (SVG).

## 3. Design brief (think → every other module)
The single hand-off object, written into `.kinetic/design.kdl` (sections
`product`, `thesis`, `expression`) and summarised in ≤ 8 lines when spoken:
```
Product   Lune — sleep, half-asleep in bed, one hand, 20–60s, daily, low stakes
Thesis    The app you open half-asleep that tells you how you slept without waking you up.
Feel      calm · held · unhurried      Never  dashboard · streaks · bright white
Spine     the light goes down
Level     2 — calm beats spectacle; identity lives in one numeral
Unknowns  partner mode?
```

## 4. Direction record (director agent → main)
Exactly the KDL `directions` list: ≥ 3 entries with `axes` (structure,
density, color, type, motion), `scores` (product_fit, distinctiveness,
usability, feasibility, risk_of_slop — 1–5), `verdict`, `because`.

## 5. Forensics report (forensics agent → main)
```json
{"source": ["lib/"], "coverage": {...from scan...},
 "dna": {...from kinetic dna...},
 "classification": {"keep": ["…"], "evolve": ["…"], "replace": ["…"], "remove": ["…"]},
 "product_reading": {"observed": ["…"], "inferred": ["…"], "unknown": ["…"]},
 "top_findings": [Finding, …]}
```

## 6. Critic judgment (critic agent → engine)
Saved as `.kinetic/critique.json`, consumed by `kinetic score --judged`:
```json
{"renders": ["shots/tonight-light.png", "shots/tonight-dark-xxl.png"],
 "context": {"thesis": "…", "level": 2, "direction": "Night paper"},
 "dimensions": {
   "product_fit":   {"score": 4, "evidence": ["shot-1: numeral dominates, one sentence"], "fix": "…"},
   "hierarchy":     {"score": 3, "evidence": ["shot-2: strip and button compete"], "fix": "…"},
   "distinctiveness": {…}, "typography": {…}, "color": {…}, "layout_craft": {…},
   "motion": {…}, "native_fidelity": {…}, "anticipation": {…}, "copy": {…}},
 "unjudged": ["motion: no recording available"],
 "tests": {"swap": "pass", "squint": "pass", "silence": "fail: …", "thumb": "pass", "night": "pass", "xxl": "fail: …", "thesis": "pass"},
 "biggest_lever": "one sentence: the single change that would lift the design most"}
```
Dimensions without a render-based evidence item are listed in `unjudged`
and omitted from `dimensions`.

## 7. Response to the user (main → user)
Design work is reported like a design lead would, not like a log:
1. **What I understood** — the brief in 2–4 lines (only when it was inferred).
2. **What I decided and why** — direction, level, the signature idea; the
   rejected alternatives in one line each.
3. **What changed** — files/screens; before → after where it matters.
4. **What I verified** — engine results (validate/scan/score) and renders
   actually inspected; state which were not.
5. **What's left or unknown** — honestly.
No dumps of the KDL or full finding lists unless asked; link the files.

## 8. Effects declaration
Every engine command declares its effects in docs/TOOLS.md. Read-only
commands: validate, palette, contrast, scan, dna, states, score, svg lint,
spring. Writing commands: init (only `.kinetic/`), export --out (refuses to
overwrite a hand-written file), svg fix --write (rewrites the given SVGs).
