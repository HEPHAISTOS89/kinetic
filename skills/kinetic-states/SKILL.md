---
name: kinetic-states
description: "Kinetic's state and environment intelligence for mobile UI: design every screen in every state (content, loading, empty, error, offline, permission, overflow, first-run) and every interactive component in every variant (pressed, disabled, loading, selected, focused, error), considering each element's environment (surface, neighbours, thumb zone, keyboard, text size, platform). Use whenever a mobile screen or flow is designed, redesigned or audited."
---

# Design every state, and the world around each element

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

Read `knowledge/states.md` (taxonomy, rules, edge cases). This module turns
it into decisions in KDL `screens[]` and verifies coverage.

## Procedure
1. **List screens and their data**: for each screen, does it load data
   (`network: true`)? What can be empty? What can fail? Which permissions?
2. **Matrix first, visuals second**: write `states:` for every screen —
   `content loading empty error` (+ `offline` when networked) and any of
   `partial permission first-run overflow stale` that apply. Describe each in
   one line of *what the user sees and can do*. `n/a: reason` only with a real reason.
   Start from `kinetic states template <id>` for new screens.
3. **Variants for interactive components**: every `button icon-button link
   field toggle chip tab row` declares `variants` (at least `pressed`,
   `disabled`; `loading` for async; `selected` for choices; `error` for fields)
   and `target` ≥ 44.
4. **Environment** (`env`) for important components: what it sits `on`,
   what it's `near`, its `zone` (thumb, under keyboard, under the notch), what
   can change around it (longer text, XXL, dark, RTL, keyboard, banners).
   Every `fg`/`bg` pair is contrast-checked by the validator.
5. **Edge cases on purpose**: longest real string, +40% translation, 0 / 1 /
   500 items, missing image, negative or huge numbers, XXL text on the
   smallest phone, offline mid-action, double tap, process death.
6. **Copy per state** (knowledge/copy.md): errors = cause + recovery; empty =
   why + first step; loading = expectation when long.
7. **Verify**:
   - `kinetic states matrix .kinetic/design.kdl` → every required state covered.
   - On code: `kinetic states code <paths>` → data screens missing handling (inferred: open the file to confirm).
   - `kinetic validate` → F06/K11/K12/F05 clean.

## Decisions that separate senior from junior
- Loading keeps the previous content whenever possible; skeletons only when the
  layout is known and the wait is > 300ms; never a blank screen with a spinner as default.
- Optimistic UI only when the action is reversible and failure is rare — and
  the failure state is designed (rollback + message).
- Disabled controls explain why nearby, or stay enabled and validate on tap.
- Empty first-use screens sell the next step, never show fake zeros or empty chart axes.
- Errors keep the user's input and offer one clear recovery.
- Offline: cached content stays readable; queued actions are visibly pending.

## Output
Updated `screens[]` in KDL, the matrix summary (e.g. "14/14 states, 9/9
components with variants"), and the list of edge cases that changed the design.
