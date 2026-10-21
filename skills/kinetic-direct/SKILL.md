---
name: kinetic-direct
description: "Kinetic's creative direction engine for mobile apps: diverge into three genuinely different art directions (structure, density, color strategy, type voice, motion personality), score them against the thesis, converge on one with reasons, and choose a signature detail. Use after kinetic-think for create/redesign, or when a mobile UI looks generic and needs a distinctive, product-specific identity."
---

# Diverge, then converge

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

The first idea is the average idea. Designers explore deliberately different
answers before committing; this module forces that and records it in KDL
`directions`, so the choice is visible and challengeable.

## 1. Material to think with
- `knowledge/directions.md` — 14 complete directions with tokens. Starting points, not costumes.
- `knowledge/exemplars.md` — mechanisms from exemplary products (what to borrow, when not to).
- `knowledge/sectors.md` — what the sector legitimately needs.
- The thesis, spine and expression level from kinetic-think (`.kinetic/design.kdl`).

For D3 work, prefer delegating the divergence to the **kinetic-director**
agent (fresh context = less anchoring), then evaluate its proposals here.

## 2. Diverge: three directions that differ on ≥ 3 axes
Axes (write all five for each direction):
| Axis | Examples of genuinely different answers |
|---|---|
| structure | single-column narrative · hub of tools · feed · canvas/map-first · one-question-at-a-time |
| density | airy · balanced · dense/expert |
| color | tinted monochrome · neutral + one accent · dominant brand surface · data-driven color · dark-first |
| type | system native · editorial serif display · grotesk tabular · rounded friendly · mono technical |
| motion | still and precise · native calm · unhurried · lively · playful physical |

Recipe that reliably produces divergence:
- **A — the faithful one**: the strongest expression of the thesis in the
  sector's language, executed better than competitors.
- **B — the reframe**: change the *structure* (e.g. dashboard → one sentence +
  one number; list → timeline; tabs → single hub).
- **C — the bold one**: push the spine or the brand to expression +1/+2, or
  borrow a mechanism from an unrelated domain (exemplars.md) that fits the moment.
Three palettes on one layout is not divergence (the validator flags K05).

Mutate library directions: take **structure from one, voice from another**,
never average two palettes. Change at least three things so the result
belongs to this product.

## 3. Score honestly (1–5)
`product_fit` (thesis + moment), `distinctiveness` (swap test),
`usability` (task speed, accessibility), `feasibility` (stack, time, assets),
`risk_of_slop` (5 = high risk). Ask of each: which slop IDs is it close to?
(e.g. a "premium dark" direction near D14.)

## 4. Converge
Choose the direction with the best product_fit that keeps risk_of_slop ≤ 2
and feasibility ≥ 3. Distinctiveness breaks ties — never overrides fit.
Write `verdict: chosen` with `because`, and a one-line `because` for each
rejected direction (it is evidence of judgment and helps the user disagree).

Hybrid is allowed only as "A with B's structure" etc., stated explicitly.

## 4b. Identity floor (all expression levels)
The expression level sets the **volume** of identity, never its presence. Every
product needs at least one ownable element in the first viewport of its main
screen: a voiced display or numeral treatment, a motif tied to the name or the
spine, or a signature component. Run the swap test on the chosen direction
before building — if renaming the app breaks nothing, add the voice now. (A/B
evidence: quiet level-2 Kinetic designs lost "distinctiveness" to bolder
baselines in rounds 2 and 3.)

## 5. The signature detail
One memorable decision derived from the spine that improves understanding or
feeling — a hero numeral, a time-aware tint, a gesture that matches the
mental model, a progress form that is the brand. Budget by expression level
(1: one quiet detail; 5: several). Write KDL `signature: {what, where, because}`.
A signature that doesn't trace to the spine is decoration — drop it.
**Legibility test**: a stranger understands the signature in one glance with no
legend, tooltip or coach mark. If it needs explaining, encode the meaning in the
element itself (a word, icon + word, a visible boundary) — D31. In the A/B
evaluation, two clever-but-cryptic signatures (a "run chip", size-coded
reachability with a legend) lost to plain words like "Too soon".

## 6. Then
Run `kinetic validate` (directions block), report the choice in 3–5 lines
(chosen + why, rejected + why), and continue with kinetic-states and
kinetic-system. If the user disagrees, switch directions without defending
sunk cost — the record makes switching cheap.
