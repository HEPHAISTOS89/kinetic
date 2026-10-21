# Brief — "Chorus" (a community choir)

Chorus is the app of one community choir: 85 singers in four parts (sopranos, altos,
tenors, basses), one conductor, rehearsals every Tuesday 19:30–21:30 in a church hall,
two concerts a term. Singers open it on Tuesday afternoon ("is rehearsal on? which
pieces tonight? where's my alto learning track?"), during the week to practise their
part, before concerts (call time, dress, where to stand, tickets for family), and when
something changes (rehearsal moved, a new piece added, the conductor is ill).
Singers are amateurs of all ages; some read music, many don't. The tone is warm,
encouraging and practical — never a music-streaming app, never a productivity tool.

Design and implement the **home screen** of the app in **React Native** (iOS and
Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the singer (name, part, attendance this term, subs paid or due), the term's
  repertoire (piece, composer, which pieces are on tonight, the singer's learning
  track for their part with length and progress, scores as PDFs);
- rehearsals (date, time, venue, focus pieces, sectionals for one part), concerts
  (date, call time, dress code, standing position, ticket sales for family);
- messages from the conductor and the committee;
- states: rehearsal cancelled or moved; a new piece added with the learning track not
  ready yet; concert week; the singer missed two rehearsals; subs overdue; summer
  break (no rehearsals); offline; first week as a new member.

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
