# Iconography and SVG construction

Icons are typography for concepts. A set looks professional when every glyph
shares one grid, one stroke, one corner language and one optical weight — and
when it contains only the icons that help the user scan, recognise or act.

## 1. First decision: system icons or custom

| Situation | Use |
|---|---|
| System concepts: share, search, settings, delete, add, close, back, more, person, home, notifications | **SF Symbols** on iOS, **Material Symbols** on Android. Always. A custom "share" icon is a regression. |
| Cross-platform app with one visual identity (Flutter, React Native) | One family for both platforms, chosen deliberately: Material Symbols (variable weight/fill/grade), Phosphor, Lucide — or SF Symbols on iOS + Material Symbols on Android when native fidelity matters more than identity. |
| Product-specific concepts with no system equivalent (a domain object, a brand action) | Custom icons drawn **on the same grid and weight as the chosen family**, by the rules below. |
| Brand marks, illustrations | Not icons. Different rules (v2 imagery). |

### Mixing rules (D06)
- One family per app. If custom icons are added, they must be indistinguishable
  in weight, corners and proportions from the family.
- One style per role: outline for idle, fill for selected (tabs, toggles). Never
  mix filled and outline icons in the same row or list.
- Never emoji as icons. Never multicolor icons in chrome (multicolor only when
  the color *is* the information: weather, battery, file types).
- Leading icons in lists only when they help scanning (settings categories,
  file types). A decorative icon on every row is noise.

## 2. Sizes and alignment

| Context | iOS (SF Symbols) | Android / custom 24-grid |
|---|---|---|
| Inline with body text | follows text style (17pt body → symbol ≈ 17pt cap-matched) | 20dp |
| Nav bar / toolbar / app bar | `.body`–`.title3` scale, ~22pt | 24dp |
| Tab bar / navigation bar | system size (~25pt) | 24dp |
| List leading icon | 17–22pt, or 28–29pt in a rounded tile | 24dp, or 40dp avatar/tile |
| Empty state / feature | 44–64pt, hierarchical rendering | 48–64dp, one weight lighter optically |

- **Align to text, not to the box.** An icon next to a label is vertically centered
  on the label's cap height / x-height, not on the line box. SF Symbols do this
  automatically in `Label`; custom icons need a manual 0.5–1pt nudge.
- **Icon + label spacing**: 6–8pt (iOS), 8dp (Material) for horizontal pairs;
  4pt for compact chips; 4–6pt between icon and label stacked vertically in tab bars.
- Hit area ≥ 44pt / 48dp regardless of glyph size (F05).
- Scale icons with text size when they sit inside text (Dynamic Type / sp).
- Large icons look heavier: at ≥ 40px reduce stroke optically (use a lighter
  weight or a 1.5 stroke variant) so they match the visual weight of small ones.

## 3. Constructing SVG icons (rules checked by `kinetic svg lint`)

### The grid
- **Canvas**: `viewBox="0 0 24 24"`, `width="24" height="24"`.
- **Live area**: 20×20, from 2 to 22 on each axis. The *outer edge* of the stroke
  (geometry ± half the stroke width) stays inside it.
- **Overshoot zone**: round shapes (circles, arcs, round caps) may extend 1px further
  (1 → 23) because curves look smaller than straight edges at the same size.
- **Keyline shapes** (outer stroke edge):
  - circle: 20 diameter (r = 9 with a 2px stroke)
  - square: 18×18 (with a 2px stroke: `rect x="4" y="4" width="16" height="16"`, outer edge 3 → 21)
  - portrait rectangle: 16 wide × 20 tall (`rect x="5" y="3" width="14" height="18"`)
  - landscape rectangle: 20 wide × 16 tall (`rect x="3" y="5" width="18" height="14"`)
  Use the keyline that matches the glyph's dominant shape so the whole set reads
  at the same optical size: **circles are drawn slightly larger than squares**.

### Strokes
- **One stroke width for the whole set**: 2 (most common, best at small sizes),
  1.75, or 1.5 (lighter, premium feel at ≥ 24px; can look weak at 16px).
- **Caps and joins**: `stroke-linecap="round" stroke-linejoin="round"` for a soft set;
  `butt` + `miter` consistently for a sharp, technical set. Never mixed within a set.
- **Outline icons**: `fill="none"` on the root, `stroke="currentColor"`.
- **Color**: `currentColor` only. Icons inherit color from text/tint. No hex in icons.

### Pixel snapping
- A stroke is centered on its geometry. A **2px** stroke on an integer coordinate
  covers exactly two pixel columns at 1× (x−1 to x+1): crisp.
- A **1px or 3px** stroke must sit on a **.5** coordinate to cover whole pixels.
- A **1.5px** stroke can never be fully crisp at 1×; on 2× and 3× screens it maps to
  3 and 4.5 device pixels. Accept it, but keep coordinates on the 0.5 grid so the
  rendering is consistent across the set.
- **Rule**: every coordinate, length and radius is a multiple of 0.5. Off-grid values
  (11.37, 7.82) are the signature of auto-traced or AI-drawn icons.

### Geometry
- **Prefer primitives**: `circle`, `rect` (with `rx`), `line`, `polyline`, `polygon`,
  `ellipse`. They're readable, editable and stay on grid. Use `path` only when
  primitives can't express the shape, and keep it short.
- **Corner radius**: 2 on the 24 grid for rectangles (matches the 2px stroke with
  round joins). One radius language across the set.
- **≤ 8 drawable elements per icon.** More is an illustration, not an icon.
- **Gaps**: the white space between two strokes is ≥ the stroke width (2px), otherwise
  they merge at small sizes. Inner details are ≥ 2px long.
- **Angles**: prefer 0°, 45°, 90°. Diagonals at other angles alias.
- **Terminals**: open strokes end on the grid; a line ending 0.5px short of a shape
  reads as a mistake — either touch or leave a clear ≥ 2px gap.

### Forbidden in icon SVG
- `transform`, `style`, `class`, `id` attributes (unpredictable, non-themable).
- `<image>`, `data:` URIs, embedded raster.
- `<text>` (fonts aren't guaranteed), `<filter>`, `<style>`, `<script>`, `<foreignObject>`,
  gradients, external `<use href>`.
- Hardcoded colors (`#000`, `black`, `rgb()`), opacity tricks for structure.

### Filled variant (selected state)
- Same outer silhouette, same stroke width kept as a stroke **and** `fill="currentColor"`,
  so the filled icon has exactly the same optical size as the outline.
- Interior details become **counters** (knocked out): draw them with a contrasting
  approach — omit them, or keep them as strokes over the fill only if the platform
  renders them in the background color. The simplest robust rule: a filled variant
  keeps the silhouette and drops interior details that would need a second color.
- Only shapes that enclose an area get filled (house, bell, bookmark). Line-only
  glyphs (plus, search lens handle) stay outline and show selection by weight or color.

## 4. `kinetic svg lint` rules

| ID | Rule | Severity | Check |
|---|---|---|---|
| SVG01 | Root has `xmlns` and `viewBox="0 0 24 24"` | error | auto |
| SVG02 | Only allowed elements: `svg g path circle rect line polyline polygon ellipse` | error | auto |
| SVG03 | No `transform`, `style`, `class`, `id` attributes | error | auto |
| SVG04 | Color values only `currentColor` or `none` | error | auto |
| SVG05 | One stroke width per icon and across the set; allowed 1.5, 1.75, 2 | error | auto |
| SVG06 | Consistent `stroke-linecap`/`stroke-linejoin` across the set (default round/round) | warning | auto |
| SVG07 | Outline icons declare `fill="none"`; fills, if any, are `currentColor` | error | auto |
| SVG08 | ≤ 8 drawable elements | warning | auto |
| SVG09 | All coordinates, lengths and radii are multiples of 0.5 (arc flags excluded) | warning | auto |
| SVG10 | Geometry ± half stroke within [2, 22]; round shapes may reach [1, 23] | warning | auto (conservative bbox from points and control points) |
| SVG11 | Path data ≤ 200 characters per `path`; prefer primitives | info | auto |
| SVG12 | No raster, `data:` URIs, `<image>`, `<text>`, filters, gradients, scripts | error | auto |
| SVG13 | Rectangle corner radius consistent across the set (2 on the 24 grid) | warning | auto |
| SVG14 | Gaps between strokes ≥ stroke width; details ≥ 2px | warning | judge (render at 16, 24, 48px) |
| SVG15 | Optical size matches the set (keyline chosen correctly) | warning | judge |

## 5. Reference set (passes every auto rule: 2px stroke, round caps/joins, 0.5 grid)

### home
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="3 11 12 4 21 11"/>
  <path d="M5 10v10h14V10"/>
  <path d="M10 20v-6h4v6"/>
</svg>
```

### search
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="7"/>
  <line x1="16" y1="16" x2="21" y2="21"/>
</svg>
```

### bell
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4l2-2z"/>
  <line x1="10" y1="21" x2="14" y2="21"/>
</svg>
```

### bell — filled (selected)
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4l2-2z" fill="currentColor"/>
  <line x1="10" y1="21" x2="14" y2="21"/>
</svg>
```

### calendar
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="5" width="18" height="16" rx="2"/>
  <line x1="3" y1="10" x2="21" y2="10"/>
  <line x1="8" y1="3" x2="8" y2="7"/>
  <line x1="16" y1="3" x2="16" y2="7"/>
</svg>
```

### check-circle
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="9"/>
  <polyline points="8 12.5 11 15.5 16 9"/>
</svg>
```

### plus
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="12" y1="5" x2="12" y2="19"/>
  <line x1="5" y1="12" x2="19" y2="12"/>
</svg>
```

### settings (sliders — not the gear cliché)
Each track stops 2px before its knob so the knob reads as a separate object.
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4 6h9M17 6h3"/>
  <circle cx="15" cy="6" r="2"/>
  <path d="M4 12h3M11 12h9"/>
  <circle cx="9" cy="12" r="2"/>
  <path d="M4 18h10M18 18h2"/>
  <circle cx="16" cy="18" r="2"/>
</svg>
```

### moon
Outer arc r 8.5, inner bite r 7.5; both arcs end on grid points.
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20 14A8.5 8.5 0 1 1 10 4a7.5 7.5 0 0 0 10 10z"/>
</svg>
```

## 6. Review checklist (judge, at 16, 24 and 48px, light and dark)
1. Line the set up in a row: do any glyphs look bigger, darker or lighter than the others?
2. At 16px, does any detail merge or disappear?
3. Do circles feel the same size as squares? (If the circle looks small, it's on the square keyline.)
4. Do selected (filled) icons keep the same silhouette as idle ones?
5. Next to body text, does the icon sit on the text's optical center?
6. Remove the label: is the meaning still recognisable? If not, the label is mandatory (F07).
