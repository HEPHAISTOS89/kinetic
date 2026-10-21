# iOS — what native and high-end actually means

An iOS app feels expensive when it behaves exactly as the system has taught
the user to expect, and then spends its identity budget on content,
typography and one or two signature moments. Fighting the platform reads as
cheap; obeying it blindly reads as a template. The craft is in between.

Facts that change with OS releases are marked **(verify against current HIG)**.

## 1. Navigation model

| Pattern | Use | Never |
|---|---|---|
| `NavigationStack` push | Drill-down into a hierarchy (list → detail) | Pushing for a modal task the user must finish or cancel |
| Large title → inline on scroll | Top-level screens of each tab; the title is the place name | Detail screens (use inline titles), titles that are sentences |
| Interactive back swipe from the left edge | Always available on pushed screens | Disabling it, or placing horizontal gestures that start at the left edge |
| Tab bar | 2–5 parallel, top-level areas the user switches between | Actions ("+", "Scan") as tabs; more than 5; hiding it on push without reason |
| Sheet (`.sheet` + `presentationDetents([.medium, .large])`) | Self-contained task, creation, filters, quick detail | Navigating deep inside a sheet; stacking sheets more than one deep |
| Full-screen cover | Immersive or blocking flow: camera, onboarding, playback | Ordinary forms |
| `Menu` / pull-down button | 2–8 secondary options attached to a control | Primary actions hidden in a "…" menu |
| Context menu (long press) | Shortcuts on content: share, copy, delete, pin | The only way to reach an action |
| Swipe actions on rows | 1–3 frequent row actions; destructive on trailing edge, full-swipe for the most common | Hiding the only path to an action; more than 3 per edge |
| Toolbar items | Screen-level actions: top-trailing for the primary, bottom toolbar for document tools | A floating action button (D09) |
| Search (`.searchable`) | In the navigation bar, revealed on pull or always visible for search-first screens | A custom search field mimicking the system one badly |

Rules of thumb:
- The **primary action** of a screen lives top-trailing (nav bar) or as a full-width
  button at the bottom of a task screen above the home indicator, never as a FAB.
- **Cancel** is top-leading in sheets; **Done/Save** top-trailing, semibold.
- Destructive actions confirm with an action sheet (`confirmationDialog`) anchored
  to the control, not a centered alert, unless the loss is severe and irreversible.
- Never put a hamburger menu on iOS (D08).

## 2. Typography

### Dynamic Type defaults (Large content size, iOS)

| Style | Size / leading (pt) | Weight |
|---|---|---|
| Large Title | 34 / 41 | Regular (often set Bold for brand) |
| Title 1 | 28 / 34 | Regular |
| Title 2 | 22 / 28 | Regular |
| Title 3 | 20 / 25 | Regular |
| Headline | 17 / 22 | Semibold |
| Body | 17 / 22 | Regular |
| Callout | 16 / 21 | Regular |
| Subheadline | 15 / 20 | Regular |
| Footnote | 13 / 18 | Regular |
| Caption 1 | 12 / 16 | Regular |
| Caption 2 | 11 / 13 | Regular |

- **Always use text styles** (`.font(.body)`, `UIFont.preferredFont(forTextStyle:)`) or
  scale custom fonts with `Font.custom(_:size:relativeTo:)` /
  `UIFontMetrics(forTextStyle:).scaledFont(for:)`. A fixed `.system(size: 17)` does not
  scale (F10 in spirit).
- Body at 17pt is the iOS reading size. A 15pt body on iOS reads as "Android port".
- Leading is generous at small sizes and tight at large ones — keep that shape when
  you customise. A 34pt title at 41pt leading; don't give a 34pt title 1.5× leading.
- At accessibility sizes (AX1–AX5), Body reaches ~53pt. Layouts must switch from
  horizontal to vertical stacking (`ViewThatFits`, `dynamicTypeSize.isAccessibilitySize`)
  rather than truncate.

### SF Pro optical sizes and tracking
- SF Pro has **Text** and **Display** optical cuts. The system font switches
  automatically: below 20pt it uses Text (wider spacing, larger x-height
  apertures), from 20pt it uses Display (tighter, finer). With the system font
  you get this for free; never force SF Pro Display on 15pt text.
- The system font also applies **size-specific tracking** automatically. If you
  use a custom font you must apply tracking yourself, following the same curve:
  positive at small sizes, negative from ~17 to ~24, near zero or slightly
  positive again at very large sizes. Apple's published SF Pro table
  (verify against current HIG): 11pt +0.06, 13pt −0.08, 15pt −0.23, 17pt −0.43,
  20pt −0.45, 22pt −0.26, 28pt +0.38, 34pt +0.40 (points of tracking).
- `.fontDesign(.rounded)` (SF Pro Rounded) suits friendly, health, kids, numerals.
  `.serif` (New York) suits editorial, reading, calm. `.monospaced` (SF Mono) only
  for code and IDs. `.monospacedDigit()` for any number that updates (timers,
  prices, counters) so digits don't jitter.
- Hierarchy on iOS is **weight + size + color together** (`.primary`, `.secondary`,
  `.tertiary`), not size alone.

## 3. SF Symbols

- Use SF Symbols for every system concept (share, delete, settings, search,
  person, chevrons). A custom icon for "share" is a regression, not identity.
- Symbols are **typographic**: they inherit font size and weight. Match the
  symbol weight to adjacent text (`.font(.body.weight(.semibold))` applies to both).
  Use `.imageScale(.small/.medium/.large)` for relative sizing, not frames.
- Rendering modes:
  - **Monochrome** — default, almost always right for UI chrome.
  - **Hierarchical** — one hue, layered opacity; good for larger feature icons.
  - **Palette** — 2–3 explicit colors; brand moments, sparingly.
  - **Multicolor** — the symbol's intrinsic colors (weather, battery); only where the color carries meaning.
- Variants: `.fill` for selected tab items and active state; outline for
  idle. `.circle`/`.square` enclosed variants for list leading icons.
- Symbol effects (iOS 17+): `.symbolEffect(.bounce, value:)` on discrete events,
  `.pulse` for ongoing activity, `.variableColor` for progress/signal,
  `.contentTransition(.symbolEffect(.replace))` when a symbol changes meaning
  (play ↔ pause). One effect per event; never loop decorative effects.
- Custom symbols: export a template from the SF Symbols app and draw on its
  guides so weights and scales interpolate; see iconography-svg.md.

## 4. Materials and Liquid Glass

- **Liquid Glass** is the design language introduced with iOS 26 (WWDC 2025):
  a translucent, refractive material for the **controls and navigation layer**
  that floats above content — tab bars, toolbars, navigation bars, sheets,
  menus, some buttons. Content sits underneath and scrolls beneath it.
  (verify against current HIG for APIs such as `.glassEffect()` and its variants)
- The principle that matters for taste:
  - **Content is not glass.** Cards, list rows, charts, text blocks stay opaque
    surfaces. Glass on content is D05.
  - **Glass on glass is mud.** Don't stack glass elements; group related controls
    into one glass container.
  - Let the system components adopt it; custom chrome should use the system
    material APIs instead of hand-rolled blur + white overlay.
  - Glass needs something behind it to be read as glass; over a flat solid
    background it's just a tint — prefer a plain surface there.
- Pre-iOS 26 materials (`.ultraThinMaterial` … `.thickMaterial`) follow the same
  rule: bars, sheets, overlays over moving content only.

## 5. Layout, spacing and shape

- **Layout margins**: 16pt on compact-width iPhones, 20pt on larger iPhones
  (system readable/layout margins adapt; use `.padding()` defaults or
  `safeAreaPadding` rather than hardcoding when possible). Keep one margin per
  screen; content, headers and dividers align to it.
- **Spacing grid**: 4pt base, with 8pt as the common step. Section gaps 24–35pt;
  grouped list sections already carry system spacing — don't fight it.
- **Safe areas**: content scrolls under the status bar and home indicator;
  controls never sit inside them. Bottom buttons sit above the home indicator
  with ≥ 8pt clearance, using `safeAreaInset(edge: .bottom)` for pinned CTAs.
  Respect the keyboard: `.scrollDismissesKeyboard`, focused field stays visible.
- **Touch targets**: 44×44pt minimum hit area, regardless of glyph size.
- **Standard metrics** (verify for current OS): nav bar 44pt (+ large title area
  ~52pt), tab bar 49pt + home indicator inset, list row min height 44pt,
  grouped inset list corner radius ~10–12pt.
- **Continuous corners** (squircle): `RoundedRectangle(cornerRadius:, style: .continuous)`.
  Circular arcs on large radii look cheap on iOS next to system shapes.
- **Concentric radii**: inner radius = outer radius − padding. A 22pt card with
  12pt padding holds 10pt inner elements.
- `ContainerRelativeShape` makes nested shapes follow their container (widgets).

## 6. Controls

- System controls (`Toggle`, `Picker`, `DatePicker`, `Stepper`, segmented
  `Picker`, `Slider`) are part of the user's muscle memory. Style with tint, not
  by re-implementing. A custom toggle must still be a `Toggle` for accessibility.
- Buttons: `.borderedProminent` for the single primary, `.bordered` for
  secondary, plain/borderless for tertiary, `role: .destructive` for delete.
  `controlSize(.large)` for bottom task CTAs (≈50pt tall, full width minus margins).
- Text fields: label above or placeholder-as-hint only when the field's meaning
  is obvious; set `textContentType`, `keyboardType`, `submitLabel` — these are
  design decisions.
- Lists: `List` with `.insetGrouped` for settings and forms; `.plain` for
  content feeds. Leading icons in settings rows use small rounded-square
  colored tiles only if they help scanning (Settings app idiom) — not by default.

## 7. Color

- System semantic colors (`.label`, `.secondaryLabel`, `.systemBackground`,
  `.secondarySystemBackground`, `.separator`, `.tint`) adapt to dark mode,
  increased contrast and elevated contexts automatically. Start from them; map
  KDL roles onto them when the expression level is 1–2.
- A custom palette is right when the thesis needs an identity the system palette
  can't carry. Then define **both** appearances and the increased-contrast
  variant in the asset catalog. Never a single hex used in both modes.
- Dark mode on iOS has **elevated** backgrounds: sheets and popovers are lighter
  than the base. Respect the hierarchy `systemBackground` < `secondary` < `tertiary`.
- One app **tint** (`.tint(...)`) drives every interactive element. If buttons,
  links, toggles and selected tabs are different colors, it's D13.

## 8. Haptics

| Event | Generator | SwiftUI (iOS 17+) |
|---|---|---|
| Selection change (picker, segmented, scrubbing) | `UISelectionFeedbackGenerator` | `.sensoryFeedback(.selection, trigger:)` |
| Task completed successfully | `UINotificationFeedbackGenerator(.success)` | `.success` |
| Validation problem | `.warning` | `.warning` |
| Failure | `.error` | `.error` |
| Physical collision/snap (drag hits a detent) | `UIImpactFeedbackGenerator(.light/.medium/.rigid)` | `.impact(weight:intensity:)` |
| Soft confirmation | `.soft` | `.impact(flexibility: .soft)` |
| Increase/decrease | — | `.increase` / `.decrease` |

- Haptics confirm what the user did or what the system concluded. Never on
  scroll, never on every tap, never on appear.
- Pair each haptic with a visual change at the same moment.
- Respect the system setting; system controls already emit their own haptics —
  don't double them.

## 9. Motion on iOS

- iOS motion is **spring-based and interruptible**. SwiftUI defaults
  (`.spring`, `.smooth`, `.snappy`, `.bouncy`) are tuned for this; prefer them or
  explicit `.spring(response:dampingFraction:)`.
- Utility transitions: `.smooth` / damping 1.0. Direct manipulation release:
  slight bounce (damping 0.8–0.9). `.bouncy` only at expression ≥ 4 or for
  playful brand moments.
- Navigation transitions belong to the system. Custom: `matchedGeometryEffect`
  or iOS 18 `.navigationTransition(.zoom(sourceID:in:))` for photo/card →
  detail continuity.
- Respect `@Environment(\.accessibilityReduceMotion)`: replace movement with
  crossfade, keep state feedback (F08).

## 10. iOS-specific slop

- Material components on iOS: FAB, ripple, Material top app bar, snackbar (D09, D24).
- Hamburger drawer navigation (D08).
- Custom back buttons that break the back swipe, or a "<" glyph instead of the system chevron.
- Centered titles on top-level screens instead of large titles; large titles on every pushed screen.
- `.system(size:)` everywhere — no Dynamic Type (F10).
- Circular corners on large cards, mixed with continuous system shapes.
- Light-only color assets; dark mode as automatic inversion.
- Toast messages (no system idiom); use inline status, banners or `.alert` only when warranted.
- Alerts for confirmations that should be undoable.
- Glass/blur on content cards (D05); glass stacked on glass.
- SF Symbols at mismatched weights next to text, or custom icons for system concepts (D06).
- Haptics on every button.
- Bottom CTAs touching the home indicator; content hidden under the tab bar.
