# Kinetic v17: where it was unclear, wrong or in the way (studio mode, create, D2)

Candid log kept during the Kiln home-screen run. Most important first.

1. **`kinetic clarity` contradicts the deal's own palettes.** The scorer marks `loud_share` as bad at 8 % of the
   screen and `loud_things` as bad at 3, but the dealt palettes prescribe a colour *field* ("orange field 10 %",
   option 1 "field 35 % (hero)"). A field of the size the deal asks for scores 0 on two components (30 % of the
   grade). With the dealt field plus one filled button, the home could not pass 72. I had to shrink the field to
   a 6 pt heat edge on closed states and keep the full field only when the kiln is the open station. The deal
   should cap field proportions at what clarity tolerates, or clarity should exempt the declared field.
2. **Clarity counts a dashed cobalt text button as a "loud area"** (the "Shelve a piece" slot) and cobalt display
   text as loud, so "one accent with one meaning" (sectors.md) and "cobalt for structure" (the dealt palette rule)
   push in opposite directions. I moved cobalt off the station words onto a 7 pt brush stroke (under the band
   threshold of 10 rows) mostly to satisfy a pixel heuristic. That is a design decision driven by a measurement artefact.
3. **The dealt type can be unreachable on the stack, and nothing says what to do.** "Wide signage" is SF Pro
   Expanded / Roboto Flex. React Native can't select a width trait by `fontFamily`, and neither face ships in the
   system folders the brief allows. `deal --redraw` only re-randomises. There is no "substitute with a stated stand-in"
   path, so I logged Superclarendon in `because` by hand. The library entries need a per-stack bundleable fallback.
4. **The deal weighted a "warm, hands-on" brief with a palette tagged `temperature: bold`** (cobalt and orange,
   cool porcelain neutral hue 255). The skill claims "warm and calm briefs are not dealt cool or loud palettes".
   It worked out (cobalt is a ceramic oxide), but the weighting claim did not hold.
5. **`kinetic export --stack react-native` emits `fontFamily: 'Superclarendon'` for a family whose files are one per
   weight** (`Superclarendon-Black`, `-Bold`). The brief/RN rule is family = file name, so the exported tokens don't
   render the display face. It also has no per-style family (my `display` and `index` need different weight files),
   and the README-style snippet uses Reanimated, which the brief disallows (the stack file does cover core `Animated`).
6. **Studio protocol gaps.** (a) Nothing says how long to keep `critic-*.json` across loops; `panel` globs every
   `critic-*.json`, so I archived loop files into subfolders by hand. (b) The editor is told to stay out of copy
   decisions about requirements, yet it cut "Wheel 8 is out until Friday" and a kiln line that served R4
   ("next firing"); a requirement check in the editor's procedure would catch that. (c) The director agent file
   lists Read/Glob/Grep tools but asks for real contrast values; directors ran the engine anyway via a general agent.
7. **`kinetic validate` F03 on data colours that are never text.** A line colour (`paper-ink`) needs an `on` text
   colour that passes 4.5:1 or validation is BLOCKED, although nothing is ever written on it. Data colours need a
   "stroke only" form.
8. **K21 reading-order check counts positions, not pixels.** The book button at reading position #5 was flagged as
   below the fold although it sits at y≈330 pt; I had to nest the verdict (`in:`) to silence it.
9. **D15 radius count includes 1-2 pt radii on hairlines** (plank ends), which no one perceives as a radius.
10. **KDL `families` budget (D12) counts two weights of one family as two families** when written as two keys;
    the docs don't say weights belong in the file list, not in `families`.
11. **Router reading list is long for D2** (think, direct, priors, identity-channels, sectors, states, system, code,
    motion, clarity, states, copy, layout, two platform files, the stack file, KDL.md, craft, critique,
    taste-rubric). In a studio run the lead never uses most of craft/critique because agents do; the D2 row could
    say "studio lead: skip craft/critique/taste-rubric, the agents read them".
12. **`kinetic init` names the product after the folder** (`name: K`) and writes `stack: mixed` without detecting
    the brief's stack; harmless but noisy.
13. **Harness interaction:** the harness type-checks every `.ts/.tsx` under the project except a fixed list of
    folders; my first idea (a `.k` symlink to the plugin at the project root) would have type-checked the plugin's
    own files. Kinetic could recommend keeping helper links inside `.kinetic/`.
14. **Stop rule vs. "consensus fixes done".** Loop 3's panel gave the same medians as loop 2 (color, layout_craft,
    native_fidelity 3), so the stop rule ends the studio, yet the panel still lists consensus fixes. Applying them
    after the last panel makes `kinetic score` say "judgment predates the current renders" and stay at ITERATE; not
    applying them leaves known fixes undone. The protocol should say which wins, or allow a cheap "confirm" re-judge.
15. **Critics swing on taste between loops.** Loop 1's identity critic asked for blue-white porcelain and cobalt
    station words; loop 3's clarity/identity critics asked for a bisque-warm ground and less cobalt on words. With
    a fresh context per loop there is no memory of what was already asked, so the lead ends up arbitrating
    reversals. Passing each critic its own previous sheet would reduce churn.
16. **Coordinator/limit resume message was stale** ("you were about to do tokens and vocabulary") — not Kinetic's fault,
    but the studio's file trail (`.kinetic/studio/loopN`) was what made resuming safe.
