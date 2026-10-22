# Kinetic v2.0 (kinetic-v17): candid feedback from a studio run

The run: mode `create`, depth D2, studio. Brief: "Branch", a neighbourhood library home screen in Flutter.

## Instructions and knowledge

1. **The library example leaks into a library brief.**
   - docs/KDL.md uses "the date stamp on the returns slip" and "spine labels" as its worked `inventory`/`idea`/`vocabulary` example.
   - kinetic-direct §4b says "a library's loans are spine labels, not list bullets; days left are date stamps".
   - For this brief the docs hand over the vocabulary, which undermines the "author first, then deal" logic and any honest distinctiveness claim. Use an example domain that is not in your eval set, or rotate examples.

2. **Studio vs router disagree on who the directors develop.**
   - Router §1b says "three directors in parallel on the dealt options".
   - Studio step 2 says director 1 develops the *authored* A, and 2 and 3 develop the dealt challengers.
   - K29 then requires the chosen direction's `engine:` to be a dealt id. The protocol never says what `engine` an authored A carries. Director 1 flagged it, and I had to map A to `verdict` by hand.

3. **No sector entry for public or civic services.** sectors.md has no library, council or civic sector. I had to triangulate from community venue, news/reading and education.

4. **`kinetic font split` is hard to find.**
   - It is mentioned only in the last paragraph of stacks/flutter.md, and in neither the router's engine reference (§7) nor the director agent.
   - All three directors told me to "split the .ttc with fontTools". fontTools is not installed, so I wrote my own TTC splitter before finding the built-in command.

5. **The word budget is unenforceable as written.**
   - clarity.md sets ≤ 45 words per first viewport, and the protocol uses `kinetic clarity` as evidence.
   - The tool's pixel heuristic reported ~29 words for hold-ready. All three critics hand-counted 55–66, docked layout_craft for it, and cited the 45-word budget I had copied into the premortem.
   - Either make the counter closer to reality (OCR-free: count glyph runs per line) or state the budget in the tool's own units.

6. **The editor never sees the panel.**
   - The editor isn't given the previous panel or lead.md, so it proposed reversing two consensus panel fixes:
     - loop 2: cut the shelf-letter plate;
     - loop 3: remove the time from the offline verdict.
   - The studio rule "a fix reversed by a later critic needs a reason that names the earlier one" applies to critics, not the editor. Give the editor lead.md too.

## Engine

7. **The deal ignored the brief's `never` and the priors.**
   - Challenger 2 was dealt the "specimen" engine, a uniform catalogue grid, for a brief that explicitly says "never a bookstore". I had to redraw it.
   - Both challengers got cream grounds (#FEF9F3, #FDFAF3), which priors.md calls spent and `scan` flags (D34).
   - Challenger 1's own type rule says "pair with a cool or green ground, not cream" next to its cream palette. That is an internal contradiction in one dealt option.

8. **Dealt Android faces are unusable offline.** Marcellus and Nunito Sans (the Android display faces) can't be bundled without network. The deal doesn't know which faces exist locally, so every director substituted a macOS face for Android. The deal should filter by `fc-list` / local font availability.

9. **`score` decides staleness by modification time.**
   - After the final panel I made a one-token spacing fix in an off-screen block, which cleared the scan's only major finding (D17 major → OK). I then re-rendered, and all 22 PNGs were byte-identical.
   - The verdict still flipped from SHIP-PENDING to ITERATE ("judgment predates the current renders/code").
   - Hash the renders, and ideally the changed files, instead of comparing mtimes. As it stands the rule punishes fixing a scan finding.

10. **The panel median can hide a capped dimension.**
    - Final layout_craft was [3, 4, 4], so the median is 4. The 3 came from the clarity & craft critic, who applied a documented cap ("rows under a sticky bar, cap 3") with specific evidence.
    - The panel reports no split (the disagreement is < 2), so a hard cap from the lens most qualified to judge it simply disappears. Consider "min of lens owner" for the dimensions a lens owns.

11. **Scan colour counts include drawn marks.** D13 counts the drawn marks' literal colours (enamel plate, spine cloth, tape) as colour chaos. `system.color.data` exists for data colours, but nothing tells you to declare vocabulary-mark materials there.

12. **Engine path friction.**
    - `kinetic init` names the product after the folder ("K").
    - `kinetic sheet` without `--out` doesn't print where the sheet went unless you read its first line.
    - Minor, but each one cost a round trip.

## Protocol and process

13. **Studio context cost is high.**
    - Every critic returns a ~4–6 KB JSON that the lead must save verbatim, because agents are read-only. With 3 critics × 3 loops plus directors and editors, most of the lead's context went to transcribing.
    - A writable `.kinetic/studio/inbox/` (or letting critics write their own file) would remove this.

14. **The last-loop rule conflicts with the editor step.**
    - The studio requires fix → render → editor → panel, and "never ship fixes nobody judged".
    - In the last loop that forces either skipping the editor or applying its cuts before the final panel. The protocol doesn't say which; I applied them before the panel.

15. **The XXL guidance conflicts with itself.**
    - Kinetic's binding advice (no lone last word, bind articles and numbers) improved 1.0x verdicts.
    - At 2.0x it produced ragged two-word lines, which two critics flagged.
    - Typography guidance should say to relax binding as the measure shrinks.

## Not Kinetic's fault, noted for the eval

- The scaffold's `test/render_test.dart` was missing from the project. I copied it unchanged from `../harness/render_test.dart`, the same file as `../render_test.dart`.
