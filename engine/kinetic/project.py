"""Project setup and configuration (.kinetic/).

`init` creates `.kinetic/config.json` and a mode-specific `design.kdl`
skeleton. It never overwrites an existing design record or any user file
(PRODUCT.md, DESIGN.md, themes) unless `force` is passed for `.kinetic/` only."""
from __future__ import annotations

import json
import os
import re

CONFIG = "config.json"
DEFAULT = {"stack": None, "platforms": ["ios", "android"], "grid": 4, "theme_paths": [], "hook": True,
           "hook_tiers": ["F", "D"], "hook_min_severity": "major"}


def find_root(start: str):
    cur = os.path.abspath(start if os.path.isdir(start) else os.path.dirname(start))
    while True:
        if os.path.isdir(os.path.join(cur, ".kinetic")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def load_config(start: str = ".") -> dict:
    root = find_root(start)
    cfg = dict(DEFAULT)
    if root:
        try:
            with open(os.path.join(root, ".kinetic", CONFIG), encoding="utf-8") as fh:
                cfg.update(json.load(fh))
        except (OSError, ValueError):
            pass
        cfg["root"] = root
    return cfg


def detect_stack(path: str) -> tuple[str, list]:
    def exists(*p):
        return os.path.exists(os.path.join(path, *p))

    if exists("pubspec.yaml"):
        plats = [p for p in ("ios", "android") if exists(p)] or ["ios", "android"]
        return "flutter", plats
    if exists("package.json"):
        try:
            with open(os.path.join(path, "package.json"), encoding="utf-8") as fh:
                pkg = fh.read()
        except OSError:
            pkg = ""
        if re.search(r"\"(react-native|expo)\"", pkg):
            return "react-native", ["ios", "android"]
        return "web", ["web"]
    for dp, dns, fns in os.walk(path):
        dns[:] = [d for d in dns if not d.startswith(".") and d not in ("Pods", "build", "node_modules", "DerivedData")]
        if any(f.endswith(".xcodeproj") for f in dns) or "Package.swift" in fns:
            return "swiftui", ["ios"]
        if any(f in fns for f in ("build.gradle.kts", "build.gradle")):
            return "compose", ["android"]
        if dp.count(os.sep) - path.count(os.sep) > 2:
            dns[:] = []
    return "mixed", ["ios", "android"]


SKELETON = """# Kinetic design record — see docs/KDL.md in the plugin. Fill every TODO;
# `kinetic validate .kinetic/design.kdl` lists what is missing or incoherent.
kdl: 1
mode: {mode}

product:
  name: {name}
  stack: {stack}
  platforms: [{platforms}]
  users: TODO who, precisely
  moment: TODO where, when, posture, attention, duration of a typical use
  frequency: TODO continuous | daily | weekly | occasional | rare
  stakes: TODO low | medium | high
  density: TODO low | medium | high
  brand:
    status: TODO none | loose | strict
    colors: []
    fonts: []
  facts: []
  unknowns: []

thesis:
  statement: TODO one sentence that could not describe another app
  feel: [TODO]
  never: [TODO]
  spine: TODO one generative idea
  spine_expressions:
    layout: TODO
    color: TODO
    motion: TODO

expression:
  level: 3
  because: TODO stakes, frequency, density, brand freedom
{audit}{create}
premortem:
  - risk: TODO
    rule: TODO
    fix: TODO
"""

CREATE = """
requirements:   # every must-have of the brief; screens reference them in `serves`
  - {id: R1, need: TODO, priority: must, above_fold: false}

directions:
  - id: A
    name: TODO
    axes: {structure: TODO, density: TODO, color: TODO, type: TODO, motion: TODO}
    scores: {product_fit: 3, distinctiveness: 3, usability: 3, feasibility: 3, risk_of_slop: 3}
    verdict: chosen
    because: TODO
  - id: B
    name: TODO
    axes: {structure: TODO, density: TODO, color: TODO, type: TODO, motion: TODO}
    verdict: rejected
    because: TODO
  - id: C
    name: TODO
    axes: {structure: TODO, density: TODO, color: TODO, type: TODO, motion: TODO}
    verdict: rejected
    because: TODO

journeys:
  - id: TODO
    steps:
      - {screen: TODO, intent: TODO, risk: TODO}

system:
  type:
    families: {display: TODO, text: TODO}
    scale:
      title: {size: 22, line: 28, weight: 600, track: -0.01}
      body: {size: 17, line: 24, weight: 400, track: 0}
      caption: {size: 13, line: 18, weight: 400, track: 0.01}
    dynamic: true
  color:
    seed: "TODO run: kinetic palette <seed> --kdl"
  space:
    unit: 4
    scale: {xs: 4, s: 8, m: 12, l: 16, xl: 24, 2xl: 32}
  shape:
    corner: continuous
    radius: {s: 8, m: 12, l: 20, full: 999}
  elevation:
    strategy: tonal
  icon:
    family: TODO
    style: outline
    selected: fill
  motion:
    personality: TODO
    springs:
      settle: {response: 0.4, damping: 0.9}
    durations: {quick: 150, standard: 250}
    reduce: crossfade
  haptics:
    select: selection

screens: []   # add screens with: kinetic states template <id> --block (set `serves` and `thumb`)

signature:
  what: TODO
  where: [TODO]
  because: TODO
"""

AUDIT = """
audit:
  source: TODO paths read
  dna: .kinetic/dna.json
  keep: []
  evolve: []
  replace: []
  remove: []
"""


def init(path: str = ".", mode: str = "create", stack: str | None = None, force: bool = False,
         name: str | None = None) -> dict:
    path = os.path.abspath(path)
    kdir = os.path.join(path, ".kinetic")
    os.makedirs(kdir, exist_ok=True)
    detected, plats = detect_stack(path)
    stack = stack or detected
    created, kept = [], []
    cfg_path = os.path.join(kdir, CONFIG)
    if os.path.exists(cfg_path) and not force:
        kept.append(cfg_path)
    else:
        cfg = dict(DEFAULT, stack=stack, platforms=plats)
        with open(cfg_path, "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=2)
        created.append(cfg_path)
    kdl_path = os.path.join(kdir, "design.kdl")
    if os.path.exists(kdl_path) and not force:
        kept.append(kdl_path)
    else:
        if stack in ("swiftui",):
            plats = ["ios"]
        text = SKELETON.format(mode=mode, name=name or os.path.basename(path), stack=stack, platforms=", ".join(plats),
                               audit=AUDIT if mode in ("redesign", "improve", "audit", "code-to-design", "evolve") else "",
                               create=CREATE if mode in ("create", "redesign") else "")
        with open(kdl_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        created.append(kdl_path)
    return {"tool": "init", "root": path, "stack": stack, "platforms": plats, "created": created,
            "kept_existing": kept,
            "effects": ["writes only inside .kinetic/", "the design hook becomes active for this project"]}
