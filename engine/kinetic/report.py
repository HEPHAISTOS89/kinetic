"""Shared finding record and human rendering (see docs/PROTOCOL.md)."""
from __future__ import annotations

from dataclasses import asdict, dataclass

TIER_ORDER = {"F": 0, "D": 1, "C": 2, "I": 3}
SEVERITY_ORDER = {"block": 0, "major": 1, "minor": 2, "info": 3}
EVIDENCE = {"observed", "derived", "inferred"}


@dataclass
class Finding:
    rule: str
    tier: str
    severity: str
    message: str
    fix: str
    evidence: str = "observed"
    file: str = ""
    line: int = 0
    path: str = ""          # KDL path, when the finding is about a decision record
    snippet: str = ""

    def order(self):
        return (TIER_ORDER.get(self.tier, 9), SEVERITY_ORDER.get(self.severity, 9))

    def as_dict(self):
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in ("", None) or k in ("rule", "message")}


def render(result: dict, limit: int = 60) -> str:
    """Compact human/model-readable rendering of any tool result."""
    lines = []
    tool = result.get("tool", "kinetic")
    head = f"kinetic {tool}"
    if "ok" in result:
        majors = sum(1 for f in result.get("findings", []) if f.get("tier") == "D" and f.get("severity") == "major")
        head += " — " + ("BLOCKED (F findings)" if not result["ok"]
                         else f"NEEDS WORK ({majors} major D findings)" if majors else "OK")
    lines.append(head)
    cov = result.get("coverage")
    if cov:
        parts = []
        for k, v in cov.items():
            if isinstance(v, (list, dict)):
                v = len(v) if not isinstance(v, dict) else ", ".join(f"{a}:{b}" for a, b in v.items())
            parts.append(f"{k}={v}")
        lines.append("coverage: " + "; ".join(parts))
    findings = result.get("findings", [])
    counts = {}
    for f in findings:
        counts[f["tier"]] = counts.get(f["tier"], 0) + 1
    if findings:
        lines.append("findings: " + ", ".join(f"{t}={counts[t]}" for t in sorted(counts, key=lambda t: TIER_ORDER.get(t, 9))))
    for f in findings[:limit]:
        loc = f.get("file", "")
        if f.get("line"):
            loc += f":{f['line']}"
        if f.get("path"):
            loc += f" [{f['path']}]"
        lines.append(f"  {f['tier']}/{f['severity']:<5} {f['rule']:<4} {loc}")
        lines.append(f"      {f['message']}  ({f.get('evidence', '')})")
        if f.get("fix"):
            lines.append(f"      → {f['fix']}")
    if len(findings) > limit:
        lines.append(f"  … {len(findings) - limit} more (use --json for all)")
    for w in result.get("waived", []):
        lines.append(f"  waived {w['rule']:<4} {w.get('file', '')}  — {w.get('reason', '')}")
    for lim in result.get("limitations", []):
        lines.append(f"limitation: {lim}")
    return "\n".join(lines)


def read_text(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()
