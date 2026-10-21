# Brief — "Furrow" (a cooperative veg box)

Furrow is the app of a small cooperative of three organic farms that delivers a weekly
vegetable box to 900 households in one city. Members open it mid-week ("what's in
Friday's box? can I swap the kale? I'm away next week"), on delivery day ("when is the
van coming? it's at the door / at the neighbour's"), and when the farm has news
(hail took the lettuces, the box will be smaller; the first strawberries are in).
The farmers write to members themselves. The tone is earthy, honest and generous —
never a supermarket delivery app, never a recipe-content feed.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the member (box size small/medium/large, delivery day, address, payment status,
  weeks paused), their next box: contents with quantities and which farm grew each
  item, the swap deadline (Wednesday 20:00), swaps made, add-ons (eggs, bread);
- delivery: the van's window, live position on delivery day (stops before yours),
  delivered (where it was left, photo), missed delivery;
- notes from the farmers (signed, sometimes a photo), a shortage replacing an item,
  a price change, the season (what's coming in the next weeks);
- states: swap deadline passed; box paused this week; payment failed; delivery late;
  van broken down; first week (no box yet); offline.

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
