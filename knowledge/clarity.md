# Clarity: the clean screen

A clean screen is not an empty one. It says the answer, proves it, offers the
next act, and stops. Everything else waits one tap away. Models clutter
because they are rewarded for coverage: every state, every fact, every
reassurance lands on the same screen at the same weight. Kinetic separates
**coverage** (all states designed) from **presence** (what one viewport shows).

## Budgets per first viewport (measured by `kinetic clarity`)
| Measure | Clean | Cluttered | Why |
|---|---|---|---|
| Words | ≤ 45 | ≥ 120 | a glance reads ~40 words; the rest is skipped, then distrusted |
| Lines of text | ≤ 12 | ≥ 28 | each line is a fixation |
| Text sizes | ≤ 4 | ≥ 7 | display, title, body, meta — a fifth needs a reason |
| Quiet rows | ≥ 60% | ≤ 35% | space does the grouping that boxes would do |
| Largest gap | ≥ 32pt around the hero | < 16pt | the hero needs air to be the hero |
| Loud colour areas | 1 | ≥ 3 | one saturated field, button or highlight per viewport; three compete |
Target `clarity ≥ 85` on the home and every key state; `< 70` is a finding
that blocks `ship` like a judged dimension below 3.

## Rules
1. **One idea per block, one block per idea.** If two blocks say the same
   thing (a status pill and a banner), delete one (D32).
2. **Answer, proof, act.** The first viewport holds the answer (verdict or
   number), its proof (one line), and the next act. A fourth block must earn
   its place against the swap of the third.
3. **Words have a budget.** Hero ≤ 10 words. Supporting line ≤ 14. A row:
   title ≤ 5 words + one meta line ≤ 6. A button: verb + object, ≤ 3 words.
   An explanation longer than one line is a sheet, not a paragraph.
4. **Labels, not sentences, for structure**; sentences only for the one thing
   the product says to you (the verdict, an alert, an empty state).
5. **No stat strips.** Three cells of numbers under a hero are a dashboard
   in disguise; say the one that matters in the sentence.
6. **Space before boxes.** Group with space and alignment first, a hairline
   second, a container last. Never a card inside a card.
7. **One loud thing per viewport**: one filled button, one display size,
   one saturated field. A second loud thing demotes the first.
8. **Meta is quiet and singular**: one meta line per item (who · when),
   text-2 colour, never two grey lines stacked.
9. **Disclose, don't display.** Rules, policies, legends, "how it works",
   secondary history: one tap away (sheet, row, "More"). Coverage lives in
   states, not in the default viewport.
10. **One column on phones.** Unequal content in a 2-up card grid staggers,
    wraps and doubles the boxes; use one column, or a 2-up only for equal,
    comparable items with aligned tops and heights.
11. **The sticky bar carries the state's action.** A persistent bottom button
    that says "Renew" during a recall competes with "Call us": the docked
    action changes with the state, or steps back to secondary when a card
    holds the primary.
12. **Remove one accessory.** Before shipping each screen, name the element
    whose removal costs least — and remove it. If nothing can go, say why.

## Calm ≠ cryptic
Cutting words must never cost comprehension. Blind critics punished "read
21:04", "1,184°", "26 paid", "Board from 18:05" and unlabelled ring styles.
- Units always (°C, m, kn); no abbreviations a newcomer can't read.
- Every visual encoding is self-evident (filled = taken, open = free, taped =
  out of order) or carries its word; a legend is a failure (D31), a missing
  legend on an ambiguous mark is worse.
- Captions ≥ 13pt at text-2 contrast; nothing that matters at 10–11pt grey.
- **Cut words, not warmth.** The editor removes repetition, boxes and meta; it
  keeps the one human sentence in the product's voice (a signed note, the
  verdict). The baseline won copy 5 vs 4 when Kinetic's editor trimmed voice.

## Calm ≠ bland
Clean is the setting for the identity, not its replacement: the vocabulary
mark, the display voice and the field colour stay — what goes is the
second sentence, the third meta line, the box around the box, the legend.
A clean screen with no identity is the category template; an identity buried
in clutter is noise. Kinetic ships neither.

## The editor's pass (kinetic-editor, or yourself without agents)
On each key render: run `kinetic clarity`, then list every element of the
first viewport with its job in ≤ 4 words. Cut list, in this order: duplicates
→ explanations that belong in a sheet → meta lines → containers → icons that
don't aid scanning → the weakest block. Re-render, re-measure; stop when
clarity ≥ 85 and nothing on the cut list would cost the user an answer.
