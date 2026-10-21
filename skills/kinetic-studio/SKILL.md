---
name: kinetic-studio
description: "Kinetic's multi-agent design studio for mobile apps: runs the work as a team in fresh contexts — three directors develop dealt directions in parallel, a rival builds the category standard, an editor cuts clutter, and a panel of three critics with different lenses judges the renders blind — with the engine merging their judgments. Use for create/redesign at screen or product depth when you can launch sub-agents, or when the user asks for the best possible result."
---

# The studio: many minds, one decision record

> Paths are relative to the Kinetic plugin root (two directories above this file). The engine is `<root>/bin/kinetic`, written `kinetic` here. Read the `kinetic` router first; this skill replaces its single-author loop when sub-agents are available.

One model in one context converges: it anchors on its first idea, it grades
its own work leniently, and it cannot see its own clutter. A studio fixes all
three with **separate contexts that never see each other's reasoning**, and
an engine that merges what they return. You are the **lead**: you own the
brief, the choices, the build and the record; the agents own divergence,
removal and judgment.

## The team (agents/)
| Role | Agent | Runs | Sees | Returns |
|---|---|---|---|---|
| Director ×3 | kinetic-director | in parallel, one per dealt option | brief, inventory, ONE option | that option developed: idea, competitor test, first viewport, vocabulary, live thing, scores |
| Rival | kinetic-rival | in parallel with the directors | brief only | the category-standard home (what to beat) |
| Editor | kinetic-editor | after each build | renders + contract | a ranked cut list + clarity |
| Critic ×3 | kinetic-critic | in parallel, different lenses | renders, KDL, rival | protocol JSON each |
| Forensics | kinetic-forensics | redesign/improve only | the existing code | style DNA, KEEP/EVOLVE/REPLACE/REMOVE |

Launch parallel agents **in one message** (several Agent calls at once).
Give each agent file paths, not your opinions: the value is the fresh context.
Agents return their work as text; you save it to the files named below (some roles are read-only).

## Protocol
1. **Brief** (you): kinetic-think → `product`, `requirements`, `thesis`,
   `inventory`, `expression`, `journeys` in `.kinetic/design.kdl`. Then sketch
   **your authored direction A** in the KDL (`source: author`) *before* reading
   any deal, and only then `kinetic deal --brief-file <brief> --options 2`.
2. **Diverge** (parallel): 3 × kinetic-director — director 1 develops **your
   authored direction A** (you wrote its thesis-led sketch in the KDL), directors
   2 and 3 each "develop dealt challenger N only" (`kinetic deal --options 2`) —
   with paths to the brief, KDL and `.kinetic/deal.json`; and 1 × kinetic-rival. Save their outputs to `.kinetic/studio/director-N.md`
   and `.kinetic/studio/rival.md`.
3. **Choose** (you): put the three developed directions in KDL `directions`,
   apply the rule (most distinctive viable, K30), write `vocabulary` and the
   `contract`. The rival's "what it gets right" becomes your floor; its
   home becomes what you must beat on distinctiveness.
4. **Build** (you): kinetic-states → kinetic-system → kinetic-code, with
   `knowledge/clarity.md` budgets from the first screen. Render every state.
5. **Edit** (agent): kinetic-editor on the renders → apply the cut list
   unless a cut would lose a `must`, an alert action or the last vocabulary
   site. Re-render. `kinetic clarity` ≥ 85 on key states, no `void_pt` > 130.
   Then the **craft floor** (kinetic-craft items 17–20): colour, type and
   layout floors and the render audit — the points blind critics docked
   Kinetic for in rounds 7–9 (colour 3.4, layout 3.6). The panel should never
   be the first to see them.
6. **Judge** (parallel): 3 × kinetic-critic, each with one **lens** stated in
   its prompt, all with the same renders, `kinetic sheet` contact sheet and
   the rival sketch:
   - lens **product**: product_fit, hierarchy, anticipation, copy first;
   - lens **identity**: distinctiveness, typography, color, cover-the-logo vs the rival;
   - lens **clarity & craft**: layout_craft, native_fidelity, clarity budgets, squint/silence.
   Every critic still scores all dimensions. Save `.kinetic/studio/loopN/critic-{product,identity,clarity}.json` (one folder per loop), then
   `kinetic panel .kinetic/studio/loopN/critic-*.json --out .kinetic/critique.json`.
   Render **both platforms**: at least the default state as an Android
   variant (Material navigation, sheets, buttons) beside iOS — native
   fidelity was 3/5 for every arm that rendered only one platform.
   From loop 2 on, every critic also receives the previous loop's
   `panel.json` and your `loopN/lead.md` (what you fixed, what you declined
   and why): their first job is to **verify those fixes**, then score. A fix
   reversed by a later critic needs a reason that names the earlier one.
7. **Iterate** (you): fix the panel's consensus fixes and every dimension
   with a median < 4 or a split (disagreement ≥ 2) — splits mean the render
   is ambiguous, not that one critic is wrong. Re-render → editor → panel.
   Max 3 loops; stop when two loops don't raise the median mean. The **last
   loop ends with a panel** on the final renders (fix → render → panel → stop):
   never ship fixes nobody judged.
8. **Prove**: `kinetic score --kdl .kinetic/design.kdl --code <src> --renders <shots> --judged .kinetic/critique.json`.
   An independent panel can reach `ship`; clarity < 70 blocks it.

## Rules for the lead
- Never show an agent another agent's output unless the protocol says so
  (directors don't see each other; critics don't see the editor's list).
- Never edit a critique. Disagree in the record (`because`), not in the JSON.
- Keep the studio's files: `.kinetic/studio/` is the audit trail of how the
  design was decided.
- Without the Agent tool, run the same protocol yourself in order, writing
  each role's output to its file before reading the next role's inputs, and
  mark the critique `self_judged`.
