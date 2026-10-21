# Typography for mobile

On a phone, typography *is* the interface: most pixels are text, and most
hierarchy should come from type before it comes from boxes, color or icons.
The silence test (anti-slop.md) is a typography test.

## 1. Hierarchy is four levers, pulled together
| Lever | Use it for | Range on mobile |
|---|---|---|
| Size | Level in the hierarchy | 5–8 steps total |
| Weight | Emphasis within a level | ≤ 3 weights per family in UI (e.g. 400/500/600) |
| Color | Recession: primary → secondary → tertiary | `text`, `text-2`, `text-3` roles |
| Space | Grouping: what belongs together | spacing scale, never per-widget |

Rule: before adding a size, try weight; before adding weight, try color;
before adding color, try space. Three text colors usually replace three sizes.

## 2. Build the ramp
Anchor on body: **17pt on iOS** (Dynamic Type Large default), **16sp on
Android** (Material Body Large). Then choose a ratio from the expression level:

| Level | Ratio | Feel | Example ramp (pt) |
|---|---|---|---|
| 1 | 1.125 | instrument, dense | 13 · 15 · 17 · 19 · 22 · 28 |
| 2 | 1.2 | calm, native | 13 · 15 · 17 · 20 · 24 · 34 |
| 3 | 1.25 | confident | 12 · 15 · 17 · 22 · 28 · 40 |
| 4 | 1.333 | editorial | 12 · 15 · 17 · 23 · 32 · 48 |
| 5 | 1.5+ with a display jump | expressive | 13 · 17 · 22 · 34 · 56 · 80 |

Ramps are guides, not math: round to integers, and merge steps that are < 2pt
apart. Platform-native apps should start from the platform ramps
(platform-ios.md / platform-android.md) and deviate deliberately.

## 3. Line height (leading)
| Size | Line ÷ size | Example |
|---|---|---|
| 11–13 | 1.35–1.45 | 13/18, 12/16 |
| 15–17 (UI) | 1.25–1.35 | 17/22 (iOS body) |
| 15–17 (reading) | 1.4–1.5 | 17/24, 16/24 |
| 20–24 | 1.2–1.3 | 22/28 |
| 28–34 | 1.1–1.2 | 34/41 |
| 40+ | 1.0–1.1 | 48/52 |

Prefer line heights on the 4pt grid (16, 20, 24, 28…); it keeps baselines in
rhythm with the spacing scale. Large display type wants *tight* leading,
small text wants *air* — the most common slop is the reverse.

## 4. Tracking (letter-spacing, in em)
- SF Pro tracks itself per size (Text vs Display optical sizes switch at 20pt);
  leave system-font tracking at 0 unless you have a reason.
- Custom fonts: display ≥ 34pt **−0.02 to −0.04em**; titles 20–28 **−0.01**;
  body **0**; captions ≤ 13 **+0.01 to +0.02**.
- ALL CAPS only for short labels (≤ 3 words), **+0.04 to +0.08em**, size ≥ 11, weight ≥ 500.
- Never negative tracking below 13pt; never positive on display type.

## 5. Weight
- Light (300) only at ≥ 28pt and never on dark backgrounds at small sizes.
- Semibold (600) is the workhorse for titles on iOS; Medium (500) for labels.
- Bold body text inside paragraphs: rarely; use it for the one word that matters.
- Dark mode: text renders optically heavier on dark — consider one step lighter
  for large display (e.g. 600 → 500) if it looks heavy; never thinner than 400 for body.

## 6. Numerals
- **Tabular** (fixed-width) for anything that changes or aligns: timers,
  prices in lists, tables, counters, scores. SwiftUI `.monospacedDigit()`,
  Flutter `FontFeature.tabularFigures()`, CSS `font-variant-numeric: tabular-nums`.
- **Proportional** in prose.
- Units and currency symbols are secondary information: smaller or `text-2`,
  separated by a thin or narrow no-break space (U+202F) when the locale allows.
- A hero numeral is one of the strongest mobile signatures (Lune, Flighty): give it
  a dedicated `display` style with tabular figures and tight tracking.

## 7. Measure and rhythm
- Body measure on a phone: 30–45 characters per line is comfortable; the 375pt
  width with 20–24pt margins gives ~40 at 17pt. Don't reduce margins to fit more.
- Paragraphs: 1–3 sentences. Walls of text are a hierarchy failure.
- Space between a heading and its body is smaller than the space above the heading
  (proximity: the heading belongs to what follows).

## 8. Choosing typefaces
**Start with the system.** On iOS, SF Pro (+ SF Pro Rounded, New York, SF Mono)
is optically tuned, supports Dynamic Type for free and reads native. It is
very often the premium choice, not the lazy one (C01). Custom type earns its
place when the thesis needs a voice the system cannot give.

Free, high-quality families and what they are for:
| Role | Families | Notes |
|---|---|---|
| Neutral UI sans | Inter, Manrope, DM Sans, IBM Plex Sans, Geist | Inter needs `ss01`/`cv11` or tight tracking at display sizes to avoid looking default |
| Characterful sans | Space Grotesk, Sora, Outfit, General Sans (check license) | expression ≥ 3; avoid for long body |
| Text serif | Source Serif 4, Newsreader, Literata | reading apps, editorial |
| Display serif | Fraunces (opsz), Instrument Serif, Playfair Display | display only; Playfair at body sizes is slop |
| Mono | JetBrains Mono, IBM Plex Mono, SF Mono | code, IDs, aligned figures (C12) |
| Rounded | SF Pro Rounded, Nunito | friendly, kids, health; check that it doesn't read childish |

Pairing rules:
- One family is enough for most apps. Two when roles are genuinely different
  (display voice + text workhorse). Three only at expression 5.
- Pair by **contrast of structure** (serif display + sans text), never two
  sans-serifs that almost look alike.
- Match x-heights roughly; adjust sizes so the pair looks the same size optically.
- Check: the font supports the app's languages (accents, Cyrillic, CJK fallbacks)
  and has the weights you specify.

## 9. Large text and Dynamic Type (F04, F10)
- Support the full range: iOS up to the accessibility sizes (AX1–AX5), Android
  font scale ≥ 2.0. Never lock scaling (F10).
- Layout strategies at large sizes, in order: let text wrap → allow 2–3 lines
  for titles → switch horizontal rows to vertical stacks (`ViewThatFits`,
  `LayoutBuilder`) → move secondary information below → hide decorative
  elements. Shrinking text to fit (D28) is not a strategy.
- Scale spacing that relates to text (`@ScaledMetric` on iOS) but keep layout
  margins fixed.
- Test at XXXL and AX3 (iOS) / 200% (Android) on the smallest supported device.

## 10. Pixel-level details (craft)
- Align icons to the **cap height** or x-height center of the adjacent text, not
  to the text box (text boxes include ascender/descender padding).
- Rows mixing sizes align on the **first baseline**, not top or center.
- Optical margin: quotes and bullets can hang outside the text edge in editorial layouts.
- Title case vs sentence case: pick one per platform voice and apply everywhere
  (Material uses sentence case; iOS English titles/buttons traditionally use title case — follow the product voice).
- Avoid one-word last lines in headlines (rewrite or re-break); on the web use `text-wrap: balance`.
- Never fake bold/italic (synthesised); ship the real weights or don't use them.
- Truncation only for secondary, user-generated content in lists — never for
  titles, prices, CTAs or legal text (D28).

## 11. Typography slop (map to the catalog)
| Slop | ID |
|---|---|
| 10+ sizes picked per widget | D12 |
| Giant headline as the only idea; tiny micro-copy below it | K07 (validate) + judge |
| A serif word patched into a sans headline "for elegance" | D12 |
| Gradient or glowing text | D26 |
| Mono caps labels as fake technicality | C12 |
| Light 300 body text on dark | F03 |
| Body under 15pt on a consumer app | F03 (validate) |
| ALL CAPS paragraphs or buttons everywhere | D12 |

## 12. In KDL
```yaml
system:
  type:
    families: {display: Fraunces, text: Inter}
    scale:
      display: {size: 40, line: 44, weight: 500, track: -0.03}
      title:   {size: 22, line: 28, weight: 600, track: -0.01}
      body:    {size: 17, line: 24, weight: 400, track: 0}
      label:   {size: 15, line: 20, weight: 500, track: 0}
      caption: {size: 13, line: 18, weight: 400, track: 0.01}
    dynamic: true
```
`kinetic validate` checks ramp size, line ratios, tracking units, weights,
minimum sizes and family budget. `kinetic export` converts em tracking per stack.
