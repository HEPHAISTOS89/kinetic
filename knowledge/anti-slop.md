# Mobile anti-slop catalog

Slop is what a model produces when it has no specific target: the statistical
average of every app it has seen. It is recognisable because it is
*interchangeable* — the screen could belong to any product. This catalog names
the patterns, gives each a stable ID (shared with `kinetic scan`, `kinetic
validate`, the critic and the skills) and, more importantly, the fix.

**A pattern is a trigger only when it causes the damage described.** A card is
not slop; a screen where every different idea wears the same card is.

## Tiers
- **F — refuse.** Integrity, function or access failures. Never ship. No aesthetic exception.
- **D — reject by default.** Generic or damaging patterns. Ship only with a
  product-specific reason stated in KDL (`because`) *and* visible in the render.
  "Premium", "modern", "clean", "the user didn't forbid it" are not reasons.
- **C — conditional.** Not slop in itself. Judge against thesis and expression level.

Scanner column: **auto** = `kinetic scan` detects a signal; **judge** = only a
render/critic can decide; **kdl** = `kinetic validate` checks the decision record.

## F — refuse

| ID | Pattern | Signal | Fix | Check |
|---|---|---|---|---|
| F01 | Fabricated proof: invented ratings, user counts, testimonials, metrics shown as real | literal "4.9★", "10k+ users", fake chart data in production paths | Use real data or an explicit, labelled placeholder state | auto+judge |
| F02 | Inert control: button/link/row that promises but does nothing | `onPressed: () {}`, `action: {}`, `onClick={() => {}}`, `href="#"` | Wire the action, or remove the control | auto |
| F03 | Unreadable text: contrast < 4.5:1 (body) / 3:1 (≥ 24pt or 19pt bold); text on photo without scrim | color pairs in KDL; text over media | Change the role color, add scrim/plate, or move text off media | kdl+judge |
| F04 | Clipping or overlap at small width, long locale, or largest text size | fixed heights around text; `maxLines: 1` on titles; overflow in screenshot at SE / XXL | Let containers grow; wrap; restructure for width, not shrink | auto+judge |
| F05 | Touch target under 44pt (iOS) / 48dp (Android) on a real control | icon buttons with 24–32 frame | Expand the hit area, keep the glyph size | auto+kdl |
| F06 | Missing state on a data screen (loading, empty, error, offline) or success shown before confirmation | no error branch; optimistic "Saved!" before the write resolves | Design every state; acknowledge only after the outcome | kdl+judge |
| F07 | Inaccessible meaning: icon-only control without label; status by color alone; focus order ≠ visual order | `IconButton` without `tooltip`/`Semantics`; `Image(systemName:)` button without `accessibilityLabel` | Label it; pair color with shape/text; fix order | auto |
| F08 | Motion without a reduce-motion path, or information only conveyed by animation | animations present, no `disableAnimations` / `accessibilityReduceMotion` / `isReduceMotionEnabled` | Branch to crossfade/instant; keep state feedback | auto |
| F09 | Safe areas, home indicator, notch or keyboard ignored | content under status bar; field hidden by keyboard; no `SafeArea`/`safeAreaInset` | Respect insets; scroll the focused field into view | auto+judge |
| F10 | User text size locked | `TextScaler.noScaling`, `textScaleFactor: 1`, `allowFontScaling={false}`, `.dynamicTypeSize(.large)` clamp, `maxFontSizeMultiplier={1}` | Support scaling; re-layout at XXL instead of locking | auto |

## D — reject by default

| ID | Pattern | Signal | Fix | Check |
|---|---|---|---|---|
| D01 | **The AI gradient** — violet/indigo/pink gradient headers, buttons or backgrounds with no product meaning | `LinearGradient` with hues 250–320° | Solid surface + one accent; if a gradient, derive it from meaning (time, data, brand) and keep it low-chroma | auto |
| D02 | **Greeting as concept** — "Good morning, Sam 👋" heading the home screen | greeting strings | Lead with the thing the user came for (today's value, next action) | auto |
| D03 | **Card soup** — every block in the same rounded, shadowed white card, regardless of its job | many identical card containers per screen | Use cards only for equivalent, separable records; group the rest with space, rules and type | auto+judge |
| D04 | **Dashboard costume** — stat tiles, rings, sparklines and "insights" that support no decision | 3+ metric tiles; progress rings | Show the one number that matters with its meaning; detail on demand | judge |
| D05 | **Glass everywhere** — blur/frosted panels as a premium shortcut | `BackdropFilter`, `.ultraThinMaterial` on content cards | Native materials only on bars/sheets/overlays over moving content | auto |
| D06 | **Icon chaos** — emoji as icons; mixed families, weights, fills; decorative icons on every row | emoji in `Text`; >1 icon family; filled+outlined mixed | One family, one weight, fill only for selection; drop icons that don't aid scanning | auto |
| D07 | **Generic illustration** — 3D blobs, stock characters, abstract waves as content | asset names `blob`, `wave`, `illustration_*` | Typography, data and real content carry the screen; images return in v2 with intent | auto+judge |
| D08 | **Navigation by habit** — 5 equal tabs where 2–3 suffice; hamburger menu on iOS; tabs for actions | tab count; drawer on iOS | Tabs for parallel top-level areas only; actions live in context | auto+judge |
| D09 | **FAB reflex** — floating action button on iOS, or when creation isn't the primary action | `FloatingActionButton` on iOS target | Toolbar/nav-bar action on iOS; FAB only for Android creation-first screens | auto |
| D10 | **Interruption habit** — toasts for every action; dialogs for non-destructive choices | many `SnackBar`/`showDialog`/`.alert` calls | Inline confirmation, undo, state change in place | auto+judge |
| D11 | **Centered everything** — centered paragraphs, lists, forms | `textAlign: center` on multi-line text | Align to a reading edge; center only single-focus moments | auto |
| D12 | **Type ramp chaos** — > 8 sizes, sizes outside the ramp, weights as decoration | distinct font sizes in code | A 5–8 step ramp; hierarchy by size+weight+color together | auto+kdl |
| D13 | **Color chaos** — more accents than the expression budget; > 6 ad-hoc neutrals | distinct literal colors | Role-based palette from one ramp; neutrals tinted from the seed | auto+kdl |
| D14 | **"Premium" by reflex** — black + gold, beige-espresso-brass, or neon on black whenever "premium" is asked | hue/chroma of accents vs thesis | Premium is precision, restraint and fit: derive the palette from the product, not the word | kdl+judge |
| D15 | **Radius chaos** — > 4 radii; nested corners that don't follow `inner = outer − padding` | distinct radii | 3–4 radii; concentric nesting; continuous corners on iOS | auto+kdl |
| D16 | **Shadow everything** — heavy shadows on flat UI; border + shadow + fill on every element | many `BoxShadow`/`.shadow` | Pick one elevation strategy (tonal, shadow or border) per system | auto |
| D17 | **Magic spacing** — off-grid values (13, 17, 23, 27) and per-widget padding | spacing values not on the 4-pt grid | Spacing scale tokens only | auto+kdl |
| D18 | **Entrance confetti** — fade-up on every element; staggered list entrances everywhere | many entrance animations | Animate what changed, where it changed; content that was there stays still | auto+judge |
| D19 | **Wrong physics** — bounce/elastic on utility UI; linear easing on UI motion; durations > 500ms on frequent actions | `Curves.bounceOut/elasticOut`, `.bouncy`, damping < 0.6, `Curves.linear` | Critically damped springs for UI, overshoot only for direct manipulation and expressive levels ≥ 4 | auto |
| D20 | **Loading theatre** — skeletons for sub-300ms loads; a centered spinner for everything | `Shimmer`, `CircularProgressIndicator` centered | Keep previous content, show progress in place, skeleton only when layout is known and wait > 300ms | auto+judge |
| D21 | **Carousel onboarding** — 3 swipe screens of vague benefits before any value | `PageView` onboarding with 3 pages | Deliver value first; ask permissions in context; one screen if any | auto+judge |
| D22 | **Copy slop** — "Unlock your potential", "Seamless", "Elevate", "Supercharge", exclamation marks, "Oops!" | phrase list | Name the thing and the outcome in the user's words; see copy.md | auto |
| D23 | **Web on a phone** — hover-dependent UI, tiny text, desktop tables, multi-column forms | `onHover`, tables, 12px body | Recompose for thumb and glance: lists, sheets, progressive disclosure | auto+judge |
| D24 | **Platform mismatch** — Material ripple/FAB/top app bar on iOS, iOS chevrons/back swipe assumptions on Android, without a deliberate cross-platform brand | platform widgets vs target | Adapt navigation, controls and feedback per platform; share identity, not chrome | auto+judge |
| D25 | **Badge confetti** — pills, "NEW", "PRO", chips used as ornament | many `Chip`/badge components | Badges only for state the user must notice | auto |
| D26 | **Gradient text, neon glow, outer glows** | `ShaderMask` on text, glow shadows | Weight, size and color carry emphasis | auto |
| D27 | **Gamified decoration** — streaks, rings, confetti, trophies that don't serve the thesis | streak/confetti code | Feedback proportional to the act; celebrate only real milestones | auto+judge |
| D28 | **Layout patches** — `FittedBox`, `minimumScaleFactor`, `adjustsFontSizeToFitWidth`, ellipsis on critical text | APIs present | Reflow the layout; give critical text the space it needs | auto |
| D29 | **Mockup sizes in code** — `width: 375`, `height: 812`, fixed screen-sized frames | literal device dimensions | Constraints and flexible layout; safe-area-aware | auto |
| D30 | **Default theme untouched** — stock Material purple / iOS default blue with no decision | `Colors.deepPurple`, `seedColor: Colors.purple`, unmodified template | Make the palette a decision from the thesis | auto |

## C — conditional (judge against thesis and level)

| ID | Choice | When it is right |
|---|---|---|
| C01 | System font vs custom font | System fonts are often *the* premium choice on iOS. Custom when the brand or thesis needs a voice the system lacks. |
| C02 | Pure black dark mode | OLED-first media apps, camera, night use. Otherwise near-black with tonal surfaces. |
| C03 | Cards | Equivalent, separable records (a list of trips, products, accounts). |
| C04 | Gradients | When they carry meaning: time of day, data intensity, brand light. Low chroma, few stops. |
| C05 | Blur/materials | Native bars, sheets, menus over scrolling content. |
| C06 | Overshoot springs | Direct manipulation, playful brands, expression ≥ 4. |
| C07 | Illustration | Empty states and onboarding when on-brand and purposeful (v2). |
| C08 | FAB | Android, creation-first screens. |
| C09 | Centered layout | Single-focus moments: a hero numeral, an auth screen, a confirmation. |
| C10 | Stock Material / Cupertino components | Deliberately chosen, themed and tuned; native fidelity is a virtue. |
| C11 | Dense UI | Expert, frequent use (trading, ops, pro tools) — density is respect there. |
| C12 | Monospace | Code, IDs, aligned figures; not as fake technicality. |

## The deeper tests (judge)
Run these before shipping anything substantial:
1. **Swap test** — replace the logo and name with a competitor's. Does anything break? If not, it's interchangeable.
2. **Squint test** — blur the screen. Is there exactly one primary thing, then a clear second?
3. **Silence test** — remove every icon, shadow and color but one accent. Does the hierarchy survive? If it collapses, decoration was doing the work typography should do.
4. **Thumb test** — one hand, walking. Can the primary action be reached and hit?
5. **Night test** — dark mode at 20% brightness. Anything glaring, anything vanishing?
6. **XXL test** — largest accessibility text size. Does it reflow, or clip?
7. **Thesis test** — point at each element and name the line of the thesis it serves. Elements that serve nothing go.
