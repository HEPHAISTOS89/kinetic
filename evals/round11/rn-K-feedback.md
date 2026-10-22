# Kinetic v2.1: candid feedback from this run (Sound, RN home, studio, create, D2)

## Most important
1. **The fold rule has no recipe, and my fix for it failed.** layout.md §3b says two things: no rows cut under a sticky bar, and no void over 130pt.
   - The harness renders a top-aligned crop, so in practice every state is judged at scroll position 0, and each state's content length differs.
   - Critics capped layout_craft at 3 in all three loops. In loop 1 the cause was cut rows. In loop 3 it was the voids that my push-below-the-fold fix created.
   - Kinetic gives neither a pattern nor a helper for this. A "fit whole rows into the remaining height" recipe, or a clarity check that flags cut rows, would have saved one loop.
2. **The clarity meter and the critics pulled the night attention field in opposite directions.**
   - The meter counts a large state-coloured field as a loud, non-quiet area. That dropped delay-dark to 68–70.
   - In loop 1 critics asked to lift the night ochre (#4A3510 → #5A4012). In loop 2 they asked to darken it again (#3F3218 or #4A3A22).
   - The field is the dealt engine's whole idea, so the meter should exempt the declared `field` role.
3. **The deal ignores the expression budget and the local machine.**
   - The type deal's display size of 56pt breaks the level-3 limit of 48. Validate flagged it (C/K07), and I scaled it down.
   - The deal named Barlow Condensed and Courier Prime. Neither is on macOS, and there is no network to fetch them. "Bundle the Android face for both" was impossible, so both directors had to substitute faces.
   - The deal should only offer faces that `kinetic font` can actually provide on this machine.
4. **The colour advice contradicts itself.**
   - color.md §3b wants a warm ground at H 50–95 and C 0.012–0.02. At L ≥ 0.93, D34 flags exactly that band as "cream/parchment".
   - The dealt palette itself (bg #FEF9F3, surface-2 #F7EFE5) trips D34. Final scan still reports the dealt surface-2 at D/info.
   - One director, and later a critic, spent effort steering around the conflict.
5. **The studio is expensive for the lead because of transcription.**
   - Agents return text and the lead re-types it into files. The panel JSONs were about 10k tokens each loop, copied by hand, which is error-prone and slow.
   - The critic definition already allows Bash. Letting critics and the editor write their own `.kinetic/studio/loopN/*.json` would remove this, and would also make "never edit a critique" enforceable.

## Other friction
- **Stop rule versus loop count:** "stop when two loops don't raise the median mean" and "max 3 loops; the last loop ends with a panel" leave no clean way to act on the final panel's fix. Loop 3's panel found a regression I had introduced (the voids), and the protocol forbade shipping a fix nobody judged. So the known issue ships, with verdict ITERATE (3.89).
- **No path to `ship` in this harness:**
  - `score` needs a judged mean of 4.0 or more.
  - Motion can never be judged from stills, so it always shows "! motion: not judged".
  - Nothing tells the lead what a realistic target is.
- **`kinetic init`** names the product after the folder ("K") and reports "no stack detected" in an empty folder. A `--stack` hint in the init call would help.
- **KDL `screens`:** this is one screen with 9 brief states. The schema has `reading_order` and `above_fold` per screen, not per state, so I serialised the states into `partial:`. A `variants` list per screen would fit state-driven homes better.
- **Vocabulary `file:`** must point to an existing file at validate time (K31). Writing the KDL before the code produced 7 noise findings.
- **scan D13** counts SVG drawing literals (a white highlight on a pin head, the QR paper) as theme leakage. Drawing internals should be exempt or marked differently.
- **Rival:** the rival agent definition is good and cheap, and critics used it well. But the studio skill does not say whether the rival should be rendered. A sketch was enough.
- **Editor:** loop-1 cuts lowered clarity at first (86 → 82). Shorter heroes pulled timetable rows into the viewport, and the meter counted those rows. The editor's predicted scores ignored that knock-on effect.
- **Directors:** all three converged on the same display face (DIN Condensed), because the authored direction and dealt option 1 both chose it. The validator only compares the axis strings, so it would not catch this real overlap.
- **The router's D2 reading list** is long (about 15 files across the phases). A one-page "studio quick path" covering what the lead must read and what each agent reads would cut context.
- **`kinetic panel`** reports only medians and consensus lines. Showing the mean and the per-dimension change against the previous loop would help apply the stop rule directly.
