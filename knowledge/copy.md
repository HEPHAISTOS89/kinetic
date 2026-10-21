# Copy — words are interface

Microcopy is the most visible design decision on a screen and the cheapest to
get wrong. Slop copy (vague, cheerful, generic) makes a precise layout read as
a template. Good copy names the thing, states the outcome and sounds like the
product's thesis.

## 1. Voice comes from the thesis

Derive voice from `thesis.feel` and `thesis.never`, not from a generic "friendly":

| Thesis feel | Voice | Example (empty state) |
|---|---|---|
| calm, held, unhurried | short, quiet, no exclamation, present tense | "Your first night will appear here tomorrow morning." |
| precise, trustworthy (fintech) | exact, numeric, neutral, no jokes | "No transactions since 1 Oct." |
| energetic, social | direct, warm, second person, contractions | "No posts yet. Follow a few people to fill this up." |
| expert, dense (pro tool) | terse, domain words, no explanation of basics | "No matches. Clear filters" |

Rules:
- One voice across the app. A playful empty state next to a legalistic error is incoherence.
- Tone may soften in failure and celebrate only real milestones — but the voice stays.
- Write in the user's words, not the database's ("Payment failed", not "TXN_ERR_402").

## 2. Tone by expression level

| Level | Copy behaviour |
|---|---|
| 1 | Neutral, informative, zero personality words. Precision is the personality. |
| 2 | Calm, human, short; one gentle phrase allowed in empty/success states. |
| 3 | Distinct voice in headings and empty states; labels stay plain. |
| 4 | Voice in most surfaces; humor allowed where it costs nothing (empty, success). |
| 5 | Strong voice; still: errors, money, health and legal copy are always plain. |

## 3. Patterns per state

### Buttons and actions
- **Verb + object**: "Save draft", "Send €40", "Add card". Not "OK", "Submit", "Yes".
- The button repeats the outcome the user chose: dialog "Delete 3 photos?" → buttons
  "Delete" / "Cancel", never "Yes" / "No".
- Primary label ≤ 3 words. Same action, same word everywhere ("Remove" vs "Delete" vs
  "Discard" are three different meanings — pick deliberately).
- Destructive actions name the loss: "Delete account", "Discard changes".

### Empty states
Structure: **what will be here** + **how it gets here** + optional single action.
- EN: "No saved places. Tap the bookmark on any place to keep it here."
- FR : « Aucun lieu enregistré. Touchez le signet d'un lieu pour le retrouver ici. »
- First-use empty ≠ cleared empty ≠ no-results empty. No-results names the query and
  offers the recovery: "No results for 'ramen' in Lyon. Try a wider area."
- Never fake zeros as data ("0 h 0 min" for a night not yet recorded).

### Errors
Structure: **what happened** + **why (if known)** + **what to do now**. No blame, no
"Oops", no codes in the headline.
- EN: "Couldn't send your message. You're offline — it will send when you reconnect."
- FR : « Message non envoyé. Vous êtes hors ligne — il partira dès la reconnexion. »
- EN: "Card declined by your bank. Try another card or contact your bank."
- FR : « Carte refusée par votre banque. Essayez une autre carte ou contactez-la. »
- Field validation: say the rule, at the field, when it's violated (on blur or submit,
  not on first keystroke): "Use at least 8 characters" / « Au moins 8 caractères ».
- Recoverable errors get a recovery action ("Retry", "Reconnect Health").

### Loading
- Under ~1s: no copy. Keep previous content or show inline progress.
- 1–5s: state what's happening, specifically: "Checking availability…" / « Vérification des disponibilités… »
- Longer: expectation + permission to leave: "Preparing your export. We'll notify you when it's ready."
- Ellipsis character `…`, not three dots, in progress labels.

### Success
- **Proportional**: a toggle needs no message; a saved draft gets a quiet inline
  "Saved"; a sent transfer gets a confirmation with the facts (amount, recipient,
  time); a real milestone may celebrate.
- Confirm only after the outcome is known (F06).
- Offer the next step or undo instead of a congratulation: "Archived · Undo".

### Permissions
Ask in context, after the user requests the feature, with the benefit in one line:
"Allow notifications to know when your order arrives." — never a cold system prompt
on first launch.

## 4. Numbers, units, dates

- Use the locale's formatter for numbers, currency, dates, units — never string concatenation.
  FR: `1 234,50 €` (narrow no-break space as thousands separator, comma decimal, space before €).
  EN-US: `$1,234.50`.
- Tabular figures for any number that updates or is compared in columns.
- Units: space between number and unit (`7 h 32 min`, `5 km`), no-break space so they never wrap apart.
- Relative dates for recency ("2 min ago", "Yesterday"), absolute for records and money ("12 Oct 2026, 14:05").
- Round to the precision the user can act on: "7 h 30" not "7.512 h".
- Plurals with the platform's plural rules (ICU / `.stringsdict` / `intl` plural) — not `item(s)`.

## 5. Truncation-safe writing

- Front-load meaning: the important word comes first ("Paris · Flight delayed" not
  "Your flight to Paris has unfortunately been delayed").
- Titles must fit at XXL text in one or two lines; if they can't, they are too long.
- Never ellipsize critical content (price, amount, name in a payment) — D28.
- Avoid text in fixed-width chips and buttons that will be translated.

## 6. Localization length

- Budget **+30–40%** length for German and French versus English; up to +50% or more
  for short strings (labels under 10 characters can double).
- Some languages are shorter but taller (CJK) or right-to-left (Arabic, Hebrew):
  mirror layout direction, not icons with meaning (media play stays the same, back arrows mirror).
- Don't concatenate translated fragments; translate whole sentences with placeholders.
- French typography: no-break space before `: ; ! ?` and inside « guillemets »;
  capitalize only the first word of titles (« Paramètres du compte », not « Paramètres Du Compte »).
- English UI: sentence case for buttons and titles in most modern apps; Title Case only
  if it's a deliberate system decision applied everywhere.

## 7. Banned phrases (D22)

The scanner flags these (case-insensitive). Each has a plain replacement.

| Slop | Why it fails | Say instead |
|---|---|---|
| Unlock your potential / Unleash | Promise without content | The concrete outcome: "Plan your week in 2 minutes" |
| Seamless / seamlessly | Unverifiable adjective | What no longer happens: "No re-entering your card" |
| Elevate / elevated | Marketing filler | Delete it |
| Supercharge / turbocharge | Hype | The measurable gain |
| Revolutionize / game-changer | Hype | Delete it |
| Effortless / effortlessly | Unverifiable | The number of steps |
| Next-level / cutting-edge / state-of-the-art | Generic | Name the feature |
| Your journey / embark | Vague | The actual activity |
| Dive in / dive into | Filler | "Start", "Open" |
| Oops! / Uh-oh! / Whoops | Infantilizes the error | State the error plainly |
| Something went wrong (alone) | No cause, no recovery | Cause + action |
| Are you sure? (alone) | No information | Name the consequence: "Delete 3 photos? This can't be undone." |
| Click here / Tap here | Label without meaning | Label the destination |
| Welcome back! as a heading | Greeting as concept (D02) | Lead with content |
| Good morning/afternoon/evening, {name} 👋 | D02 | Lead with today's value |
| Let's get started! / Let's go! | Filler, exclamation | "Continue", "Create account" |
| Amazing / Awesome / Great job! | Disproportionate praise | Proportional confirmation |
| Powered by AI / AI-powered | Feature is not a benefit | What it does for the user |
| Lorem ipsum / placeholder text | Unfinished | Real content |
| Submit | Bureaucratic | Verb + object |
| Simply / just / easily | Condescending when it isn't | Delete it |

French equivalents to flag: « Libérez votre potentiel », « sans effort », « sans
couture/fluide » as filler, « révolutionnaire », « Oups ! », « Une erreur est survenue »
(alone), « C'est parti ! », « Cliquez ici », « Êtes-vous sûr ? » (alone).

## 8. Punctuation and typography in UI
- No exclamation marks in buttons, labels, errors. At most one in a real celebration.
- No trailing period on single-sentence labels, buttons, titles; periods in multi-sentence body text.
- Curly quotes and apostrophes (’ “ ”), real ellipsis (…), en dash for ranges (9–17 h),
  × for dimensions, minus sign − for negative numbers in finance.
- Emoji in copy only at expression ≥ 4 and never as icons or in errors (D06).
