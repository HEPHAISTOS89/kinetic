# Brief — "Kiln" (a shared pottery studio)

Kiln is the app of a shared ceramics studio: 60 members, 8 wheels, two electric kilns,
a glaze room, open from 7:00 to 23:00. Members are hobby potters with day jobs.
They open it before coming in ("is a wheel free tonight?"), at the studio (book a
wheel, put a piece on the bisque or glaze shelf, see what's coming out of the kiln),
and when something is ready or wrong ("your mugs are out of the glaze firing",
"a piece cracked in the kiln", "your shelf space is full"). The studio is run by two
potters; the tone is warm, hands-on and unfussy — never a booking-platform app,
never a social feed of pots.

Design and implement the **home screen** of the app in **React Native** (iOS and
Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the member (membership: monthly / 10-session pass with sessions left / paused),
  their shelf space (used / allowed), their wheel bookings (date, time, wheel number);
- wheels right now and tonight (free / booked / out of order), studio opening hours,
  who is on duty;
- the member's pieces and where each one is in the process: drying → bisque shelf →
  bisque firing → glaze shelf → glaze firing → ready to collect (with dates); kiln
  schedule (next firing, which kiln, temperature reached, cooling, unloading time);
- states: a firing finished and pieces are ready; a piece cracked or a glaze ran
  (with a photo and a note from the studio); the kiln is late or broken; shelf full;
  no session left on the pass; studio closed (holidays); offline in the studio
  basement; first visit (no pieces yet).

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
