"""Taste evaluation engine.

Shape: workflow. It joins two kinds of evidence and never blends them silently:
- MEASURED: deterministic sub-scores computed from `validate`, `scan`, `dna`
  and `states` (each formula is printed in the report);
- JUDGED: rubric scores from an independent critic (agents/kinetic-critic),
  each 1–5 with evidence, validated for shape before use.
A verdict is derived from explicit gates, not from an average."""
from __future__ import annotations

import json
import os

from . import dna as dna_mod
from . import states as states_mod
from . import validate as validate_mod
from .kdl import parse_file
from .scan import scan

JUDGED_DIMENSIONS = {
    "product_fit": "embodies the thesis; serves the user moment",
    "hierarchy": "one primary thing per screen, clear second, calm rest",
    "distinctiveness": "passes the swap test; could not belong to another product",
    "typography": "ramp, measure, rhythm, numerals, optical details",
    "color": "role logic, atmosphere, restraint, both themes designed",
    "layout_craft": "grid, alignment, spacing rhythm, optical corrections, concentric radii",
    "motion": "purposeful, native physics, interruptible, reduce-motion",
    "native_fidelity": "platform conventions honoured where they help the user",
    "anticipation": "states, edge cases, long content, XXL text, errors with recovery",
    "copy": "specific, human, short; voice from the thesis",
}
SEV_POINTS = {"block": 6, "major": 3, "minor": 1, "info": 0}


def _measured(kdl_result, scan_result, dna_result, states_kdl, states_code):
    m, formulas = {}, {}
    all_f = (kdl_result or {}).get("findings", []) + (scan_result or {}).get("findings", []) + \
        (states_code or {}).get("findings", [])
    # inferred findings are hypotheses: they are listed to confirm, never used as gates
    confirmed = [f for f in all_f if f.get("evidence") != "inferred"]
    blocks = [f for f in confirmed if f["tier"] == "F" and f["severity"] == "block"]
    f_major = [f for f in confirmed if f["tier"] == "F" and f["severity"] == "major"]
    m["integrity"] = max(0, 100 - 25 * len(blocks) - 10 * len(f_major))
    formulas["integrity"] = "100 − 25·F(block) − 10·F(major), observed/derived only"
    parts = []
    if dna_result and dna_result.get("coherence_mean") is not None:
        parts.append(dna_result["coherence_mean"] * 100)
    if kdl_result:
        sys_pen = sum(SEV_POINTS[f["severity"]] for f in kdl_result["findings"]
                      if str(f.get("path", "")).startswith("system") and f["tier"] in ("D", "F"))
        parts.append(100 / (1 + sys_pen / 10))
    if parts:
        m["system_coherence"] = round(sum(parts) / len(parts))
        formulas["system_coherence"] = "mean(code DNA coherence×100, 100/(1+system_penalty/10))"
    d_pts = sum(SEV_POINTS[f["severity"]] * (0.5 if f.get("evidence") == "inferred" else 1)
                for f in all_f if f["tier"] == "D")
    files = max(1, (scan_result or {}).get("coverage", {}).get("files_scanned", 1)) if scan_result else 1
    m["slop_density"] = round(100 / (1 + (d_pts / files) / 6))
    formulas["slop_density"] = "100/(1 + (D points per file)/6); major=3, minor=1"
    ratios = [r for r in ((states_kdl or {}).get("coverage", {}).get("ratio"),) if r is not None]
    if not ratios and states_code and states_code.get("screens"):  # code heuristics only when no decision record
        handled = [sum(v for k, v in s["handles"].items() if k != "offline") / 3 for s in states_code["screens"]]
        ratios.append(sum(handled) / len(handled))
    if ratios:
        m["state_coverage"] = round(100 * sum(ratios) / len(ratios))
        formulas["state_coverage"] = "share of required states designed (KDL) / handled (code)"
    a11y_rules = ("F03", "F05", "F07", "F10", "F09")
    a11y = [f for f in confirmed if f["rule"] in a11y_rules]
    contrast = (kdl_result or {}).get("contrast") or []
    pass_rate = (sum(1 for c in contrast if c["ok"]) / len(contrast)) if contrast else 1.0
    m["accessibility_floor"] = max(0, round(100 * pass_rate - 15 * len(a11y)))
    formulas["accessibility_floor"] = "100·contrast_pass_rate − 15·(F03/F05/F07/F09/F10 findings)"
    mot = [f for f in confirmed if f["rule"] in ("F08", "D18", "D19")]
    m["motion_hygiene"] = max(0, 100 - sum({"block": 40, "major": 15, "minor": 6, "info": 2}[f["severity"]] for f in mot))
    formulas["motion_hygiene"] = "100 − 40·F08 − 15·major − 6·minor (D18/D19)"
    to_confirm = [f for f in all_f if f.get("evidence") == "inferred" and f["tier"] == "F"]
    return m, formulas, blocks, to_confirm


def _newest_mtime(paths, exts):
    newest = 0.0
    for root in paths:
        for dp, dns, fns in os.walk(root) if os.path.isdir(root) else [(os.path.dirname(root), [], [os.path.basename(root)])]:
            dns[:] = [d for d in dns if not d.startswith(".") and d not in ("build", "Pods", "node_modules")]
            for f in fns:
                if f.endswith(exts):
                    try:
                        newest = max(newest, os.path.getmtime(os.path.join(dp, f)))
                    except OSError:
                        pass
    return newest


def check_judged(judged: dict) -> tuple[dict, list]:
    """Validate critic JSON (docs/PROTOCOL.md §critic). Returns (scores, problems)."""
    ok, problems = {}, []
    dims = (judged or {}).get("dimensions", {})
    for name in JUDGED_DIMENSIONS:
        d = dims.get(name)
        if d is None:
            problems.append(f"{name}: not judged")
            continue
        s = d.get("score")
        ev = d.get("evidence")
        if not isinstance(s, int) or not 1 <= s <= 5:
            problems.append(f"{name}: score must be an integer 1–5")
        elif not ev or (isinstance(ev, list) and not any(ev)):
            problems.append(f"{name}: score without evidence is ignored")
        else:
            ok[name] = {"score": s, "evidence": ev, "fix": d.get("fix")}
    return ok, problems


def _declared_unjudged(meta) -> set:
    """Dimensions the critic declared unjudgeable, with a reason (e.g. 'motion: no recording')."""
    out = set()
    for item in (meta or {}).get("unjudged", []):
        name = str(item).split(":")[0].strip()
        if name in JUDGED_DIMENSIONS and ":" in str(item):
            out.add(name)
    return out


def verdict(measured, blocks, judged_scores, meta=None):
    reasons = []
    if blocks:
        return "blocked", [f"{len(blocks)} F(block) findings — integrity/function failures ship nothing"]
    low_measured = [k for k, v in measured.items() if v < 70]
    if not judged_scores:
        return "measured-only", ["no valid critic judgment: run the kinetic-critic agent on renders"] + \
            [f"measured {k} < 70" for k in low_measured]
    vals = [v["score"] for v in judged_scores.values()]
    mean = sum(vals) / len(vals)
    pf = judged_scores.get("product_fit", {}).get("score", 0)
    di = judged_scores.get("distinctiveness", {}).get("score", 0)
    if pf <= 2 or di <= 2 or mean < 3:
        return "rethink", [f"product_fit={pf}, distinctiveness={di}, judged mean={mean:.2f}: the direction, not the polish, is wrong"]
    weak = [k for k, v in judged_scores.items() if v["score"] < 3]
    if (meta or {}).get("stale"):
        return "iterate", ["the judgment predates the current renders/code — re-judge before deciding"]
    declared = _declared_unjudged(meta)
    covered = set(judged_scores) | declared
    if not low_measured and mean >= 4.0 and not weak and pf >= 4 and covered >= set(JUDGED_DIMENSIONS):
        pending = sorted(declared - set(judged_scores))
        if (meta or {}).get("self_judged"):
            return "ship-pending", [f"judged mean {mean:.2f} but self-judged: an independent critic must confirm"] + \
                [f"unjudged: {d}" for d in pending]
        if pending:
            return "ship-pending", [f"judged mean {mean:.2f}; verify on device: {', '.join(pending)}"]
        return "ship", [f"judged mean {mean:.2f}, all measured ≥ 70, no dimension < 3"]
    reasons += [f"measured {k} = {measured[k]} < 70" for k in low_measured]
    reasons += [f"judged {k} = {judged_scores[k]['score']} < 3" for k in weak]
    if mean < 4.0:
        reasons.append(f"judged mean {mean:.2f} < 4.0")
    missing = [k for k in JUDGED_DIMENSIONS if k not in judged_scores and k not in declared]
    if missing:
        reasons.append(f"not judged: {', '.join(missing)}")
    return "iterate", reasons


def run(kdl_path=None, code_paths=None, judged_path=None, platforms=("ios", "android"), grid=4) -> dict:
    kdl_result = states_kdl = scan_result = dna_result = states_code = None
    if kdl_path:
        kdl_result = validate_mod.validate_file(kdl_path)
        try:
            states_kdl = states_mod.matrix(parse_file(kdl_path))
        except Exception:  # syntax errors are already in kdl_result
            states_kdl = None
    if code_paths:
        from .project import data_hexes
        scan_result = scan(code_paths, platforms, grid, None, data_hexes(code_paths[0]))
        dna_result = dna_mod.dna(scan_result, grid)
        states_code = states_mod.code(code_paths)
    measured, formulas, blocks, to_confirm = _measured(kdl_result, scan_result, dna_result, states_kdl, states_code)
    judged_scores, problems, meta = {}, [], {}
    if judged_path:
        with open(judged_path, encoding="utf-8") as fh:
            raw = json.load(fh)
        judged_scores, problems = check_judged(raw)
        meta = {"self_judged": bool(raw.get("self_judged")), "unjudged": raw.get("unjudged") or []}
        newest = _newest_mtime(code_paths or [], (".swift", ".dart", ".kt", ".tsx", ".jsx", ".css", ".png"))
        if newest and newest > os.path.getmtime(judged_path) + 1:
            problems.append("judgment is older than the current code/renders: re-run the critic on the new renders")
            meta["stale"] = True
    v, reasons = verdict(measured, blocks, judged_scores, meta)
    # next actions: F first, then the weakest judged dimensions' fixes, then biggest D clusters
    nxt = []
    for f in blocks[:5]:
        nxt.append(f"[{f['rule']}] {f['message']} → {f.get('fix', '')}")
    for k, d in sorted(judged_scores.items(), key=lambda kv: kv[1]["score"])[:3]:
        if d["score"] < 4 and d.get("fix"):
            nxt.append(f"[judged {k}={d['score']}] {d['fix']}")
    all_d = [f for r in (kdl_result, scan_result) if r for f in r["findings"] if f["tier"] == "D" and f["severity"] == "major"]
    for f in all_d[: max(0, 8 - len(nxt))]:
        nxt.append(f"[{f['rule']}] {f['message']} → {f.get('fix', '')}")
    jmean = round(sum(d["score"] for d in judged_scores.values()) / len(judged_scores), 2) if judged_scores else None
    return {
        "tool": "score",
        "verdict": v,
        "reasons": reasons,
        "measured": measured,
        "formulas": formulas,
        "judged": {k: d["score"] for k, d in judged_scores.items()},
        "judged_mean": jmean,
        "self_judged": bool(meta.get("self_judged")),
        "judged_problems": problems,
        "next": nxt,
        "to_confirm": [f"[{f['rule']}] {f.get('file', '')}: {f['message']}" for f in to_confirm],
        "inputs": {"kdl": kdl_path, "code": code_paths, "judged": judged_path},
        "limitations": ["measured scores are about rules and structure, not beauty",
                        "judged scores are only as good as the renders the critic saw",
                        "no single taste number is produced: read the two blocks and the gates"],
    }


def render(r: dict) -> str:
    out = [f"kinetic score — verdict: {r['verdict'].upper()}"]
    for reason in r["reasons"]:
        out.append(f"  · {reason}")
    out.append("measured (deterministic):")
    for k, v in r["measured"].items():
        bar = "█" * int(round(v / 10)) + "·" * (10 - int(round(v / 10)))
        out.append(f"  {k:<20} {v:>3} {bar}   {r['formulas'].get(k, '')}")
    out.append(("judged (SELF — not independent, cannot ship):" if r.get("self_judged") else "judged (independent critic):")
               if r["judged"] else "judged: none")
    for k, v in r["judged"].items():
        out.append(f"  {k:<20} {v}/5  {'●' * v}{'○' * (5 - v)}")
    if r["judged_mean"] is not None:
        out.append(f"  mean {r['judged_mean']}")
    for p in r["judged_problems"]:
        out.append(f"  ! {p}")
    if r.get("to_confirm"):
        out.append("to confirm (inferred, not gating):")
        out += [f"  - {t}" for t in r["to_confirm"][:8]]
    if r["next"]:
        out.append("next:")
        out += [f"  {i + 1}. {n}" for i, n in enumerate(r["next"])]
    return "\n".join(out)

