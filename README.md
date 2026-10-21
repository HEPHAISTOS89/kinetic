# Kinetic

**Un système de design complet pour le modèle, dédié aux apps mobiles** (Flutter,
SwiftUI, Jetpack Compose, React Native). Le modèle doit penser comme un
directeur de design avant de styliser, décider avec précision, anticiper chaque
état, puis prouver la qualité du résultat.

> Penser comme un design lead, livrer comme un ingénieur.

## Pourquoi les modèles produisent du « slop », et la réponse de Kinetic

| Cause | Symptôme | Couche Kinetic |
|---|---|---|
| Retour à la moyenne : sans cible précise, le modèle produit l'app moyenne | dégradé violet, « Bonjour Sam 👋 », grille de cartes | **Savoir de goût** concret (14 directions chiffrées, exemplaires, secteurs) + **thèse** propre au produit |
| Raisonnement superficiel : on décide au pixel avant de comprendre | joli écran qui répond à la mauvaise question, aucun état d'erreur | **Architecture cognitive** : comprendre → décider → anticiper → systématiser → réaliser → prouver |
| Décisions implicites, invérifiables | 14 tailles de police, 9 gris, 6 rayons | **KDL**, le langage de raisonnement design : chaque décision est explicite, justifiée et vérifiée |
| Auto-critique complaisante | « ça a l'air premium » | **Moteur de goût** (mesuré) + **critique indépendant** (jugé, dans un contexte neuf) |

## Architecture

```
kinetic/
├── skills/                 la couche cognitive (9 modules)
│   ├── kinetic/            routeur : mode × cible × profondeur, boucle, règles F
│   ├── kinetic-think/      lecture produit, moment d'usage, thèse/anti-thèse, idée directrice, niveau d'expression, parcours
│   ├── kinetic-direct/     3 directions vraiment divergentes → 1 choisie, avec raisons ; signature
│   ├── kinetic-states/     chaque écran × chaque état, chaque composant × chaque variante, l'environnement de chaque élément
│   ├── kinetic-system/     typo → couleur → espace → forme → élévation → icônes → mouvement → haptique
│   ├── kinetic-craft/      précision au pixel, revue de code pointilleuse, icônes et SVG dessinés à la main
│   ├── kinetic-motion/     physique (springs), chorégraphie, gestes, reduce-motion, haptique
│   ├── kinetic-code/       design→code et code→design en Flutter, SwiftUI, Compose, React Native, web mobile
│   └── kinetic-critique/   pré-mortem, audit, évaluation du goût, verdicts, boucle d'amélioration
├── agents/                 kinetic-critic (adversarial, à l'aveugle) · kinetic-director (divergence) · kinetic-forensics (code→design)
├── commands/               /kinetic:create · redesign · improve · audit · system · build · read · evolve
├── knowledge/              ~2 900 lignes de savoir concret : anti-slop (52 règles F/D/C), typographie, couleur (OKLCH),
│                           layout, mouvement, états, iconographie/SVG, iOS, Android, copy, 14 directions, exemplaires,
│                           18 secteurs, grille de goût, et 5 stacks
├── docs/                   ARCHITECTURE · KDL (le langage) · PROTOCOL (communication) · TOOLS (contrats) · EVALUATION
├── engine/ + bin/kinetic   moteur déterministe, Python 3 sans dépendance
├── hooks/                  lint design continu après chaque modification UI (seulement dans les projets avec .kinetic/)
├── examples/lune/          un enregistrement KDL complet de référence
├── evals/                  4 rounds A/B à l'aveugle : briefs, harness (SwiftUI, Flutter, React Native), résultats, retours
└── tests/                  52 tests, dont la compilation réelle des exports Swift (iOS + macOS), TypeScript, Flutter et Kotlin (stubs)
```

### Le langage : KDL
`.kinetic/design.kdl` contient toutes les décisions, de la thèse jusqu'au
dernier état du dernier bouton. C'est un sous-ensemble strict de YAML, avec un
vocabulaire fermé et des références de tokens (`$color.accent`, `$spring.settle`).
Le moteur vérifie que l'enregistrement est complet et cohérent ; le même fichier
s'exporte vers 5 stacks. Spécification : [docs/KDL.md](docs/KDL.md). Exemple
complet : [examples/lune/design.kdl](examples/lune/design.kdl).

### Le moteur
```bash
bin/kinetic init .                                 # .kinetic/ (config + squelette KDL), détecte la stack
bin/kinetic validate .kinetic/design.kdl           # complétude + cohérence (contraste, grille, rampe, états, physique…)
bin/kinetic palette "#C9A27E" --kdl                # rôles clair/sombre en OKLCH, contrastes WCAG + APCA vérifiés
bin/kinetic scan lib/                              # faits de design + slop dans le code, fichier:ligne, niveau de preuve
bin/kinetic dna lib/ --kdl                         # code → système de design réel + proposition consolidée
bin/kinetic states code lib/                       # écrans qui chargent des données sans état erreur/vide/chargement
bin/kinetic export .kinetic/design.kdl --stack swiftui --out Sources/Design/
bin/kinetic svg lint icons/                        # 13 règles de fabrication d'icônes, sur un fichier et sur le set
bin/kinetic spring 0.4 0.9                         # un spring traduit pour SwiftUI, Flutter, Compose, Reanimated, CSS
bin/kinetic score --kdl … --code … --judged .kinetic/critique.json   # mesuré + jugé → verdict
```
Chaque résultat sépare ce qui est **observé**, **dérivé** et **inféré**. Une
zone non scannée est **inconnue**, jamais « propre ». Contrats : [docs/TOOLS.md](docs/TOOLS.md).

## Installation (Claude Code)
```bash
claude plugin marketplace add /chemin/vers/kinetic
```
```bash
claude plugin install kinetic@kinetic-local
```
Pour Codex, le manifeste `.codex-plugin/plugin.json` expose les mêmes skills.

## Utilisation
Demande naturellement (« redesign mon app Flutter, elle fait cheap ») ou
utilise un mode explicite : `/kinetic:create`, `/kinetic:redesign`,
`/kinetic:improve`, `/kinetic:audit`, `/kinetic:system`, `/kinetic:build`,
`/kinetic:read`, `/kinetic:evolve`.

## Vérifier
```bash
python3 -m unittest discover -s tests -v
```
Protocole d'évaluation (moteur, déclenchement, A/B à l'aveugle) : [docs/EVALUATION.md](docs/EVALUATION.md).

## Ce que l'évaluation montre (4 rounds A/B à l'aveugle, 12 lectures de critiques indépendants)
| Round | Brief | Stack | Moyenne jugée (modèle seul / Kinetic) | Findings mesurés (modèle seul / Kinetic) |
|---|---|---|---|---|
| 1 | Courant (transport) | SwiftUI | 3,67 / 3,78 | 3 majeurs / 0 |
| 2 | Courant (transport) | SwiftUI | 3,78 / 3,56 | 3 majeurs / 0 |
| 3 | Tally (dépenses partagées), les deux avec boucle critique | SwiftUI | 3,83 / 3,83 | 1 F + 6 D / 0 |
| 4a | Prise (salle d'escalade), 3 critiques | Flutter | 4,26 / 4,22 | 5 F + 6 D / 1 mineur |
| 4b | Petit Jour (crèche, interface en français), 3 critiques | React Native | 3,81 / 3,96 | 1 F + 8 D / 0 |

- En qualité jugée à l'aveugle, Kinetic **égale** un modèle de pointe (3,91 contre 3,90 sur les 12 lectures) ; il ne le dépasse pas.
- Le compromis est stable sur 4 briefs et 3 stacks : Kinetic gagne en **anticipation** (états, hors-ligne, XXL, mode « en séance »), en **fidélité native** et en **rigueur mesurée** ; le modèle seul gagne en **identité** (6 critiques sur 6 au round 4).
- Le plancher d'identité v1.4 n'a pas suffi. Le round 4 montre pourquoi : les designs gagnants dessinent un **vocabulaire tiré du domaine** (prises, scotch, bâtons de comptage, lune/soleil/maison) et le substituent aux éléments génériques. La v1.5 réécrit la règle en ce sens (kinetic-direct §4b), ajoute le héros « verdict d'abord » et les règles des moments à fort enjeu — **pas encore re-mesurée**.
- L'auto-critique s'est calibrée (±0,1 au round 4) mais surestime encore l'identité : `ship` exige un critique indépendant.
Détails et rapports : [docs/EVALUATION.md](docs/EVALUATION.md), `evals/`.

## Limites assumées
- Le scan est lexical (sans AST) : ses findings `inferred` sont des hypothèses à confirmer.
- Le score ne donne jamais un « chiffre de goût » unique : le mesuré et le jugé restent séparés.
- L'export Compose est compilé avec `kotlinc` contre des stubs de signatures Compose, pas contre les vraies librairies : seul un build Gradle dans l'app le prouve totalement.
- Génération d'images (illustrations, icône d'app) : hors périmètre de la v1.
