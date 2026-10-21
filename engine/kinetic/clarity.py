"""Clarity: measure clutter on a render (stdlib only).

Clean design is mostly *absence*: few lines of text, few type sizes, real empty
space, one loud thing. A model can't see that in its own code, and critics
only feel it. This reads a screenshot and counts what a squinting reader
counts: lines of text, an estimate of words, the share of quiet rows, the
number of distinct text sizes, and the largest breathing gap. Thresholds are
per phone viewport (393pt wide, first 852pt), calibrated on blind-judged
renders (docs/EVALUATION.md).

Heuristics, not OCR: a "line" is a horizontal band of rows dense in sharp
light/dark transitions; a "word" is a run of ink inside a line separated by a
gap wider than ~0.35 × the line's height. Illustrations taller than a text line
count as graphics, not text. Report results as `derived` evidence."""
from __future__ import annotations

import math
import os
from collections import Counter

from . import sheet

VIEW_W, VIEW_H = 393, 852
EDGE = 48            # luma step that counts as a glyph edge
TEXT_ROW_EDGES = 6   # edges per 393px row for a row to be "texty"


def _luma(px, w, h):
    return [[(px[y][3 * x] * 299 + px[y][3 * x + 1] * 587 + px[y][3 * x + 2] * 114) // 1000 for x in range(w)]
            for y in range(h)]


def _bands(flags, gap=1):
    out, start, miss = [], None, 0
    for i, f in enumerate(flags + [False] * (gap + 1)):
        if f:
            if start is None:
                start = i
            miss = 0
        elif start is not None:
            miss += 1
            if miss > gap:
                out.append((start, i - miss + 1))
                start, miss = None, 0
    return out


def _words(lum_rows, y0, y1, w):
    """Ink runs along a text band: columns with an edge anywhere in the band, split by wide gaps."""
    hgt = y1 - y0
    cols = [False] * w
    for y in range(y0, y1):
        r = lum_rows[y]
        for x in range(1, w):
            if abs(r[x] - r[x - 1]) > EDGE:
                cols[x] = True
    runs = _bands(cols, gap=max(2, int(0.35 * hgt)))
    return len(runs), (runs[0][0] if runs else 0)


def measure(path: str) -> dict:
    w0, h0, px = sheet.read_png(path)
    w, h, px = sheet.downscale(w0, h0, px, VIEW_W) if w0 > VIEW_W * 1.4 else (w0, h0, px)
    h = min(h, VIEW_H)
    lum = _luma(px, w, h)
    edges = [sum(1 for x in range(1, w) if abs(r[x] - r[x - 1]) > EDGE) * VIEW_W / w for r in lum]
    texty = [e >= TEXT_ROW_EDGES for e in edges]
    lines, graphics = [], []
    for y0, y1 in _bands(texty, gap=1):
        hh = y1 - y0
        if hh < 5:
            continue
        (lines if hh <= 44 else graphics).append((y0, y1))
    words = 0
    for y0, y1 in lines:
        n, _ = _words(lum, y0, y1, w)
        words += n
    quiet = [e < 2 for e in edges]
    gaps = [b - a for a, b in _bands(quiet, gap=0)]
    sizes = Counter()
    for y0, y1 in lines:  # band height varies with ascenders/descenders: bucket by ~30% steps, ignore one-offs
        sizes[round(math.log(y1 - y0) / math.log(1.3))] += 1
    distinct_sizes = sum(1 for _, n in sizes.items() if n >= 2) + (1 if any(n == 1 for n in sizes.values()) else 0)
    text_rows = sum(b - a for a, b in lines)
    # loudness: saturated colour areas. One loud thing per viewport reads as calm; two or three compete.
    loud_rows, loud_px = [], 0
    for y in range(h):
        row = px[y]
        n = 0
        for x in range(0, w, 2):
            r, g, b = row[3 * x], row[3 * x + 1], row[3 * x + 2]
            mx, mn = max(r, g, b), min(r, g, b)
            if mx - mn > 70 and mx > 90:
                n += 1
        loud_px += n
        loud_rows.append(n >= 0.08 * (w / 2))
    loud_bands = [b for b in _bands(loud_rows, gap=8) if b[1] - b[0] >= 10]
    return {
        "file": path,
        "lines": len(lines),
        "words": words,
        "graphics": len(graphics),
        "text_sizes": distinct_sizes,
        "quiet_share": round(sum(quiet) / h, 2),
        "text_share": round(text_rows / h, 2),
        "largest_gap_pt": max(gaps) if gaps else 0,
        "edge_density": round(sum(edges) / (VIEW_W * h), 3),
        "loud_share": round(loud_px / (h * w / 2), 3),
        "loud_things": len(loud_bands),
    }


# per-viewport budgets: (good, bad) — linear between
BUDGET = {"words": (45, 120), "lines": (12, 28), "text_sizes": (4, 7), "quiet_share": (0.60, 0.35),
          "edge_density": (0.030, 0.07), "loud_share": (0.02, 0.08), "loud_things": (1, 3)}


def _sub(v, good, bad):
    if good < bad:
        return max(0.0, min(1.0, (bad - v) / (bad - good)))
    return max(0.0, min(1.0, (v - bad) / (good - bad)))


def grade(m: dict) -> dict:
    parts = {k: round(_sub(m[k], *BUDGET[k]) * 100) for k in BUDGET}
    if m["loud_things"] <= 1:
        parts["loud_share"] = 100  # one deliberate colour field (a state field, a hot kiln) is the one loud thing, not clutter
    score = round(0.25 * parts["words"] + 0.12 * parts["lines"] + 0.10 * parts["text_sizes"]
                  + 0.15 * parts["quiet_share"] + 0.08 * parts["edge_density"]
                  + 0.15 * parts["loud_share"] + 0.15 * parts["loud_things"])
    notes = []
    if m["words"] > BUDGET["words"][1] * 0.8:
        notes.append(f"~{m['words']} words in the first viewport: cut to the answer, its proof and one action")
    if m["text_sizes"] > 6:
        notes.append(f"{m['text_sizes']} text sizes: merge to 4–5 (display, title, body, meta)")
    if m["quiet_share"] < 0.33:
        notes.append(f"only {int(m['quiet_share'] * 100)}% quiet rows: remove containers or a block, let space group")
    if m["loud_things"] > 1:
        notes.append(f"{m['loud_things']} loud colour areas compete: keep one (the answer or the act), quiet the rest")
    if m["largest_gap_pt"] < 24:
        notes.append("no breathing gap ≥ 24pt anywhere: give the hero room")
    return {"clarity": score, "parts": parts, "notes": notes}


def clarity(items, limit_files: int = 400) -> dict:
    files = []
    for it in items:
        if os.path.isdir(it):
            files += [os.path.join(it, f) for f in sorted(os.listdir(it)) if f.lower().endswith(".png")]
        elif it.lower().endswith(".png"):
            files.append(it)
    rows = []
    for f in files[:limit_files]:
        m = measure(f)
        m.update(grade(m))
        rows.append(m)
    if not rows:
        raise ValueError("no PNG renders given")
    mean = round(sum(r["clarity"] for r in rows) / len(rows))
    worst = sorted(rows, key=lambda r: r["clarity"])[:3]
    return {"tool": "clarity", "mean": mean, "renders": rows,
            "worst": [{"file": os.path.basename(r["file"]), "clarity": r["clarity"], "notes": r["notes"]} for r in worst],
            "limitations": ["heuristic counts from pixels (not OCR); photos and dense illustrations read as graphics",
                            "first 852pt of each render only; scrolled entries are judged as their own viewport"]}
