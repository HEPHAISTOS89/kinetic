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

from kinetic import cli, color, dna, export, kdl, score, states, svg, validate  # noqa: E402
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
        shim = os.path.join(self.tmp, "rn-shim.d.ts")
        with open(shim, "w") as fh:
            fh.write("declare module 'react-native' { export function useColorScheme(): 'light' | 'dark' | null | undefined; }\n")
        r = subprocess.run(["tsc", "--noEmit", "--strict", "--target", "es2020", "--module", "esnext",
                            "--moduleResolution", "bundler", self.files["react-native"], shim], capture_output=True, text=True)
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
        code, out = self.run_cli("contrast", "#5C5249", "#F6F1EA", "--json")
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
