---
name: kinetic-direct
description: "Kinetic's creative direction step for mobile apps: deal three directions from Kinetic's library (composition engine, native type system, palette with a colour field, motion personality), fuse the chosen one with the product's inventory into an idea and a drawn vocabulary, and pick the most distinctive viable direction. Use after kinetic-think for create/redesign, or when a mobile UI looks generic, templated or interchangeable."
---

# Author, deal, choose the most distinctive viable

> Paths are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here.

Two failure modes, both measured in blind rounds. Directions you generate
alone come from your prior: correct and forgettable (rounds 1–4). Directions
dealt at random and adopted whole fight the brief: a cool navy for "a warm
local shop", engraved 9pt capitals for tired readers, lines under every line
(round 6 lost 6/6). So Kinetic does both, in this order:

## 1. Author first, then deal two challengers
1. **A — yours, from the thesis.** Before seeing any deal, write the direction
   the brief itself asks for: its tone words, `thesis.feel`, the inventory.
   It may be warm paper and a serif when the brief asks for warmth — make it
   *this* product's paper and type, never the generic cream (priors.md).
   Mark it `source: author`.
2. **B, C — dealt challengers.** `kinetic deal --brief-file <brief> --options 2`.
   The deal weights the palette by the brief's tone (warm and calm briefs are
   not dealt cool or loud palettes). Each challenger must still pass the
   thesis: a slot that contradicts `thesis.feel`/`never` or the brief's tone
   is redrawn with that reason (`--redraw 2.palette --reason "thesis.never: cold portal"`).
3. **Fuse, don't copy.** The best result often takes A's voice with a
   challenger's engine (composition) or vocabulary idea. A fusion is its own
   direction marked `source: fusion` with the `engine:` it borrows; say what
   came from where in `because`.
- The category standard is always available as an exit if the *user* asks
  for it. Never recommend it.

## 2. Each direction meets the inventory
For each direction (yours and the challengers), write the **idea sentence** with an item from
`inventory` (kinetic-think writes 8–12):

> In this app, **[inventory item]** becomes **[the engine's device]**.

Then the **competitor test**: name the nearest competitor and say why the
sentence fails for them. If it fits them too, it is the category's idea — pick
another inventory item. Sketch the home's first viewport in five lines using
the engine's geometry (primary, proof, vocabulary object, next decision, thumb
action). Write the three as KDL `directions` (`source: author` on yours, `engine:` set
to the dealt id on the challengers) with all six axes (structure, density, color, type, motion, material).

## 3. Score honestly (1–5)
`product_fit` (thesis + moment), `usability` (task speed, accessibility, the
brief's must-haves above the fold), `feasibility` (stack, time, assets),
`distinctiveness` (cover-the-logo: could this home belong to a competitor?),
`risk_of_slop` (which D IDs and which prior is it near?).

## 4. Converge: the most distinctive viable direction
1. **Viable** = product_fit ≥ 4, usability ≥ 4, feasibility ≥ 3, every `must`
   requirement served in the first viewport where the brief needs it, no slot
   contradicting `thesis.feel`/`never`, and the clarity budgets reachable
   (knowledge/clarity.md: a direction that needs two loud things per screen
   or a two-column card grid is not viable on a phone).
2. Among viable directions, **choose the highest distinctiveness**. Fit is a
   floor, not the tie-breaker: a calm, correct, forgettable direction lost
   every blind round. If a brand or user fact rules the more distinctive one
   out, lower its fit score and write the fact in `because` (K30 checks).
3. If no option is viable, redraw the weakest slot with its reason — don't
   retreat to the category standard.
Write `verdict: chosen` + `because`, one `because` per rejected direction.

## 4b. Identity: inventory → idea → vocabulary (all expression levels)
The expression level sets the **volume** of identity, never its presence
(`knowledge/identity-channels.md`: native frame, owned content).
1. **Vocabulary as an artefact.** Draw 6–10 marks from the inventory
   (`.kinetic/vocab/*.svg` or code-drawn, `kinetic svg lint` clean on the 24
   grid) and record them in KDL `vocabulary: [{mark, from, replaces, sites,
   file}]`. Each **replaces** a generic part: progress_bar, status_dot, chip,
   badge, tab_icon, empty_illustration, data_mark, divider, card… Examples
   from other domains: a library's loans are spine labels, not list bullets;
   days left are date stamps, not a progress bar; a renewal waiting for signal
   is an *outlined* stamp.
2. **≥ 4 sites**: the hero, a list item, a data encoding, a degraded state
   (K31). The scanner flags a stock progress bar or chip left in a role the
   vocabulary covers (D35).
3. **The hero is the vocabulary's home.** The first viewport holds the answer
   *and* the identity. When the glance question is qualitative, the answer is a
   display-size verdict sentence in the product's voice, with the number under
   it (layout.md §glance headers).
4. **Identity never costs legibility**: every mark carries a word or a grade
   (D31); controls stay native.

Gate before building: list every block of the first two viewports as
**ownable** (only this product could have it) or **generic** (swap test).
At least half ownable at expression ≥ 3; at ≤ 2 the hero and one more.

## 5. Signature move and live thing
- **Signature move**: the dealt engine's signature, made from the idea (a
  detail a stranger understands in one glance, no legend — D31).
- **One live thing**: a direct manipulation made from the idea (scrub the
  spine, drag the needle, tear the stub), one-handed, with a reduce-motion path
  and a plain-control equivalent. It must never block a task.
- **Substance**: real content at full density (fixture data labelled as
  such), one drawn or photographed moment per key empty/first-run state.

## 6. Contract, then build
Write KDL `contract` (≤ 200 words, K32): thesis, idea, own_world,
first_viewport, vocabulary, signature_move, live_thing. Re-read it before
each screen; it protects the idea through the build. Then `kinetic validate`,
report the choice in 3–5 lines (chosen + why, rejected + why, redraws), and
continue with kinetic-states and kinetic-system — those systemise the dealt
type, palette and motion; they don't re-choose them.
