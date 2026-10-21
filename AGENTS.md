# AGENTS.md

## Mission

Ce dépôt fournit un kit métier autonome pour produire la revue de presse du SNUM
dans l’Assistant DINUM. Le dispositif comporte deux Projets distincts :
`Newsletter SNUM - Collecte` produit un paquet JSON validé et
`Newsletter SNUM - Rendu HTML` le transforme selon le gabarit Bacoco. Une troisième
option, le fichier `outil-rendu-dsfr.html`, produit un courriel HTML autonome à
partir du même paquet ; elle ne remplace aucun des deux Projets historiques. Le
Projet Assistant DSFR essayé auparavant reste un candidat non validé.

Le poste métier utilise l’Assistant pour Collecte et Rendu HTML. Le rendu de mail
DSFR utilise un fichier HTML local, selon le choix accepté après les échecs de
reproduction du logo. Python et Node.js servent uniquement à la maintenance et aux
tests ; aucun terminal n’est ajouté au parcours métier.

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
- `NOTICE-RENDU-DSFR-V1.0.md` et `_source/30-BLOCS-MAIL-DSFR.md` : canal mail complémentaire ;
- `scripts/newsletter_mail.py` et `scripts/build_mail_kit.py` : rendu et génération du kit mail ;
- `_source/mail-tool-*.js`, `_source/mail-tool-shell.html` et `scripts/build_mail_tool.py` : outil autonome de rendu DSFR ;
- `tests/` : invariants exécutables.

Les anciennes versions vivent uniquement sous
`_documentation/archives/releases/`. Ne jamais les modifier pour corriger la
version active.

## Architecture et invariants

- Conserver deux Projets Assistant séparés et deux conversations :
  `COLLECTE → JSON → RENDU`.
- Dans Collecte, l’utilisateur fournit uniquement `DATE_EDITION` et `PERIODE`.
  Le Projet lance lui-même une recherche Web composite couvrant les cinq rubriques,
  filtre la fenêtre, déduplique les URL et produit le paquet V519 dans sa première
  réponse.
- Le Web est activé dans Collecte et désactivé dans Rendu. Aucun chat Web ordinaire,
  requête à recopier, commande intermédiaire ou relance automatique n’appartient au
  parcours métier.
- Une rubrique vide et une collecte de moins de cinq sources sont signalées dans
  `watch` sans empêcher le JSON.
- Le Projet Rendu n’utilise jamais le Web ; toute modification du contenu
  éditorial est interdite.
- `articles=[]` est un paquet best effort valide. Rendu produit alors le bloc
  `VIDE`, suivi de `SURVEILLER` si `watch` contient des alertes.
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

Exception autorisée explicitement le 21 octobre 2026 : les trois adresses métier
déjà présentes dans le pied de page du gabarit mail DSFR livré ce jour peuvent
être versionnées avec ce gabarit et ses dérivés dans ce dépôt GitHub. Cette
exception ne couvre aucune autre adresse ni donnée personnelle.

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
- la recette réelle lance la recherche Web depuis Collecte à partir de
  `DATE_EDITION` et `PERIODE`, puis produit directement un paquet V519 sans URL
  dupliquée ni action intermédiaire ;
- le Projet Rendu produit au premier passage un HTML dont la première ligne est
  `## HTML COMPLET`, y compris pour un paquet best effort vide, sans `A_COMPLETER`
  ni préambule ;
- le rendu est comparé au gabarit canonique selon le contrat annoncé ;
- `README.md`, la notice et le rapport décrivent les preuves et les limites ;
- le commit local et la branche distante publiée désignent le même SHA après le push.

## Extension de courriel DSFR

- Préserver les instructions, ressources et ZIP des deux Projets historiques.
- Le parcours historique reste inchangé ; le mail DSFR passe de Collecte au fichier autonome, sans conversation de rendu supplémentaire.
- Modifier la source `_source/30-BLOCS-MAIL-DSFR.md`, puis régénérer avec `python3 scripts/build_mail_kit.py`. Ne pas éditer les dérivés `31` à `34` ni le ZIP à la main.
- Préserver l’autonomie, le logo base64, la signature et les flèches décoratives.
- Les dates hors fenêtre restent présentées normalement dans le mail, sans changer Collecte. Le paramètre `allow_outside_window` du validateur partagé reste `False` par défaut pour le rendu historique.
- Le prompt mail reste sous 4 000 caractères et chacune de ses neuf ressources sous 4 500.
- Vérifier aussi `python3 scripts/build_mail_kit.py --check` et comparer chaque sortie réelle au canon avec `python3 scripts/newsletter_mail.py verify --input paquet.json --html sortie.html`.
- La recette réelle du nouveau Projet n’exige pas de relancer ou reconfigurer Collecte. Les tests locaux seuls ne prouvent pas la copie fidèle du logo par l’Assistant.
- Les preuves et le statut courant sont dans `_documentation/recette-mail-dsfr/RAPPORT.md`. Ne pas conclure à une conformité Outlook depuis un aperçu navigateur.
- Pour le livrable métier, exécuter `python3 scripts/build_mail_tool.py`, puis `python3 scripts/build_mail_tool.py --check`. Ne pas éditer `outil-rendu-dsfr.html` directement.
- Le moteur JavaScript doit produire le même HTML que le moteur Python pour les mêmes paquets. Les tests exercent les scripts inclus dans le fichier distribué, et non seulement leurs sources.
- Les alertes `watch` de Collecte restent réservées à l’expéditeur, dans un encadré hors de l’aperçu. Ne jamais les intégrer au mail DSFR, même sous forme de commentaires HTML. Les rubriques sans article sont omises ; Collecte et le Rendu HTML historique restent inchangés.
- Préserver le fonctionnement hors connexion : aucun script distant, appel réseau ou stockage du paquet. L’aperçu est isolé dans une iframe sans permission de script ; une modification de l’entrée retire le téléchargement précédent.
- La préparation du téléchargement est vérifiée en simulation du DOM. Ne pas la présenter comme un téléchargement réel ni comme une recette visuelle dans un navigateur.
