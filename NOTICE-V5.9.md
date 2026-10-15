# Configurer l’Assistant DINUM pour la revue SNUM V5.9 progressive

Ce guide permet de configurer un Projet dans l’Assistant DINUM sans script, terminal ni accès GitHub sur le poste métier. La sortie reste dans le chat.

## Verdict vérifié

La limite de 4 000 caractères du champ **Instructions (expérimental)** est contournée : le prompt système mesure moins de 4 000 caractères et le canon HTML est réparti en fragments Markdown indexés.

La récupération des six fragments a été observée deux fois dans l’Assistant. En revanche, leur copie littérale dans une longue réponse reste non déterministe. La livraison est donc :

- exploitable pour une recette assistée ;
- sûre grâce à l’arrêt `A_COMPLETER — HTML canonique non établi` ;
- **NO-GO pour une production autonome garantissant un HTML identique à Bacoco**.

Le garde-fou est volontaire : un arrêt explicite vaut mieux qu’un HTML inventé.

## Fichiers à utiliser

Utiliser le paquet `kit-dinum-snum-v5-9-progressif-8-fichiers.zip` et le prompt `PROMPT-SYSTEME-SNUM-V5.9.md`.

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

Le texte à installer est le contenu intégral de `PROMPT-SYSTEME-SNUM-V5.9.md`. Il ne contient ni date d’édition ni fenêtre de collecte : ces valeurs sont fournies au niveau 2.

1. Ouvrir <https://assistant.numerique.gouv.fr/>.
2. Ouvrir le panneau de gauche, puis choisir **Nouveau projet**.
3. Nommer le Projet `Newsletter SNUM`.
4. Copier intégralement `PROMPT-SYSTEME-SNUM-V5.9.md` dans **Instructions (expérimental)**.
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
PHASE COLLECTE.
Utilise le Web.
Édition du {{DATE_EDITION}}.
Fenêtre du {{DEBUT}} au {{FIN}} inclus.
Ne rédige ni REVUE ni HTML.
Exécute au moins dix requêtes distinctes : deux par rubrique,
dont une générale et une ciblée, sur au moins cinq domaines.
Si la première passe produit moins de cinq candidats,
effectue une seconde passe sur d’autres sources officielles
ou spécialisées.
Réponds d’abord sous COUVERTURE_COLLECTE avec une ligne par requête :
rubrique | requête | domaine | résultat | URL ouverte.
Réponds sous CANDIDATS avec une liste numérotée.
Pour chaque candidat, indique :
- le titre ;
- l’URL canonique ;
- la date de publication explicitement lue sur la page,
  au format AAAA-MM-JJ ou DATE_INCONNUE ;
- l’accès intégral OUI/NON ;
- la rubrique exacte ;
- le fait essentiel.
Ne décide pas encore si la date est dans la fenêtre.
Termine par COLLECTE_TERMINEE seulement si les cinq rubriques,
les dix requêtes, les cinq domaines et au moins cinq candidats
sont établis.
Sinon termine par COLLECTE_INSUFFISANTE avec les critères manquants.
Ne pose aucune question.
```

Attendre `COLLECTE_TERMINEE`. La réponse doit contenir `COUVERTURE_COLLECTE`, au moins cinq `CANDIDATS`, sans `REVUE` ni HTML. Si elle contient `COLLECTE_INSUFFISANTE`, renvoyer une seule fois le même message puis arrêter l’édition si le second essai échoue.

#### 2. Validation — Web désactivé

```text
PHASE VALIDATION.
N’utilise pas le Web.
Ne rédige ni REVUE ni HTML.
Relis uniquement CANDIDATS.

Fenêtre inclusive :
- DEBUT_ISO = {{DEBUT_ISO}}
- FIN_ISO = {{FIN_ISO}}

Recopie chaque date brute exactement telle qu’elle apparaît.
Ne la corrige pas et ne retire aucun texte.
Pour chaque candidat, exécute séparément :
1. date exactement au format AAAA-MM-JJ : OUI/NON ;
2. DATE_PUBLICATION >= {{DEBUT_ISO}} : OUI/NON ;
3. DATE_PUBLICATION <= {{FIN_ISO}} : OUI/NON ;
4. accès intégral = OUI : OUI/NON.

Une source est valide seulement si les quatre réponses sont OUI.
Exemples de comparaison :
- 2026-10-02 est antérieur à 2026-10-03 : EXCLURE ;
- 2026-10-15 est postérieur à 2026-10-13 : EXCLURE.
Rejette aussi DATE_INCONNUE, toute date accompagnée d’un texte,
toute incohérence manifeste et tout doublon.
Conserve une seule URL canonique par événement.

Réponds d’abord sous CONTROLE_DATES avec une ligne par candidat :
titre | date brute | format exact | borne basse | borne haute |
accès | décision.

Réponds ensuite sous SOURCES_VALIDES avec titre, URL, date,
rubrique exacte et fait essentiel.
Ajoute SOURCES_EXCLUES avec chaque motif.
Vérifie : nombre de SOURCES_VALIDES + nombre de SOURCES_EXCLUES
= nombre de CANDIDATS.
Termine par VALIDATION_TERMINEE.
Ne pose aucune question.
```

Attendre `VALIDATION_TERMINEE`. Contrôler que chaque source valide possède quatre `OUI` et que le total des sources valides et exclues égale le nombre de candidats. Seules les entrées de `SOURCES_VALIDES` pourront alimenter le rendu.

### Production de la newsletter — phase B

#### 3. Canon — Web désactivé

```text
PHASE CANON. N’utilise pas le Web. Recherche SNUM_CANON_V59_INDEX_START et SNUM_CANON_V59_INDEX_END dans les ressources du Projet, suis READ_NEXT et charge intégralement les fragments 06, 07, 08 et 09. Vérifie la paire d’index et les six paires de fragments START/END. Ne rends pas encore la newsletter. Réponds CANON_HTML_PRET avec la paire d’index, les six paires et leurs blocs html, ou CANON_HTML_INCOMPLET avec le jeton manquant.
```

Ne continuer que si la réponse contient `CANON_HTML_PRET`, `SNUM_CANON_V59_INDEX_START / SNUM_CANON_V59_INDEX_END` et les six paires :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_SHELL_TAIL_START / SNUM_SHELL_TAIL_END` ;
- `SNUM_ESSENTIAL_START / SNUM_ESSENTIAL_END` ;
- `SNUM_RUBRIC_START / SNUM_RUBRIC_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

#### 4. Rendu — Web désactivé

```text
PHASE RENDU.
N’utilise pas le Web.
Utilise exclusivement SOURCES_VALIDES et les fragments canoniques
chargés au tour précédent.
Ne recherche plus les ressources ni les jetons.
Utilise les blocs affichés dans la réponse CANON précédente.
Copie littéralement 06.
Insère les blocs 08 et 09 nécessaires.
Ajoute ensuite 07.
Remplace seulement les marqueurs @@.
Ne crée aucune balise ni classe absente des fragments.
Pour chaque source de SOURCES_VALIDES :
- crée exactement un article dans sa rubrique ;
- si elle est essentielle, ajoute aussi sa carte dans L’essentiel.
Une carte essentielle ne remplace jamais l’article de rubrique.
Avec moins de trois sources valides, ne crée ni section ni lien
L’essentiel.
À partir de trois sources valides, crée exactement trois cartes
essentielles.
Pour chaque lien href="#id" du menu de rubriques,
crée exactement une section id="id".
Chaque rubrique produite possède exactement un lien dans ce menu.
Livre exactement, dans cet ordre :
1. ## REVUE
2. ## HTML COMPLET, avec un unique bloc html allant de
   <!doctype html> à </html>
3. ## DOSSIER PRIVÉ
Avant affichage, vérifie :
- le title ;
- /revue-presse-snum/styles.css?v=20260917 ;
- l’absence de marqueur @@ ;
- chaque source valide dans sa rubrique ;
- chaque lien interne avec sa section cible ;
- fr-theme-modal ;
- les scripts DSFR 1.15.2.
Si un point n’est pas établi :
- commence ta réponse par A_COMPLETER ;
- n’affiche aucun code.
Ne pose aucune question.
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
- chaque source valide apparaît exactement une fois comme article dans sa rubrique ;
- un événement essentiel apparaît aussi dans sa rubrique ;
- avec moins de trois sources valides, la section et le lien `L’essentiel` sont absents ;
- à partir de trois sources valides, `L’essentiel` contient exactement trois cartes ;
- chaque lien `href="#id"` du menu possède exactement une section `id="id"` ;
- chaque rubrique produite possède exactement un lien dans le menu ;
- les rubriques et la navigation utilisent uniquement les libellés canoniques.

Si l’Assistant renvoie `A_COMPLETER`, le garde-fou a fonctionné. Ce résultat nécessite une reprise ou un contrôle extérieur ; il ne doit pas être présenté comme une édition prête.

## Recette du 15 octobre 2026

La V5.9 a été installée dans le Projet unique `Newsletter SNUM` avec un prompt système de 3 740 caractères et les huit fichiers attendus.

La première recette V5.9 a établi douze candidats après dix requêtes couvrant les cinq rubriques et plus de cinq domaines. La validation a conservé six sources et en a exclu six. Le premier rendu s’est arrêté parce qu’il recherchait de nouveau le jeton d’index, pourtant chargé au tour précédent.

Le contrat `CANON → RENDU` a été corrigé, réinstallé et rejoué dans une nouvelle conversation. La seconde collecte a produit onze candidats ; la validation en a conservé quatre et exclu sept. Après un unique réessai dû à une erreur technique de l’Assistant, `CANON` a confirmé la paire d’index et les six paires de fragments. `RENDU` a néanmoins répondu `A_COMPLETER` sans HTML.

Verdict : **NO-GO pour une livraison autonome garantissant un HTML identique à Bacoco**. Le garde-fou bloque désormais les sorties non établies, mais l’Assistant ne réussit pas encore l’assemblage final de façon fiable. Voir le [compte rendu V5.9](./_documentation/installation-v5.9-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md).

## Preuves de la recette du 14 octobre 2026

- [première conversation V5.9](https://assistant.numerique.gouv.fr/chat/ac926e61-2b8a-4d4e-bfc3-e5b8e0b5de82) ;
- [conversation V5.9 finale](https://assistant.numerique.gouv.fr/chat/68369f19-beff-4a6d-a3d6-80903fdacc60) ;
- [compte rendu V5.9](./_documentation/installation-v5.9-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;

- [conversation à deux phases : canon retrouvé, écarts éditoriaux](https://assistant.numerique.gouv.fr/chat/88b774da-c07b-4b78-a5bb-22739def300f) ;
- [conversation de durcissement : date corrigée après audit](https://assistant.numerique.gouv.fr/chat/066f718b-db2f-432c-a576-ec96104ebb57) ;
- [conversation en phases séparées : collecte et validation réussies, rendu arrêté proprement](https://assistant.numerique.gouv.fr/chat/4dddefda-e5da-4736-b4ca-9464e8b5c9dd) ;
- [compte rendu détaillé](./_documentation/validation-v5.8-progressive-2026-10-14/RESULTAT-RECETTE-PROGRESSIVE.md).

Une recette prouve seulement le cas exécuté. L’autoévaluation de l’Assistant ne remplace pas un validateur indépendant ni un audit RGAA.
