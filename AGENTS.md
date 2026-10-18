# AGENTS.md

## Mission

Ce dépôt fournit un kit métier autonome pour produire la revue de presse du SNUM
dans l’Assistant DINUM. Le dispositif comporte deux Projets distincts :
`Newsletter SNUM - Collecte` produit un paquet JSON validé et
`Newsletter SNUM - Rendu HTML` le transforme selon le gabarit Bacoco.

Le poste métier utilise uniquement l’Assistant. Les scripts Python servent à la
maintenance, à la génération des kits et à la vérification avant livraison.

## Sources de vérité

À lire au démarrage :

- `README.md` : parcours pédagogique complet ;
- `NOTICE-V5.23.md` : installation et séquence métier de la version active ;
- `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` : orchestration de la collecte ;
- `02-METHODE-COLLECTE-SNUM-V5.23.md` : recherche composite et normalisation ;
- `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` : contrat V519 transmis au rendu ;
- `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md` : contrat de rendu ;
- `_source/05-BLOCS-HTML-CANONIQUES.md` : source unique des blocs HTML ;
- `scripts/build_split_kit.py` : génération des ressources et des deux ZIP ;
- `tests/` : invariants exécutables.

Les anciennes versions vivent uniquement sous
`_documentation/archives/releases/`. Ne jamais les modifier pour corriger la
version active.

## Architecture et invariants

- Conserver deux Projets Assistant séparés et la séquence
  `COLLECTE → CHAT WEB ORDINAIRE → JSON → RENDU`.
- Dans le Projet Collecte, l’utilisateur fournit `DATE_EDITION`, `PERIODE` et
  `RECHERCHE_COMPOSITE` dans le même premier message. Le Projet rend une seule
  requête couvrant les cinq rubriques, sans appeler le Web.
- Le métier exécute cette requête dans un nouveau chat Assistant ordinaire avec le
  Web, puis copie toute la réponse dans le chat Collecte d’origine.
- Le Projet Collecte filtre la fenêtre, déduplique les URL et ignore une absence
  contradictoire si la rubrique possède un résultat valide. Au collage, il mémorise
  `SOURCES_NORMALISEES` puis demande l’unique commande `NORMALISER_V519`, qui produit
  le paquet V519 sans nouvelle recherche.
- Aucun des deux Projets enregistrés n’utilise le Web. Seul le chat ordinaire de
  recherche l’utilise.
- Une rubrique vide et une collecte de moins de cinq sources sont signalées dans
  `watch` sans empêcher le JSON.
- Le Projet Rendu n’utilise jamais le Web ; toute modification du contenu
  éditorial est interdite.
- Conserver exactement quatre ressources HTML, numérotées de `21` à `24`,
  chacune limitée à 4 500 caractères.
- Limiter chaque prompt système à 4 000 caractères.
- Une URL canonique ne peut apparaître qu’une fois dans `articles`.
- La racine contient uniquement les fichiers numérotés de la version active et
  les sources permanentes. Archiver la version précédente avant une livraison.
- Les deux ZIP portent exactement les noms des Projets Assistant. Ne jamais
  demander au métier de téléverser le ZIP lui-même.

BON : corriger `_source/05-BLOCS-HTML-CANONIQUES.md`, puis régénérer les quatre
ressources avec le script.

MAUVAIS : modifier directement `21-CANON-HTML-COQUE-A-*.md` ou un ZIP généré.

## Commandes de validation

Depuis la racine du dépôt :

```bash
python3 -m unittest discover -s tests -v
ruff check --no-cache scripts tests
python3 scripts/build_split_kit.py --check
git diff --check
```

Après une modification des prompts, des blocs ou du générateur :

```bash
python3 scripts/build_split_kit.py
python3 scripts/build_split_kit.py --check
```

Après chaque écriture Markdown, depuis `/Users/alex/Claude` :

```bash
bash scripts/check-accents.sh git-hors-workflow/assistant-ia-newsletter-com-snum/<fichier.md>
```

## Conventions

- Python standard library uniquement pour le moteur et les tests actuels.
- Tests publics via `scripts/newsletter_html.py`, sans tester les fonctions
  privées quand la CLI permet d’observer le comportement.
- Les versions de fichiers doivent rester cohérentes dans chaque Projet. La
  Collecte V5.23 conserve volontairement le schéma de paquet V519 consommé par le
  Rendu V5.19.
- Le saut de ligne entre `COQUE_A` et `COQUE_B` fait partie du contrat canonique.
- Les dates affichées utilisent le mois en toutes lettres ; les dates ISO servent
  aux contrôles.

BON : un test rouge reproduit le défaut, puis le changement minimal le rend vert.

MAUVAIS : assouplir le validateur pour faire accepter une sortie de l’Assistant.

## Zones à préserver

- `_documentation/archives/` : historique figé ;
- `_documentation/prompt-loic.md` : archive du prompt planificateur ;
- `_source/` : sources techniques non téléversées dans l’Assistant ;
- `Newsletter SNUM - Collecte.zip` et `Newsletter SNUM - Rendu HTML.zip` :
  artefacts générés, jamais édités manuellement.

Ne jamais commiter de secret, d’adresse de diffusion, de donnée restreinte ou de
`.DS_Store`. Ne jamais publier sur GitHub Pages ni envoyer un courriel pendant une
recette sans demande explicite.

## Git

Le dépôt de référence est `alexandra-guiderdoni/assistant-ia-newsletter-com-snum`
sur `main`. Avant un push, vérifier le remote, la divergence, le diff indexé, les
tests et l’absence de fichiers parasites. Ne jamais forcer un push et ne jamais
ajouter d’attribution d’agent au message de commit.

## Modes d’échec connus

- Un même article peut recevoir deux `CLE_EVENEMENT` différentes : contrôler
  aussi l’unicité des URL canoniques.
- Un LLM peut modifier les espaces ou l’indentation : ne déclarer une identité
  octet par octet qu’après comparaison déterministe.
- Un contrôle local vert ne prouve pas le comportement de l’Assistant : réaliser
  une recette réelle dans deux Projets vierges pour chaque nouvelle version.
- Si une réponse commence par `A_COMPLETER`, arrêter la chaîne et corriger la
  cause ; ne jamais transmettre le paquet ou le HTML suivant.
- Un préambule avant le marqueur de paquet ou avant `## HTML COMPLET` est un échec,
  même si le JSON ou le HTML qui suit est valide.

## Définition de fin

Une version est livrable seulement si :

- la suite `unittest`, Ruff et `build_split_kit.py --check` est verte ;
- les prompts respectent 4 000 caractères et les quatre ressources 4 500 ;
- les ZIP contiennent exactement les fichiers attendus dans l’ordre documenté ;
- la recette réelle produit une requête composite à partir de `DATE_EDITION`,
  `PERIODE` et `RECHERCHE_COMPOSITE`, enregistre la réponse Web sans JSON, puis
  produit un paquet V519 après `NORMALISER_V519`, sans URL dupliquée ;
- le Projet Rendu produit au premier passage un HTML dont la première ligne est
  `## HTML COMPLET`, sans `A_COMPLETER` ni préambule ;
- le rendu est comparé au gabarit canonique selon le contrat annoncé ;
- `README.md`, la notice et le rapport décrivent les preuves et les limites ;
- le commit local et la branche distante publiée désignent le même SHA après le push.
