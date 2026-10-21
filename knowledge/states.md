# States and environments

A screenshot shows one state. A product lives in all of them. Senior
designers are recognisable by what they design *without being asked*: the
first-run empty screen, the failed payment, the 40-character German label,
the user at 200% text size, the subway with no signal.

## 1. The screen state taxonomy
| State | Question to answer | Design rule |
|---|---|---|
| **content** | the nominal case with *real* data | design with realistic lengths and volumes, not lorem ipsum |
| **loading** | what does the user see while waiting, and for how long? | < 300ms: show nothing new (keep previous content); 0.3–2s: inline progress or skeleton *if layout is known*; > 2s: progress with expectation ("Fetching 3 accounts…"); never a blank screen with a centered spinner as the default |
| **empty — first use** | why is it empty and what's the first step? | explain the value, one primary action; no fake data |
| **empty — no results** | what was searched, how to widen it? | echo the query, suggest an alternative, offer to clear filters |
| **empty — cleared** | did the user finish? | acknowledge (inbox zero) proportionally |
| **error — recoverable** | what happened, what can I do? | plain cause + one recovery action (retry, edit, reconnect); keep user input. When the error concerns one object (an expense that didn't sync, a message that failed), **show that object** — pinned or highlighted with its action — rather than a banner that describes it while the object is scrolled away |
| **error — blocking** | what is unavailable and when will it be back? | say what still works; never a dead end without a way back |
| **offline** | what still works, when does it sync? | cached content readable; actions queued and shown as pending; banner, not modal |
| **partial** | some data loaded, some failed | show what you have, mark the gap |
| **permission** | denied camera/location/notifications/health | explain value, offer the settings path; app still works where it can |
| **first-run** | no history, no preferences | progressive: ask in context, not upfront |
| **overflow** | longest strings, biggest numbers, largest text, smallest screen | wrap and reflow; never clip (F04) |
| **stale** | data is old | change the *data's* appearance, not only a pill: dim or mark values ("~", "sched."), recompute time-relative values from the timestamp, timestamp + pull to refresh. A stale number at full weight is a lie of emphasis |

KDL requires `content loading empty error` (+ `offline` when `network: true`)
for every screen; other states as relevant. `n/a: reason` is allowed only with a reason.

## 2. Component variants (interactive elements)
| Variant | Must show | Notes |
|---|---|---|
| default | its affordance | buttons look pressable, rows look tappable |
| pressed | immediate feedback (≤ 100ms) | scale 0.97 / opacity 0.7 / platform highlight |
| disabled | why it's unavailable (nearby text) | 38–50% opacity *and* not focusable; prefer explaining over disabling |
| loading | progress in place | keep width stable; block double submit |
| selected | selection with more than color | fill, weight, checkmark |
| focused | visible focus ring (keyboard, switch control) | ≥ 3:1 contrast |
| error | what is wrong and how to fix it, next to the field | never only a red border |
| success | proportional confirmation | inline check, haptic `success`; toasts rarely (D10) |

## 3. The environment of each element
"Think about the environment, not just the page": for every important
component, write its `env` in KDL and check it.
- **What it sits on** (`on`): bg, surface, accent, media/photo → determines contrast pair and elevation.
- **What it sits next to** (`near`): neighbouring elements compete or support; spacing and weight must say which.
- **Where it sits** (thumb zone, under the keyboard, under the notch, inside a scroll).
- **What can change around it**: content length, dynamic type, dark mode, RTL, the keyboard appearing, a banner pushing it down.
- **What it becomes on other platforms**: iOS vs Android variants (switch, date picker, back affordance).
- **What happens before and after**: the state it comes from and the one it leads to (journey).

Example:
```yaml
- id: pay-button
  kind: button
  fg: $color.on-accent
  bg: $color.accent
  target: 52
  variants: [default, pressed, disabled, loading]
  env: {on: $color.surface, near: [total, legal-note], zone: bottom thumb, keyboard: stays above, density: low}
```

## 3b. Direction-aware actions
The same control must not serve opposite situations. If the user owes, the
action is to pay ("Pay Priya", prominent); if they are owed, it is to record
("Record payment", quiet; never "Remind" in social money). Same for
following/followed, sent/received, late/early: the state decides the verb and
the weight.

## 3c. High-stakes moments: precision over coverage
Coverage wins "anticipation"; the moment that frightens the user decides trust.
In round 4 the more complete design lost these points to the less complete one:
- **An alert takes over the screen's meaning.** When an alert shows (fever,
  failed payment, delay), every other block re-answers in relation to it: the
  hero says how the child is *now* and who is with her, the pick-up row becomes
  "Venir plus tôt", the routine fact ("woke up at 13:55") steps down. Two equal
  masses (alert + unchanged hero) fail the squint test.
- **An alert is an event, not a rule.** Name who, what, when, and the one action
  with its means: "Inès a mesuré 38,4 °C à 14 h 05 · appel manqué à 14 h 07" +
  "Appeler la crèche · 01 42 …". The rule ("above 38 °C the team must talk to
  you") is secondary text at most.
- **Unknown is not "didn't happen".** During a logging lag or offline, a
  missing entry reads "pas encore notée" / "not logged yet", never "Pas encore"
  or "0", which state a fact the app doesn't have.
- **A switcher shows each item's live state**, not its category: "Léa · dort
  depuis 13 h 05 | Noé · au jardin", not two identical "À la crèche".
- **Every offered action is valid for the object's state** (no "Flash" on a
  boulder with logged attempts, no "Pay" when settled): check the domain logic
  per state, not only the visuals.

## 4. Edge cases to design on purpose
- **Text**: the longest name in the dataset, German/French (+30–40% length), Arabic/Hebrew (RTL mirroring), emoji in user names, 1-character names.
- **Numbers**: 0, 1 (singular), 1,000,000+, negative, decimals, currencies with different symbol positions, missing values (show "—", not 0).
- **Media**: missing image, portrait vs landscape, very dark/light photos under text.
- **Time**: just now, yesterday, timezones, 24h vs 12h, very old items.
- **Lists**: 0, 1, 2, 500 items; pagination end; pull-to-refresh while loading.
- **System**: dark mode, increased contrast, bold text, reduce motion, reduce transparency, 200% text, VoiceOver/TalkBack order, small phone (SE), large phone, keyboard open, split view/foldable.
- **Interruption**: phone call, app backgrounded mid-flow, process death (state restoration), double tap on submit.

## 4b. Fixtures that add up
Gallery and preview data are evidence: a precise product is judged on its
numbers. Derive totals from the fixture items (balances from expenses, counts
from lists) instead of hard-coding them, keep cross-screen facts consistent
(a flag in one state must exist in the others), and include long names, large
amounts (−€1,240.00) and a second locale (de_DE "38,40 €").

## 5. Copy per state
See copy.md. Errors name the cause and the recovery ("Couldn't send — no
connection. We'll retry when you're back online."), never "Oops!" or an error code alone.

## 6. Tools
```
kinetic states matrix .kinetic/design.kdl   # screens × states, components × variants
kinetic states code lib/                    # data screens whose code lacks loading/error/empty handling (inferred)
kinetic states template checkout            # KDL skeleton for a new screen with every state
```

## 7. State slop
| Slop | ID |
|---|---|
| Happy path only | F06 |
| "Saved!" before the write resolves | F06 |
| Disabled button with no explanation | F06/judge |
| Centered spinner on a blank screen for every load | D20 |
| Fake zero data on first use ("0 steps", empty chart axes) | F01/F06 |
| Error = red toast that disappears | D10/F06 |
| Truncating the longest real string | D28 |
