---
name: kinetic-think
description: "Kinetic's reasoning layer: read a mobile product like a senior designer before any styling — product truth, user moment, thesis and anti-thesis, concept spine, expression level, simulated journeys and anticipated failures. Use at the start of any Kinetic create/redesign/improve/system task, or when a mobile design request is vague."
---

# Think before you design

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

Slop is what happens when design starts at the pixel. This module produces
the **design brief** (KDL `product`, `thesis`, `expression`, `journeys`) that
every later decision is checked against. It is short to write and expensive
to skip.

## Step 1 — Read the product (facts before opinions)
Inspect what exists: routes/screens, data models, copy, assets, onboarding,
analytics events, README/PRODUCT.md, store listing text if present. For a
brief, extract its nouns and verbs. Sort everything into:
- **facts** (observed in code/brief), **user statements** (preferences,
  suggested solutions — "use a carousel" is a suggestion, not a requirement),
  **inferences** (yours, labelled), **unknowns** (material ones only).

## Step 2 — The user moment (the most important field)
Answer concretely, as if filming it:
- **Who** exactly (not "users"): role, expertise, emotional state.
- **Where/when**: in bed, on a platform, in a kitchen with wet hands, at a desk between meetings.
- **Posture & attention**: one hand / two, walking / seated, glance (2s) / session (10 min).
- **Frequency**: continuous, daily, weekly, rare. Frequency buys learnability;
  rare use demands self-explanation.
- **Stakes**: what does a wrong tap cost? (money, health, a message to the wrong person, nothing)
- **What they came to do in the first 3 seconds.**

Then read `knowledge/sectors.md` for the sector lens — as context, not as a
palette rule. A sector tells you what must be *legitimately* trustworthy, not what color to use.

## Step 3 — The thesis
One sentence: **who, which moment, what the app does for them, how it should feel**.
- Bad: "A modern, clean and intuitive finance app." (describes ten apps)
- Bad: "Premium experience for managing money." ("premium" is not a decision)
- Good: "The account you check on the bus in five seconds to know whether you can say yes to dinner."
- Good: "The app you open half-asleep that tells you how you slept without waking you up."

Add:
- `feel`: 2–3 precise emotion words (calm, held, brisk, assured, playful, focused) — not adjectives of style.
- `never`: the anti-thesis — what it must never feel like (a dashboard, a casino, a hospital, a to-do list that judges you). The anti-thesis is how you'll recognise slop later.

**Failure tests** — rewrite until all pass:
1. Could this sentence describe a competitor unchanged? → too generic.
2. Does it contain a style adjective (modern, clean, sleek, minimal, premium)? → replace with the situation that implies it.
3. Does it promise a feature that doesn't exist? → remove.
4. Can you point at a screen element and say which word of the thesis it serves? → if not, the thesis is too abstract.

## Step 4 — The concept spine
One generative idea that can drive **layout, color and motion at once**, so
the design has a mind instead of a theme. Techniques to find it:
- **From the moment**: half-asleep → "the light goes down"; on a bus → "one glance, one answer".
- **From the data's nature**: a flight is a line through time → "the journey is a single line"; money is a balance → "level, not dashboard".
- **From the core verb**: log, check, decide, share, learn → what does that verb look like physically?
- **From a material/place** (sparingly): paper, instrument panel, field notebook — only if it connects to the moment.
Write `spine_expressions` for layout, color and motion. If the spine can't
generate all three, it's a decoration, not a spine — find another.

## Step 5 — Expression level (1–5)
Decide from four factors; write `because`:
| Factor | Pushes toward 1–2 (precise) | Pushes toward 4–5 (expressive) |
|---|---|---|
| stakes | money, health, safety, work | entertainment, self-expression |
| frequency | continuous, many times a day | occasional, event-like |
| density | many records, comparison | single focus, content-led |
| brand freedom | strict brand, regulated | new brand, character-driven |
High stakes cap the level at 3 (put expression in details, not chrome).
The level sets budgets (accents, families, signature moments, display size) that `kinetic validate` enforces.

## Step 6 — Journeys: simulate before drawing
For the 2–3 journeys that matter, walk them as the user, screen by screen:
`{screen, intent, risk}`. At each step ask:
- What do I see first? Is it what I need?
- What do I do next, with which thumb?
- What can go wrong here? (no data, slow network, permission denied, wrong input, interruption)
- What do I feel? Does it match `feel` or drift toward `never`?
Every risk becomes a state or a design decision later (kinetic-states).

## Step 7 — Anticipate (the designer's second look)
List what the brief didn't ask for but the product will meet: first run,
empty/no-results, errors and recovery, offline, permissions, 0/1/many items,
longest strings and other languages, XXL text, dark mode at night, small and
large phones, interruptions. These go to `screens[].states` and `premortem`.

## Step 8 — Write it down
`kinetic init` (if no `.kinetic/`), then fill `product`, `thesis`,
`expression`, `journeys` in `.kinetic/design.kdl`. Run `kinetic validate`;
fix every K02/K04/K06 finding in these sections before moving on.

## When to ask the user
Only for unknowns that change the product: target audience, factual claims,
brand constraints, scope. Ask one concise question, propose your default, and
keep working on everything that doesn't depend on the answer. Never push
design decisions (fonts, colors, spacing) back to the user as questions.

## Output (spoken, ≤ 8 lines — docs/PROTOCOL.md §3)
Product · Thesis · Feel / Never · Spine · Level (+ why) · Unknowns.
