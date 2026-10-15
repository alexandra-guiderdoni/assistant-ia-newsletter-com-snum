# Newsletter SNUM avec l’Assistant DINUM - guide V5.8

Ce dépôt fournit un kit prêt à installer pour préparer une revue de presse SNUM dans l’Assistant DINUM, sans terminal ni script sur le poste métier. La newsletter et son HTML sont livrés dans le chat ; rien n’est publié ni envoyé automatiquement.

> **Verdict actuel.** L’installation, la collecte et le filtrage ont été vérifiés. En revanche, l’Assistant peut encore altérer le HTML canonique sans déclencher son arrêt de sécurité. La V5.8 convient donc à une recette assistée, mais reste **NO-GO pour garantir de façon autonome un rendu identique à Bacoco**. Un résultat `A_COMPLETER` est un arrêt normal, pas une newsletter prête.

## Pourquoi ce kit existe

La difficulté n’est pas d’écrire une newsletter : elle est de faire respecter simultanément une fenêtre de dates, des sources lisibles, une ligne éditoriale et un gabarit HTML exact dans un champ système limité à 4 000 caractères.

La V5.8 sépare donc les responsabilités :

- le **prompt système** contient les règles permanentes ;
- les **huit fichiers du Projet** servent de mémoire documentaire et de canon HTML ;
- les **quatre prompts utilisateur** font avancer une édition par étapes contrôlables ;
- des **jetons de fin** empêchent de continuer silencieusement après une étape incomplète.

## Le modèle mental

Imaginez l’Assistant comme un générateur probabiliste doté d’une mémoire de travail limitée, et non comme un compilateur qui copie toujours un fichier à l’octet près.

```text
Prompt système       → les règles stables
Fichiers du Projet   → la mémoire de référence
COLLECTE             → trouver des candidats
VALIDATION           → éliminer les candidats non conformes
CANON                → charger le gabarit juste à temps
RENDU                → assembler la livraison finale
Contrôle humain      → décider si le HTML est utilisable
```

Chaque séparation répond à un risque précis : le Web sert à découvrir, mais pas à décider ; la validation applique des règles simples ; le canon est chargé juste avant le rendu pour limiter sa dégradation dans le contexte ; le contrôle humain couvre ce que l’autoévaluation du modèle ne prouve pas.

## Ce qu’il faut préparer

- un accès actif à <https://assistant.numerique.gouv.fr/> ;
- [`kit-dinum-snum-v5-8-progressif-8-fichiers.zip`](./kit-dinum-snum-v5-8-progressif-8-fichiers.zip) ;
- [`PROMPT-SYSTEME-SNUM-V5.8.md`](./PROMPT-SYSTEME-SNUM-V5.8.md) ;
- la date d’édition et les deux bornes inclusives de la période à couvrir.

Le kit contient exactement huit ressources. Ne les renommez pas et ne les modifiez pas séparément : elles sont dérivées d’une source canonique unique.

## Installer le Projet une seule fois

1. Décompressez `kit-dinum-snum-v5-8-progressif-8-fichiers.zip` sur votre poste.
2. Ouvrez l’Assistant DINUM, puis choisissez **Nouveau projet** dans le panneau de gauche.
3. Nommez le Projet `Newsletter SNUM`.
4. Ouvrez [`PROMPT-SYSTEME-SNUM-V5.8.md`](./PROMPT-SYSTEME-SNUM-V5.8.md) et copiez tout son contenu dans **Instructions (expérimental)**.
5. Vérifiez que le texte se termine exactement par `N’affirme aucun contrôle non exécuté.`. Cette vérification détecte une éventuelle troncature.
6. Téléversez exactement les huit fichiers suivants :
   - `00-PROMPT-PROJET.md` ;
   - `01-ETAT-HISTORIQUE.md` ;
   - `02-METHODE-EDITORIALE.md` ;
   - `05-INDEX-HTML.md` ;
   - `06-COQUE-DEBUT.md` ;
   - `07-COQUE-FIN.md` ;
   - `08-BLOC-ESSENTIEL.md` ;
   - `09-BLOCS-RUBRIQUES.md`.
7. Créez le Projet et attendez la disparition du message d’indexation.
8. Lancez la conversation depuis le Projet avec **Start new conversation in Newsletter SNUM**. Une conversation générale n’a pas accès aux huit ressources.

Le prompt système est installé une seule fois. Ne le collez jamais dans la conversation. Les quatre prompts ci-dessous sont, eux, envoyés pour chaque édition.

## Préparer une édition

Choisissez quatre valeurs avant de commencer :

- `{{DATE_EDITION}}` : date longue affichée, par exemple `14 octobre 2026` ;
- `{{DEBUT}}` et `{{FIN}}` : bornes longues inclusives ;
- `{{DEBUT_ISO}}` et `{{FIN_ISO}}` : les mêmes bornes au format `AAAA-MM-JJ`.

Envoyez les quatre messages dans **la même conversation**, dans l’ordre suivant. N’ouvrez une nouvelle conversation que pour recommencer toute l’édition.

## Première phase - qualifier les sources

### 1. COLLECTE - Web activé

Pourquoi : cette étape cherche et ouvre les pages. Elle collecte des faits observables sans encore décider si les sources sont admissibles.

```text
PHASE COLLECTE. Utilise le Web. Édition du {{DATE_EDITION}}, fenêtre du {{DEBUT}} au {{FIN}} inclus. Ne rédige ni REVUE ni HTML. Recherche et ouvre les sources publiques intégralement accessibles. Réponds sous CANDIDATS avec une liste numérotée ; pour chaque candidat : titre, URL canonique, date de publication explicitement lue sur la page au format AAAA-MM-JJ ou DATE_INCONNUE, accès intégral OUI/NON, rubrique exacte et fait essentiel. Ne décide pas encore si la date est dans la fenêtre. Termine par COLLECTE_TERMINEE, sans question.
```

Attendez `COLLECTE_TERMINEE`. La réponse doit contenir `CANDIDATS`, sans `REVUE` ni HTML. Sinon, arrêtez-vous et relancez cette étape.

### 2. VALIDATION - Web désactivé

Pourquoi : couper le Web réduit les nouvelles informations parasites. L’Assistant doit seulement appliquer la fenêtre, l’accès intégral et le dédoublonnage aux candidats déjà observés.

```text
PHASE VALIDATION. N’utilise pas le Web et ne rédige ni REVUE ni HTML. Relis uniquement CANDIDATS. Applique exactement {{DEBUT_ISO}} <= DATE_PUBLICATION <= {{FIN_ISO}} et exige accès intégral OUI. Rejette DATE_INCONNUE, incohérence manifeste et doublon ; conserve une seule URL canonique par événement. Réponds sous SOURCES_VALIDES avec titre, URL, date, rubrique exacte et fait essentiel ; puis SOURCES_EXCLUES avec chaque motif ; termine par VALIDATION_TERMINEE. Ne pose aucune question.
```

Attendez `VALIDATION_TERMINEE`. Vérifiez que chaque source retenue est bien comprise entre les deux dates incluses. Seules les entrées de `SOURCES_VALIDES` pourront alimenter le rendu.

## Seconde phase - produire la newsletter

### 3. CANON - Web désactivé

Pourquoi : le gabarit est rechargé juste avant sa consommation. Ce « juste-à-temps » limite le risque que ses balises et ses classes soient perdues après une longue collecte.

```text
PHASE CANON. N’utilise pas le Web. Recherche SNUM_CANON_V58_INDEX_START dans les ressources du Projet, suis READ_NEXT et charge intégralement les fragments 06, 07, 08 et 09. Vérifie les six paires START/END et conserve littéralement les blocs html. Ne rends pas encore la newsletter. Réponds seulement CANON_HTML_PRET puis les six paires, ou CANON_HTML_INCOMPLET puis le jeton manquant.
```

Ne continuez que si la réponse contient `CANON_HTML_PRET` et ces six paires :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_SHELL_TAIL_START / SNUM_SHELL_TAIL_END` ;
- `SNUM_ESSENTIAL_START / SNUM_ESSENTIAL_END` ;
- `SNUM_RUBRIC_START / SNUM_RUBRIC_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

### 4. RENDU - Web désactivé

Pourquoi : cette étape assemble des éléments déjà validés. Elle ne doit ni rechercher une nouvelle source ni improviser une balise ou une classe.

```text
PHASE RENDU. N’utilise pas le Web. Utilise exclusivement SOURCES_VALIDES et les fragments canoniques chargés au tour précédent. Copie littéralement 06, insère les blocs 08 et 09 nécessaires, puis 07 ; remplace seulement les marqueurs @@. Ne crée aucune balise ni classe absente des fragments. Livre exactement ## REVUE, ## HTML COMPLET avec un unique bloc html de <!doctype html> à </html>, puis ## DOSSIER PRIVÉ. Avant affichage, vérifie le title, /revue-presse-snum/styles.css?v=20260917, l’absence de marqueur @@, fr-theme-modal et les scripts DSFR 1.15.2. Si un point n’est pas établi, réponds A_COMPLETER - HTML canonique non établi sans afficher de code. Ne pose aucune question.
```

## Contrôler avant d’utiliser le résultat

N’utilisez pas le HTML si un seul contrôle échoue :

- les trois titres `## REVUE`, `## HTML COMPLET` et `## DOSSIER PRIVÉ` sont présents dans cet ordre ;
- toutes les sources du rendu figurent dans `SOURCES_VALIDES` ;
- un seul bloc HTML va de `<!doctype html>` à `</html>` ;
- aucun marqueur `@@` ne subsiste ;
- le titre suit `Revue de presse du … - SNUM` ;
- `/revue-presse-snum/styles.css?v=20260917` est présent ;
- les trois accès rapides, un seul `h1`, `fr-theme-modal` et les deux scripts DSFR 1.15.2 sont présents ;
- la navigation contient seulement les rubriques produites ;
- la rubrique IA utilise `<section id="ia" class="section-muted">` ;
- la rubrique RH utilise `<section id="rh" class="section-muted">`.

Si l’Assistant répond `A_COMPLETER - HTML canonique non établi`, le garde-fou a fonctionné : ne demandez pas de « continuer quand même ». Reprenez à `CANON` ou faites contrôler le résultat extérieurement.

## Ce que la V5.8 ne garantit pas encore

La recette réelle du 15 octobre 2026 a réussi `COLLECTE`, `VALIDATION` et `CANON`, puis a produit un HTML complet. Pourtant, les classes `section-muted` des rubriques IA et RH ont disparu sans déclencher `A_COMPLETER`.

La bonne posture est donc : **faire confiance au protocole pour structurer le travail, mais faire confiance aux preuves pour accepter le livrable**. L’affirmation `CANON_HTML_PRET` de l’Assistant n’est pas, à elle seule, une preuve d’identité avec le canon Bacoco.

## Dépannage rapide

- `the authentication session has expired` : reconnectez-vous à AgentConnect, puis recommencez dans le Projet ; ce message ne prouve pas une panne du kit.
- `CANON_HTML_INCOMPLET SNUM_CANON_V58_INDEX_START` : vérifiez que la conversation appartient bien à `Newsletter SNUM` et que les huit fichiers sont indexés.
- source hors fenêtre : reprenez à `VALIDATION` avec les bornes ISO exactes.
- HTML affiché malgré un écart : n’utilisez pas la sortie ; le contrôle humain prime.

## Sources et preuves

- [notice opérationnelle complète](./NOTICE-V5.8.md) ;
- [prompt système à installer](./PROMPT-SYSTEME-SNUM-V5.8.md) ;
- [rapport de contrôle V5.8](./RAPPORT-V5.8.md) ;
- [résultat de l’installation et de la recette réelle](./_documentation/installation-v5.8-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md).
