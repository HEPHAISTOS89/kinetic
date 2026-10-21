# Exemplars — mechanisms worth stealing

These are principles drawn from widely praised mobile products, written as
**transferable mechanisms**. Borrow the mechanism and never the trade dress:
no logos, signature colors, mascots, icon sets or layouts copied wholesale. Each
entry also says when borrowing would be wrong, because a great pattern in the
wrong product is still slop.

Claims below are limited to well-known, publicly visible characteristics.
Specific values (hexes, durations) are deliberately not attributed to these
products. Kinetic's own numbers live in directions.md.

---

### Things 3 — calm hierarchy and creation by direct manipulation
**Mechanism:** generous whitespace and a restrained palette make a task list feel
calm instead of urgent. The floating "magic plus" can be dragged to the exact
position where the new item should go, so where you drop it is the decision.
Lists expand into a full-screen item without leaving context.
**Principle:** let the gesture carry the decision. When placement matters, create
in place instead of create-then-sort. Calm is achieved by subtraction, not by
pastel colors.
**Wrong to borrow when:** the domain is high-volume or operational. A ticket
queue needs density, filters and bulk actions, not serenity.

### Flighty — live data as typography, states you can read at a glance
**Mechanism:** a flight's status is communicated by a few large, glanceable
facts (time, gate, delay) and by explicit, distinct states (scheduled, boarding,
departed, delayed, landed). Live Activities and widgets turn the lock screen
into the primary surface.
**Principle:** for anything that changes over time, design the **state machine
first** and make each state look different at a glance. Put the one changing
number in display type.
**Wrong to borrow when:** the data doesn't change often enough to justify a live
surface. A static receipt doesn't need a Live Activity.

### Apple Weather — atmosphere that carries meaning
**Mechanism:** backgrounds and animated conditions reflect the actual weather
and time of day. Precipitation and temperature ranges are shown as bars and
maps whose color means temperature, not decoration.
**Principle:** a gradient or animation is justified when it **encodes data**
(time, intensity, condition). This is the legitimate form of C04.
**Wrong to borrow when:** the gradient means nothing. That is D01. Weather can be
atmospheric because the atmosphere *is* the content.

### Halide — professional density without clutter
**Mechanism:** a camera app with pro controls (focus, exposure, manual modes)
exposed through gestures and compact instrument-style readouts. The viewfinder
remains the hero. Tactile dials and haptics make adjustments feel physical.
**Principle:** expert users want **controls at the point of action** and
precise feedback. Density is acceptable when every element is a working
instrument, and haptics can replace looking.
**Wrong to borrow when:** the users are novices doing a task once. Then a single
obvious button beats a dial cluster.

### Linear (mobile) — speed as a design value
**Mechanism:** the app is built around fast triage: quick actions, consistent
list rows with clear status and priority glyphs, a restrained monochrome UI
where color is mostly reserved for status.
**Principle:** in work tools, perceived speed *is* quality. Reserve color for
status, keep row anatomy identical across every list, and make the top 3 actions
one tap away.
**Wrong to borrow when:** the product is emotional or brand-led. Monochrome
restraint can read as cold in consumer wellness.

### Arc Search — the answer before the list
**Mechanism:** "browse for me" composes a readable page from search results,
so the user gets a synthesized answer before (or instead of) a list of links.
Simple gestures like pinch to summarise replace menus.
**Principle:** **deliver the outcome, not the inventory.** When the user's goal
is an answer, design the answer screen first and the result list second.
**Wrong to borrow when:** users need to verify sources or compare options
themselves (legal, medical, procurement). Then the list *is* the answer.

### Revolut — breadth organized by a strong home hierarchy
**Mechanism:** a very broad product (accounts, cards, exchange, investing) is
held together by a dominant home balance and consistent transaction rows, with
secondary products surfaced as modules.
**Principle:** when a product does many things, choose **one anchor number**
and one repeated row anatomy. Everything else hangs off them.
**Wrong to borrow when:** the product does one thing. Module stacks then become
a dashboard costume (D04).

### Monzo — humane language and transparent money
**Mechanism:** plain, warm copy ("You've spent £x today"), merchant names and
logos that make transactions recognisable, and instant notifications that turn
the app into a trustworthy real-time ledger.
**Principle:** **copy is interface.** Translate system data into the user's own
words, and make every transaction instantly recognisable without decoding.
**Wrong to borrow when:** the tone becomes jokey in serious moments. A declined
payment or a fraud alert needs clarity, not personality.

### Airbnb — category navigation with photos first
**Mechanism:** an icon-and-label category bar lets people browse by kind of
place. Listings are photo-led cards with consistent metadata order, and search
is a structured, step-by-step sheet (where, when, who).
**Principle:** when the decision is emotional and visual, **lead with real
media** and keep metadata order identical across every card. Break a complex
query into a guided sequence.
**Wrong to borrow when:** you have no real photos (images are out of v1 scope).
A photo-first layout with stock imagery is D07.

### Duolingo — feedback as character and motion
**Mechanism:** immediate, animated, sound-backed feedback for right and wrong
answers, a character that reacts, and progress made visible after each lesson.
**Principle:** **feedback should be proportional and immediate**: a small win
gets a small response, a real milestone gets a bigger one. Motion and sound can
make correctness felt.
**Wrong to borrow when:** almost always for the gamification itself. Streaks,
leagues and guilt notifications serve Duolingo's model, and copied elsewhere
they are D27. Borrow the feedback timing, not the streak.

### Headspace — soft, but structurally disciplined
**Mechanism:** a warm, friendly visual language (rounded shapes, gentle color)
sits on a simple, consistent structure: a clear daily recommendation, short
sessions and a single play action.
**Principle:** **softness is a voice, not a structure.** Keep the grid, the type
ramp and the primary action rigorous, and let shape and color carry the warmth.
See Soft Tactile in directions.md.
**Wrong to borrow when:** the domain is clinical or serious. Rounded whimsy can
trivialise medical information.

### Apple Fitness / Activity — one encoding, learned once
**Mechanism:** progress toward daily goals is shown with a single, consistent
visual encoding (the rings) everywhere: app, watch, widgets and sharing.
**Principle:** if you invent a visual encoding, **use it everywhere** and make it
the product's vocabulary. Consistency is what turns a chart into a symbol.
**Wrong to borrow when:** you copy the rings. Progress rings are the most
imitated slop element in fitness (D04/D27). Invent an encoding that belongs to
your spine, or use plain numbers.

### Craft / Bear — editorial typography for writing tools
**Mechanism:** typography and spacing are tuned for reading and writing, with
comfortable measure, clear heading hierarchy, restrained chrome that disappears
while typing, and themes that change mood without changing structure.
**Principle:** in writing tools, **the document is the interface**. Hide chrome
while the user types, and invest in the type ramp before anything else.
**Wrong to borrow when:** the core task is structured data entry. A serif
document aesthetic for a form is pretentious and slow.

### (Not Boring) Weather, CARROT Weather — expression at level 5
**Mechanism:** a mundane utility made memorable through a strong, consistent
personality: bold 3D or illustrative visuals, sound, motion and an attitude in
copy, while the actual forecast stays legible.
**Principle:** high expression works when the **core data remains instantly
readable** underneath the personality, and when the personality is coherent
(one voice, everywhere).
**Wrong to borrow when:** the user is stressed, in a hurry, or the stakes are
high. Personality on a banking error screen is hostile.

### Copilot Money — clarity in a dense financial picture
**Mechanism:** spending is categorised, reviewed and summarized with clear charts
and a review flow for new transactions. Recurring items and budgets are shown
relative to expectations.
**Principle:** **show numbers relative to an expectation** (budget, last month,
typical) so every figure answers "is this OK?". A review queue turns passive
data into a small, finishable task.
**Wrong to borrow when:** the user doesn't have the habit of review. Then the
queue becomes guilt. Start with a single "safe to spend" answer instead.

---

## Cross-cutting lessons
1. **One anchor per screen** (Revolut balance, Flighty status, Fitness rings). Find yours in `screens[].primary`.
2. **The state machine is the design** for anything live (Flighty). Write `states` before visuals.
3. **Meaningful atmosphere** (Weather) is the only legitimate gradient.
4. **Gesture as decision** (Things, Halide). Direct manipulation beats dialogs.
5. **Copy is interface** (Monzo). Every label is a design decision.
6. **Personality on top of legibility** (Carrot, Headspace), never instead of it.
