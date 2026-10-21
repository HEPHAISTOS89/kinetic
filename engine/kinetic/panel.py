"""Panel: merge several independent critiques into one judgment.

One critic is one sample: in Kinetic's blind rounds, critics of the same pair
disagreed on the winner in three rounds out of five while agreeing on almost
every dimension. A panel of critics with different lenses (product,
identity, clarity…) is aggregated by **median per dimension**, keeps every
critic's evidence, reports **disagreement** (max − min) so a split is visible,
and keeps the fixes that **two or more critics** asked for as consensus."""
from __future__ import annotations

import json
import re
import statistics
from collections import Counter


def _median_int(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) // 2  # even: round the middle pair down


def _key(text: str) -> str:
    return " ".join(sorted(set(re.findall(r"[a-z]{4,}", (text or "").lower())))[:60])


def merge(critiques: list, lenses=None) -> dict:
    if len(critiques) < 2:
        raise ValueError("a panel needs at least 2 critiques")
    dims = sorted({d for c in critiques for d in (c.get("dimensions") or {})})
    out_dims, disagreement, consensus = {}, {}, []
    for d in dims:
        entries = [c["dimensions"][d] for c in critiques if d in (c.get("dimensions") or {})
                   and isinstance(c["dimensions"][d].get("score"), int)]
        if len(entries) < 2:
            continue
        scores = [e["score"] for e in entries]
        ev = []
        for e in entries:
            ev += (e.get("evidence") or [])[:2]
        fixes = [e.get("fix", "") for e in entries if e.get("fix")]
        out_dims[d] = {"score": _median_int(scores), "scores": scores, "evidence": ev,
                       "fix": fixes[0] if fixes else ""}
        disagreement[d] = max(scores) - min(scores)
        # consensus: fixes whose content words overlap strongly across critics
        keys = [set(_key(f).split()) for f in fixes]
        for i, f in enumerate(fixes):
            if any(len(keys[i] & keys[j]) >= 3 for j in range(len(fixes)) if j != i):
                consensus.append(f"{d}: {f}")
                break
    unjudged = sorted({u for c in critiques for u in (c.get("unjudged") or [])})
    tests = {}
    for t in sorted({t for c in critiques for t in (c.get("tests") or {})}):
        verdicts = [str(c["tests"][t]) for c in critiques if t in (c.get("tests") or {})]
        fails = sum(1 for v in verdicts if v.lower().startswith("fail"))
        tests[t] = f"{len(verdicts) - fails}/{len(verdicts)} pass" + (f" — {next(v for v in verdicts if v.lower().startswith('fail'))}" if fails else "")
    levers = [c.get("biggest_lever") for c in critiques if c.get("biggest_lever")]
    return {
        "renders": sorted({r for c in critiques for r in (c.get("renders") or [])}),
        "dimensions": out_dims,
        "unjudged": unjudged,
        "tests": tests,
        "biggest_lever": levers[0] if levers else "",
        "panel": {"size": len(critiques), "lenses": lenses or [c.get("lens", f"critic-{i + 1}") for i, c in enumerate(critiques)],
                  "disagreement": disagreement, "split": sorted(d for d, v in disagreement.items() if v >= 2),
                  "levers": levers, "consensus_fixes": consensus},
        "self_judged": any(bool(c.get("self_judged")) for c in critiques),
    }


def merge_files(paths) -> dict:
    cs = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            cs.append(json.load(fh))
    return merge(cs)
