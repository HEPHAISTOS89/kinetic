# Brief — "Sound" (an island car ferry)

Sound is the app of one small car ferry that crosses a two-mile sound between the
mainland and an island of 2,000 people, 14 crossings a day, 32 cars per boat. Island
residents use it daily (commuters, the school run, the vet, deliveries); visitors use
it in summer. People open it before leaving home ("is the 08:10 running? is there
space for my car? is the weather going to stop it?"), in the queue at the slipway
(show the ticket, which lane), and when plans change (a cancellation, a swap to a
later sailing, a refund). The tone is plain, reliable and local — never a travel
deals app, never a cruise brochure.

Design and implement the **home screen** of the app in **React Native** (iOS and
Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the traveller (name, resident or visitor, their vehicle and its registration and
  length, a book of 10 resident tickets with how many are left), their bookings
  (sailing time, direction, vehicle, passengers, ticket QR);
- today's timetable both ways (each sailing's time, car spaces left, foot passengers
  always welcome), the boat's live position and delay, the weather and sea state,
  the skipper's notices (signed), the tide (the slipway is unusable at very low tide);
- states: an ordinary morning with a booking on the 08:10; in the queue at the
  slipway now (show the ticket, lane 2); the 08:10 is full (next spaces, standby);
  sailings at risk from wind (a decision at 07:00); all sailings cancelled for the
  day (rebook, refunds, the emergency arrangements); a 25-minute delay; only 1
  resident ticket left; a visitor's first crossing (where to queue, how to pay).

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
