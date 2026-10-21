# Directions — legacy reference (v1.5)

> Since v1.6 directions are **dealt** by `kinetic deal` from `knowledge/library/`
> (engines, native type systems, palettes with fields, motion personalities).
> This file stays as reference for ramps and token sets. Several of its type
> choices (Inter, Fraunces, DM Sans, Space Grotesk, IBM Plex, a cream ground)
> are now listed as spent in `priors.md`: don't pick them by default.

A model with no target designs the average app. This library gives it fourteen
specific targets, each a complete, internally consistent system with numbers
you can paste into KDL `system`. They are **starting points, not costumes**.

## How to use it

1. **Shortlist from the thesis, not the sector.** Read `thesis.feel`,
   `thesis.never` and `expression.level`, then use the selection table below.
   Shortlist 3 directions that differ on structure, color strategy and type
   voice. These become the `directions` A/B/C in KDL.
2. **Pick one, or blend two, deliberately.**
   - Take **structure** (grid, density, spacing, elevation, shape) from one
     direction and **voice** (type families, accent, motion personality) from
     the other.
   - **Never average two palettes.** Averaging gives mud. One direction owns
     color.
   - Never blend three. Three sources give a collage.
3. **Mutate from the product.** Change at least three things so the result
   belongs to this product: the accent hue (derive it from the brand seed or
   the spine), one type role, and the signature move. If the result could ship
   unchanged for a competitor, you haven't mutated enough (run the swap test in
   anti-slop.md).
4. **Respect the expression budget** of the chosen level (see KDL.md). Each
   direction states a range. Outside that range it breaks.
5. **Verify.** The palettes below pass WCAG checks as given (text/bg,
   text/surface, text-2/bg, text-2/surface ≥ 4.5; on-accent/accent ≥ 4.5;
   accent/bg and accent/surface ≥ 3.0, in both light and dark). Every change
   you make must go through `kinetic contrast` again.

Notation: type ramp `role size/line weight track(em)`. Sizes are pt (iOS) and
dp/sp (Android). Springs use `{response s, damping ratio}`: SwiftUI
`.spring(response:dampingFraction:)`, Flutter `SpringDescription.withDampingRatio`,
Compose `spring(dampingRatio, stiffness)` (stiffness ≈ (2π/response)²).

## Selection table

| # | Direction | Expression | Stakes it tolerates | Density | Fits best |
|---|---|---|---|---|---|
| 1 | Swiss Instrument | 1–2 | high | medium–high | finance, tools, transit |
| 2 | Editorial Serif | 2–3 | low–medium | low–medium | reading, journaling, culture |
| 3 | Warm Paper Night | 2 | low | low | sleep, reflection, evening use |
| 4 | Quiet Native | 1 | any | medium | utilities, settings-heavy, productivity |
| 5 | Mono-Accent Bold | 3–4 | low–medium | medium | consumer brands, launches, commerce |
| 6 | Brutal Tabular | 2–3 | medium–high | high | trading, analytics, devtools, logistics |
| 7 | Soft Tactile | 3 | low–medium | low–medium | wellness, habits, family, nutrition |
| 8 | Cinematic Dark | 4 | low | low | streaming, music, photo, events |
| 9 | Playful Geometric | 4–5 | low | low–medium | kids, learning, social games |
| 10 | Luxe Restraint | 2 | medium | low | private banking, hospitality, fashion |
| 11 | Field High-Contrast | 1–2 | high | medium | outdoor, workforce, field service, navigation |
| 12 | Clinical Calm | 1–2 | high | medium | health, medical, insurance |
| 13 | Kinetic Sport | 4–5 | low–medium | medium | fitness, running, sport live |
| 14 | Gallery Whitespace | 2–3 | low | low | portfolio, art, architecture, premium retail |

---

## 1. Swiss Instrument
**Essence:** a precision instrument. Grid, figures and one signal color.
**Range:** 1–2. **Fits:** banking, budgeting, transit, timers, B2B tools. **Misfits:** wellness, kids, anything that should feel warm.
**Type:** SF Pro (iOS), Inter (Android/cross-platform). Use system fonts here: they are the best grotesque on each platform. Ramp: `display 34/40 700 -0.02` · `title 22/28 600 -0.01` · `headline 17/22 600 0` · `body 17/24 400 0` · `callout 15/20 400 0` · `caption 12/16 500 0.02` · `micro 11/13 600 0.04 (caps sparingly)`. Numerals: tabular, lining, always.
**Color (strategy: neutral + one signal accent):**
- light: bg `#FFFFFF` · surface `#F4F4F2` · text `#111111` · text-2 `#5E5E5A` · border `#E2E2DE` · accent `#D7261E` · on-accent `#FFFFFF`
- dark: bg `#0B0B0B` · surface `#171717` · text `#F2F2F0` · text-2 `#A3A39E` · border `#2A2A28` · accent `#FF5A4E` · on-accent `#1A0503`
**Space:** unit 4, margins 16/20, density medium-high; 8-pt rhythm between rows, 24 between groups. **Shape:** radius s 4 · m 8 · l 12; corners circular (sharpness is the voice). **Elevation:** border (hairline 0.5–1px), no shadows.
**Icons:** SF Symbols / Material Symbols outlined, weight regular, 20pt; filled only for selection. **Motion:** fast, exact, critically damped: `snap {0.25, 1.0}`, `move {0.35, 1.0}`, fade 150ms; no overshoot. **Haptics:** crisp `selection` on value change, `rigid` on commit.
**Signature moves:** figures that tick digit by digit when they update (monospaced digits, per-digit roll); a single red element per screen, reserved for the one thing that needs attention; hairline rules in place of containers.
**Never:** rounded pill buttons with gradients; more than one accent; decorative icons on rows.

## 2. Editorial Serif
**Essence:** a well-set magazine page. Typography does the art direction.
**Range:** 2–3. **Fits:** reading, newsletters, journaling, books, culture, recipes. **Misfits:** dense operational tools, high-frequency transactional flows.
**Type:** New York (iOS system serif) or Fraunces / Instrument Serif for display; SF Pro / Inter for UI text. On iOS, New York is free, native and Dynamic Type-ready; prefer it. Ramp: `display 40/44 400 -0.02 serif` · `title 26/32 500 -0.01 serif` · `headline 17/22 600 0 sans` · `body 18/27 400 0 serif (reading)` · `ui 16/22 400 0 sans` · `caption 13/18 500 0.01 sans` · `kicker 12/16 600 0.06 sans caps`. Numerals: oldstyle in prose, lining in UI.
**Color (strategy: warm neutral + ink accent):**
- light: bg `#FBF8F3` · surface `#FFFFFF` · text `#1C1A17` · text-2 `#5F5850` · border `#E8E1D6` · accent `#8C2F1B` · on-accent `#FFFFFF`
- dark: bg `#121110` · surface `#1C1A18` · text `#EEE8DF` · text-2 `#A9A095` · border `#2E2A26` · accent `#E08A6E` · on-accent `#2A0E05`
**Space:** unit 4, margins 20/24, measure 32–38 em for reading, generous leading. **Shape:** radius s 2 · m 6 · l 10; almost square. **Elevation:** none or border; hierarchy from type and space.
**Icons:** thin outline (SF Symbols light/regular), used rarely; text buttons over icon buttons. **Motion:** page-like and calm: `turn {0.45, 0.95}`, `settle {0.5, 1.0}`, fade 240ms; text never animates letter by letter. **Haptics:** almost none; `soft` on save.
**Signature moves:** a drop cap or oversized first numeral on the lead story; section kicker plus serif headline pairs; reading progress shown as a hairline at the top edge.
**Never:** serif for buttons and labels; justified text on a phone; serif mixed with a second display serif.

## 3. Warm Paper Night
**Essence:** a lamp-lit page at night. Warm, dim, unhurried.
**Range:** 2. **Fits:** sleep, meditation, journaling, evening reading, reflection. **Misfits:** daytime productivity, finance, anything that needs urgency.
**Type:** New York or Fraunces (opsz soft) for numerals and display; SF Pro Rounded / Manrope for UI. Ramp: `display 40/44 300 -0.02` · `title 22/28 600 -0.01` · `body 17/24 400 0` · `callout 15/21 400 0` · `caption 13/18 500 0.01`. Numerals: proportional for display, tabular in data.
**Color (strategy: monochrome warm, dark-first):**
- light: bg `#F2F1EE` · surface `#FFFDF9` · text `#1E1A16` · text-2 `#5C5249` · border `#E4DAD0` · accent `#8A5A2B` · on-accent `#FFFFFF`
- dark: bg `#0F0D0B` · surface `#1A1714` · text `#EDE6DE` · text-2 `#A89C90` · border `#2C2722` · accent `#D9A877` · on-accent `#1E1408`
**Space:** unit 4, margins 24, density low; content gravitates to the lower half of the screen (thumb and lying-down posture). **Shape:** radius s 10 · m 16 · l 24, continuous. **Elevation:** tonal only (surface steps of about 3% lightness).
**Icons:** SF Symbols regular, rounded where available, 22pt. **Motion:** slow, heavily damped: `gentle {0.55, 1.0}`, `breath {1.2, 1.0}`, fade 300ms; nothing faster than 250ms. **Haptics:** `soft` only, low intensity.
**Signature moves:** the background tint follows the real clock (warmer and darker toward bedtime); one large light-weight numeral as the hero; no pure white anywhere at night.
**Never:** blue accents (they read alert/awake); bouncy springs; gold (D14).

## 4. Quiet Native
**Essence:** the platform itself, perfectly tuned. Invisible design that feels "of course".
**Range:** 1. **Fits:** utilities, settings-heavy apps, productivity, enterprise. **Misfits:** brand-led consumer launches that need to be remembered.
**Type:** system only: SF Pro with the platform Dynamic Type styles; Roboto Flex / the M3 type scale on Android. Ramp (iOS defaults, size/line weight): `largeTitle 34/41 700` · `title2 22/28 700` · `headline 17/22 600` · `body 17/22 400` · `subheadline 15/20 400` · `footnote 13/18 400` · `caption 12/16 400`. Tracking: write `track: 0` in KDL — SF applies its own optical tracking per size (≈ +0.01em at 34pt, ≈ −0.025em at 17pt); adding it again doubles it. Numerals: tabular in lists.
**Color (strategy: system neutrals + one chosen tint, never the default blue untouched, D30):**
- light: bg `#F2F2F7` · surface `#FFFFFF` · text `#000000` · text-2 `#6C6C70` · border `#D8D8DD` · accent `#1F6F5C` · on-accent `#FFFFFF`
- dark: bg `#000000` · surface `#1C1C1E` · text `#FFFFFF` · text-2 `#AEAEB2` · border `#38383A` · accent `#4FC3A6` · on-accent `#00261C`
**Space:** platform defaults: 16 margins (iOS), 16/24 (M3); inset grouped lists. **Shape:** iOS radius s 8 · m 10 · l 16 continuous; M3 shape scale. **Elevation:** platform (grouped backgrounds on iOS, tonal elevation in M3).
**Icons:** SF Symbols / Material Symbols with hierarchical rendering; follow the platform. **Motion:** platform defaults: iOS `.smooth` ≈ `{0.5, 1.0}`, `.snappy` ≈ `{0.3, 0.85}`; M3 standard easing, 200–300ms. **Haptics:** platform semantics (`selection`, `success`, `warning`).
**Signature moves:** one custom tint applied with discipline everywhere; a single bespoke component (for example the main list row) crafted to a level beyond stock; native sheets with detents instead of custom modals.
**Never:** cross-platform chrome (D24); custom navigation bars that break back-swipe; decoration that the platform wouldn't do.

## 5. Mono-Accent Bold
**Essence:** one loud color, everything else disciplined. A poster with a grid.
**Range:** 3–4. **Fits:** consumer brands, commerce, launches, food delivery, events. **Misfits:** medical, high-stakes finance, long reading.
**Type:** Inter Display / SF Pro Display heavy for display; Inter / SF Pro text. Alternatively Space Grotesk display for a more technical voice. Ramp: `display 48/50 800 -0.03` · `title 28/32 700 -0.02` · `headline 18/24 700 -0.01` · `body 16/24 400 0` · `label 15/20 600 0` · `caption 12/16 600 0.02`. Numerals: lining, tabular in prices.
**Color (strategy: neutral + one saturated accent used in large fields):**
- light: bg `#FFFFFF` · surface `#F5F3EE` · text `#0E0E0E` · text-2 `#55534E` · border `#E6E3DC` · accent `#E64500` · on-accent `#0E0E0E`
- dark: bg `#0E0E0E` · surface `#1A1A1A` · text `#F5F3EE` · text-2 `#A6A39C` · border `#2B2B2B` · accent `#FF6A1F` · on-accent `#140500`
Note: dark text on the orange accent is intentional. White on this orange fails 4.5.
**Space:** unit 4, margins 20, density medium; big jumps (48+) between sections. **Shape:** radius s 6 · m 12 · l 20 · full for the primary CTA only. **Elevation:** none; color fields create the layers.
**Icons:** filled, bold weight, 24pt; few. **Motion:** confident with a slight overshoot on reveal moments: `pop {0.32, 0.78}`, `move {0.38, 0.9}`, fade 180ms. **Haptics:** `medium` impact on primary actions.
**Signature moves:** the accent floods an entire surface at one key moment (order placed, booking confirmed); oversized heavy numerals for price or ETA; the accent never appears in more than two places per screen.
**Never:** a second saturated color; gradient on the accent (D01); accent body text.

## 6. Brutal Tabular
**Essence:** data, honestly shown. Rules, columns, monospaced figures, no ornament.
**Range:** 2–3. **Fits:** trading, analytics, devtools, logistics, ops dashboards on mobile. **Misfits:** onboarding-heavy consumer apps, wellness.
**Type:** IBM Plex Sans + IBM Plex Mono (free) or SF Pro + SF Mono. Ramp: `display 32/36 600 -0.02` · `title 20/24 600 -0.01` · `body 15/20 400 0` · `data 15/20 500 0 mono tabular` · `label 12/16 600 0.04 caps` · `micro 11/14 500 0.02 mono`. Numerals: tabular, slashed zero in mono.
**Color (strategy: black and white + one electric accent; semantic up/down colors kept separate):**
- light: bg `#FFFFFF` · surface `#F7F7F7` · text `#000000` · text-2 `#4D4D4D` · border `#000000` · accent `#0038FF` · on-accent `#FFFFFF`
- dark: bg `#000000` · surface `#0D0D0D` · text `#FFFFFF` · text-2 `#B3B3B3` · border `#FFFFFF` · accent `#7A9CFF` · on-accent `#000000`
Semantic: up/down must be distinguishable by sign and arrow as well as color (F07).
**Space:** unit 4, margins 12/16, density high; row height 44 minimum for touch. **Shape:** radius 0 everywhere (full only for status dots). **Elevation:** border, 1px solid, as structure.
**Icons:** minimal, outlined, 18pt, often replaced by text labels. **Motion:** none decorative; value changes flash the cell background for 400ms; `snap {0.2, 1.0}`. **Haptics:** `selection` on scrubbing a chart; `rigid` on order placement.
**Signature moves:** a live table whose updated cells flash then settle; column headers that sort with an exact arrow; a scrubbable sparkline with crosshair readout.
**Never:** soft shadows or rounded cards (the voice dies); color-only gain/loss; chart junk.

## 7. Soft Tactile
**Essence:** soft and friendly, with disciplined structure underneath. Pastel tints, a firm grid.
**Range:** 3. **Fits:** habits, wellness, nutrition, family organisers, journaling for younger audiences. **Misfits:** pro tools, finance, anything urgent.
**Type:** SF Pro Rounded / Nunito for display; SF Pro / DM Sans for text. Ramp: `display 34/40 700 -0.01 rounded` · `title 22/28 700 0 rounded` · `headline 17/22 600 0` · `body 17/24 400 0` · `callout 15/20 500 0` · `caption 13/18 500 0.01`. Numerals: rounded, proportional.
**Color (strategy: warm neutral base + deep accent + 3 pastel category tints used as fills only):**
- light: bg `#F4F1EC` · surface `#FFFFFF` · text `#22201D` · text-2 `#5E5A54` · border `#E6E0D7` · accent `#2F6B4F` · on-accent `#FFFFFF`
- dark: bg `#151513` · surface `#201F1C` · text `#EFECE6` · text-2 `#ABA69E` · border `#34322E` · accent `#8FCCAA` · on-accent `#0B2418`
- category tints (light, fills behind dark text only): sage `#DCEBE2` · peach `#F6DCCB` · mist `#DDE3F3` (text on each ≥ 12:1). In dark, derive the tints at roughly 18% lightness with the same hue.
**Space:** unit 4, margins 20, density low–medium, 12 between related items. **Shape:** radius s 12 · m 18 · l 28, continuous; pills for chips. **Elevation:** tonal plus very soft shadow on draggable elements only (y 2, blur 8, 6% opacity).
**Icons:** rounded, filled duotone in category tints, 24pt; one family. **Motion:** soft, slightly springy for direct manipulation: `squish {0.35, 0.72}` on press, `settle {0.45, 0.9}`, fade 200ms. **Haptics:** `soft` on check-off, `light` on drag pickup.
**Signature moves:** completing an item compresses it like a pressed button, then a calm tick; category tints carry the information architecture (not decoration); progress shown as a filled shape, not a ring.
**Never:** more than 3 tints; pastel text (fails contrast); confetti (D27).

## 8. Cinematic Dark
**Essence:** the content is the light source. The UI recedes into black.
**Range:** 4. **Fits:** streaming, music, photo and video, events, gaming hubs. **Misfits:** forms-heavy flows, finance, health.
**Type:** SF Pro Display / Inter Tight, condensed weights for titles. Ramp: `display 44/46 800 -0.03` · `title 24/28 700 -0.02` · `headline 17/22 600 -0.01` · `body 15/21 400 0` · `meta 13/18 500 0.01` · `badge 11/13 700 0.06 caps`. Numerals: tabular for times.
**Color (strategy: dark-first, accent sampled from content where possible; fallback accent below):**
- light: bg `#FAFAFA` · surface `#FFFFFF` · text `#0A0A0A` · text-2 `#5A5A5A` · border `#E3E3E3` · accent `#C8102E` · on-accent `#FFFFFF`
- dark: bg `#050505` · surface `#121212` · text `#F5F5F5` · text-2 `#9E9E9E` · border `#262626` · accent `#FF3B4E` · on-accent `#1A0004`
**Space:** unit 4, margins 16, edge-to-edge media, density low. **Shape:** radius s 6 · m 10 · l 16 for posters; media full-bleed. **Elevation:** scrims and gradients from the media (black 0→80% over the bottom 40%). This is the one place where a gradient carries meaning (C04).
**Icons:** filled, 24–28pt, white at 90% opacity over media. **Motion:** cinematic shared-element transitions: `hero {0.5, 0.88}`, `sheet {0.42, 0.9}`, crossfade 300ms; parallax only on the hero poster, 0.2 ratio max. **Haptics:** `light` on play/pause, `medium` on scrub snap points.
**Signature moves:** the poster expands into the detail screen (matched geometry / Hero); the ambient background picks up the dominant color of the artwork at 15–20% opacity; the playback scrubber becomes the main control in landscape.
**Never:** light grey cards on black; text over media without a scrim (F03); blur on everything (D05).

## 9. Playful Geometric
**Essence:** bold primary shapes, ink on paper, joyful but legible.
**Range:** 4–5. **Fits:** kids, learning, social games, creative tools for beginners. **Misfits:** finance, medical, enterprise.
**Type:** Space Grotesk or DM Sans heavy for display; DM Sans / SF Pro Rounded text. Ramp: `display 44/48 800 -0.02` · `title 26/30 700 -0.01` · `headline 18/24 700 0` · `body 17/24 500 0` · `label 15/20 700 0.01` · `caption 13/18 600 0.02`. Numerals: proportional, large.
**Color (strategy: ink navy + coral accent + 2 supporting primaries as shape fills):**
- light: bg `#FFF8EC` · surface `#FFFFFF` · text `#1A1446` · text-2 `#4C4770` · border `#EDE3CF` · accent `#F65A30` · on-accent `#1A1446`
- dark: bg `#120F2A` · surface `#1D1940` · text `#FFF8EC` · text-2 `#B9B3D9` · border `#2F2A5C` · accent `#FF7A5C` · on-accent `#1A0A05`
- supporting fills (shapes and backgrounds behind ink text): sun `#FFC93C` (ink on it 11:1), sky `#7FA4FF` (ink on it 7:1)
Note: ink-on-coral is intentional. White on this coral fails 4.5.
**Space:** unit 8, margins 20, density low; big tap targets (56+). **Shape:** mixed geometry by meaning (circle = person, square = content, triangle = action); radius m 16 · l 28. **Elevation:** hard offset shadow (x 0, y 4, no blur, ink at 100%) on primary buttons only.
**Icons:** custom thick-stroke (2.5px at 24) geometric icons, or Phosphor bold. **Motion:** expressive overshoot: `boing {0.4, 0.6}` for rewards, `press {0.25, 0.7}`, fade 160ms. **Haptics:** `success` notification on milestones only.
**Signature moves:** the hard offset shadow collapses on press (the button physically goes down); shapes that rearrange to celebrate a milestone; the mascot replaced by geometry (no generic character, D07).
**Never:** more than 3 colors on one screen; childish copy for adults; rewards for non-achievements (D27).

## 10. Luxe Restraint
**Essence:** premium as precision and silence. Deep neutral tones, no gold, no black-and-gold.
**Range:** 2. **Fits:** private banking, hospitality, fashion, members' clubs, high-end real estate. **Misfits:** mass-market discount retail, kids.
**Type:** a refined grotesque (SF Pro with tight tracking, or Inter) plus an elegant serif for rare display (New York, or Instrument Serif). Ramp: `display 36/42 300 -0.02 serif` · `title 20/26 500 -0.005` · `headline 15/20 600 0.02 caps-small` · `body 16/24 400 0` · `caption 12/16 500 0.04` · `price 22/26 400 -0.01 tabular`. Numerals: lining, tabular for amounts.
**Color (strategy: deep green-graphite monochrome; luxury signalled by restraint and material, not metallics):**
- light: bg `#F7F6F3` · surface `#FFFFFF` · text `#1B1B1A` · text-2 `#61605B` · border `#E3E1DB` · accent `#2E3A33` · on-accent `#F7F6F3`
- dark: bg `#101211` · surface `#1A1C1B` · text `#ECEAE4` · text-2 `#A3A19A` · border `#2B2E2C` · accent `#C9D1C4` · on-accent `#141714`
**Space:** unit 4, margins 24/28, density low; whitespace is the luxury. **Shape:** radius s 2 · m 4 · l 8; corners nearly square. **Elevation:** hairline borders; one soft shadow for floating cards (y 8, blur 24, 5%).
**Icons:** thin outline (light weight), 20pt, sparing. **Motion:** slow and silky, never springy: `glide {0.6, 1.0}`, fade 320ms, ease-out cubic(0.2, 0, 0, 1). **Haptics:** `soft`, rare.
**Signature moves:** a single serif line used once per screen; amounts set large and light; transitions that fade through the surface color rather than slide.
**Never:** gold, brass or black+gold (D14); bold heavy type; badges and promos (D25).

## 11. Field High-Contrast
**Essence:** readable in sunlight with gloves on. Maximum legibility, huge targets.
**Range:** 1–2. **Fits:** field service, workforce, outdoor sports, navigation, construction, agriculture. **Misfits:** lifestyle and luxury.
**Type:** SF Pro / Roboto, heavier weights and larger sizes than usual. Ramp: `display 36/40 800 -0.02` · `title 24/30 700 -0.01` · `body 19/26 500 0` · `label 17/22 700 0` · `caption 15/20 600 0.01`. Body minimum 17. Numerals: tabular, heavy.
**Color (strategy: black and white + high-visibility accent; semantic colors also carry shape):**
- light: bg `#FFFFFF` · surface `#F0F0F0` · text `#000000` · text-2 `#3D3D3D` · border `#8A8A8A` · accent `#B54700` · on-accent `#FFFFFF`
- dark: bg `#000000` · surface `#141414` · text `#FFFFFF` · text-2 `#C7C7C7` · border `#6B6B6B` · accent `#FFB000` · on-accent `#000000`
**Space:** unit 8, margins 16, density medium; targets 56–64, spacing between targets ≥ 12. **Shape:** radius s 6 · m 10 · l 14. **Elevation:** thick borders (2px) for focus and selection, no shadows (they disappear in sun).
**Icons:** filled, bold, 28pt, always paired with a text label. **Motion:** minimal and instant feedback: `snap {0.2, 1.0}`, fade 120ms; nothing that delays reading. **Haptics:** strong `heavy`/`success`/`error`, because eyes are often elsewhere.
**Signature moves:** one-thumb bottom action bar with 2 giant actions; status conveyed by color, shape and word together; offline state promoted to a first-class, always-visible indicator.
**Never:** light grey text; thin weights; gesture-only actions.

## 12. Clinical Calm
**Essence:** calm competence. Trustworthy, clear, never cold.
**Range:** 1–2. **Fits:** health, medical, telehealth, insurance, pharmacy. **Misfits:** entertainment, gaming.
**Type:** SF Pro / Inter, regular weights; never condensed. Ramp: `display 32/38 600 -0.01` · `title 22/28 600 0` · `headline 17/22 600 0` · `body 17/25 400 0` · `callout 15/21 400 0` · `caption 13/18 500 0.01`. Numerals: tabular for measurements, units always shown.
**Color (strategy: blue-green calm + strict semantic system):**
- light: bg `#F7FAFA` · surface `#FFFFFF` · text `#102A2E` · text-2 `#4A6266` · border `#DCE6E7` · accent `#00707A` · on-accent `#FFFFFF`
- dark: bg `#0A1416` · surface `#132124` · text `#E6F0F1` · text-2 `#9BB0B3` · border `#23373A` · accent `#5CC8D2` · on-accent `#002A2E`
Semantic: in-range / watch / out-of-range get distinct hue, icon and text; never red for "not yet measured".
**Space:** unit 4, margins 20, density medium; one primary action per screen. **Shape:** radius s 8 · m 12 · l 18, continuous. **Elevation:** tonal with a subtle border.
**Icons:** SF Symbols / Material outlined, regular weight; medical icons literal and conventional. **Motion:** reassuring, gentle and never playful: `calm {0.45, 1.0}`, fade 220ms. **Haptics:** `soft` confirmation, `warning` only for genuinely critical alerts.
**Signature moves:** measurements shown with their range band so the number has meaning; explicit "no data yet" vs "zero" states; plain-language interpretation under every clinical value.
**Never:** fear colors for neutral info; fabricated "doctor approved" badges (F01); gamified health streaks (D27).

## 13. Kinetic Sport
**Essence:** energy and live data. Big numbers that move with the body.
**Range:** 4–5. **Fits:** running, cycling, gym, live sport, fitness classes. **Misfits:** reading, calm wellness, finance.
**Type:** SF Pro Expanded/Condensed (iOS supports width axes), Inter Tight, or Space Grotesk for numbers. Ramp: `metric 64/64 800 -0.03 tabular` · `display 40/42 800 -0.02` · `title 22/26 700 -0.01` · `body 16/22 500 0` · `label 13/16 700 0.04 caps` · `caption 12/16 600 0.02`. Numerals: tabular always (live values must not jitter).
**Color (strategy: dark-first, near-black + volt accent; light mode uses a deep green-olive accent):**
- light: bg `#F5F6F2` · surface `#FFFFFF` · text `#0B0C0A` · text-2 `#50534C` · border `#DFE1DA` · accent `#3F6A00` · on-accent `#FFFFFF`
- dark: bg `#0B0C0A` · surface `#171915` · text `#F5F6F2` · text-2 `#A0A39A` · border `#2A2D27` · accent `#C8F31D` · on-accent `#0B0C0A`
Zones (heart rate, pace) get their own ordered ramp of 5 hues and are never mixed with the accent.
**Space:** unit 4, margins 16, density medium; glance layouts with 1–3 metrics maximum while moving. **Shape:** radius s 8 · m 14 · l 22; italic/slanted shapes allowed as accent (not on text blocks). **Elevation:** tonal; none during workout.
**Icons:** filled, bold, 24pt. **Motion:** fast and athletic: `burst {0.28, 0.75}`, `track {0.18, 1.0}` for live values, fade 140ms; numbers roll, never fade. **Haptics:** rich: interval changes, splits and goal reached each have a distinct pattern.
**Signature moves:** the live metric fills the screen and adapts to wrist/lock-screen glance; a workout summary that replays the route; the accent appears only when you're on target.
**Never:** small numbers during activity; streak shaming; light-on-light while sweating in sun (test in bright light).

## 14. Gallery Whitespace
**Essence:** the white wall of a gallery. Content framed by emptiness and exact alignment.
**Range:** 2–3. **Fits:** portfolios, art, architecture, photography, premium retail, furniture. **Misfits:** dense data, utilities.
**Type:** one grotesque (Inter, SF Pro or Manrope), all hierarchy by size and position. Ramp: `display 40/44 500 -0.03` · `title 24/30 500 -0.02` · `body 15/22 400 0` · `caption 12/16 400 0.02` · `index 11/14 500 0.08 caps`. Numerals: lining, proportional.
**Color (strategy: achromatic; the content provides all color; the accent is ink):**
- light: bg `#FFFFFF` · surface `#FAFAFA` · text `#141414` · text-2 `#6B6B6B` · border `#EBEBEB` · accent `#141414` · on-accent `#FFFFFF`
- dark: bg `#0C0C0C` · surface `#161616` · text `#EDEDED` · text-2 `#9A9A9A` · border `#262626` · accent `#EDEDED` · on-accent `#0C0C0C`
**Space:** unit 4, margins 24/32, density low; asymmetric layouts on a 6-column grid; 64+ between works. **Shape:** radius 0 for media, s 4 for controls. **Elevation:** none.
**Icons:** almost none; text labels ("Close", "Next") over glyphs. **Motion:** quiet and precise: `place {0.5, 1.0}`, crossfade 280ms; zoom transitions from thumbnail to full. **Haptics:** none or `selection` on paging.
**Signature moves:** captions set like wall labels (title, year, medium) at caption size; images snap-scroll with exact alignment to a column; one full-bleed moment per screen.
**Never:** cards around images; colored UI competing with work; cramped thumbnails.

---

## Mutating a direction: worked micro-example
Product: a budgeting app for freelancers whose income is irregular. Thesis
feel: "steady, in control, no shame". Expression 2.
Shortlist: Swiss Instrument (1), Clinical Calm (12), Warm Paper Night (3).
Chosen: **structure from Swiss, voice from Clinical Calm**. Grid, hairlines,
tabular figures and the 4-pt density come from Swiss. The calm blue-green
accent, softer radii (8/12) and gentle motion come from Clinical Calm. The red
signal is dropped entirely, because the thesis says "no shame". Overspending is
shown in text-2 with a clear label instead of alarm red. Signature: the month's
"safe to spend" number, set at display size and recalculated as income arrives.
The swap test passes: a generic bank would never show "safe to spend for an
irregular income" as its hero.
