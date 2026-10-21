# Kinetic feedback log (Courant home, create / D2, SwiftUI)

Candid notes on where the instructions, knowledge or engine were unclear, wrong, missing or in the way.

## Instructions / skills
- **Reading cost before the first pixel is high.** For D2 the router sends you through 8 module skills + ~12 knowledge files (~3,800 lines). There is no "D2 minimum reading list"; I read nearly everything to be safe. A per-depth checklist ("for D2 SwiftUI read: states.md, copy.md §3, stacks/swiftui.md, platform-ios.md §2/§5/§8, anti-slop F+D tables") would save a lot.
- **The motion skill says "spec every animation in KDL", but the validator counts every motion entry against the *signature-moment* budget** (D18 "4 motion moments for expression 2"). A toggle's symbol swap or a text crossfade is feedback, not a signature moment. Following one instruction trips the other. I resolved it by making two changes instant (which fit my spine anyway), but the rule conflates "feedback motion" with "signature moments". Suggest a `kind: feedback | transition | signature` field and budget only `signature`.
- **The init skeleton for `--mode create` omits sections that `create` requires** (`directions`, `journeys`, `system`, `screens`, `signature`); you have to assemble them from KDL.md and `kinetic states template <id>` (whose output is a bare list item with no `screens:` key, so it can't be pasted as-is). I rewrote the file from the KDL.md example instead.
- `kinetic init` in an empty directory named the product after the folder ("B") and set `stack: mixed, platforms: [ios, android]`. There is no `--stack` / `--name` flag for greenfield projects, so the first thing you do is fix wrong guesses.
- The critique module requires renders "default + largest text size, smallest + largest phone", but the provided harness can only do 393x852 at default size (and the plugin itself acknowledges macOS ImageRenderer ignores Dynamic Type). There is no fallback guidance (e.g. "render the AX layout by forcing the accessibility branch in a gallery entry"). I did that myself.
- The agents (director / critic / forensics) are mandatory in the pipeline text; when agents can't be launched there is no "self-critique protocol" to reduce author bias (e.g. "critique from renders only, before re-reading your own KDL").

## Knowledge
- No **transit / mobility-at-a-glance** sector entry beyond "Mobility / maps / delivery", which assumes the map is the canvas and a bottom sheet holds the state. For a departures board that is the wrong default (the map is exactly what a walking rider does not need). A "Transit / timetables" playbook (realtime vs scheduled, last departure, end of service, closures with alternatives, line colors as data) would help.
- **Data colors vs accent budget is not addressed.** Transit line colors are network identity (data), not accents, but nothing says how they relate to the level-2 "1 saturated accent" budget, or whether they belong in KDL roles. I kept them out of `system.color` and in fixture data.

## Engine
- `kinetic contrast` + zsh: no issue in the engine itself, but the docs' loop examples assume bash word splitting.
- `kinetic export --stack swiftui`: no way to express **font width** (SF Pro Condensed/Compressed) — `families: {numeric: SF Pro Condensed}` is silently ignored (`family: nil`), so the exported style is regular width. I had to hand-write a condensed modifier next to the generated file.
- `kinetic export --stack swiftui`: `headline` maps to `relativeTo: .body` instead of `.headline` (fine for size, but semantic mismatch).
- **`kinetic states code` false positive weighs on the verdict.** It flags `HomeView.swift` with F06 error (F/major) + loading (D/minor) because the handling lives in components (`FreshnessNotice` `.failed` + Try again, `MinutesPlaceholder`, `MinutesPhase.loading`). The finding is labelled `inferred`, yet `kinetic score` counts it as if observed: integrity drops to 90 and state_coverage to 67 (< 70 gate), so the verdict stays ITERATE even though KDL states are 10/10 and every state is rendered. Either follow references into the files the screen imports, or exclude `inferred` findings from gates. The only way to "fix" it is keyword stuffing (`onRetry` does not even match `\bretry\b`), which is exactly the wrong incentive.
- **`kinetic scan` is blind to its own exporter's color initializer.** Hand-written `Color(kLight: 0x121417, kDark: 0x121417)` literals (and fixture hexes) report `colors: []`. Token arithmetic such as `KSpace.xs / 2`, `KSpace.s - 2` (off-grid 2pt/6pt) and literal `.frame(width: 134, height: 54)` / `@ScaledMetric … = 28` were also not reported. A clean scan here meant less than it seemed; I found and snapped the off-grid arithmetic by grep.
- **`kinetic score` can never reach `ship` for a still-render pipeline**: motion is always unjudged without a recording, and the gate requires all 10 dimensions. The harness the eval uses can only produce PNGs. There should be an explicit "motion unjudgeable → verdict capped at iterate, report as such" rule, or a code-based motion review path.
- **Intermittent `(eval):1: no such file or directory` running `bin/kinetic`** from zsh when invoked as `cd X && K="…"; "$K" …` (exit 127) even though the file exists; the same call through `bash -c` always worked. Possibly the harness shell, but worth a note in TOOLS.md ("call through bash").

## Harness / stack knowledge gaps (SwiftUI)
- **macOS `ImageRenderer` draws nothing inside `ScrollView` / `List` and no navigation bar.** stacks/swiftui.md recommends `NavigationStack` + large titles + `List(.insetGrouped)` for native fidelity, but with the provided render harness all of those come out blank. My first render was an empty white page. I had to add a macOS-only top-aligned container and mirror the iOS large-title header in content. The SwiftUI knowledge should warn about this and give the pattern.
- `ProgressView()` renders as an orange square in the macOS harness; `.tint` is ignored. Worth a note.
- Formatting pitfalls not covered: `Date.formatted()` / `Measurement.formatted()` use `Locale.current`, not the SwiftUI `\.locale` environment, so a gallery set to `en_GB` still showed "9:59 AM" and feet; and `en_GB` road distances are yards. copy.md says "use the locale's formatter" but not how to make it follow the environment locale in SwiftUI.

## Bad or weak suggestions
- The KDL `families` budget treats SF Pro Condensed as a second family (it is a width of the same family); I described it as `numeric:` and the validator accepted it, but the export dropped it (see above). The typography knowledge never mentions font *width* axes (SF Pro Condensed/Compressed/Expanded), which are one of the best native tools for numeral-heavy UIs.
- `directions.md` "Swiss Instrument" suggests a red signal accent for transit; for transit that collides with the universal red of closures/danger. A note on status-color collisions per sector would help.
- The critique module's "default + largest text" requirement plus the harness' limitation pushed me to add a `home-accessibility-layout` gallery entry that only forces the layout branch (text is not scaled). That is useful but could be mistaken for a real AX5 render; the plugin should prescribe how to label such partial evidence.

## Top 5 (priority order)
1. `kinetic score` gates on `inferred` `states code` findings (false F06 on a screen whose states live in components) — kept the verdict at ITERATE despite 10/10 designed and rendered states.
2. SwiftUI knowledge recommends NavigationStack/List/large titles but the render harness (macOS ImageRenderer) draws blank ScrollView/List/nav bars — no warning or workaround in the plugin.
3. Validator counts every motion spec against the *signature-moment* budget (D18), contradicting "spec every animation in KDL".
4. Scanner misses literal colors written with the exporter's own `Color(kLight:kDark:)` initializer, token arithmetic off the grid, and literal frames — a "clean" scan overstated cleanliness.
5. No transit/timetable sector playbook and no rule for data colors (line colors) vs the accent budget; KDL/export can't express font width (SF Pro Condensed silently dropped).
