---
name: kinetic-direct
description: "Kinetic's creative direction step for mobile apps: deal three directions from Kinetic's library (composition engine, native type system, palette with a colour field, motion personality), fuse the chosen one with the product's inventory into an idea and a drawn vocabulary, and pick the most distinctive viable direction. Use after kinetic-think for create/redesign, or when a mobile UI looks generic, templated or interchangeable."
---

# Deal, fuse, choose the most distinctive viable

> Paths are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here.

Directions you generate yourself come from your prior: the category's average
and your own habits (`knowledge/priors.md`). In four blind rounds that prior
made Kinetic correct and forgettable. So the first draw comes from outside you:

## 1. Deal (before you imagine anything)
```
kinetic deal --brief-file <brief or PRODUCT.md>        # writes .kinetic/deal.json
```
You get three options, each an **engine** (how something of the product's
world becomes the screen's device, with first-viewport geometry), a native
**type system**, a **palette** with a colour field and proportions
(contrast-checked roles), and a **motion personality**. Read the sheet; read
`knowledge/library/*.json` only for the dealt ids if you need more.

Rules:
- Choose **among the dealt options**. Do not blend them back toward what you
  would have done anyway.
- Replace a slot only with `kinetic deal --redraw N.slot --reason "…"`, and
  only for a **product fact or brand constraint** ("brand colour is #0A7A3E",
  "the venue has no printed artefact"). "I prefer…" is not a reason. Redraws
  are logged; the validator rejects a chosen engine that was never dealt (K29).
- The category standard is always available as an exit if the *user* asks for
  it. Never recommend it.

## 2. Fuse each option with the inventory
For each dealt option, write the **idea sentence** with an item from
`inventory` (kinetic-think writes 8–12):

> In this app, **[inventory item]** becomes **[the engine's device]**.

Then the **competitor test**: name the nearest competitor and say why the
sentence fails for them. If it fits them too, it is the category's idea — pick
another inventory item. Sketch the home's first viewport in five lines using
the engine's geometry (primary, proof, vocabulary object, next decision, thumb
action). Write the three as KDL `directions` with `engine:` set to the dealt id
and all six axes (structure, density, color, type, motion, material).

## 3. Score honestly (1–5)
`product_fit` (thesis + moment), `usability` (task speed, accessibility, the
brief's must-haves above the fold), `feasibility` (stack, time, assets),
`distinctiveness` (cover-the-logo: could this home belong to a competitor?),
`risk_of_slop` (which D IDs and which prior is it near?).

## 4. Converge: the most distinctive viable direction
1. **Viable** = product_fit ≥ 4, usability ≥ 4, feasibility ≥ 3, every `must`
   requirement served in the first viewport where the brief needs it.
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
