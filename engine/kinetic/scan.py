"""Lexical design scanner for Flutter, SwiftUI, Compose, React Native and web.

Shape: inspect. It reports design *facts* found in source text (colors, type
sizes, spacing, radii, motion, icons, effects) with file:line, and the catalog
rules those facts trigger. It does not parse ASTs: every rule declares its
evidence level — `observed` (the literal is in the file), `derived` (computed
over observed facts), `inferred` (heuristic about intent). Files it cannot
read are reported as unknown coverage, never as clean."""
from __future__ import annotations

import itertools
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from . import color
from .report import Finding

EXCLUDE_DIRS = {
    ".git", ".dart_tool", "build", "Pods", "node_modules", "DerivedData", ".gradle", ".idea",
    ".next", "dist", ".expo", "coverage", ".build", "Carthage", "vendor", ".venv", "__pycache__",
    "android/app/build", ".kinetic", ".swiftpm", "out", "generated",
}
LANG_BY_EXT = {
    ".dart": "flutter", ".swift": "swiftui", ".kt": "compose", ".kts": None,
    ".tsx": "tsx", ".jsx": "tsx", ".ts": "tsx", ".js": "tsx",
    ".css": "css", ".scss": "css", ".vue": "tsx", ".svelte": "tsx", ".html": "css",
}
SKIP_FILE = re.compile(r"(\.g\.dart|\.freezed\.dart|\.mocks\.dart|\.min\.js|\.d\.ts|\.test\.|\.spec\.|_test\.dart|Tests?\.swift|Test\.kt)$")
FIXTURE_PATH = re.compile(r"(fixture|mock|fake|preview|gallery|sample|demo|stub|storybook|golden)s?", re.I)
_DATA_WORDS = ['line', 'route', 'lane', 'category', 'categories', 'series', 'chart', 'data', 'status', 'severity', 'danger', 'error', 'warning', 'success', 'delay', 'closure', 'closed', 'alert', 'info', 'badge', 'tag', 'mode', 'network']
DATA_CONTEXT = re.compile(
    r"(?:(?<![A-Za-z])(?:" + "|".join(_DATA_WORDS) + r")|(?<=[a-z])(?:" + "|".join(w.capitalize() for w in _DATA_WORDS) + r"))"
    r"(?![a-z])")
DATA_PATH = re.compile(r"(line|route|category|chart|data|status|severity)[_-]?colou?rs?", re.I)
BLOCK_THEME = re.compile(r"(?i)(?:\b(?:let|var|val|const|final|static)\s+\w*?(dark|night|light)\w*\s*(?::[^=]+)?=\s*[\w.]*\s*[\(\{\[]\s*$"
                         r"|case\s+\.(dark|light)\s*:|\b(dark|light)\w*\s*:\s*[\w.]*\(\s*$)")
THEME_PATH = re.compile(r"(theme|tokens?|colou?rs?|palette|design[_-]?system|styles?|appearance|brand)", re.I)

MATERIAL_COLORS = {
    "red": "#F44336", "pink": "#E91E63", "purple": "#9C27B0", "deepPurple": "#673AB7",
    "indigo": "#3F51B5", "blue": "#2196F3", "lightBlue": "#03A9F4", "cyan": "#00BCD4",
    "teal": "#009688", "green": "#4CAF50", "lightGreen": "#8BC34A", "lime": "#CDDC39",
    "yellow": "#FFEB3B", "amber": "#FFC107", "orange": "#FF9800", "deepOrange": "#FF5722",
    "brown": "#795548", "grey": "#9E9E9E", "blueGrey": "#607D8B", "black": "#000000",
    "white": "#FFFFFF", "purpleAccent": "#E040FB", "deepPurpleAccent": "#7C4DFF",
    "indigoAccent": "#536DFE", "pinkAccent": "#FF4081", "blueAccent": "#448AFF",
}
SWIFT_COLORS = {
    "blue": "#007AFF", "purple": "#AF52DE", "indigo": "#5856D6", "pink": "#FF2D55", "red": "#FF3B30",
    "orange": "#FF9500", "yellow": "#FFCC00", "green": "#34C759", "mint": "#00C7BE", "teal": "#30B0C7",
    "cyan": "#32ADE6", "brown": "#A2845E", "gray": "#8E8E93", "black": "#000000", "white": "#FFFFFF",
}
COMPOSE_COLORS = {
    "Red": "#FF0000", "Blue": "#0000FF", "Green": "#00FF00", "Magenta": "#FF00FF", "Cyan": "#00FFFF",
    "Yellow": "#FFFF00", "Gray": "#888888", "DarkGray": "#444444", "LightGray": "#CCCCCC",
    "Black": "#000000", "White": "#FFFFFF",
}

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF⭐✅❌]")
GREETING = re.compile(r"\b(good\s+(morning|afternoon|evening|night)|welcome back|bonjour|bonsoir|hello|hi|hey|salut|coucou)\b\s*[,!]?\s*(\$|\{|\\\(|[A-Z])", re.I)
COPY_SLOP = re.compile(r"\b(unlock (your|the)|supercharge|elevate your|empower|revolutioni[sz]e|next[- ]level|game[- ]changer|seamless(ly)?|cutting[- ]edge|boostez|débloquez|révolutionn|oops!|whoops)\b", re.I)
FAKE_PROOF = re.compile(r"(\b[45](\.\d)?\s*(★|stars?|/\s*5)|\b\d+(\.\d+)?\s*[kKmM]\+?\s*(users|customers|clients|downloads|utilisateurs|members)|trusted by\s+\d|★★★★)", re.I)
LOG_LINE = re.compile(r"\b(debugPrint|print|log|logger\.\w+|_log\w*|Log\.[a-z]|developer\.log|NSLog|os_log|Logger\b|console\.\w+|"
                      r"assert|throw|Exception|Error\(|fatalError|precondition|Timber\.\w)\s*\(?", re.I)
LOG_TAG = re.compile(r"\[[A-Z][\w .:/-]{2,40}\]|^\$_?\w*prefix", re.I)
STRING_LIT = re.compile(r"\"((?:[^\"\\\n]|\\.){2,200})\"|'((?:[^'\\\n]|\\.){2,200})'")
JSX_TEXT = re.compile(r">\s*([^<>{}\n]{3,160}?)\s*<")


@dataclass
class Fact:
    kind: str
    value: object
    file: str
    line: int
    raw: str = ""
    themed: bool = False
    context: str = ""
    theme: str = "light"


@dataclass
class FileScan:
    path: str
    lang: str
    loc: int
    facts: list = field(default_factory=list)
    findings: list = field(default_factory=list)
    flags: Counter = field(default_factory=Counter)
    fixture: bool = False


# ----------------------------------------------------------------- helpers
def _num(s):
    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except (TypeError, ValueError):
        return None


def _frac(expr: str):
    expr = expr.strip()
    m = re.fullmatch(r"([\d.]+)\s*/\s*([\d.]+)", expr)
    if m:
        return float(m.group(1)) / float(m.group(2))
    try:
        return float(expr)
    except ValueError:
        return None


def _argb(h: str) -> str:
    a, rgb = h[:2], h[2:]
    return f"#{rgb.upper()}" if a.upper() == "FF" else f"#{rgb.upper()}{a.upper()}"


def _region(text: str, start: int, limit: int = 1500) -> str:
    """Text from `start` (an opening bracket) to its matching close."""
    i = text.find("(", start)
    j = text.find("{", start)
    cands = [x for x in (i, j) if x != -1]
    if not cands:
        return text[start:start + limit]
    i = min(cands)
    open_ch = text[i]
    close_ch = ")" if open_ch == "(" else "}"
    depth = 0
    for k in range(i, min(len(text), i + limit)):
        ch = text[k]
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start:k + 1]
    return text[start:start + limit]


def _closures(text: str, start: int, limit: int = 1500) -> str:
    """Call region plus any trailing closures/lambdas (`f(...) { }`, `label: { }`)."""
    end = start
    reg = _region(text, start, limit)
    end = start + len(reg)
    for _ in range(3):
        m = re.match(r"\s*(?:label\s*:\s*)?\{", text[end:end + 40])
        if not m:
            break
        nxt = _region(text, end + m.end() - 1, limit)
        end = end + m.end() - 1 + len(nxt)
    return text[start:end]


def _line_at(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def _code_lines(text: str):
    """(line_no, line) skipping comment-only lines."""
    in_block = False
    for no, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if in_block:
            if "*/" in s:
                in_block = False
            continue
        if s.startswith("/*"):
            in_block = "*/" not in s
            continue
        if s.startswith("//") or s.startswith("*") or s.startswith("#!"):
            continue
        yield no, line


# ------------------------------------------------------- per-language specs
# value extractors: (kind, regex, converter(match) -> value or None)
COMMON_HEX = (r"[\"'](#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?|#[0-9A-Fa-f]{3})[\"']", lambda m: m.group(1).upper())

EXTRACT = {
    "flutter": [
        ("color", r"Color\(\s*0x([0-9A-Fa-f]{8})\s*\)", lambda m: _argb(m.group(1))),
        ("color", r"Color\.fromARGB\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
         lambda m: color.to_hex(tuple(int(m.group(k)) / 255 for k in (2, 3, 4)))),
        ("color", r"Color\.fromRGBO\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,",
         lambda m: color.to_hex(tuple(int(m.group(k)) / 255 for k in (1, 2, 3)))),
        ("color", r"\bColors\.([a-zA-Z]+?)(?:Accent)?(?:\[\d+\]|\.shade\d+)?\b(?!\()",
         lambda m: MATERIAL_COLORS.get(m.group(1)) if m.group(1) not in ("transparent",) else None),
        ("font_size", r"fontSize\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("spacing", r"EdgeInsets\.(?:all|symmetric|only|fromLTRB|directional)\(([^)]*)\)", None),
        ("spacing", r"SizedBox\(\s*(?:height|width)\s*:\s*([\d.]+)\s*\)", lambda m: _num(m.group(1))),
        ("spacing", r"\b(?:Gap|SliverGap)\(\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("spacing", r"\b(?:spacing|runSpacing|mainAxisSpacing|crossAxisSpacing)\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("radius", r"(?:BorderRadius|Radius)\.circular\(\s*([\d.]+)\s*\)", lambda m: _num(m.group(1))),
        ("duration", r"Duration\(\s*milliseconds\s*:\s*(\d+)", lambda m: int(m.group(1))),
        ("duration", r"Duration\(\s*seconds\s*:\s*(\d+)", lambda m: int(m.group(1)) * 1000),
        ("curve", r"Curves\.(\w+)", lambda m: m.group(1)),
        ("icon", r"\bIcons\.(\w+)", lambda m: "material:" + ("outlined" if re.search(r"_outline(d)?$", m.group(1)) else "rounded" if m.group(1).endswith("_rounded") else "sharp" if m.group(1).endswith("_sharp") else "filled")),
        ("icon", r"\bCupertinoIcons\.(\w+)", lambda m: "cupertino"),
        ("icon", r"\b(PhosphorIcons|LucideIcons|FontAwesomeIcons|HugeIcons|Iconsax|FeatherIcons|Ionicons|TablerIcons|BoxIcons|EvaIcons)\b", lambda m: m.group(1).lower()),
        ("icon", r"SvgPicture\.asset", lambda m: "custom-svg"),
    ],
    "swiftui": [
        ("color", r"Color\(\s*(?:\.sRGB\s*,\s*)?red\s*:\s*([^,]+),\s*green\s*:\s*([^,]+),\s*blue\s*:\s*([^,)]+)",
         lambda m: (lambda r, g, b: color.to_hex((r, g, b)) if None not in (r, g, b) and max(r, g, b) <= 1 else None)(
             _frac(m.group(1)), _frac(m.group(2)), _frac(m.group(3)))),
        ("color", r"(?:Color|UIColor)\(\s*hex\s*:\s*\"?#?(?:0x)?([0-9A-Fa-f]{6})", lambda m: "#" + m.group(1).upper()),
        ("color", r"(?:Color|UIColor)\(\s*\"#?([0-9A-Fa-f]{6})\"", lambda m: "#" + m.group(1).upper()),
        ("color", r"(?:Color|UIColor)\([^)\n]*?\b(?:kLight|light|hex|rgb)\s*:\s*0x([0-9A-Fa-f]{6})", lambda m: "#" + m.group(1).upper()),
        ("color", r"(?:Color|UIColor)\([^)\n]*?\b(?:kDark|dark)\s*:\s*0x([0-9A-Fa-f]{6})", lambda m: "#" + m.group(1).upper()),
        ("color", r"(?:Color\.|foregroundStyle\(\.|foregroundColor\(\.|tint\(\.|background\(\.|fill\(\.)\b(blue|purple|indigo|pink|red|orange|yellow|green|mint|teal|cyan|brown|gray|black|white)\b",
         lambda m: SWIFT_COLORS.get(m.group(1))),
        ("font_size", r"\.system\(\s*size\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("font_size", r"\.custom\(\s*\"[^\"]+\"\s*,\s*(?:size|fixedSize)\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("text_style", r"\.font\(\s*\.(largeTitle|title|title2|title3|headline|subheadline|body|callout|footnote|caption|caption2)\b", lambda m: m.group(1)),
        ("spacing", r"\.padding\(\s*([\d.]+)\s*\)", lambda m: _num(m.group(1))),
        ("spacing", r"\.padding\(\s*\.[\w\[\], .]+,\s*([\d.]+)\s*\)", lambda m: _num(m.group(1))),
        ("spacing", r"\bspacing\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("spacing", r"Spacer\(\)\.frame\(\s*(?:height|width)\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("radius", r"cornerRadius\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("radius", r"\.cornerRadius\(\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("duration", r"\.(?:easeInOut|easeIn|easeOut|linear|spring|snappy|smooth|bouncy)\(\s*duration\s*:\s*([\d.]+)", lambda m: int(float(m.group(1)) * 1000)),
        ("curve", r"(?:withAnimation\(|\.animation\(|Animation)\s*\.(easeInOut|easeIn|easeOut|linear|spring|interactiveSpring|interpolatingSpring|bouncy|snappy|smooth)\b", lambda m: m.group(1)),
        ("spring", r"\.spring\(\s*response\s*:\s*([\d.]+)\s*,\s*dampingFraction\s*:\s*([\d.]+)", lambda m: (float(m.group(1)), float(m.group(2)))),
        ("icon", r"Image\(\s*systemName\s*:", lambda m: "sf-symbols"),
        ("icon", r"(?:Label\([^)]*systemImage\s*:)", lambda m: "sf-symbols"),
    ],
    "compose": [
        ("color", r"Color\(\s*0x([0-9A-Fa-f]{8})\s*\)", lambda m: _argb(m.group(1))),
        ("color", r"Color\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*[,)]",
         lambda m: color.to_hex(tuple(int(m.group(k)) / 255 for k in (1, 2, 3))) if max(int(m.group(k)) for k in (1, 2, 3)) <= 255 else None),
        ("color", r"\bColor\.(Red|Blue|Green|Magenta|Cyan|Yellow|Gray|DarkGray|LightGray|Black|White)\b", lambda m: COMPOSE_COLORS[m.group(1)]),
        ("font_size", r"fontSize\s*=\s*([\d.]+)\.sp", lambda m: _num(m.group(1))),
        ("text_style", r"MaterialTheme\.typography\.(\w+)", lambda m: m.group(1)),
        ("spacing", r"\.padding\(\s*([\d.]+)\.dp\s*\)", lambda m: _num(m.group(1))),
        ("spacing", r"(?:horizontal|vertical|start|end|top|bottom|all)\s*=\s*([\d.]+)\.dp", lambda m: _num(m.group(1))),
        ("spacing", r"Spacer\(\s*(?:Modifier|modifier\s*=\s*Modifier)\.(?:height|width)\(\s*([\d.]+)\.dp", lambda m: _num(m.group(1))),
        ("spacing", r"spacedBy\(\s*([\d.]+)\.dp", lambda m: _num(m.group(1))),
        ("radius", r"RoundedCornerShape\(\s*([\d.]+)\.dp", lambda m: _num(m.group(1))),
        ("duration", r"(?:tween|keyframes)\(\s*(?:durationMillis\s*=\s*)?(\d+)", lambda m: int(m.group(1))),
        ("duration", r"durationMillis\s*=\s*(\d+)", lambda m: int(m.group(1))),
        ("curve", r"\b(LinearEasing|FastOutSlowInEasing|LinearOutSlowInEasing|FastOutLinearInEasing|EaseInOut\w*)\b", lambda m: m.group(1)),
        ("icon", r"\bIcons\.(Filled|Outlined|Rounded|Sharp|TwoTone|Default|AutoMirrored\.\w+)\.", lambda m: "material:" + m.group(1).split(".")[0].lower()),
        ("icon", r"painterResource\(\s*R\.drawable\.ic_", lambda m: "custom-drawable"),
    ],
    "tsx": [
        COMMON_HEX[:1] and ("color", COMMON_HEX[0], COMMON_HEX[1]),
        ("color", r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", lambda m: color.to_hex(tuple(int(m.group(k)) / 255 for k in (1, 2, 3)))),
        ("font_size", r"fontSize\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("font_size", r"\btext-\[(\d+)px\]", lambda m: _num(m.group(1))),
        ("spacing", r"\b(?:margin|padding)(?:Top|Bottom|Left|Right|Horizontal|Vertical|Start|End)?\s*:\s*([\d.]+)\b", lambda m: _num(m.group(1))),
        ("spacing", r"\b(?:gap|rowGap|columnGap)\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("spacing", r"\b[pm][xytrbl]?-\[(\d+)px\]", lambda m: _num(m.group(1))),
        ("radius", r"borderRadius\s*:\s*([\d.]+)", lambda m: _num(m.group(1))),
        ("radius", r"\brounded-\[(\d+)px\]", lambda m: _num(m.group(1))),
        ("duration", r"duration\s*:\s*(\d+)", lambda m: int(m.group(1))),
        ("curve", r"Easing\.(linear|bounce|elastic|ease|bezier|inOut|out|in)\b", lambda m: m.group(1)),
        ("icon", r"from\s+['\"](lucide-react(?:-native)?|@expo/vector-icons[^'\"]*|react-native-vector-icons/\w+|phosphor-react(?:-native)?|@heroicons/react[^'\"]*|react-icons/\w+|@tabler/icons-react|iconsax-react(?:-native)?|@mui/icons-material|react-native-heroicons[^'\"]*)['\"]",
         lambda m: "/".join(m.group(1).split("/")[:2]) if m.group(1).startswith("@") else m.group(1).split("/")[0]),
    ],
    "css": [
        ("color", r"(#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?|#[0-9A-Fa-f]{3})\b", lambda m: m.group(1).upper()),
        ("color", r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", lambda m: color.to_hex(tuple(int(m.group(k)) / 255 for k in (1, 2, 3)))),
        ("font_size", r"font-size\s*:\s*([\d.]+)px", lambda m: _num(m.group(1))),
        ("font_size", r"font-size\s*:\s*([\d.]+)rem", lambda m: _num(round(float(m.group(1)) * 16, 1))),
        ("spacing", r"\b(?:margin|padding|gap|row-gap|column-gap)(?:-[a-z]+)?\s*:\s*([^;}{]+)", None),
        ("radius", r"border-radius\s*:\s*([\d.]+)px", lambda m: _num(m.group(1))),
        ("duration", r"(?:transition|animation)(?:-duration)?\s*:[^;]*?(\d+)ms", lambda m: int(m.group(1))),
        ("duration", r"(?:transition|animation)(?:-duration)?\s*:[^;]*?\b(\d*\.?\d+)s\b", lambda m: int(float(m.group(1)) * 1000)),
    ],
}
EXTRACT["tsx"] = [e for e in EXTRACT["tsx"] if e]

# direct signals: (rule, tier, severity, evidence, regex, message, fix)
SIG = {
    "flutter": [
        ("D17", "D", "minor", "inferred", r"\bKSpace\.\w+\s*[-+]\s*\d+(?:\.\d+)?\b|\bKSpace\.\w+\s*/\s*\d", "spacing token arithmetic (often lands off the grid)", "use a scale step; add one to the scale if it is genuinely missing"),
        ("F02", "F", "major", "observed", r"\bon(?:Pressed|Tap|LongPress|Changed|Submitted)\s*:\s*\(\s*\w?\s*\)\s*(?:\{\s*\}|=>\s*\{\s*\})", "empty handler: the control looks active but does nothing", "wire the action; while loading/unavailable pass null so it renders disabled"),
        ("F10", "F", "block", "observed", r"TextScaler\.noScaling|textScaleFactor\s*:\s*1(?:\.0)?\b|TextScaler\.linear\(\s*1(?:\.0)?\s*\)", "user text size is locked", "support text scaling; reflow at large sizes (withClampedTextScaling only with a stated maximum ≥ 2.0)"),
        ("F05", "F", "major", "observed", r"MaterialTapTargetSize\.shrinkWrap", "tap target shrunk below 48dp", "keep the padded tap target; shrink the glyph instead"),
        ("D28", "D", "major", "observed", r"\bFittedBox\(", "FittedBox used as a layout patch", "reflow the layout; give critical text room"),
        ("D28", "D", "info", "observed", r"TextOverflow\.ellipsis", "ellipsis truncation (fine for secondary text, harmful on critical content)", "check each: wrap or restructure titles, prices, CTAs and legal text"),
        ("D30", "D", "major", "observed", r"seedColor\s*:\s*Colors\.(deepPurple|purple|indigo)|primarySwatch\s*:\s*Colors\.blue\b", "Flutter template default palette left in place", "make the palette a decision from the thesis (`kinetic palette`)"),
        ("D26", "D", "minor", "inferred", r"\bShaderMask\(", "ShaderMask (often gradient text / glow)", "carry emphasis with weight, size, color"),
        ("D05", "D", "minor", "observed", r"\bBackdropFilter\(|ImageFilter\.blur", "blur filter", "native materials on bars/sheets only; never as card decoration"),
        ("D09", "D", "minor", "inferred", r"\bFloatingActionButton(?:\.\w+)?\(", "floating action button", "on iOS use a nav-bar/toolbar action; on Android only for creation-first screens"),
        ("D08", "D", "minor", "inferred", r"\bdrawer\s*:\s*Drawer\(|\bNavigationDrawer\(", "navigation drawer", "drawers hide navigation; avoid on iOS; prefer tabs or a hub"),
        ("D20", "D", "info", "inferred", r"\bShimmer\b|\bSkeletonizer\b|\bskeleton", "skeleton/shimmer loading", "only when layout is known and the wait exceeds ~300ms"),
        ("D23", "D", "minor", "inferred", r"\bonHover\s*:|\bMouseRegion\(", "hover-dependent interaction", "phones have no hover; provide tap/long-press equivalents"),
        ("D29", "D", "major", "observed", r"\b(?:width|height)\s*:\s*(?:375|390|393|402|414|428|430|440|667|736|812|844|852|874|896|926|932|956)(?:\.0)?\b", "mockup device dimension hard-coded", "use constraints (LayoutBuilder, Expanded, MediaQuery.sizeOf)"),
        ("D11", "D", "info", "inferred", r"textAlign\s*:\s*TextAlign\.center", "centered text", "center only single-focus moments; align paragraphs to a reading edge"),
        ("D16", "D", "info", "observed", r"\bBoxShadow\(", "box shadow", "pick one elevation strategy per system"),
        ("D27", "D", "info", "inferred", r"\b(confetti|ConfettiWidget|streak)\b", "gamified decoration", "celebrate only real milestones"),
        ("D21", "D", "info", "inferred", r"\bPageView(?:\.builder)?\(", "PageView (carousel onboarding?)", "deliver value first; avoid 3-screen benefit carousels"),
        ("D25", "D", "info", "observed", r"\b(?:Chip|FilterChip|ChoiceChip|Badge)\(", "chip/badge", "badges only for state the user must notice"),
        ("D10", "D", "info", "observed", r"\bshowDialog\(|\bSnackBar\(|showModalBottomSheet\(|Fluttertoast", "interruptive feedback", "inline confirmation and undo before dialogs/toasts"),
        ("D03", "D", "info", "observed", r"\bCard\(", "Card container", "cards for equivalent records only"),
    ],
    "swiftui": [
        ("D17", "D", "minor", "inferred", r"\bKSpace\.\w+\s*[-+]\s*\d+(?:\.\d+)?\b|\bKSpace\.\w+\s*/\s*\d", "spacing token arithmetic (often lands off the grid)", "use a scale step; add one to the scale if it is genuinely missing"),
        ("D29", "D", "info", "observed", r"\.frame\(\s*width\s*:\s*\d{3,}\s*,\s*height\s*:\s*\d{2,}", "literal frame size", "derive from content, tokens or the container"),
        ("F02", "F", "block", "observed", r"Button\(\s*\"[^\"]*\"\s*\)\s*\{\s*\}|action\s*:\s*\{\s*\}|Button\s*\{\s*\}\s*label", "empty button action", "wire the action or remove the control"),
        ("F10", "F", "block", "observed", r"\.dynamicTypeSize\(\s*\.(?:xSmall|small|medium|large|xLarge|xxLarge)\s*\)|\.custom\([^)]*fixedSize\s*:", "Dynamic Type locked", "use relativeTo:/text styles; restrict with a range only per view and with a reason"),
        ("D28", "D", "major", "observed", r"\.minimumScaleFactor\(", "text shrinks to fit", "reflow (ViewThatFits, wrapping) instead of shrinking"),
        ("D05", "D", "minor", "observed", r"\.(?:ultraThin|thin|regular|thick|ultraThick)Material\b|\.blur\(\s*radius", "material/blur", "materials belong to bars, sheets and overlays above moving content"),
        ("D26", "D", "minor", "inferred", r"\.foregroundStyle\(\s*(?:LinearGradient|AngularGradient|RadialGradient)|\.mask\(\s*Text", "gradient on text", "weight, size and one color carry emphasis"),
        ("D08", "D", "minor", "inferred", r"\"line\.3\.horizontal\"|\"line\.horizontal\.3\"", "hamburger menu icon on iOS", "tab bar or a hub screen; avoid hidden navigation"),
        ("D29", "D", "major", "observed", r"\.frame\([^)]*(?:width|height)\s*:\s*(?:375|390|393|402|414|428|430|440|667|736|812|844|852|874|896|926|932|956)(?:\.0)?\b", "mockup device dimension hard-coded", "use flexible frames, containerRelativeFrame, safe areas"),
        ("D11", "D", "info", "inferred", r"\.multilineTextAlignment\(\s*\.center\s*\)", "centered multi-line text", "center only single-focus moments"),
        ("D16", "D", "info", "observed", r"\.shadow\(", "shadow", "pick one elevation strategy per system"),
        ("D23", "D", "minor", "inferred", r"\.onHover\b", "hover-dependent interaction", "provide tap/long-press/context-menu equivalents"),
        ("D27", "D", "info", "inferred", r"\b(confetti|streak)\b", "gamified decoration", "celebrate only real milestones"),
        ("D21", "D", "info", "inferred", r"\.tabViewStyle\(\s*\.page", "paged TabView (carousel onboarding?)", "deliver value first"),
        ("D10", "D", "info", "observed", r"\.alert\(|\.confirmationDialog\(", "alert/dialog", "dialogs only for destructive or blocking decisions"),
        ("D09", "D", "minor", "inferred", r"Circle\(\)[^\n]{0,80}\n?[^\n]{0,80}(?:bottomTrailing|\.overlay\(alignment:\s*\.bottomTrailing)", "floating circular action button (FAB pattern)", "use a toolbar or nav-bar action on iOS"),
        ("D24", "D", "minor", "inferred", r"\bRipple\b|\bFloatingActionButton\b", "Material idiom in SwiftUI", "use iOS-native feedback and actions"),
    ],
    "compose": [
        ("F02", "F", "block", "observed", r"onClick\s*=\s*\{\s*\}", "empty click handler", "wire the action or remove the control"),
        ("F10", "F", "block", "observed", r"fontScale\s*=\s*1(?:\.0)?f", "font scale locked", "respect the user's font scale; reflow"),
        ("D28", "D", "info", "observed", r"TextOverflow\.Ellipsis", "ellipsis truncation", "check each: wrap or restructure critical text"),
        ("D28", "D", "major", "observed", r"\bautoSize\b|TextAutoSize", "auto-shrinking text", "reflow instead of shrinking"),
        ("D05", "D", "minor", "observed", r"Modifier\.blur\(|\.blur\(\s*\d", "blur", "reserve for overlays"),
        ("D29", "D", "major", "observed", r"\.(?:width|height|size)\(\s*(?:360|375|390|393|411|412|414|640|731|800|812|844|851|915)\.dp", "mockup device dimension hard-coded", "use fillMaxWidth, weights, WindowSizeClass"),
        ("D11", "D", "info", "inferred", r"textAlign\s*=\s*TextAlign\.Center", "centered text", "center only single-focus moments"),
        ("D16", "D", "info", "observed", r"\.shadow\(|elevation\s*=\s*\d", "shadow/elevation", "Material 3 prefers tonal elevation"),
        ("D23", "D", "minor", "inferred", r"\bhoverable\(|onPointerEvent", "hover-dependent interaction", "provide tap equivalents"),
        ("D30", "D", "minor", "inferred", r"Purple40|Purple80|PurpleGrey40|Pink40|Pink80", "Android Studio template colors left in place", "make the palette a decision (`kinetic palette`)"),
        ("D10", "D", "info", "observed", r"\bAlertDialog\(|\bSnackbar\(|Toast\.makeText", "interruptive feedback", "inline confirmation and undo before dialogs/toasts"),
        ("D03", "D", "info", "observed", r"\b(?:Card|ElevatedCard|OutlinedCard)\(", "Card container", "cards for equivalent records only"),
        ("D25", "D", "info", "observed", r"\b(?:AssistChip|FilterChip|SuggestionChip|InputChip|Badge)\(", "chip/badge", "badges only for state the user must notice"),
    ],
    "tsx": [
        ("F02", "F", "block", "observed", r"on(?:Press|Click|LongPress)\s*=\s*\{\s*\(\s*\)\s*=>\s*\{\s*\}\s*\}|href\s*=\s*[\"']#[\"']", "control does nothing", "wire the action or remove the control"),
        ("F10", "F", "block", "observed", r"allowFontScaling\s*=\s*\{\s*false\s*\}|maxFontSizeMultiplier\s*=\s*\{\s*1(?:\.0)?\s*\}|user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?\b", "user text size or zoom is locked", "allow scaling; reflow at large sizes"),
        ("D28", "D", "major", "observed", r"adjustsFontSizeToFit", "text shrinks to fit", "reflow instead"),
        ("D01", "D", "major", "inferred", r"\b(?:from|via|to)-(?:purple|violet|indigo|fuchsia|pink)-\d{2,3}\b", "violet/indigo/pink gradient utility classes (the AI gradient)", "solid surface + one accent; meaningful gradients only"),
        ("D26", "D", "major", "observed", r"bg-clip-text[^\"'`]*text-transparent|text-transparent[^\"'`]*bg-clip-text|WebkitBackgroundClip\s*:\s*['\"]text", "gradient text", "weight, size and color carry emphasis"),
        ("D05", "D", "minor", "observed", r"\bbackdrop-blur\b|\bBlurView\b|backdropFilter", "blur", "reserve for overlays over moving content"),
        ("D16", "D", "info", "observed", r"\bshadow-(?:lg|xl|2xl)\b|shadowOpacity|boxShadow", "shadow", "pick one elevation strategy"),
        ("D23", "D", "minor", "inferred", r"onHoverIn|onMouseEnter|\bhover:", "hover-dependent interaction", "phones have no hover; provide tap equivalents"),
        ("D29", "D", "major", "observed", r"(?:width|height)\s*:\s*(?:375|390|393|414|428|430|667|812|844|852|896|926|932)\b|\bh-screen\b|100vh", "fixed device size or 100vh (breaks with mobile browser chrome)", "flex layout; 100dvh/svh on web"),
        ("D11", "D", "info", "inferred", r"textAlign\s*:\s*['\"]center['\"]|\btext-center\b", "centered text", "center only single-focus moments"),
        ("D10", "D", "info", "observed", r"Alert\.alert\(|\btoast\(|Toast\.show", "interruptive feedback", "inline confirmation and undo"),
        ("D27", "D", "info", "inferred", r"\b(confetti|streak)\b", "gamified decoration", "celebrate only real milestones"),
    ],
    "css": [
        ("F10", "F", "block", "observed", r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?\b", "zoom is locked", "allow zoom"),
        ("D26", "D", "major", "observed", r"background-clip\s*:\s*text", "gradient text", "weight, size and color carry emphasis"),
        ("D05", "D", "minor", "observed", r"backdrop-filter\s*:\s*blur", "blur", "reserve for overlays"),
        ("D29", "D", "minor", "observed", r"\b100vh\b", "100vh on mobile (jumps with browser chrome)", "use 100dvh/svh"),
        ("D16", "D", "info", "observed", r"box-shadow\s*:", "shadow", "pick one elevation strategy"),
        ("D19", "D", "minor", "inferred", r"transition[^;]*\blinear\b", "linear easing on a UI transition", "ease-out or a spring approximation for UI"),
    ],
}

GRADIENT_START = {
    "flutter": r"\b(?:Linear|Radial|Sweep)Gradient\(",
    "swiftui": r"\b(?:Linear|Radial|Angular|Elliptical|Mesh)Gradient\(",
    "compose": r"Brush\.(?:linear|horizontal|vertical|radial|sweep)Gradient\(",
    "tsx": r"<LinearGradient\b|linear-gradient\(|radial-gradient\(",
    "css": r"linear-gradient\(|radial-gradient\(|conic-gradient\(",
}
ANIMATION = {
    "flutter": r"AnimationController\(|Animated[A-Z]\w*\(|TweenAnimationBuilder|\.animate\(|Hero\(|AnimatedSwitcher|SpringSimulation",
    "swiftui": r"withAnimation|\.animation\(|\.transition\(|matchedGeometryEffect|PhaseAnimator|KeyframeAnimator|\.symbolEffect",
    "compose": r"animate\w*AsState|AnimatedVisibility|AnimatedContent|Animatable\(|updateTransition|rememberInfiniteTransition|animateContentSize",
    "tsx": r"useSharedValue|withTiming|withSpring|Animated\.|LayoutAnimation|framer-motion|motion\.[a-z]+|entering=\{|@keyframes|animation\s*:",
    "css": r"@keyframes|animation\s*:|transition\s*:",
}
REDUCE_MOTION = re.compile(r"disableAnimations|accessibilityReduceMotion|isReduceMotionEnabled|useReducedMotion|ReduceMotion|prefers-reduced-motion|ANIMATOR_DURATION_SCALE|reduceMotion|reducedMotion", re.I)
HAPTIC = re.compile(r"HapticFeedback|sensoryFeedback|UIImpactFeedbackGenerator|UISelectionFeedbackGenerator|UINotificationFeedbackGenerator|performHapticFeedback|expo-haptics|Haptics\.")
ENTRANCE = re.compile(r"\.fadeIn\(|\.slide[XY]\(|FadeIn\w*|SlideIn\w*|\.transition\(\s*\.(?:opacity|move|slide|push|scale)|initial=\{\{\s*opacity\s*:\s*0|fadeIn\(\)|slideIn\w*\(|\.onAppear\s*\{\s*withAnimation")
BOUNCE = {
    "flutter": re.compile(r"Curves\.(bounce\w*|elastic\w*)"),
    "swiftui": re.compile(r"\.bouncy\b|\.interpolatingSpring|dampingFraction\s*:\s*0?\.[0-5]\d*\b|bounce\s*:\s*0?\.[3-9]"),
    "compose": re.compile(r"DampingRatio(?:High|Medium)Bouncy|dampingRatio\s*=\s*0?\.[0-4]\d*f"),
    "tsx": re.compile(r"Easing\.(?:bounce|elastic)|bounciness\s*:\s*[1-9]|damping\s*:\s*[1-5]\b"),
    "css": re.compile(r"cubic-bezier\([^)]*?,\s*(?:1\.[3-9]|[2-9]\.\d)"),
}
LINEAR = {
    "flutter": re.compile(r"Curves\.linear\b"),
    "swiftui": re.compile(r"(?:withAnimation\(|\.animation\(|Animation)\s*\.linear\b"),
    "compose": re.compile(r"\bLinearEasing\b"),
    "tsx": re.compile(r"Easing\.linear\b"),
    "css": re.compile(r"$^"),
}


# ------------------------------------------------------------ the scanner
class Scanner:
    def __init__(self, platforms=("ios", "android"), grid=4, theme_paths=None, data_hexes=()):
        self.data_hexes = {h.upper()[:7] for h in data_hexes}
        self.platforms = set(platforms or ())
        self.grid = grid
        self.theme_paths = [re.compile(p) for p in (theme_paths or [])]

    def lang_of(self, path: str, text: str):
        ext = os.path.splitext(path)[1].lower()
        lang = LANG_BY_EXT.get(ext)
        if ext == ".kt" and "@Composable" not in text and "androidx.compose" not in text:
            return "compose" if re.search(r"Color\(0x|\.dp\b|\.sp\b", text) else None
        if ext in (".ts", ".js") and not re.search(r"react|StyleSheet|className|jsx", text):
            return None
        return lang

    def is_theme(self, path: str) -> bool:
        if any(p.search(path) for p in self.theme_paths):
            return True
        return bool(THEME_PATH.search(os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path)))

    def scan_text(self, path: str, text: str, lang: str) -> FileScan:
        fs = FileScan(path=path, lang=lang, loc=text.count("\n") + 1)
        fs.fixture = bool(FIXTURE_PATH.search(os.path.basename(path)))
        themed = self.is_theme(path)
        lines = list(_code_lines(text))
        themes, current = {}, "light"
        for no, line in lines:  # which theme block each line belongs to (`static let dark = Palette(`, `case .dark:`)
            m = BLOCK_THEME.search(line)
            if m:
                word = next(g for g in m.groups() if g)
                current = "dark" if word.lower() in ("dark", "night") else "light"
            themes[no] = current
        for kind, rx, conv in EXTRACT.get(lang, []):
            cre = re.compile(rx)
            for no, line in lines:
                for m in cre.finditer(line):
                    if conv is None:
                        for v in self._spacing_list(m.group(1), lang):
                            fs.facts.append(Fact(kind, v, path, no, m.group(0)[:80], themed))
                        continue
                    try:
                        v = conv(m)
                    except (ValueError, TypeError, ZeroDivisionError):
                        v = None
                    if v is not None:
                        th = themes.get(no, "light")
                        if kind == "color":
                            hx = str(v)[1:7]
                            if re.search(rf"(?i)\b(?:k?dark\w*)\s*[:=]\s*[^,)]*?{hx}", line):
                                th = "dark"
                            elif re.search(rf"(?i)\b(?:k?light\w*)\s*[:=]\s*[^,)]*?{hx}", line):
                                th = "light"
                        fs.facts.append(Fact(kind, v, path, no, m.group(0)[:80], themed, line.strip()[:200], th))
        for rule, tier, sev, ev, rx, msg, fix in SIG.get(lang, []):
            cre = re.compile(rx)
            for no, line in lines:
                if cre.search(line):
                    fs.findings.append(Finding(rule=rule, tier=tier, severity=sev, evidence=ev, file=path,
                                               line=no, message=msg, fix=fix, snippet=line.strip()[:120]))
                    fs.flags[rule] += 1
        if lang == "tsx" and re.search(r"from\s+['\"]react-native['\"]", text):
            fs.flags["react_native"] = 1
        if re.search(r"SafeAreaView|useSafeAreaInsets|SafeAreaProvider|safeAreaInset|env\(safe-area-inset", text):
            fs.flags["safe_area"] = 1
        if lang == "flutter" and re.search(r"Cupertino|\.adaptive\(|TargetPlatform|Platform\.isIOS|defaultTargetPlatform", text):
            fs.flags["adaptive"] = 1
        self._structural(fs, text, lang)
        self._strings(fs, lines, lang)
        self._motion(fs, lines, lang, text)
        self._gradients(fs, text, lang)
        if fs.fixture:  # previews/fixtures: keep integrity findings, drop system/layout ones
            fs.findings = [f for f in fs.findings if f.tier == "F" and f.rule not in ("F01",)]
        return fs

    def _spacing_list(self, args: str, lang: str):
        if lang == "css":
            out = []
            for tok in re.findall(r"(-?[\d.]+)(px|rem)?", args):
                v = _num(tok[0])
                if v is None or v <= 0:
                    continue
                out.append(_num(round(float(v) * 16, 1)) if tok[1] == "rem" else v)
            return out if re.search(r"px|rem|\b0\b", args) else []
        nums = re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])", args)
        return [v for v in (_num(n) for n in nums) if v is not None and v > 0]

    # structural heuristics needing more than one line
    def _structural(self, fs: FileScan, text: str, lang: str):
        if lang == "flutter":
            for m in re.finditer(r"\bIconButton(?:\.(?:filled|filledTonal|outlined))?\(", text):
                reg = _region(text, m.start(), 900)
                if "tooltip" not in reg and "Semantics" not in text[max(0, m.start() - 200):m.start()] \
                        and "semanticLabel" not in reg:
                    fs.findings.append(Finding(rule="F07", tier="F", severity="major", evidence="inferred",
                                               file=fs.path, line=_line_at(text, m.start()),
                                               message="icon-only IconButton without tooltip/semantic label",
                                               fix="add `tooltip:` (also used as the accessibility label)"))
            tabs = len(re.findall(r"\b(?:BottomNavigationBarItem|NavigationDestination)\(", text))
            if tabs >= 5:
                fs.findings.append(Finding(rule="D08", tier="D", severity="minor", evidence="observed", file=fs.path,
                                           line=_line_at(text, text.find("Navigation")),
                                           message=f"{tabs} bottom navigation destinations",
                                           fix="3–4 parallel top-level areas; actions don't belong in tabs"))
        elif lang == "swiftui":
            for m in re.finditer(r"\bButton\b\s*[({]", text):
                reg = _closures(text, m.start(), 700)
                tail = text[m.start() + len(reg):].split("\n")
                mods = [tail[0]] + [ln for ln in itertools.takewhile(
                    lambda ln: ln.strip().startswith("."), tail[1:8])]
                after = reg + "\n".join(mods)
                if "Image(systemName" in reg and not re.search(r"\bText\(|\bLabel\(", reg) \
                        and ".accessibilityLabel" not in after:
                    fs.findings.append(Finding(rule="F07", tier="F", severity="major", evidence="inferred",
                                               file=fs.path, line=_line_at(text, m.start()),
                                               message="icon-only Button without accessibilityLabel",
                                               fix="use Label(\"Title\", systemImage:) with .labelStyle(.iconOnly) or add .accessibilityLabel"))
                frames = re.findall(r"\.frame\(\s*(?:min)?[wW]idth\s*:\s*(\d+)\s*,\s*(?:min)?[hH]eight\s*:\s*(\d+)", after)
                fm = re.search(r"\.frame\(\s*width\s*:\s*(\d+)\s*,\s*height\s*:\s*(\d+)", after)
                biggest = max((min(int(w), int(h)) for w, h in frames), default=0)
                if fm and biggest < 44 and ".contentShape" not in after and ".padding" not in after:
                    fs.findings.append(Finding(rule="F05", tier="F", severity="major", evidence="inferred",
                                               file=fs.path, line=_line_at(text, m.start()),
                                               message=f"button frame {fm.group(1)}×{fm.group(2)} below 44pt",
                                               fix="pad the hit area to 44×44 (.frame(minWidth:44,minHeight:44).contentShape(Rectangle()))"))
        elif lang == "compose":
            for m in re.finditer(r"\bIconButton\(", text):
                reg = _closures(text, m.start(), 900)
                if re.search(r"contentDescription\s*=\s*null", reg):
                    fs.findings.append(Finding(rule="F07", tier="F", severity="major", evidence="observed",
                                               file=fs.path, line=_line_at(text, m.start()),
                                               message="IconButton icon has contentDescription = null",
                                               fix="describe the action in contentDescription"))
            for m in re.finditer(r"Modifier\s*\.size\(\s*(\d+)\.dp\s*\)\s*\.clickable", text):
                if int(m.group(1)) < 48:
                    fs.findings.append(Finding(rule="F05", tier="F", severity="major", evidence="observed",
                                               file=fs.path, line=_line_at(text, m.start()),
                                               message=f"clickable area {m.group(1)}dp below 48dp",
                                               fix="use minimumInteractiveComponentSize() or pad to 48dp"))
        elif lang == "tsx":
            for m in re.finditer(r"<(Pressable|TouchableOpacity|TouchableHighlight|TouchableWithoutFeedback|button|IconButton)\b", text):
                end = text.find(f"</{m.group(1)}>", m.start())
                reg = text[m.start(): end if end != -1 and end - m.start() < 1200 else m.start() + 400]
                has_icon = re.search(r"<\w*Icon\b|<(?:Ionicons|Feather|MaterialIcons|MaterialCommunityIcons|FontAwesome\w*|AntDesign|Entypo|svg|Svg)\b", reg)
                has_text = re.search(r"<Text\b|>\s*[A-Za-zÀ-ÿ]{2,}", reg[reg.find(">") + 1:] if ">" in reg else "")
                if has_icon and not has_text and not re.search(r"accessibilityLabel|aria-label|title=", reg):
                    fs.findings.append(Finding(rule="F07", tier="F", severity="major", evidence="inferred",
                                               file=fs.path, line=_line_at(text, m.start()),
                                               message=f"icon-only <{m.group(1)}> without accessibilityLabel/aria-label",
                                               fix="add accessibilityLabel (RN) or aria-label (web)"))

    def _strings(self, fs: FileScan, lines, lang: str):
        ui_file = not re.search(r"(model|service|repository|api|dto|entity|test|mock|fixture|logger|log)s?\b",
                                os.path.basename(fs.path), re.I)
        log_depth = 0
        for no, line in lines:
            if log_depth > 0:
                log_depth += line.count("(") - line.count(")")
                continue
            m = LOG_LINE.search(line)
            if m:
                log_depth = max(0, line[m.start():].count("(") - line[m.start():].count(")"))
                continue
            if re.search(r"^\s*(import|export\s+\*|package|@)", line):
                continue
            chunks = [a or b for a, b in STRING_LIT.findall(line)]
            if lang == "tsx":
                chunks += JSX_TEXT.findall(line)
            for s in chunks:
                if not ui_file:
                    break
                if LOG_TAG.search(s):
                    continue
                if EMOJI.search(s):
                    fs.findings.append(Finding(rule="D06", tier="D", severity="minor", evidence="observed", file=fs.path,
                                               line=no, message=f"emoji in UI text: {s[:50]!r}",
                                               fix="use the icon system, or remove; emoji are not icons", snippet=s[:80]))
                if GREETING.search(s):
                    fs.findings.append(Finding(rule="D02", tier="D", severity="major", evidence="inferred", file=fs.path,
                                               line=no, message=f"greeting copy: {s[:50]!r}",
                                               fix="lead with what the user came for, not a salutation", snippet=s[:80]))
                if COPY_SLOP.search(s):
                    fs.findings.append(Finding(rule="D22", tier="D", severity="minor", evidence="observed", file=fs.path,
                                               line=no, message=f"copy slop: {s[:60]!r}",
                                               fix="name the concrete thing and outcome (knowledge/copy.md)", snippet=s[:80]))
                if FAKE_PROOF.search(s):
                    fs.findings.append(Finding(rule="F01", tier="F", severity="major", evidence="inferred", file=fs.path,
                                               line=no, message=f"proof-like claim in a literal: {s[:60]!r}",
                                               fix="show real data, or a clearly labelled placeholder; never invent proof", snippet=s[:80]))

    def _motion(self, fs: FileScan, lines, lang: str, text: str):
        anim = re.compile(ANIMATION.get(lang, r"$^"))
        for no, line in lines:
            if anim.search(line):
                fs.flags["animation"] += 1
                fs.facts.append(Fact("animation", 1, fs.path, no, line.strip()[:60]))
            if REDUCE_MOTION.search(line):
                fs.flags["reduce_motion"] += 1
            if ENTRANCE.search(line):
                fs.flags["entrance"] += 1
            b = BOUNCE.get(lang)
            if b and b.search(line):
                fs.findings.append(Finding(rule="D19", tier="D", severity="minor", evidence="observed", file=fs.path,
                                           line=no, message="bouncy/elastic motion",
                                           fix="critically damped springs for UI; overshoot only for direct manipulation or expression ≥4",
                                           snippet=line.strip()[:100]))
            lin = LINEAR.get(lang)
            if lin and lin.search(line) and not re.search(r"repeat|progress|loop|forever|infinite", line, re.I):
                fs.findings.append(Finding(rule="D19", tier="D", severity="info", evidence="inferred", file=fs.path,
                                           line=no, message="linear easing on UI motion",
                                           fix="linear is for progress and loops; UI motion wants ease-out or springs",
                                           snippet=line.strip()[:100]))
            if HAPTIC.search(line):
                fs.flags["haptics"] += 1
        if fs.flags["entrance"] >= 4:
            fs.findings.append(Finding(rule="D18", tier="D", severity="minor", evidence="inferred", file=fs.path,
                                       line=0, message=f"{fs.flags['entrance']} entrance animations in one file",
                                       fix="animate what changed, where it changed; content that was there stays still"))

    def _gradients(self, fs: FileScan, text: str, lang: str):
        start = GRADIENT_START.get(lang)
        if not start:
            return
        for m in re.finditer(start, text):
            reg = _region(text, m.start(), 600)
            hexes = []
            for kind, rx, conv in EXTRACT.get(lang, []):
                if kind != "color":
                    continue
                for cm in re.finditer(rx, reg):
                    try:
                        v = conv(cm) if conv else None
                    except (ValueError, TypeError, ZeroDivisionError):
                        v = None
                    if v:
                        hexes.append(v[:7])
            if lang == "swiftui":
                hexes += [SWIFT_COLORS[n] for n in re.findall(r"\.(\w+)\b", reg) if n in SWIFT_COLORS]
            if lang == "flutter":
                hexes += [MATERIAL_COLORS[n] for n in re.findall(r"Colors\.(\w+)", reg) if n in MATERIAL_COLORS]
            fs.flags["gradient"] += 1
            purple = [h for h in hexes if color.is_hex(h) and color.is_ai_purple(h)]
            ln = _line_at(text, m.start())
            if purple:
                fs.findings.append(Finding(rule="D01", tier="D", severity="major", evidence="inferred", file=fs.path,
                                           line=ln, message=f"violet/indigo/pink gradient ({', '.join(purple[:3])})",
                                           fix="solid surface + one accent; a gradient must carry meaning (time, data, brand) and stay low-chroma"))
            elif len(hexes) >= 2:
                chroma = [color.hex_to_oklch(h)[1] for h in hexes if color.is_hex(h)]
                if chroma and max(chroma) > 0.15:
                    fs.findings.append(Finding(rule="C04", tier="C", severity="info", evidence="inferred", file=fs.path,
                                               line=ln, message="high-chroma gradient",
                                               fix="confirm it carries meaning; keep stops few and chroma low"))

    # ------------------------------------------------------------- walk
    def scan_paths(self, paths) -> dict:
        files, unknown, skipped = [], [], Counter()
        absroots = [os.path.abspath(p if os.path.isdir(p) else os.path.dirname(p)) for p in paths]
        self.root = os.path.commonpath(absroots) if absroots else None
        for root in paths:
            if os.path.isfile(root):
                cand = [root]
            else:
                cand = []
                for dp, dns, fns in os.walk(root):
                    rel = os.path.relpath(dp, root)
                    dns[:] = [d for d in dns if d not in EXCLUDE_DIRS and not d.startswith(".")
                              and not any(rel.endswith(x) for x in ("android/app/build",))]
                    for fn in fns:
                        cand.append(os.path.join(dp, fn))
            for p in cand:
                p = os.path.abspath(p)
                ext = os.path.splitext(p)[1].lower()
                if ext not in LANG_BY_EXT or SKIP_FILE.search(p):
                    if ext in LANG_BY_EXT:
                        skipped["generated_or_test"] += 1
                    continue
                try:
                    if os.path.getsize(p) > 600_000:
                        unknown.append({"file": p, "reason": "file larger than 600 KB not scanned"})
                        continue
                    with open(p, encoding="utf-8", errors="replace") as fh:
                        text = fh.read()
                except OSError as e:
                    unknown.append({"file": p, "reason": str(e)})
                    continue
                lang = self.lang_of(p, text)
                if not lang:
                    skipped["not_ui_source"] += 1
                    continue
                files.append(self.scan_text(p, text, lang))
        return self.aggregate(files, unknown, skipped)

    # --------------------------------------------------------- project-level
    def aggregate(self, files, unknown, skipped) -> dict:
        fixtures = [fs.path for fs in files if fs.fixture]
        facts = [f for fs in files if not fs.fixture for f in fs.facts]
        findings = [f for fs in files for f in fs.findings]
        by_kind = defaultdict(list)
        for f in facts:
            by_kind[f.kind].append(f)
        loc = sum(fs.loc for fs in files)

        def first(kind, pred=lambda f: True):
            for f in by_kind[kind]:
                if pred(f):
                    return f
            return None

        # type sizes
        sizes = Counter(f.value for f in by_kind["font_size"] if isinstance(f.value, (int, float)))
        if len(sizes) > 8:
            f0 = first("font_size")
            findings.append(Finding(rule="D12", tier="D", severity="major", evidence="derived", file=f0.file, line=f0.line,
                                    message=f"{len(sizes)} distinct font sizes: {', '.join(str(s) for s, _ in sorted(sizes.items()))}",
                                    fix="consolidate into a 5–8 step ramp (`kinetic dna --kdl` proposes one)"))
        raw_sizes = len(by_kind["font_size"])
        styled = len(by_kind["text_style"])
        if raw_sizes >= 10 and styled < raw_sizes / 3:
            findings.append(Finding(rule="D12", tier="D", severity="minor", evidence="derived", file="", line=0,
                                    message=f"{raw_sizes} literal font sizes vs {styled} semantic text-style uses",
                                    fix="route text through theme styles so Dynamic Type and consistency follow"))
        # colors
        def dedupe(hexes):
            out = []
            for h in hexes:
                if color.is_hex(h) and all(color.delta_e_ok(h, u) > 0.02 for u in out):
                    out.append(h)
            return out

        def is_data(f):
            return bool(str(f.value).upper()[:7] in self.data_hexes or DATA_PATH.search(os.path.basename(f.file))
                        or DATA_CONTEXT.search(f.context))

        def is_dark(f):
            return f.theme == "dark"

        ui_colors = [f for f in by_kind["color"] if not is_data(f)]
        uniq = dedupe([str(f.value)[:7] for f in by_kind["color"]])
        light_n = [h for h in dedupe([str(f.value)[:7] for f in ui_colors if not is_dark(f)]) if color.hex_to_oklch(h)[1] < 0.03]
        dark_n = [h for h in dedupe([str(f.value)[:7] for f in ui_colors if is_dark(f)]) if color.hex_to_oklch(h)[1] < 0.03]
        neutrals = dedupe(light_n + dark_n)
        hues = Counter(color.hue_family(color.hex_to_oklch(h)[2], color.hex_to_oklch(h)[1])
                       for h in dedupe([str(f.value)[:7] for f in ui_colors]) if color.hex_to_oklch(h)[1] >= 0.06)
        data_hues = len(uniq) - len(dedupe([str(f.value)[:7] for f in ui_colors]))
        # each theme legitimately holds ~6–8 neutral roles; status/data hues are separate, legitimate roles
        worst = max(len(light_n), len(dark_n))
        if worst > 8:
            findings.append(Finding(rule="D13", tier="D", severity="major" if worst > 11 else "minor",
                                    evidence="derived", file="", line=0,
                                    message=f"{worst} distinct neutrals in one theme (light {len(light_n)}, dark {len(dark_n)}): "
                                            f"{', '.join((light_n if len(light_n) >= len(dark_n) else dark_n)[:10])}",
                                    fix="one neutral ramp per theme (≈6–8 roles), tinted from the seed; roles, not values"))
        if len(hues) > 3:
            findings.append(Finding(rule="D13", tier="D", severity="major" if len(hues) > 5 else "minor",
                                    evidence="derived", file="", line=0,
                                    message=f"{len(hues)} saturated hue families: {', '.join(sorted(hues))}",
                                    fix="one accent carries meaning; status (danger/success/warning) and data colors must be separate, named roles"))
        hard = Counter(f.file for f in by_kind["color"] if not f.themed)
        heavy = [(p, n) for p, n in hard.most_common() if n >= 3]
        if heavy:
            top = ", ".join(f"{self._rel(p)} ({n})" for p, n in heavy[:6])
            f0 = first("color", lambda f, p=heavy[0][0]: f.file == p and not f.themed)
            findings.append(Finding(rule="D13", tier="D", severity="minor" if len(heavy) < 10 else "major", evidence="inferred",
                                    file=heavy[0][0], line=f0.line if f0 else 0,
                                    message=f"hard-coded colors outside the theme in {len(heavy)} files — top: {top}",
                                    fix="reference theme roles (dark mode and rebranding depend on it); keep literals in one token file"))
        # radii
        radii = Counter(f.value for f in by_kind["radius"] if isinstance(f.value, (int, float)) and 0 < f.value < 100)
        if len(radii) > 4:
            f0 = first("radius")
            findings.append(Finding(rule="D15", tier="D", severity="major", evidence="derived", file=f0.file, line=f0.line,
                                    message=f"{len(radii)} distinct radii: {', '.join(str(r) for r in sorted(radii))}",
                                    fix="3–4 radii; nested corners follow inner = outer − padding"))
        # spacing grid
        sp = [f for f in by_kind["spacing"] if isinstance(f.value, (int, float)) and f.value > 2]
        off = [f for f in sp if f.value % self.grid]
        if sp and len(off) / len(sp) > 0.10:
            vals = Counter(f.value for f in off)
            findings.append(Finding(rule="D17", tier="D", severity="major" if len(off) / len(sp) > 0.25 else "minor",
                                    evidence="derived", file=off[0].file, line=off[0].line,
                                    message=f"{len(off)}/{len(sp)} spacing values off the {self.grid}pt grid ({', '.join(str(v) for v, _ in vals.most_common(8))})",
                                    fix=f"snap to the spacing scale (multiples of {self.grid})"))
        # icon families
        fams = Counter(str(f.value).split(":")[0] for f in by_kind["icon"])
        material_styles = {str(f.value).split(":")[1] for f in by_kind["icon"] if str(f.value).startswith("material:")}
        real_fams = [k for k in fams if k not in ("custom-svg", "custom-drawable")]
        if len(real_fams) > 1:
            f0 = by_kind["icon"][0]
            findings.append(Finding(rule="D06", tier="D", severity="major", evidence="observed", file=f0.file, line=f0.line,
                                    message=f"{len(real_fams)} icon families mixed: {', '.join(sorted(real_fams))}",
                                    fix="one family, one weight; fill only for selection"))
        if len(material_styles - {"filled"}) >= 2 or ("filled" in material_styles and len(material_styles) >= 3):
            findings.append(Finding(rule="D06", tier="D", severity="minor", evidence="observed", file="", line=0,
                                    message=f"Material icon styles mixed: {', '.join(sorted(material_styles))}",
                                    fix="pick one style (outlined or rounded); filled only for the selected state"))
        # motion
        animated = sum(fs.flags["animation"] for fs in files)
        reduced = sum(fs.flags["reduce_motion"] for fs in files)
        if animated and not reduced:
            f0 = first("animation")
            findings.append(Finding(rule="F08", tier="F", severity="block", evidence="derived",
                                    file=f0.file if f0 else "", line=f0.line if f0 else 0,
                                    message=f"{animated} animation sites and no reduce-motion handling anywhere",
                                    fix="branch on the platform's reduce-motion setting (see knowledge/motion.md)"))
        long_d = [f for f in by_kind["duration"] if isinstance(f.value, int) and f.value > 600]
        if long_d:
            findings.append(Finding(rule="D19", tier="D", severity="minor", evidence="inferred", file=long_d[0].file,
                                    line=long_d[0].line,
                                    message=f"{len(long_d)} durations above 600ms ({', '.join(sorted({str(f.value) for f in long_d})[:6])}ms)",
                                    fix="UI transitions 150–400ms; long only for ambient or narrative motion"))
        entr = sum(fs.flags["entrance"] for fs in files)
        if entr >= 8:
            findings.append(Finding(rule="D18", tier="D", severity="minor", evidence="derived", file="", line=0,
                                    message=f"{entr} entrance animations across the project",
                                    fix="entrances only for content that is new to the user"))
        texts = {fs.path: fs for fs in files}
        rn = [fs for fs in files if fs.lang == "tsx" and fs.flags.get("react_native")]
        if rn and not any(fs.flags.get("safe_area") for fs in files):
            findings.append(Finding(rule="F09", tier="F", severity="major", evidence="inferred", file=rn[0].path, line=0,
                                    message="React Native screens and no SafeAreaView/useSafeAreaInsets anywhere",
                                    fix="wrap screens with react-native-safe-area-context and respect insets"))
        fl = [fs for fs in files if fs.lang == "flutter"]
        if fl and "ios" in self.platforms and not any(fs.flags.get("adaptive") for fs in fl):
            findings.append(Finding(rule="D24", tier="D", severity="info", evidence="inferred", file=fl[0].path, line=0,
                                    message="no platform adaptation found (Cupertino, .adaptive, TargetPlatform) in a Flutter app targeting iOS",
                                    fix="adapt navigation, switches, dialogs, scroll physics and feedback per platform (knowledge/stacks/flutter.md)"))
        del texts
        # density-style counters (aggregate info signals into one finding per rule/file)
        findings = self._collapse(findings)
        # platform-aware filters
        if "ios" not in self.platforms:
            findings = [f for f in findings if not (f.rule in ("D09", "D08") and "iOS" in f.fix and f.evidence == "inferred")]
        langs = Counter(fs.lang for fs in files)
        summary = {
            "colors": [color.describe(h) for h in uniq[:40]],
            "neutral_count": len(neutrals),
            "neutrals_per_theme": {"light": len(light_n), "dark": len(dark_n)},
            "data_or_status_colors": data_hues,
            "hue_families": dict(hues),
            "font_sizes": dict(sorted(sizes.items())),
            "text_styles": dict(Counter(f.value for f in by_kind["text_style"])),
            "spacing": dict(sorted(Counter(f.value for f in sp).items())),
            "spacing_on_grid_ratio": round(1 - len(off) / len(sp), 3) if sp else None,
            "radii": dict(sorted(radii.items())),
            "durations_ms": dict(sorted(Counter(f.value for f in by_kind["duration"]).items())),
            "curves": dict(Counter(f.value for f in by_kind["curve"])),
            "springs": [list(f.value) for f in by_kind["spring"]],
            "icon_families": dict(fams),
            "animation_sites": animated,
            "reduce_motion_sites": reduced,
            "haptic_sites": sum(fs.flags["haptics"] for fs in files),
            "gradients": sum(fs.flags["gradient"] for fs in files),
            "shadows": sum(fs.flags["D16"] for fs in files),
            "blur": sum(fs.flags["D05"] for fs in files),
        }
        findings.sort(key=lambda f: (f.order(), f.file, f.line))
        return {
            "tool": "scan",
            "ok": not any(f.tier == "F" and f.severity == "block" for f in findings),
            "coverage": {"files_scanned": len(files), "loc": loc, "by_language": dict(langs),
                         "fixture_files": [self._rel(p) for p in fixtures],
                         "skipped": dict(skipped), "unknown": unknown},
            "summary": summary,
            "findings": [f.as_dict() for f in findings],
            "facts": [{"kind": f.kind, "value": f.value, "file": f.file, "line": f.line, "themed": f.themed,
                       "data": f.kind == "color" and is_data(f)}
                      for f in facts if f.kind != "animation"],
            "limitations": [
                "lexical scan: no AST; values built at runtime or behind helpers are not seen",
                "`inferred` findings are heuristics about intent and need a look at the render",
                "a file not listed in coverage was not scanned and is unknown, not clean",
            ],
        }

    def _rel(self, path: str) -> str:
        root = getattr(self, "root", None)
        return os.path.relpath(path, root) if root and path.startswith(root) else path

    def _collapse(self, findings):
        """Info-level counters (D03, D10, D11, D16, D25…) become one finding per file with a count."""
        keep, buckets = [], defaultdict(list)
        emoji = defaultdict(list)
        for f in findings:
            if f.rule == "D06" and f.message.startswith("emoji in UI text"):
                emoji[f.file].append(f)
                continue
            if f.severity == "info" and f.rule in ("D03", "D10", "D11", "D16", "D25", "D20", "D21", "D27", "D19", "D28"):
                buckets[(f.rule, f.file)].append(f)
            else:
                keep.append(f)
        thresholds = {"D03": 5, "D10": 4, "D11": 5, "D16": 4, "D25": 8, "D20": 1, "D21": 1, "D27": 1, "D19": 2, "D28": 3}
        for (rule, path), group in buckets.items():
            if len(group) >= thresholds.get(rule, 1):
                g0 = group[0]
                sev = "minor" if rule in ("D03", "D10", "D16", "D25") and len(group) >= thresholds[rule] else "info"
                keep.append(Finding(rule=rule, tier=g0.tier, severity=sev, evidence="derived" if len(group) > 1 else g0.evidence,
                                    file=path, line=g0.line,
                                    message=f"{g0.message} ×{len(group)}" if len(group) > 1 else g0.message,
                                    fix=g0.fix, snippet=g0.snippet))
        for path, group in emoji.items():
            g0 = group[0]
            keep.append(Finding(rule="D06", tier="D", severity="minor", evidence="observed", file=path, line=g0.line,
                                message=g0.message if len(group) == 1 else
                                f"emoji in UI text ×{len(group)} (e.g. {g0.snippet[:40]!r})",
                                fix=g0.fix, snippet=g0.snippet))
        return keep


def scan(paths, platforms=("ios", "android"), grid=4, theme_paths=None, data_hexes=()) -> dict:
    return Scanner(platforms, grid, theme_paths, data_hexes).scan_paths(paths if isinstance(paths, (list, tuple)) else [paths])
