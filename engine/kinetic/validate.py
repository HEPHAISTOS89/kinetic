"""Semantic validation of a KDL decision record.

Every check is `derived` evidence: computed from the decisions written in the
file, never from a render. Codes: catalog IDs (F/D) when the check maps to a
catalog rule, K-codes for structural completeness."""
from __future__ import annotations

import json
import os
import re

from . import color
from .kdl import KDLError, Map, Seq, line_of, parse_file, parse
from .report import Finding

MODES = {"create", "improve", "redesign", "audit", "system", "design-to-code",
         "code-to-design", "evolve"}

REQUIRED = {
    "create": ["product", "requirements", "thesis", "expression", "directions", "journeys", "system", "screens",
               "signature", "premortem"],
    "redesign": ["product", "requirements", "thesis", "expression", "audit", "directions", "journeys", "system",
                 "screens", "signature", "premortem"],
    "improve": ["product", "thesis", "audit", "screens", "premortem"],
    "system": ["product", "thesis", "expression", "system", "premortem"],
    "audit": ["product", "audit"],
    "design-to-code": ["product", "system", "screens"],
    "code-to-design": ["product", "audit"],
    "evolve": ["product", "thesis", "audit"],
}

ENUMS = {
    "product.stack": {"flutter", "swiftui", "compose", "react-native", "web", "mixed"},
    "product.frequency": {"continuous", "daily", "weekly", "occasional", "rare"},
    "product.stakes": {"low", "medium", "high"},
    "product.density": {"low", "medium", "high"},
    "product.brand.status": {"none", "loose", "strict"},
    "system.shape.corner": {"continuous", "circular"},
    "system.elevation.strategy": {"tonal", "shadow", "border", "none", "mixed"},
    "system.motion.reduce": {"crossfade", "instant", "keep-feedback-only"},
}

INTERACTIVE = {"button", "icon-button", "link", "field", "toggle", "chip", "tab", "row"}
KINDS = {"text", "numeral", "button", "icon-button", "link", "field", "toggle", "chip", "tab",
         "row", "list", "card", "sheet", "dialog", "chart", "media", "badge", "progress",
         "nav-bar", "tab-bar", "toolbar", "image", "icon", "divider", "slider", "picker",
         "segmented", "stepper", "map", "avatar", "banner", "menu", "search"}
SCREEN_STATES = ["content", "loading", "empty", "error"]
REQUIRED_ROLES = ["bg", "surface", "text", "text-2", "border", "accent", "on-accent"]
SECTIONS = {"kdl", "mode", "product", "requirements", "thesis", "expression", "audit", "directions", "journeys",
            "system", "screens", "signature", "premortem", "exceptions",
            "inventory", "idea", "vocabulary", "contract"}
VOCAB_ROLES = {"progress_bar", "status_dot", "chip", "badge", "tab_icon", "empty_illustration", "data_mark", "divider",
               "input_control", "card", "banner", "map", "chart", "thumbnail", "header", "avatar", "background"}
CONTRACT_KEYS = ("thesis", "idea", "own_world", "first_viewport", "vocabulary", "signature_move", "live_thing")
STYLE_KEYS = {"size", "line", "weight", "track", "numerals", "width", "family", "case", "use"}
STATUS = ("danger", "success", "warning", "error", "info", "caution", "critical", "positive", "negative",
          "alert", "urgent", "attention")
MOTION_KINDS = ("feedback", "transition", "signature", "ambient")
LONG_DURATION = re.compile(r"(ambient|loop|breath|pulse|idle|shimmer)", re.I)


def _is_status_role(role: str) -> bool:
    """`danger`, `on-danger`, `danger-wash`, `warning-text`: status roles and their partners are not accents."""
    base = re.sub(r"^on-", "", role)
    return any(base == st or base.startswith(st + "-") for st in STATUS)


HAPTICS = {"selection", "light", "medium", "heavy", "soft", "rigid", "success", "warning",
           "error", "none"}

# level -> (saturated accents, type families max, motion signature max, display max)
BUDGET = {1: (1, 1, 1, 34), 2: (1, 2, 2, 40), 3: (2, 2, 3, 48), 4: (3, 2, 5, 64), 5: (4, 3, 99, 96)}

GENERIC_WORDS = {
    "seamless", "seamlessly", "modern", "clean", "intuitive", "sleek", "beautiful", "stunning",
    "user-friendly", "elegant", "minimal", "premium", "simple", "easy", "powerful", "innovative",
    "delightful", "effortless", "fluide", "intuitif", "intuitive", "moderne", "élégant", "épuré",
    "simple", "puissant", "innovant", "beau", "belle", "premium",
}
SLOP_PHRASES = [
    r"\bunlock (your|the|new|a|more|premium)\b", r"\bsupercharge", r"\belevate\b", r"\bempower", r"\brevolutioni[sz]e",
    r"\bnext[- ]level\b", r"\bcutting[- ]edge\b", r"\bgame[- ]changer\b", r"\bseamless",
    r"\bboostez\b", r"\brévolutionn", r"\bsans effort\b", r"\bdébloquez\b", r"\bpassez au niveau\b",
]
REF = re.compile(r"\$([a-z]+)\.([A-Za-z0-9_\-]+)")
REF_TARGETS = {
    "color": ("system.color.roles.light", "system.color.roles.dark"),
    "type": ("system.type.scale",),
    "space": ("system.space.scale",),
    "radius": ("system.shape.radius",),
    "spring": ("system.motion.springs",),
    "duration": ("system.motion.durations",),
    "haptic": ("system.haptics",),
    "data": ("system.color.data",),
}


def _get(doc, path):
    cur = doc
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def _is_na(v) -> bool:
    return isinstance(v, str) and v.strip().lower().startswith("n/a")


def _words(text: str) -> list:
    return re.findall(r"[\wÀ-ÿ'-]+", str(text).lower())


class Validator:
    def __init__(self, doc, path="design.kdl", deal=None, root=None):
        self.doc = doc
        self.path = path
        self.deal = deal
        self.root = root
        self.findings: list[Finding] = []
        self.checked: list[str] = []

    # ------------------------------------------------------------ helpers
    def add(self, rule, tier, severity, where, message, fix, line=0):
        self.findings.append(Finding(rule=rule, tier=tier, severity=severity, file=self.path,
                                     line=line, path=where, evidence="derived",
                                     message=message, fix=fix))

    def line(self, dotted: str) -> int:
        parts = dotted.split(".")
        node = self.doc
        ln = getattr(node, "line", 0)
        for p in parts:
            if isinstance(node, Map) and p in node:
                ln = node.lines.get(p, ln)
                node = node[p]
            elif isinstance(node, Seq) and p.isdigit() and int(p) < len(node):
                ln = node.lines[int(p)] if int(p) < len(node.lines) else ln
                node = node[int(p)]
            else:
                break
        return ln

    # -------------------------------------------------------------- run
    def run(self):
        doc = self.doc
        if not isinstance(doc, dict):
            self.add("K01", "F", "block", "", "document is not a mapping", "start with `kdl: 1`")
            return self
        mode = doc.get("mode", "create")
        if mode not in MODES:
            self.add("K18", "I", "major", "mode", f"unknown mode {mode!r}",
                     f"use one of: {', '.join(sorted(MODES))}", self.line("mode"))
            mode = "create"
        self.mode = mode
        for section in REQUIRED[mode]:
            if section not in doc or doc[section] in (None, ""):
                self.add("K01", "D", "major", section, f"mode `{mode}` requires `{section}`",
                         "list every must-have of the brief (id, need, priority) so the design can't silently drop one"
                         if section == "requirements" else f"write the `{section}` section (see docs/KDL.md)")
        for key in doc:
            if key not in SECTIONS:
                self.add("K18", "I", "minor", str(key), f"unknown section `{key}` (ignored by every check)",
                         f"sections: {', '.join(sorted(SECTIONS))}", self.line(str(key)))
        self.check_enums()
        self.check_product()
        self.check_thesis()
        level = self.check_expression()
        self.check_audit()
        self.check_directions()
        self.check_identity()
        self.check_system(level)
        self.check_screens(level)
        self.check_requirements()
        self.check_refs()
        self.check_signature()
        self.check_premortem()
        self.check_exceptions()
        return self

    def check_exceptions(self):
        """`exceptions`: findings accepted on purpose, each with a reason; `kinetic scan` reports them as waived."""
        ex = self.doc.get("exceptions")
        if ex is None:
            return
        if not isinstance(ex, list):
            self.add("K08", "D", "major", "exceptions", "`exceptions` must be a list of {rule, where, reason}",
                     "- {rule: D09, where: lib/app.dart, reason: why this is right here}", self.line("exceptions"))
            return
        for i, e in enumerate(ex):
            ln = self.line(f"exceptions.{i}") or self.line("exceptions")
            if not isinstance(e, dict) or not e.get("rule"):
                self.add("K08", "D", "major", f"exceptions.{i}", "an exception needs a `rule`",
                         "{rule: D09, where: lib/app.dart, reason: …}", ln)
                continue
            reason = str(e.get("reason") or "")
            if len(reason.split()) < 4 and not re.search(r"\bTODO\b", reason):  # TODO is reported by K02 already
                self.add("K02", "D", "major", f"exceptions.{i}.reason",
                         f"exception to {e['rule']} has no real reason",
                         "say why breaking the rule is right here, in a sentence a reviewer can check", ln)
            if str(e["rule"]).upper().startswith("F"):
                self.add("K08", "F", "block", f"exceptions.{i}.rule",
                         f"{e['rule']} is an F rule: F findings cannot be waived", "fix it instead", ln)

    def check_enums(self):
        for path, allowed in ENUMS.items():
            v = _get(self.doc, path)
            if v is not None and str(v) not in allowed:
                self.add("K18", "I", "minor", path, f"`{path}` = {v!r} is not in the vocabulary",
                         f"use one of: {', '.join(sorted(allowed))}", self.line(path))

    def check_product(self):
        p = self.doc.get("product")
        if not isinstance(p, dict):
            return
        self.checked.append("product")
        for k in ("name", "users", "moment"):
            if not p.get(k):
                self.add("K02", "D", "major", f"product.{k}", f"product.{k} is missing",
                         "a design without its user moment regresses to the average app",
                         self.line("product"))
        if not p.get("unknowns") and not p.get("facts"):
            self.add("K02", "C", "minor", "product.facts",
                     "no facts or unknowns recorded",
                     "separate observed facts from assumptions; list material unknowns",
                     self.line("product"))

    def check_thesis(self):
        t = self.doc.get("thesis")
        if not isinstance(t, dict):
            return
        self.checked.append("thesis")
        st = str(t.get("statement") or "")
        words = _words(st)
        if len(words) < 6:
            self.add("K04", "D", "major", "thesis.statement", "thesis statement is too short to steer design",
                     "one sentence: who, which moment, what the app does for them, how it should feel",
                     self.line("thesis.statement"))
        generic = [w for w in words if w in GENERIC_WORDS]
        if words and len(generic) / max(1, len(words)) > 0.15 or len(generic) >= 2:
            self.add("K04", "D", "major", "thesis.statement",
                     f"thesis leans on generic words: {', '.join(sorted(set(generic)))}",
                     "replace adjectives with the product's specific situation; could this sentence describe ten apps?",
                     self.line("thesis.statement"))
        for k in ("feel", "never", "spine"):
            if not t.get(k):
                self.add("K02", "D", "major", f"thesis.{k}", f"thesis.{k} is missing",
                         {"feel": "2–3 words for the target emotion",
                          "never": "what the app must never feel like (the anti-thesis)",
                          "spine": "one generative idea that links layout, color and motion"}[k],
                         self.line("thesis"))
        feel = t.get("feel") or []
        if isinstance(feel, list):
            g = [f for f in feel if str(f).lower() in GENERIC_WORDS]
            if g:
                self.add("K04", "C", "minor", "thesis.feel", f"generic feel words: {', '.join(map(str, g))}",
                         "name the emotion precisely (calm, held, brisk, confident, playful…)", self.line("thesis.feel"))

    def check_expression(self) -> int:
        e = self.doc.get("expression")
        if not isinstance(e, dict):
            return 3
        self.checked.append("expression")
        lvl = e.get("level")
        if not isinstance(lvl, int) or not 1 <= lvl <= 5:
            self.add("K06", "D", "major", "expression.level", f"expression.level must be 1–5, got {lvl!r}",
                     "1 precise … 5 expressive; decide from stakes, frequency, density and brand freedom",
                     self.line("expression.level"))
            return 3
        if not e.get("because"):
            self.add("K17", "D", "minor", "expression.because", "expression level has no reason",
                     "tie the level to stakes, frequency, density and brand freedom", self.line("expression"))
        stakes = _get(self.doc, "product.stakes")
        if stakes == "high" and lvl >= 4:
            self.add("K06", "D", "major", "expression.level",
                     f"expression {lvl} with high stakes",
                     "high-stakes products earn trust through precision; keep 1–3 and put expression in details",
                     self.line("expression.level"))
        return lvl

    def check_audit(self):
        a = self.doc.get("audit")
        if not isinstance(a, dict):
            return
        self.checked.append("audit")
        if not any(a.get(k) for k in ("keep", "evolve", "replace", "remove")):
            self.add("K19", "D", "major", "audit", "audit has no KEEP/EVOLVE/REPLACE/REMOVE classification",
                     "classify existing choices before redesigning", self.line("audit"))
        if self.mode in ("redesign", "improve") and not a.get("keep"):
            self.add("K19", "C", "minor", "audit.keep", "nothing kept from the existing product",
                     "redesigns that keep nothing lose recognition; confirm this is intended", self.line("audit"))

    def check_directions(self):
        d = self.doc.get("directions")
        if d is None:
            return
        self.checked.append("directions")
        if not isinstance(d, list):
            self.add("K05", "D", "major", "directions", "directions must be a list", "see docs/KDL.md")
            return
        if len(d) < 3:
            self.add("K05", "D", "major", "directions", f"only {len(d)} direction(s) explored",
                     "explore ≥3 genuinely different directions before converging", self.line("directions"))
        chosen = [x for x in d if isinstance(x, dict) and x.get("verdict") == "chosen"]
        if len(chosen) != 1:
            self.add("K05", "D", "major", "directions", f"{len(chosen)} directions marked chosen",
                     "mark exactly one direction `verdict: chosen`", self.line("directions"))
        for i, x in enumerate(d):
            if isinstance(x, dict) and not x.get("because"):
                self.add("K17", "D", "minor", f"directions.{i}", f"direction {x.get('id', i)} has no `because`",
                         "a rejected direction is evidence of judgment; say why", self.line(f"directions.{i}"))
        axes = [x.get("axes") for x in d if isinstance(x, dict) and isinstance(x.get("axes"), dict)]
        for i in range(len(axes)):
            for j in range(i + 1, len(axes)):
                keys = set(axes[i]) & set(axes[j])
                same = [k for k in keys if str(axes[i][k]).lower() == str(axes[j][k]).lower()]
                if keys and len(keys) - len(same) < 3:
                    self.add("K05", "D", "major", "directions",
                             f"directions {i + 1} and {j + 1} differ on fewer than 3 axes",
                             "vary structure, density, color strategy, type voice and motion — not three palettes on one layout",
                             self.line("directions"))

    # ----------------------------------------------------------- identity
    def check_identity(self):
        """v1.6 identity gate: inventory → idea → dealt engine → most distinctive viable direction → vocabulary."""
        d = self.doc.get("directions")
        if not isinstance(d, list) or self.mode not in ("create", "redesign"):
            return
        self.checked.append("identity")
        inv = self.doc.get("inventory")
        items = [str(x.get("item") if isinstance(x, dict) else x) for x in inv] if isinstance(inv, list) else []
        if not items:
            self.add("K28", "D", "major", "inventory", "no `inventory` of things only this product has",
                     "list 8–12 items of the product's own world (objects, places, rituals, printed artefacts, numbers, names) before any direction",
                     self.line("inventory"))
        elif len(items) < 8:
            self.add("K28", "D", "minor", "inventory", f"inventory has {len(items)} items",
                     "8–12 items: the identity is drawn from them, and a short list is the category's list",
                     self.line("inventory"))
        idea = self.doc.get("idea")
        if not isinstance(idea, dict):
            self.add("K28", "D", "major", "idea", "no `idea` (In this app, [inventory item] becomes [the engine's device])",
                     "write idea: {subject_item, becomes, competitor_test: {competitor, fails_because}}", self.line("idea"))
        else:
            for k in ("subject_item", "becomes"):
                if not idea.get(k):
                    self.add("K28", "D", "minor", f"idea.{k}", f"idea has no `{k}`", "complete the idea sentence",
                             self.line("idea"))
            ct = idea.get("competitor_test")
            if not isinstance(ct, dict) or not ct.get("competitor") or not ct.get("fails_because"):
                self.add("K28", "D", "minor", "idea.competitor_test",
                         "idea has no competitor test", "name the nearest competitor and why the idea fails for it — "
                         "if it fits them too, it is the category's idea, not this product's", self.line("idea"))
            subj = str(idea.get("subject_item") or "").lower()
            if subj and items and not any(subj in i.lower() or i.lower() in subj for i in items):
                self.add("K28", "D", "minor", "idea.subject_item", f"`{idea.get('subject_item')}` is not in the inventory",
                         "the idea must start from an inventory item", self.line("idea"))
        chosen = next((x for x in d if isinstance(x, dict) and x.get("verdict") == "chosen"), None)
        dealt = [o["engine"]["id"] for o in (self.deal or {}).get("options", []) if isinstance(o, dict)]
        if self.deal is None:
            self.add("K29", "I", "info", "directions", "no `.kinetic/deal.json` next to this record",
                     "run `kinetic deal --brief …` and choose among the dealt options", self.line("directions"))
        authored = [x for x in d if isinstance(x, dict) and x.get("source") == "author"]
        if len(authored) > 1:
            self.add("K29", "D", "minor", "directions", f"{len(authored)} directions marked `source: author`",
                     "one direction is yours (from the thesis); the others are the dealt challengers", self.line("directions"))
        if self.deal is not None and chosen is not None and chosen.get("source") != "author" and chosen.get("engine") not in dealt:
            self.add("K29", "D", "major", "directions", f"chosen direction's engine `{chosen.get('engine')}` was not dealt "
                     f"({', '.join(dealt)})", "choose a dealt option, or redraw its engine with "
                     "`kinetic deal --redraw N.engine --reason …`", self.line("directions"))
        for h in (self.deal or {}).get("history", []):
            if len(str(h.get("reason") or "").strip()) < 12:
                self.add("K33", "D", "major", "deal.history", f"redraw of option {h.get('option')} {h.get('slot')} has no reason",
                         "every redraw states the product fact or brand constraint that rules the dealt slot out")

        def sc(x, k):
            try:
                return float((x.get("scores") or {}).get(k))
            except (TypeError, ValueError, AttributeError):
                return None

        def viable(x):
            f, u, fe = sc(x, "product_fit"), sc(x, "usability"), sc(x, "feasibility")
            return f is not None and u is not None and fe is not None and f >= 4 and u >= 4 and fe >= 3
        if chosen is not None and sc(chosen, "distinctiveness") is not None:
            better = [x for x in d if isinstance(x, dict) and x is not chosen and viable(x)
                      and (sc(x, "distinctiveness") or 0) > (sc(chosen, "distinctiveness") or 0)]
            if better:
                self.add("K30", "D", "major", "directions",
                         f"a more distinctive viable direction ({better[0].get('id')}) was rejected for a safer one",
                         "rule: among directions with fit ≥ 4, usability ≥ 4, feasibility ≥ 3, choose the most distinctive "
                         "(write the brand/user fact that forbids it in `because` if one truly does, and lower its fit score)",
                         self.line("directions"))
        voc = self.doc.get("vocabulary")
        if not isinstance(voc, list) or not voc:
            self.add("K31", "D", "major", "vocabulary", "no drawn `vocabulary`",
                     "6–10 marks drawn from the inventory, each replacing a generic part: "
                     "[{mark, from, replaces, sites, file}]", self.line("vocabulary"))
        else:
            sites = []
            for i, m in enumerate(voc):
                if not isinstance(m, dict):
                    continue
                ss = m.get("sites") or []
                sites += [str(x).lower() for x in (ss if isinstance(ss, list) else [ss])]
                rep = m.get("replaces")
                if rep and str(rep) not in VOCAB_ROLES:
                    self.add("K31", "I", "info", f"vocabulary.{i}.replaces", f"unknown role `{rep}`",
                             f"roles: {', '.join(sorted(VOCAB_ROLES))}", self.line(f"vocabulary.{i}"))
                f = m.get("file")
                if f and self.root and not os.path.exists(os.path.join(self.root, str(f))):
                    self.add("K31", "D", "minor", f"vocabulary.{i}.file", f"mark file `{f}` not found",
                             "draw the mark as SVG (kinetic svg lint) or in code, and point `file` at it",
                             self.line(f"vocabulary.{i}"))
            if len(sites) < 4:
                self.add("K31", "D", "major", "vocabulary", f"the vocabulary appears in {len(sites)} place(s)",
                         "carry it into ≥ 4 places: the hero, a list item, a data encoding, a degraded state",
                         self.line("vocabulary"))
            if not any("hero" in x for x in sites):
                self.add("K31", "D", "minor", "vocabulary", "the vocabulary is not in the hero",
                         "the first viewport is the vocabulary's home", self.line("vocabulary"))
        c = self.doc.get("contract")
        if not isinstance(c, dict):
            self.add("K32", "D", "minor", "contract", "no direction `contract`",
                     f"≤ 200 words protecting the idea through the build: {', '.join(CONTRACT_KEYS)}", self.line("contract"))
        else:
            missing = [k for k in CONTRACT_KEYS if not c.get(k)]
            if missing:
                self.add("K32", "D", "minor", "contract", f"contract misses {', '.join(missing)}",
                         "every block in one or two sentences", self.line("contract"))
            words = sum(len(str(v).split()) for v in c.values())
            if words > 220:
                self.add("K32", "I", "info", "contract", f"contract is {words} words",
                         "≤ 200: it is read before every screen, so it must stay a contract, not a spec", self.line("contract"))

    # ------------------------------------------------------------- system
    def check_system(self, level: int):
        s = self.doc.get("system")
        if not isinstance(s, dict):
            return
        self.checked.append("system")
        budget = BUDGET.get(level, BUDGET[3])
        self._check_type(s.get("type"), budget)
        self._check_color(s.get("color"), budget)
        self._check_space(s.get("space"))
        self._check_shape(s.get("shape"))
        self._check_motion(s.get("motion"), level)
        self._check_haptics(s.get("haptics"))
        if not s.get("icon"):
            self.add("K02", "D", "minor", "system.icon", "no icon system declared",
                     "declare one family, one style, how selection is shown, sizes", self.line("system"))

    def _check_type(self, t, budget):
        if not isinstance(t, dict):
            self.add("K02", "D", "major", "system.type", "no type system", "define families and a 5–8 step ramp",
                     self.line("system"))
            return
        fams = t.get("families") or {}
        def _names(v):
            return [str(x) for x in v.values()] if isinstance(v, dict) else [str(v)]
        distinct = {n.split(" ")[0].lower() for v in fams.values() for n in _names(v)} if isinstance(fams, dict) else set()
        for st in (t.get("scale") or {}).values() if isinstance(t.get("scale"), dict) else ():
            own = st.get("family") if isinstance(st, dict) else None
            if isinstance(own, str) and isinstance(fams, dict) and own not in fams:
                distinct.add(own.split(" ")[0].lower())
        if len(distinct) > budget[1]:
            self.add("D12", "D", "minor", "system.type.families",
                     f"{len(distinct)} type families exceed the budget ({budget[1]}) for this expression level",
                     "fewer families, more contrast within one", self.line("system.type.families"))
        scale = t.get("scale")
        if not isinstance(scale, dict) or not scale:
            self.add("K07", "D", "major", "system.type.scale", "type scale missing", "define a ramp",
                     self.line("system.type"))
            return
        if len(scale) > 8:
            self.add("D12", "D", "major", "system.type.scale", f"{len(scale)} type styles (> 8)",
                     "merge styles; hierarchy comes from size+weight+color together", self.line("system.type.scale"))
        if len(scale) < 4:
            self.add("K07", "C", "minor", "system.type.scale", f"only {len(scale)} type styles",
                     "most products need 5–7 (display, title, headline, body, callout/label, caption)",
                     self.line("system.type.scale"))
        sizes = []
        for name, st in scale.items():
            ln = self.line(f"system.type.scale.{name}")
            if not isinstance(st, dict) or not isinstance(st.get("size"), (int, float)):
                self.add("K07", "D", "major", f"system.type.scale.{name}", f"style `{name}` needs a numeric size",
                         "{size, line, weight, track}", ln)
                continue
            for key in st:
                if key not in STYLE_KEYS:
                    self.add("K18", "I", "minor", f"system.type.scale.{name}.{key}",
                             f"unknown key `{key}` in style `{name}` (export ignores it)",
                             f"style keys: {', '.join(sorted(STYLE_KEYS))}", ln)
            size, line_h = st["size"], st.get("line")
            sizes.append((size, name))
            if not isinstance(line_h, (int, float)):
                self.add("K07", "D", "minor", f"system.type.scale.{name}", f"`{name}` has no line height",
                         "set line explicitly; defaults are rarely right", ln)
            else:
                ratio = line_h / size
                lo, hi = (1.0, 1.3) if size >= 28 else (1.15, 1.6)
                if str(st.get("case", "")).lower() == "upper" or "numeral" in str(st.get("use", "")).lower():
                    lo = 0.95  # caps and figures have no descenders: tight leading is correct
                if not lo <= ratio <= hi:
                    self.add("K07", "D", "minor", f"system.type.scale.{name}",
                             f"`{name}` line/size = {ratio:.2f} (expected {lo}–{hi} at {size}pt)",
                             "large type wants tight leading; small text wants air", ln)
            track = st.get("track")
            if isinstance(track, (int, float)):
                if abs(track) > 0.5:
                    self.add("K07", "D", "major", f"system.type.scale.{name}",
                             f"`{name}` track {track} looks like points, not em", "track is in em (e.g. -0.02)", ln)
                elif size >= 28 and track > 0.005:
                    self.add("K07", "C", "minor", f"system.type.scale.{name}",
                             f"positive tracking on {size}pt display text", "large sizes usually want 0 to -0.03em", ln)
                elif size <= 12 and track < 0:
                    self.add("K07", "D", "minor", f"system.type.scale.{name}",
                             f"negative tracking on {size}pt text hurts legibility", "small sizes want 0 to +0.02em", ln)
            w = st.get("weight")
            if isinstance(w, int) and not (100 <= w <= 900 and w % 100 == 0):
                self.add("K07", "D", "minor", f"system.type.scale.{name}", f"weight {w} is not a CSS weight",
                         "use 100–900 in steps of 100", ln)
        if sizes:
            body = [s for s, n in sizes if n in ("body", "body-l", "body-m", "text")]
            if body and min(body) < 15:
                self.add("F03", "D", "major", "system.type.scale.body",
                         f"body size {min(body)}pt is below the mobile reading floor",
                         "iOS body is 17pt, Material body large is 16sp; go below 15 only for dense pro tools",
                         self.line("system.type.scale"))
            if min(s for s, _ in sizes) < 11:
                self.add("F03", "F", "block", "system.type.scale", "a type style is below 11pt",
                         "nothing readable goes under 11pt", self.line("system.type.scale"))
            mx = max(s for s, _ in sizes)
            if mx > budget[3]:
                self.add("K07", "C", "minor", "system.type.scale",
                         f"display {mx}pt exceeds the {budget[3]}pt guide for this expression level",
                         "a giant headline as the only idea is a costume; justify it in `because` or scale down",
                         self.line("system.type.scale"))
            uniq = sorted({s for s, _ in sizes})
            for a, b in zip(uniq, uniq[1:]):
                if b - a < 1:
                    self.add("D12", "D", "minor", "system.type.scale", f"sizes {a} and {b} are indistinguishable",
                             "merge them or separate by ≥2pt and weight", self.line("system.type.scale"))

    def _check_color(self, c, budget):
        if not isinstance(c, dict):
            self.add("K08", "D", "major", "system.color", "no color system", "define roles for light and dark",
                     self.line("system"))
            return
        roles = c.get("roles")
        if not isinstance(roles, dict):
            self.add("K08", "D", "major", "system.color.roles", "color roles missing",
                     "use `kinetic palette <seed>` to derive light/dark roles", self.line("system.color"))
            return
        if "dark" not in roles:
            self.add("K09", "D", "major", "system.color.roles.dark", "no dark theme",
                     "design dark mode (lifted tonal surfaces, desaturated accent) — don't invert",
                     self.line("system.color.roles"))
        for theme in ("light", "dark"):
            r = roles.get(theme)
            if not isinstance(r, dict):
                continue
            for role in REQUIRED_ROLES:
                if role not in r:
                    self.add("K08", "D", "major", f"system.color.roles.{theme}.{role}",
                             f"{theme} theme is missing role `{role}`", "define every required role",
                             self.line(f"system.color.roles.{theme}"))
            for role, v in r.items():
                if not color.is_hex(str(v)):
                    self.add("K08", "D", "major", f"system.color.roles.{theme}.{role}",
                             f"{theme}.{role} = {v!r} is not a hex color", "write #RRGGBB",
                             self.line(f"system.color.roles.{theme}.{role}"))
            accents = set()
            for role, v in r.items():
                # a palette's colour field and its state fields are proportion, not accents (knowledge/library/palettes.json)
                if _is_status_role(role) or not color.is_hex(str(v)) or re.match(r"^(on-)?(field|state-[\w-]+)$", role):
                    continue
                L, C, H = color.hex_to_oklch(str(v))
                if C >= 0.06:
                    accents.add(color.hue_family(H, C))
            if len(accents) > budget[0]:
                self.add("D13", "D", "major", f"system.color.roles.{theme}",
                         f"{len(accents)} saturated hue families ({', '.join(sorted(accents))}) exceed the budget ({budget[0]})",
                         "one accent carries meaning; the rest are tinted neutrals",
                         self.line(f"system.color.roles.{theme}"))
            neutrals = [str(r[k]) for k in ("bg", "surface", "text-2", "border") if color.is_hex(str(r.get(k)))]
            if neutrals and all(color.hex_to_oklch(v)[1] < 0.004 for v in neutrals):
                self.add("K23", "C", "minor", f"system.color.roles.{theme}",
                         f"{theme} neutrals are untinted greys",
                         "tint neutrals toward the seed (OKLCH C ≈ 0.005–0.02): the cheapest way to stop looking default (color.md §3)",
                         self.line(f"system.color.roles.{theme}"))
            acc, txt = str(r.get("accent", "")), str(r.get("text", ""))
            if theme == "light" and color.is_hex(acc) and (acc.upper() == txt.upper() or color.hex_to_oklch(acc)[1] < 0.03) \
                    and "monochrome" not in str(_get(self.doc, "system.color.strategy") or ""):
                self.add("K24", "C", "minor", f"system.color.roles.{theme}.accent",
                         "the accent is achromatic (same as text): nothing signals 'act here' by color",
                         "give interactive elements one meaningful accent, or declare `strategy: monochrome` and carry affordance with shape and weight",
                         self.line(f"system.color.roles.{theme}.accent"))
            if theme == "light" and str(r.get("bg", "")).upper() in ("#FFFFFF", "#FFF"):
                self.add("K23", "C", "info", f"system.color.roles.{theme}.bg",
                         "pure white canvas", "an off-white tinted bg (L 0.97–0.99) lets white surfaces lift without shadows (color.md §6)",
                         self.line(f"system.color.roles.{theme}.bg"))
            bg = r.get("bg")
            if theme == "dark" and color.is_hex(str(bg)) and color.parse_hex(str(bg))[:3] == (0, 0, 0):
                self.add("C02", "C", "info", "system.color.roles.dark.bg", "pure black dark background",
                         "right for OLED media/night apps; otherwise use near-black with tonal surfaces",
                         self.line("system.color.roles.dark.bg"))
            for v in r.values():
                if color.is_hex(str(v)) and color.is_ai_purple(str(v)) and _get(self.doc, "product.brand.status") != "strict":
                    self.add("D01", "C", "minor", f"system.color.roles.{theme}",
                             f"{v} sits in the violet/indigo 'AI default' family",
                             "keep it only if it comes from the brand or the thesis; say so in `because`",
                             self.line(f"system.color.roles.{theme}"))
                    break
        self._check_data_colors(c.get("data"), roles)
        for rep in color.check_roles({k: v for k, v in roles.items() if isinstance(v, dict)}):
            if not rep["ok"]:
                self.add("F03", "F", "block", f"system.color.roles.{rep['theme']}",
                         f"{rep['theme']} {rep['pair']} contrast {rep['wcag']}:1 < {rep['minimum']}:1 (APCA Lc {rep['apca_lc']})",
                         "adjust lightness of the foreground role; `kinetic contrast` shows passing values",
                         self.line(f"system.color.roles.{rep['theme']}"))
        self.contrast = color.check_roles({k: v for k, v in roles.items() if isinstance(v, dict)})

    def _check_data_colors(self, data, roles):
        """Data colors (transit lines, categories): text on them must pass; they must not mimic danger."""
        if not isinstance(data, dict):
            return
        # compare each data fill with the danger of its own theme (light fills vs light danger, dark vs dark)
        danger_by = {t: str(r.get("danger")) for t, r in roles.items() if isinstance(r, dict) and color.is_hex(str(r.get("danger")))}
        for name, v in data.items():
            path = f"system.color.data.{name}"
            entries = []
            if color.is_hex(str(v)):
                entries.append(("fill", str(v), None))
            elif isinstance(v, dict):
                for fk, ok in (("fill", "on"), ("light", "on"), ("fill_dark", "on_dark"), ("dark", "on_dark")):
                    if color.is_hex(str(v.get(fk))):
                        entries.append((fk, str(v[fk]), str(v.get(ok)) if color.is_hex(str(v.get(ok))) else None))
            else:
                self.add("K08", "D", "minor", path, f"data color `{name}` must be a hex or {{fill, on}}",
                         "{fill: \"#2E7D4F\", on: \"#FFFFFF\"}", self.line(path))
                continue
            graphic = isinstance(v, dict) and (v.get("graphic") is True or v.get("label") is False)
            for fk, fill, on in entries:
                if graphic:
                    for theme, r in roles.items():
                        bgv = r.get("bg") if isinstance(r, dict) else None
                        if color.is_hex(str(bgv)) and (("dark" in fk) == (theme == "dark")) and color.wcag(fill, bgv) < 3.0:
                            self.add("F03", "D", "major", path,
                                     f"graphic data color `{name}` {fill} is {color.wcag(fill, bgv):.2f}:1 on {theme} bg (< 3:1)",
                                     "meaningful graphics need 3:1 against their background", self.line(path))
                    continue
                if on:
                    ratio = color.wcag(on, fill)
                    if ratio < 4.5:
                        self.add("F03", "F", "block", path, f"`{name}` text {on} on {fill} = {ratio:.2f}:1 < 4.5:1",
                                 "pick the passing text color (white or near-black) or adjust the fill", self.line(path))
                else:
                    best = max(("#FFFFFF", "#111111"), key=lambda t: color.wcag(t, fill))
                    if color.wcag(best, fill) < 4.5:
                        self.add("F03", "D", "major", path,
                                 f"no readable label color on `{name}` {fill} (best {best} = {color.wcag(best, fill):.2f}:1)",
                                 "badge text needs 4.5:1: adjust the fill or enlarge the label to ≥ 3:1 large-text use", self.line(path))
                    else:
                        self.add("K25", "I", "info", path, f"`{name}` has no `on` color; {best} passes ({color.wcag(best, fill):.1f}:1)",
                                 f"declare `on: \"{best}\"` so the export carries it", self.line(path))
                theme = "dark" if fk in ("fill_dark", "dark") else "light"
                for d in ([danger_by[theme]] if theme in danger_by else list(danger_by.values())):
                    if color.delta_e_ok(fill, d) < 0.08:
                        self.add("K26", "C", "minor", path, f"data color `{name}` {fill} is close to danger {d}",
                                 "pair status with icon + word, or move the danger hue away from the data palette (color.md §8b)",
                                 self.line(path))
                        break

    def _check_space(self, sp):
        if not isinstance(sp, dict):
            self.add("K10", "D", "major", "system.space", "no spacing system", "unit 4 and a named scale",
                     self.line("system"))
            return
        unit = sp.get("unit", 4)
        scale = sp.get("scale") or {}
        vals = scale.values() if isinstance(scale, dict) else scale
        for v in vals:
            if isinstance(v, (int, float)) and v > 2 and v % unit:
                self.add("D17", "D", "major", "system.space.scale", f"spacing {v} is off the {unit}pt grid",
                         f"use multiples of {unit}", self.line("system.space.scale"))
        if isinstance(scale, dict) and len(scale) > 10:
            self.add("D17", "D", "minor", "system.space.scale", f"{len(scale)} spacing steps",
                     "6–9 steps are enough; more steps means arbitrary choices", self.line("system.space.scale"))
        m = sp.get("margins")
        if isinstance(m, dict):
            for k, v in m.items():
                if isinstance(v, (int, float)) and v % unit:
                    self.add("D17", "D", "minor", f"system.space.margins.{k}", f"margin {v} is off-grid",
                             f"use a multiple of {unit} (16, 20, 24)", self.line("system.space.margins"))

    def _check_shape(self, sh):
        if not isinstance(sh, dict):
            return
        r = sh.get("radius")
        if isinstance(r, dict):
            real = {v for v in r.values() if isinstance(v, (int, float)) and 0 < v < 500}
            if len(real) > 4:
                self.add("D15", "D", "major", "system.shape.radius", f"{len(real)} radii",
                         "3–4 radii plus `full`; nested corners follow inner = outer − padding",
                         self.line("system.shape.radius"))
        if _get(self.doc, "product.platforms") and "ios" in (_get(self.doc, "product.platforms") or []) \
                and sh.get("corner") == "circular":
            self.add("D24", "C", "info", "system.shape.corner", "circular corners on iOS",
                     "iOS uses continuous (squircle) corners; circular reads slightly off-native",
                     self.line("system.shape.corner"))

    def _check_motion(self, m, level):
        if not isinstance(m, dict):
            self.add("K13", "D", "major", "system.motion", "no motion system",
                     "personality, springs, durations, reduce-motion behaviour", self.line("system"))
            return
        if not m.get("reduce"):
            self.add("F08", "F", "block", "system.motion.reduce", "no reduce-motion behaviour declared",
                     "crossfade | instant | keep-feedback-only", self.line("system.motion"))
        if not m.get("personality"):
            self.add("K13", "C", "minor", "system.motion.personality", "motion personality not named",
                     "name it (e.g. 'unhurried, damped, never bouncy') so every animation can be checked against it",
                     self.line("system.motion"))
        springs = m.get("springs") or {}
        if isinstance(springs, dict):
            for name, sp in springs.items():
                ln = self.line(f"system.motion.springs.{name}")
                if not isinstance(sp, dict):
                    continue
                resp, damp = sp.get("response"), sp.get("damping")
                if not isinstance(resp, (int, float)) or not isinstance(damp, (int, float)):
                    self.add("K14", "D", "major", f"system.motion.springs.{name}",
                             f"spring `{name}` needs numeric response (s) and damping (ratio)",
                             "e.g. {response: 0.35, damping: 0.85}", ln)
                    continue
                if not 0.12 <= resp <= 1.5:
                    self.add("K14", "D", "minor", f"system.motion.springs.{name}",
                             f"response {resp}s is outside 0.12–1.5", "UI springs live in 0.2–0.6s", ln)
                if damp < 0.5:
                    self.add("D19", "D", "major", f"system.motion.springs.{name}",
                             f"damping {damp} oscillates visibly", "≥0.7 for UI, 0.5–0.7 only for playful direct manipulation", ln)
                elif damp < 0.7 and level <= 3:
                    self.add("D19", "D", "minor", f"system.motion.springs.{name}",
                             f"bouncy spring (damping {damp}) at expression level {level}",
                             "reserve overshoot for direct manipulation or expression ≥4", ln)
        durs = m.get("durations") or {}
        if isinstance(durs, dict):
            for name, ms in durs.items():
                hi = 8000 if LONG_DURATION.search(str(name)) else 1200  # ambient loops breathe slowly
                if isinstance(ms, (int, float)) and (ms < 60 or ms > hi):
                    self.add("K14", "D", "minor", f"system.motion.durations.{name}",
                             f"duration {ms}ms outside 60–{hi}",
                             "durations are in ms; name ambient loops `ambient-…`/`pulse-…` (≤ 8 s, still under reduce motion)",
                             self.line("system.motion.durations"))

    def _check_haptics(self, h):
        if not isinstance(h, dict):
            return
        for k, v in h.items():
            if str(v) not in HAPTICS:
                self.add("K18", "I", "minor", f"system.haptics.{k}", f"unknown haptic {v!r}",
                         f"use one of: {', '.join(sorted(HAPTICS))}", self.line(f"system.haptics.{k}"))

    # ------------------------------------------------------------ screens
    def check_screens(self, level):
        screens = self.doc.get("screens")
        if not isinstance(screens, list):
            return
        self.checked.append("screens")
        roles = _get(self.doc, "system.color.roles") or {}
        motion_moments = 0
        for i, sc in enumerate(screens):
            if not isinstance(sc, dict):
                continue
            sid = sc.get("id", f"#{i}")
            base = f"screens.{i}"
            ln = self.line(base)
            for k in ("job", "primary"):
                if not sc.get(k):
                    self.add("K02", "D", "major", f"{base}.{k}", f"screen `{sid}` has no `{k}`",
                             "name the one job and the one primary element before styling", ln)
            states = sc.get("states")
            needed = list(SCREEN_STATES) + (["offline"] if sc.get("network") else [])
            if not isinstance(states, dict):
                self.add("F06", "F", "block", f"{base}.states", f"screen `{sid}` declares no states",
                         f"describe {', '.join(needed)} (or `n/a: reason`)", ln)
            else:
                for st in needed:
                    if st not in states or states[st] in (None, ""):
                        self.add("F06", "F" if st in ("error", "empty") else "D",
                                 "block" if st in ("error", "empty") else "major",
                                 f"{base}.states.{st}", f"screen `{sid}` is missing the `{st}` state",
                                 "design it, or write `n/a: <reason>`", self.line(f"{base}.states"))
                    elif _is_na(states[st]) and len(str(states[st])) < 8:
                        self.add("K11", "D", "minor", f"{base}.states.{st}",
                                 f"`{st}` marked n/a without a reason", "say why it cannot happen",
                                 self.line(f"{base}.states.{st}"))
            comps = sc.get("components") or []
            for j, cp in enumerate(comps if isinstance(comps, list) else []):
                if not isinstance(cp, dict):
                    continue
                cbase = f"{base}.components.{j}"
                cln = self.line(cbase)
                kind = cp.get("kind")
                cid = cp.get("id", f"#{j}")
                if kind and kind not in KINDS:
                    self.add("K18", "I", "minor", f"{cbase}.kind", f"unknown component kind {kind!r}",
                             "see component kinds in docs/KDL.md", cln)
                if kind in INTERACTIVE:
                    variants = cp.get("variants") or []
                    # a map may waive one with a reason: {pressed: …, disabled: "n/a: logging is local, never blocked"}
                    if isinstance(variants, dict):
                        for v, why in variants.items():
                            if str(why).lower().startswith("n/a") and len(str(why).split()) < 3:
                                self.add("K02", "D", "minor", f"{cbase}.variants.{v}",
                                         f"`{sid}/{cid}` waives `{v}` without a reason", "n/a: why it cannot happen", cln)
                    missing = [v for v in ("pressed", "disabled") if v not in variants]
                    if missing:
                        self.add("K12", "D", "major", f"{cbase}.variants",
                                 f"`{sid}/{cid}` lacks variants: {', '.join(missing)}",
                                 "design pressed and disabled (and loading for async actions)", cln)
                    tgt = cp.get("target")
                    if tgt is None:
                        self.add("F05", "D", "minor", f"{cbase}.target", f"`{sid}/{cid}` has no declared touch target",
                                 "declare target ≥ 44 (iOS) / 48 (Android)", cln)
                    elif isinstance(tgt, (int, float)) and tgt < 44:
                        self.add("F05", "F", "block", f"{cbase}.target", f"`{sid}/{cid}` target {tgt} < 44",
                                 "expand the hit area; the glyph can stay small", cln)
                fg, bg = cp.get("fg"), cp.get("bg")
                if isinstance(fg, str) and fg.strip() == "$color.text-3" and kind in ("text", "numeral", "label", None) \
                        and not cp.get("decorative"):
                    self.add("K27", "D", "minor", f"{cbase}.fg", f"`{sid}/{cid}` uses tertiary text for content",
                             "text-3 is for placeholders/disabled/decoration only; information needs text or text-2 (4.5:1)", cln)
                if isinstance(fg, str) and isinstance(bg, str) and isinstance(roles, dict):
                    for theme, r in roles.items():
                        if not isinstance(r, dict):
                            continue
                        f_hex, b_hex = self._resolve_color(fg, r), self._resolve_color(bg, r)
                        if f_hex and b_hex:
                            ratio = color.wcag(f_hex, b_hex)
                            size = self._comp_size(cp)
                            minimum = 3.0 if size and size >= 24 else 4.5
                            if kind in ("icon", "icon-button", "progress", "divider"):
                                minimum = 3.0
                            if ratio < minimum:
                                self.add("F03", "F", "block", cbase,
                                         f"`{sid}/{cid}` {theme}: {fg} on {bg} = {ratio:.2f}:1 < {minimum}:1",
                                         "use a role pair that passes, or change the role", cln)
            mot = sc.get("motion") or []
            for k, mv in enumerate(mot if isinstance(mot, list) else []):
                if not isinstance(mv, dict):
                    continue
                mkind = mv.get("kind", "transition")
                if mkind not in MOTION_KINDS:
                    self.add("K18", "I", "minor", f"{base}.motion.{k}.kind", f"unknown motion kind {mkind!r}",
                             " | ".join(MOTION_KINDS), self.line(f"{base}.motion.{k}"))
                if mkind == "signature":
                    motion_moments += 1
                mbase = f"{base}.motion.{k}"
                for f in ("trigger", "change", "reduce"):
                    if not mv.get(f):
                        self.add("F08" if f == "reduce" else "K13", "F" if f == "reduce" else "D",
                                 "block" if f == "reduce" else "major", f"{mbase}.{f}",
                                 f"motion `{mv.get('id', k)}` on `{sid}` lacks `{f}`",
                                 "every animation: trigger, what changes, physics, reduce-motion path",
                                 self.line(mbase))
                if not mv.get("spring") and not mv.get("duration"):
                    self.add("K13", "D", "major", f"{mbase}", f"motion `{mv.get('id', k)}` has no spring or duration",
                             "reference a system spring ($spring.x) or duration", self.line(mbase))
        budget = BUDGET.get(level, BUDGET[3])[2]
        if motion_moments > budget:
            self.add("D18", "D", "minor", "screens",
                     f"{motion_moments} signature motion moments exceed the budget ({budget}) for expression {level}",
                     "keep signature motion for the moments that carry the spine; feedback and transitions don't count",
                     self.line("screens"))

    def _resolve_color(self, ref: str, theme_roles: dict):
        m = REF.fullmatch(ref.strip())
        if m and m.group(1) == "data":
            v = (_get(self.doc, "system.color.data") or {}).get(m.group(2))
            v = v.get("fill") if isinstance(v, dict) else v
            return v if color.is_hex(str(v)) else None
        if m and m.group(1) == "color":
            v = theme_roles.get(m.group(2))
            return v if color.is_hex(str(v)) else None
        return ref if color.is_hex(ref) else None

    def _comp_size(self, cp):
        t = cp.get("type")
        if isinstance(t, str):
            m = REF.fullmatch(t.strip())
            if m and m.group(1) == "type":
                st = _get(self.doc, f"system.type.scale.{m.group(2)}")
                if isinstance(st, dict):
                    return st.get("size")
        return None

    # --------------------------------------------------------- references
    def check_refs(self):
        def walk(node, path):
            if isinstance(node, dict):
                for k, v in node.items():
                    yield from walk(v, f"{path}.{k}" if path else str(k))
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    yield from walk(v, f"{path}.{i}")
            elif isinstance(node, str):
                yield path, node

        for path, value in walk(self.doc, ""):
            if value.strip().upper().startswith("TODO"):
                self.add("K02", "D", "major", path, f"`{path}` is still a TODO",
                         "make the decision (or remove the field if it does not apply)", self.line(path))
                continue
            for m in REF.finditer(value):
                group, name = m.group(1), m.group(2)
                targets = REF_TARGETS.get(group)
                if not targets:
                    self.add("K03", "D", "minor", path, f"unknown token group `${group}`",
                             f"groups: {', '.join('$' + g for g in REF_TARGETS)}", self.line(path))
                    continue
                existing = [t for t in targets if isinstance(_get(self.doc, t), dict)] or targets[:1]
                for t in existing:
                    node = _get(self.doc, t)
                    if not isinstance(node, dict) or name not in node:
                        self.add("K03", "D", "major", path, f"`${group}.{name}` does not resolve in `{t}`",
                                 "define the token or fix the reference", self.line(path))
                        break
            for pat in SLOP_PHRASES:
                if re.search(pat, value, re.I):
                    self.add("D22", "D", "minor", path, f"copy slop in `{path}`: {value[:60]!r}",
                             "name the concrete thing and outcome (knowledge/copy.md)", self.line(path))
                    break

    def check_requirements(self):
        """Brief coverage: every `must` requirement is served by a screen, above the fold when asked."""
        reqs = self.doc.get("requirements")
        if reqs is None:
            return  # K01 already reports it for create/redesign
        self.checked.append("requirements")
        served = {}
        for i, sc in enumerate(self.doc.get("screens") or []):
            if isinstance(sc, dict):
                for rid in sc.get("serves") or []:
                    served.setdefault(str(rid), []).append((sc.get("id", f"#{i}"), sc))
                if not sc.get("thumb") and not sc.get("modal"):
                    self.add("K22", "D", "minor", f"screens.{i}.thumb",
                             f"screen `{sc.get('id', i)}` declares nothing in the thumb zone",
                             "list the actions/navigation reachable in the bottom third (search, primary action, tabs)",
                             self.line(f"screens.{i}"))
        for j, r in enumerate(reqs if isinstance(reqs, list) else []):
            if not isinstance(r, dict):
                continue
            rid, prio = str(r.get("id", j)), r.get("priority", "must")
            if prio == "must" and rid not in served:
                self.add("K21", "D", "major", f"requirements.{j}",
                         f"must-have `{rid}` ({str(r.get('need', ''))[:60]}) is served by no screen",
                         "add it to a screen's `serves`, or argue in `because` why the brief is wrong",
                         self.line(f"requirements.{j}"))
            if r.get("above_fold") and rid in served:
                for sid, sc in served[rid]:
                    order = [str(x) for x in (sc.get("reading_order") or [])]
                    where = str(r.get("element", ""))
                    # a nested element takes the position of the block it sits `in:` (pickup-row in now-card)
                    parents = {str(c.get("id")): str(c.get("in")) for c in (sc.get("components") or [])
                               if isinstance(c, dict) and c.get("in")}
                    seen = set()
                    while where and where not in order and where in parents and where not in seen:
                        seen.add(where)
                        where = parents[where]
                    pinned = {str(c.get("id")) for c in (sc.get("components") or [])
                              if isinstance(c, dict) and c.get("pinned")}
                    if where in pinned:  # a pinned bar/CTA is in every viewport whatever its reading position
                        continue
                    if where and where not in order:
                        self.add("K21", "I", "info", f"requirements.{j}",
                                 f"`{rid}` must be above the fold, but `{where}` is not in `{sid}` reading_order: position unknown",
                                 "list it in reading_order, or set `in: <block>` on its component", self.line(f"requirements.{j}"))
                    elif where and order.index(where) > 3:
                        self.add("K21", "D", "minor", f"requirements.{j}",
                                 f"`{rid}` must be above the fold but `{where}` is #{order.index(where) + 1} in `{sid}` reading order",
                                 "move it up or make its first instance compact", self.line(f"requirements.{j}"))

    def check_signature(self):
        sig = self.doc.get("signature")
        if sig is None:
            return
        self.checked.append("signature")
        if not isinstance(sig, dict) or not sig.get("what") or not sig.get("because"):
            self.add("K15", "D", "minor", "signature", "signature needs `what` and `because`",
                     "one memorable detail derived from the spine", self.line("signature"))

    def check_premortem(self):
        pm = self.doc.get("premortem")
        if pm is None:
            return
        self.checked.append("premortem")
        if not isinstance(pm, list) or not pm:
            self.add("K16", "D", "major", "premortem", "premortem is empty",
                     "list where this design could fail or read as slop, with the fix", self.line("premortem"))
            return
        for i, r in enumerate(pm):
            if isinstance(r, dict) and not r.get("fix"):
                self.add("K16", "D", "minor", f"premortem.{i}", "risk without a fix", "add `fix`",
                         self.line(f"premortem.{i}"))


def _waive(findings, exceptions):
    """KDL `exceptions` with `where` matching a finding's KDL path (or no `where`) accept a D/C finding of that rule;
    F findings and the exception checks themselves are never waived."""
    ex = [e for e in (exceptions or []) if isinstance(e, dict) and e.get("rule")
          and len(str(e.get("reason") or "").split()) >= 4]
    keep, waived = [], []
    for f in findings:
        hit = next((e for e in ex if str(e["rule"]).upper() == f.rule and f.tier != "F" and f.rule not in ("K08", "K02")
                    and (not e.get("where") or str(e["where"]) in (f.path or "") or (f.path or "") in str(e["where"]))), None)
        if hit:
            waived.append({"rule": f.rule, "path": f.path, "message": f.message, "reason": str(hit.get("reason"))})
        else:
            keep.append(f)
    return keep, waived


def validate_text(text: str, path="design.kdl", deal=None, root=None) -> dict:
    try:
        doc = parse(text)
    except KDLError as e:
        f = Finding(rule="K00", tier="F", severity="block", file=path, line=e.line, path="",
                    evidence="observed", message=f"syntax: {e.message}", fix="fix the KDL syntax (docs/KDL.md)")
        return {"tool": "validate", "ok": False, "mode": None, "findings": [f.as_dict()],
                "coverage": {"sections_checked": []}}
    v = Validator(doc, path, deal, root).run()
    fs, waived = _waive(v.findings, doc.get("exceptions") if isinstance(doc, dict) else None)
    fs = sorted(fs, key=lambda f: (f.order(), f.line))
    return {
        "tool": "validate",
        "ok": not any(f.tier == "F" for f in fs),
        "mode": getattr(v, "mode", None),
        "findings": [f.as_dict() for f in fs],
        "contrast": getattr(v, "contrast", []),
        "coverage": {"sections_checked": v.checked,
                     "contrast_pairs": len(getattr(v, "contrast", [])),
                     "data_colors": len(((doc.get("system") or {}).get("color") or {}).get("data") or {})
                     if isinstance(doc, dict) else 0,
                     "screens": len(doc.get("screens") or []) if isinstance(doc, dict) else 0,
                     "sections_absent": [s for s in REQUIRED.get(getattr(v, "mode", "create"), [])
                                         if s not in (doc or {})]},
        "waived": waived,
        "limitations": ["checks decisions written in KDL; it cannot see the render or the code"],
    }


def validate_file(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    kdir = os.path.dirname(os.path.abspath(path))
    deal, dpath = None, os.path.join(kdir, "deal.json")
    if os.path.exists(dpath):
        try:
            with open(dpath, encoding="utf-8") as fh:
                deal = json.load(fh)
        except (OSError, ValueError):
            deal = None
    root = os.path.dirname(kdir) if os.path.basename(kdir) == ".kinetic" else kdir
    return validate_text(text, path, deal, root)
