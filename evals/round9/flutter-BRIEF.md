# Brief — "Plot 42" (a community allotment site)

Plot 42 is the app of one allotment site run by its members: 120 plots, a water
network of standpipes, a shared tool shed, a compost bay and a monthly working party.
Plot holders (many retired, some young families) open it at home before going down
("is the water on? is it frosty tonight? whose turn is the watering rota?"), on the
plot (log what they sowed or harvested, book the rotavator, report a broken tap), and
when the committee needs them (inspection week, an overgrown-plot warning, rent due,
a harvest swap on Saturday). The tone is neighbourly, practical and unhurried —
never a smart-garden gadget app, never a social network.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the plot holder (name, plot number and size, years on the site, rent paid/due),
  their plot: beds with what is growing, sown/planted dates, expected harvest;
- site status: water on/off per standpipe (off in winter or for repairs), frost or
  heat warnings, gate code changes, the tool shed (rotavator and strimmer bookings);
- the watering rota (whose turn this week), the working party date, the committee's
  notices (signed), inspections (date, what inspectors look for), the harvest swap;
- states: water off (with when it comes back); frost tonight; inspection week with a
  warning on this plot ("beds 3 and 4 need clearing by Sunday"); rent overdue;
  rotavator booked by someone else; winter (little growing); offline on the site;
  first season (new plot holder, empty beds).

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
