# Sector playbooks

A sector is **context, not a palette**. These playbooks state what users need
to feel and do, the usual expression range, density, legitimate versus
fabricated trust, the sector's typical slop (IDs from anti-slop.md) and the
states that most often go missing. Break a tendency when the thesis demands it,
and write down why in KDL `because`.

Legend: **Expr** = expression level (1–5). **Dir** = suggested directions (directions.md #).

---

### Fintech (payments, budgeting, investing)
- **Feel / do:** in control, informed, never ashamed. Check, move, decide.
- **Expr** 1–3 · **Density** medium–high · **Dir** 1, 6, 12, 4.
- **Legitimate trust:** exact amounts with currency, clear fees *before* confirmation, real-time status, regulatory info in context, biometric confirmation. **Fabricated:** "bank-grade security" shields, invented user counts, fake portfolio growth on onboarding (F01).
- **Sector slop:** D04 dashboard costume, D01 violet card gradients, D14 black+gold "premium", D27 investing streaks, F07 gain/loss by color alone.
- **Tendencies:** tabular numerals always, one anchor balance, restrained color, and up/down semantics with sign and arrow. **Break it** when the audience is young or new to money: warmth and plain language beat terminal aesthetics.
- **Critical states:** pending vs completed vs failed vs reversed transfer; insufficient funds *before* submit; stale market data (timestamp it); duplicate-submit protection; offline with cached balance labelled "as of".

### Banking (retail / traditional)
- **Feel / do:** safe and competent. Balance, pay, cards, help.
- **Expr** 1–2 · **Density** medium · **Dir** 4, 12, 10.
- **Legitimate trust:** consistency with the bank's identity, clear security actions (freeze card), human help reachable. **Fabricated:** padlock ornaments, fake "AI insights".
- **Sector slop:** D03 card soup on home, D10 dialogs for everything, D21 carousel onboarding, D02 greeting.
- **Tendencies:** platform-native, accessible-first, large type support essential (older users). **Break it** with one signature, never with chrome.
- **Critical states:** session timeout with draft preserved; card frozen/lost; disputed transaction; maintenance windows; identity verification in progress.

### Health / medical
- **Feel / do:** reassured, understood, safe to act. Read results, book, take medication, message clinicians.
- **Expr** 1–2 · **Density** medium · **Dir** 12, 4.
- **Legitimate trust:** named clinicians and credentials where real, sources for guidance, clear data provenance (device, lab, self-reported). **Fabricated:** "doctor-approved" badges, invented accuracy claims (F01).
- **Sector slop:** D27 gamified health, D04 rings and vanity metrics, alarming red for neutral info, D22 wellness copy ("Unlock your best self").
- **Tendencies:** plain-language interpretation under every value, reference ranges, units always, calm accent, high contrast. **Break it** never on clinical surfaces. Warmth belongs only in onboarding and support copy.
- **Critical states:** **missing data ≠ zero**; out-of-range value with next step; device disconnected; permission revoked (HealthKit / Health Connect); emergency escalation path; appointment cancelled/rescheduled.

### Wellness / meditation / sleep
- **Feel / do:** calm, held, unhurried. Start a session, reflect, wind down.
- **Expr** 2–3 · **Density** low · **Dir** 3, 7, 2.
- **Legitimate trust:** credible guidance authors, honest expected outcomes. **Fabricated:** "scientifically proven" without source, fake community stats.
- **Sector slop:** D01 purple/indigo night gradients, D07 blobs and abstract waves, D27 streak guilt, D18 entrance confetti, D19 bouncy motion.
- **Tendencies:** dim and warm palettes at night, slow damped motion, one primary action. **Break it** for daytime energy products, but keep motion soft.
- **Critical states:** session interrupted (call, lock), downloaded vs streaming content, first session, a missed day with no shame copy.

### Fitness / sport
- **Feel / do:** energized and capable. Start a workout, track live, review.
- **Expr** 3–5 · **Density** medium · **Dir** 13, 5, 11.
- **Legitimate trust:** accurate sensor data with source, honest PRs. **Fabricated:** inflated calorie claims, fake leaderboards.
- **Sector slop:** D04 ring clones, D27 streak shaming, small numbers mid-workout (F04 at a glance), D26 neon glow.
- **Tendencies:** dark-first, huge tabular live metrics, strong haptics. **Break it** for rehab and senior fitness, where calm and clinical clarity beat energy.
- **Critical states:** GPS lost; sensor disconnected mid-workout; auto-pause; workout recovered after a crash; bright-sun legibility.

### Nutrition / food tracking
- **Feel / do:** supported, not judged. Log quickly, understand patterns.
- **Expr** 2–3 · **Density** medium · **Dir** 7, 12.
- **Legitimate trust:** nutrition sources, editable entries, estimated-vs-exact labels. **Fabricated:** "AI knows your calories" certainty.
- **Sector slop:** red "over budget" shaming, D04 macro rings everywhere, D07 food illustrations.
- **Tendencies:** speed of logging is everything (recent items, barcode, voice), neutral semantics. **Break it** for clinical diets (diabetes): there, precision and Clinical Calm win.
- **Critical states:** unknown food, partial logging, estimate flagged, duplicate entry, day not finished.

### Education / learning
- **Feel / do:** guided, progressing, confident. Continue a lesson, practise, review.
- **Expr** 2–4 (kids 4–5) · **Density** low–medium · **Dir** 9, 7, 2.
- **Legitimate trust:** clear curriculum, honest progress, qualified authors. **Fabricated:** "Learn X in 7 days" claims.
- **Sector slop:** D27 copied streak/league systems, D07 generic mascots, D21 carousel onboarding, D22 hype copy.
- **Tendencies:** one clear "continue" action, immediate proportional feedback, readable type at large sizes. **Break it** for adult professional learning: Editorial Serif beats cartoon.
- **Critical states:** wrong answer with explanation, lesson resumed mid-way, offline content, completed course, an answer that can't be graded.

### Productivity / notes / tasks
- **Feel / do:** focused and fast. Capture, organise, complete.
- **Expr** 1–2 · **Density** medium · **Dir** 4, 1, 2.
- **Legitimate trust:** reliable sync with visible status, export. **Fabricated:** productivity scores.
- **Sector slop:** D04 productivity dashboards, D03 card soup for tasks, D10 toasts on every check-off, D09 FAB on iOS.
- **Tendencies:** capture in ≤ 1 tap, identical row anatomy, keyboard and gesture shortcuts, minimal color. **Break it** when the brand needs to be remembered, by adding one signature interaction (Things' magic plus).
- **Critical states:** sync conflict, offline edits pending, empty project, overdue, undo after delete.

### Social / community
- **Feel / do:** belonging and expression. Browse, post, react, talk.
- **Expr** 3–5 · **Density** medium · **Dir** 5, 9, 8.
- **Legitimate trust:** real people and identities, moderation visible, safety tools. **Fabricated:** fake activity ("12 people are viewing"), bot-inflated counts.
- **Sector slop:** D25 badge confetti, D27 gamified engagement, D18 entrance animation on every post, F07 icon-only actions.
- **Tendencies:** content first, the UI recedes, reactions are fast and tactile. **Break it** for professional communities, where calm and density help.
- **Critical states:** post failed/pending upload, content removed, blocked user, empty feed for a new user (not fake content), slow network media.

### Messaging
- **Feel / do:** instant, private, reliable. Read, reply, share.
- **Expr** 1–3 · **Density** medium · **Dir** 4, 1.
- **Legitimate trust:** encryption stated plainly, delivery/read states, verified contacts. **Fabricated:** security theatre badges.
- **Sector slop:** D24 cross-platform chrome, D05 glass bubbles, heavy D19 motion on send.
- **Tendencies:** platform-native, bubble anatomy rigorous, keyboard-safe composer (F09). **Break it** rarely, since messaging is muscle memory.
- **Critical states:** sending / sent / delivered / read / failed with retry; offline queue; long messages and links; attachment uploading; deleted message.

### Marketplace / commerce
- **Feel / do:** confident choice and frictionless purchase. Discover, compare, buy, track.
- **Expr** 2–4 · **Density** medium · **Dir** 5, 14, 4.
- **Legitimate trust:** real reviews with counts and distribution, return policy, delivery estimates, total price before checkout. **Fabricated:** fake scarcity ("Only 2 left!"), fake reviews (F01), countdown timers.
- **Sector slop:** D25 sale badges everywhere, D21 onboarding, D03 identical product cards with unequal information, D22 hype copy.
- **Tendencies:** consistent card metadata order (price position never moves), sticky purchase action, real media. **Break it** for luxury: Gallery Whitespace or Luxe Restraint.
- **Critical states:** out of stock, price changed in cart, payment declined, address invalid, order delayed/partially shipped, refund pending.

### Travel
- **Feel / do:** prepared and calm under pressure. Search, book, travel day, change plans.
- **Expr** 2–4 · **Density** medium · **Dir** 1, 11, 5.
- **Legitimate trust:** live status, total price incl. fees, change/cancel rules upfront. **Fabricated:** urgency banners.
- **Sector slop:** D07 stock destination imagery, D25 deal badges, missing live states.
- **Tendencies:** the travel day is a different app: glanceable, large type, offline-ready boarding pass. **Break it** in inspiration and planning, where expression can rise.
- **Critical states:** delay, gate change, cancellation with rebooking, offline at destination, timezone changes, boarding pass without network.

### Media / streaming / music
- **Feel / do:** immersed. Find something, play, continue.
- **Expr** 3–5 · **Density** low · **Dir** 8, 5.
- **Legitimate trust:** accurate metadata, honest availability per region. **Fabricated:** fake "trending" lists.
- **Sector slop:** text over artwork without scrim (F03), D05 glass everywhere, autoplay noise.
- **Tendencies:** dark-first, content-sampled color, shared-element transitions, continue-watching as the anchor. **Break it** for audiobooks and podcasts: Editorial Serif and readable chapters.
- **Critical states:** downloading/downloaded/expired, region-locked, playback error with retry, casting/AirPlay, offline library.

### News / reading
- **Feel / do:** informed and respected. Scan headlines, read, save.
- **Expr** 2–3 · **Density** medium · **Dir** 2, 14.
- **Legitimate trust:** bylines, timestamps, corrections, sources, clearly labelled opinion vs reporting. **Fabricated:** engagement bait.
- **Sector slop:** D22 clickbait copy, D25 "BREAKING" badges as decoration, cramped measure.
- **Tendencies:** type-led hierarchy, comfortable measure, reader controls (text size, theme). **Break it** for live events (election night): data and Swiss precision.
- **Critical states:** article updated, paywall (honest), offline saved, live blog refresh, retracted article.

### Devtools / technical
- **Feel / do:** precise and fast. Monitor, triage, deploy, read logs.
- **Expr** 1–3 · **Density** high · **Dir** 6, 1, 4.
- **Legitimate trust:** exact timestamps, IDs, real status, links to source. **Fabricated:** "AI health score".
- **Sector slop:** D13 fake terminal costumes (monospace caps everywhere), D26 neon on black, D04 dashboard tiles.
- **Tendencies:** monospace only for code and IDs, status color plus shape, dense but tappable rows. **Break it** for onboarding new developers: friendlier explanation layers.
- **Critical states:** incident active, partial outage, stale data with timestamp, permission denied, long-running job progress, log truncation.

### Kids
- **Feel / do:** joyful, safe, capable. Play, learn, create.
- **Expr** 4–5 · **Density** low · **Dir** 9, 7.
- **Legitimate trust (for parents):** parental gate, privacy clarity, no dark patterns. **Fabricated:** ads disguised as content.
- **Sector slop:** D07 generic mascots, manipulative D27 rewards, text-heavy screens for pre-readers.
- **Tendencies:** huge targets (64+), audio and visual instructions, few colors used boldly, no time pressure. **Break it** for the parent area, which should be Quiet Native.
- **Critical states:** parental gate, offline play, progress saved, accidental exit, content locked behind purchase (parent-only).

### B2B field apps (service, inspection, logistics)
- **Feel / do:** efficient under real conditions. Next job, capture evidence, complete, sync.
- **Expr** 1–2 · **Density** medium · **Dir** 11, 6, 4.
- **Legitimate trust:** sync status, audit trail, timestamps, GPS accuracy shown honestly. **Fabricated:** productivity gamification.
- **Sector slop:** D23 web dashboards squeezed onto phones, thin type, tiny targets (F05), gesture-only actions.
- **Tendencies:** glove-sized targets, offline-first with explicit queue, camera and scan as primary inputs, high contrast. **Break it** essentially never.
- **Critical states:** offline queue with N pending, sync failed for one item, form partially complete, photo upload failed, job reassigned, low battery.

### Mobility / maps / delivery
- **Feel / do:** oriented, informed of ETA, safe. Request, wait, ride/track, pay.
- **Expr** 2–4 · **Density** medium · **Dir** 1, 11, 5.
- **Legitimate trust:** live position, driver/courier identity, upfront price, safety tools. **Fabricated:** fake ETAs and "searching nearby" theatre.
- **Sector slop:** cluttered map overlays, D10 dialogs over the map, small ETA text.
- **Tendencies:** the map is the canvas, a bottom sheet holds the state, ETA in display type. **Break it** for brand moments (order confirmed) with Mono-Accent flood.
- **Critical states:** no drivers, driver cancelled, location permission denied, GPS inaccurate, route changed, payment failed after the ride.

---

## Choosing when the product spans sectors
Pick the sector of the **riskiest moment**, not the most common one. A
social fitness app that also takes payments needs fintech rigor on the payment
screens and sport energy elsewhere. State this split in KDL `screens[].job`
and keep the system shared.

## Transit / timetables / departures
- **Need**: in 1–2 seconds, walking, one hand: "when is my next departure, can I make it, is anything broken on my line?". Trust in the data's freshness matters as much as the data.
- **Expression**: 1–3. Density medium. The map is *not* the canvas for departures (a walking rider doesn't need it); board/list first, map as a secondary action.
- **Legitimate trust**: live vs timetable distinguished per departure; "updated hh:mm" always visible; offline = last board kept, clearly marked estimated; official line colors and names.
- **Fabricated trust (refuse)**: fake "on time" when no realtime data exists; hiding staleness.
- **Signature opportunities**: walk-aware minutes (only departures you can reach), condensed tabular numerals, mode shapes for line badges (shape + color, not color alone).
- **Sector slop**: map-first home for a departures app; disruption banners for the whole network (filter to lines on screen); red line colors confused with closures; centered spinners on every refresh (keep the board, update in place).
- **Critical states**: no realtime (timetable only), last departure / end of service, closure with alternative, stop moved, location denied (saved stops first), offline underground, stale data, first run with no saved stops, very long stop names.
- **Colors**: line colors are data (color.md §8b). The chrome is *quiet*, not colorless: tinted neutrals (warm or cool, decided by the thesis) plus **one chromatic accent with one meaning** (interactive, or live). A black-and-grey chrome with black buttons was judged generic by blind critics twice — don't. Status hues stay distinguishable from the network palette.
- **Header**: a glance screen spends its top on *answers*, not a page label: location + live status + a one-line summary of disruptions that affect the user. No large "Departures" title.
- **Disruptions**: a summary scoped to the user at the top ("Affects your trip to Work", "At your closest stop") with the alternative; delays shown inline on the affected rows (amber minutes, "6 min late"); network-wide noise collapsed to one line.
- **Order**: rows ordered by the first catchable departure, not by line number.
- **Trust in every number**: stale and offline times must *look* different on the number itself (dimmed, "~", "sched."), and be recomputed from the timestamp — never show a 9-minute-old "2 min" at full weight.
