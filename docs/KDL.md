# KDL — Kinetic Design Language (v1)

KDL is the language in which Kinetic *thinks out loud in a checkable form*.
One file per product, `.kinetic/design.kdl`, holds every design decision from
the thesis to the last state of the last button. Prose explains; KDL decides.

Design goals, in priority order:
1. **Force decisions.** Every field is a decision a senior designer would make
   consciously. Empty fields are visible gaps, not silent defaults.
2. **Make decisions traceable.** `because:` links a choice to the thesis,
   the user moment or a constraint. A choice without a reason is a smell.
3. **Make decisions checkable.** `kinetic validate` verifies completeness,
   references, contrast, grid, type ramp, state coverage and motion hygiene.
4. **Stay stack-neutral.** The same file exports to Flutter, SwiftUI, Compose,
   React Native and CSS (`kinetic export`).
5. **Stay cheap for a model.** Indented key/value text; no braces soup.

## Syntax (strict YAML subset)

- Mappings `key: value`, nested by **2-space** indentation.
- Lists `- item`; list of maps `- id: home` followed by indented keys.
- Inline lists `[a, b, c]` and flat inline maps `{size: 17, line: 22}`.
- Scalars: bare or quoted strings, integers, decimals, `true`/`false`, `null`.
- Literal blocks with `|` for multi-line prose.
- Prose in inline maps may contain commas and apostrophes (`{need: see every member's balance, then settle}`);
  a quote only opens a string at the start of a value. Quote a value to be explicit.
- Comments: `#` at line start, or ` # ` after a value. **Hex colors may be bare**
  (`accent: #3D5AFE`): a `#` directly followed by a hex digit is a value.
- Token references: `$group.name` (e.g. `$color.accent`, `$type.body`,
  `$space.l`, `$radius.m`, `$spring.snappy`, `$duration.quick`, `$haptic.confirm`).
- `n/a: reason` marks a deliberately absent item (e.g. `offline: n/a: no network`).

## Top-level sections

| Section | Purpose | Required for modes |
|---|---|---|
| `kdl` | Version, always `1` | all |
| `mode` | create · improve · redesign · audit · system · design-to-code · code-to-design · evolve | all |
| `product` | Product truth and usage context | all |
| `requirements` | Every must-have of the brief, traced to screens | create, redesign |
| `thesis` | The idea the design must embody | create, redesign, system, improve |
| `expression` | Expression level 1–5 and its reasons | create, redesign, system |
| `audit` | Existing design DNA and classification | redesign, audit, code-to-design, improve |
| `directions` | ≥3 divergent directions, one chosen | create, redesign |
| `journeys` | Simulated user walk-throughs | create, redesign |
| `system` | Tokens: type, color, space, shape, elevation, icon, motion, haptics | create, redesign, system, design-to-code |
| `screens` | Per-screen hierarchy, components, states, motion | create, redesign, improve, design-to-code |
| `signature` | The one memorable detail | create, redesign |
| `premortem` | Where this could fail or read as slop, and the fix | create, redesign, improve, system |

### `product`
```yaml
product:
  name: Lune
  stack: flutter            # flutter | swiftui | compose | react-native | web
  platforms: [ios, android]
  users: adults with irregular sleep who want to understand it, not optimise it
  moment: in bed, lights off, half-awake, one hand, 20–60 seconds
  frequency: daily          # continuous | daily | weekly | occasional | rare
  stakes: low               # low | medium | high   (cost of a wrong decision in the app)
  density: low              # low | medium | high
  brand:
    status: none            # none | loose | strict
    colors: []
    fonts: []
  facts:
    - sleep data comes from HealthKit / Health Connect
  unknowns:
    - whether a partner mode is planned
```

### `requirements` (brief coverage)
```yaml
requirements:
  - {id: R1, need: see last night's sleep at a glance, priority: must, above_fold: true, element: numeral}
  - {id: R3, need: set tonight's bedtime, priority: must}
```
Screens declare `serves: [R1, R3]`. The validator flags any `must` served by no
screen (K21) and an `above_fold` element placed after #4 in `reading_order`.
A strong idea never excuses a dropped requirement — the A/B evaluation showed
exactly that failure (saved stops pushed below the fold).

### `thesis`
```yaml
thesis:
  statement: The app you open half-asleep that reassures without waking you.
  feel: [calm, held, unhurried]
  never: [performance dashboard, gamified streaks, bright clinical white]
  spine: the light goes down       # one generative idea
  spine_expressions:
    layout: content sinks toward the bottom of the screen as bedtime approaches
    color: palette shifts warmer and darker with the real clock
    motion: everything slows and softens at night
```
Validator warnings: statement shorter than 6 words; statement made of generic
words (seamless, modern, clean, intuitive, sleek, beautiful, user-friendly…);
missing `never`; missing `spine`.

### `expression`
```yaml
expression:
  level: 2                  # 1 precise … 5 expressive
  because: low stakes but used at night in a fragile state; calm beats spectacle
  factors: {stakes: low, frequency: daily, density: low, brand_freedom: high}
```
The level sets budgets the validator enforces:

| Level | Saturated accents | Type families | Motion signature moments | Display size max |
|---|---|---|---|---|
| 1 | 1 | 1 | 0–1 | 34 |
| 2 | 1 | 1–2 | 1–2 | 40 |
| 3 | 2 | 2 | 2–3 | 48 |
| 4 | 3 | 2 | 3–5 | 64 |
| 5 | 4 | 3 | unlimited, still purposeful | 96 |

### `audit` (existing products)
```yaml
audit:
  source: lib/                     # what was read
  dna: .kinetic/dna.json           # output of `kinetic dna`
  keep: [warm off-white background, the sleep-phase chart]
  evolve: [type ramp has 11 sizes → 7]
  replace: [purple→blue gradient header]
  remove: [greeting card "Good evening, Sam 👋"]
```

### `directions`
```yaml
directions:
  - id: A
    name: Night paper
    axes: {structure: single column narrative, density: airy, color: warm dark monochrome,
           type: large light serif numerals, motion: slow breath}
    scores: {product_fit: 5, distinctiveness: 4, usability: 5, feasibility: 5, risk_of_slop: 1}
    verdict: chosen
    because: matches half-asleep moment; numerals carry the data without charts
  - id: B
    name: Sky instrument
    verdict: rejected
    because: precise but cold; reads as a performance dashboard (thesis.never)
  - id: C
    name: Soft garden
    verdict: rejected
    because: illustration-dependent; images are out of scope; risk of whimsy slop
```
Rules: ≥3 directions; exactly one `chosen`; every direction has `because`;
directions must differ on ≥3 axes (the validator compares axis strings).

### `journeys`
```yaml
journeys:
  - id: check-last-night
    steps:
      - {screen: tonight, intent: glance at last night, risk: bright screen wakes user}
      - {screen: night-detail, intent: understand a bad night, risk: data shown without meaning}
```

### `system`
```yaml
system:
  type:
    families: {display: New York, text: SF Pro Text, numeric: SF Pro Rounded}
    scale:                           # size/line in pt (dp/sp), track in em
      display: {size: 40, line: 44, weight: 300, track: -0.02, numerals: tabular}   # optional width: condensed | compressed | expanded
      title:   {size: 22, line: 28, weight: 600, track: -0.01}
      body:    {size: 17, line: 24, weight: 400, track: 0}
      caption: {size: 13, line: 18, weight: 500, track: 0.01}
    dynamic: true                    # scales with user text size
  color:
    seed: "#C9A27E"
    strategy: monochrome-warm        # monochrome | analogous | complementary | brand-led | neutral+accent
    roles:
      light:
        bg: "#F6F1EA"
        surface: "#FFFFFF"
        text: "#1E1A16"
        text-2: "#5C5249"
        border: "#E4DAD0"
        accent: "#8A5A2B"
        on-accent: "#FFFFFF"
        danger: "#B3261E"
      dark:
        bg: "#0F0D0B"
        surface: "#1A1714"
        text: "#EDE6DE"
        text-2: "#A89C90"
        border: "#2C2722"
        accent: "#D9A877"
        on-accent: "#1E1408"
        danger: "#F2B8B5"
  space:
    unit: 4
    scale: {xs: 4, s: 8, m: 12, l: 16, xl: 24, 2xl: 32, 3xl: 48}
    margins: {compact: 20, regular: 24}
  shape:
    corner: continuous               # continuous | circular
    radius: {s: 8, m: 14, l: 22, full: 999}
  elevation:
    strategy: tonal                  # tonal | shadow | border | none
  icon:
    family: sf-symbols               # sf-symbols | material-symbols | custom | phosphor | lucide
    style: outline                   # outline | fill | duotone
    selected: fill                   # how selection is shown
    sizes: [17, 22]
    weight: regular
  motion:
    personality: unhurried, damped, never bouncy
    springs:
      gentle: {response: 0.55, damping: 1.0}
      settle: {response: 0.4, damping: 0.9}
    durations: {fade: 220, slow: 600}
    reduce: crossfade                # crossfade | instant | keep-feedback-only
  haptics:
    select: selection
    confirm: soft
    error: warning
```
Data colors (transit lines, categories, chart series, avatar tints) are **not** roles and
don't count against the accent budget: put them in `system.color.data`
(`{T2: "#2E7D4F", M1: "#1F5FAF"}`), give each a text color that passes on it,
and never reuse a status hue (red/amber/green) for data unless it means status.
Accepted forms: `name: "#hex"`, `{fill, on, fill_dark, on_dark}` or `{light, dark, on, on_dark}`.
`kinetic scan` exempts these hex values from the color-chaos counts, and `export` emits them (`KData`, `Color.kData…`, `--k-data-…`).

Required roles in both `light` and `dark`: `bg surface text text-2 border accent on-accent`.
Checked contrast pairs (WCAG 2.x, plus APCA Lc reported): `text/bg ≥ 4.5`,
`text/surface ≥ 4.5`, `text-2/bg ≥ 4.5`, `text-2/surface ≥ 4.5`,
`on-accent/accent ≥ 4.5`, `accent/bg ≥ 3.0`, `danger/bg ≥ 3.0`, `text-3/bg ≥ 3.0`.

### `screens`
```yaml
screens:
  - id: tonight
    job: tell me at a glance whether last night was ok
    network: false
    primary: last night's duration as a single numeral
    secondary: one sentence that interprets it
    reading_order: [numeral, interpretation, week strip, settings]
    serves: [R1, R3]
    thumb: [bedtime button]        # what the thumb reaches in the bottom third
    components:
      - id: duration
        kind: numeral                 # see component kinds below
        type: $type.display
        fg: $color.text
        bg: $color.bg
      - id: week-strip
        kind: chart
        role: compare tonight with the last 7 nights
        env: {on: $color.surface, near: [interpretation], density: low}
      - id: log-button
        kind: button
        fg: $color.on-accent
        bg: $color.accent
        target: 48
        variants: [default, pressed, disabled, loading]
        haptic: $haptic.confirm
    states:
      content: numeral + interpretation + strip
      loading: n/a: data is local and synchronous
      empty: first night — explain what will appear tomorrow, no fake zeros
      error: Health permission revoked — say so and offer to reconnect
      offline: n/a: no network
      overflow: 7-digit locale strings and Dynamic Type XXL keep numeral on one line
      first-run: n/a: covered by onboarding
    motion:
      - id: numeral-enter
        kind: signature               # feedback | transition | signature (only signature counts against the budget)
        trigger: screen appears
        change: numeral settles 8pt upward and fades in
        spring: $spring.gentle
        reduce: crossfade
        interruptible: true
```
Component kinds: `text numeral button icon-button link field toggle chip tab
row list card sheet dialog chart media badge progress nav-bar tab-bar toolbar`.
Interactive kinds (`button icon-button link field toggle chip tab row`) must
declare `variants` including `pressed` and `disabled`, and `target ≥ 44`.
Any component with both `fg` and `bg` color references gets a contrast check.
Required screen states: `content loading empty error` (+ `offline` when
`network: true`). Each is either described or `n/a: reason`.
Each motion entry needs `trigger`, `change`, `spring` or `duration`, `reduce`.
`kind` defaults to `transition`; the expression budget limits only `signature` moments.
New screens: `kinetic states template <id> --block` prints a paste-ready block.

### `signature`
```yaml
signature:
  what: the background tint follows the real clock between 20:00 and 02:00
  where: [tonight]
  because: makes the spine (the light goes down) literal without decoration
```

### `premortem`
```yaml
premortem:
  - risk: warm dark palette reads as generic "luxury" brown
    rule: D14
    fix: keep chroma low, let the numeral carry identity, no gold
```

## Validation output
`kinetic validate .kinetic/design.kdl --json` returns
`{ok, mode, findings:[{id, tier, severity, path, message, fix, evidence}], coverage}`.
`tier`: F (refuse), D (reject by default), C (conditional), I (info).
`evidence`: always `derived` for KDL checks (computed from your own decisions).
