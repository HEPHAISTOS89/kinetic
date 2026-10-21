"""State intelligence: the matrix of every screen × state and component ×
variant, from KDL (decisions) or from code (inferred handling).

Shapes: `matrix` (derived from KDL), `code` (inspect; evidence `inferred`),
`template` (generate a KDL skeleton for a new screen)."""
from __future__ import annotations

import os
import re

from .report import Finding, read_text
from .scan import EXCLUDE_DIRS, LANG_BY_EXT, SKIP_FILE
from .validate import INTERACTIVE, SCREEN_STATES

FETCH = re.compile(r"FutureBuilder|StreamBuilder|AsyncValue|ref\.watch\(|BlocBuilder|\bhttp\.|\bdio\.|\.task\s*\{|URLSession|"
                   r"\basync let\b|@Query\b|LaunchedEffect|collectAsState\w*\(|\buseQuery\(|\buseSWR\(|\bfetch\(|\baxios\b|"
                   r"\bawait\b|\.refreshable|Supabase|Firestore|firebase", re.I)
HANDLES = {
    "loading": re.compile(r"CircularProgressIndicator|LinearProgressIndicator|isLoading|\bloading\b|ProgressView|"
                          r"\.redacted\(|ActivityIndicator|Skeleton|Shimmer|ConnectionState\.waiting|isPending|isFetching", re.I),
    "error": re.compile(r"hasError|\berror\b|\bcatch\b|onError|failure|isError|ErrorView|retry|tryAgain|\.failure|\.failed\b|Result\.failure", re.I),
    "empty": re.compile(r"isEmpty|\bempty\b|ContentUnavailableView|EmptyView|no results|ListEmptyComponent|\.count\s*==\s*0|"
                        r"length\s*===?\s*0|NoData|nothing (here|yet)|aucun", re.I),
    "offline": re.compile(r"connectivity|offline|NWPathMonitor|NetInfo|isConnected|reachab", re.I),
}
SCREEN_FILE = re.compile(r"(screen|view|page|route|tab|sheet)s?\b", re.I)


def matrix(doc) -> dict:
    rows, findings = [], []
    for i, sc in enumerate(doc.get("screens") or []):
        if not isinstance(sc, dict):
            continue
        sid = sc.get("id", f"#{i}")
        states = sc.get("states") if isinstance(sc.get("states"), dict) else {}
        needed = list(SCREEN_STATES) + (["offline"] if sc.get("network") else [])
        extra = [k for k in states if k not in needed]
        row = {"screen": sid, "states": {}}
        for st in needed + extra:
            v = states.get(st)
            row["states"][st] = "missing" if v in (None, "") else ("n/a" if str(v).lower().startswith("n/a") else "designed")
        comps = []
        for cp in sc.get("components") or []:
            if isinstance(cp, dict) and cp.get("kind") in INTERACTIVE:
                var = cp.get("variants") or []
                comps.append({"id": cp.get("id"), "kind": cp.get("kind"),
                              "variants": {v: v in var for v in ("default", "pressed", "disabled", "loading", "selected", "focused")}})
        row["components"] = comps
        rows.append(row)
    total = sum(len(r["states"]) for r in rows)
    covered = sum(1 for r in rows for v in r["states"].values() if v != "missing")
    return {"tool": "states", "view": "matrix", "screens": rows,
            "coverage": {"screens": len(rows), "states_required": total, "states_covered": covered,
                         "ratio": round(covered / total, 3) if total else None},
            "findings": [f.as_dict() for f in findings]}


def code(paths) -> dict:
    rows, findings, scanned = [], [], 0
    files = []
    for root in paths:
        if os.path.isfile(root):
            files.append(root)
            continue
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in EXCLUDE_DIRS and not d.startswith(".")]
            files += [os.path.join(dp, f) for f in fns]
    texts = {}
    for p in files:
        if os.path.splitext(p)[1].lower() not in LANG_BY_EXT or SKIP_FILE.search(p):
            continue
        try:
            texts[p] = read_text(p)
        except OSError:
            continue
    # where each type is declared, so a screen's handling inside its components is seen
    declared = {}
    for p, text in texts.items():
        for name in re.findall(r"\b(?:struct|class|enum|fun|function|const)\s+([A-Z]\w+)", text):
            declared.setdefault(name, p)
    for p, text in texts.items():
        scanned += 1
        if not SCREEN_FILE.search(os.path.basename(p)) or not FETCH.search(text):
            continue
        used = {declared[n] for n in set(re.findall(r"\b([A-Z]\w+)", text)) if n in declared and declared[n] != p}
        context = text + "\n".join(texts[u] for u in used)
        handled = {k: bool(rx.search(context)) for k, rx in HANDLES.items()}
        rows.append({"file": p, "fetches": True, "handles": handled, "followed": sorted(used)})
        for st in ("error", "empty", "loading"):
            if not handled[st]:
                findings.append(Finding(rule="F06", tier="F" if st != "loading" else "D",
                                        severity="major" if st != "loading" else "minor", evidence="inferred",
                                        file=p, line=0,
                                        message=f"screen loads data but no `{st}` handling was found",
                                        fix=f"design and implement the {st} state (knowledge/states.md)"))
    findings.sort(key=lambda f: (f.order(), f.file))
    return {"tool": "states", "view": "code", "screens": rows,
            "coverage": {"files_scanned": scanned, "data_screens": len(rows)},
            "findings": [f.as_dict() for f in findings],
            "limitations": ["keyword heuristics; component files declared in the scanned set are followed one level deep",
                            "only files whose name looks like a screen/view/page are evaluated"]}


def template(screen_id: str, network: bool = True) -> str:
    lines = [
        f"  - id: {screen_id}",
        "    job: TODO one sentence — what this screen does for the user",
        "    serves: [TODO requirement ids]",
        "    thumb: [TODO actions and navigation reachable in the bottom third]",
        f"    network: {'true' if network else 'false'}",
        "    primary: TODO the one thing that must be seen first",
        "    secondary: TODO",
        "    reading_order: [TODO]",
        "    components:",
        "      - id: primary-action",
        "        kind: button",
        "        fg: $color.on-accent",
        "        bg: $color.accent",
        "        target: 48",
        "        variants: [default, pressed, disabled, loading]",
        "    states:",
        "      content: TODO",
        "      loading: TODO what is shown while waiting (keep previous content? skeleton only if > 300ms)",
        "      empty: TODO first-use and no-results versions; explain and offer the next step",
        "      error: TODO cause in plain words + recovery action",
    ]
    if network:
        lines.append("      offline: TODO what still works; when it retries")
    lines += [
        "      overflow: TODO longest real strings, largest text size, smallest screen",
        "    motion:",
        "      - id: TODO",
        "        trigger: TODO",
        "        change: TODO",
        "        spring: $spring.TODO",
        "        reduce: crossfade",
        "        interruptible: true",
    ]
    return "\n".join(lines) + "\n"
