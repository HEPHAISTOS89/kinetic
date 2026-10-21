"""kinetic — command line for the Kinetic design engine.

Exit codes: 0 ok · 1 F findings (blocked) · 2 usage/input error.
Every command accepts --json for the full machine-readable result."""
from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__
from . import clarity, color, deal, dna, export, panel, project, report, score, sheet, states, svg, validate
from .kdl import KDLError, parse_file
from .scan import scan


def _out(result: dict, as_json: bool, text: str | None = None, limit: int = 60):
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print(text if text is not None else report.render(result, limit))


def _filter(result, tiers, min_sev):
    order = report.SEVERITY_ORDER
    fs = result.get("findings", [])
    if tiers:
        fs = [f for f in fs if f["tier"] in tiers]
    if min_sev:
        fs = [f for f in fs if order.get(f["severity"], 9) <= order[min_sev]]
    result["findings"] = fs
    return result


def cmd_validate(a):
    r = validate.validate_file(a.file)
    _out(_filter(r, a.tiers, a.min_severity), a.json, limit=a.limit)
    return 0 if r["ok"] else 1


def cmd_palette(a):
    roles = color.derive_roles(a.seed, a.strategy, a.neutral_chroma, a.temperature, a.neutral_hue)
    checks = color.check_roles(roles)
    r = {"tool": "palette", "seed": a.seed, "seed_oklch": color.describe(a.seed)["oklch"], "strategy": a.strategy,
         "roles": roles, "ramp": color.ramp(a.seed), "contrast": checks, "ok": all(c["ok"] for c in checks)}
    if a.json:
        _out(r, True)
    elif a.kdl:
        lines = ["  color:", f"    seed: \"{a.seed}\"", f"    strategy: {a.strategy}", "    roles:"]
        for theme, rr in roles.items():
            lines.append(f"      {theme}:")
            lines += [f"        {k}: \"{v}\"" for k, v in rr.items()]
        print("\n".join(lines))
    else:
        out = [f"kinetic palette {a.seed}  oklch{tuple(r['seed_oklch'])}  strategy={a.strategy}"]
        for theme, rr in roles.items():
            out.append(f"  {theme}:")
            out += [f"    {k:<12} {v}" for k, v in rr.items()]
        out.append("  contrast:")
        out += [f"    {c['theme']:<5} {c['pair']:<18} {c['wcag']:>5}:1  Lc {c['apca_lc']:>6}  {'ok' if c['ok'] else 'FAIL'}"
                for c in checks]
        out.append("  ramp: " + " ".join(f"{k}:{v}" for k, v in r["ramp"].items()))
        print("\n".join(out))
    return 0 if r["ok"] else 1


def cmd_contrast(a):
    rep = color.contrast_report(a.fg, a.bg)
    rep["tool"] = "contrast"
    text = (f"{a.fg} on {a.bg}: WCAG {rep['wcag']}:1 (AA body {'✓' if rep['aa_body'] else '✗'}, "
            f"AA large {'✓' if rep['aa_large'] else '✗'}, AAA {'✓' if rep['aaa_body'] else '✗'}) · "
            f"APCA Lc {rep['apca_lc']} (body ≥75 {'✓' if rep['apca_body'] else '✗'}, fluent ≥60 {'✓' if rep['apca_fluent'] else '✗'})")
    _out(rep, a.json, text)
    return 0 if rep["aa_body"] else 1


def _cfg(a, paths):
    cfg = project.load_config(paths[0] if paths else ".")
    plats = a.platforms.split(",") if getattr(a, "platforms", None) else cfg["platforms"]
    grid = getattr(a, "grid", None) or cfg["grid"]
    return cfg, plats, grid


def cmd_scan(a):
    cfg, plats, grid = _cfg(a, a.paths)
    r = scan(a.paths, plats, grid, cfg.get("theme_paths"), project.data_hexes(a.paths[0]),
             project.exceptions(a.paths[0]), project.vocabulary_roles(a.paths[0]))
    if not a.facts:
        r.pop("facts", None)
    _out(_filter(r, a.tiers, a.min_severity), a.json, limit=a.limit)
    return 0 if r["ok"] else 1


def cmd_dna(a):
    cfg, plats, grid = _cfg(a, a.paths)
    d = dna.dna(scan(a.paths, plats, grid, cfg.get("theme_paths"), project.data_hexes(a.paths[0]),
             project.exceptions(a.paths[0])), grid)
    if a.kdl:
        print(dna.to_kdl(d))
    elif a.json:
        _out(d, True)
    else:
        out = ["kinetic dna — coherence " + ", ".join(f"{k}={v}" for k, v in d["coherence"].items() if v is not None)
               + f" · mean {d['coherence_mean']}"]
        p = d["dna"]
        out.append(f"  neutrals ({len(p['palette']['neutrals'])}): {' '.join(p['palette']['neutrals'][:12])}")
        out.append(f"  accents  ({len(p['palette']['accents'])}): {' '.join(p['palette']['accents'][:12])}")
        out.append(f"  type sizes: {p['type_sizes']}  text styles: {p['text_styles']}")
        out.append(f"  spacing: {p['spacing']}")
        out.append(f"  radii: {p['radii']}")
        out.append(f"  motion: {p['motion']}")
        out.append(f"  icons: {p['icons']}  effects: {p['effects']}")
        scale = d["proposal"]["type"]["scale"]
        out.append("  proposed ramp: " + ", ".join(f"{k}={v['size']}" for k, v in scale.items() if k != "_outliers")
                   + (f"  (outliers: {scale['_outliers']})" if "_outliers" in scale else ""))
        out.append("  (use --kdl to get an editable KDL audit + system draft)")
        print("\n".join(out))
    return 0


def cmd_states(a):
    if a.view == "matrix":
        r = states.matrix(parse_file(a.target[0]))
        if a.json:
            _out(r, True)
        else:
            out = [f"kinetic states — {r['coverage']['states_covered']}/{r['coverage']['states_required']} required states covered"]
            for row in r["screens"]:
                cells = "  ".join(f"{k}:{'✓' if v == 'designed' else '–' if v == 'n/a' else '✗'}" for k, v in row["states"].items())
                out.append(f"  {row['screen']:<16} {cells}")
                for c in row["components"]:
                    miss = [k for k, v in c["variants"].items() if not v and k in ("pressed", "disabled")]
                    out.append(f"      {c['id']} ({c['kind']}) {'missing ' + ', '.join(miss) if miss else 'variants ok'}")
            print("\n".join(out))
        return 0 if r["coverage"]["states_required"] == r["coverage"]["states_covered"] else 1
    if a.view == "code":
        r = states.code(a.target)
        _out(r, a.json)
        return 0
    item = states.template(a.target[0] if a.target else "new-screen", not a.no_network)
    print(("screens:\n" + item) if a.block else item)
    return 0


def cmd_score(a):
    if not (a.kdl or a.code):
        print("score needs --kdl and/or --code", file=sys.stderr)
        return 2
    cfg, plats, grid = _cfg(a, a.code or [os.path.dirname(a.kdl) or "."])
    r = score.run(a.kdl, a.code, a.judged, plats, grid, a.renders)
    _out(r, a.json, score.render(r))
    return 1 if r["verdict"] == "blocked" else 0


def cmd_export(a):
    doc = parse_file(a.file)
    stack = a.stack or ((doc.get("product") or {}).get("stack"))
    if not stack:
        print("no --stack given and product.stack is empty", file=sys.stderr)
        return 2
    kw = {"package": a.package} if stack == "compose" and a.package else {}
    text = export.export(doc, stack, os.path.relpath(a.file), **kw)
    if a.out:
        # a path without an extension is a folder (`--out design` → design/tokens.ts), whether or not it exists yet
        is_dir = os.path.isdir(a.out) or a.out.endswith(("/", os.sep)) or not os.path.splitext(a.out)[1]
        out = os.path.join(a.out, export.FILENAMES[stack]) if is_dir else a.out
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        if os.path.exists(out) and not a.force:
            with open(out, encoding="utf-8") as fh:
                if "GENERATED by `kinetic export`" not in fh.read(400):
                    print(f"refusing to overwrite hand-written {out} (use --force)", file=sys.stderr)
                    return 2
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {out} ({stack})")
    else:
        sys.stdout.write(text)
    return 0


def cmd_svg(a):
    if a.action == "lint":
        r = svg.lint(a.paths)
        _out(r, a.json, limit=a.limit)
        return 0 if r["ok"] else 1
    for p in a.paths:
        cleaned = svg.normalize(p)
        if a.write:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(cleaned + "\n")
            print(f"normalized {p}")
        else:
            print(cleaned)
    return 0


def cmd_init(a):
    r = project.init(a.path, a.mode, a.stack, a.force, a.name)
    _out(r, a.json, "\n".join([f"kinetic init — {r['root']} ({r['stack']}, {', '.join(r['platforms'])})"] +
                               [f"  created {p}" for p in r["created"]] + [f"  kept    {p}" for p in r["kept_existing"]] +
                               [f"  hint: {h}" for h in r.get("hints", [])] +
                               ["  next: fill .kinetic/design.kdl, then `kinetic validate .kinetic/design.kdl`"]))
    return 0


def cmd_spring(a):
    p = export.spring_physics(a.response, a.damping)
    ms, pts = export.spring_samples(a.response, a.damping, 20)
    r = {"tool": "spring", "response": a.response, "damping": a.damping, "physics": p, "settle_ms": ms,
         "overshoot_pct": round(max(0, max(pts) - 1) * 100, 1),
         "swiftui": f".spring(response: {a.response}, dampingFraction: {a.damping})",
         "flutter": f"SpringDescription.withDampingRatio(mass: 1, stiffness: {p['stiffness']}, ratio: {a.damping})",
         "compose": f"spring(dampingRatio = {a.damping}f, stiffness = {p['stiffness']}f)",
         "reanimated": f"withSpring(v, {{ mass: 1, stiffness: {p['stiffness']}, damping: {p['damping']} }})",
         "css": f"linear({', '.join(map(str, pts))}) {ms}ms"}
    _out(r, a.json, "\n".join(f"{k:<11} {v}" for k, v in r.items() if k != "tool"))
    return 0


def _deal_path(a):
    if a.out:
        return a.out
    root = project.find_root(".")
    return os.path.join(root or ".", ".kinetic", "deal.json")


def cmd_deal(a):
    path = _deal_path(a)
    if a.redraw:
        opt, _, slot = a.redraw.partition(".")
        state = deal.redraw(deal.load(path), int(opt), slot, a.reason or "")
    elif a.show:
        state = deal.load(path)
    else:
        if os.path.exists(path) and not a.fresh:
            raise ValueError(f"{path} exists: a project is dealt once (use --show, --redraw N.slot --reason, or --fresh)")
        brief = a.brief or ""
        if a.brief_file:
            with open(a.brief_file, encoding="utf-8") as fh:
                brief += "\n" + fh.read()
        state = deal.deal(brief, a.seed, a.options, a.exclude.split(",") if a.exclude else ())
    if not a.show:
        deal.save(state, path)
    _out(dict(state, path=path), a.json, deal.sheet(state) + f"\n\nsaved: {path}")
    return 0


def cmd_clarity(a):
    r = clarity.clarity(a.images)
    if a.json:
        _out(r, True)
        return 0
    out = [f"kinetic clarity — mean {r['mean']}/100 over {len(r['renders'])} renders (clean ≥ 85, cluttered < 70)"]
    for m in r["renders"]:
        out.append(f"  {m['clarity']:>3}  {os.path.basename(m['file']):<40} words~{m['words']:<4} lines {m['lines']:<3} "
                   f"sizes {m['text_sizes']}  quiet {int(m['quiet_share'] * 100)}%  gap {m['largest_gap_pt']}pt")
    for wst in r["worst"]:
        for n in wst["notes"]:
            out.append(f"  → {wst['file']}: {n}")
    out.append("limitation: " + r["limitations"][0])
    print("\n".join(out))
    return 0


def cmd_panel(a):
    r = panel.merge_files(a.critiques)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=1, ensure_ascii=False)
    p = r["panel"]
    lines = [f"kinetic panel — {p['size']} critics merged by median → {a.out}"]
    for d, v in r["dimensions"].items():
        lines.append(f"  {d:<16} {v['score']}  {v['scores']}{'  SPLIT' if d in p['split'] else ''}")
    lines += [f"  consensus: {c}" for c in p["consensus_fixes"][:6]]
    print("\n".join(lines))
    return 0


def cmd_sheet(a):
    r = sheet.contact_sheet(a.images, a.out, a.cols, a.width)
    _out(r, a.json, f"contact sheet {r['out']}  ({r['count']} renders, {r['cols']} columns)\n" +
         "\n".join(f"  {i + 1:>2}. {os.path.basename(f)}" for i, f in enumerate(r["order"])))
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="kinetic", description="Kinetic design engine")
    p.add_argument("--version", action="version", version=f"kinetic {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, findings=True):
        sp.add_argument("--json", action="store_true", help="full machine-readable result")
        if findings:
            sp.add_argument("--tiers", type=lambda s: set(s.split(",")), help="e.g. F,D")
            sp.add_argument("--min-severity", choices=["block", "major", "minor", "info"])
            sp.add_argument("--limit", type=int, default=60)

    s = sub.add_parser("validate", help="check a KDL decision record")
    s.add_argument("file")
    common(s)
    s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("palette", help="derive light/dark color roles from a seed")
    s.add_argument("seed")
    s.add_argument("--strategy", default="neutral+accent", choices=["neutral+accent", "monochrome", "brand-led"])
    s.add_argument("--temperature", default="auto", choices=["auto", "warm", "cool"])
    s.add_argument("--neutral-hue", type=float, help="hue of the tinted neutrals (OKLCH degrees), e.g. 80 for warm concrete")
    s.add_argument("--neutral-chroma", type=float, help="chroma of the tinted neutrals (default 0.008)")
    s.add_argument("--kdl", action="store_true", help="print as a KDL `color` block")
    common(s, False)
    s.set_defaults(fn=cmd_palette)

    s = sub.add_parser("contrast", help="WCAG 2 + APCA contrast of two colors")
    s.add_argument("fg")
    s.add_argument("bg")
    common(s, False)
    s.set_defaults(fn=cmd_contrast)

    for name, fn, helptext in (("scan", cmd_scan, "inspect UI source for design facts and slop"),
                               ("dna", cmd_dna, "derive the de-facto design system from code")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("paths", nargs="+")
        s.add_argument("--platforms", help="ios,android (default from .kinetic/config.json)")
        s.add_argument("--grid", type=int)
        if name == "scan":
            s.add_argument("--facts", action="store_true", help="include every extracted fact")
            common(s)
        else:
            s.add_argument("--kdl", action="store_true", help="print an editable KDL audit + system draft")
            common(s, False)
        s.set_defaults(fn=fn)

    s = sub.add_parser("states", help="state matrix from KDL, inferred handling from code, or a screen template")
    s.add_argument("view", choices=["matrix", "code", "template"])
    s.add_argument("target", nargs="*")
    s.add_argument("--no-network", action="store_true")
    s.add_argument("--block", action="store_true", help="template: include the `screens:` key")
    common(s, False)
    s.set_defaults(fn=cmd_states)

    s = sub.add_parser("score", help="taste report: measured + independently judged")
    s.add_argument("--kdl")
    s.add_argument("--code", nargs="+")
    s.add_argument("--judged", help="critic JSON (docs/PROTOCOL.md) or a panel from `kinetic panel`")
    s.add_argument("--renders", nargs="+", help="render PNGs/folders: adds the measured `clarity` score")
    s.add_argument("--platforms")
    s.add_argument("--grid", type=int)
    common(s, False)
    s.set_defaults(fn=cmd_score)

    s = sub.add_parser("export", help="compile KDL system tokens for a stack")
    s.add_argument("file")
    s.add_argument("--stack", choices=list(export.STACKS) + ["web"])
    s.add_argument("--out")
    s.add_argument("--package", help="Kotlin package for compose")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_export)

    s = sub.add_parser("svg", help="lint or normalize icon SVGs")
    s.add_argument("action", choices=["lint", "fix"])
    s.add_argument("paths", nargs="+")
    s.add_argument("--write", action="store_true", help="fix: overwrite files")
    common(s)
    s.set_defaults(fn=cmd_svg)

    s = sub.add_parser("init", help="create .kinetic/ (config + design.kdl skeleton)")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("--mode", default="create", choices=sorted(validate.MODES))
    s.add_argument("--stack", choices=["flutter", "swiftui", "compose", "react-native", "web", "mixed"])
    s.add_argument("--name", help="product name (default: folder name)")
    s.add_argument("--force", action="store_true")
    common(s, False)
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("deal", help="deal directions (engine, type, palette, motion) from the library")
    s.add_argument("--brief", help="brief text (weights the deal; never decides it)")
    s.add_argument("--brief-file", help="read the brief from a file")
    s.add_argument("--seed", type=int, help="reproduce a deal (default: random, recorded)")
    s.add_argument("--options", type=int, default=3)
    s.add_argument("--exclude", help="library ids to leave out (comma-separated)")
    s.add_argument("--redraw", help="N.slot, e.g. 2.type — replace one dealt slot (needs --reason)")
    s.add_argument("--reason", help="why the dealt slot cannot work (a product fact or brand constraint)")
    s.add_argument("--show", action="store_true", help="print the recorded deal")
    s.add_argument("--fresh", action="store_true", help="deal again even if .kinetic/deal.json exists")
    s.add_argument("--out", help="deal file (default .kinetic/deal.json)")
    common(s, False)
    s.set_defaults(fn=cmd_deal)

    s = sub.add_parser("clarity", help="measure clutter on renders: words, lines, text sizes, quiet space")
    s.add_argument("images", nargs="+", help="PNG files or folders")
    common(s, False)
    s.set_defaults(fn=cmd_clarity)

    s = sub.add_parser("panel", help="merge independent critiques (median per dimension, disagreement, consensus)")
    s.add_argument("critiques", nargs="+")
    s.add_argument("--out", default=".kinetic/critique.json")
    common(s, False)
    s.set_defaults(fn=cmd_panel)

    s = sub.add_parser("sheet", help="contact sheet of renders (one PNG) for judging the system at once")
    s.add_argument("images", nargs="+", help="PNG files or folders")
    s.add_argument("--out", default="contact-sheet.png")
    s.add_argument("--cols", type=int, default=0, help="columns (default: by count)")
    s.add_argument("--width", type=int, default=240, help="cell width in px")
    common(s, False)
    s.set_defaults(fn=cmd_sheet)

    s = sub.add_parser("spring", help="convert a KDL spring to every stack")
    s.add_argument("response", type=float)
    s.add_argument("damping", type=float)
    common(s, False)
    s.set_defaults(fn=cmd_spring)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except (KDLError, ValueError, OSError) as e:
        print(f"kinetic {args.cmd}: {e}", file=sys.stderr)
        return 2
