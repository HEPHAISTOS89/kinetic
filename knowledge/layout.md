# Layout, space, shape and composition on a phone

A phone screen is ~375–440pt wide, held in one hand, read in glances. Good
mobile layout is mostly **subtraction and rhythm**: one primary thing, a clear
second, consistent spacing that groups without boxes, and actions where the
thumb already is.

## 1. Composition before components
Decide, per screen, before styling (KDL `screens[].primary/secondary/reading_order`):
1. **The job** in one sentence.
2. **The primary element** — the thing seen in the first 500ms. Exactly one.
3. **The second read** — what explains or qualifies it.
4. **The action** — where it sits relative to the thumb.
5. Everything else is tertiary and must look it.

The squint test: blur the screen; the primary element should still be the
darkest/largest/most contrasted mass.

**Glance screens spend the top on answers.** On screens used in 1–3 seconds
(departures, weather, balance, sleep), the first 150pt carry the answer and its
trust state, not a page label. A 34pt large title there costs the primary
element its place (blind critics penalised exactly this). Use large titles for
browse/list hubs; use a compact contextual header for glance screens.

**Answer a qualitative question with a verdict, then the number.** When the
user's glance question is a judgement ("is it packed?", "is she OK?", "can I
afford it?"), the display-size element is a short verdict sentence in the
product's voice ("Plenty left until two.", "Your fern can wait until
Thursday."), and the number supports it underneath ("62 loaves · usually gone
by 15:00"). The sentence also carries data age by grammar ("Was plenty at
11:40."). Blind critics have ranked the verdict-sentence hero above a numeral
hero for the same data. Keep the numeral as the hero only when the number *is* the
answer (a balance, a departure in 3 min, a temperature).

**One loud mass per viewport.** A multicolour grid of chips (categories,
tags, status pills) is visually the heaviest thing on a screen. Below the hero,
show only what is new or yours at full colour and the rest
behind "All …" or at reduced chroma, so the squint test still finds the answer.

**Secondary blocks stay compact.** A chart or list that supports the primary
answer uses single-line rows (label, inline bar, value ≈ 44pt), so the action
and the first content item stay in the first viewport. Two-line rows for a
secondary chart pushed "Settle up" and "Recent" below the fold in the A/B tests.

## 2. Spacing scale (4pt grid)
Use a named scale and nothing else (D17):

| Token | pt | Typical use |
|---|---|---|
| xs | 4 | icon ↔ label, tight inline gaps |
| s | 8 | related items inside a group |
| m | 12 | list row internal padding (vertical) |
| l | 16 | standard padding, between controls |
| xl | 24 | between groups / sections on compact screens |
| 2xl | 32 | between major sections |
| 3xl | 48 | breathing space around a hero element |

- **Proximity defines grouping**: space inside a group < space between groups
  (ratio ≥ 1.5×, e.g. 8 inside / 16 or 24 between). If you need a box to show
  grouping, the spacing is wrong.
- Screen margins: **16 or 20pt** on iOS (system layout margins are 16/20),
  **16dp** on Android compact; 24 for airy, editorial directions. One value per app.
- Vertical rhythm: line heights and spacing on the 4pt grid keep baselines regular.

## 3. Ergonomics: the thumb and the glance
- Bottom third = easy reach; top corners = hard reach. Primary and frequent
  actions go low (tab bar, bottom sheet actions, bottom-anchored buttons);
  destructive and rare actions can live high.
- Touch targets **≥ 44×44pt (iOS) / 48×48dp (Android)** with ≥ 8pt between
  adjacent targets (F05). The glyph can be 17–24pt; the hit area cannot.
- One-handed reachability: avoid essential controls in the top 20% on tall phones.
- Glanceability: the primary information should be legible at arm's length,
  in sunlight, in 1 second — size and contrast over decoration.

## 3b. Layout craft floor (what blind critics docked, rounds 7–9)
Kinetic's layout craft averaged 3.6 vs 4.0 for the best competitors; every
point lost came from the list below. Check each on every render before the panel.
1. **Short states are composed, not abandoned.** A state with less content
   (done, a single prompt, an empty day) must not leave a hole between the
   content and the pinned bar ("accidental voids", "top-heavy"). Either set
   the answer at the optical centre (~40% of the height) with the action at
   the thumb, or bring up the next useful block (what's next, the summary,
   the season). `kinetic clarity` reports `void_pt`; > 130pt is a finding.
   Space around a hero is calm; space *below everything* is unfinished.
   **The scrolling-home pattern** that satisfies both this and item 2: the
   first viewport ends on a *complete* row or on the next section's heading
   fully visible with ~8pt of its first row (a deliberate peek); the scroll
   content carries bottom padding = pinned bar + tab bar + 24pt; a short state
   fills the space with the next useful block, never by pushing content down.
2. **Sticky bars reserve their space.** Scroll content ends with bottom
   padding = bar height + tab bar + 24pt; the last row never sits half under
   a pinned action or a fade ("'Keep tomorrow' cut off by the tab bar" cost
   points in 4 of 6 reads). **No fade over content** (D37): a gradient that
   dissolves rows into a dock reads as "faded, half-cut, muddy" (round 10,
   3 of 3 critics); the fold falls on space between sections, or the dock
   sits on a solid band with the scroll ending above it.
3. **Drawn data snaps to a grid.** Columns in a drawing are fixed slots (a
   row of 3 events aligns with a row of 4 by time, with explicit empty cells);
   labels are centred on their node or all aligned the same way; nothing
   overlaps a numeral (check the threshold mark vs the axis label); brackets
   and ranges snap to the column edges they span.
4. **Header elements don't move between states.** Badges, avatars and dates
   sit on the same baseline in every state; an added status line goes below,
   never shifts them. On scroll, a compact header (or the platform's large
   title collapse) keeps content from sliding under the status bar.
5. **One alignment for a list's trailing values**: right-aligned numbers in
   tabular figures; checkmarks and chevrons on the same column.
6. **Encodings without legends** (D31): filled = taken, open = free, taped =
   broken; if a mark needs a key, label it in place.
7. **Explain the signature in its calm state.** A vocabulary mark that encodes
   a threshold (a flood line, a limit, a capacity) is labelled once in the
   default state ("S4 path floods above 6.0 m"), so it reads before it becomes
   an alert (round 9, all three critics).

## 4. Grids and alignment
- Single column is the default on phones. Two columns only for equivalent,
  scannable items (media grids, products); never for forms or reading.
- One left edge: text, icons and controls share the content edge; indents mean hierarchy.
- Align on **first baselines** in rows, **optical centers** for icons, **cap
  height** for icon + text pairs.
- Numbers in lists right-align with tabular figures.
- Avoid accidental near-alignments (an element 2pt off an edge looks like a mistake;
  either align exactly or offset clearly).

## 5. Shape: radius as a system
- 3–4 radii plus `full` (D15). Example: s 8 (chips, small controls), m 12–14
  (fields, cards), l 20–28 (sheets, large cards), full (pills, avatars).
- **Concentric rule**: `inner radius = outer radius − padding`. A 24pt card with
  12pt padding holds 12pt-radius content. Equal radii nested look wrong.
- **Continuous corners** (squircle) on iOS: `RoundedRectangle(style: .continuous)`;
  Flutter/Compose need superellipse shapes or tuned values (see stacks/).
- Radius expresses voice: small radii (4–8) read precise/professional;
  large (20+) read soft/friendly. Mixing both without a rule is chaos.

## 6. Elevation: pick one strategy (D16)
| Strategy | How | Fits |
|---|---|---|
| tonal | surfaces differ by lightness (dark mode native; Material 3) | most apps, all dark modes |
| border | 1px hairlines in `border` role | precise, dense, editorial |
| shadow | one or two soft shadows, low opacity (≤ 8–12%), large blur, small y | light themes, floating elements only |
| none | space and type alone | calm, editorial, expression 1–2 |

Overlays (sheets, menus, dialogs) are the exception that always lifts — with
the platform's material and dimming, not a heavy custom shadow.

## 7. Containers: when to use a card (D03, C03)
Use a card when the content is **an object** the user can act on as a unit
and there are **many of them** (a trip, an account, a product). Don't card:
single settings, explanatory text, headers, the one hero element, groups that
spacing can already separate. Lists with dividers or plain rows are often
more native than stacks of cards.

## 8. Lists and rows (the backbone of mobile)
- Row height ≥ 44pt; comfortable 56–72 for two-line rows.
- Leading element (icon/avatar) 24–40pt, aligned to first text baseline or centered for single-line rows.
- Trailing: value (text-2), chevron for navigation (iOS), switch/checkbox for settings.
- Dividers inset to the text edge (iOS) or full-width (Material lists) — follow the platform.
- Swipe actions for frequent per-row operations; always with a visible alternative.

## 9. Navigation structure
- Tab bar for 3–5 parallel top-level areas used often. Not for actions (D08).
- Stack navigation for depth; large title collapsing to inline (iOS) for top-level lists.
- Sheets for focused sub-tasks that return (detents: medium for quick choices, large for editing).
- Full-screen modals for creation flows that need commitment.
- Never hide primary navigation behind a hamburger on iOS.

## 10. Adaptivity
- Layout responds to **available space**, not device model: compact width
  (< 600dp / most phones portrait), medium (foldables, small tablets), expanded.
- Safe areas, notch/dynamic island, home indicator, keyboard insets (F09).
- Landscape on phones: at minimum don't break; media apps should design it.
- Test widths: 320 (iPhone SE 1st gen / small Android), 375, 393–402, 430–440; heights down to 568.

## 11. Composition patterns that read as designed
- **Hero numeral**: one large figure + one sentence of meaning + quiet detail (finance, health, sleep, weather).
- **Editorial stack**: large title, generous measure, images full-bleed, captions small (reading, travel).
- **Tool surface**: dense list/grid, persistent toolbar, inspector sheet (pro tools, photo, notes).
- **Feed with intent**: content first, actions inline, chrome recedes on scroll (social, media).
- **Wizard with progress**: one question per screen, progress visible, back always possible (onboarding, forms).

## 12. Layout slop (map to the catalog)
| Slop | ID |
|---|---|
| Off-grid magic padding | D17 |
| Card soup | D03 |
| Bento of empty or random cells | D03/D04 |
| 5 equal tabs, hamburger on iOS | D08 |
| Fixed 375×812 frames | D29 |
| Everything centered | D11 |
| Content under the status bar / keyboard | F09 |
| Truncated titles to fit a fixed row | D28 |
