"""PostToolUse hook: design lint for the file that was just edited.

Contract: reads the hook JSON on stdin; acts only when the edited file is a
UI source file inside a project that contains `.kinetic/` and whose config
has `hook: true`. Emits `additionalContext` with at most 10 F/D findings for
that file. Never blocks, never writes, exits 0 on every path."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

UI_EXT = {".dart", ".swift", ".kt", ".tsx", ".jsx", ".css", ".scss", ".vue", ".svelte"}


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path")
    if not path or os.path.splitext(path)[1].lower() not in UI_EXT or not os.path.isfile(path):
        return
    from kinetic import project
    from kinetic.report import SEVERITY_ORDER
    from kinetic.scan import scan

    cfg = project.load_config(path)
    if not cfg.get("root") or not cfg.get("hook", True):
        return
    r = scan([path], cfg["platforms"], cfg["grid"], cfg.get("theme_paths"))
    tiers = set(cfg.get("hook_tiers") or ["F", "D"])
    floor = SEVERITY_ORDER.get(cfg.get("hook_min_severity", "major"), 1)
    fs = [f for f in r["findings"]
          if f["tier"] in tiers and SEVERITY_ORDER.get(f["severity"], 9) <= floor
          and (not f.get("file") or os.path.abspath(f["file"]) == os.path.abspath(path))]
    if not fs:
        return
    rel = os.path.relpath(path, cfg["root"])
    lines = [f"Kinetic design lint — {rel}: {len(fs)} finding(s). Fix F now; fix D or justify it in .kinetic/design.kdl."]
    for f in fs[:10]:
        lines.append(f"- {f['tier']}/{f['rule']} line {f.get('line', 0)}: {f['message']} → {f.get('fix', '')} ({f.get('evidence')})")
    if len(fs) > 10:
        lines.append(f"- … {len(fs) - 10} more: run `kinetic scan {rel}`")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(lines)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:  # a design lint must never break the user's edit loop
        pass
    sys.exit(0)
