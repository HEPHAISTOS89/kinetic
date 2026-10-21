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
└── tests/                  36 tests, dont la compilation réelle des exports Swift / TypeScript / Flutter
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

## Limites assumées
- Le scan est lexical (sans AST) : ses findings `inferred` sont des hypothèses à confirmer.
- Le score ne donne jamais un « chiffre de goût » unique : le mesuré et le jugé restent séparés.
- L'export Compose n'est pas compilé dans les tests (pas de toolchain Kotlin ici).
- Génération d'images (illustrations, icône d'app) : hors périmètre de la v1.
