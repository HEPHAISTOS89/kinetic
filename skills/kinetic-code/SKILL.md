---
name: kinetic-code
description: "Kinetic's design-to-code and code-to-design layer for Flutter/Dart, SwiftUI, Jetpack Compose/Kotlin, React Native/TypeScript and mobile web: read an existing codebase's real design system, implement a KDL design idiomatically with exported tokens and the smallest coherent diff, and verify with the stack's analyzers and renders. Use whenever Kinetic design decisions must become code, or code must be understood as design."
---

# Code is where design becomes true (or false)

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

## Code-to-design (understand before changing)
1. Detect the stack (`kinetic init` does it; or read `pubspec.yaml`,
   `*.xcodeproj`/`Package.swift`, `build.gradle(.kts)`, `package.json`).
2. Read `knowledge/stacks/<stack>.md` §Detect & read: where the theme, tokens,
   components and navigation live.
3. `kinetic scan <src>` → facts and findings with file:line.
   `kinetic dna <src>` → the de-facto system and coherence per dimension.
   `kinetic dna <src> --kdl` → editable `audit` + `system` draft.
   `kinetic states code <src>` → data screens missing state handling.
4. Open the files behind the main findings; confirm `inferred` ones in context.
5. For D2–D3 audits, delegate to the **kinetic-forensics** agent (fresh
   context, returns docs/PROTOCOL.md §5) and merge its classification into KDL `audit`.

## Design-to-code (implement)
1. **Tokens first**: `kinetic export .kinetic/design.kdl --stack <stack> --out <theme dir>`;
   wire the theme entry point (stacks/<stack>.md §Token architecture).
2. **Components next**: buttons, fields, rows, cards, sheets with all KDL
   `variants` and states, reading only tokens.
3. **Screens last**: composition per KDL `screens[]` — primary element,
   reading order, thumb-zone actions, every state branch, motion specs.
4. **Smallest coherent diff** in the existing architecture: no new packages
   unless the repo proves the need; no state-management, navigation or data
   changes for a visual task; reuse decent components; replace cheap ones.
5. **Platform adaptation**: native controls, navigation and feedback per
   platform (`knowledge/platform-ios.md`, `knowledge/platform-android.md`);
   share identity, not chrome.
6. **Accessibility in the code, not after**: labels, traits/roles, grouping,
   focus order, Dynamic Type / font scale, reduce motion, contrast via roles.

## Multi-language standards
| Stack | Tokens | Must use | Must avoid |
|---|---|---|---|
| Flutter | `ThemeExtension`, `ThemeData` | `TextScaler` respected, `LayoutBuilder`/`MediaQuery.sizeOf`, `SafeArea`, `MediaQuery.disableAnimationsOf`, adaptive widgets | `TextScaler.noScaling`, `FittedBox` patches, `width: 375`, scattered `Color(0x…)` |
| SwiftUI | `Color`/`ShapeStyle` extensions, `KTextStyle` | text styles / `relativeTo:`, `@ScaledMetric`, `ViewThatFits`, `.continuous` corners, `accessibilityReduceMotion`, `sensoryFeedback` | `.font(.system(size:))` everywhere, `minimumScaleFactor`, fixed frames, `.dynamicTypeSize(.large)` |
| Compose | `MaterialTheme` + `CompositionLocal` | `sp` for text, `WindowInsets`, `minimumInteractiveComponentSize`, `contentDescription` | `fontScale = 1f`, `contentDescription = null` on actions, `Color(0x…)` in screens |
| React Native | typed tokens + `useTokens()` | safe-area-context, `accessibilityLabel`, Reanimated springs, `useReducedMotion` | `allowFontScaling={false}`, `onPress={() => {}}`, inline magic numbers |
| Web (mobile) | CSS custom properties | `dvh`, `env(safe-area-inset-*)`, `prefers-reduced-motion`, `rem` type | `100vh`, `user-scalable=no`, hover-only interactions |

## Verify (every change)
- `kinetic scan <changed files>` → no F, no new major D.
- Stack analyzers: `flutter analyze` (+ golden tests if present) · `xcodebuild … build` or `swiftc -typecheck` · `./gradlew lint` · `tsc --noEmit && eslint`.
- Renders: simulator/emulator screenshots of each changed screen in light/dark and default/largest text (`knowledge/stacks/<stack>.md` §Verification lists the commands; the iOS Simulator tool can capture directly).
- Never claim a render was checked if it wasn't; say which states were not rendered.
