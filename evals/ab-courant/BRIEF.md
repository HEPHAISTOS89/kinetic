# Brief — "Courant"

Courant is a public-transport departures app for one city (buses, trams, metro).
People open it while walking toward a stop, phone in one hand, often in a hurry,
sometimes in bad network conditions underground. They want to know, in a glance,
when the next departures leave from the stops near them or from their saved stops,
and whether there is a disruption that affects them.

Design and implement the **home screen** of the iOS app in SwiftUI (iOS 17+).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- nearby stops (from location) with next departures per line and direction, in minutes;
- saved stops (user-chosen);
- service disruptions per line (severity: info / delay / closed);
- last update time; network can fail; location permission can be denied.

## Deliverables (all in your working directory)
- Swift source files for the home screen (and any tokens/components you create).
- A `Gallery` type that lists every state you designed, so it can be rendered:
  `enum Gallery { @MainActor static var screens: [(String, AnyView)] { [...] } }`
  Use short kebab-case names (e.g. "home", "home-empty"...). Include as many states as you consider necessary.
- The code must compile **for iOS 17 and for macOS 14** (the render harness runs on macOS):
  guard any UIKit-only API with `#if canImport(UIKit)`.
- Render and look at your own result with the harness, as many times as you like:
  `xcrun swiftc -parse-as-library -target arm64-apple-macos14.0 <HARNESS>/Render.swift *.swift -o render && ./render shots`
  (renders each gallery entry at 393×852pt, light and dark, into ./shots). Also check it type-checks for iOS:
  `xcrun --sdk iphonesimulator swiftc -typecheck -target arm64-apple-ios17.0-simulator *.swift` (exclude the harness).
- A short NOTES.md: what you designed and why (≤ 25 lines).
