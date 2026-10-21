# Engine tool contracts

`bin/kinetic <command>` — Python 3.9+, standard library only. Every command
takes `--json`. Exit codes: `0` ok · `1` F findings (blocked) · `2` usage or input error.
Each contract states boundary, input, result, evidence, effects, nearest
alternative and how it is verified (tests/).

| Command | Shape | Boundary — what it answers | Evidence | Effects |
|---|---|---|---|---|
| `validate <kdl>` | validate | Is this decision record complete and coherent? (sections per mode, thesis genericity, divergence, type ramp, contrast, grid, radii, motion, states, variants, targets, references, slop phrases, TODOs) | derived | read-only |
| `palette <seed>` | compute | Light + dark role sets from one seed, contrast-checked (WCAG 2 + APCA), plus an 11-step OKLCH ramp | derived | read-only |
| `contrast <fg> <bg>` | compute | WCAG ratio and APCA Lc with pass flags | derived | read-only |
| `scan <paths>` | inspect | Design facts in UI source (colors, sizes, spacing, radii, durations, curves, springs, icons, effects) and the catalog rules they trigger, per file:line | observed / derived / inferred per finding | read-only |
| `dna <paths>` | derive | The de-facto design system in code, coherence per dimension, a consolidated proposal (`--kdl` for an editable draft) | derived | read-only |
| `states matrix <kdl>` | derive | Screens × states and components × variants coverage | derived | read-only |
| `states code <paths>` | inspect | Data screens whose code lacks loading/error/empty handling | inferred | read-only |
| `states template <id>` | generate | KDL skeleton for a screen with every state | — | prints only |
| `score [--kdl] [--code] [--judged]` | workflow | Taste report: measured sub-scores (formulas printed), validated critic scores, gated verdict, next actions | derived + judged | read-only |
| `export <kdl> --stack S [--out]` | generate | Tokens for flutter · swiftui · compose · react-native · css, physics converted exactly | — | writes `--out` only; refuses to overwrite a non-generated file without `--force` |
| `svg lint <paths>` | inspect | Icon craft rules SVG01–SVG13 per file and across the set | observed / derived | read-only; refuses DOCTYPE/ENTITY |
| `svg fix <files> [--write]` | generate | Normalized SVG (no ids/classes/styles, currentColor, 2-decimal precision) | — | `--write` overwrites the given files |
| `init [path]` | generate | `.kinetic/config.json` + mode skeleton `design.kdl` | — | writes only inside `.kinetic/`; keeps existing files unless `--force` |
| `spring <response> <damping>` | compute | Exact spring parameters for SwiftUI, Flutter, Compose, Reanimated and CSS `linear()` | derived | read-only |

## Coverage and limits (stated in every result)
- `scan` is lexical: values computed at runtime, behind helper functions or in
  binary assets are not seen; unscanned or oversized files are listed as
  `unknown`. Generated files (`*.g.dart`, `*.freezed.dart`), tests and build
  folders are skipped and counted.
- `inferred` findings require a look at the code context or the render before
  being reported as facts.
- `score` never outputs a single taste number: it shows measured and judged
  blocks side by side and the gates that produced the verdict.
- Exports are compiled in `tests/` when toolchains are present: SwiftUI (iOS +
  macOS, `swiftc`), TypeScript (`tsc`), Flutter (`flutter analyze`, with
  `KINETIC_SLOW=1`). Compose is compiled with `kotlinc` against signature stubs
  of the Compose APIs it uses (`tests/compose_stubs/`) — this checks syntax and
  typing, not the real artifacts; a Gradle build in the app is the final proof.

## Nearest alternatives
- Visual regression / pixel diff: not provided; use the platform's snapshot
  tests (golden tests, swift-snapshot-testing, Paparazzi). Kinetic judges
  design quality, not pixel drift.
- Full AST linters (dart analyze, SwiftLint, detekt, ESLint): complementary;
  they check code correctness, Kinetic checks design decisions.

## Invocation notes
- The plugin path often contains spaces: always quote it (`"$KROOT/bin/kinetic" scan lib`).
  In zsh, prefer an alias or `bash "$KROOT/bin/kinetic" …` over `K=…; "$K"` constructs inside `eval`.

## Configuration (`.kinetic/config.json`)
```json
{"stack": "flutter", "platforms": ["ios", "android"], "grid": 4,
 "theme_paths": ["lib/theme/"], "hook": true, "hook_tiers": ["F", "D"], "hook_min_severity": "major"}
```
`theme_paths` (regex) marks files where literal colors are definitions rather
than hard-coded values. `hook: false` silences the edit hook for the project.
