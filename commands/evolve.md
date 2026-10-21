---
description: Continue an existing Kinetic project: apply a change inside the recorded thesis and system, keep .kinetic/design.kdl the source of truth
argument-hint: "<the change to make>"
---

Use the `kinetic` skill in **evolve** mode for: $ARGUMENTS

Read and validate .kinetic/design.kdl first; change the decision record before the code; re-export tokens if the system changed; finish with kinetic-critique.

Follow the router's pipeline for this mode and depth, write decisions to `.kinetic/design.kdl` (run `kinetic init --mode evolve` first if the project has no `.kinetic/`), verify with the engine, and report per docs/PROTOCOL.md §7.
