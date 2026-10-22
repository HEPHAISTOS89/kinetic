# Brief — "Fernhill" (a small-town veterinary practice)

Fernhill is the app of one independent veterinary practice in a market town: three
vets, four nurses, a consulting room for small animals, a farm round two days a week,
and a 24-hour emergency line shared with the next town. Pet owners (from first-time
puppy owners to retired farmers with sheepdogs) open it when something is wrong ("can
I get an appointment today? is this an emergency?"), when something is due (vaccines,
flea and worm treatment, a repeat prescription to collect), and after a visit (what
the vet said, the medication schedule, the bill). The tone is calm, competent and
kind — never cutesy, never a pet social network, never an insurance upsell.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the owner (name, address), their animals (name, species and breed, age, weight
  history, photo placeholder), each animal's care plan (vaccines with due dates,
  flea/worm treatment, a repeat prescription with collections left), past visits
  (date, vet, notes, bill paid or due);
- the practice (opening hours, which vets are in today, same-day appointments left,
  the emergency number and where to go at night), notices from the practice (signed);
- states: an ordinary week with nothing due; a vaccine due next week; a prescription
  ready to collect; an animal recovering after surgery (medication schedule today,
  wound check on Friday); a possible emergency (the owner opens the app in a hurry);
  out of hours (the shared emergency service); a household with three animals (two
  dogs and a cat); a bill overdue.

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
