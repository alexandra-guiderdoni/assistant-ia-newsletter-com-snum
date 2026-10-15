# Configurer l’Assistant DINUM pour la revue SNUM V5.8 progressive

Ce guide permet de configurer un Projet dans l’Assistant DINUM sans script, terminal ni accès GitHub sur le poste métier. La sortie reste dans le chat.

## Verdict vérifié

La limite de 4 000 caractères du champ **Instructions (expérimental)** est contournée : le prompt système mesure moins de 4 000 caractères et le canon HTML est réparti en fragments Markdown indexés.

La récupération des six fragments a été observée deux fois dans l’Assistant. En revanche, leur copie littérale dans une longue réponse reste non déterministe. La livraison est donc :

- exploitable pour une recette assistée ;
- sûre grâce à l’arrêt `A_COMPLETER — HTML canonique non établi` ;
- **NO-GO pour une production autonome garantissant un HTML identique à Bacoco**.

Le garde-fou est volontaire : un arrêt explicite vaut mieux qu’un HTML inventé.

## Fichiers à utiliser

Utiliser le paquet `kit-dinum-snum-v5-8-progressif-8-fichiers.zip` et le prompt `PROMPT-SYSTEME-SNUM-V5.8.md`.

Après extraction, téléverser exactement :

1. `00-PROMPT-PROJET.md` ;
2. `01-ETAT-HISTORIQUE.md` ;
3. `02-METHODE-EDITORIALE.md` ;
4. `05-INDEX-HTML.md` ;
5. `06-COQUE-DEBUT.md` ;
6. `07-COQUE-FIN.md` ;
7. `08-BLOC-ESSENTIEL.md` ;
8. `09-BLOCS-RUBRIQUES.md`.

`05-BLOCS-HTML-CANONIQUES.md` reste la source locale unique. Les fichiers `05` à `09` du paquet progressif sont générés depuis cette source ; ils ne doivent pas être modifiés séparément.

## Les deux niveaux de prompts

Le dispositif ne repose pas sur un prompt unique à répéter. Il comporte deux niveaux complémentaires :

1. **Le prompt système du Projet**, installé une seule fois dans **Instructions (expérimental)**. Il fixe les règles permanentes, l’ordre des opérations, les contrôles et l’arrêt `A_COMPLETER`.
2. **Les prompts utilisateur de chaque édition**, envoyés dans une même conversation. Ils déclenchent successivement la qualification des sources puis la production du HTML.

Ne pas coller le prompt système dans la conversation. Ne pas placer les prompts utilisateur dans **Instructions (expérimental)**.

## Niveau 1 — Installer le prompt système et les ressources

Le texte à installer est le contenu intégral de `PROMPT-SYSTEME-SNUM-V5.8.md`. Il ne contient ni date d’édition ni fenêtre de collecte : ces valeurs sont fournies au niveau 2.

1. Ouvrir <https://assistant.numerique.gouv.fr/>.
2. Ouvrir le panneau de gauche, puis choisir **Nouveau projet**.
3. Nommer le Projet `Newsletter SNUM`.
4. Copier intégralement `PROMPT-SYSTEME-SNUM-V5.8.md` dans **Instructions (expérimental)**.
5. Vérifier que le champ n’est pas tronqué et se termine par `N’affirme aucun contrôle non exécuté.`
6. Ajouter les huit fichiers Markdown.
7. Créer le Projet et attendre la disparition du message d’indexation.
8. Ouvrir une conversation depuis ce Projet.

Contrôle observé le 15 octobre 2026 : prompt de 3 715 caractères, terminaison exacte et huit noms de fichiers présents après indexation.

Les captures de l’interface restent disponibles dans [le guide de validation précédent](./_documentation/validation-v5.8-2026-10-14/GUIDE-VALIDATION-ASSISTANT-DINUM-V5.8.md).

## Niveau 2 — Utiliser les prompts de chaque édition

Les quatre messages doivent être envoyés dans la même conversation et dans l’ordre indiqué. Ils forment deux phases métier :

- **Qualification** : `COLLECTE` avec le Web, puis `VALIDATION` sans Web ;
- **Production** : `CANON` sans Web, puis `RENDU` sans Web.

Ne pas passer à l’étape suivante si le jeton de fin attendu manque. Le canon est chargé juste avant le rendu : un chargement effectué trop tôt se dégrade dans le contexte.

### Qualification des sources — phase A

#### 1. Collecte — Web activé

```text
PHASE COLLECTE. Utilise le Web. Édition du {{DATE_EDITION}}, fenêtre du {{DEBUT}} au {{FIN}} inclus. Ne rédige ni REVUE ni HTML. Recherche et ouvre les sources publiques intégralement accessibles. Réponds sous CANDIDATS avec une liste numérotée ; pour chaque candidat : titre, URL canonique, date de publication explicitement lue sur la page au format AAAA-MM-JJ ou DATE_INCONNUE, accès intégral OUI/NON, rubrique exacte et fait essentiel. Ne décide pas encore si la date est dans la fenêtre. Termine par COLLECTE_TERMINEE, sans question.
```

Attendre `COLLECTE_TERMINEE`. La réponse doit contenir `CANDIDATS`, sans `REVUE` ni HTML.

#### 2. Validation — Web désactivé

```text
PHASE VALIDATION. N’utilise pas le Web et ne rédige ni REVUE ni HTML. Relis uniquement CANDIDATS. Applique exactement {{DEBUT_ISO}} <= DATE_PUBLICATION <= {{FIN_ISO}} et exige accès intégral OUI. Rejette DATE_INCONNUE, incohérence manifeste et doublon ; conserve une seule URL canonique par événement. Réponds sous SOURCES_VALIDES avec titre, URL, date, rubrique exacte et fait essentiel ; puis SOURCES_EXCLUES avec chaque motif ; termine par VALIDATION_TERMINEE. Ne pose aucune question.
```

Attendre `VALIDATION_TERMINEE`. Seules les entrées de `SOURCES_VALIDES` pourront alimenter le rendu.

### Production de la newsletter — phase B

#### 3. Canon — Web désactivé

```text
PHASE CANON. N’utilise pas le Web. Recherche SNUM_CANON_V58_INDEX_START dans les ressources du Projet, suis READ_NEXT et charge intégralement les fragments 06, 07, 08 et 09. Vérifie les six paires START/END et conserve littéralement les blocs html. Ne rends pas encore la newsletter. Réponds seulement CANON_HTML_PRET puis les six paires, ou CANON_HTML_INCOMPLET puis le jeton manquant.
```

Ne continuer que si la réponse contient `CANON_HTML_PRET` et les six paires :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_SHELL_TAIL_START / SNUM_SHELL_TAIL_END` ;
- `SNUM_ESSENTIAL_START / SNUM_ESSENTIAL_END` ;
- `SNUM_RUBRIC_START / SNUM_RUBRIC_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

#### 4. Rendu — Web désactivé

```text
PHASE RENDU. N’utilise pas le Web. Utilise exclusivement SOURCES_VALIDES et les fragments canoniques chargés au tour précédent. Copie littéralement 06, insère les blocs 08 et 09 nécessaires, puis 07 ; remplace seulement les marqueurs @@. Ne crée aucune balise ni classe absente des fragments. Livre exactement ## REVUE, ## HTML COMPLET avec un unique bloc html de <!doctype html> à </html>, puis ## DOSSIER PRIVÉ. Avant affichage, vérifie le title, /revue-presse-snum/styles.css?v=20260917, l’absence de marqueur @@, fr-theme-modal et les scripts DSFR 1.15.2. Si un point n’est pas établi, réponds A_COMPLETER — HTML canonique non établi sans afficher de code. Ne pose aucune question.
```

## Contrôle métier minimal

Ne pas utiliser le HTML si l’un de ces contrôles échoue :

- les trois titres sont présents dans l’ordre attendu ;
- chaque source est dans `SOURCES_VALIDES` ;
- aucun marqueur `@@` ne subsiste ;
- un seul bloc HTML va de `<!doctype html>` à `</html>` ;
- le titre est `Revue de presse du … - SNUM` ;
- la feuille `/revue-presse-snum/styles.css?v=20260917` est présente ;
- les trois accès rapides, un seul `h1` et le modal `fr-theme-modal` sont présents ;
- les scripts DSFR 1.15.2 module et nomodule sont présents ;
- les rubriques et la navigation utilisent uniquement les libellés canoniques.

Si l’Assistant renvoie `A_COMPLETER`, le garde-fou a fonctionné. Ce résultat nécessite une reprise ou un contrôle extérieur ; il ne doit pas être présenté comme une édition prête.

## Recette du 15 octobre 2026

Le kit a été installé dans le nouveau Projet unique `Newsletter SNUM`, puis une collecte de recette a été lancée pour l’édition du 14 octobre 2026, fenêtre du 3 au 13 octobre inclus.

Trois envois ont échoué avant toute réponse. Le journal du navigateur indique `the authentication session has expired`. Cela prouve une expiration de la session AgentConnect, pas une erreur du kit et pas une indisponibilité générale de l’Assistant.

Après reconnexion, une première reprise a été faite par erreur dans une conversation générale, sans accès aux ressources du Projet. La recette complète a ensuite été relancée depuis `Newsletter SNUM` : `COLLECTE`, `VALIDATION` et `CANON` ont abouti, puis `RENDU` a produit un HTML complet.

Le rendu reste non conforme au canon : les rubriques `ia` et `rh` ont perdu leur classe obligatoire `section-muted`, sans déclencher l’arrêt `A_COMPLETER`. Le verdict reste **NO-GO pour une livraison autonome garantissant un HTML identique à Bacoco**. Voir le [compte rendu d’installation et de recette](./_documentation/installation-v5.8-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md).

## Preuves de la recette du 14 octobre 2026

- [conversation à deux phases : canon retrouvé, écarts éditoriaux](https://assistant.numerique.gouv.fr/chat/88b774da-c07b-4b78-a5bb-22739def300f) ;
- [conversation de durcissement : date corrigée après audit](https://assistant.numerique.gouv.fr/chat/066f718b-db2f-432c-a576-ec96104ebb57) ;
- [conversation en phases séparées : collecte et validation réussies, rendu arrêté proprement](https://assistant.numerique.gouv.fr/chat/4dddefda-e5da-4736-b4ca-9464e8b5c9dd) ;
- [compte rendu détaillé](./_documentation/validation-v5.8-progressive-2026-10-14/RESULTAT-RECETTE-PROGRESSIVE.md).

Une recette prouve seulement le cas exécuté. L’autoévaluation de l’Assistant ne remplace pas un validateur indépendant ni un audit RGAA.
