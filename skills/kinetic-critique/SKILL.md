---
name: kinetic-critique
description: "Kinetic's reasoning-and-critique system for mobile design: pre-mortem before building, audit of existing apps, independent taste evaluation (measured engine scores + a fresh-context critic agent judging renders against a 10-dimension rubric), gated verdicts (blocked / rethink / iterate / ship) and a continuous improvement loop. Use to review, audit or score a mobile UI, before declaring any Kinetic design done, or when asked 'is this good / premium / ready?'."
---

# Prove it, don't claim it

> Paths below are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Part of the `kinetic` skill's pipeline; read that router first if you arrived here directly.

Two kinds of evidence, never blended: **measured** (engine) and **judged**
(an independent critic looking at renders). The author never grades its own work.

## 1. Pre-mortem (before code, D2–D3)
Imagine the design shipped and was called generic, confusing or broken.
Write the 3–6 most likely reasons into KDL `premortem` with the catalog rule
and the fix (e.g. "warm dark palette reads as luxury brown — D14 — keep chroma
low, no gold"). Re-read it before the critique.

## 2. Measured evidence (engine)
```
kinetic validate .kinetic/design.kdl
kinetic scan <changed or audited paths>
kinetic states code <paths>
kinetic score --kdl .kinetic/design.kdl --code <paths>
```
F findings block everything. Confirm `inferred` findings in code before reporting them.

## 3. Renders (required for judgment)
Capture each key screen: light + dark, default + largest text size, smallest +
largest phone, plus the empty and error states. Tools: the iOS Simulator
control tool (screenshot), `xcrun simctl io booted screenshot <file>`,
`adb exec-out screencap -p > <file>`, `flutter screenshot`, previews. Save
under `.kinetic/shots/` with descriptive names. Motion needs a recording;
otherwise mark motion `unjudged`.

## 4. Judged evidence (independent critic)
Launch the **kinetic-critic** agent with: the path to `.kinetic/design.kdl`,
the render files, the changed source paths, and the instruction to return
docs/PROTOCOL.md §6 JSON. It works in a fresh context and has not seen your
reasoning — that is the point. Save its output to `.kinetic/critique.json`, then:
```
kinetic score --kdl .kinetic/design.kdl --code <paths> --judged .kinetic/critique.json
```

## 5. Verdict and loop
| Verdict | Meaning | Next |
|---|---|---|
| blocked | F(block) findings | fix integrity/function first |
| rethink | product_fit ≤ 2, distinctiveness ≤ 2 or mean < 3 | go back to kinetic-direct; polish won't save it |
| iterate | gates not met | fix the lowest judged dimensions and major D findings, re-render, re-judge |
| ship | all gates pass | report |
**Stop rule**: at most 3 iterate loops; if two consecutive loops don't raise
the judged mean, stop and report the remaining gap honestly, with the
critic's `biggest_lever`.

## 6. Audit mode (no code changes)
Forensics (kinetic-code / kinetic-forensics agent) → states code → renders →
critic → score. Report: verdict, the 3 problems that matter most (with
evidence), what to keep, what to change first, and the expected gain. Use the
catalog IDs so findings are actionable.

## 7. Continuous improvement (`evolve`, projects with `.kinetic/`)
The PostToolUse hook reports F/D drift on every UI edit — fix F immediately,
fix D or record the exception in KDL with `because`. Periodically (after a
feature lands) run `kinetic score` and refresh `.kinetic/critique.json`.
Keep `.kinetic/design.kdl` the source of truth: when the product changes,
change the thesis or system there first, then the code.

## 8. Reporting
Lead with the verdict and the biggest lever; then measured vs judged blocks
in one line each; then the next actions. Never present a single "taste
score"; never claim renders, states or devices you did not inspect.
