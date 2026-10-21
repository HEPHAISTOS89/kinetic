# Brief — "The Rialto" (independent cinema)

The Rialto is a single-screen-and-a-half independent cinema (Screen 1: 180 seats with a
balcony; the Studio: 40 seats) run by a small team and its members. Members open the app
on the way out of work ("what's on tonight, are there seats, can I still make the 18:45?"),
at the door (their ticket and their membership card), and on Sunday to plan the week.
Programming is the point: retrospectives, a weekly classic, Q&As with directors, a
silent film with live piano once a month. The tone is cinephile, warm and a little
witty — never a multiplex chain app, never a streaming catalogue of posters.

Design and implement the **home screen ("Tonight")** of the app in **React Native**
(iOS and Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- tonight's and this week's screenings: film (title, director, year, country, runtime,
  format: 35mm / DCP / restored 4K), version (original + subtitles), screen, start time,
  seats left (by zone: stalls / balcony), events (intro, Q&A, live music), age rating;
- the member: membership (annual, renews on a date; or none), free tickets left this
  year, their booked tickets (seat, screen, time, entry code), their watchlist;
- states: sold out (with a waiting list), few seats left, screening cancelled or moved
  (projector fault), starting late, nothing on tonight (closed Mondays), the membership
  has expired, offline at the door (the ticket must still show), first visit (no
  membership, no tickets).

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
