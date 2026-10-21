# Flutter — design ↔ code

Load when `product.stack: flutter` or `pubspec.yaml` contains `flutter:`.

## 1. Detect and read (code-to-design)

| Look at | Reveals |
|---|---|
| `pubspec.yaml` | Fonts (`flutter: fonts:`), icon packages (`cupertino_icons`, `phosphor_flutter`, `lucide_icons`…), animation/UI packages, `google_fonts` |
| `lib/main.dart`, `lib/app.dart` | `MaterialApp`/`CupertinoApp`, `theme:`, `darkTheme:`, `themeMode:`, `useMaterial3`, router |
| `lib/**/theme*.dart`, `lib/core/theme/`, `lib/design_system/` | `ThemeData`, `ColorScheme`, `TextTheme`, `ThemeExtension`s, constants files (`AppColors`, `AppSpacing`) |
| `assets/` | Images/illustrations (D07 candidates), Lottie files, custom icon fonts |
| Widgets in `lib/**/screens|pages|features` | De-facto system: literal `Color(0x…)`, `fontSize:`, `EdgeInsets`, `BorderRadius.circular`, `BoxShadow`, `Duration(milliseconds:)`, `Curves.*` |

Run `kinetic dna lib/ --json` first; then confirm by reading the theme file and 2–3 representative screens. Map to KDL `audit`:

- **keep** — coherent choices used consistently (one radius family, a real brand color).
- **evolve** — the right idea poorly executed (11 font sizes → a 6-step ramp; shadows → tonal elevation).
- **replace** — defaults never decided (`ColorScheme.fromSeed(seedColor: Colors.deepPurple)` = D30), generic gradients (D01).
- **remove** — greeting headers (D02), decorative badges (D25), unused packages for effects.

Signals that the theme is bypassed: many `Color(0x…)` literals in widgets, `TextStyle(fontSize:…)` without `Theme.of(context).textTheme`, `const EdgeInsets.all(13)`.

## 2. Token architecture (KDL `system` → code)

One file `lib/design/tokens.dart` + one `lib/design/theme.dart`. Material roles go in `ColorScheme`; everything Material does not model (spacing, radii, springs, extra roles, haptics) goes in a `ThemeExtension`.

```dart
@immutable
class KineticTokens extends ThemeExtension<KineticTokens> {
  const KineticTokens({required this.text2, required this.border, required this.space, required this.radius});
  final Color text2;
  final Color border;
  final KSpace space;
  final KRadius radius;

  @override
  KineticTokens copyWith({Color? text2, Color? border}) =>
      KineticTokens(text2: text2 ?? this.text2, border: border ?? this.border, space: space, radius: radius);

  @override
  KineticTokens lerp(ThemeExtension<KineticTokens>? other, double t) {
    if (other is! KineticTokens) return this;
    return KineticTokens(
      text2: Color.lerp(text2, other.text2, t)!,
      border: Color.lerp(border, other.border, t)!,
      space: space, radius: radius, // non-color tokens do not interpolate
    );
  }
}

class KSpace { const KSpace(); final double xs = 4, s = 8, m = 12, l = 16, xl = 24, xxl = 32; }
class KRadius { const KRadius(); final double s = 8, m = 14, l = 22; }

extension KineticX on BuildContext {
  KineticTokens get k => Theme.of(this).extension<KineticTokens>()!;
  ColorScheme get colors => Theme.of(this).colorScheme;
  TextTheme get type => Theme.of(this).textTheme;
}
```

KDL roles → `ColorScheme`: `bg → surface`, `surface → surfaceContainerLow` (or `surfaceContainer`), `text → onSurface`, `text-2 → onSurfaceVariant` (and in the extension), `border → outlineVariant`, `accent → primary`, `on-accent → onPrimary`, `danger → error`. Build the scheme explicitly (`ColorScheme(brightness: …, primary: …)`) or start from `ColorScheme.fromSeed(seedColor:, brightness:)` and `.copyWith(...)` every KDL role — never ship the raw seed output as the design.

Type: KDL `track` is in em; Flutter `letterSpacing` is in logical pixels → `letterSpacing = track * size`; `height = line / size`.

```dart
TextStyle _style(double size, double line, FontWeight w, double trackEm, {String? family, bool tabular = false}) =>
    TextStyle(fontFamily: family, fontSize: size, height: line / size, fontWeight: w,
      letterSpacing: trackEm * size,
      fontFeatures: tabular ? const [FontFeature.tabularFigures()] : null);

final textTheme = TextTheme(
  displaySmall: _style(40, 44, FontWeight.w300, -0.02, tabular: true),
  titleLarge:   _style(22, 28, FontWeight.w600, -0.01),
  bodyLarge:    _style(17, 24, FontWeight.w400, 0),
  labelMedium:  _style(13, 18, FontWeight.w500, 0.01),
);
```

Use `TextHeightBehavior`/`leadingDistribution: TextLeadingDistribution.even` when vertical centering inside pills/buttons looks off. Register fonts in `pubspec.yaml`; on iOS the system font is used when `fontFamily` is null (SF Pro), on Android Roboto.

Assemble: `ThemeData(useMaterial3: true, colorScheme: scheme, textTheme: textTheme, extensions: [tokens], splashFactory: …, pageTransitionsTheme: …)` for light and dark; `MaterialApp(theme:, darkTheme:, themeMode: ThemeMode.system)`.

## 3. Layout and responsive

- Layout responds to **constraints**, not device names: `LayoutBuilder` for local decisions, `MediaQuery.sizeOf(context)` for viewport decisions (the `*Of` accessors rebuild only on that aspect).
- Safe areas: `SafeArea` around screen bodies, or `MediaQuery.paddingOf(context)` when backgrounds must bleed under the status bar while content stays inside. Never hard-code status bar heights.
- Keyboard: `Scaffold(resizeToAvoidBottomInset: true)` (default) + scrollable bodies; `MediaQuery.viewInsetsOf(context).bottom` for custom bottom bars; `Scrollable.ensureVisible` for the focused field if needed.
- Text scaling: read `MediaQuery.textScalerOf(context)`. **Never** `TextScaler.noScaling` or `MediaQuery(data: …copyWith(textScaler: TextScaler.linear(1)))` app-wide (F10). If one display numeral would break layout, clamp *that widget only*, with a reason: `MediaQuery.withClampedTextScaling(maxScaleFactor: 1.6, child: …)`, and reflow (switch `Row` → `Column` via `LayoutBuilder`) at large scales.
- Wrapping: `Flexible`/`Expanded` + `softWrap`; `Wrap` for chips. No `maxLines: 1` + ellipsis on titles, prices, legal text (F04/D28).
- Continuous corners: `ContinuousRectangleBorder` exists but its `borderRadius` does not render like an equal `BorderRadius.circular` — tune the value visually against the design. Recent Flutter versions add `RoundedSuperellipseBorder` / `ClipRSuperellipse` (iOS-style squircle) — verify availability for the project's Flutter version before using.
- Concentric radii: inner radius = outer radius − padding.

## 4. Motion

KDL spring `{response, damping}`: response = period of the undamped oscillation (s), damping = ratio ζ.

```dart
SpringDescription kSpring(double response, double damping, {double mass = 1}) {
  final stiffness = math.pow(2 * math.pi / response, 2) * mass;     // k = (2π/T)² m
  return SpringDescription.withDampingRatio(mass: mass, stiffness: stiffness.toDouble(), ratio: damping);
  // equivalent coefficient: c = 4π ζ m / T
}

// Drive a controller with physics (interruptible: re-run from current value + velocity)
void settleTo(AnimationController c, double target) {
  c.animateWith(SpringSimulation(kSpring(0.4, 0.9), c.value, target, c.velocity));
}
```

- **Implicit** (`AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher`, `TweenAnimationBuilder`) for state-driven changes; they retarget when the value changes mid-flight. Curves only — use `Curves.easeOutCubic`/`Curves.fastOutSlowIn`/`Easing.emphasizedDecelerate` (M3) for UI; no `bounceOut`/`elasticOut` on utility UI (D19).
- **Explicit** `AnimationController` + `SpringSimulation` for gestures and anything interruptible; pass the gesture's `velocity.pixelsPerSecond` normalised to the controller's units.
- Shared element: `Hero(tag:)` across routes; keep tags unique per screen. For in-screen morphs, animate a single widget between layouts (`AnimatedAlign`, `AnimatedSize`) rather than cross-fading two.
- Page transitions: `PageTransitionsTheme(builders: {TargetPlatform.iOS: CupertinoPageTransitionsBuilder(), TargetPlatform.android: …})` — keep iOS back-swipe working.
- Reduce motion: `MediaQuery.disableAnimationsOf(context)` (reflects iOS Reduce Motion / Android remove animations). Branch:

```dart
final reduce = MediaQuery.disableAnimationsOf(context);
final duration = reduce ? Duration.zero : const Duration(milliseconds: 220);
// or replace slide/scale with a FadeTransition when reduce is true
```

- Lifecycle: dispose controllers (`SingleTickerProviderStateMixin` + `dispose()`); stop repeating animations when offscreen (`VisibilityDetector` is a package — prefer route-aware pausing with `RouteAware` when already available).

## 5. Haptics (`package:flutter/services.dart`)

| KDL | Flutter |
|---|---|
| selection | `HapticFeedback.selectionClick()` |
| light / soft | `HapticFeedback.lightImpact()` |
| medium / success | `HapticFeedback.mediumImpact()` |
| heavy / rigid | `HapticFeedback.heavyImpact()` |
| warning / error | `HapticFeedback.heavyImpact()` (no notification types in the SDK; a plugin is needed for true iOS notification haptics — justify before adding) |

Fire haptics on the confirmed outcome, not on tap-down of an async action.

## 6. Accessibility

- `IconButton(tooltip: 'Delete entry', …)` gives a label; custom tappables: `Semantics(button: true, label: '…', child: …)`.
- Group: `MergeSemantics` for a row with title + value; `ExcludeSemantics` for decorative glyphs.
- Headers: `Semantics(header: true, child: Text(…))`.
- Targets: `kMinInteractiveDimension` = 48; keep `materialTapTargetSize: MaterialTapTargetSize.padded`; for small glyphs wrap in `SizedBox(width: 48, height: 48)` / `ConstrainedBox`.
- Order: `FocusTraversalGroup` / `OrderedTraversalPolicy` when visual order ≠ tree order.
- Test: `flutter test` with `meetsGuideline(androidTapTargetGuideline)`, `iOSTapTargetGuideline`, `textContrastGuideline`, `labeledTapTargetGuideline`.

## 7. Native fidelity

- Material 3 is the default (`useMaterial3: true`). On iOS, Material chrome reads foreign (D24). Options per element:
  - `Switch.adaptive`, `Slider.adaptive`, `CircularProgressIndicator.adaptive`, `Checkbox.adaptive`, `AlertDialog.adaptive` + `showAdaptiveDialog`.
  - `CupertinoPageRoute`/Cupertino transitions on iOS; `CupertinoSliverNavigationBar` for large titles when the brand is iOS-first.
  - Bottom sheets: `showModalBottomSheet(useSafeArea: true, showDragHandle: true)` on Android; on iOS the native page sheet is `CupertinoSheetRoute` / `showCupertinoSheet` (Flutter ≥ 3.29) — `showCupertinoModalPopup` is for action sheets and pickers.
- Share identity (color, type, shape, motion), adapt chrome (navigation, controls, feedback). Branch on `Theme.of(context).platform`, not `Platform.isIOS` scattered in widgets.
- Ripple on iOS: set `splashFactory: NoSplash.splashFactory` in the iOS theme if the design wants iOS-style highlight; supply a pressed state (opacity/scale 0.97) instead.

## 8. Flutter-specific slop

| ID | Code signal | Fix |
|---|---|---|
| F02 | `onPressed: () {}`, `onTap: () {}` | Wire it or remove the control |
| F05 | `IconButton(constraints: BoxConstraints(), padding: EdgeInsets.zero)`, `visualDensity: VisualDensity.compact` on primary actions | Keep 48 dp hit area |
| F07 | `IconButton` without `tooltip`, `GestureDetector` without `Semantics` | Label |
| F08 | `AnimationController` with no `disableAnimationsOf` branch | Branch |
| F09 | Body without `SafeArea`; hard-coded `padding: EdgeInsets.only(top: 44)` | `SafeArea` / `MediaQuery.paddingOf` |
| F10 | `TextScaler.noScaling`, `textScaleFactor: 1.0` | Remove; reflow |
| D01 | `LinearGradient(colors: [Colors.purple, Colors.blue])` | Solid + accent, or meaningful low-chroma gradient |
| D05 | `BackdropFilter(filter: ImageFilter.blur(…))` on content cards | Tonal surface |
| D09 | `floatingActionButton:` on iOS target | Nav-bar action |
| D16 | `BoxShadow(blurRadius: 20+)` on many containers | One elevation strategy |
| D19 | `Curves.bounceOut`, `Curves.elasticOut`, `Curves.linear` on UI | Damped spring / easeOut |
| D20 | `Shimmer` package everywhere, centered `CircularProgressIndicator` | Keep content, progress in place |
| D28 | `FittedBox` around text, `overflow: TextOverflow.ellipsis` on critical text | Reflow |
| D29 | `width: 375`, `height: 812`, `MediaQuery.of(context).size.height * 0.37` everywhere | Constraints, flexible layout |
| D30 | `ColorScheme.fromSeed(seedColor: Colors.deepPurple)` untouched, `primarySwatch: Colors.blue` | Decide the palette |

## 9. Verify

```bash
flutter analyze
flutter test                                  # incl. golden + a11y guideline tests
flutter test --update-goldens test/golden/    # only when the change is intended
flutter run -d <simulator-id>
flutter screenshot -o shots/home.png          # from a running app on a device/simulator
xcrun simctl io booted screenshot shots/ios_home.png
adb exec-out screencap -p > shots/android_home.png
```

Golden/gallery gotchas:
- A golden that pumps once renders a route pushed in a post-frame callback at its *start* position (an invisible sheet). Render sheets and dialogs as initial routes (`onGenerateInitialRoutes`) or pump until settled.
- `Ink`/`InkWell` decorations are painted on the nearest `Material`; inside a coloured `DecoratedBox`/`Container` the fill hides them and a filled button looks disabled — put the colour on a `Material`/`Ink`, not on the box behind it.
- Display numerals built with a fixed `fontSize` ignore `textScaler`; scale them with `MediaQuery.textScalerOf(context).clamp(maxScaleFactor: 1.6)` so the hero still leads at XXL.

Golden matrix (one test, parameterised): sizes 320×568, 390×844, 430×932; `textScaler` 1.0 and 2.0; light and dark. Wrap with `MediaQuery(data: MediaQueryData(size:, textScaler: TextScaler.linear(2), platformBrightness: Brightness.dark))`. Device checks: iOS Settings → Accessibility → Larger Text; Android `adb shell settings put system font_scale 2.0`; dark via `xcrun simctl ui booted appearance dark` / `adb shell cmd uimode night yes`.
