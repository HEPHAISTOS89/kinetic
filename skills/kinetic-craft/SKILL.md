---
name: kinetic-craft
description: "Kinetic's visual precision layer for mobile UI: pixel-level craft (optical alignment, baselines, concentric radii, hairlines, rhythm, scrims, numerals), iconography systems and hand-built SVG icons that pass a lint, and meticulous detail review of UI code. Use for polish, icon work, custom SVGs, 'make it pixel-perfect', and the final pass of any Kinetic design."
---

# The last 10% is what people call taste

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

Most of the perceived quality of a premium app lives in details nobody
names. Review like a jeweller: one property at a time, across the whole screen.

## 1. Detail pass (run in this order on each screen)
1. **Edges** — one content edge; everything aligns to it or is clearly indented. No 2pt near-misses.
2. **Baselines** — rows with mixed sizes align on the first baseline; icon + label align on cap height center.
3. **Rhythm** — every gap is a scale token; inner gaps < outer gaps (≥ 1.5×). Equal spacing everywhere = no grouping.
4. **Radii** — ≤ 4 radii; nested corners follow `inner = outer − padding`; continuous corners on iOS.
5. **Hairlines** — 1 physical pixel (`1 / scale`) for separators on retina, in the `border` role, inset to the text edge on iOS lists.
6. **Type details** — tabular numerals where values change or align; units smaller/lighter; no orphan words in titles; no truncated critical text; title vs sentence case consistent.
7. **Color discipline** — accent only where it means "act / yours"; tertiary text never carries needed information; status colors only for status.
8. **Icons** — one family, weight matched to adjacent text weight, optical size per text style (17pt body → 17–20pt glyph), filled = selected only.
9. **Media** — consistent aspect ratios; focal point safe in every crop; scrims (≥ 4.5:1 for text) instead of text-shadow; placeholders the same size as the media.
10. **Touch** — targets ≥ 44/48 with ≥ 8pt separation; pressed states visible within 100ms.
11. **Both themes, both extremes** — check dark mode at low brightness and XXL text on the smallest phone before calling it done.

## 2. Code-level detail review (pointilleux)
Read the UI code like a reviewer who cares about pixels:
- Literal colors, sizes, paddings, radii, durations outside the token files → replace with tokens (`kinetic scan` lists them with file:line).
- `FittedBox` / `minimumScaleFactor` / `adjustsFontSizeToFit` / ellipsis on critical text → reflow (D28).
- Fixed widths/heights copied from mockups → constraints (D29).
- Icon-only buttons without labels (F07); hit areas shrunk (F05).
- Missing `const`/`@immutable`/stable keys that cause jank in animated lists (performance is perceived quality).
- Platform idioms: chevrons, back affordances, switches, pickers, sheets, haptics per platform (`knowledge/platform-*.md`).
Each fix: smallest diff, then `kinetic scan <file>` again.

## 3. Iconography and custom SVG
Default to the platform symbol set for system concepts (SF Symbols, Material
Symbols). Draw custom icons only for product-specific concepts, following
`knowledge/iconography-svg.md` exactly:
- `viewBox="0 0 24 24"`, live area 2–22 (round shapes may touch 1–23), one
  stroke width for the set (1.5 / 1.75 / 2), round caps and joins,
  `fill="none"` + `stroke="currentColor"`, coordinates on the 0.5 grid,
  primitives over long paths, ≤ 8 elements, no transforms/ids/styles.
- Use keyline shapes: circle Ø20, square 18, portrait 16×20, landscape 20×16 (optical balance).
- Selected variant: filled with `currentColor`, same outer size.
- Loop: draw → `kinetic svg lint <dir>` → fix → lint again, until clean. Then
  review at 16, 24 and 48px for gaps narrower than the stroke (SVG14) and optical size vs the set (SVG15).
- `kinetic svg fix <file> --write` normalizes ids/styles/colors/precision of
  imported icons; it does not bake transforms — redraw instead.

## 4. The signature detail
Execute the KDL `signature` with more care than anything else on the screen:
it is the one thing people will remember. Spec it fully (sizes, timing,
states, reduce-motion, dark mode) before coding.

## 5. Done when
The detail pass finds nothing on any key screen in both themes; `kinetic scan`
on changed files has no F and no major D; `kinetic svg lint` passes for custom icons.
