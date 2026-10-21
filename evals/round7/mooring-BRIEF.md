# Brief — "Mooring" (a small marina's app for boat owners)

Mooring is the app of one small harbour on a tidal estuary: 140 berths on pontoons,
a fuel dock, a slipway, a harbour office open 8:00–18:00 in season. Its users own small
boats (sailing and motor) and come down at weekends or after work. They open it at home
("can I go out tomorrow morning — tide, wind, is my berth OK?"), on the pontoon
("is the fuel dock open, where is the visitor I'm rafting with?"), and when the harbour
needs them (a storm warning, a mooring line found chafed, the annual fee due).
The harbour team is three people who know everyone. The tone is practical, seasoned and
quiet — never a yachting-luxury app, never a weather-data dashboard.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the owner, their boat (name, length, draught), their berth (pontoon C, berth 14),
  berth status (occupied / boat out / away until a date) and the annual fee status;
- tides for today and tomorrow (high/low times and heights), the depth at the harbour
  sill (the boat can only pass when there is enough water over the sill for its draught),
  wind (speed, gusts, direction) and the inshore forecast;
- harbour notices: from the office (a person, with time), storm or gale warnings, works
  on a pontoon, the fuel dock open/closed, the slipway booked;
- states: the sill is closed for this boat right now (and opens again at a time); a gale
  warning (the harbour asks owners to double their lines); a notice that concerns the
  owner's boat ("chafed bow line on C14 — we've added a spare"); fee overdue; offline
  on the pontoon; out of season (office closed, emergency number).

## Deliverables (all in your working directory)
- A Flutter project (already scaffolded: `pubspec.yaml`, `lib/`, `test/render_test.dart`).
  Put your code in `lib/`. Available packages (offline, already in pubspec): flutter,
  cupertino_icons, flutter_svg, intl. No network: no google_fonts download, no network images.
  You may bundle fonts: copy .ttf/.otf files from /System/Library/Fonts/Supplemental or
  /Library/Fonts into `fonts/` and declare them in pubspec.yaml (see the comment there).
- `lib/gallery.dart` must expose every state you designed:
  `typedef GalleryEntry = (String name, Widget Function(Brightness brightness) build);`
  `List<GalleryEntry> get gallery => [...]` — each builder returns the whole app for that
  state (your theme included) in the given brightness. Short kebab-case names.
  Include as many states as you consider necessary.
- Render and look at your own result as many times as you like:
  `flutter test --update-goldens test/render_test.dart`
  (renders each entry at 393×852 logical px, top-aligned/cropped, with iPhone-like safe-area
  insets, light and dark, into ./shots). Do not modify `test/render_test.dart`.
  Note: the renderer has no SF Pro; Roboto stands in for the system font on both platforms.
  Text scaling is not rendered unless you build an entry that sets it (MediaQuery textScaler).
- `flutter analyze` must report no errors.
- A short NOTES.md: what you designed and why (≤ 25 lines).
