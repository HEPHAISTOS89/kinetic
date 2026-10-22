# Brief — "Branch" (a neighbourhood public library)

Branch is the app of one neighbourhood branch of a city library: 40,000 books, a
children's corner, six study desks you can book, a computer room, and a programme
of free events (story time, a Tuesday repair café, a reading group, English
conversation classes). Members of every age open it on the way ("is my hold ready?
when do my books go back? is it open late tonight?"), at the counter (scan their
card, pick up holds, renew), and at home (search, place a hold, book a desk, see
what's on this week). Many members are older or new to the country; many are
parents with children. The tone is quiet, literate and welcoming to everyone —
never a bookstore, never a gamified reading tracker.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the member (name, card number and barcode, home branch, family members on the
  same account), their loans (title, author, due date, renewals left), their holds
  (position in the queue, or ready to collect with the shelf it's on and the last
  day to collect), their desk bookings;
- the branch (opening hours today and this week, late night on Thursday, closures),
  this week's events (time, room, places left, whether booking is needed), the
  librarians' picks (signed), new arrivals;
- states: an ordinary day with two loans out; a hold ready to collect (last day
  tomorrow); books overdue (fines are suspended for children's books but not for
  adults'); branch closed today (a burst pipe, with the nearest open branch); a
  desk booked for this afternoon; a family account (a parent with two children's
  cards); a new member's first week; offline at the counter (show the card
  barcode anyway).

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
