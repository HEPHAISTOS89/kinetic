# Kinetic v16 — candid feedback from the Officine run (create, D2, Flutter)

## The deal
- **Useful, no redraw.** Option 1 (pinned-board + copperplate-signage + highlighter + settled) fused naturally with the pharmacy: the stapled bag label became the pinned notice, the pharmacist's highlighter the field, engraved small caps the shop sign. Without the deal I would have gone straight to the teal-on-cream prior that priors.md names. Options 2 (time-atmosphere) and 3 (specimen grid) were honestly weaker (3 reads as a retail catalogue — the brief's anti-thesis).
- **The deal ignores the expression budget.** The dealt palette has a saturated field (#FFE45C) on top of the accent; `validate` then fires D13 major (2 hue families > budget 1) at level 2 — the level sectors.md recommends for health (1–2). I had to raise the level to 3 to keep the dealt palette. The deal should know the sector/level, or the validator should count the dealt `field` as part of the palette, not as a second accent.
- **The deal and the validator disagree on the accent.** Dealt seed #1A2B6D (navy ink) is flagged D01 "violet/indigo AI default" by `validate`. Its fix says "say so in `because`", but no `because` silences it (only `brand.status: strict`). Either don't deal it or honour a reason.
- **Dealt Android face (Cinzel, "bundle") is unobtainable offline**, and Copperplate only exists as a .ttc that Flutter can't select a face from; I had to write a TTC splitter to extract Copperplate Bold and ship it on both platforms. Dealing two different display faces per platform is also odd for one shop's signage.
- Pinned-board's first viewport ("2-column masonry, 0–2° rotation") is risky for the brief's older users with large text; the engine card says nothing about a single-column fallback. I dropped rotation and switched to one column at text scale ≥ 1.3.

## Engine bugs / friction
- **`scan` flags the engine's own export.** `kinetic export` writes `static const light = KColors(...)` and `dark` on single lines; `scan` then reads both themes as one light theme ("13 neutrals, light 13, dark 1") → D13 **major**. It disappears after `dart format` — i.e. the verdict depends on line wrapping. A KDL `exceptions` entry with `where: lib/design/kinetic_tokens.dart` does **not** waive it (the finding has no path), so the documented escape hatch doesn't work for project-wide findings.
- `validate` K21 (info) checked requirement R2's element `renew-button` against `renew-sheet` (the second screen that serves R2) instead of `home`, where it is listed in `reading_order`.
- The exported `kineticTheme()` doesn't set `fontFamily`, so button labels risk Ahem boxes in goldens (the flutter.md gotcha). I built my own theme on the exported tokens; the export could take the platform family as a parameter.
- `kinetic states code lib` printed only coverage ("data_screens=1; screens_not_evaluated=1") with no list of which screen was evaluated or why the other wasn't — unclear whether it passed.
- `score` correctly refuses a stale critique, but in a self-critique loop that means re-saving critique.json after every render; fine, just friction.
- No help for checking overflow at XXL text below the fold: the harness renders the top 852 px only. I wrote a tall + 2.0× inspection test; Kinetic could ship one per stack.

## Instructions / knowledge
- The D2 reading list is long (think, direct, priors, identity-channels, sectors, states, system, code, motion, states.md, copy.md, layout §1–3, two platform files, flutter.md, KDL.md, craft, critique, taste-rubric): ~3,000 lines before the first pixel. A one-page D2 checklist would save time.
- sectors.md has no pharmacy / "local shop with health stakes" entry; Health says Expr 1–2 and "warmth only in onboarding and support copy", which conflicts with a brief asking for the warmth of a local counter. I had to argue the level myself.
- flutter.md's golden gotcha about sheets is good, but `CupertinoSheetRoute`/`showCupertinoSheet` have no animation-style switch; I had to subclass the route to render the iOS sheet as an initial state. Worth a line.
- Craft rule 12 ("never a full-width button slab at night") isn't enforceable with the dealt dark palette (accent #8AA2E3 is bright and is also the filled-button colour). I added an `action`/`on-action` role (#4A61B8, white text) — the palette library could carry it.
- The self-critique cap ("distinctiveness ≤ 3 unless …") is helpful; the rule list is clear.
