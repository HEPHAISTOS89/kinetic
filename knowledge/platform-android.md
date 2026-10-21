# Android — Material 3 done with taste

A high-end Android app is not an iOS app with a back arrow, and not stock
Material with the default purple. It uses Material 3's systems (tonal color,
type roles, shape, motion) as a **coherent engine** and tunes them to the
product's thesis. Facts that move between Material releases are marked
**(verify against m3.material.io)**.

## 1. Type scale (Material 3 baseline, Roboto / Roboto Flex)

| Role | Size / line (sp) | Weight | Tracking (sp) |
|---|---|---|---|
| Display Large | 57 / 64 | 400 | −0.25 |
| Display Medium | 45 / 52 | 400 | 0 |
| Display Small | 36 / 44 | 400 | 0 |
| Headline Large | 32 / 40 | 400 | 0 |
| Headline Medium | 28 / 36 | 400 | 0 |
| Headline Small | 24 / 32 | 400 | 0 |
| Title Large | 22 / 28 | 400 | 0 |
| Title Medium | 16 / 24 | 500 | +0.15 |
| Title Small | 14 / 20 | 500 | +0.1 |
| Body Large | 16 / 24 | 400 | +0.5 |
| Body Medium | 14 / 20 | 400 | +0.25 |
| Body Small | 12 / 16 | 400 | +0.4 |
| Label Large | 14 / 20 | 500 | +0.1 |
| Label Medium | 12 / 16 | 500 | +0.5 |
| Label Small | 11 / 16 | 500 | +0.5 |

- Map every text in the app to one role. In Compose use `MaterialTheme.typography.*`;
  in Flutter `Theme.of(context).textTheme.*` (same role names). A raw `fontSize = 15.sp`
  outside the theme is D12.
- Text sizes in **sp** (scale with the user's font size, up to 200% on Android 14+).
  Layouts must reflow at 200%, not clip (F04, F10).
- Display roles are for short, hero numerals or names — not for paragraphs.
- Custom brand fonts: replace families per role group (display/headline vs body/label),
  keep the size/line structure, re-tune tracking (positive at small sizes, near zero
  or negative at display sizes). Roboto Flex's optical size axis can do this
  automatically when supported.
- Material 3 Expressive adds emphasized type variants (heavier weights for
  stronger hierarchy) (verify against m3.material.io). Use emphasis for the one
  thing per screen that matters, not across the board.

## 2. Color system

### Roles
Material 3 colors are **roles**, each generated from a tonal palette (tones 0–100):

| Role | Light tone | Dark tone | Use |
|---|---|---|---|
| primary / onPrimary | 40 / 100 | 80 / 20 | Key actions, active states |
| primaryContainer / onPrimaryContainer | 90 / 10 | 30 / 90 | Prominent but less emphatic fills (FAB, selected chips) |
| secondary, tertiary (+ containers) | same pattern | same pattern | Supporting accents; tertiary for contrast/brand moments |
| error / onError / errorContainer | 40 / 100 / 90 | 80 / 20 / 30 | Errors only |
| surface / onSurface | 98 / 10 | 6 / 90 | Base background and text |
| onSurfaceVariant | 30 | 80 | Secondary text, icons |
| outline / outlineVariant | 50 / 80 | 60 / 30 | Borders, dividers |

(Tone assignments are the baseline scheme; verify against m3.material.io for the
current generator, which has evolved with newer scheme variants.)

### Surface containers replace shadows
Elevation in M3 is **tonal**, not shadow: `surfaceContainerLowest`,
`surfaceContainerLow`, `surfaceContainer`, `surfaceContainerHigh`,
`surfaceContainerHighest` express layers. Cards on `surfaceContainerLow`,
sheets on `surfaceContainerLow`/`High`, navigation bar on `surfaceContainer`.
Shadows are reserved for elements that truly float (FAB, menus, dragged items).
Mixing heavy shadows with tonal surfaces is D16.

### Dynamic color (Material You)
- **Support it when** the app is a utility or personal tool where harmony with
  the user's wallpaper is a feature (notes, clock, calculator, launcher, reader).
- **Override it when** the brand color carries meaning or recognition (banking,
  commerce, media, any strict brand). Then generate the scheme from the brand seed
  (`ColorScheme.fromSeed` in Flutter, `dynamicColorScheme` off + custom scheme in
  Compose) and keep semantic colors (error, success) fixed.
- A middle path: brand-locked primary, dynamic-harmonised neutrals; or
  `harmonize` custom colors against the dynamic primary.
- Never ship the default seed (`Colors.deepPurple`, `#6750A4`) as a decision — D30.

## 3. Shape scale

| Token | Radius (dp) | Typical components |
|---|---|---|
| None | 0 | Full-bleed media, edge sheets' outer edges |
| Extra small | 4 | Text field corners (filled top), snackbars, small badges |
| Small | 8 | Chips, menus |
| Medium | 12 | Cards |
| Large | 16 | FAB, navigation drawer, larger cards |
| Extra large | 28 | Dialogs, bottom sheets (top corners) |
| Full | 50% | Buttons, search bar, switches, sliders' handles |

Material 3 Expressive adds intermediate and larger tokens and shape morphing
between states (e.g. a button changing shape when pressed) (verify against
m3.material.io). Morphing is a signature tool: use it on one or two key
controls, not everywhere.

## 4. Navigation

| Pattern | Use |
|---|---|
| Navigation bar (bottom) | 3–5 top-level destinations on phones. Selected item: filled icon + active indicator pill + label. |
| Navigation rail | Medium/expanded widths (tablets, foldables, landscape) — same destinations moved to the side. |
| Navigation drawer | 5+ destinations or secondary destinations on large screens; avoid as the primary model on phones. |
| Top app bar (small / center-aligned / medium / large) | Medium and large collapse on scroll — the Android analogue of large titles. |
| Bottom sheet (modal / standard) | Secondary content and tasks; drag handle visible; respects predictive back. |
| FAB / extended FAB | The single creation-first action of a screen (C08). Extended FAB with label when the action isn't obvious from the icon. |

- **Predictive back**: users see a preview of the destination as they swipe back.
  Opt in (`android:enableOnBackInvokedCallback="true"`), use AndroidX
  `OnBackPressedDispatcher` / Compose `PredictiveBackHandler` / Flutter
  `PopScope`, and never intercept back to "confirm exit". System back-to-home
  animation is enforced from Android 15 for opted-in apps (verify against current
  Android docs).
- Up (top-left arrow) and Back are different: Up stays within the app's hierarchy.
- Adaptive layouts: use window size classes (compact < 600dp, medium 600–840dp,
  expanded ≥ 840dp) to switch bar → rail and single pane → list-detail.

## 5. Edge-to-edge and insets

- Draw behind the status and navigation bars (`enableEdgeToEdge()`); apps
  targeting SDK 35 (Android 15) are edge-to-edge by default (verify against
  current Android docs).
- Pad content with `WindowInsets` (Compose: `Modifier.windowInsetsPadding`,
  `safeDrawing`; Flutter: `SafeArea`/`MediaQuery.paddingOf`). Interactive
  elements never sit under gesture navigation areas.
- Handle `imePadding()` so focused fields stay visible above the keyboard.
- Display cutouts: treat like iOS notches; no critical content under them.

## 6. Touch targets and density
- **48×48dp** minimum touch target (icons stay 24dp; the target grows).
- Default list item heights: 56dp (one line), 72dp (two lines), 88dp (three lines).
- Spacing grid: 4dp base, 8dp step; screen margins 16dp on compact, 24dp on medium+.
- Density: Material defaults are calm; expert apps may tighten (C11), never below
  targets and readable sizes.

## 7. Motion

Material 3 motion is built on transition patterns and easing tokens:

| Pattern | Use |
|---|---|
| Container transform | An element becomes a screen (card → detail, FAB → compose). Strongest continuity. |
| Shared axis (X / Y / Z) | Spatial or navigational relationship: steps in a flow (X), scroll-related (Y), parent → child (Z). |
| Fade through | Switching between unrelated destinations (bottom nav tabs). |
| Fade | Elements entering/exiting within the screen (dialogs, menus). |

Easing and duration tokens (baseline; verify against m3.material.io):
- Emphasized: `cubic-bezier(0.2, 0, 0, 1)` — most transitions.
- Emphasized decelerate `(0.05, 0.7, 0.1, 1)` for entering, emphasized accelerate
  `(0.3, 0, 0.8, 0.15)` for exiting.
- Standard `(0.2, 0, 0, 1)` for small utility changes.
- Durations: short 50–200ms (selection, small state), medium 250–400ms
  (expanding, sheets), long 450–600ms (full-screen container transforms).

Material 3 Expressive introduces a **spring-based motion scheme** (spatial
springs for movement, effects springs for color/opacity, with standard and
expressive variants) (verify against m3.material.io for exact parameters). In
Compose prefer `spring()` specs from `MaterialTheme.motionScheme` where available.
Animate what changed; respect "Remove animations"
(`Settings.Global.ANIMATOR_DURATION_SCALE == 0`, Flutter
`MediaQuery.disableAnimationsOf`) (F08).

## 8. Haptics

- Use `View.performHapticFeedback(HapticFeedbackConstants.X)` (Compose:
  `LocalHapticFeedback`, Flutter: `HapticFeedback.*`). These respect user settings
  and device capability; avoid raw `Vibrator` waveforms for UI feedback.
- `CONFIRM` / `REJECT` (API 30+) for outcomes, `CLOCK_TICK` / `SEGMENT_TICK` for
  scrubbing and selection steps, `LONG_PRESS` for long press, `GESTURE_START` /
  `GESTURE_END` for drag thresholds, `TOGGLE_ON` / `TOGGLE_OFF` (API 34+)
  (verify availability per API level).
- Same discipline as iOS: confirm acts and outcomes, never decorate.

## 9. Components with taste
- Buttons: filled (one primary per screen), tonal (secondary emphasis), outlined
  (medium), text (low). Five button styles on one screen is chaos.
- Cards: elevated / filled / outlined — pick one card style per app (D03, D16).
- Chips: assist, filter, input, suggestion — chips are interactive; don't use them
  as decorative tags (D25).
- Snackbar: brief feedback with an optional single action ("Undo"). Not for errors
  that need reading, not for every save (D10).
- Ripples are correct on Android; pressed states should still exist on custom
  components (state layer at 10–12% of the content color).

## 10. Android-specific slop
- The default Material purple / template color scheme untouched (D30).
- iOS idioms on Android: chevron-left back icon, bottom-aligned iOS action sheets,
  centered iOS-style titles everywhere, segmented controls copied from iOS (D24).
- Shadow + tonal surface + outline on the same card (D16).
- A FAB on every screen, or a FAB for non-creation actions (D09).
- Hamburger drawer on a phone app with three destinations (D08).
- Fixed `dp` text sizes, or text that clips at 200% font scale (F10, F04).
- Ignoring edge-to-edge: grey system bars, content behind the gesture bar (F09).
- Back intercepted with "Press back again to exit" dialogs.
- Snackbars for every action; toasts (`Toast.makeText`) as the main feedback (D10).
- Ripple disabled globally to look "iOS-clean" — removes essential feedback.
- Random accent colors outside the generated scheme; hand-picked greys
  instead of `onSurfaceVariant` / `outline` roles (D13).
