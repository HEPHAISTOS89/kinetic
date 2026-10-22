# Kinetic

**Un studio de design mobile pour l'agent** : Flutter, SwiftUI, Jetpack Compose,
React Native. Kinetic fait penser le modèle comme une équipe de design
(directeurs, rival, éditeur, critiques à l'aveugle), décide par écrit, construit
chaque état, puis **prouve** le résultat avec un moteur déterministe.

> Penser comme un design lead, livrer comme un ingénieur.

---

## Installer (2 minutes)

Prérequis : Claude Code, Python 3.9+ (aucune dépendance), un accès au repo GitHub.

```bash
claude plugin marketplace add HEPHAISTOS89/kinetic
```
```bash
claude plugin install kinetic@kinetic-local
```

Installation testée le 21 octobre 2026 avec Claude Code 2.1.307 : le plugin
apparaît activé (`claude plugin list`). Pour travailler sur le code, clone le
repo (`git clone https://github.com/HEPHAISTOS89/kinetic.git`).

Vérifier que tout fonctionne :

```bash
python3 -m unittest discover -s tests   # depuis le dossier cloné
```

Codex : le manifeste `.codex-plugin/plugin.json` expose les mêmes skills.

## Utiliser

Demande simplement, en langage naturel :

> « Redesign l'écran d'accueil de mon app Flutter, elle fait générique. »

Ou choisis un mode :

| Commande | Pour |
|---|---|
| `/kinetic:studio <quoi>` | **le meilleur résultat** : l'équipe complète d'agents (recommandé) |
| `/kinetic:create` | concevoir une app, un parcours ou un écran |
| `/kinetic:redesign` | refaire une app existante en gardant ce qui marche |
| `/kinetic:improve` | améliorer sans tout changer |
| `/kinetic:audit` | diagnostic chiffré, sans modifier le code |
| `/kinetic:system` | design system : tokens, rôles couleur, typo, motion |
| `/kinetic:build` | implémenter un design décidé |
| `/kinetic:read` | lire une app existante et en extraire son vrai système |
| `/kinetic:evolve` | faire évoluer un design system en place |

Tout est consigné dans `.kinetic/` à la racine du projet : le dossier de
décisions (`design.kdl`), le tirage des directions, le travail du studio par
boucle, et le verdict des critiques.

## Comment ça marche

```
brief ─► comprendre ─► diverger ─► choisir ─► construire ─► nettoyer ─► juger ─► prouver
         (thèse,       (3 directeurs  (le plus     (états,      (éditeur,   (3 critiques   (moteur :
          inventaire)   en parallèle   distinctif   système,     budgets     à l'aveugle,   score + verdict)
                        + un rival)    viable)      contrats)    de clarté)  médiane)
```

1. **Comprendre** : produit, moments d'usage, thèse, inventaire des choses que
   seul ce produit possède.
2. **Diverger** : une direction écrite par le lead, plus deux directions
   **tirées au sort** dans une bibliothèque native (21 compositions,
   20 typographies, 30 palettes, 8 personnalités de mouvement). C'est ce qui
   empêche le design « moyen ». Un **rival** dessine le standard de la
   catégorie à battre.
3. **Choisir** : la direction la plus distinctive qui reste viable, avec son
   **vocabulaire dessiné** (les objets du domaine remplacent les pièces
   génériques).
4. **Construire** : chaque écran × chaque état (vide, erreur, hors-ligne,
   grand texte, nuit, Android et iOS), avec des **contrats de composants** qui
   fixent le comportement sans jamais imposer d'apparence.
5. **Nettoyer** : un éditeur coupe le superflu. Le moteur mesure l'encombrement
   directement sur les rendus (mots, tailles, vides, zones bruyantes).
6. **Juger** : trois critiques à l'aveugle, chacun avec son angle (produit,
   identité, clarté et finition). Leurs notes sont fusionnées par médiane.
   Jusqu'à 3 boucles.
7. **Prouver** : `kinetic score` combine le mesuré et le jugé, puis rend un
   verdict (`ship` ou `iterate`).

## Ce qu'il y a dedans

```
kinetic/
├── skills/        10 skills : routeur, think, direct, states, system, craft,
│                  motion, code, critique, studio (l'équipe multi-agents)
├── agents/        5 agents : director, rival, editor, critic, forensics
├── commands/      9 commandes /kinetic:*
├── knowledge/     ~3 600 lignes de savoir concret : couleur (OKLCH, chaleur,
│                  nuit), typographie, mise en page, clarté, contrats de
│                  composants, états, mouvement, iOS, Android, copy, anti-slop
│                  (catalogue F/D/C), priors, 5 stacks, et la bibliothèque de
│                  directions (library/*.json)
├── engine/ + bin/kinetic   moteur Python sans dépendance
├── hooks/         lint de design après chaque modification UI (actif seulement
│                  dans les projets qui ont un dossier .kinetic/)
├── docs/          ARCHITECTURE · KDL · PROTOCOL · TOOLS · EVALUATION
├── examples/lune/ un dossier de décisions KDL complet de référence
├── evals/         11 rounds de tests à l'aveugle : briefs, résultats, retours
└── tests/         79 tests (dont la compilation réelle des exports)
```

### Le moteur

```bash
bin/kinetic init .                                 # crée .kinetic/ et détecte la stack
bin/kinetic deal --brief-file BRIEF.md --options 2 # tire 2 directions adaptées au ton du brief
bin/kinetic validate .kinetic/design.kdl           # complétude, contrastes, rampe, chaleur, nuit…
bin/kinetic palette "#7A2430" --kdl                # rôles clair/sombre en OKLCH, contrastes vérifiés
bin/kinetic scan lib/                              # slop et défauts dans le code, fichier:ligne
bin/kinetic clarity shots/                         # encombrement mesuré sur les rendus PNG
bin/kinetic sheet shots/                           # planche contact de tous les états
bin/kinetic panel loop3/critic-*.json --renders shots   # fusionne 3 critiques (médiane, désaccords)
bin/kinetic export .kinetic/design.kdl --stack flutter --out lib/design/
bin/kinetic score --kdl .kinetic/design.kdl --code lib --renders shots --judged .kinetic/critique.json
```

Chaque résultat distingue ce qui est **observé**, **dérivé** et **inféré**.
Une zone non scannée est « inconnue », jamais « propre ».
Contrats des outils : [docs/TOOLS.md](docs/TOOLS.md). Le langage de
décision : [docs/KDL.md](docs/KDL.md).

## Résultats : 11 rounds à l'aveugle

Protocole : même brief inédit pour chaque bras. Les rendus sont anonymisés
(X/Y/Z), puis jugés par trois critiques indépendants qui ne savent pas qui a
fait quoi. Notes sur 9 dimensions, de 1 à 5.

| Round | Contre | Kinetic | Adversaire(s) | 1er dans |
|---|---|---|---|---|
| 8 | taste-skill, impeccable | **4.31** | 3.98 · 3.41 | 5 / 6 lectures |
| 9 | native-polish, frontend-design, modèle seul | **4.41** | 3.81 · 3.69 · 3.48 | 6 / 6 |
| 10 | taste-skill, ui-ux-pro-max | **4.31** | 3.91 · 3.35 | 5 / 6 |
| 11 | taste-skill, ui-ux-pro-max | **4.15** | 3.93 · 3.20 | 4 / 6 |

Points forts constants de Kinetic :
- l'adéquation au produit ;
- l'anticipation des états (souvent 5/5) ;
- le texte ;
- la fidélité native (variantes Android et iOS) ;
- un mode sombre vraiment conçu.

Ce qui reste à gagner :
- la **propreté** face à taste-skill (3,3 à 3,7 contre 4) ;
- la finition de la mise en page près de la barre d'action.

La v2.2 cible ces deux points (contrats de composants, règle « aucun ornement
sans fonction ») ; le round 12 la mesure en A/B. Le détail honnête de chaque
round, biais compris, est dans [docs/EVALUATION.md](docs/EVALUATION.md).

## Limites assumées

- Le scan est lexical (sans AST) : ses findings `inferred` sont des hypothèses
  à vérifier sur le rendu.
- La mesure de clarté est une heuristique sur les pixels, pas de l'OCR.
- La motion n'a jamais été jugée par les critiques : ils ne voient que des
  rendus fixes.
- L'export Compose compile contre des stubs ; seul un build Gradle dans l'app
  le prouve totalement.
- Kinetic conçoit des apps mobiles, pas des sites vitrines.
