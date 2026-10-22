# Kinetic — architecture

Kinetic is a design system *for the model*: a cognitive architecture, a design
reasoning language, a body of taste knowledge and a deterministic engine that
together make a coding agent design mobile products like a senior designer —
understand first, decide deliberately, execute precisely, then prove it.

## The problem, stated precisely

Models produce slop for four separable reasons. Each layer of Kinetic targets one.

| Cause | What it looks like | Kinetic layer |
|---|---|---|
| **Regression to the mean** — with no specific target, the model emits the average of its training data | purple gradient, greeting + card grid, Inter everywhere, fade-up on everything | **Taste knowledge** (concrete directions, numbers, exemplars) + **Thesis** (a target that belongs to *this* product) |
| **Shallow reasoning** — decisions made at the pixel level before the product is understood | pretty screen that answers the wrong question; no empty/error state | **Cognitive pipeline** (understand → decide → anticipate → realise → prove) |
| **Implicit, unverifiable decisions** — choices live only in prose or in scattered code | 14 font sizes, 9 greys, 6 radii, durations chosen per widget | **KDL**, the design reasoning language: every decision explicit, typed, cross-checked |
| **Lenient self-review** — the author grades its own work in the same context | "looks premium" | **Taste engine** (measured) + **independent critic** (judged, fresh context) |

## Layers

```
┌───────────────────────────────────────────────────────────────────────┐
│ 1. ENTRY        kinetic (router) — mode × target × depth                  │
├───────────────────────────────────────────────────────────────────────┤
│ 2. COGNITION    think · direct · states · system · craft · motion ·       │
│                 code · critique · studio (modules, loaded when needed)    │
├───────────────────────────────────────────────────────────────────────┤
│ 3. LANGUAGE     KDL — .kinetic/design.kdl (decisions) + findings protocol  │
├───────────────────────────────────────────────────────────────────────┤
│ 4. KNOWLEDGE    knowledge/*.md — color, typography, layout, clarity,      │
│                 component contracts, states, motion, anti-slop, priors,   │
│                 stacks + library/*.json (the deal: engines, type, palettes,│
│                 motion)                                                    │
├───────────────────────────────────────────────────────────────────────┤
│ 5. ENGINE       bin/kinetic — validate · palette · contrast · scan · dna · │
│                 states · score · export · svg · init · deal · clarity ·    │
│                 panel · sheet · font · spring          (Python stdlib)     │
├───────────────────────────────────────────────────────────────────────┤
│ 6. AGENTS       director ×3 · rival · editor · critic ×3 (lenses) ·        │
│                 forensics — the studio, merged by `kinetic panel`          │
│ 7. HOOK         continuous design lint on UI edits (opt-in per project)    │
└───────────────────────────────────────────────────────────────────────┘
```

### 1. Entry: route by mode, target and depth
Inspired by REA: *route the target first*. The router identifies the mode
(create, improve, redesign, audit, system, design-to-code, code-to-design,
evolve), the target the user supplied (brief, codebase, screen file, screenshot,
KDL) and the depth the request deserves (D0 touch-up → D3 product). Depth
decides which modules run. A padding fix never runs the full pipeline; a new
product always does.

### 2. Cognition: modules, not agents
Each module is a skill with one job and a written output in KDL. They are
capabilities composed by the router; they are not mandatory subagents.

| Module | Job | Writes |
|---|---|---|
| think | Read the product; thesis, expression level, concept spine, journey simulation | `product`, `thesis`, `expression`, `journeys` |
| direct | Diverge into 3 genuinely different directions; converge on one with reasons | `directions` |
| states | Every screen/component in every state and environment | `screens[].states`, `components[].env` |
| system | Type, color, space, shape, elevation, icon, motion tokens | `system` |
| craft | Pixel-level visual intelligence: optics, type detail, icon/SVG construction | `signature`, icon files, review notes |
| motion | Choreography, physics, haptics, reduce-motion | `system.motion`, `screens[].motion` |
| code | Design↔code in Flutter, SwiftUI, Compose, React Native, web | source edits, token exports |
| critique | Audit, taste evaluation, pre-mortem, improvement loop | `premortem`, findings, score |

### 3. Language: KDL
A design-reasoning language optimised for models (see [KDL.md](KDL.md)).
It is *not* an orchestration language — REA's rule applies: no custom
orchestration without an observed need. KDL is a **decision record** with a
closed vocabulary, because the observed failure is that design decisions are
implicit, scattered and unverifiable. Writing KDL forces each decision to be
made, named, justified (`because`) and linked to the thesis; the engine then
checks completeness and coherence mechanically (state coverage, token
resolution, contrast, grid conformity, motion completeness, slop phrases).
It is stack-neutral, so one design compiles to five stacks.

### 4. Knowledge: concrete taste
Rules alone produce "avoids X but still mediocre". The knowledge base is
mostly *positive and numeric*: exact platform type ramps, spring parameters,
OKLCH ramp construction, radius concentricity, icon keylines, complete art
directions with tokens, principles drawn from exemplary apps. The anti-slop
catalog keeps Prismora's three tiers (F refuse / D reject by default /
C conditional) and gives each rule a stable ID shared by the scanner.

### 5. Engine: deterministic primitives
REA's shapes, applied to design:

| Shape | Command | Answers |
|---|---|---|
| inspect | `scan`, `svg lint` | What design facts does this source/SVG contain, where, and which rules fire? |
| trace/derive | `dna` | What is the de-facto design system implied by this code? |
| validate | `validate` | Is this KDL complete and coherent? |
| compute | `palette`, `contrast` | Correct color math (OKLCH, WCAG 2, APCA) |
| generate | `export`, `states`, `init` | Tokens in a target stack; state-matrix skeleton; project setup |
| workflow | `score` | Taste report: measured sub-scores + independently judged sub-scores, never merged silently |

Every result is JSON (`--json`) with `evidence` per finding:
`observed` (parsed from source), `derived` (computed from observed facts),
`inferred` (heuristic). Unscanned files and unsupported syntax are reported as
**unknown coverage**, never as "no problem found".

### 6. Agents: independence where it matters
- **kinetic-critic** — adversarial reviewer in a fresh context. Judges renders
  and code against the rubric, returns protocol JSON. Exists because
  self-critique in the same context is lenient.
- **kinetic-director** — produces divergent directions without anchoring on
  the first idea.
- **kinetic-forensics** — code-to-design: reads a codebase, runs `dna`, returns
  style DNA and KEEP/EVOLVE/REPLACE/REMOVE.

### 7. Hook: continuous improvement
`PostToolUse` on Edit/Write. Active only in projects containing `.kinetic/`.
Scans the edited UI file and returns only F/D findings as context, so drift
is caught at the moment it is introduced. Silent otherwise.

## Decisions and their alternatives

| Decision | Chosen | Rejected alternative and why |
|---|---|---|
| Engine language | Python 3 stdlib, zero dependencies | Node/TS (Prismora): heavier install; PyYAML: not present on host |
| KDL syntax | Strict YAML subset with own parser | JSON: verbose and noisy for models; full YAML: needs dependency, ambiguous |
| Code analysis | Lexical extractors per language | Full AST per language: 5 toolchains to depend on; lexical extraction with explicit `evidence: inferred` is honest and fast |
| Stacks | Flutter + SwiftUI deep; Compose, React Native, web solid | Flutter-only: user needs multi-language performance |
| Self-review | Independent critic agent | Same-context review: lenient |
| Images | Out of v1 scope | Raster generation: v2 |
| Prose language of skills | English (instructions); user-facing replies follow the user | Mixed FR/EN (Prismora): weaker adherence, harder to maintain |

## What Kinetic will not claim
A scan finding is a fact about source text, not a verdict on beauty. A taste
score separates what was measured from what was judged. A render screenshot is
not a journey test. An unscanned file is unknown, not clean.
