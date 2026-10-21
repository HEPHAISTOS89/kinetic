"""Deal directions from Kinetic's library (knowledge/library/*.json).

A model asked for three directions draws them from its own prior, so they
converge on the category's average. `deal` moves the first draw outside the
model: it deals composition engines (from different families), then a type
system, a palette and a motion personality per option, with a recorded seed.
The model chooses among what was dealt and fuses it with the product's
inventory; changing a dealt slot is a `redraw` that must carry a reason and is
logged in `.kinetic/deal.json`.

Brief words only *weight* the deal (fits +, misfits excluded); they never pick
the answer, so two deals of the same brief with different seeds differ."""
from __future__ import annotations

import json
import os
import random
import re
import time

from . import color

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "knowledge", "library")
SLOTS = ("engine", "type", "palette", "motion")
MIN_REASON = 12


def load_library(lib_dir: str = LIB) -> dict:
    def rd(name, key):
        with open(os.path.join(lib_dir, name), encoding="utf-8") as fh:
            return json.load(fh)[key]
    return {"engine": rd("engines.json", "engines"), "type": rd("type.json", "systems"),
            "palette": rd("palettes.json", "palettes"), "motion": rd("motion.json", "personalities")}


def _words(text: str) -> set:
    return {w for w in re.findall(r"[a-zà-ÿ]+", (text or "").lower()) if len(w) > 2}


def _hits(phrases, words: set) -> int:
    n = 0
    for p in phrases or []:
        toks = [t for t in re.findall(r"[a-zà-ÿ]+", p.lower()) if len(t) > 2]
        if toks and any(t in words or t.rstrip("s") in words or t + "s" in words for t in toks):
            n += 1
    return n


def _weighted(rng: random.Random, items: list, weights: list):
    total = sum(weights)
    if total <= 0:
        return rng.choice(items)
    x = rng.uniform(0, total)
    for it, w in zip(items, weights):
        x -= w
        if x <= 0:
            return it
    return items[-1]


def _pick(rng, pool, words, taken, slot, engine=None):
    cand = [p for p in pool if p["id"] not in taken]
    if not cand:
        cand = list(pool)
    weights = []
    for p in cand:
        w = 1.0 + 1.5 * _hits(p.get("fits"), words)
        if engine is not None:
            # an engine names the slots it works best with
            if slot == "palette" and engine["id"] == "state-field":
                w *= 6.0 if "states" in p else 0.3
            if slot == "motion" and _hits(p.get("fits"), _words(engine["id"] + " " + engine["family"])):
                w *= 2.5
        weights.append(w)
    return _weighted(rng, cand, weights)


def _roles(pal: dict) -> dict:
    roles = color.derive_roles(pal["seed"], pal.get("strategy", "neutral+accent"),
                               neutral_chroma=pal.get("neutral_chroma"), neutral_hue=pal.get("neutral_hue"))
    fields = {"field": pal.get("field", {})}
    fields.update({f"state-{k}": v for k, v in (pal.get("states") or {}).items()})
    for name, f in fields.items():
        for theme in ("light", "dark"):
            fill = f.get(theme) if isinstance(f, dict) else None
            if not fill:
                continue
            inks = [roles[theme]["text"], roles["dark" if theme == "light" else "light"]["text"], "#FFFFFF", "#111111"]
            ground: str = fill
            best = max(inks, key=lambda c: color.wcag(c, ground))
            roles[theme][name] = fill
            roles[theme][f"on-{name}"] = best
    return roles


def _engine_ok(e, words):
    # a misfit named in the brief removes the engine ("no printed artefact" etc. are judged by the model)
    return _hits(e.get("misfits"), words) == 0


def _option(rng, lib, words, taken, families, engine=None):
    if engine is None:
        pool = [e for e in lib["engine"] if _engine_ok(e, words) and e["family"] not in families] \
            or [e for e in lib["engine"] if e["family"] not in families] or lib["engine"]
        engine = _pick(rng, pool, words, taken["engine"], "engine")
    opt = {"engine": engine}
    for slot in ("type", "palette", "motion"):
        opt[slot] = _pick(rng, lib[slot], words, taken[slot], slot, engine)
    for slot in SLOTS:
        taken[slot].add(opt[slot]["id"])
    families.add(engine["family"])
    return opt


def _summary(opt: dict) -> dict:
    e, t, p, m = opt["engine"], opt["type"], opt["palette"], opt["motion"]
    return {
        "engine": {k: e[k] for k in ("id", "name", "family", "device", "shell", "first_viewport",
                                      "vocabulary_slots", "signature_move", "live_thing", "risks") if k in e},
        "type": {k: t[k] for k in ("id", "name", "voice", "display", "text", "ramp", "rule") if k in t},
        "palette": {"id": p["id"], "name": p["name"], "proportion": p.get("proportion"), "rule": p.get("rule"),
                    "roles": _roles(p)},
        "motion": {k: m[k] for k in ("id", "name", "springs", "durations", "haptics", "reduce") if k in m},
    }


def deal(brief: str = "", seed: int | None = None, options: int = 3, exclude=(), lib_dir: str = LIB) -> dict:
    lib = load_library(lib_dir)
    if seed is None:
        seed = int.from_bytes(os.urandom(4), "big")
    rng = random.Random(seed)
    words = _words(brief)
    taken = {s: set(exclude) for s in SLOTS}
    families: set = set()
    opts = []
    for _ in range(max(1, min(options, 5))):
        opts.append(_summary(_option(rng, lib, words, taken, families)))
    return {"tool": "deal", "seed": seed, "brief_words": sorted(words)[:40], "options": opts,
            "standing_exit": "The category standard (what a competent template would ship) is always available "
                             "as an exit if the user asks for it — never recommend it.",
            "history": [], "dealt_at": time.strftime("%Y-%m-%dT%H:%M:%S")}


def redraw(state: dict, option: int, slot: str, reason: str, lib_dir: str = LIB) -> dict:
    if slot not in SLOTS:
        raise ValueError(f"slot must be one of {', '.join(SLOTS)}")
    if not reason or len(reason.strip()) < MIN_REASON:
        raise ValueError("a redraw needs a reason (a product fact or brand constraint, >= 12 characters)")
    if not 1 <= option <= len(state["options"]):
        raise ValueError(f"option must be 1..{len(state['options'])}")
    lib = load_library(lib_dir)
    rng = random.Random(f"{state['seed']}:{len(state['history'])}:{option}:{slot}")
    words = set(state.get("brief_words", []))
    taken = {s: {o[s]["id"] for o in state["options"]} for s in SLOTS}
    cur = state["options"][option - 1]
    if slot == "engine":
        fams = {o["engine"]["family"] for i, o in enumerate(state["options"]) if i != option - 1}
        pool = [e for e in lib["engine"] if e["id"] not in taken["engine"] and e["family"] not in fams and _engine_ok(e, words)] \
            or [e for e in lib["engine"] if e["id"] not in taken["engine"]]
        new = _pick(rng, pool, words, set(), "engine")
    else:
        eng = next(e for e in lib["engine"] if e["id"] == cur["engine"]["id"])
        new = _pick(rng, lib[slot], words, taken[slot], slot, eng)
    full = {"engine": next(e for e in lib["engine"] if e["id"] == cur["engine"]["id"]),
            "type": next(t for t in lib["type"] if t["id"] == cur["type"]["id"]),
            "palette": next(p for p in lib["palette"] if p["id"] == cur["palette"]["id"]),
            "motion": next(m for m in lib["motion"] if m["id"] == cur["motion"]["id"])}
    old = full[slot]["id"]
    full[slot] = new
    state["options"][option - 1] = _summary(full)
    state["history"].append({"option": option, "slot": slot, "from": old, "to": new["id"], "reason": reason.strip(),
                             "at": time.strftime("%Y-%m-%dT%H:%M:%S")})
    return state


def sheet(state: dict) -> str:
    out = [f"Kinetic deal · seed {state['seed']}  (choose among these; redraw a slot only with a stated reason)"]
    for i, o in enumerate(state["options"], 1):
        e, t, p, m = o["engine"], o["type"], o["palette"], o["motion"]
        lt = p["roles"]["light"]
        out += ["", f"── Option {i}: {e['name']} · {t['name']} · {p['name']} · {m['name']}",
                f"  engine   {e['device']}",
                f"  shell    {e.get('shell', '')}"]
        out += [f"  viewport {b}" for b in e.get("first_viewport", [])]
        out += [f"  replaces {', '.join(e.get('vocabulary_slots', []))} with the product's drawn vocabulary",
                f"  signature {e.get('signature_move', '')}",
                f"  live     {e.get('live_thing', '')}",
                f"  type     display iOS {t['display']['ios']} · Android {t['display']['android']} · text {t['text']}",
                f"           ramp {t.get('ramp')} · rule: {t.get('rule', '')}",
                f"  palette  bg {lt['bg']} · text {lt['text']} · accent {lt['accent']} · field {lt.get('field', '-')}"
                f" (on-field {lt.get('on-field', '-')}) · {p.get('proportion', '')}",
                f"  motion   {m['springs']} · haptics {m.get('haptics')} · reduce: {m.get('reduce')}"]
        if e.get("risks"):
            out.append(f"  risks    {'; '.join(e['risks'])}")
    for h in state.get("history", []):
        out.append(f"\nredraw option {h['option']} {h['slot']}: {h['from']} → {h['to']} — {h['reason']}")
    out += ["", "Exit: " + state["standing_exit"]]
    return "\n".join(out)


def save(state: dict, path: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1, ensure_ascii=False)
    return path


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
