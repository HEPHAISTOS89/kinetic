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
kinetic contrast "#5C5249" "#F6F1EA"  # WCAG 2 + APCA
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
| Gray text on colored backgrounds | F03 |
