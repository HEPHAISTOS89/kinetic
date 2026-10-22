# Color for mobile

Color in a designed app is a **system of roles**, not a set of swatches. The
average app (slop) uses default greys, one saturated brand color everywhere,
and a dark mode made by inverting. A designed app uses tinted neutrals, an
accent that *means* something, and two themes designed separately.

## 1. Work in OKLCH
OKLCH (lightness L 0–1, chroma C, hue H°) is perceptually even: equal steps
in L look like equal steps. HSL lies — a yellow and a blue at "50% lightness"
look nothing alike. Kinetic's engine does all color math in OKLab/OKLCH and
gamut-maps by reducing chroma (hue and lightness preserved).

```
kinetic palette "#C9A27E"            # roles for light + dark, contrast checked
kinetic palette "#C9A27E" --kdl      # paste-ready KDL `color` block
kinetic contrast "#5C5249" "#F2F1EE"  # WCAG 2 + APCA
```

## 2. Roles (what every KDL theme defines)
| Role | Job | Rule |
|---|---|---|
| `bg` | the canvas | near-white / near-black, tinted toward the seed hue |
| `surface` | raised content (cards, sheets, fields) | light: white or bg+1 step; dark: *lighter* than bg |
| `surface-2` | nested or pressed surfaces | one more step |
| `border` | hairlines, field outlines | low contrast (≈1.3–1.6:1 vs surface); separation, not decoration |
| `text` | primary text | ≥ 4.5:1 on bg *and* surface (aim ≥ 12:1 light, ≥ 11:1 dark) |
| `text-2` | secondary text | ≥ 4.5:1 — secondary is not "barely visible" |
| `text-3` | tertiary, placeholders, disabled | ≥ 3:1; never for information the user needs |
| `accent` | the one color that means "act here / this is yours" | ≥ 3:1 vs bg (non-text UI) |
| `on-accent` | text/icons on accent | ≥ 4.5:1 vs accent |
| `danger`, `success`, `warning` | status only | ≥ 3:1 vs bg; ≥ 4.5:1 when used as text |
| `focus` | keyboard/focus rings | ≥ 3:1 vs adjacent colors |

The validator checks the contrast pairs; `kinetic palette` derives a set that passes.

## 3. Tinted neutrals — the single biggest upgrade
Default greys (#F5F5F5, #9E9E9E, #E0E0E0) are hue-less and read generic.
Borrow the seed hue at very low chroma (OKLCH C ≈ 0.005–0.02):
- Warm products (food, home, wellness, night): neutrals toward H 60–80.
- Cool products (finance, tools, health-clinical): toward H 240–260.
- Brand-led: toward the brand hue.
One neutral ramp, used through roles. More than ~6 ad-hoc greys in code is D13.

## 3b. Warmth is a dial the brief sets (K34)
Blind critics scored Kinetic's colour lowest of every arm for three rounds
(3.4 vs 3.8–4.0) for one reason: **near-grey neutrals on friendly briefs**
("cold and austere", "clinical", "reads like a code editor at night"). The
competitors that won colour all did the same thing: warm tinted neutrals in
*both* themes, an accent from the product's world, a designed warm night.
- Read the brief's people and tone words (friendly, patient, community,
  volunteers, retired, encouraging, local). Any of them → **warm ground**:
  light neutrals at H 50–95, C 0.012–0.02 (oat, sand, putty, kraft,
  driftwood); text-2 carries the same hue. `kinetic deal` raises the chroma
  floor for warm briefs; `validate` flags grey neutrals under a warm thesis.
- Avoiding the cream-and-clay cluster (priors.md) is about **specificity, not
  temperature**. Generic parchment + terracotta is spent; this co-op's kraft,
  this coast's sand, this studio's oat are not. Never fix a cliché by going grey.
- Greyscale is a thesis ("an instrument, nothing else"), never the default for
  people-facing products. Even an instrument for volunteers is warm.

## 3c. The accent comes from the product's world (K36)
Name the accent after a material in the inventory before picking a hex:
glaze, soil, beet, stamp ink, buoy paint, heather, pine, saffron, brick.
- **UI link blue** (OKLCH H 245–272, C ≥ 0.13 — #1E4FD8, #2F6BFF, royal,
  cobalt) reads "default" to every critic, even with a story ("member's blue
  biro" lost the colour point in round 8). If the world is truly blue (water,
  sky, transit), use the world's blue: petrol, slate, sea-glass, Prussian —
  lower chroma, never the system link colour.
- A black filled button is not an accent: it reads as "no decision" on a warm
  brief. The primary action wears the accent.
- **One warm lift for encouraging moments**: a second, quiet warm tone
  (candlelight, ochre wash, sage) used only for done, thanks, a first time.
  A palette of ink + red has no way to say "well done" (round 8: "a little
  sombre for warm and encouraging").

## 4. Accent strategy by expression level
| Level | Strategy | Accent usage |
|---|---|---|
| 1 | neutral + one quiet accent | accent only for the primary action and selection |
| 2 | neutral + accent, or monochrome tinted | accent ≤ ~5% of the screen |
| 3 | accent + one supporting hue (category, data) | supporting hue never competes with actions |
| 4 | a dominant brand color as a surface | color blocks carry sections; text stays on high-contrast pairs |
| 5 | multiple saturated hues, deliberate | still role-based; every hue has a job |

Status colors are not accents: they appear only for status.

**Monochrome is a thesis, not a default.** An ink-only chrome (black buttons,
grey everything, color only from data) reads as generic to users and critics
unless the brand is genuinely typographic (editorial, luxury restraint). Most
products are better served by tinted neutrals + one chromatic accent with a
single meaning. `kinetic validate` flags an achromatic accent (K24). A screen where
the accent, red badges, a green chart and a purple header compete has no accent.

## 5. Dark mode is a second design, not an inversion
- **Surfaces get lighter as they rise** (tonal elevation): bg L≈0.16, surface
  L≈0.20, surface-2 L≈0.25 (OKLCH). Shadows barely read on dark.
- **Desaturate and lighten the accent**: a #3D5AFE that sings on white
  vibrates on black. Lift L to ~0.72 and reduce C by ~15%.
- **Text is not pure white**: L ≈ 0.90–0.93 (e.g. #EDE6DE warm, #DCDEE3 cool)
  avoids halation; pure #FFF on #000 at full size vibrates (C02 for OLED/media exceptions).
- Images and illustrations may need a dimmed variant.
- Test at 20% screen brightness (the night test).
- **The night has the brief's temperature.** A warm product's dark ground is a
  warm black (umber, olive or wet-sand black, L 0.17–0.20, C ≤ 0.012), never a
  blue-black or a neutral #1A1A1A ("an inversion, not a design"); a coastal or
  cool product may go blue-black.
- **The primary stays filled at night (K35).** Lift the accent (L 0.72–0.80,
  C × 0.85) and put dark ink on it. An outline or ghost primary in dark mode
  "fades at 20% brightness" (round 9, all three critics).
- **Every field and state surface has a night variant.** A pale hero, state
  band or coupon kept light in dark mode is the brightest slab on a black
  screen and glares; give it the same hue at L 0.25–0.35 (K35). Order of
  brightness is preserved: in dark, the primary button is the only light mass.

## 6. Light theme details
- bg slightly off-white (L 0.97–0.99) lets white `surface` cards lift without shadows.
- Avoid pure black text; L ≈ 0.20–0.25 (#1E1A16, #2A2E33) is softer and still ≥ 12:1.
- A white bg with white cards needs a border or shadow; an off-white bg with white
  cards needs neither — choose one elevation strategy (D16).

## 7. Gradients (D01, C04)
A gradient is earned when it **carries meaning**: time of day, temperature,
data intensity, a brand light. Then:
- 2–3 stops, adjacent hues (≤ 60° apart) or one hue in lightness;
- low chroma (C ≤ 0.12) for backgrounds;
- interpolate in OKLCH, not sRGB, to avoid the grey dead zone;
- never behind body text without a contrast check on its darkest/lightest frame.
The violet→pink "AI gradient" with no product meaning is D01.

## 8. Color and meaning
- Never encode information by color alone (F07): pair with icon, text or shape.
- Red/green pairs: add a second channel (arrow, sign, label) for color-blind users.
- Semantic consistency: if accent = "yours / actionable", don't use it for decoration.
- **Severity is a ladder with distinct steps**: routine notice (neutral or
  accent-soft), attention (ochre), danger (brick/red + icon + word). A gale
  warning in the same tint as a fee reminder has no urgency (round 7).
- **Each state its own step**: "full", "at risk" and "late" are different
  severities; three states in one ochre can't be told apart (round 11). Map
  them: late = quiet note tone, full = attention, at risk = attention + the
  decision time, cancelled = danger.
- **Good news is never alarm-coloured.** A rare bird, a new piece, a free slot
  are welcome: accent or the warm lift, never the danger hue (round 9: "a
  welcome rare bird reads as an error").
- **Soft alerts on warm products**: terracotta/brick reads as a neighbourly
  nudge, rose-red as a bank warning. Reserve true red for safety.
- Data color: sequential ramps from one hue for magnitude; diverging (two hues
  through neutral) for above/below; categorical ≤ 6 hues with similar L.

## 8b. Data colors are not accents
Transit lines, categories, calendar colors and chart series are **data**: they
come from the domain (a network's official line colors) or encode categories.
- Keep them in `system.color.data`, outside the role set and the accent budget.
- Each needs a foreground that passes on it (badge text) in both themes; dark mode may need a lifted variant.
- Never let data hues collide with status: if a line is officially red, closures
  still need an icon + word, not just "more red". Pick status hues that stay
  distinguishable from the data palette (e.g. a vermilion danger next to a crimson line + icon).
- With many data colors, the UI chrome must go quieter (neutral + one accent or no accent).

## 9. Brand colors
- `brand.status: strict` → keep the exact brand hex for logo/brand moments;
  derive UI roles from it (the brand hex may fail as text — derive a darker
  `accent` for text and actions and keep the brand hex for fills).
- A brand color that fails contrast as a button fill with white text is common
  (yellows, cyans, light greens): use dark `on-accent` text, or a deeper accent.
- Never let the brand color become every surface at expression ≤ 3.

## 10. Contrast standards
- **WCAG 2.x** (legal baseline in most markets): 4.5:1 body, 3:1 large text
  (≥ 24px, or ≥ 18.66px bold) and non-text UI components.
- **APCA Lc** (perceptual, reported alongside): ≈ 75 for body text, 60 for
  fluent/large text, 45 for large headlines and icons, 30 for non-text.
  APCA is better at dark-mode judgments; WCAG remains the gate.

## 11. Color slop (map to the catalog)
| Slop | ID |
|---|---|
| Violet/indigo/pink gradient as identity | D01 |
| Stock template seed (Material deepPurple) | D30 |
| 7+ unrelated greys | D13 |
| "Premium" = black + gold / beige-brass | D14 |
| Neon accent on pure black for a calm product | D14 |
| Accent used for decoration, status and actions at once | D13 |
| Dark mode by inversion; same saturated accent in both themes | K09 + judge |
| Grey neutrals on a warm brief; blue-black night for a warm product | K34 + judge |
| UI link blue as the accent of a product whose world isn't blue | K36 |
| Outline-only primary in dark mode; pale state slab kept light at night | K35 + judge |
| Gray text on colored backgrounds | F03 |
