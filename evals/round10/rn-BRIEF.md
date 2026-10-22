# Brief — "Lido" (an open-air municipal swimming pool)

Lido is the app of one open-air 50-metre municipal pool, heated, open all year,
with eight lanes (slow, medium, fast and two club lanes), a learner pool, a sauna
and early "dawn swims". Members book a lane slot (45 minutes) and open the app the
night before ("is there a fast-lane slot at 7? how warm is the water? will it
close for lightning?"), at the gate (show their pass, see which lane), and after
(log the swim, see their distance this month). Regulars swim three or four times a
week, all ages; winter swimmers are proud of it. The tone is brisk, bright and
exact — never a fitness tracker with streaks and badges, never a wellness spa.

Design and implement the **home screen** of the app in **React Native** (iOS and
Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the member (name, membership type and expiry, pass QR code), their next booking
  (date, time, lane, lane speed), their swims this month (count, distance),
  their usual slot;
- the pool today: water and air temperature, opening hours, slots per lane with
  places left, lifeguard notices (signed), closures (lightning — reopens 30 minutes
  after the last strike —, cleaning, a club gala), the sauna's hours;
- states: a booked swim tomorrow at 07:00; at the gate now (pass up, lane 6); fully
  booked at the usual time (next free slots and the waitlist); closed for lightning
  (with the reopening estimate); winter (water 26 °C, air 3 °C, the dawn swim);
  membership expiring in 5 days; a cancelled slot (a club gala) with an offered
  swap; the first visit (where the lockers are, the lane etiquette).

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
