---
name: kinetic-motion
description: "Kinetic's motion and haptics design for mobile apps: decide what should move and why, give motion a personality, specify springs/durations/choreography per animation, shared-element continuity, gesture-driven interruptible physics, reduce-motion paths and haptic pairing, then implement in SwiftUI, Flutter, Compose or React Native. Use for animations, transitions, micro-interactions, gestures, haptics, or when motion feels cheap, bouncy or decorative."
---

# Motion is physics with a purpose

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

Read `knowledge/motion.md`. Implementation details per stack: `knowledge/stacks/<stack>.md`.

## Procedure
1. **Inventory the changes, not the elements.** List every state change on
   the screen/flow (open, close, select, add, delete, load, fail, navigate).
   Motion belongs to changes; elements that don't change stay still.
2. **Gate each change** with the five questions (explain a change · acknowledge
   an action · follow the hand · direct attention · signature). No yes → no motion.
3. **Personality** from the thesis (`system.motion.personality`) and 2–4
   springs + durations in KDL. One personality per product.
4. **Spec every animation in KDL** (`screens[].motion`) with its `kind`:
   `feedback` (press, toggle, symbol swap), `transition` (state/screen change) or
   `signature` (the spine made visible) or `ambient` (a slow loop that says
   "live": a breathing dot on an ongoing session or a live count — one per screen,
   ≥ 1.2 s per half-cycle, name its duration `ambient-…`/`pulse-…`, still under
   reduce motion). Only `signature` counts against the expression budget. Then: `trigger`, `change`
   (what moves, from where to where, amplitude), `spring` or `duration`,
   `haptic` if any, `reduce`, `interruptible`. The validator rejects incomplete specs.
5. **Choreograph**: the meaningful element leads; others follow by 20–40ms or
   fade; shared elements carry identity across screens; exits ≈ 75% of entrance time.
6. **Gestures**: animation tracks the finger 1:1 during the drag; on release
   hand the gesture velocity to a spring (ζ 0.75–0.9); define thresholds and
   the haptic at the threshold; every gesture has a visible alternative.
7. **Reduce motion**: crossfade ≈ 150ms instead of spatial movement; keep state
   feedback; test with the setting on.
8. **Implement with the exported tokens** (`KMotion`, `Animation.k…`, spring
   configs from `kinetic export` / `kinetic spring`). Prefer platform
   primitives (implicit animations, matchedGeometryEffect/Hero/SharedTransition,
   sheets, navigation transitions) over custom timelines.
9. **Verify on device or simulator**: trigger, interrupt mid-way, reverse,
   repeat fast, reduce-motion on, low-power mode; check 60/120fps; screen-record
   when the critic needs to judge motion (screenshots cannot).

## Defaults that are almost always right
- Press: scale 0.97 + opacity 0.85, spring 0.25/1.0, release spring 0.35/0.9.
- Sheet/card expand: spring 0.4/0.9; content inside fades in after 60–80ms.
- List insertion: height animates (spring 0.35/1.0), item fades + 8pt rise; deletion collapses faster.
- Toggle / selection: 150–200ms + `selection` haptic.
- Success: inline check draws in 250ms + `success` haptic; no confetti (D27) unless the milestone is real and the level ≥ 4.

## Anti-patterns (reject)
Fade-up on every element on every visit (D18) · bounce on utility UI (D19) ·
linear easing for movement (D19) · durations > 500ms on frequent actions ·
animations that block input · infinite decorative loops · motion without
reduce-motion (F08) · haptics without a visible change.
