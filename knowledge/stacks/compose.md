# Jetpack Compose — design ↔ code

Load when `product.stack: compose` or Gradle files depend on `androidx.compose`.

## 1. Detect and read (code-to-design)

| Look at | Reveals |
|---|---|
| `ui/theme/Color.kt`, `Theme.kt`, `Type.kt`, `Shape.kt` (Android Studio template) | `lightColorScheme`/`darkColorScheme`, `Typography`, `Shapes`; dynamic color usage |
| `res/values/colors.xml`, `themes.xml`, `values-night/` | Legacy View theme, splash/window colors, status bar handling |
| `res/font/` | Bundled fonts |
| `build.gradle(.kts)` / `libs.versions.toml` | Compose BOM version (decides API availability), material3 version, icon packs (`material-icons-extended`) |
| Composables | Literal `Color(0xFF…)`, `16.dp` paddings, `fontSize = 15.sp`, `RoundedCornerShape(…)`, `Modifier.shadow(…)`, `tween(…)` |

The Studio template ships purple `Purple80/PurpleGrey80/Pink80` — if still present, it is D30. `dynamicColor = true` (Material You) is a legitimate choice only when the thesis accepts the user's wallpaper over brand identity; record it as a decision.

Run `kinetic dna app/src/main --json`, read the theme files, then 2–3 screens; fill KDL `audit`.

## 2. Token architecture

```kotlin
// KDL roles → Material 3 ColorScheme
private val LightColors = lightColorScheme(
    primary = Color(0xFF8A5A2B), onPrimary = Color.White,
    background = Color(0xFFF6F1EA), surface = Color(0xFFF6F1EA),
    surfaceContainerLow = Color(0xFFFFFFFF),
    onSurface = Color(0xFF1E1A16), onSurfaceVariant = Color(0xFF5C5249),
    outlineVariant = Color(0xFFE4DAD0), error = Color(0xFFB3261E),
)
// darkColorScheme(...) likewise

// Tokens Material does not model
@Immutable
data class KineticTokens(
    val space: KSpace = KSpace(), val radius: KRadius = KRadius(),
)
@Immutable data class KSpace(val xs: Dp = 4.dp, val s: Dp = 8.dp, val m: Dp = 12.dp, val l: Dp = 16.dp, val xl: Dp = 24.dp, val xxl: Dp = 32.dp)
@Immutable data class KRadius(val s: Dp = 8.dp, val m: Dp = 14.dp, val l: Dp = 22.dp)

val LocalKinetic = staticCompositionLocalOf { KineticTokens() }

@Composable
fun KineticTheme(dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalKinetic provides KineticTokens()) {
        MaterialTheme(
            colorScheme = if (dark) DarkColors else LightColors,
            typography = KTypography,
            shapes = Shapes(small = RoundedCornerShape(8.dp), medium = RoundedCornerShape(14.dp), large = RoundedCornerShape(22.dp)),
            content = content,
        )
    }
}
object K { val tokens: KineticTokens @Composable get() = LocalKinetic.current }
```

Typography: sizes in `sp` (scale with user font size), KDL `track` em → `letterSpacing = (-0.02).em`; `lineHeight = 44.sp`.

```kotlin
val KTypography = Typography(
    displaySmall = TextStyle(fontFamily = Display, fontSize = 40.sp, lineHeight = 44.sp, fontWeight = FontWeight.Light,
        letterSpacing = (-0.02).em, fontFeatureSettings = "tnum"),
    titleLarge = TextStyle(fontSize = 22.sp, lineHeight = 28.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.01).em),
    bodyLarge = TextStyle(fontSize = 17.sp, lineHeight = 24.sp),
    labelMedium = TextStyle(fontSize = 13.sp, lineHeight = 18.sp, fontWeight = FontWeight.Medium, letterSpacing = 0.01.em),
)
```

Material 3 default ramp (sp): display 57/45/36, headline 32/28/24, title 22/16/14, body 16/14/12, label 14/12/11. Collapse onto KDL's 5–8 steps; do not use all 15.

## 3. Layout and responsive

- Edge-to-edge: `enableEdgeToEdge()` in the Activity; handle insets with `Modifier.windowInsetsPadding(WindowInsets.safeDrawing)` or `Scaffold`'s `innerPadding`. Keyboard: `Modifier.imePadding()`; scrollable forms.
- Constraints, not devices: `BoxWithConstraints` locally; window size classes (`currentWindowAdaptiveInfo()` in material3-adaptive — verify artifact/version) for screen-level structure.
- Font scale: `sp` scales automatically; read `LocalDensity.current.fontScale` to reflow (Row → Column) at ≥ 1.5. Do not convert text sizes to `dp` to escape scaling (F10).
- Text: `softWrap = true`; `maxLines = 1` + `TextOverflow.Ellipsis` only for non-critical text (D28).
- Corners: `RoundedCornerShape` is circular; no continuous corner in the platform shapes — accept it on Android (it is native) unless the brand demands squircles.

## 4. Motion

```kotlin
fun <T> kSpring(response: Float, damping: Float) = spring<T>(
    dampingRatio = damping,
    stiffness = (2f * PI.toFloat() / response).pow(2),   // k = (2π/T)² with mass 1
)
// Presets for reference: Spring.StiffnessLow = 200, StiffnessMediumLow = 400, StiffnessMedium = 1500
```

- State-driven: `animateDpAsState`, `animateColorAsState`, `animateFloatAsState(targetValue, animationSpec = kSpring(0.4f, 0.9f))` — they retarget mid-flight.
- `AnimatedVisibility(enter = fadeIn() + expandVertically(), exit = …)`, `AnimatedContent(targetState) { … }` with `togetherWith`; `Modifier.animateContentSize()`.
- Gestures/interruptible: `Animatable` + `animateTo(target, spec, initialVelocity = velocity)` inside a coroutine; `Modifier.draggable`/`anchoredDraggable`.
- Shared elements: `SharedTransitionLayout { … Modifier.sharedElement(rememberSharedContentState(key = id), animatedVisibilityScope = this@AnimatedContent) }` — experimental API (`@OptIn(ExperimentalSharedTransitionApi::class)`); verify against the project's Compose version.
- Easing for tweens: M3 motion tokens (emphasized decelerate ≈ `CubicBezierEasing(0.05f, 0.7f, 0.1f, 1f)`); never `LinearEasing` on UI movement (D19).
- Reduce motion: Android's user setting is "Remove animations", which sets `Settings.Global.ANIMATOR_DURATION_SCALE` to 0:

```kotlin
@Composable
fun rememberReduceMotion(): Boolean {
    val ctx = LocalContext.current
    return remember { Settings.Global.getFloat(ctx.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) == 0f }
}
```

  Whether Compose animations automatically honour the animator scale depends on the Compose version — verify against current docs and branch explicitly for decorative motion.

## 5. Haptics

```kotlin
val haptics = LocalHapticFeedback.current
haptics.performHapticFeedback(HapticFeedbackType.LongPress)
// View-level, richer constants:
val view = LocalView.current
view.performHapticFeedback(HapticFeedbackConstants.CONFIRM)   // API 30+
```

| KDL | Android |
|---|---|
| selection | `HapticFeedbackConstants.CLOCK_TICK` or `SEGMENT_TICK` (API 34) / `HapticFeedbackType.TextHandleMove` |
| light / soft | `HapticFeedbackConstants.KEYBOARD_TAP` / `VIRTUAL_KEY` |
| medium / heavy / rigid | `HapticFeedbackConstants.LONG_PRESS` / `HapticFeedbackType.LongPress` |
| success | `HapticFeedbackConstants.CONFIRM` (API 30+) |
| warning / error | `HapticFeedbackConstants.REJECT` (API 30+) |

Newer Compose versions extend `HapticFeedbackType` (e.g. Confirm, Reject, ToggleOn) — verify for the project's version. Guard API levels with `Build.VERSION.SDK_INT`.

## 6. Accessibility

- `IconButton(onClick = …) { Icon(Icons.Outlined.Delete, contentDescription = "Delete entry") }`; decorative icons `contentDescription = null`.
- Grouping: `Modifier.semantics(mergeDescendants = true) {}` on rows; `Modifier.clearAndSetSemantics { contentDescription = "…" }` for custom summaries.
- `Modifier.semantics { heading() }` on section titles; `role = Role.Button` for custom clickables (`Modifier.clickable(role = Role.Button)`).
- Targets: Material components enforce 48 dp via `Modifier.minimumInteractiveComponentSize()`; keep it on custom controls.
- Traversal: `Modifier.semantics { traversalIndex = 1f }` + `isTraversalGroup = true` when visual order ≠ composition order.

## 7. Native fidelity

- Material 3 components are the native language on Android: `TopAppBar`/`LargeTopAppBar` with scroll behavior, `NavigationBar` (3–5 destinations), `ModalBottomSheet`, `FloatingActionButton` only for creation-first screens (C08), `SnackbarHost` with actions for undo (not for every confirmation, D10).
- Predictive back: keep system back working; `BackHandler` only to intercept for unsaved changes.
- Identity lives in color, type, shape and motion; do not import iOS chevrons/segmented controls wholesale (D24).

## 8. Compose-specific slop

| ID | Code signal | Fix |
|---|---|---|
| F02 | `onClick = {}` | Wire or remove |
| F07 | `Icon(…, contentDescription = null)` inside an `IconButton` | Describe it |
| F10 | text sizes in `.dp` or fixed `Density(fontScale = 1f)` | `sp`, reflow |
| D01 | `Brush.linearGradient(listOf(Purple, Blue))` | Solid + accent, or meaningful gradient |
| D16 | `Modifier.shadow(16.dp)` on many cards | Tonal elevation (`surfaceContainer*`) |
| D19 | `spring(dampingRatio = Spring.DampingRatioHighBouncy)` on utility UI, `LinearEasing` | Damped spring |
| D28 | `maxLines = 1, overflow = Ellipsis` on titles/prices; auto-size text hacks | Reflow |
| D29 | `Modifier.width(360.dp)` screen-sized frames | `fillMaxWidth`, constraints |
| D30 | Template `Purple40/PurpleGrey40/Pink40` | Decide the palette |

## 9. Verify

```bash
./gradlew lint
./gradlew testDebugUnitTest
./gradlew connectedDebugAndroidTest
adb shell cmd uimode night yes
adb shell settings put system font_scale 2.0
adb exec-out screencap -p > shots/android_xxl_dark.png
adb shell settings put system font_scale 1.0
```

Previews as a state matrix:

```kotlin
@Preview(name = "XXL dark", fontScale = 2f, uiMode = Configuration.UI_MODE_NIGHT_YES, widthDp = 320)
@Preview(name = "Default", widthDp = 411)
@Composable fun TonightPreview() = KineticTheme { TonightScreen(state = TonightState.Content(fixture)) }
```

Screenshot testing libraries (Paparazzi, Roborazzi, Compose Preview Screenshot Testing) are options when already in the project; do not add one only to verify a single change.
