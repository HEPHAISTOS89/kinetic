"""Icon SVG craft linter and normalizer (rules SVG01–SVG13 of
knowledge/iconography-svg.md). Shape: inspect (+ an explicit `--fix` writer).

Evidence: `observed` for attribute/element facts; `derived` for geometry
(bounding boxes computed from points and control points — conservative, so
curves may be reported slightly larger than drawn). SVG14/15 need a render
and a designer's eye; they are listed under `not_checked`."""
from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET

from .report import Finding, read_text

NS = "{http://www.w3.org/2000/svg}"
ALLOWED = {"svg", "g", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "title", "desc"}
DRAWABLE = {"path", "circle", "rect", "line", "polyline", "polygon", "ellipse"}
FORBIDDEN_ATTR = {"transform", "style", "class", "id"}
FORBIDDEN_EL = {"image", "text", "filter", "linearGradient", "radialGradient", "script", "foreignObject",
                "use", "mask", "clipPath", "pattern", "style"}
STROKES = {1.5, 1.75, 2.0}
DTD = re.compile(r"<!\s*(DOCTYPE|ENTITY)", re.I)
NUM = re.compile(r"-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _tag(el) -> str:
    return el.tag.replace(NS, "").split("}")[-1]


def _f(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def _inherited(el, parents, attr):
    if el.get(attr) is not None:
        return el.get(attr)
    for p in reversed(parents):
        if p.get(attr) is not None:
            return p.get(attr)
    return None


def arc_points(x1, y1, rx, ry, phi_deg, fa, fs, x2, y2, n=24):
    """Sample an SVG elliptical arc (endpoint → center parameterization, SVG 1.1 F.6.5)."""
    import math
    if rx == 0 or ry == 0 or (x1 == x2 and y1 == y2):
        return [(x2, y2)]
    rx, ry = abs(rx), abs(ry)
    phi = math.radians(phi_deg % 360)
    cp, sp = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    coef = math.sqrt(max(0.0, num / den)) if den else 0.0
    if fa == fs:
        coef = -coef
    cxp, cyp = coef * rx * y1p / ry, -coef * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a

    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    out = []
    for i in range(n + 1):
        t = t1 + dt * i / n
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        out.append((cp * ex - sp * ey + cx, sp * ex + cp * ey + cy))
    return out


def path_points(d: str):
    """Absolute points (endpoints and control points) of a path; arcs approximated by endpoints ± radius."""
    toks = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]|" + NUM.pattern, d or "")
    pts, i, cmd = [], 0, None
    authored = []
    x = y = sx = sy = 0.0
    arc_r = []
    counts = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}

    def take(n):
        nonlocal i
        vals = [float(t) for t in toks[i:i + n]]
        i += n
        return vals

    while i < len(toks):
        t = toks[i]
        if re.fullmatch(r"[A-Za-z]", t):
            cmd = t
            i += 1
            if cmd in "Zz":
                x, y = sx, sy
                continue
        if cmd is None:
            break
        n = counts[cmd.upper()]
        if i + n > len(toks):
            break
        v = take(n)
        authored.extend([v[0], v[1], v[5], v[6]] if cmd.upper() == "A" else v)
        rel = cmd.islower()
        C = cmd.upper()
        if C in "ML T":
            nx, ny = (x + v[0], y + v[1]) if rel else (v[0], v[1])
            pts.append((nx, ny))
            x, y = nx, ny
            if C == "M":
                sx, sy = x, y
                cmd = "l" if rel else "L"
        elif C == "H":
            x = x + v[0] if rel else v[0]
            pts.append((x, y))
        elif C == "V":
            y = y + v[0] if rel else v[0]
            pts.append((x, y))
        elif C in "CSQ":
            pairs = [(v[k], v[k + 1]) for k in range(0, n, 2)]
            ab = [((x + a, y + b) if rel else (a, b)) for a, b in pairs]
            pts.extend(ab)
            x, y = ab[-1]
        elif C == "A":
            nx, ny = (x + v[5], y + v[6]) if rel else (v[5], v[6])
            arc_r.append((v[0], v[1]))
            pts.extend(arc_points(x, y, v[0], v[1], v[2], int(v[3]), int(v[4]), nx, ny))
            x, y = nx, ny
    return pts, arc_r, authored


def _geometry(el, tag):
    """(points for bbox, scalar lengths for grid check)."""
    g = lambda k: _f(el.get(k))
    if tag == "circle":
        cx, cy, r = g("cx"), g("cy"), g("r")
        return [(cx - r, cy - r), (cx + r, cy + r)], [cx, cy, r], True
    if tag == "ellipse":
        cx, cy, rx, ry = g("cx"), g("cy"), g("rx"), g("ry")
        return [(cx - rx, cy - ry), (cx + rx, cy + ry)], [cx, cy, rx, ry], True
    if tag == "rect":
        x, y, w, h = g("x"), g("y"), g("width"), g("height")
        return [(x, y), (x + w, y + h)], [x, y, w, h, _f(el.get("rx")), _f(el.get("ry"))], False
    if tag == "line":
        return [(g("x1"), g("y1")), (g("x2"), g("y2"))], [g("x1"), g("y1"), g("x2"), g("y2")], False
    if tag in ("polyline", "polygon"):
        nums = [float(n) for n in NUM.findall(el.get("points", ""))]
        pts = list(zip(nums[0::2], nums[1::2]))
        return pts, nums, False
    if tag == "path":
        pts, arcs, authored = path_points(el.get("d", ""))
        return pts, authored, bool(arcs)
    return [], [], False


def lint_file(path: str, grid: int = 24) -> dict:
    findings, facts = [], {}

    def add(rule, sev, msg, fix, ev="observed"):
        tier = {"error": "F" if rule in ("SVG12",) else "D", "warning": "D", "info": "C"}[sev]
        findings.append(Finding(rule=rule, tier=tier, severity={"error": "major", "warning": "minor", "info": "info"}[sev],
                                evidence=ev, file=path, line=0, message=msg, fix=fix))

    try:
        raw = read_text(path)
        if DTD.search(raw):
            add("SVG12", "error", "DOCTYPE/ENTITY declarations are refused (XXE / entity expansion risk)",
                "icons never need a DTD; remove it")
            return {"file": path, "findings": findings, "facts": facts}
        root = ET.fromstring(raw)
    except (OSError, ET.ParseError) as e:
        add("SVG01", "error", f"not parseable as SVG: {e}", "write valid XML")
        return {"file": path, "findings": findings, "facts": facts}
    if "data:" in raw:
        add("SVG12", "error", "embedded data: URI", "icons are vector primitives only")
    if _tag(root) != "svg":
        add("SVG01", "error", "root element is not <svg>", "wrap in <svg xmlns=… viewBox=\"0 0 24 24\">")
    if not root.tag.startswith(NS):
        add("SVG01", "error", "missing xmlns=\"http://www.w3.org/2000/svg\"", "add the SVG namespace")
    vb = root.get("viewBox", "")
    if [ _f(x) for x in vb.replace(",", " ").split()] != [0, 0, grid, grid]:
        add("SVG01", "error", f"viewBox is {vb!r}, expected '0 0 {grid} {grid}'", f"draw on the {grid}×{grid} grid")
    for k in ("width", "height"):
        if root.get(k) and _f(str(root.get(k)).rstrip("px")) != grid:
            add("SVG01", "warning", f"root {k}={root.get(k)} fixes the rendered size", "omit width/height; size at use")
    strokes, caps, joins, radii, count = set(), set(), set(), set(), 0
    off_grid, out_of_bounds, long_paths, fill_mixed = [], [], [], False
    stack = [(root, [])]
    while stack:
        el, parents = stack.pop()
        tag = _tag(el)
        if tag in FORBIDDEN_EL:
            add("SVG12", "error", f"<{tag}> is not allowed in an icon", "use vector primitives only")
        elif tag not in ALLOWED:
            add("SVG02", "error", f"element <{tag}> is not allowed", "svg g path circle rect line polyline polygon ellipse")
        bad = [a for a in el.attrib if a.split("}")[-1] in FORBIDDEN_ATTR or a.startswith("data-")]
        if bad:
            add("SVG03", "error", f"<{tag}> has {', '.join(bad)}", "bake transforms into coordinates; no ids/classes/styles")
        for a in ("stroke", "fill", "color", "stop-color"):
            v = el.get(a)
            if v is not None and v not in ("currentColor", "none"):
                add("SVG04", "error", f"<{tag}> {a}=\"{v}\"", "use currentColor (or none) so the icon takes the text color")
        if tag in DRAWABLE:
            count += 1
            sw = _inherited(el, parents + [el], "stroke-width")
            stroke = _inherited(el, parents + [el], "stroke")
            fill = _inherited(el, parents + [el], "fill")
            if stroke not in (None, "none"):
                strokes.add(_f(sw, 1.0) if sw is not None else 1.0)
                caps.add(_inherited(el, parents + [el], "stroke-linecap") or "butt")
                joins.add(_inherited(el, parents + [el], "stroke-linejoin") or "miter")
                if fill is None:
                    add("SVG07", "error", f"<{tag}> is stroked but fill is not declared (defaults to black)",
                        "set fill=\"none\" on the root for outline icons")
                elif fill not in ("none", "currentColor"):
                    fill_mixed = True
            pts, vals, round_shape = _geometry(el, tag)
            if tag == "rect" and (el.get("rx") or el.get("ry")):
                radii.add(_f(el.get("rx") or el.get("ry")))
            for v in vals:
                if abs(v * 2 - round(v * 2)) > 1e-6:
                    off_grid.append(round(v, 3))
            if tag == "path" and len(el.get("d", "")) > 200:
                long_paths.append(len(el.get("d", "")))
            if pts:
                half = (_f(sw, 1.0) if sw else 1.0) / 2 if stroke not in (None, "none") else 0
                lo, hi = (1, grid - 1) if round_shape else (2, grid - 2)
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                bx = (min(xs) - half, min(ys) - half, max(xs) + half, max(ys) + half)
                if bx[0] < lo - 1e-6 or bx[1] < lo - 1e-6 or bx[2] > hi + 1e-6 or bx[3] > hi + 1e-6:
                    out_of_bounds.append((tag, tuple(round(b, 2) for b in bx)))
        for ch in list(el):
            stack.append((ch, parents + [el]))
    facts.update(strokes=sorted(strokes), caps=sorted(caps), joins=sorted(joins), radii=sorted(radii),
                 elements=count, fill_mixed=fill_mixed)
    if len(strokes) > 1:
        add("SVG05", "error", f"mixed stroke widths {sorted(strokes)}", "one stroke width per icon (1.5, 1.75 or 2)")
    elif strokes and next(iter(strokes)) not in STROKES:
        add("SVG05", "error", f"stroke width {next(iter(strokes))} is not 1.5, 1.75 or 2", "use the set's stroke width")
    if len(caps) > 1 or len(joins) > 1:
        add("SVG06", "warning", f"mixed caps {sorted(caps)} / joins {sorted(joins)}", "round/round across the set")
    if count > 8:
        add("SVG08", "warning", f"{count} drawable elements", "simplify; an icon reads at 16px")
    if off_grid:
        add("SVG09", "warning", f"{len(off_grid)} values off the 0.5 grid (e.g. {', '.join(map(str, off_grid[:5]))})",
            "snap to 0.5 so 1.5/2px strokes render crisp", ev="derived")
    for tag, bx in out_of_bounds[:3]:
        add("SVG10", "warning", f"<{tag}> extends to {bx}, outside the live area", "keep geometry within [2, 22] (round shapes [1, 23])",
            ev="derived")
    for n in long_paths[:3]:
        add("SVG11", "info", f"path data {n} chars (traced or auto-generated?)", "rebuild with primitives (circle, rect rx, line)")
    if fill_mixed:
        add("SVG07", "warning", "stroked element with a non-none fill", "outline icons: fill none; filled variant: no strokes")
    return {"file": path, "findings": findings, "facts": facts}


def lint(paths, grid: int = 24) -> dict:
    files = []
    for p in paths:
        if os.path.isdir(p):
            for dp, _, fns in os.walk(p):
                files += [os.path.join(dp, f) for f in sorted(fns) if f.lower().endswith(".svg")]
        else:
            files.append(p)
    results = [lint_file(f, grid) for f in files]
    findings = [f for r in results for f in r["findings"]]
    set_strokes = {s for r in results for s in r["facts"].get("strokes", [])}
    set_caps = {s for r in results for s in r["facts"].get("caps", [])}
    set_radii = {s for r in results for s in r["facts"].get("radii", [])}
    if len(results) > 1:
        if len(set_strokes) > 1:
            findings.append(Finding(rule="SVG05", tier="D", severity="major", evidence="derived", file="(set)",
                                    message=f"stroke widths differ across the set: {sorted(set_strokes)}",
                                    fix="one stroke width for every icon in the family"))
        if len(set_caps) > 1:
            findings.append(Finding(rule="SVG06", tier="D", severity="minor", evidence="derived", file="(set)",
                                    message=f"line caps differ across the set: {sorted(set_caps)}", fix="round caps everywhere"))
        if len(set_radii) > 1:
            findings.append(Finding(rule="SVG13", tier="D", severity="minor", evidence="derived", file="(set)",
                                    message=f"rect corner radii differ across the set: {sorted(set_radii)}",
                                    fix="one corner radius (2 on the 24 grid)"))
    findings.sort(key=lambda f: (f.order(), f.file))
    return {"tool": "svg", "ok": not any(f.severity == "major" for f in findings),
            "coverage": {"files": len(files)}, "findings": [f.as_dict() for f in findings],
            "facts": {r["file"]: r["facts"] for r in results},
            "not_checked": ["SVG14 gaps/detail size (render at 16/24/48px)", "SVG15 optical size vs the set"],
            "limitations": ["bounding boxes include control points, so curves may be flagged slightly early"]}


def normalize(path: str) -> str:
    """Return a cleaned SVG: no ids/classes/styles, currentColor, 2-decimal precision.
    Transforms are NOT baked — they are reported so the author redraws."""
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    raw = read_text(path)
    if DTD.search(raw):
        raise ValueError("refusing SVG with DOCTYPE/ENTITY declarations")
    root = ET.fromstring(raw)
    for el in root.iter():
        for a in list(el.attrib):
            if a.split("}")[-1] in ("id", "class", "style") or a.startswith("data-") or "inkscape" in a or "sodipodi" in a:
                del el.attrib[a]
        for a in ("stroke", "fill"):
            v = el.get(a)
            if v and v not in ("none", "currentColor"):
                el.set(a, "currentColor")
        for a in ("d", "points"):
            val = el.get(a)
            if val:
                el.set(a, NUM.sub(lambda m: f"{float(m.group(0)):.2f}".rstrip("0").rstrip("."), val))
    if root.get("fill") is None and any(el.get("stroke") for el in root.iter()):
        root.set("fill", "none")
    return ET.tostring(root, encoding="unicode")
