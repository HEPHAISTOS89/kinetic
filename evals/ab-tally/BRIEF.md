# Brief — "Tally"

Tally helps people who share a flat (2–5 flatmates) keep track of shared expenses —
groceries, rent, utilities, the cleaning person — and settle up fairly without
awkward conversations. People open it right after paying for something (in the
shop queue, phone in one hand) to log it in seconds, and once in a while to see
who owes whom and settle up. Money between friends is sensitive: the app must feel
fair, precise and calm, never like a debt collector.

Design and implement the **home screen** of the iOS app in SwiftUI (iOS 17+).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the flat's members (names, avatars or initials), the current user;
- recent expenses (who paid, amount, currency EUR, how it's split, date, category);
- each person's net balance and the simplest set of transfers to settle up;
- sync status: expenses added offline are queued; a sync can fail; two people can
  edit the same expense (conflict); the user can be in several flats.

## Deliverables (all in your working directory)
- Swift source files for the home screen (and any tokens/components you create).
- A `Gallery` type that lists every state you designed, so it can be rendered:
  `enum Gallery { @MainActor static var screens: [(String, AnyView)] { [...] } }`
  Use short kebab-case names. Include as many states as you consider necessary.
- The code must compile **for iOS 17 and for macOS 14** (the render harness runs on macOS):
  guard any UIKit-only API with `#if canImport(UIKit)`.
- Render and look at your own result with the harness, as many times as you like:
  `xcrun swiftc -parse-as-library -target arm64-apple-macos14.0 <HARNESS>/Render.swift *.swift -o render && ./render shots`
  (renders each gallery entry at 393×852pt, top-aligned and cropped, light and dark, into ./shots).
  Note: macOS rendering draws ScrollView/List/navigation bars blank and does not scale Dynamic Type;
  lay out gallery entries with plain stacks if you need them visible. Also check it type-checks for iOS:
  `xcrun --sdk iphonesimulator swiftc -typecheck -target arm64-apple-ios17.0-simulator *.swift` (exclude the harness).
- A short NOTES.md: what you designed and why (≤ 25 lines).
