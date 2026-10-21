# Brief — "Officine" (neighbourhood pharmacy, repeat prescriptions)

Officine is the app of one independent neighbourhood pharmacy (two pharmacists, a small
team, open six days a week). Its users are people on long-term treatments — and the
relatives who manage medicines for them (a daughter for her father, a parent for a child
with asthma). They open it to know whether this month's medicines are ready to collect,
to renew a repeat prescription before it runs out, and when something goes wrong
(a medicine out of stock, the doctor hasn't renewed, a substitution needs their OK).
They are often tired, sometimes worried, sometimes old with large text on. The pharmacy
wants to feel like the counter of a trusted local shop — never a retail e-commerce app,
never a cold hospital portal.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the account holder and the people they manage (self, a parent, a child), each with their
  repeat prescriptions (medicine name, strength, quantity, days of supply left, prescriber,
  renewal date, number of renewals left);
- orders in progress: requested → checked by the pharmacist → ready to collect (shelf/bag
  number, collect-by date) / partly ready (one item back-ordered with an expected date) /
  waiting for the doctor / substitution proposed (generic or different strength, needs OK);
- the pharmacy: opening hours today, closed today (then the on-duty pharmacy nearby),
  a message from the pharmacist, the phone number;
- states: nothing due; a treatment running out in 3 days with no renewal possible
  (must see the doctor); offline (the app shows what it last knew); a recall notice on a
  batch of one medicine (rare, serious).

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
