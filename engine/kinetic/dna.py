"""Code-to-design: derive the de-facto design system ("style DNA") implied by
source code, score its coherence and propose a consolidated KDL system.

Shape: trace/derive. Input is a `scan` result. Every number here is `derived`
from observed facts; the proposed system is a starting point for judgment,
not a design decision (it snaps what exists, it does not invent a direction)."""
from __future__ import annotations

import math
from collections import Counter

from . import color

IOS_STYLES = [("largeTitle", 34), ("title", 28), ("title2", 22), ("title3", 20), ("headline", 17),
              ("body", 17), ("callout", 16), ("subheadline", 15), ("footnote", 13), ("caption", 12),
              ("caption2", 11)]
NAMES = ["display", "title", "headline", "body", "callout", "caption", "micro"]


def _cluster(values: Counter, ratio: float) -> list:
    """Greedy merge: values within `ratio` of a more frequent value join it."""
    order = sorted(values.items(), key=lambda kv: (-kv[1], -kv[0]))
    centers = []
    for v, n in order:
        for c in centers:
            if max(v, c["v"]) / max(min(v, c["v"]), 1e-9) < ratio:
                c["members"].append(v)
                c["n"] += n
                break
        else:
            centers.append({"v": v, "n": n, "members": [v]})
    return sorted(centers, key=lambda c: -c["v"])


def _weighted_median(items):
    items = sorted(items)
    total = sum(w for _, w in items)
    acc = 0
    for v, w in items:
        acc += w
        if acc >= total / 2:
            return v
    return items[-1][0]


def _kmeans_log(counts: Counter, k: int, iters: int = 60) -> list:
    """Weighted 1-D k-means on log(size); centers are weighted medians (real, used values)."""
    vals = sorted(counts)
    if len(vals) <= k:
        return [[v] for v in vals]
    # initialise log-uniformly across the observed range so large sizes keep their own steps
    lo, hi = math.log(vals[0]), math.log(vals[-1])
    centers = sorted({min(vals, key=lambda v: abs(math.log(v) - (lo + (hi - lo) * i / (k - 1)))) for i in range(k)})
    groups = []
    for _ in range(iters):
        groups = [[] for _ in centers]
        for v in vals:
            j = min(range(len(centers)), key=lambda i: abs(math.log(v) - math.log(centers[i])))
            groups[j].append(v)
        new = [_weighted_median([(v, counts[v]) for v in g]) if g else c for g, c in zip(groups, centers)]
        if new == centers:
            break
        centers = new
    return [g for g in groups if g]


def propose_type(sizes: dict, max_steps: int = 7) -> dict:
    """Consolidate observed sizes into ≤ max_steps styles named around the body size.

    Rare sizes (one use) far outside the main range are kept out of the ramp and
    reported as `outliers` — they are usually one-off hero numerals or mistakes."""
    counts = Counter({float(k): v for k, v in sizes.items() if float(k) > 0})
    if not counts:
        return {}
    total = sum(counts.values())
    main = Counter({v: n for v, n in counts.items() if not (n <= max(1, total // 200) and (v > 48 or v < 9))})
    k = min(max_steps, len(main))
    groups = _kmeans_log(main, k)
    raw = sorted(((max(11, round(_weighted_median([(v, main[v]) for v in g]))), g) for g in groups),
                 key=lambda cg: -cg[0])
    centers = []
    for size, g in raw:  # merge steps that collapse to (nearly) the same size
        if centers and centers[-1][0] - size < 2:
            keep = centers[-1] if sum(main[v] for v in centers[-1][1]) >= sum(main[v] for v in g) else (size, g)
            centers[-1] = (keep[0], centers[-1][1] + g)
        else:
            centers.append((size, g))
    body_i = min(range(len(centers)), key=lambda i: (abs(centers[i][0] - 16.5) if 14 <= centers[i][0] <= 18 else 99,
                                                    -sum(main[v] for v in centers[i][1])))
    above = ["headline", "title", "display", "display-l"]
    below = ["callout", "caption", "micro", "micro-2"]
    out = {}
    for i, (size, g) in enumerate(centers):
        if i == body_i:
            name = "body"
        elif i < body_i:
            name = above[min(body_i - i - 1, len(above) - 1)]
        else:
            name = below[min(i - body_i - 1, len(below) - 1)]
        while name in out:
            name += "-2"
        line = round(size * (1.2 if size >= 28 else 1.32 if size >= 15 else 1.38))
        track = -0.02 if size >= 28 else -0.01 if size >= 20 else 0 if size >= 13 else 0.01
        out[name] = {"size": size, "line": line, "weight": 600 if size >= 20 else 400, "track": track,
                     "merged_from": sorted({round(m, 1) for m in g}), "uses": sum(main[v] for v in g)}
    outliers = sorted(set(counts) - set(main))
    if outliers:
        out["_outliers"] = outliers
    return dict(sorted(((n, v) for n, v in out.items() if n != "_outliers"),
                       key=lambda kv: -kv[1]["size"])) | ({"_outliers": outliers} if outliers else {})


def propose_space(spacing: dict, grid: int = 4) -> dict:
    snapped = Counter()
    for v, n in spacing.items():
        v = float(v)
        if v <= 2:
            continue
        s = max(grid, round(v / grid) * grid)
        snapped[s] += n
    vals = sorted(v for v, _ in snapped.most_common(8))
    names = ["xs", "s", "m", "l", "xl", "2xl", "3xl", "4xl"]
    return {names[i]: int(v) for i, v in enumerate(vals)}


def propose_radius(radii: dict) -> dict:
    counts = Counter({float(k): v for k, v in radii.items()})
    if not counts:
        return {}
    ratio = 1.25
    centers = _cluster(counts, ratio)
    while len(centers) > 4 and ratio < 3:
        ratio += 0.15
        centers = _cluster(counts, ratio)
    names = ["s", "m", "l", "xl"]
    vals = sorted(round(c["v"] / 2) * 2 for c in centers)
    out = {names[i]: v for i, v in enumerate(vals[:4])}
    out["full"] = 999
    return out


def dna(scan_result: dict, grid: int = 4) -> dict:
    s = scan_result.get("summary", {})
    cols = s.get("colors", [])
    neutrals = sorted((c for c in cols if c["neutral"]), key=lambda c: -c["oklch"][0])
    accents = [c for c in cols if not c["neutral"]]
    fams = {k: v for k, v in s.get("icon_families", {}).items() if not k.startswith("custom")}
    n_sizes = len(s.get("font_sizes", {}))
    n_radii = len(s.get("radii", {}))
    hues = len(s.get("hue_families", {}))
    coherence = {
        "type": round(max(0.0, 1 - max(0, n_sizes - 7) / 8), 2) if n_sizes else None,
        "spacing": s.get("spacing_on_grid_ratio"),
        "color": round(max(0.0, 1 - max(0, len(neutrals) - 6) / 8 - max(0, hues - 2) / 4), 2) if cols else None,
        "radius": round(max(0.0, 1 - max(0, n_radii - 4) / 6), 2) if n_radii else None,
        "icons": round(1 / len(fams), 2) if fams else None,
        "motion": round(0.5 * (1.0 if s.get("reduce_motion_sites") else 0.0)
                        + 0.5 * max(0.0, 1 - max(0, len(s.get("durations_ms", {})) - 6) / 12), 2)
        if s.get("animation_sites") else None,
    }
    known = [v for v in coherence.values() if v is not None]
    seed = None
    if accents:
        seed = max(accents, key=lambda c: c["oklch"][1])["hex"]
    elev = "shadow" if s.get("shadows", 0) >= 3 else "none"
    proposal = {
        "type": {"scale": propose_type(s.get("font_sizes", {}))},
        "color": {"seed": seed, "observed_neutrals": [c["hex"] for c in neutrals],
                  "observed_accents": [c["hex"] for c in accents]},
        "space": {"unit": grid, "scale": propose_space(s.get("spacing", {}), grid)},
        "shape": {"radius": propose_radius(s.get("radii", {}))},
        "motion": {"observed_durations_ms": s.get("durations_ms", {}), "observed_curves": s.get("curves", {}),
                   "observed_springs": s.get("springs", []),
                   "reduce_motion_handled": bool(s.get("reduce_motion_sites"))},
        "icon": {"observed_families": fams},
        "elevation": {"observed_strategy": elev, "shadow_sites": s.get("shadows", 0), "blur_sites": s.get("blur", 0)},
    }
    return {
        "tool": "dna",
        "coverage": scan_result.get("coverage", {}),
        "coherence": coherence,
        "coherence_mean": round(sum(known) / len(known), 2) if known else None,
        "dna": {
            "palette": {"neutrals": [c["hex"] for c in neutrals], "accents": [c["hex"] for c in accents],
                        "hue_families": s.get("hue_families", {})},
            "type_sizes": s.get("font_sizes", {}), "text_styles": s.get("text_styles", {}),
            "spacing": s.get("spacing", {}), "radii": s.get("radii", {}),
            "motion": {"durations_ms": s.get("durations_ms", {}), "curves": s.get("curves", {}),
                       "animation_sites": s.get("animation_sites", 0),
                       "reduce_motion_sites": s.get("reduce_motion_sites", 0),
                       "haptic_sites": s.get("haptic_sites", 0)},
            "icons": s.get("icon_families", {}),
            "effects": {"gradients": s.get("gradients", 0), "shadows": s.get("shadows", 0), "blur": s.get("blur", 0)},
        },
        "proposal": proposal,
        "limitations": [
            "the proposal consolidates what exists; it is not a direction — run the think/direct modules first",
            "colors computed at runtime or from assets are not seen",
        ],
    }


def to_kdl(d: dict) -> str:
    """Render the DNA as KDL `audit` + a `system` draft the model then edits."""
    p = d["proposal"]
    out = ["audit:", "  source: scanned code", "  coherence: {" + ", ".join(
        f"{k}: {v}" for k, v in d["coherence"].items() if v is not None) + "}"]
    out += ["  keep: []", "  evolve: []", "  replace: []", "  remove: []", "", "system:", "  type:",
            "    families: {display: TODO, text: TODO}", "    scale:"]
    for name, st in p["type"]["scale"].items():
        if name == "_outliers":
            out.append(f"      # outliers kept out of the ramp (one-off sizes): {st}")
            continue
        out.append(f"      {name}: {{size: {st['size']}, line: {st['line']}, weight: {st['weight']}, track: {st['track']}}}"
                   f"   # merged {st['merged_from']}")
    out += ["    dynamic: true", "  color:"]
    if p["color"]["seed"]:
        out.append(f"    seed: \"{p['color']['seed']}\"   # most chromatic observed color — confirm or replace")
        roles = color.derive_roles(p["color"]["seed"])
        out.append("    strategy: neutral+accent")
        out.append("    roles:   # derived by `kinetic palette`; edit to taste, keep contrast")
        for theme, r in roles.items():
            out.append(f"      {theme}:")
            for k, v in r.items():
                out.append(f"        {k}: \"{v}\"")
    out += ["  space:", f"    unit: {p['space']['unit']}",
            "    scale: {" + ", ".join(f"{k}: {v}" for k, v in p["space"]["scale"].items()) + "}",
            "  shape:", "    corner: continuous",
            "    radius: {" + ", ".join(f"{k}: {v}" for k, v in p["shape"]["radius"].items()) + "}",
            f"  elevation:\n    strategy: {'shadow' if p['elevation']['observed_strategy'] == 'shadow' else 'tonal'}",
            "  icon:", f"    family: {next(iter(p['icon']['observed_families']), 'TODO')}",
            "    style: outline", "    selected: fill", "  motion:", "    personality: TODO",
            "    springs:", "      default: {response: 0.35, damping: 0.9}",
            "    durations: {quick: 150, standard: 250}", "    reduce: crossfade"]
    return "\n".join(out) + "\n"
