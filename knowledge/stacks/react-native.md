# React Native / Expo — design ↔ code

Load when `product.stack: react-native` or `package.json` depends on `react-native` / `expo`.

## 1. Detect and read (code-to-design)

| Look at | Reveals |
|---|---|
| `package.json` | Expo SDK, navigation (`@react-navigation/*`, `expo-router`), animation (`react-native-reanimated`, `moti`), styling (`nativewind`, `tamagui`, `@shopify/restyle`, `unistyles`), icons (`@expo/vector-icons`, `lucide-react-native`, `expo-symbols`), `expo-haptics`, `react-native-safe-area-context` |
| `theme.ts`, `tokens.ts`, `constants/Colors.ts` (Expo template), `tailwind.config.js` | Palette, type, spacing — the Expo template's `Colors.ts` with `tint: '#0a7ea4'` untouched is D30 |
| `app.json` / `app.config.ts` | `userInterfaceStyle` (`automatic` needed for dark mode), splash/background colors |
| Components | Inline `style={{ padding: 13, fontSize: 15, color: '#333' }}`, `StyleSheet.create` literals, `shadowOpacity`/`elevation` |

Run `kinetic dna src --json` (or `app/`), read the theme module and 2–3 screens, fill KDL `audit`. If a styling library already owns tokens (Restyle, Tamagui, NativeWind config), implement KDL *through it* — do not add a second token system.

## 2. Token architecture

```ts
// design/tokens.ts
export const palette = {
  light: { bg: '#F2F1EE', surface: '#FFFFFF', text: '#1E1A16', text2: '#5C5249', border: '#E4DAD0', accent: '#8A5A2B', onAccent: '#FFFFFF', danger: '#B3261E' },
  dark:  { bg: '#0F0D0B', surface: '#1A1714', text: '#EDE6DE', text2: '#A89C90', border: '#2C2722', accent: '#D9A877', onAccent: '#1E1408', danger: '#F2B8B5' },
} as const;
export type Roles = typeof palette.light;

export const space = { xs: 4, s: 8, m: 12, l: 16, xl: 24, xxl: 32 } as const;
export const radius = { s: 8, m: 14, l: 22, full: 999 } as const;

// KDL track is em; RN letterSpacing is in points → track * fontSize
const t = (size: number, line: number, weight: '300'|'400'|'500'|'600'|'700', trackEm = 0, family?: string) =>
  ({ fontSize: size, lineHeight: line, fontWeight: weight, letterSpacing: trackEm * size, fontFamily: family });
export const type = {
  display: { ...t(40, 44, '300', -0.02), fontVariant: ['tabular-nums'] as const },
  title: t(22, 28, '600', -0.01),
  body: t(17, 24, '400'),
  caption: t(13, 18, '500', 0.01),
} as const;
```

```ts
// design/useTheme.ts
import { useColorScheme } from 'react-native';
export function useTheme() {
  const scheme = useColorScheme();               // 'light' | 'dark' | null
  const colors = palette[scheme === 'dark' ? 'dark' : 'light'];
  return { colors, space, radius, type };
}
```

Custom font families with weights: on Android each weight is usually a separate family name (`Inter-SemiBold`), and `fontWeight` alone may not select it — verify with the font loading setup (`expo-font`).

## 3. Layout and responsive

- Flexbox defaults to `column`; use `flexShrink: 1` on text in rows so it wraps instead of overflowing.
- Safe areas: `react-native-safe-area-context` — `SafeAreaProvider` at root, `useSafeAreaInsets()` for custom headers/bottom bars. (Core `SafeAreaView` is iOS-only and limited.)
- Keyboard: `KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined}`; `keyboardShouldPersistTaps="handled"` on scroll views.
- Dimensions: `useWindowDimensions()` (reactive) rather than `Dimensions.get` at module load.
- Text scaling: `allowFontScaling` defaults to true — keep it (F10). `maxFontSizeMultiplier` per component only with a reason (a hero numeral), never globally. Read `useWindowDimensions().fontScale` to reflow rows at large scales.
- Continuous corners on iOS: `borderCurve: 'continuous'` style (iOS only; ignored on Android).
- Hit areas: `Pressable hitSlop={8}` + `minWidth/minHeight: 44` (iOS) / 48 (Android).

## 4. Motion (Reanimated)

```ts
import { withSpring, withTiming, useReducedMotion, ReduceMotion } from 'react-native-reanimated';

// KDL {response, damping} → physics config (mass 1)
export const kSpring = (response: number, damping: number) => ({
  mass: 1,
  stiffness: Math.pow((2 * Math.PI) / response, 2),   // k = (2π/T)²
  damping: (4 * Math.PI * damping) / response,         // c = 4πζ/T
});
// usage: offset.value = withSpring(target, { ...kSpring(0.4, 0.9), reduceMotion: ReduceMotion.System });
```

- Reanimated 3 also accepts a `{ duration, dampingRatio }` spring config; physics config above is the exact mapping from KDL.
- Animations run on the UI thread via shared values and `useAnimatedStyle`; keep JS-thread `Animated` API only for legacy code.
- Layout animations: `entering={FadeIn.duration(200)}`, `layout={LinearTransition.springify()}` — use for what actually changed, not every list item (D18). Check names against the installed Reanimated version.
- Gestures: `react-native-gesture-handler` `Gesture.Pan()` → on end `withSpring(target, { ...kSpring(…), velocity: e.velocityX })` for interruptible settling.
- Shared element transitions: Reanimated `sharedTransitionTag` is experimental — verify support for the installed version and navigator before relying on it.
- Reduce motion: `useReducedMotion()` (Reanimated) or `AccessibilityInfo.isReduceMotionEnabled()` + `AccessibilityInfo.addEventListener('reduceMotionChanged', …)`; `reduceMotion: ReduceMotion.System` on individual animations.
- **Core `Animated` only** (no Reanimated installed — brownfield apps, sandboxes): `Animated.spring(value, { stiffness, damping, mass: 1, useNativeDriver: true })` takes the same physics config as the export (`springs.*`); animate only `transform` and `opacity` with the native driver; gate every loop on `AccessibilityInfo.isReduceMotionEnabled()` read once in a hook (`useEffect` + `reduceMotionChanged` listener) and render the still end state when it is on. Ambient loops (a breathing "live" dot) use `Animated.loop` with ≥ 1.2 s per half-cycle and stop under reduce motion.

## 5. Haptics (`expo-haptics`)

| KDL | expo-haptics |
|---|---|
| selection | `Haptics.selectionAsync()` |
| light / medium / heavy | `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light / Medium / Heavy)` |
| soft / rigid | `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft / Rigid)` |
| success / warning / error | `Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success / Warning / Error)` |

Bare RN without Expo: `react-native-haptic-feedback` is the common alternative — check what is installed first. With no haptics package at all, map every KDL haptic to `none` (validate accepts it) and keep the visual confirmation — never call `Vibration.vibrate()` as a stand-in for UI feedback.

## 6. Accessibility

- `accessibilityRole="button"`, `accessibilityLabel="Delete entry"`, `accessibilityState={{ disabled, selected }}`, `accessibilityHint` sparingly.
- Group a row: `accessible` on the container (children merge on iOS); decorative: `accessibilityElementsHidden` (iOS) + `importantForAccessibility="no-hide-descendants"` (Android).
- Headers: `accessibilityRole="header"`.
- Check: `AccessibilityInfo.isScreenReaderEnabled()`; test with VoiceOver/TalkBack on device.

## 7. Native fidelity

- Navigation: native stack (`@react-navigation/native-stack` / `expo-router` Stack) gives real iOS large titles, back swipe and Android predictive back; prefer it to JS stacks. Sheets: native-stack `presentation: 'formSheet'` with detents where supported (verify version), or `@gorhom/bottom-sheet` if already used.
- Icons: `expo-symbols` renders SF Symbols on iOS — pair with a Material Symbols fallback on Android; one family per platform (D06).
- Controls: platform `Switch`, `@react-native-community/datetimepicker`; Android ripple via `Pressable android_ripple`, iOS pressed opacity/scale — branch with `Platform.select`.

## 8. RN-specific slop

| ID | Code signal | Fix |
|---|---|---|
| F02 | `onPress={() => {}}` | Wire or remove |
| F07 | `Pressable`/`TouchableOpacity` with only an icon and no `accessibilityLabel` | Label |
| F10 | `allowFontScaling={false}`, `maxFontSizeMultiplier={1}` broadly | Remove; reflow |
| D01 | `expo-linear-gradient` with violet/blue stops | Solid + accent |
| D16 | `shadowOpacity: 0.3, shadowRadius: 20` / `elevation: 10` everywhere | One elevation strategy |
| D19 | `Easing.bounce`, `Easing.elastic`, `Easing.linear` on UI, very low damping | Damped spring |
| D28 | `adjustsFontSizeToFit`, `numberOfLines={1}` on critical text | Reflow |
| D29 | `width: 375`, `Dimensions.get('window').height * 0.4` layouts | Flex, `useWindowDimensions` |
| D30 | Expo template `tint` colors untouched | Decide the palette |

## 9. Verify

```bash
npx tsc --noEmit
npx eslint .
npx expo start            # or: npx react-native run-ios / run-android
xcrun simctl io booted screenshot shots/ios.png
adb exec-out screencap -p > shots/android.png
```

Static previews (react-native-web, Storybook) ignore the OS font scale: to show the XXL layout, render an entry inside a preview-only context that multiplies the type tokens (e.g. ×1.6 and ×2) — label it as a simulation and keep `allowFontScaling` on in the real components.

E2E/screenshot flows: Maestro (`maestro test flow.yaml`, `takeScreenshot`) or Detox, if already present. Matrix: iPhone SE + Pro Max, small Android (360 dp), light/dark, font scale 1 and 2, Reduce Motion on.

## Bundling dealt faces
macOS ships most native display faces as `.ttc` collections (Charter, Avenir Next, Didot, Copperplate…), which neither Flutter nor React Native can load. Run `kinetic font split /System/Library/Fonts/Supplemental/<Face>.ttc --out fonts/` and declare the faces you use (one file per weight).

## Bundled faces with several weights
On Android, React Native selects a bundled font by family name per file: declare one family per weight (`Charter-Bold`, `Charter-Roman`) in a small map in your theme (`fontFamily: weights[700]`) rather than `fontWeight` on one family, which falls back to faux bold on Android and web.
