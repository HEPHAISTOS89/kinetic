# SwiftUI — design ↔ code

Load when `product.stack: swiftui` or the project has `*.xcodeproj` / `Package.swift` with `import SwiftUI` views.

## 1. Detect and read (code-to-design)

| Look at | Reveals |
|---|---|
| `Assets.xcassets/*.colorset/Contents.json` | Named colors with Any/Dark appearances (the real palette, often) |
| `Assets.xcassets/AccentColor.colorset` | Global tint — check it was decided, not left default blue (D30) |
| `**/Color+*.swift`, `**/Theme*.swift`, `**/DesignSystem/` | `extension Color`, `extension Font`, `ShapeStyle` extensions, spacing enums |
| `Info.plist` → `UIAppFonts` | Custom fonts bundled |
| Views | Literal `.padding(13)`, `.font(.system(size: 15))`, `Color(red:green:blue:)`, `.cornerRadius(…)`, `.shadow(…)`, `.animation(.easeInOut)` |
| Deployment target (project settings) | Which APIs are allowed: iOS 16 (`ViewThatFits`, `presentationDetents`), 17 (`sensoryFeedback`, `Spring(duration:bounce:)`, `.spring(duration:bounce:)`), 18 (`navigationTransition(.zoom)`, `MeshGradient`), 26 (Liquid Glass) |

Run `kinetic dna <Sources> --json`, then read the theme files and 2–3 screens. Map to KDL `audit` (keep / evolve / replace / remove). Strong SwiftUI apps often keep system typography and semantic colors — that is a *keep*, not a lack of design (C01, C10).

Signals of a bypassed system: `.font(.system(size:))` everywhere (no Dynamic Type), hex initialisers inline, `.foregroundColor(.black)` (breaks dark mode), `.cornerRadius` (deprecated, circular corners).

## 2. Token architecture

```swift
import SwiftUI

// Colors: dynamic light/dark from code (or from asset catalog — prefer assets for designers' handoff)
extension Color {
    init(light: UInt32, dark: UInt32) {
        self.init(uiColor: UIColor { $0.userInterfaceStyle == .dark ? UIColor(hex: dark) : UIColor(hex: light) })
    }
    static let kBg      = Color(light: 0xF2F1EE, dark: 0x0F0D0B)
    static let kSurface = Color(light: 0xFFFFFF, dark: 0x1A1714)
    static let kText    = Color(light: 0x1E1A16, dark: 0xEDE6DE)
    static let kText2   = Color(light: 0x5C5249, dark: 0xA89C90)
    static let kAccent  = Color(light: 0x8A5A2B, dark: 0xD9A877)
}
extension UIColor {
    convenience init(hex: UInt32) {
        self.init(red: CGFloat((hex >> 16) & 0xFF) / 255, green: CGFloat((hex >> 8) & 0xFF) / 255,
                  blue: CGFloat(hex & 0xFF) / 255, alpha: 1)
    }
}
// Optional: ShapeStyle access so `.foregroundStyle(.kText)` works
extension ShapeStyle where Self == Color { static var kText: Color { .kText } }

// Spacing & radius: plain enums; scale with Dynamic Type only where layout should breathe
enum KSpace { static let xs: CGFloat = 4, s: CGFloat = 8, m: CGFloat = 12, l: CGFloat = 16, xl: CGFloat = 24, xxl: CGFloat = 32 }
enum KRadius { static let s: CGFloat = 8, m: CGFloat = 14, l: CGFloat = 22 }
```

Typography — every style must scale with Dynamic Type. KDL `track` (em) → `.tracking(track * size)`; `line` → `.lineSpacing(line - font.lineHeight)` is approximate; prefer the system styles' built-in leading, adjust with `.lineSpacing` only where measured.

```swift
struct KType {
    let font: Font; let tracking: CGFloat
    static let display = KType(font: .custom("NewYork-Light", size: 40, relativeTo: .largeTitle), tracking: -0.02 * 40)
    static let title   = KType(font: .system(.title2, design: .default, weight: .semibold), tracking: -0.01 * 22)
    static let body    = KType(font: .body, tracking: 0)
    static let caption = KType(font: .system(.footnote, weight: .medium), tracking: 0.01 * 13)
}
extension View {
    func kType(_ t: KType) -> some View { self.font(t.font).tracking(t.tracking) }
}
```

- `Font.system(size:)` does **not** scale with Dynamic Type — use text styles (`.body`, `.title2`…) or `.custom(_:size:relativeTo:)`.
- Numerals: `.monospacedDigit()` for counters/prices; `.fontDesign(.rounded)` (iOS 16.1+) when KDL `numeric` is SF Pro Rounded.
- Spacing that must grow with text: `@ScaledMetric(relativeTo: .body) private var rowPadding: CGFloat = 12`.
- iOS default type ramp (Large size, pt): largeTitle 34, title 28, title2 22, title3 20, headline 17 semibold, body 17, callout 16, subheadline 15, footnote 13, caption 12, caption2 11. Prefer mapping KDL steps onto these.

Inject non-color tokens with an `EnvironmentKey` only when they vary (themes, brands); static enums are simpler otherwise.

## 3. Layout and responsive

- Let views size themselves; use `.frame(maxWidth: .infinity, alignment: .leading)` instead of fixed widths (D29).
- `ViewThatFits { HStack { … }; VStack { … } }` (iOS 16) to switch arrangement when content or Dynamic Type no longer fits.
- `@Environment(\.dynamicTypeSize) var size` + `if size.isAccessibilitySize { VStack… }` for explicit reflow.
- Clamp Dynamic Type only per view, with a reason (a 96 pt hero numeral): `.dynamicTypeSize(...DynamicTypeSize.accessibility2)`. Never app-wide (F10).
- Safe areas are respected by default; use `.ignoresSafeArea(edges:)` only for backgrounds. Bottom bars: `.safeAreaInset(edge: .bottom) { … }` so scroll content is not hidden.
- Keyboard: SwiftUI avoids the keyboard by default in scroll views; `@FocusState` + `.scrollDismissesKeyboard(.interactively)`; `.toolbar { ToolbarItemGroup(placement: .keyboard) { … } }` for actions.
- Corners: `RoundedRectangle(cornerRadius: KRadius.m, style: .continuous)`; `.clipShape(.rect(cornerRadius: 14, style: .continuous))` (iOS 17). `.cornerRadius()` is deprecated and circular. Concentric: inner = outer − padding (iOS 26 adds `ConcentricRectangle` — verify against current docs before use).
- `.contentShape(Rectangle())` so the whole row is tappable, not just the text.

## 4. Motion

KDL `{response, damping}` maps directly:

```swift
extension Animation {
    static func kSpring(_ response: Double, _ damping: Double) -> Animation {
        .spring(response: response, dampingFraction: damping)          // iOS 13+
    }
}
// iOS 17 equivalent: .spring(duration: response, bounce: 1 - damping)  // approximation valid for damping ≤ 1; verify feel
// Spring value type (iOS 17): Spring(response: 0.4, dampingRatio: 0.9)
```

- SwiftUI springs are interruptible and retarget with velocity preserved — prefer them to `.easeInOut(duration:)` for UI state changes. No `.bouncy` on utility UI (D19); `.snappy`/`.smooth` presets are acceptable defaults when KDL does not specify.
- Scope animations: `withAnimation(.kSpring(0.4, 0.9)) { state.toggle() }` or `.animation(.kSpring(…), value: state)` — never value-less `.animation(_:)` (deprecated; animates everything).
- Transitions: `.transition(.opacity.combined(with: .scale(scale: 0.98)))`, `.contentTransition(.numericText())` for changing numbers (iOS 16+), `.symbolEffect(.bounce, value:)` / `.contentTransition(.symbolEffect(.replace))` for SF Symbols (iOS 17).
- Shared element in a screen: `@Namespace var ns` + `.matchedGeometryEffect(id: item.id, in: ns)`. Across navigation (iOS 18): source `.matchedTransitionSource(id: item.id, in: ns)`, destination `.navigationTransition(.zoom(sourceID: item.id, in: ns))`.
- Gestures: `DragGesture` with `.onEnded { v in withAnimation(.interpolatingSpring(…)) }`; feed `v.velocity` (iOS 17) when settling.
- Reduce motion:

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion
…
.transition(reduceMotion ? .opacity : .move(edge: .bottom).combined(with: .opacity))
withAnimation(reduceMotion ? .easeOut(duration: 0.15) : .kSpring(0.4, 0.9)) { … }
```

## 5. Haptics

```swift
.sensoryFeedback(.selection, trigger: selectedTab)                 // iOS 17
.sensoryFeedback(.impact(flexibility: .soft, intensity: 0.6), trigger: count)
.sensoryFeedback(.success, trigger: saveSucceeded)                 // fire on the confirmed outcome
// iOS < 17: UIImpactFeedbackGenerator(style: .soft).impactOccurred()
//           UINotificationFeedbackGenerator().notificationOccurred(.success)
//           UISelectionFeedbackGenerator().selectionChanged()
```

| KDL | SwiftUI `SensoryFeedback` (17+) | UIKit |
|---|---|---|
| selection | `.selection` | `UISelectionFeedbackGenerator` |
| light / medium / heavy | `.impact(weight: .light/.medium/.heavy)` | `UIImpactFeedbackGenerator(style: .light/.medium/.heavy)` |
| soft / rigid | `.impact(flexibility: .soft/.rigid)` | `UIImpactFeedbackGenerator(style: .soft/.rigid)` |
| success / warning / error | `.success` / `.warning` / `.error` | `UINotificationFeedbackGenerator` |

## 6. Accessibility

- Icon-only buttons: `Button { … } label: { Image(systemName: "trash") }.accessibilityLabel("Delete entry")`, or use `Label("Delete", systemImage: "trash").labelStyle(.iconOnly)` which keeps the title for VoiceOver.
- Group: `.accessibilityElement(children: .combine)` on rows; `.accessibilityHidden(true)` on decoration.
- Traits: `.accessibilityAddTraits(.isHeader)` on section titles; `.accessibilityValue("7 hours 40")` for custom controls.
- Order: `.accessibilitySortPriority(_:)` when visual order differs.
- Targets ≥ 44×44 pt: `.frame(minWidth: 44, minHeight: 44).contentShape(Rectangle())`.
- Respect `\.legibilityWeight` (Bold Text), `\.colorSchemeContrast` (Increase Contrast) when custom colors are subtle.

## 7. Native fidelity

- Prefer system containers: `NavigationStack` with `.navigationTitle` + `.navigationBarTitleDisplayMode(.large)`; `List`/`Form` with `.listStyle(.insetGrouped)`; `.toolbar` items; `.searchable`; `.refreshable`; `.swipeActions`; `Menu`; `.confirmationDialog` for destructive choices.
- Sheets: `.sheet` + `.presentationDetents([.medium, .large])` + `.presentationDragIndicator(.visible)` + `.presentationCornerRadius` (iOS 16.4).
- Materials (`.regularMaterial`, `.ultraThinMaterial`) belong on bars, sheets and overlays over moving content, not on cards (D05). iOS 26 Liquid Glass (`.glassEffect()`, glass button styles) — apply to navigation/controls layer only, per Apple guidance; verify API names against the current SDK.
- SF Symbols: one weight family per screen, matched to the text weight (`.fontWeight` affects symbols); `.symbolRenderingMode(.hierarchical)` for depth without new colors; `.symbolVariant(.fill)` for selection only.
- No FAB (D09), no hamburger drawer (D08), no Material ripple (D24). Pressed state: `ButtonStyle` with `configuration.isPressed` → opacity 0.7 or scale 0.97 + spring.

```swift
struct KPressStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .opacity(configuration.isPressed ? 0.85 : 1)
            .animation(.kSpring(0.25, 0.9), value: configuration.isPressed)
    }
}
```

## 8. SwiftUI-specific slop

| ID | Code signal | Fix |
|---|---|---|
| F02 | `Button("…") { }`, `Button(action: {})` | Wire or remove |
| F07 | `Button { } label: { Image(systemName:) }` without `accessibilityLabel` | Label / `Label` + `.iconOnly` |
| F08 | `withAnimation`/`.transition(.move…)` with no `accessibilityReduceMotion` branch | Branch |
| F10 | `.dynamicTypeSize(.large)` (fixed) at app root, `.font(.system(size:))` everywhere | Text styles / `relativeTo:` |
| D01 | `LinearGradient(colors: [.purple, .blue] …)` | Solid + accent, or meaningful gradient |
| D05 | `.background(.ultraThinMaterial)` on content cards | Tonal surface |
| D15 | `.cornerRadius(…)` mixed values, circular corners | `RoundedRectangle(…, style: .continuous)`, 3–4 radii |
| D16 | `.shadow(radius: 10+)` on many views | One elevation strategy |
| D19 | `.interpolatingSpring(stiffness:damping:)` very low damping, `.bouncy` on utility UI, `.linear` | Damped spring |
| D28 | `.minimumScaleFactor(0.5)`, `.lineLimit(1)` on critical text | Reflow / `ViewThatFits` |
| D29 | `.frame(width: 375)`, `UIScreen.main.bounds` arithmetic | Flexible frames, `GeometryReader` only when necessary |
| D30 | AccentColor left default blue with no decision | Decide accent |
| — | `.foregroundColor(.black)` / `.white` on text | Semantic/dynamic colors (`.primary`, tokens) |

## 9. Verify

```bash
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' build
xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 16'
xcrun simctl boot "iPhone SE (3rd generation)"
xcrun simctl ui booted appearance dark
xcrun simctl io booted screenshot shots/se_dark.png
```

Set larger text in the simulator through Settings → Accessibility → Display & Text Size → Larger Text (a `simctl ui … content_size` subcommand exists in recent Xcode versions — verify with `xcrun simctl ui help`).

Previews as a state matrix:

```swift
#Preview("XXL · dark") {
    TonightView(model: .fixture(.content))
        .environment(\.dynamicTypeSize, .accessibility3)
        .preferredColorScheme(.dark)
}
#Preview("Empty") { TonightView(model: .fixture(.empty)) }
#Preview("Error") { TonightView(model: .fixture(.error)) }
```

Devices to cover: iPhone SE (375×667 pt, smallest current), iPhone 16 / 16 Pro, iPhone 16 Pro Max; light/dark; Large and AX3 text; Reduce Motion on (Settings → Accessibility → Motion).

## Rendering for review (macOS `ImageRenderer` harnesses)
Kinetic's A/B harness and quick reviews render SwiftUI to PNG on macOS. Know its limits so a blank render isn't mistaken for a broken screen:
- `ScrollView`, `List` and navigation bars render **empty** with `ImageRenderer`; for review renders, put the content in a `VStack` behind a `#if os(macOS)`/gallery flag and keep the real `ScrollView`/`List`/`NavigationStack` for the app.
- Dynamic Type does not scale (`@ScaledMetric`, text styles stay at Large): XXL evidence needs the iOS Simulator. A gallery entry that forces the accessibility *layout* branch is useful but must be labelled "layout only, text not scaled".
- `ProgressView` may draw as a solid square; mark loading renders as approximate.
- Navigation bars/toolbars are not drawn: keep the real `NavigationStack` + `.toolbar` for the app (inside `#if canImport(UIKit)` where it uses iOS-only placements such as `.topBarLeading`) and give gallery entries a stand-in bar view so the renders show the header.
- A `fixedSize` stack wrapped in `.frame(maxHeight: .infinity, alignment: .top)` still reports its full height as the minimum; add `minHeight: 0` so the device frame doesn't overflow and re-centre.
- Content taller than the fixed render frame is **centred and compressed** (rows overlap, text clips). For review renders, lay the screen out at its natural height and crop: `content.fixedSize(horizontal: false, vertical: true).frame(width: 393, height: 852, alignment: .top).clipped()`.
- Dark mode: pass `.environment(\.colorScheme, .dark)` and render inside `NSAppearance(named: .darkAqua)!.performAsCurrentDrawingAppearance { }` so dynamic `NSColor`s resolve.

## Locale-correct formatting
`Date.formatted()` and `Measurement.formatted()` use `Locale.current`, not the SwiftUI `\.locale` environment. Read `@Environment(\.locale)` and pass it: `date.formatted(.dateTime.hour().minute().locale(locale))`, `distance.formatted(.measurement(width: .abbreviated, usage: .road).locale(locale))` (en_GB road distances use yards/miles; fr_FR uses metres). Previews should set `.environment(\.locale, Locale(identifier: "fr_FR"))` to test.

## Font width
`Font.system(size:weight:design:).width(.condensed)` (iOS 16+) or `.fontWidth(.condensed)` on Text. `kinetic export` emits it from KDL `width:`.
