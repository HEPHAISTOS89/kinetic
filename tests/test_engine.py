"""Kinetic engine tests. Run: python3 -m unittest discover -s tests -v
Set KINETIC_SLOW=1 to also compile Flutter exports (flutter analyze)."""
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


def rd(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from kinetic import clarity, cli, color, deal, dna, export, kdl, panel, score, sheet, states, svg, validate  # noqa: E402
from kinetic.scan import scan  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures")
LUNE = os.path.join(ROOT, "examples", "lune", "design.kdl")


def rules(result):
    return {f["rule"] for f in result["findings"]}


class TestKDL(unittest.TestCase):
    def test_structures(self):
        doc = kdl.parse(
            "a: 1\nb:\n  c: [x, y, {z: 2}]\n  d: 'q: r'\nlist:\n  - id: one\n    v: 1.5\n  - plain\n"
            "multi: {k: 1,\n  j: 2}\nblock: |\n  line one\n  line two\nhex: #3D5AFE # comment\n"
            "na: n/a: data is local\nflag: true\nnothing: null\n")
        self.assertEqual(doc["a"], 1)
        self.assertEqual(doc["b"]["c"], ["x", "y", {"z": 2}])
        self.assertEqual(doc["b"]["d"], "q: r")
        self.assertEqual(doc["list"][0], {"id": "one", "v": 1.5})
        self.assertEqual(doc["list"][1], "plain")
        self.assertEqual(doc["multi"], {"k": 1, "j": 2})
        self.assertEqual(doc["block"], "line one\nline two")
        self.assertEqual(doc["hex"], "#3D5AFE")
        self.assertEqual(doc["na"], "n/a: data is local")
        self.assertIs(doc["flag"], True)
        self.assertIsNone(doc["nothing"])

    def test_prose_with_apostrophes_and_commas(self):
        doc = kdl.parse("r: {id: R1, need: see every member's balance, then settle, priority: must}\n"
                        "q: 'quoted, with comma'\nl: [a, \"b, c\"]\n")
        self.assertEqual(doc["r"]["need"], "see every member's balance, then settle")
        self.assertEqual(doc["r"]["priority"], "must")
        self.assertEqual(doc["q"], "quoted, with comma")
        self.assertEqual(doc["l"], ["a", "b, c"])

    def test_line_numbers(self):
        doc = kdl.parse("x: 1\n\ny:\n  z: 2\n")
        self.assertEqual(doc.lines["y"], 3)
        self.assertEqual(doc["y"].lines["z"], 4)

    def test_errors(self):
        for bad, msg in (("a:\n\tb: 1\n", "tabs"), ("a: 1\na: 2\n", "duplicate"), ("a: [1, 2\n", "unclosed"),
                         ("a: 1\n   b: 2\n", "indentation")):
            with self.assertRaises(kdl.KDLError, msg=bad) as cm:
                kdl.parse(bad)
            self.assertIn(msg, str(cm.exception))

    def test_lune_parses(self):
        doc = kdl.parse_file(LUNE)
        self.assertEqual(len(doc["directions"]), 3)
        self.assertEqual(doc["system"]["color"]["roles"]["dark"]["accent"], "#D9A877")


class TestColor(unittest.TestCase):
    def test_custom_on_roles_are_checked(self):
        bad = {"light": {"bg": "#FFFFFF", "action": "#6CC0BB", "on-action": "#FFFFFF"}}
        pairs = {(c["pair"], c["ok"]) for c in color.check_roles(bad)}
        self.assertIn(("on-action/action", False), pairs)

    def test_reference_values(self):
        self.assertAlmostEqual(color.wcag("#FFFFFF", "#000000"), 21.0, places=2)
        self.assertAlmostEqual(color.apca("#000000", "#FFFFFF"), 106.0, delta=0.1)
        self.assertAlmostEqual(color.apca("#FFFFFF", "#000000"), -107.9, delta=0.1)
        self.assertAlmostEqual(color.apca("#888888", "#FFFFFF"), 63.1, delta=0.1)

    def test_roundtrip_and_gamut(self):
        for h in ("#3D5AFE", "#C9A27E", "#00C7BE", "#111111", "#FFFFFF"):
            self.assertLess(color.delta_e_ok(h, color.oklch_to_hex(color.hex_to_oklch(h))), 0.005)
        self.assertTrue(color.is_hex(color.oklch_to_hex((0.7, 0.4, 145))))  # out of gamut → mapped

    def test_roles_pass_for_many_seeds(self):
        for seed in ("#0A84FF", "#FACC15", "#16A34A", "#E64500", "#C9A27E", "#7C3AED", "#00C7BE", "#111111",
                     "#E11D48", "#8B5CF6", "#0EA5E9", "#A3E635"):
            fails = [c for c in color.check_roles(color.derive_roles(seed)) if not c["ok"]]
            self.assertEqual(fails, [], seed)

    def test_ramp_monotonic(self):
        r = color.ramp("#3D5AFE")
        ls = [color.hex_to_oklch(v)[0] for v in r.values()]
        self.assertEqual(ls, sorted(ls, reverse=True))

    def test_ai_purple(self):
        self.assertTrue(color.is_ai_purple("#7C3AED"))
        self.assertFalse(color.is_ai_purple("#3D5AFE") and color.is_ai_purple("#C9A27E"))


class TestValidate(unittest.TestCase):
    def test_golden_example_is_clean(self):
        r = validate.validate_file(LUNE)
        self.assertTrue(r["ok"])
        self.assertEqual([f for f in r["findings"] if f["tier"] in ("F", "D") and f["severity"] in ("block", "major")], [])

    def test_slop_record(self):
        r = validate.validate_file(os.path.join(FIX, "slop.kdl"))
        self.assertFalse(r["ok"])
        expected = {"F03", "F05", "F06", "F08", "K01", "K04", "K05", "K06", "K09", "D12", "D15", "D17", "D19", "K03", "D22"}
        self.assertTrue(expected <= rules(r), expected - rules(r))

    def test_data_colors(self):
        base = rd(LUNE)
        doc = base.replace('  space:\n    unit: 4', '  space:\n    unit: 4', 1)
        txt = base.replace("    strategy: monochrome-warm\n", "    strategy: monochrome-warm\n    data:\n      T2: {fill: \"#2E7D4F\", on: \"#FFFFFF\"}\n      M1: {fill: \"#FFD400\", on: \"#FFFFFF\"}\n      B3: \"#B5261C\"\n", 1)
        r = validate.validate_text(txt)
        msgs = [(f["rule"], f.get("path", "")) for f in r["findings"]]
        self.assertIn(("F03", "system.color.data.M1"), msgs)       # white on yellow fails
        self.assertIn(("K26", "system.color.data.B3"), msgs)       # too close to danger
        self.assertNotIn(("F03", "system.color.data.T2"), msgs)
        d = kdl.parse(txt)
        for st in export.STACKS:
            self.assertIn("2E7D4F", export.export(d, st).upper(), st)

    def test_todo_and_syntax(self):
        r = validate.validate_text("kdl: 1\nmode: audit\nproduct:\n  name: x\n  users: TODO who\n  moment: m\naudit:\n  keep: [a]\n")
        self.assertIn("K02", rules(r))
        r = validate.validate_text("kdl: 1\nproduct: [unclosed\n")
        self.assertEqual(r["findings"][0]["rule"], "K00")


class TestScan(unittest.TestCase):
    CASES = {
        "flutter_slop": {"F01", "F02", "F05", "F07", "F08", "F10", "D01", "D02", "D06", "D12", "D13", "D15", "D17", "D19", "D22", "D28", "D29", "D30"},
        "swiftui_slop": {"F02", "F05", "F07", "F08", "F10", "D01", "D02", "D05", "D17", "D19", "D22", "D28", "D29"},
        "compose_slop": {"F02", "F05", "F07", "F08", "D01", "D02", "D17", "D19", "D22"},
        "rn_slop": {"F01", "F02", "F07", "F08", "F09", "F10", "D01", "D02", "D06", "D17", "D29"},
    }

    def test_slop_fixtures(self):
        for name, expected in self.CASES.items():
            got = rules(scan(os.path.join(FIX, name)))
            self.assertTrue(expected <= got, f"{name}: missing {expected - got}")

    def test_clean_fixture_has_no_f_or_major_d(self):
        r = scan(os.path.join(FIX, "flutter_clean"))
        bad = [f for f in r["findings"] if f["tier"] == "F" or (f["tier"] == "D" and f["severity"] in ("major", "minor"))]
        self.assertEqual(bad, [])
        self.assertTrue(r["ok"])

    def test_every_finding_has_evidence_and_known_rule(self):
        catalog = rd(os.path.join(ROOT, "knowledge", "anti-slop.md"))
        for name in self.CASES:
            for f in scan(os.path.join(FIX, name))["findings"]:
                self.assertIn(f["evidence"], ("observed", "derived", "inferred"))
                self.assertRegex(catalog, rf"\| {f['rule']} \|", f"{f['rule']} not in catalog")

    def test_coverage_reports_unknown(self):
        d = tempfile.mkdtemp()
        try:
            big = os.path.join(d, "huge_screen.dart")
            with open(big, "w") as fh:
                fh.write("// x\n" * 200_000)
            r = scan(d)
            self.assertEqual(len(r["coverage"]["unknown"]), 1)
        finally:
            shutil.rmtree(d)


class TestDNA(unittest.TestCase):
    def test_proposal(self):
        d = dna.dna(scan(os.path.join(FIX, "flutter_slop")))
        self.assertLessEqual(len(d["proposal"]["type"]["scale"]), 7)
        self.assertLess(d["coherence"]["type"], 0.6)
        text = dna.to_kdl(d)
        doc = kdl.parse("kdl: 1\nmode: code-to-design\nproduct: {name: x, users: y, moment: z}\n" + text)
        self.assertIn("scale", doc["system"]["type"])


def _have(cmd):
    return shutil.which(cmd) is not None


KOTLINC = os.environ.get("KOTLINC") or next(
    (p for p in ("/Applications/Android Studio.app/Contents/plugins/Kotlin/kotlinc/bin/kotlinc",) if os.path.exists(p)), None)


class TestExport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = kdl.parse_file(LUNE)
        cls.tmp = tempfile.mkdtemp()
        cls.files = {}
        for st in export.STACKS:
            p = os.path.join(cls.tmp, export.FILENAMES[st])
            with open(p, "w") as fh:
                fh.write(export.export(cls.doc, st, "examples/lune/design.kdl"))
            cls.files[st] = p

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_physics(self):
        p = export.spring_physics(0.4, 0.9)
        self.assertAlmostEqual(p["stiffness"], (2 * 3.141592653589793 / 0.4) ** 2, delta=0.05)
        ms, pts = export.spring_samples(0.4, 1.0, 20)
        self.assertLessEqual(max(pts), 1.0005)  # critically damped: no overshoot
        ms2, pts2 = export.spring_samples(0.4, 0.5, 20)
        self.assertGreater(max(pts2), 1.05)  # underdamped overshoots

    def test_identifiers(self):
        self.assertEqual(export.ident("2xl"), "xxl")
        self.assertEqual(export.ident("on-accent"), "onAccent")
        self.assertEqual(export.ident("text-2", "pascal"), "Text2")

    def test_contents(self):
        dart = rd(self.files["flutter"])
        self.assertIn("class KColors extends ThemeExtension<KColors>", dart)
        self.assertIn("MediaQuery.disableAnimationsOf", dart)
        swift = rd(self.files["swiftui"])
        self.assertIn("accessibilityReduceMotion", swift)
        self.assertIn("@ScaledMetric", swift)
        css = rd(self.files["css"])
        self.assertIn("prefers-reduced-motion", css)
        self.assertRegex(css, r"--k-spring-gentle: linear\(")

    @unittest.skipUnless(_have("xcrun"), "xcrun not available")
    def test_swift_typechecks(self):
        for target, sdk in (("arm64-apple-ios17.0-simulator", ["--sdk", "iphonesimulator"]), ("arm64-apple-macos14.0", [])):
            r = subprocess.run(["xcrun", *sdk, "swiftc", "-typecheck", "-target", target, self.files["swiftui"]],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr[-2000:])

    @unittest.skipUnless(_have("xcrun"), "xcrun not available")
    def test_swift_font_width_typechecks(self):
        doc = kdl.parse_file(LUNE)
        doc["system"]["type"]["scale"]["display"]["width"] = "condensed"
        doc["system"]["type"]["families"]["numeric"] = "SF Pro Condensed"
        p = os.path.join(self.tmp, "Width.swift")
        with open(p, "w") as fh:
            fh.write(export.export(doc, "swiftui"))
        self.assertIn("width: .condensed", rd(p))
        r = subprocess.run(["xcrun", "--sdk", "iphonesimulator", "swiftc", "-typecheck", "-target",
                            "arm64-apple-ios17.0-simulator", p], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])

    @unittest.skipUnless(_have("tsc"), "tsc not available")
    def test_typescript_typechecks(self):
        # the shim mirrors React Native 0.81's own signatures (mutable FontVariant[], Platform.select)
        shim = os.path.join(self.tmp, "rn-shim.d.ts")
        with open(shim, "w") as fh:
            fh.write("""declare module 'react-native' {
  export function useColorScheme(): 'light' | 'dark' | null | undefined;
  export type FontVariant = 'small-caps' | 'oldstyle-nums' | 'lining-nums' | 'tabular-nums' | 'proportional-nums';
  export interface TextStyle {
    fontSize?: number; lineHeight?: number; letterSpacing?: number; fontFamily?: string;
    fontWeight?: 'normal' | 'bold' | '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900' | number;
    fontVariant?: FontVariant[];
  }
  export const Platform: { OS: 'ios' | 'android' | 'web'; select<T>(spec: { ios?: T; android?: T; default?: T }): T | undefined };
}
""")
        doc = kdl.parse_file(LUNE)
        doc["system"]["type"]["families"]["display"] = {"ios": "New York", "android": "Fraunces"}
        doc["system"]["type"]["scale"]["body"]["numerals"] = "tabular"
        doc["system"]["type"]["scale"]["body"]["family"] = "display"
        doc["system"]["color"]["data"] = {"food": "#C2410C", "rent": {"light": "#1D4ED8", "dark": "#93C5FD"}}
        rich = os.path.join(self.tmp, "tokens_rich.ts")
        with open(rich, "w") as fh:
            fh.write(export.export(doc, "react-native"))
        text = rd(rich)
        self.assertIn("Platform.select({ android: 'Fraunces' })", text)
        self.assertIn("fontVariant: ['tabular-nums']", text)
        self.assertIn("data: scheme === 'dark' ? dataDark : dataLight", text)
        usage = os.path.join(self.tmp, "use.ts")
        with open(usage, "w") as fh:  # the tokens must be assignable where RN expects a TextStyle
            fh.write("import type { TextStyle } from 'react-native';\nimport { type } from './tokens_rich';\n"
                     "const body: TextStyle = type.body;\nexport default body;\n")
        for files in ([self.files["react-native"], shim], [rich, usage, shim]):
            r = subprocess.run(["tsc", "--noEmit", "--strict", "--target", "es2020", "--module", "esnext",
                                "--moduleResolution", "bundler", *files], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout[-2000:])

    @unittest.skipUnless(KOTLINC, "kotlinc not found (set KOTLINC and JAVA_HOME)")
    def test_compose_compiles_against_signature_stubs(self):
        stubs = [os.path.join(ROOT, "tests", "compose_stubs", f) for f in sorted(os.listdir(os.path.join(ROOT, "tests", "compose_stubs")))]
        env = dict(os.environ)
        jbr = "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
        if "JAVA_HOME" not in env and os.path.isdir(jbr):
            env["JAVA_HOME"] = jbr
            env["PATH"] = os.path.join(jbr, "bin") + os.pathsep + env.get("PATH", "")
        r = subprocess.run(["bash", KOTLINC, "-nowarn", *stubs, self.files["compose"], "-d", os.path.join(self.tmp, "kout")],
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, (r.stdout + r.stderr)[-2000:])

    @unittest.skipUnless(os.environ.get("KINETIC_SLOW") and _have("flutter"), "set KINETIC_SLOW=1 with flutter on PATH")
    def test_flutter_analyzes(self):
        proj = os.path.join(self.tmp, "fl")
        subprocess.run(["flutter", "create", "--empty", "--project-name", "kcheck", proj], capture_output=True, check=True)
        shutil.copy(self.files["flutter"], os.path.join(proj, "lib"))
        r = subprocess.run(["flutter", "analyze", "lib/kinetic_tokens.dart"], cwd=proj, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])


class TestSVG(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_knowledge_icons_pass(self):
        text = rd(os.path.join(ROOT, "knowledge", "iconography-svg.md"))
        icons = re.findall(r"(<svg[\s\S]*?</svg>)", text)
        self.assertGreaterEqual(len(icons), 8)
        paths = []
        for i, s in enumerate(icons):
            p = os.path.join(self.tmp, f"i{i}.svg")
            with open(p, "w") as fh:
                fh.write(s)
            paths.append(p)
        r = svg.lint(paths)
        self.assertEqual(r["findings"], [], r["findings"][:3])

    def test_bad_icon_and_dtd(self):
        bad = os.path.join(self.tmp, "bad.svg")
        with open(bad, "w") as fh:
            fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" id="x"><g transform="translate(1,1)">'
                     '<path stroke="#333" stroke-width="1.3" d="M0.123 0.456 L 31 31.777"/>'
                     '<circle cx="16" cy="16" r="10" stroke-width="2" stroke="currentColor"/></g></svg>')
        self.assertTrue({"SVG01", "SVG03", "SVG04", "SVG05", "SVG07", "SVG09", "SVG10"} <= rules(svg.lint([bad])))
        xxe = os.path.join(self.tmp, "xxe.svg")
        with open(xxe, "w") as fh:
            fh.write('<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
                     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">&x;</svg>')
        r = svg.lint([xxe])
        self.assertIn("SVG12", rules(r))
        with self.assertRaises(ValueError):
            svg.normalize(xxe)

    def test_arc_geometry(self):
        pts = svg.arc_points(0, 10, 10, 10, 0, 0, 1, 20, 10)
        self.assertAlmostEqual(min(p[1] for p in pts), 0.0, places=6)


class TestStates(unittest.TestCase):
    def test_matrix(self):
        m = states.matrix(kdl.parse_file(LUNE))
        self.assertEqual(m["coverage"]["states_required"], m["coverage"]["states_covered"])

    def test_template_is_valid_kdl(self):
        doc = kdl.parse("screens:\n" + states.template("checkout"))
        self.assertIn("offline", doc["screens"][0]["states"])


class TestScore(unittest.TestCase):
    def _judged(self, val, **override):
        dims = {k: {"score": override.get(k, val), "evidence": ["shot-1: observed"], "fix": "x"} for k in score.JUDGED_DIMENSIONS}
        fd, p = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as fh:
            json.dump({"dimensions": dims}, fh)
        return p

    def test_gates(self):
        clean = os.path.join(FIX, "flutter_clean")
        self.assertEqual(score.run(LUNE, [clean])["verdict"], "measured-only")
        self.assertEqual(score.run(LUNE, [clean], self._judged(4))["verdict"], "ship")
        self.assertEqual(score.run(LUNE, [clean], self._judged(4, product_fit=2))["verdict"], "rethink")
        self.assertEqual(score.run(LUNE, [clean], self._judged(4, motion=2))["verdict"], "iterate")
        self.assertEqual(score.run(None, [os.path.join(FIX, "flutter_slop")], self._judged(5))["verdict"], "blocked")

    def test_stale_judgment_cannot_decide(self):
        d = tempfile.mkdtemp()
        try:
            j = self._judged(5)
            os.utime(j, (1, 1))  # judgment from 1970
            shutil.copy(os.path.join(FIX, "flutter_clean", "lib", "tonight_screen.dart"), d)
            r = score.run(LUNE, [d], j)
            self.assertEqual(r["verdict"], "iterate")
            self.assertTrue(any("older" in p for p in r["judged_problems"]))
        finally:
            shutil.rmtree(d)

    def test_scores_without_evidence_are_ignored(self):
        ok, problems = score.check_judged({"dimensions": {"hierarchy": {"score": 5, "evidence": []}}})
        self.assertNotIn("hierarchy", ok)
        self.assertTrue(any("without evidence" in p for p in problems))


class TestCLI(unittest.TestCase):
    def run_cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            code = cli.main(list(args))
        return code, buf.getvalue()

    def test_exit_codes(self):
        self.assertEqual(self.run_cli("validate", LUNE)[0], 0)
        self.assertEqual(self.run_cli("validate", os.path.join(FIX, "slop.kdl"))[0], 1)
        self.assertEqual(self.run_cli("scan", os.path.join(FIX, "flutter_slop"))[0], 1)
        self.assertEqual(self.run_cli("validate", "/nonexistent.kdl")[0], 2)
        code, out = self.run_cli("contrast", "#5C5249", "#F3F4F1", "--json")
        self.assertEqual(json.loads(out)["aa_body"], True)

    def test_init_create_skeleton_has_every_required_section(self):
        d = tempfile.mkdtemp()
        try:
            self.run_cli("init", d, "--stack", "swiftui", "--name", "Courant")
            doc = kdl.parse_file(os.path.join(d, ".kinetic", "design.kdl"))
            for section in validate.REQUIRED["create"]:
                self.assertIn(section, doc, section)
            self.assertEqual(doc["product"]["name"], "Courant")
        finally:
            shutil.rmtree(d)

    def test_init_does_not_overwrite(self):
        d = tempfile.mkdtemp()
        try:
            open(os.path.join(d, "pubspec.yaml"), "w").close()
            self.run_cli("init", d)
            p = os.path.join(d, ".kinetic", "design.kdl")
            with open(p, "a") as fh:
                fh.write("# mine\n")
            self.run_cli("init", d)
            self.assertTrue(rd(p).endswith("# mine\n"))
            self.assertEqual(json.loads(rd(os.path.join(d, ".kinetic", "config.json")))["stack"], "flutter")
        finally:
            shutil.rmtree(d)

    def test_export_refuses_handwritten(self):
        d = tempfile.mkdtemp()
        try:
            target = os.path.join(d, "kinetic_tokens.dart")
            with open(target, "w") as fh:
                fh.write("// my own theme\n")
            self.assertEqual(self.run_cli("export", LUNE, "--stack", "flutter", "--out", target)[0], 2)
            self.assertEqual(rd(target), "// my own theme\n")
        finally:
            shutil.rmtree(d)


class TestRound4Regressions(unittest.TestCase):
    """False positives and gaps found by the round-4 A/B arms (Flutter + React Native)."""

    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def write(self, rel, text):
        p = os.path.join(self.d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        return p

    def test_categorical_palette_is_data_not_accent_chaos(self):
        self.write("lib/theme.dart", "import 'package:flutter/material.dart';\nconst circuits = {\n" + "".join(
            f"  Circuit.c{i}: Color(0xFF{h}),\n" for i, h in enumerate(["F0BE2C", "3B9A57", "2E6AD1", "D23C2E", "7E4DC0"])) + "};\n")
        r = scan(os.path.join(self.d, "lib"))
        self.assertFalse(any(f["rule"] == "D13" and "hue families" in f["message"] for f in r["findings"]))

    def test_theme_accessor_counts_as_semantic_text_style(self):
        body = "".join(f"      Text('a', style: t.body),\n      Text('b', style: t.title),\n" for _ in range(6))
        self.write("lib/screen.dart", "import 'package:flutter/material.dart';\nWidget b(t) => Column(children: [\n" + body +
                   "".join(f"      Text('x', style: TextStyle(fontSize: {12 + i})),\n" for i in range(4)) + "]);\n")
        self.write("lib/design/kinetic_tokens.dart", "// GENERATED by `kinetic export` from design.kdl\n" +
                   "".join(f"const s{i} = TextStyle(fontSize: {10 + i});\n" for i in range(12)))
        r = scan(os.path.join(self.d, "lib"))
        self.assertFalse(any(f["rule"] == "D12" and "semantic" in f["message"] for f in r["findings"]))

    def test_fixture_folder_is_a_fixture(self):
        self.write("fixtures/photoArt.tsx", "import { View } from 'react-native';\nexport const A = () => <View style={{backgroundColor: '#C2410C', borderColor: '#1D4ED8', shadowColor: '#7E22CE'}} />;\n")
        r = scan(self.d)
        self.assertIn("fixtures/photoArt.tsx", " ".join(r["coverage"]["fixture_files"]))
        self.assertNotIn("D13", rules(r))

    def test_exceptions_waive_d_findings_but_never_f(self):
        self.write("lib/app.dart", "import 'package:flutter/material.dart';\n"
                   "Widget a() => Scaffold(floatingActionButton: FloatingActionButton(onPressed: go, child: Icon(Icons.add)));\n")
        ex = [{"rule": "D09", "where": "app.dart", "reason": "Android-only FAB in session mode, on purpose"},
              {"rule": "F08", "reason": "cannot waive an F rule"}]
        r = scan(os.path.join(self.d, "lib"), exceptions=ex)
        self.assertNotIn("D09", rules(r))
        self.assertEqual([w["rule"] for w in r["waived"]], ["D09"])
        v = validate.validate_text("kdl: 1\nmode: audit\nproduct: {name: T, stack: flutter}\naudit: {findings: []}\n"
                                   "exceptions:\n  - {rule: F08, reason: we did not have time for it}\n")
        self.assertTrue(any(f["rule"] == "K08" and f["tier"] == "F" for f in v["findings"]))

    def test_optical_comment_exempts_spacing(self):
        self.write("lib/a.dart", "import 'package:flutter/material.dart';\n" + "".join(
            f"final p{i} = EdgeInsets.only(top: 7); // optical: DIN sits 2pt low next to Roboto\n" for i in range(12)))
        self.assertNotIn("D17", rules(scan(os.path.join(self.d, "lib"))))

    def test_prose_may_open_with_a_quotation(self):
        doc = kdl.parse('premortem:\n  - {risk: "~" prefix reads as noise, fix: drop it when live}\n')
        self.assertEqual(doc["premortem"][0]["risk"], '"~" prefix reads as noise')

    def test_unknown_keys_and_status_partners(self):
        text = rd(LUNE).replace("      body:    {size: 17, line: 24, weight: 400, track: 0}",
                                "      body:    {size: 17, line: 24, weight: 400, track: 0, platform_note: x}")
        v = validate.validate_text(text + "\nbogus_section: 1\n")
        msgs = " ".join(f["message"] for f in v["findings"] if f["rule"] == "K18")
        self.assertIn("platform_note", msgs)
        self.assertIn("bogus_section", msgs)
        self.assertTrue(validate._is_status_role("on-danger") and validate._is_status_role("warning-wash"))
        self.assertFalse(validate._is_status_role("accent"))

    def test_stack_inferred_from_sources_without_manifest(self):
        self.write("Gallery.tsx", "import { View } from 'react-native';\nexport const g = [];\n")
        from kinetic import project
        self.assertEqual(project.detect_stack(self.d)[0], "react-native")

    def test_export_out_creates_the_folder(self):
        out = os.path.join(self.d, "lib", "design") + os.sep
        with contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(["export", LUNE, "--stack", "flutter", "--out", out])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(os.path.join(out, export.FILENAMES["flutter"])))


class TestHook(unittest.TestCase):
    def test_silent_outside_and_active_inside(self):
        d = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(d, "lib"))
            f = os.path.join(d, "lib", "home_screen.dart")
            shutil.copy(os.path.join(FIX, "flutter_slop", "lib", "home_screen.dart"), f)
            payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": f}})
            hook = os.path.join(ROOT, "hooks", "post_edit.py")
            r = subprocess.run([sys.executable, "-I", hook], input=payload, capture_output=True, text=True)
            self.assertEqual((r.returncode, r.stdout), (0, ""))
            os.makedirs(os.path.join(d, ".kinetic"))
            r = subprocess.run([sys.executable, "-I", hook], input=payload, capture_output=True, text=True)
            ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn("F10", ctx)
            r = subprocess.run([sys.executable, "-I", hook], input="not json", capture_output=True, text=True)
            self.assertEqual((r.returncode, r.stdout), (0, ""))
        finally:
            shutil.rmtree(d)


LIBRARY_KDL = """kdl: 1
mode: create
product: {name: Shelf, stack: flutter, platforms: [ios, android], users: readers, moment: at the returns slot,
          frequency: weekly, stakes: low, density: low, brand: {status: none}}
thesis: {statement: the library card that tells you what is due before the fine does, feel: [calm], never: [a fine notice],
         spine: due dates are stamps}
expression: {level: 2, because: weekly utility}
inventory: [the date stamp, spine labels, the returns slot, the reading room, the card number, the hold shelf,
            the overdue slip, the opening hours board]
idea: {subject_item: the date stamp, becomes: days left as stamps, competitor_test: {competitor: Libby, fails_because: no stamps}}
directions:
  - {id: A, engine: ENG_A, name: Stamped, axes: {structure: a, density: b, color: c, type: d, motion: e},
     scores: {product_fit: 4, distinctiveness: 3, usability: 4, feasibility: 4, risk_of_slop: 2}, verdict: chosen, because: x}
  - {id: B, engine: ENG_B, name: Shelf, axes: {structure: f, density: g, color: h, type: i, motion: j},
     scores: {product_fit: 4, distinctiveness: 5, usability: 4, feasibility: 4, risk_of_slop: 2}, verdict: rejected, because: y}
  - {id: C, engine: ENG_C, name: Board, axes: {structure: k, density: l, color: m, type: n, motion: o},
     scores: {product_fit: 2, distinctiveness: 5, usability: 3, feasibility: 3, risk_of_slop: 3}, verdict: rejected, because: z}
vocabulary:
  - {mark: stamp, from: the date stamp, replaces: progress_bar, sites: [hero, loan rows]}
  - {mark: spine, from: spine labels, replaces: data_mark, sites: [loan rows, empty shelf]}
contract: {thesis: a, idea: b, own_world: c, first_viewport: d, vocabulary: e, signature_move: f, live_thing: g}
"""


class TestV16Identity(unittest.TestCase):
    def test_deal_is_seeded_diverse_and_contrast_checked(self):
        a = deal.deal("a library app for loans and holds", seed=11)
        b = deal.deal("a library app for loans and holds", seed=11)
        c = deal.deal("a library app for loans and holds", seed=12)
        ids = lambda st: [o["engine"]["id"] for o in st["options"]]
        self.assertEqual(ids(a), ids(b))
        self.assertEqual(len({o["engine"]["family"] for o in a["options"]}), 3)
        self.assertNotEqual([ids(deal.deal("x", seed=s)) for s in range(5)].count(ids(c)), 5)
        for o in a["options"]:
            for theme, r in o["palette"]["roles"].items():
                self.assertGreaterEqual(color.wcag(r["text"], r["bg"]), 4.5)
                if "field" in r:
                    self.assertGreaterEqual(color.wcag(r["on-field"], r["field"]), 4.5, (o["palette"]["id"], theme))

    def test_every_library_palette_field_has_readable_ink(self):
        lib = deal.load_library()
        for p in lib["palette"]:
            roles = deal._roles(p)
            for theme, r in roles.items():
                for k in [k for k in r if k == "field" or k.startswith("state-")]:
                    self.assertGreaterEqual(color.wcag(r["on-" + k], r[k]), 4.5, (p["id"], theme, k))
                self.assertTrue(all(c["ok"] for c in color.check_roles({theme: {k: v for k, v in r.items()
                                                                                  if not k.startswith(("field", "on-field", "state-", "on-state-"))}})), p["id"])

    def test_redraw_needs_a_reason_and_is_logged(self):
        st = deal.deal("library", seed=3)
        with self.assertRaises(ValueError):
            deal.redraw(st, 1, "type", "nicer")
        old = st["options"][0]["type"]["id"]
        st = deal.redraw(st, 1, "type", "the brand pins a slab serif in its signage")
        self.assertNotEqual(st["options"][0]["type"]["id"], old)
        self.assertEqual(st["history"][0]["from"], old)

    def test_identity_gate(self):
        st = deal.deal("library", seed=5)
        e = [o["engine"]["id"] for o in st["options"]]
        text = LIBRARY_KDL.replace("ENG_A", e[0]).replace("ENG_B", e[1]).replace("ENG_C", e[2])
        rules = lambda r: {(f["rule"], f["severity"]) for f in r["findings"]}
        r = validate.validate_text(text, deal=st)
        self.assertIn(("K30", "major"), rules(r))          # B is viable and more distinctive than A
        self.assertNotIn(("K29", "major"), rules(r))
        self.assertNotIn(("K31", "major"), rules(r))       # 4 sites incl. hero
        r = validate.validate_text(text.replace(e[0], "ledger-made-up"), deal=st)
        self.assertIn(("K29", "major"), rules(r))
        r = validate.validate_text(text.replace("subject_item: the date stamp", "subject_item: a moon"), deal=st)
        self.assertIn(("K28", "minor"), rules(r))
        bare = re.sub(r"(?ms)^vocabulary:.*?(?=^contract:)", "", text)
        self.assertIn(("K31", "major"), rules(validate.validate_text(bare, deal=st)))

    def test_scan_flags_spent_defaults_and_vocabulary_leftovers(self):
        d = tempfile.mkdtemp()
        try:
            with open(os.path.join(d, "home.dart"), "w") as fh:
                fh.write("import 'package:flutter/material.dart';\n"
                         "const bg = Color(0xFFF4F1EA);\n"
                         "final t = TextStyle(fontFamily: 'Space Grotesk');\n"
                         "Widget p() => LinearProgressIndicator(value: 0.3);\n")
            got = {f["rule"] for f in scan([d], vocab_roles={"progress_bar"})["findings"]}
            self.assertTrue({"D33", "D34", "D35"} <= got, got)
            got = {f["rule"] for f in scan([d])["findings"]}
            self.assertNotIn("D35", got)
        finally:
            shutil.rmtree(d)

    def test_contact_sheet_roundtrip(self):
        d = tempfile.mkdtemp()
        try:
            rows = [bytearray(b"".join(bytes((x * 4 % 256, y * 4 % 256, 90)) for x in range(60))) for y in range(100)]
            for i in range(3):
                sheet.write_png(os.path.join(d, f"s{i}.png"), 60, 100, rows)
            r = sheet.contact_sheet([d], os.path.join(d, "out.png"), 0, 30)
            w, h, px = sheet.read_png(r["out"])
            self.assertEqual((r["count"], w), (3, 12 + 3 * (30 + 12)))
            self.assertEqual(px[12][12 * 3:12 * 3 + 3], bytearray((2, 2, 90)))  # 2x2 box average
        finally:
            shutil.rmtree(d)


class TestRound5Regressions(unittest.TestCase):
    def test_validate_honours_exceptions_but_never_f(self):
        text = rd(os.path.join(ROOT, "examples", "lune", "design.kdl"))
        base = {f["rule"] for f in validate.validate_text(text)["findings"]}
        self.assertIn("K29", base)
        r = validate.validate_text(text + "\nexceptions:\n  - {rule: K29, reason: this example has no deal file on purpose}\n")
        self.assertNotIn("K29", {f["rule"] for f in r["findings"]})
        self.assertEqual(r["waived"][0]["rule"], "K29")

    def test_export_out_without_extension_is_a_folder(self):
        d = tempfile.mkdtemp()
        try:
            out = os.path.join(d, "design")
            with contextlib.redirect_stdout(io.StringIO()):
                code = cli.main(["export", os.path.join(ROOT, "examples", "lune", "design.kdl"), "--stack", "react-native", "--out", out])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.isdir(out))
        finally:
            shutil.rmtree(d)

    def test_alert_role_is_a_status_role(self):
        self.assertTrue(validate._is_status_role("alert"))
        self.assertTrue(validate._is_status_role("on-alert"))


def _png_with_lines(path, n_lines, words_per_line, gap=40):
    w, h = 393, 852
    rows = [bytearray(b"\xf8\xf8\xf8" * w) for _ in range(h)]
    y = 60
    for _ in range(n_lines):
        for yy in range(y, y + 14):
            x = 20
            for _ in range(words_per_line):
                for xx in range(x, min(x + 30, w - 10)):
                    if (xx + yy) % 3 == 0:
                        rows[yy][3 * xx:3 * xx + 3] = b"\x20\x20\x20"
                x += 44
        y += 14 + gap
        if y > h - 30:
            break
    sheet.write_png(path, w, h, rows)


class TestV17Studio(unittest.TestCase):
    def test_clarity_separates_sparse_from_dense(self):
        d = tempfile.mkdtemp()
        try:
            _png_with_lines(os.path.join(d, "calm.png"), 6, 3, gap=60)
            _png_with_lines(os.path.join(d, "dense.png"), 40, 8, gap=4)
            calm = clarity.measure(os.path.join(d, "calm.png"))
            dense = clarity.measure(os.path.join(d, "dense.png"))
            self.assertLess(calm["lines"], dense["lines"])
            self.assertLess(calm["words"], dense["words"])
            self.assertGreater(clarity.grade(calm)["clarity"], 85)
            self.assertLess(clarity.grade(dense)["clarity"], 60)
        finally:
            shutil.rmtree(d)

    def test_panel_median_split_and_consensus(self):
        def c(scores, fix):
            return {"dimensions": {"hierarchy": {"score": scores[0], "fix": fix},
                                   "distinctiveness": {"score": scores[1], "fix": "draw the vocabulary in the hero"}},
                    "tests": {"squint": "pass"}, "biggest_lever": fix}
        r = panel.merge([c((4, 3), "reduce the stacked bottom chrome under the hero"),
                         c((2, 4), "remove the stacked bottom chrome and the pinned bar"),
                         c((4, 4), "tighten copy")])
        self.assertEqual(r["dimensions"]["hierarchy"]["score"], 4)
        self.assertIn("hierarchy", r["panel"]["split"])
        self.assertTrue(any(f.startswith("hierarchy") for f in r["panel"]["consensus_fixes"]))
        self.assertFalse(r["self_judged"])
        with self.assertRaises(ValueError):
            panel.merge([c((4, 4), "x")])


class TestPluginStructure(unittest.TestCase):
    def test_skills_frontmatter_and_links(self):
        for name in os.listdir(os.path.join(ROOT, "skills")):
            text = rd(os.path.join(ROOT, "skills", name, "SKILL.md"))
            m = re.match(r"---\nname: (\S+)\ndescription: \"(.+?)\"\n", text)
            self.assertTrue(m, name)
            self.assertEqual(m.group(1), name)
            self.assertLess(len(m.group(2)), 1024, name)
            for ref in re.findall(r"`(knowledge/[\w/-]+\.md)`", text):
                self.assertTrue(os.path.exists(os.path.join(ROOT, ref)), f"{name}: {ref}")
            for ref in re.findall(r"`(docs/[\w-]+\.md)`", text):
                self.assertTrue(os.path.exists(os.path.join(ROOT, ref)), f"{name}: {ref}")

    def test_manifests(self):
        for p in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/marketplace.json", "hooks/hooks.json"):
            json.loads(rd(os.path.join(ROOT, p)))


if __name__ == "__main__":
    unittest.main()
