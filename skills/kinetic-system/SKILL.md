---
name: kinetic-system
description: "Kinetic's design-system generator for mobile apps: decide typography, color roles (light and dark), spacing, shape, elevation, iconography, motion tokens and haptics in a fixed order, as KDL tokens validated for contrast, grid, ramp and budgets, then exported to Flutter, SwiftUI, Compose, React Native or CSS. Use for design systems, themes, tokens, palettes, type scales, or when a mobile UI's colors, fonts, spacing or radii are inconsistent."
---

# Build the system in the order decisions constrain each other

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

Each decision narrows the next. Making them out of order is how palettes end
up fighting typography and radii fight density.

In create/redesign the **type system, palette and motion personality were
dealt** (`.kinetic/deal.json`, chosen option): systemise them, don't re-choose
them. The display face carries the voice; text stays the platform face. The
palette's **field** and **proportion** are part of the decision (the field goes
in `system.color.roles.<theme>.field` with its `on-field`).

**Dark is designed, not derived.** The dark ground's hue follows the
thesis temperature, not the accent: a warm brief gets a warm near-black
(umber, clay), never the accent's navy; tape, paper and photo surfaces get
their own dark values so they don't turn to mud. In round 7 every Kinetic
design lost colour points (3 vs 4) on an untinted or cold dark theme.

## Order (write each into KDL `system`, then `kinetic validate`)
1. **Type** (`knowledge/typography.md`): families (system first on iOS), a
   5–8 step ramp anchored on body 17 (iOS) / 16 (Android), ratio from the
   expression level, line heights, em tracking, numerals, width (condensed numerals for dense figures, typography.md §8b). Platform ramps:
   `knowledge/platform-ios.md`, `knowledge/platform-android.md`.
2. **Color** (`knowledge/color.md`; data colors such as transit lines or categories go in `system.color.data`, §8b): the dealt palette's seed (or the brand's) →
   `kinetic palette "#seed" --kdl` → edit roles for atmosphere (warm/cool
   neutrals, accent restraint) → keep every pair passing. Dark theme designed:
   tonal surfaces, desaturated accent, near-white text.
3. **Space** (`knowledge/layout.md`): unit 4, 6–9 named steps, one screen margin per class.
4. **Shape**: 3–4 radii + full, concentric nesting rule, continuous corners on iOS.
5. **Elevation**: one strategy — tonal, border, shadow or none.
6. **Icon** (`knowledge/iconography-svg.md`): one family, one weight matched to
   text, selection by fill; sizes per text style. Custom SVGs follow the 24-grid rules.
7. **Motion** (`knowledge/motion.md`): personality, 2–4 springs `{response, damping}`,
   2–4 durations, reduce-motion policy. `kinetic spring r d` shows the physics.
8. **Haptics**: map events to `selection light soft medium rigid heavy success warning error`.

## Rules
- **Roles, not values.** Components reference `$color.text-2`, `$type.body`,
  `$space.l` — never literals. The validator resolves every reference.
- **Budgets come from the expression level** (accents, families, display size,
  signature moments). Exceeding a budget needs a `because` tied to the thesis.
- **Respect a coherent existing system** (redesign/improve): start from
  `kinetic dna <paths> --kdl`, KEEP what is coherent, EVOLVE what drifts, and
  only REPLACE what is cheap or harmful. A design system for one screen is overkill — tokens exist when reused.
- **Brand**: `strict` → brand hex kept for brand moments, UI roles derived
  (darker accent for text/actions if the brand hex fails contrast).
- Name tokens by role and scale (`text-2`, `space.l`, `radius.m`), never by
  value (`grey-600-ish`) or by screen (`home-card-padding`).

## Export and integrate
```
kinetic validate .kinetic/design.kdl
kinetic export .kinetic/design.kdl --stack flutter --out lib/theme/
kinetic export .kinetic/design.kdl --stack swiftui --out Sources/DesignSystem/
```
Flutter: `ThemeExtension<KColors>` + `kineticTheme(Brightness)`, `KSpace`,
`KRadius`, `KType`, `KMotion.of(context, d)` (reduce-motion aware), `KHaptics`.
SwiftUI: `Color.kText` / `.foregroundStyle(.kText)`, `.kText(KType.body)`
(Dynamic Type via `@ScaledMetric`), `KSpace`, `KRadius.shape()`,
`Animation.kSettle`, `.kAnimation(_, value:)` (reduce-motion aware), `KHaptic`.
Compose: `KineticTheme {}`, `LocalKColors`, `KSpace`, `KRadius`, `KType`, `KMotion`.
RN: `useTokens()`, Reanimated spring configs. CSS: custom properties + `linear()` springs.
Generated files carry a header; edit the KDL and re-export instead of editing them.
Then wire the stack's theme entry point (see `knowledge/stacks/<stack>.md`).

## Done when
`kinetic validate` shows no F and no major D in `system`; the contrast table
passes in both themes; every component reference resolves; the export
compiles in the project (`flutter analyze`, `xcodebuild`/`swiftc -typecheck`, `tsc`, Gradle).
