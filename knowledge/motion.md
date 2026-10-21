# Motion and haptics for mobile

Motion on a phone is **physics and continuity**: things move as if they have
mass, follow the finger, can be interrupted, and tell you where something came
from and where it went. Slop motion is *decoration*: fade-up on everything,
bounce on everything, durations picked per widget.

## 1. Should it move at all? (ask in this order)
1. Does it **explain a change** (where did that come from, where did it go)?
2. Does it **acknowledge an action** (press, toggle, send)?
3. Does it **follow the user's hand** (drag, swipe, pinch)?
4. Does it **direct attention** to something that changed off-focus?
5. Is it **identity** (one signature moment allowed by the expression budget)?
If none: it doesn't move. Content that was already there stays still.

## 2. Personality first
Name it in KDL (`system.motion.personality`) so every animation can be checked:
| Personality | Springs | Feels |
|---|---|---|
| precise | response 0.25–0.3, damping 1.0 | instrument, finance, tools |
| native calm | response 0.35–0.45, damping 0.85–1.0 | most apps; iOS default feel |
| unhurried | response 0.5–0.6, damping 1.0 | sleep, meditation, reading |
| lively | response 0.3–0.4, damping 0.7–0.8 | social, consumer, expression 3–4 |
| playful | response 0.35–0.45, damping 0.55–0.7 | kids, games, expression 5 — only on direct manipulation |

## 3. Springs: the KDL model
A KDL spring is `{response, damping}`: **response** ≈ the period of the
oscillation in seconds (perceived speed), **damping** = damping ratio ζ
(1.0 = no overshoot, < 1 = overshoot). With unit mass:
`stiffness = (2π / response)²`, `damping coefficient = 4π·ζ / response`.

`kinetic spring 0.4 0.9` prints the exact parameters for SwiftUI, Flutter,
Compose, Reanimated and a CSS `linear()` curve with its settle time.

Rules:
- UI transitions (navigation, sheets, state changes): ζ 0.85–1.0.
- Direct manipulation release (drag-to-dismiss, card fling): ζ 0.7–0.9, carry the finger's velocity.
- Overshoot (ζ < 0.7) only for direct manipulation or expression ≥ 4 (D19).
- Springs are interruptible by nature: a new target retargets from the current
  position and velocity. Prefer springs over fixed-duration curves for anything the user can interrupt.

## 4. Durations (when not a spring)
| Kind | ms | Easing |
|---|---|---|
| Press feedback (scale/opacity) | 80–120 in, 150–200 out | ease-out |
| Small state change (toggle, check, color) | 150–200 | ease-out / spring 0.3 |
| Element enter/exit within a screen | 200–300 | ease-out in, ease-in out (exits faster) |
| Screen / sheet transitions | platform default (≈ 350–500) | platform spring |
| Ambient / narrative (onboarding, signature) | 400–800 | spring or custom |
| Loops (loading) | 800–1500 period | linear (rotation) or ease-in-out (pulse) |
Exits are faster than entrances (≈ 70–80%). Frequent actions get the shortest durations.

## 5. Choreography
- **One thing leads.** In a transition, the element with meaning (the tapped
  card) moves first or alone; others follow with 20–40ms offsets or simply fade.
- **Shared elements** carry identity across screens (Hero, matchedGeometryEffect,
  navigationTransition(.zoom), SharedTransitionLayout).
- **Stagger** only lists that are new to the user, ≤ 5 items, 20–30ms apart, total < 200ms. Never stagger on every visit (D18).
- **Direction means something**: push = deeper, pop = back, up = more detail/sheet, down = dismiss.
- **Amplitude is small**: entrances move 8–16pt, not 50. Scale 0.96–0.98 for press, not 0.8.
- Don't animate layout properties that cause relayout of the whole screen if a transform achieves it.

## 6. Reduce motion (F08 — mandatory)
Every animation declares its reduce-motion path (`reduce: crossfade | instant |
keep-feedback-only`):
- iOS: `@Environment(\.accessibilityReduceMotion)`; Flutter:
  `MediaQuery.disableAnimationsOf(context)`; Android: animator duration scale
  (see stacks/compose.md); RN: `useReducedMotion()` (Reanimated) /
  `AccessibilityInfo.isReduceMotionEnabled`; web: `prefers-reduced-motion`.
- Replace spatial movement (slides, zooms, parallax) with short crossfades
  (≈150ms). Keep state feedback (a toggle still changes; a checkmark still appears).
- Never convey information only through motion.

## 7. Haptics: touch has a voice
| Event | iOS | Android | KDL |
|---|---|---|---|
| Selection change (picker, segmented, toggle) | selection | CLOCK_TICK / SEGMENT_TICK | `selection` |
| Light confirmation (add, like) | impact light / soft | CONFIRM / CONTEXT_CLICK | `light` / `soft` |
| Commit (send, complete, purchase done) | success notification | CONFIRM | `success` |
| Snap / threshold crossed (drag reaches action) | impact medium/rigid | GESTURE_THRESHOLD_ACTIVATE | `rigid` |
| Warning / destructive confirm | warning | REJECT | `warning` |
| Failure | error | REJECT | `error` |
Rules: haptics pair with a visible change, never alone; one haptic per user
action; none on scroll or passive updates; respect system settings. Exact API
names per stack are in stacks/*.md.

## 8. Signature motion
The expression level sets how many signature moments the product gets
(KDL budget). A signature motion derives from the thesis spine (Lune: "the
light goes down" → the background tint follows the real clock). It happens
at a meaningful moment, once, and has a reduce-motion version.

## 9. Performance
- Animate transforms and opacity; avoid animating blur, shadows and layout on
  large surfaces per frame.
- 60fps minimum, 120Hz ProMotion on iPhone Pro — test on device, not only simulator.
- Clean up controllers/observers on dispose; pause offscreen animations.
- Lottie/Rive only when vector illustration motion is genuinely needed; never for a spinner.

## 10. Motion slop (map to the catalog)
| Slop | ID |
|---|---|
| Fade-up entrance on every element, every visit | D18 |
| Bounce/elastic on utility UI | D19 |
| Linear easing on UI movement | D19 |
| 900ms transitions on frequent actions | D19 |
| Infinite decorative loops, parallax, floating blobs | D18/D07 |
| Confetti for routine actions | D27 |
| No reduce-motion branch | F08 |
| Skeleton shimmer for 100ms loads | D20 |
