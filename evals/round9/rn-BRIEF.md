# Brief — "Tern" (a coastal bird survey)

Tern is the app of a volunteer bird survey on one stretch of estuary coast: 60
volunteers each walk a fixed route ("transect") once a month at high tide and count
birds. Volunteers open it the evening before ("is my survey tomorrow? what time is
high tide? will it rain?"), on the shore (log counts species by species, often with
cold wet hands and binoculars in the other hand), and after (sync, see what others
counted, the coordinator's notes: "a spoonbill was seen at the north pool!"). Many are
retired; some are students. The tone is patient, precise and friendly — never a
gamified birding app, never a social feed.

Design and implement the **home screen** of the app in **React Native** (iOS and
Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the volunteer (name, their transect and its sections, surveys done this year),
  their next survey (date, high-tide time and height, the window to start, weather),
  this month's partial counts if they have started (species, count per section);
- the coordinator's notes (signed), notable sightings on the estuary this week,
  the season (which species are arriving or leaving);
- states: survey tomorrow; survey in progress (counts saved on the phone, not yet
  synced); survey done and synced; weather too bad (postpone, with the next window);
  access closed (a section flooded or fenced off); a rare species logged that needs a
  description; offline on the shore; first survey (training walk with a mentor).

## Deliverables (all in your working directory)
- TypeScript/TSX source files. Allowed imports: `react`, `react-native`,
  `react-native-svg` (draw your own icons with it — there is no icon font),
  `react-native-safe-area-context` (the harness provides the insets: use
  `useSafeAreaInsets` / `SafeAreaView`, but do not add a `SafeAreaProvider`).
  Nothing else (no npm install). Images: no network; draw placeholders or use local files.
  You may bundle fonts: copy .ttf/.otf files from /System/Library/Fonts/Supplemental or
  /Library/Fonts into `fonts/`; the font family name is the file name without extension
  (one file per weight, as React Native does on Android).
- `Gallery.tsx` at the root of your directory, exporting every state you designed:
  `export const gallery: Array<[string, React.ComponentType]> = [...]`
  (each component renders the whole screen for that state; read the colour scheme with
  `useColorScheme()`). Short kebab-case names. Include as many states as you consider necessary.
- Render and look at your own result as many times as you like, from your directory:
  `node <HARNESS>/render.mjs`
  It type-checks every .ts/.tsx file (strict, React Native 0.81 types) and renders each
  entry at 393×852pt, top-aligned/cropped, with iPhone-like safe-area insets, light and dark,
  into ./shots (react-native-web in Chromium; the system font renders as SF Pro).
  The type-check must pass.
- A short NOTES.md: what you designed and why (≤ 25 lines).
