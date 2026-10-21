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
