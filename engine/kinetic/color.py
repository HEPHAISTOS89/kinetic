"""Color science for Kinetic: sRGB, OKLab/OKLCH, WCAG 2 contrast, APCA Lc,
gamut mapping, tonal ramps and role derivation for light and dark themes."""
from __future__ import annotations

import math
import re

_HEX = re.compile(r"^#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")


# ---------------------------------------------------------------- parsing
def parse_hex(value: str):
    """'#RGB' | '#RRGGBB' | '#RRGGBBAA' -> (r, g, b, a) floats 0..1."""
    m = _HEX.match(str(value).strip())
    if not m:
        raise ValueError(f"not a hex color: {value!r}")
    h = m.group(1)
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return r, g, b, a


def is_hex(value) -> bool:
    return isinstance(value, str) and bool(_HEX.match(value.strip())) and value.strip().startswith("#")


def to_hex(rgb) -> str:
    r, g, b = (max(0, min(255, round(c * 255))) for c in rgb[:3])
    return f"#{r:02X}{g:02X}{b:02X}"


# ------------------------------------------------------------ transforms
def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def srgb_to_oklab(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )


def oklab_to_linear(lab):
    L, a, b = lab
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_oklab(lch):
    L, C, H = lch
    return L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))


def oklab_to_oklch(lab):
    L, a, b = lab
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H


def hex_to_oklch(value: str):
    return oklab_to_oklch(srgb_to_oklab(parse_hex(value)))


def in_gamut(lin, eps=1e-6) -> bool:
    return all(-eps <= c <= 1 + eps for c in lin)


def oklch_to_hex(lch) -> str:
    """Convert with gamut mapping by chroma reduction (hue and lightness kept)."""
    L, C, H = lch
    L = max(0.0, min(1.0, L))
    lin = oklab_to_linear(oklch_to_oklab((L, C, H)))
    if not in_gamut(lin):
        lo, hi = 0.0, C
        for _ in range(30):
            mid = (lo + hi) / 2
            if in_gamut(oklab_to_linear(oklch_to_oklab((L, mid, H)))):
                lo = mid
            else:
                hi = mid
        lin = oklab_to_linear(oklch_to_oklab((L, lo, H)))
    return to_hex(tuple(_gam(max(0.0, min(1.0, c))) for c in lin))


def delta_e_ok(a: str, b: str) -> float:
    la, lb = srgb_to_oklab(parse_hex(a)), srgb_to_oklab(parse_hex(b))
    return math.dist(la, lb)


# ------------------------------------------------------------- contrast
def luminance(value) -> float:
    rgb = parse_hex(value) if isinstance(value, str) else value
    r, g, b = (_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def composite(fg: str, bg: str) -> str:
    """Flatten a translucent foreground over an opaque background."""
    fr, fgc, fb, fa = parse_hex(fg)
    br, bgc, bb, _ = parse_hex(bg)
    return to_hex((fr * fa + br * (1 - fa), fgc * fa + bgc * (1 - fa), fb * fa + bb * (1 - fa)))


def wcag(fg: str, bg: str) -> float:
    if parse_hex(fg)[3] < 1:
        fg = composite(fg, bg)
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def apca(fg: str, bg: str) -> float:
    """APCA-W3 0.0.98G-4g lightness contrast Lc (signed: + dark-on-light)."""
    if parse_hex(fg)[3] < 1:
        fg = composite(fg, bg)

    def y(value):
        r, g, b, _ = parse_hex(value)
        yy = 0.2126729 * r ** 2.4 + 0.7151522 * g ** 2.4 + 0.0721750 * b ** 2.4
        return yy + (0.022 - yy) ** 1.414 if yy < 0.022 else yy

    yt, yb = y(fg), y(bg)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        sapc = (yb ** 0.56 - yt ** 0.57) * 1.14
        out = 0.0 if sapc < 0.1 else sapc - 0.027
    else:
        sapc = (yb ** 0.65 - yt ** 0.62) * 1.14
        out = 0.0 if sapc > -0.1 else sapc + 0.027
    return round(out * 100, 1)


def contrast_report(fg: str, bg: str) -> dict:
    ratio = wcag(fg, bg)
    lc = apca(fg, bg)
    return {
        "fg": fg,
        "bg": bg,
        "wcag": round(ratio, 2),
        "apca_lc": lc,
        "aa_body": ratio >= 4.5,
        "aa_large": ratio >= 3.0,
        "aaa_body": ratio >= 7.0,
        "apca_body": abs(lc) >= 75,
        "apca_fluent": abs(lc) >= 60,
    }


# ----------------------------------------------------------------- ramps
RAMP_STOPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
_RAMP_L = [0.975, 0.945, 0.890, 0.810, 0.715, 0.625, 0.535, 0.445, 0.355, 0.270, 0.205]


def ramp(seed: str, chroma_scale: float = 1.0) -> dict:
    """Perceptually even tonal ramp keeping the seed hue.

    Chroma follows a bell curve peaking near the seed's own lightness so that
    tints and shades stay in gamut and don't go muddy or neon."""
    L0, C0, H = hex_to_oklch(seed)
    out = {}
    for stop, L in zip(RAMP_STOPS, _RAMP_L):
        bell = math.exp(-((L - L0) ** 2) / (2 * 0.22 ** 2))
        C = C0 * chroma_scale * (0.25 + 0.75 * bell)
        # warm hues drift slightly toward yellow in tints, cool toward blue in shades
        h = H + (4 if L > L0 else -3) * (abs(L - L0) / 0.5)
        out[stop] = oklch_to_hex((L, C, h))
    return out


def _solve_l(hue: float, chroma: float, against: str, target: float, direction: int,
             start: float) -> str:
    """Walk lightness from `start` in `direction` until WCAG >= target against `against`."""
    L = start
    best = oklch_to_hex((L, chroma, hue))
    for _ in range(200):
        cand = oklch_to_hex((L, chroma, hue))
        if wcag(cand, against) >= target:
            return cand
        best = cand
        L += 0.004 * direction
        if L <= 0 or L >= 1:
            break
    return best


def derive_roles(seed: str, strategy: str = "neutral+accent", neutral_chroma: float | None = None,
                 temperature: str = "auto") -> dict:
    """Derive complete light/dark role sets that pass Kinetic's contrast floor.

    strategy: neutral+accent | monochrome | brand-led
    The neutrals borrow the seed hue at very low chroma (tinted greys), which is
    the single biggest difference between a designed palette and default greys."""
    L0, C0, H = hex_to_oklch(seed)
    if C0 < 0.03 and strategy != "brand-led":
        strategy = "monochrome"  # an ink/grey seed means a monochrome system, not a grey accent
    nc = neutral_chroma
    if nc is None:
        nc = {"monochrome": 0.018, "brand-led": 0.010}.get(strategy, 0.008)
    nh = H
    if C0 < 0.03:  # achromatic seed: its hue is noise; neutrals follow the requested temperature
        nh = 250.0
        nc = min(nc, 0.006)
    if temperature == "warm":
        nh = 70.0
    elif temperature == "cool":
        nh = 250.0

    def n(L, c=nc):
        return oklch_to_hex((L, c, nh))

    roles = {}
    # ---- light
    bg = n(0.985, nc * 0.6)
    surface = n(1.0, 0) if strategy != "monochrome" else n(0.995, nc * 0.4)
    surface2 = n(0.955, nc)
    border = n(0.895, nc)
    text = _solve_l(nh, nc * 1.4, bg, 13.0, -1, 0.30)
    text2 = _solve_l(nh, nc * 1.6, bg, 5.2, -1, 0.56)
    text3 = _solve_l(nh, nc * 1.4, bg, 3.2, -1, 0.66)
    accent_l = min(L0, 0.62)
    accent = _solve_l(H, C0, bg, 3.4, -1, accent_l)
    if wcag("#FFFFFF", accent) >= 4.5:
        on_accent = "#FFFFFF"
    else:
        # designers deepen a bright accent slightly so white text works, before
        # resorting to dark text on it (which reads as a warning/yellow pattern)
        deeper = _solve_l(H, C0, "#FFFFFF", 4.6, -1, accent_l)
        if wcag("#FFFFFF", deeper) >= 4.5 and hex_to_oklch(accent)[0] - hex_to_oklch(deeper)[0] <= 0.12:
            accent, on_accent = deeper, "#FFFFFF"
        else:
            on_accent = _solve_l(H, 0.02, accent, 4.6, -1, 0.25)
    if wcag(on_accent, accent) < 4.5:
        accent = _solve_l(H, C0, "#FFFFFF", 4.6, -1, accent_l)
        on_accent = "#FFFFFF"
    roles["light"] = {
        "bg": bg, "surface": surface, "surface-2": surface2, "border": border,
        "text": text, "text-2": text2, "text-3": text3,
        "accent": accent, "on-accent": on_accent,
        "accent-soft": oklch_to_hex((0.94, min(C0, 0.06), H)),
        "danger": _solve_l(27, 0.19, bg, 4.6, -1, 0.55),
        "success": _solve_l(150, 0.14, bg, 4.6, -1, 0.55),
        "warning": _solve_l(70, 0.15, bg, 4.6, -1, 0.60),
        "focus": accent,
    }
    # ---- dark (designed, not inverted: lifted surfaces, desaturated accent)
    dbg = n(0.165, nc * 1.2)
    dsurface = n(0.205, nc * 1.2)
    dsurface2 = n(0.250, nc * 1.2)
    dborder = n(0.315, nc * 1.2)
    dtext = _solve_l(nh, nc, dbg, 13.0, 1, 0.90)
    dtext2 = _solve_l(nh, nc * 1.4, dsurface, 5.2, 1, 0.70)
    dtext3 = _solve_l(nh, nc * 1.2, dbg, 3.2, 1, 0.55)
    if C0 < 0.03:  # monochrome: the accent is the ink itself, inverted for dark
        dacc = _solve_l(nh, nc, dbg, 12.0, 1, 0.90)
    else:
        dacc = _solve_l(H, C0 * 0.85, dbg, 5.0, 1, max(L0, 0.72))
    d_on = _solve_l(H, 0.03, dacc, 4.6, -1, 0.22)
    roles["dark"] = {
        "bg": dbg, "surface": dsurface, "surface-2": dsurface2, "border": dborder,
        "text": dtext, "text-2": dtext2, "text-3": dtext3,
        "accent": dacc, "on-accent": d_on,
        "accent-soft": oklch_to_hex((0.30, min(C0, 0.07), H)),
        "danger": _solve_l(27, 0.13, dbg, 4.6, 1, 0.70),
        "success": _solve_l(150, 0.12, dbg, 4.6, 1, 0.70),
        "warning": _solve_l(80, 0.13, dbg, 4.6, 1, 0.75),
        "focus": dacc,
    }
    return roles


CONTRAST_PAIRS = [
    ("text", "bg", 4.5), ("text", "surface", 4.5),
    ("text-2", "bg", 4.5), ("text-2", "surface", 4.5),
    ("on-accent", "accent", 4.5), ("accent", "bg", 3.0),
    ("danger", "bg", 3.0), ("text-3", "bg", 3.0),
]


def check_roles(roles: dict) -> list:
    """Check every contrast pair for every theme (incl. custom `on-X`/`X` pairs); returns list of dicts."""
    results = []
    for theme, r in roles.items():
        if not isinstance(r, dict):
            continue
        pairs = list(CONTRAST_PAIRS)
        known = {(a, b) for a, b, _ in pairs}
        for key in r:
            if key.startswith("on-") and key[3:] in r and (key, key[3:]) not in known:
                pairs.append((key, key[3:], 4.5))
        for fg, bg, minimum in pairs:
            if fg in r and bg in r and is_hex(r[fg]) and is_hex(r[bg]):
                rep = contrast_report(r[fg], r[bg])
                rep.update(theme=theme, pair=f"{fg}/{bg}", minimum=minimum, ok=rep["wcag"] >= minimum)
                results.append(rep)
    return results


def describe(value: str) -> dict:
    L, C, H = hex_to_oklch(value)
    return {"hex": to_hex(parse_hex(value)), "oklch": [round(L, 3), round(C, 3), round(H, 1)],
            "neutral": C < 0.03, "hue_family": hue_family(H, C)}


def hue_family(H: float, C: float) -> str:
    if C < 0.03:
        return "neutral"
    for name, lo, hi in [("red", 0, 40), ("orange", 40, 70), ("yellow", 70, 105),
                         ("green", 105, 165), ("teal", 165, 200), ("blue", 200, 255),
                         ("violet", 255, 300), ("magenta", 300, 345), ("red", 345, 361)]:
        if lo <= H < hi:
            return name
    return "red"


def is_ai_purple(value: str) -> bool:
    """The default 'AI gradient' family: violet/indigo/magenta with real chroma."""
    _, C, H = hex_to_oklch(value)
    return C >= 0.08 and 250 <= H <= 330
