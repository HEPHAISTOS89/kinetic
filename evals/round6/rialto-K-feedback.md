# Kinetic v16 — candid feedback from this run (The Rialto, RN, create D2)

## The deal
- **Useful, kept with no redraw.** Option 2 (notebook engine + Futura "geometric poster" + tangerine on navy + weighty) fitted a cinema with uncanny precision. The box-office day sheet *is* a ruled page with times down the margin, Futura is the film-poster face, and "edits strike through and keep history" became the signature for the late, moved, cancelled and expired states. Without the deal I would have drawn a poster/showtime-chip layout or my usual serif-on-cream.
- **Option 1 dealt the lake-teal palette**, which `priors.md` itself lists as Kinetic's spent habit (teal accent on pale ground). The library still deals what the priors file forbids.
- **The dealt light accent fails its own contrast promise.** `#CB4B00` on `#F7FBFF` is 4.44:1. The deal says "contrast-checked roles", but the role fails AA body text, so I darkened it to `#B84300`.
- **The dealt "drop" spring [0.45, 0.75] is bouncy**, which the motion skill says to avoid on utility UI. I raised damping to 0.85. There is no `--redraw` for a parameter tweak, so this change is not logged anywhere except the KDL.
- **The engine geometry says "a 44pt margin column holds times".** A time at the dealt type size (Futura Bold 20) is about 55–62pt wide, so I needed 76pt. The geometry numbers were not checked against the dealt type ramp.
- **The dealt type rule contradicts priors.md.** It says "generous tracking on small labels" (label 13/16, 0.06em), while priors.md calls tracked ALL-CAPS labels template chrome. I confined caps labels to the margin day names and the wordmark.

## Engine
- **`export --stack react-native` emits `fontFamily: 'Futura'` plus `fontWeight: '700'`.** With bundled fonts, Android cannot select a weight inside a family, and on web this produced a faux-bold risk. I had to write `design/theme.ts` to map role → per-weight family (`Futura-Bold`, `Futura-Medium`) and reset `fontWeight`. KDL has no way to say "family + weight → file".
- **Naming per-weight families tripped D12.** `families: {display: Futura-Bold, label: Futura-Medium}` was counted as 3 families, over the budget. I collapsed it to `Futura`, which is what made the export wrong for RN (previous point).
- **`export` silently filled dark roles from light.** Before I added `on-field-2`, `field-line` and the other field roles to `dark`, `tokens.ts` dark already contained them, copied from light. `validate` only complained once a component referenced the missing dark token.
- **`scan` D34 flagged the dealt palette's own dark `danger` (`#E47C72`)** as a "terracotta/clay accent (generated-look tell)". The scanner and the deal library disagree. I removed the unused status roles instead.
- **D13 counts on-colours as neutrals.** `on-accent` `#26160F` and `on-field` `#FFFFFF` count toward the "9 neutrals" ramp, so the minor finding can't be resolved without deleting real roles.
- **D17 / D15 / D12 were useful.** They pushed me onto tokens and found 6 radii and 9 font sizes I wouldn't have counted. The `// optical:` exemption is a good mechanism.
- **K31 vocabulary vs code duplication.** The marks must exist as `.kinetic/vocab/*.svg` (linted) *and* as react-native-svg code, and nothing checks that they match. A `kinetic svg export --stack react-native` would remove the duplication.
- **`score` reaches ITERATE at a self-judged mean of 3.89, mostly from `native_fidelity: 3`.** The harness renders through react-native-web, so platform fidelity (ripple, predictive back, native tab bar) cannot be evidenced in the renders. With an honest self-judgment, a web-render harness caps the verdict.

## Instructions and knowledge
- **The D2 reading list is long (about 15 files plus 9 skills)** for a router that says "think (short)". The think skill alone has 8 steps. It was worth reading, but it is not short.
- **The dealt faces are macOS `.ttc` collections** (Futura.ttc, Charter.ttc, GillSans.ttc), and the brief's harness loads only .ttf/.otf. Nothing in Kinetic mentions this; with no fontTools available, I wrote a 40-line TTC splitter. The dealt Android alternative (Jost) is not available offline.
- **The RN stack file assumes Reanimated and expo-haptics.** The "Core Animated only" paragraph covered this sandbox well. Haptics → `none` is documented. Good.
- **`kinetic-direct` §4b says the hero is "the vocabulary's home"**, and the engine's ruled layout made margin marks (cue dot, reel, star) the natural carrier. Aligning a margin mark with a wrapped title needed measuring line counts (`onLayout`). The engine "risks" mention "ruling must follow the text ramp" but not this.
- **Agents (director, critic, rival, forensics) could not be launched.** The self-critique protocol is clear, and the identity-inventory and cover-the-logo tests were genuinely useful. I could not tell whether my 4/5 on distinctiveness is the usual +0.5 to +1 self-inflation the skill warns about.
