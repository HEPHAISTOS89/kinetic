# Brief — "Prise" (bouldering gym companion)

Prise is the app of an independent bouldering gym (one gym, two walls: "Le Hangar" and
"La Cave"). Members open it on the way to the gym ("is it packed right now? what's new
on the wall?"), at the wall between attempts — chalky fingers, phone on the mat, 30 seconds
of rest — to log a boulder they just topped or flashed, and at home to see their week.
Route setters reset one sector every week; new boulders are the main reason to come.
The gym's tone is warm, a bit raw, community-run — never a gamified fitness app, never
"crush your goals".

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the member (name, membership: monthly / 10-entry card with entries left / expired);
- live occupancy (people inside now, capacity, typical curve for today), opening hours;
- boulders currently on the walls: sector, colour of holds, grade (the gym uses colour
  circuits + Font grades 4 → 7C), setter, date set, how many members topped it;
  this week's reset (sector, date) and boulders coming down soon;
- the member's log: sends (top / flash), projects in progress (attempts), this week's sessions;
- sync: logs made on the wall without signal are queued; occupancy can be stale or
  unavailable; the gym can be closed (holiday, competition day).

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
