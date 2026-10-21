# Kinetic feedback log (candid)

Task: Tally home screen, mode `create`, depth D2, SwiftUI, rendered on macOS.

## Routing / reading
- Router §1 depth table says D2 runs "think → direct → states → system → motion → code → critique" (no craft),
  but the D2 minimum-reading row lists the craft skill and not motion/code. Small inconsistency; I read all of them.
- D2 says docs/KDL.md is D3-only reading, but writing `.kinetic/design.kdl` at D2 needs the syntax and the field list
  (`serves`, `thumb`, component kinds, `n/a:` form). In practice I had to read KDL.md and the Lune example anyway.
- `kinetic init` in an empty directory (a brief, no code yet) silently defaults to `stack: mixed, platforms: [ios, android]`.
  For a brief-driven create it should say "no stack detected — pass --stack" instead of guessing two platforms.

## Engine
- **KDL parser: an apostrophe inside a word opens a quoted string.** `need: see every member's net balance` inside an
  inline map produced `K00 syntax: unclosed bracket` at that line — the message points at brackets, not at the quote.
  Natural English (member's, didn't, flat's) is exactly what the KDL prose fields invite. Either treat `'` as a quote only
  at the start of a scalar, or say "unterminated quote (') — quote the value or use ’" in the error.
- **KDL parser: commas inside inline-map values silently split the entry** (`need: log it in seconds, one-handed, …`
  → "inline map entry without ':'"). The error is clear enough, but KDL.md shows prose inside `{…}` maps without warning
  that commas must be quoted. A one-line note in KDL.md §Syntax would save a few validate loops.
- `kinetic validate` returned OK with zero findings on the first syntactically valid pass. Good, but I can't tell
  whether it actually checked e.g. `system.color.data` foregrounds (KDL.md says each data color needs a passing text
  color) — no I-level line says "data colors: 7 checked". A coverage line per check family would build trust.
- `kinetic export --stack swiftui` is excellent: cross-platform (`#if canImport(UIKit) … AppKit`), so it compiled for
  the macOS render harness without edits. **But `system.color.data` is not exported at all** — the person tints and the
  bar color I declared in KDL had to be hand-written in a second Swift file. Export them as `Color.kData.sand` etc.
- `kinetic export --out .` writes relative to the engine's cwd, fine; it prints `wrote ./KineticTokens.swift`
  (relative) — an absolute path would avoid confusion when called from another directory.
- `kinetic scan` **F05 false positive**: `Image(...).frame(width: 36, height: 36).background(Circle()).frame(width: 44, height: 44)`
  — a 44pt hit area with a 36pt visual — was reported as "button frame 36×36 below 44pt" (F tier!). The scanner reads
  the first frame, not the outermost. I rewrote it as `.frame(44).background(Circle().padding(4))` to silence it, but an
  F-tier false positive is costly: it blocks the verdict. Consider taking the largest frame in the label chain.
- `kinetic scan` **D13 major counted my data colours as neutrals** (person avatar tints are low-chroma by design, so
  they look like greys). It went away only after I moved them into a file named `…DataColors.swift`, because the scanner
  keys data-ness on the *filename* regex `(line|route|category|chart|data|status|severity)colors`. That convention is
  undocumented (I found it by reading scan.py). Document it in stacks/swiftui.md or, better, read KDL `system.color.data`
  hexes and exempt those values wherever they appear.
- The scanner only reads the `kLight:` value of `Color(kLight:kDark:)`; dark literals are invisible to the neutral count.
- `kinetic states code .` reported `data_screens=0` for a folder containing `HomeScreen.swift` with loading/empty/error/offline
  branches — so the check silently checked nothing. It should say "HomeScreen.swift looked like a screen but had no
  network keyword; not evaluated" rather than a clean-looking result.
- `kinetic score` with a self-judged critique works as documented (caps at ITERATE / ship-pending, lists motion as unjudged).
  Nice that `self_judged` is honoured. It would help if `score` printed the `unjudged` reasons it accepted.
- The macOS render notes in stacks/swiftui.md ("ScrollView renders blank", "content taller than the frame is centred and
  compressed", fixedSize + top alignment) were accurate and saved real time. One thing missing: a `.frame(maxHeight: .infinity,
  alignment: .top)` wrapper around a `fixedSize` stack still reports the child's height as its *minimum*, so the whole
  device frame overflowed and got centred — you also need `minHeight: 0`. Worth one line in that section.
- knowledge files: the D2 reading list was right-sized. platform-ios.md + layout.md "glance screens spend the top on
  answers" directly shaped the compact header (no large title) — good guidance.

## Phase 2 (after the independent critic)
- The independent critic was the most valuable part of the loop. It caught things my self-critique scored 4
  (hierarchy, typography, layout craft) with file:line evidence: the even line's 2.4:1 bar ink, "owes" contradicting
  my own signature `because`, one sync fact said three times. Self-critique missed all three. Rubric note: the self pass
  should be forced to run the *thesis test* row by row against the KDL `never` list — that alone would have caught "owes".
- **`kinetic score --judged` doesn't notice a stale judgment.** After a full redesign of the judged elements it still
  reports the v1 critic scores (mean 3.44, ITERATE) with no warning. It could compare the render files listed in the
  critique (or their mtimes/hashes) with the current ones and print "judgment predates N changed renders: re-judge".
- `kinetic validate` now checks data colours (coverage `data_colors=7`). That's good, but:
  (a) it treats every data colour as a badge fill that needs a label colour, so a pure graphic (the axis line) was a
  **D/major F03** ("no readable label color") and the bar fill gets two K25 infos. There's no way to declare
  "graphic, no label" (e.g. `role: graphic`). I moved the axis to `$color.text-3`, which is fine but was
  forced by the tool rather than chosen.
  (b) The `{light, dark, on, on_dark}` schema is accepted but not documented in KDL.md, which only shows
  `{fill, on}` / bare hex. I found `on_dark` by reading validate.py.
- Adding a role (`action` / `on-action`, for a calmer dark CTA) exported cleanly as `Color.kAction` / `kOnAction`.
  Nice. The validator doesn't contrast-check custom roles, though (on-action/action, action/bg). I checked them by
  hand with `kinetic contrast`.
- `kinetic scan` D17 "spacing token arithmetic" fires on `KSpace.s + 2` inside a placeholder *height* (not spacing).
  It's reasonable as a minor, but the message could say which value it computed (10) so you can judge it quickly.
- SwiftUI stack file: worth adding the macOS-render recipe for navigation bars (ImageRenderer draws them blank).
  Render a stand-in bar in still mode and keep `.toolbar` for the app. Also note that `ToolbarItemPlacement.topBarLeading`
  and `.navigationBarTitleDisplayMode` need `#if canImport(UIKit)` to build for macOS.
