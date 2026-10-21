---
description: Design-to-code: implement a Kinetic design (KDL, mockup or description) in Flutter, SwiftUI, Compose or React Native with exported tokens and every state
argument-hint: "<KDL path, mockup, or screen description>"
---

Use the `kinetic` skill in **build** mode for: $ARGUMENTS

Tokens first (kinetic export), components with all variants, then screens with every state branch and motion spec; verify with the stack analyzer and kinetic scan.

Follow the router's pipeline for this mode and depth, write decisions to `.kinetic/design.kdl` (run `kinetic init --mode design-to-code` first if the project has no `.kinetic/`), verify with the engine, and report per docs/PROTOCOL.md §7.
