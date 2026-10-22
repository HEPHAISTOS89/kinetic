# Component contracts: the skeleton, never the skin

Every recurring mobile part has a **behaviour** that is the same in every
product and a **look** that must never be the same. Kinetic standardises the
first and leaves the second to the deal, the vocabulary and the thesis.
A contract says what the part must do, in every state and on both platforms;
it says nothing about colour, type, radius or ornament. If you find yourself
copying a look from here, stop: there is none to copy.

Why this file exists: across eleven blind rounds Kinetic lost points not on
ideas but on the same behaviours rebuilt badly each time (rows cut under a
dock, a badge that jumps between states, a pass with no native sheet, an
offline state with no time, links that look like web pages). Each contract
below lists the failure it prevents and how it is checked.

How to use: when a screen needs one of these parts, read its contract before
building it, record it in KDL `screens[].components` with its `kind`, and
render every state listed. The craft pass (kinetic-craft §1) checks them.

---

## 1. Docked action (the state's one action, pinned above the tab bar)
- **Job**: the primary act of *this state*, always in thumb reach.
- **Anatomy**: one primary + at most one secondary; label = verb + object
  (≤ 3 words); a solid band behind it (no gradient fade over content).
- **Rules**: the scroll content above it ends with bottom padding = band height
  + tab bar + 24pt; the label changes with the state (no "Renew" during a
  recall); when the state needs no action, the band goes away — never an
  empty or generic button.
- **States**: enabled, pressed, loading (label stays, spinner replaces icon),
  disabled with a reason line, offline (queued: "Will send when back online").
- **iOS**: full-width rounded-rect or capsule per the system, above the tab
  bar, respecting the home indicator. **Android**: M3 filled button (pill),
  above the navigation bar; a FAB only for creation-first screens.
- **Prevents**: rows half-hidden under the dock (round 10–11, 7 reads), D37
  fades, two filled buttons fighting. **Check**: last row fully visible in
  every render; `scan` D37; one filled button per viewport.

## 2. Navigation shell (tab bar / navigation bar)
- **Job**: the app's two to five places, reachable one-handed.
- **Rules**: present on every top-level screen (a home with no navigation
  scored native fidelity 2 in round 11); labels at platform size, regular
  weight, under regular-weight icons; the selected state is shape + weight,
  not colour alone; no badge unless the user must act.
- **iOS**: `CupertinoTabBar` / `TabView`, translucent material or a solid
  ground — never content ghosting through a clear bar. **Android**: M3
  `NavigationBar` with the pill indicator. Never the M3 pill on iOS.
- **Prevents**: Material chrome on iOS, ghost text under a clear bar, missing
  navigation. **Check**: both platform renders show their own shell.

## 3. Sheet, pass and ticket
- **Job**: a focused object over the home: a pass at a gate, a card at a
  counter, a choice.
- **Rules**: iOS page/form sheet with grabber and detents, `Done` top-right;
  Android modal bottom sheet or a full-screen route with back. A scannable code
  (QR, barcode) stays on a white plate in both themes, raises brightness while
  open, and says it works offline when it does. Wallet button where the
  platform has one (Apple Wallet / Google Wallet), platform-styled.
- **States**: loading (keep the last code), offline (code + "saved on this
  phone, checked 08:12"), expired, family/multiple (paged, with names).
- **Prevents**: a pass as an ordinary tab page, a pass that dims in dark mode.

## 4. State hero (the top of the home)
- **Job**: answer the glance question *for this state*.
- **Rules**: the state's priority owns it (layout.md §1: a due dose, an
  overdue bill, a closure); it draws that state's **evidence** (the gusts vs
  the limit, the full deck, the closed section), not just a new tint; one
  display size constant across states; the everyday answer collapses to one
  line when another item leads; combined states rank both above the fold.
- **Prevents**: a brand banner pushing every task below the fold; a hero that
  only changes colour.

## 5. Status and severity
- **Job**: say how worried to be.
- **Rules**: a ladder of distinct steps — routine (neutral), late (quiet
  note), attention (one hue + the decision time), danger (danger hue + icon +
  word); never two severities in one colour; good news never in the danger
  hue; status said once, where it can be acted on (D32).
- **Prevents**: wind risk, full deck and delay in the same ochre (round 11).

## 6. List row
- **Job**: one item, scannable.
- **Anatomy**: leading mark (the vocabulary's, not a generic avatar), title
  ≤ 5 words, one meta line ≤ 6 words at text-2, trailing value or action.
- **Rules**: ≥ 44/48pt tall; trailing numbers right-aligned in tabular
  figures; one trailing action, a real button (not underlined text); at XXL
  the row stacks (title, then meta, then action) — never clips.
- **Prevents**: underlined web links as row actions (D38), wobbling stamp
  widths, avatars as filler.

## 7. Schedule / timetable
- **Job**: times the user chooses between.
- **Rules**: times in tabular figures on a fixed column; capacity as a word or
  number next to any glyph ("3 left"); disruptions inline on the affected row
  ("Low tide: may wait"), never as a separate banner; a delay propagates to
  the following rows; your own entry marked by shape + word.
- **Prevents**: unexplained pie/pip glyphs, misaligned 3-vs-4 columns.

## 8. Offline and stale data
- **Job**: keep the product honest without signal.
- **Rules**: say the age of every stale fact in words ("as of 06:31", never
  "Board from 06:31"); keep what works offline working and say so (the pass,
  the emergency number, the last plan); queue actions with their promise
  ("will renew when back online"); offer `Retry` once, quietly. Stale numbers
  carry the age in a caption, not a tilde inside display numerals.
- **Prevents**: offline states with no time; "~27 °C" in display type.

## 9. Error with recovery
- **Rules**: what happened in the user's words, what still works, one way
  forward ("Today's list didn't load. The emergency line below always
  works."); never a dead end, never "Oops".

## 10. Compact header on scroll
- **Rules**: the large title or hero collapses to a one-line summary + the
  state's key action ("Two books · due Wed 4 Nov · Card"); the header has a
  solid or material ground with a hairline once content passes under it; its
  elements keep their baseline in every state (a status line goes below, never
  shifts a badge).
- **Prevents**: half-cut text under a transparent pinned header (round 11,
  3 reads); badges that jump between states (round 8).

## 11. Section label
- **Rules**: one style for the whole app (≥ 13pt, text-2 contrast); sentence
  case; no tracked all-caps eyebrow above every card (a template tell critics
  name every round).

## 12. Secondary action
- **Rules**: a platform text button or tonal button with a ≥ 44/48pt target;
  never underlined body text (`textDecorationLine: 'underline'` on a
  pressable, `TextDecoration.underline` on a tappable — D38); one per block.

## 13. Signed note (a person speaking)
- **Rules**: the note itself, unboxed, in the voice face's italic or the text
  italic; the signature with a time on its own line ("Maya R., lifeguard,
  20:40"); one note per viewport; the age shown when it is about "this
  afternoon" and the time has passed.

## 14. Drawn data signature (the vocabulary as a chart)
- **Rules**: two volumes (clarity.md): yours and actionable at full ink, the
  rest at text-3 or collapsed; every mark carries its word; labels ≥ 13pt and
  centred on their node or uniformly aligned; nothing overlaps a numeral; at
  XXL it reflows (codes + list) rather than shrinking.

## 15. First run / empty
- **Rules**: one sentence of what this place is for *you*, one action, and the
  thing that will appear here drawn at rest (the empty shelf, the empty deck);
  no carousel, no illustrations of people waving.

---

Contracts are behaviour. The look of each part comes from the dealt
direction and the inventory; two Kinetic apps should share none of it.
