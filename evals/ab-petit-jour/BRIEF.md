# Brief — "Petit Jour" (daycare day for parents)

Petit Jour is used by a small network of daycares (crèches) in France. The carers log each
child's day on a shared tablet — arrival, meals (how much was eaten), naps (start/end),
nappies, small moments with an occasional photo, notes ("a bit warm this afternoon, 37.9°").
Parents use the phone app: glancing at it during the work day ("is she napping? did she
eat?"), at pick-up time, and when something needs their attention (a message from the
carers, a form to sign, "please bring nappies"). Parents can be anxious; carers are
professionals, not a social network. The app must reassure without hiding anything, and
never turn a toddler's day into metrics or a feed to scroll.

Design and implement the **home screen ("today")** of the parent app in **React Native**
(iOS and Android). The interface language is **French**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the parent, their child(ren) (first name, age in months, group "Les Lucioles"), the
  daycare and its opening hours; some families have two children in the same daycare;
- today's timeline as logged by carers: arrival time, meals (with quantity: all / half /
  a little / refused), naps (in progress or done, with times), nappies, moments (text,
  sometimes a photo), temperature or health notes, who logged it and when;
- pending things: unread message from the carers, a document to sign, an item to bring,
  a planned absence, pick-up time and who picks up (a parent or an authorised person);
- states: the child isn't there yet / absent today / day over; the daycare is closed;
  carers sometimes log late (the timeline can lag by an hour); network can be offline;
  a health note can be important (fever above 38° → the parent must be called).

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
