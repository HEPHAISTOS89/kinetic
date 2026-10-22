"""Scaffold a blind round: make_round.py <workdir> <round> <briefs.json>
briefs.json: {"flutter": "<brief markdown without deliverables>", "rn": "..."}; arms K (Kinetic studio at KROOT_K),
C (Kinetic studio at KROOT_C, optional), T (taste-skill). Writes BRIEF.md, project scaffolds, each arm's TASK.md and the critic TASK.md."""
import json, os, shutil, sys
W, RND, BRIEFS = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
KROOT_K = os.environ["KROOT_K"]; KROOT_C = os.environ.get("KROOT_C"); VK = os.environ.get("VK", "2.2"); VC = os.environ.get("VC", "2.1")
H = os.path.join(W, "harness")
E = os.path.join(W, f"eval{RND}")
FL_DELIV = """## Deliverables (all in your working directory)
- A Flutter project (already scaffolded: `pubspec.yaml`, `lib/`, `test/render_test.dart`).
  Put your code in `lib/`. Available packages (offline, already in pubspec): flutter,
  cupertino_icons, flutter_svg, intl. No network: no google_fonts download, no network images.
  You may bundle fonts: copy .ttf/.otf files from /System/Library/Fonts/Supplemental or
  /Library/Fonts into `fonts/` and declare them in pubspec.yaml (see the comment there).
- `lib/gallery.dart` must expose every state you designed:
  `typedef GalleryEntry = (String name, Widget Function(Brightness brightness) build);`
  `List<GalleryEntry> get gallery => [...]` — each builder returns the whole app for that
  state (your theme included) in the given brightness. Short kebab-case names.
  Include as many states as you consider necessary.
- Render and look at your own result as many times as you like:
  `flutter test --update-goldens test/render_test.dart`
  (renders each entry at 393×852 logical px, top-aligned/cropped, with iPhone-like safe-area
  insets, light and dark, into ./shots). Do not modify `test/render_test.dart`.
  Note: the renderer has no SF Pro; Roboto stands in for the system font on both platforms.
  Text scaling is not rendered unless you build an entry that sets it (MediaQuery textScaler).
- `flutter analyze` must report no errors.
- A short NOTES.md: what you designed and why (≤ 25 lines).
"""
RN_DELIV = """## Deliverables (all in your working directory)
- TypeScript/TSX source files. Allowed imports: `react`, `react-native`,
  `react-native-svg` (draw your own icons with it — there is no icon font),
  `react-native-safe-area-context` (the harness provides the insets: use
  `useSafeAreaInsets` / `SafeAreaView`, but do not add a `SafeAreaProvider`).
  Nothing else (no npm install). Images: no network; draw placeholders or use local files.
  You may bundle fonts: copy .ttf/.otf files from /System/Library/Fonts/Supplemental or
  /Library/Fonts into `fonts/`; the font family name is the file name without extension
  (one file per weight, as React Native does on Android).
- `Gallery.tsx` at the root of your directory, exporting every state you designed:
  `export const gallery: Array<[string, React.ComponentType]> = [...]`
  (each component renders the whole screen for that state; read the colour scheme with
  `useColorScheme()`). Short kebab-case names. Include as many states as you consider necessary.
- Render and look at your own result as many times as you like, from your directory:
  `node <HARNESS>/render.mjs`
  It type-checks every .ts/.tsx file (strict, React Native 0.81 types) and renders each
  entry at 393×852pt, top-aligned/cropped, with iPhone-like safe-area insets, light and dark,
  into ./shots (react-native-web in Chromium; the system font renders as SF Pro).
  The type-check must pass.
- A short NOTES.md: what you designed and why (≤ 25 lines).
"""
FORBID = 'Do NOT read anything outside your working directory, KROOT and the brief, except system fonts; never read other arms\' folders, any "keys" folder or *_key*.json, and never read the folders "kinetic", "kinetic-v16", "kinetic-v17" or "kinetic-control" other than your own KROOT.'
def kinetic_task(stack, arm, kroot, ver):
    wd = os.path.join(E, stack, arm)
    harness = f'\n- The harness directory <HARNESS> is: {H}/rn (do not modify it; run it as `node "<HARNESS>/render.mjs"` from your directory — quote the path).' if stack == "rn" else ""
    check = "the harness type-check passes" if stack == "rn" else "`flutter analyze` reports no errors"
    return f"""You are the lead of a mobile design studio. Complete the design task in the brief below using the Kinetic design plugin in **studio** mode, with a real team of sub-agents.

Constraints for this task:
- Use the Kinetic plugin located at {kroot} (call it KROOT; it is Kinetic v{ver}). Start by reading KROOT/skills/kinetic/SKILL.md and then KROOT/skills/kinetic-studio/SKILL.md, and follow the studio protocol for mode `create` at depth D2, reading in the order the router gives. The engine is KROOT/bin/kinetic — run it as `bash "KROOT/bin/kinetic" …` (the path contains spaces).
- You CAN launch sub-agents with your Agent tool: do it for every studio role (3 directors in parallel + the rival in the same message; the editor; 3 critics with their lenses in parallel). Launch each as a `general-purpose` agent whose prompt starts with: "Act as the agent defined in KROOT/agents/kinetic-<role>.md — read that file first and follow it exactly." followed by the absolute KROOT path, the file paths it needs, its specific instruction and the output file it must write. Tell every sub-agent the same reading limits as yours.
- Do NOT invoke any other skills, plugins or slash commands (an installed "kinetic" plugin included — use only KROOT). Do NOT read KROOT/evals, KROOT/README.md or KROOT/docs/EVALUATION.md. {FORBID}
- Work only inside this directory (your working directory for all files, including `.kinetic/` and helper scripts): {wd}{" (a Flutter project is already scaffolded there; use `flutter pub get --offline` if needed — no network)" if stack == "flutter" else ""}{harness}
- Read the brief at {os.path.join(E, stack, "BRIEF.md")} and deliver exactly what it asks.
- Aim for the best, most premium, most thoughtful result — clean and uncluttered as well as distinctive. Render and inspect your screenshots (open the PNGs), and iterate (max 3 studio loops; the last loop ends with a panel on the final renders).
- At the end: {check}, ./shots contains the final renders of every gallery entry (re-render after your last change; delete stale shots). Leave .kinetic/ (design.kdl, deal.json, studio/, critique.json) and run `kinetic validate`, `kinetic scan`, `kinetic clarity shots` and `kinetic score --renders shots --judged .kinetic/critique.json`.

Keep a short candid log in KINETIC_FEEDBACK.md of every place where the Kinetic instructions, knowledge, engine or studio protocol were unclear, wrong, missing something or got in your way.

When done, reply with a short summary: gallery entries, what was authored/dealt and chosen, main design decisions, final engine results, and the top 5 items from KINETIC_FEEDBACK.md.
"""
def taste_task(stack):
    wd = os.path.join(E, stack, "T")
    harness = f'\n- The harness directory <HARNESS> is: {H}/rn (do not modify it; run it as `node "<HARNESS>/render.mjs"` from your directory — quote the path).' if stack == "rn" else ""
    check = "the harness type-check passes" if stack == "rn" else "`flutter analyze` reports no errors"
    return f"""You are a skilled mobile designer-engineer. Complete the design task in the brief below using the "taste-skill" (design-taste-frontend) design skill.

Constraints for this task:
- Use the skill installed at ~/.claude/skills/taste-skill: start by reading ~/.claude/skills/taste-skill/SKILL.md and follow its workflow as fully as it applies to a native app screen (its direction dealing scripts, idea engines, house rules, critique passes). Where a step is web-only, adapt it: use the render harness and judge the PNGs instead. You may read any file inside ~/.claude/skills/taste-skill and run its scripts (write output inside your working directory). Do NOT invoke any other skills, plugins or slash commands. {FORBID}
- Work only inside this directory: {wd}{" (a Flutter project is already scaffolded there; use `flutter pub get --offline` if needed — no network)" if stack == "flutter" else ""}{harness}
- Read the brief at {os.path.join(E, stack, "BRIEF.md")} and deliver exactly what it asks.
- Aim for the best, most premium, most thoughtful result you can. Render and inspect your screenshots, critique them as a demanding design director would, and iterate until you are satisfied.
- At the end: {check} and ./shots contains the final renders of every gallery entry (re-render after your last change; delete stale shots).

When done, reply with a short summary: gallery entries, which parts of the skill you used (and what you adapted), and the main design decisions.
"""
def critic_task(stack):
    j = os.path.join(E, stack, "judge")
    rend = ("Renders are static 393×852pt (top-aligned, cropped, iPhone-like safe areas, no status bar drawn), light and dark, produced by react-native-web in Chromium (system font = SF Pro)."
            if stack == "rn" else
            "Renders are static 393×852 logical px (top-aligned, cropped, iPhone-like safe areas, no status bar drawn), light and dark, produced by Flutter's test renderer. Roboto stands in for the system font on all designs (SF Pro is unavailable to the renderer) — do not penalise any design for Roboto appearing where an iOS build would show SF.")
    return f"""You are an exacting, fair mobile design director doing a BLIND review of three independent designs (X, Y and Z) of the same mobile screen. You do not know who made them and must not try to find out.

Strict rules:
- Read ONLY these: the brief {j}/BRIEF.md ; the renders in the X/, Y/ and Z/ folders of {j}/blind/ ; and the rubric {W}/rubric/taste-rubric.md plus the "deeper tests" section of {W}/rubric/anti-slop.md.
- Do NOT read anything else: no other folders, no keys, no source code, NOTES or other files. Do not invoke skills or plugins.
- Look at every render of all three designs (open the PNG files with your Read tool). Each design shows the states its author chose (the number of states differs); judging which states exist and how well they're handled is part of "anticipation" — reward states that matter, not sheer count.
- {rend} Some entries are the same screen scrolled further. Motion cannot be judged: leave it unjudged. Judge large-text behaviour only if a design renders it.

Score each design on the rubric's dimensions except motion (product_fit, hierarchy, distinctiveness, typography, color, layout_craft, native_fidelity, anticipation, copy), 1–5 against the anchors (3 = competent and forgettable). Every score needs concrete evidence citing render filenames, and one concrete fix. Also run the swap/squint/silence/thumb/night/thesis tests on each. Separately (not part of the rubric), rate each design's CLEANNESS 1–5: how uncluttered, calm and classy the screens are — few words, no dense text, generous space, one loud thing per screen (5 = reference-grade calm and clear; 1 = crowded walls of text and boxes), with evidence. Finally rank the three designs.

Return ONLY JSON:
{{"X": {{"dimensions": {{name: {{"score": int, "evidence": [str], "fix": str}}}}, "clean": {{"score": int, "evidence": [str]}}, "tests": {{...}}, "biggest_lever": str}},
 "Y": {{...same...}}, "Z": {{...same...}},
 "comparison": {{"ranking": ["best label", "second", "third"], "margins": {{"first_vs_second": "large"|"clear"|"slight"|"none", "second_vs_third": "large"|"clear"|"slight"|"none"}}, "why": str (≤6 sentences), "what_each_does_best": {{"X": [str], "Y": [str], "Z": [str]}}}}}}
"""
for stack, text in BRIEFS.items():
    d = os.path.join(E, stack); os.makedirs(os.path.join(d, "judge", "prompt"), exist_ok=True)
    brief = text.rstrip() + "\n\n" + (FL_DELIV if stack == "flutter" else RN_DELIV)
    open(os.path.join(d, "BRIEF.md"), "w").write(brief); open(os.path.join(d, "judge", "BRIEF.md"), "w").write(brief)
    arms = {"K": kinetic_task(stack, "K", KROOT_K, VK), "T": taste_task(stack)}
    if KROOT_C:
        arms["C"] = kinetic_task(stack, "C", KROOT_C, VC)
    for arm, task in arms.items():
        a = os.path.join(d, arm); os.makedirs(a, exist_ok=True)
        if stack == "flutter":
            shutil.copytree(os.path.join(H, "flutter", "template"), a, dirs_exist_ok=True)
            os.makedirs(os.path.join(a, "test"), exist_ok=True); os.makedirs(os.path.join(a, "fonts"), exist_ok=True)
            shutil.copy(os.path.join(H, "flutter", "render_test.dart"), os.path.join(a, "test"))
        open(os.path.join(a, "TASK.md"), "w").write(task)
    open(os.path.join(d, "judge", "prompt", "TASK.md"), "w").write(critic_task(stack))
print("ok", E)
