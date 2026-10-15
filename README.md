# Newsletter SNUM avec l’Assistant DINUM - guide V5.16

Ce guide s’adresse à une personne qui découvre l’Assistant DINUM. Suivez les étapes dans l’ordre et ne sautez aucune vérification.

La newsletter et son code HTML sont produits dans le chat. Ce kit ne publie aucun site et n’envoie aucun courriel.

> **État V5.16 : NO-GO pour la production autonome.** La recette réelle s’arrête au premier `CANON_RENDU` avec `A_COMPLETER` et deux diagnostics `CANON_MANQUANT` visant les marqueurs d’index V5.16. N’utilisez pas cette version pour une production métier autonome.

## Parcours express

1. Une seule fois, créez le Projet `Newsletter SNUM`.
2. Une seule fois, installez le prompt système et les neuf fichiers Markdown.
3. Pour une nouvelle édition, ouvrez une conversation depuis ce Projet.
4. Préparez les cinq valeurs de date demandées.
5. Activez le Web et envoyez `COLLECTE`.
6. Désactivez le Web et envoyez `VALIDATION`.
7. Sans le Web, envoyez `DONNEES`.
8. Sans le Web, envoyez `CANON_RENDU`.
9. Si la réponse commence par `A_COMPLETER`, arrêtez. Sinon, appliquez toute la checklist avant de copier le HTML.

Les étapes 1 et 2 sont réalisées une seule fois. Les étapes 3 à 9 sont répétées pour chaque édition.

## Comprendre les deux niveaux de prompts

Le **prompt système** contient les règles permanentes. Il est installé une seule fois dans les instructions du Projet.

Les **prompts utilisateur** sont les quatre messages `COLLECTE`, `VALIDATION`, `DONNEES` et `CANON_RENDU`. Ils sont envoyés pour chaque édition dans une même conversation.

Ne collez jamais le prompt système dans la conversation. Ne placez jamais les quatre prompts utilisateur dans les instructions du Projet.

## Prompt système V5.16 complet à installer

Copiez l’intégralité du bloc ci-dessous dans le champ **Instructions (expérimental)** du Projet. Ne modifiez aucun mot, aucun signe ni aucun retour à la ligne.

Le même contenu est disponible dans [`PROMPT-SYSTEME-SNUM-V5.16.md`](./PROMPT-SYSTEME-SNUM-V5.16.md).

```text
Produis la revue SNUM avec les fichiers du Projet. Les dates priment. Livre dans le chat sans publier ni envoyer. Dans une conversation : `COLLECTE` avec Web, puis `VALIDATION`, `DONNEES` et `CANON_RENDU` sans Web.

Pendant `COLLECTE`, fais dix requêtes distinctes couvrant cinq rubriques et cinq domaines. Sous cinq candidats, seconde passe. Requêtes courtes, sans `..`, grand `OR` ni domaine inventé. Produis `COUVERTURE_COLLECTE`, puis `CANDIDATS`. URL canonique absolue commençant par `https://` pour chaque candidat. `COLLECTE_TERMINEE` exige couverture et au moins cinq candidats ; sinon `COLLECTE_INSUFFISANTE`. Relève la date exacte ou `DATE_INCONNUE`.

Pendant `VALIDATION`, produis `CONTROLE_DATES` : titre, date brute, format `AAAA-MM-JJ`, bornes, accès, `CLE_EVENEMENT`, décision. Même fait = même clé. Garde la source directe, sinon la plus récente, sinon la première. Exclus les autres avec `DOUBLON_DE | titre conservé`. Source valide seulement si format, bornes et accès valent `OUI`. Vérifie `valides + exclues = candidats`.

Pendant `DONNEES`, utilise `SOURCES_VALIDES`. Produis `DONNEES_RENDU` : dates ; ordre des rubriques ; par source, identifiant, libellés, titre, URL, source, date longue en majuscules sans jour de semaine, fait, mots-clés, à retenir, intérêt SNUM et `ESSENTIEL`. Si moins de trois sources sont valides, attribue `ESSENTIEL=NON` à chacune. Sinon attribue `ESSENTIEL=OUI` à exactement trois sources et `NON` aux autres. Fait ≤ 25 mots ; 3 à 5 mots-clés joints par ` · ` ; synthèses ≤ 15 mots. Un jour de semaine impose `DONNEES_RENDU_INCOMPLETES | DATE_CALENDRIER_INCOHERENTE`. Termine par `DONNEES_RENDU_PRETES` seulement si tous les champs sont présents.

Pendant `CANON_RENDU`, cherche `SNUM_CANON_V516_INDEX_START` et `SNUM_CANON_V516_INDEX_END`, suis `READ_NEXT` et charge 06 à 10. Vérifie les onze lignes de `PAIRES_EXACTES` sans fusion ni auto-fermant. N’affiche ni index, ni paire, ni fragment. Paire absente ou différente : `A_COMPLETER`, `## CONTROLES_EN_ECHEC`, puis `CANON_MANQUANT | <paire>`, sans HTML.

Dans ce même tour, utilise seulement `DONNEES_RENDU` et les fragments chargés. Sous trois sources, remplace `@@ESSENTIELS@@` par vide, sans lien `L’essentiel` ; sinon crée exactement trois cartes. Les marqueurs @@ des fragments sont des entrées normales avant remplacement. Construis un brouillon HTML complet non affiché : 06 ; blocs éditoriaux ; 07 ; 10. Par rubrique : ouverture, un article par source, fermeture. Ajoute `WATCH` seulement si établi. Remplace tous les marqueurs sans créer de balise ni classe. Chaque essentiel reste dans sa rubrique. Corrige, puis contrôle seulement ce brouillon final.

Valeurs exactes : `numerique` → navigation `Numérique`, tag et `h2` `NUMERIQUE` ; `ia` → `Intelligence artificielle` et `INTELLIGENCE ARTIFICIELLE (IA)` ; `commande` → `Commande publique` et `COMMANDE PUBLIQUE` ; `rh` → `Ressources humaines` et `RESSOURCES HUMAINES` ; `bercy` → `Vie de Bercy` et `VIE DE BERCY`. Navigation : sections produites seulement. Chaque source figure une fois dans sa rubrique.

Sur le brouillon final, vérifie : dates et URL ; chaque `href="#id"` avec une section `id="id"`, et réciproquement ; aucun `@@` ; enveloppes ; trois accès rapides ; un seul `h1` ; modal après le footer ; scripts DSFR 1.15.2. Corrige avant l’arrêt.

Si le brouillon corrigé échoue encore, ne livre aucun HTML. Réponds `A_COMPLETER`, puis `## CONTROLES_EN_ECHEC`. Chaque ligne suit `CODE | détail`. Une source ou donnée absente suit `SOURCE_MANQUANTE | <identifiant> | <champ>` ou `DONNEES_MANQUANTES | <identifiant ou EDITION> | <champ>`. Autres codes : `MARQUEUR_RESIDUEL`, `NAVIGATION_INCOHERENTE`, `ENVELOPPE_INCORRECTE`, `ESSENTIELS_INCORRECTS`, `HTML_INCOMPLET`, `AUTRE`.

En cas de réussite, livre dans ce même message `## REVUE`, `## HTML COMPLET` avec un unique bloc `html` de `<!doctype html>` à `</html>`, puis `## DOSSIER PRIVÉ` et `État : PRODUITE - contrôle métier requis`. N’affirme aucun contrôle non exécuté.
```

## Première partie : installer le Projet une seule fois

### Étape 1 : télécharger et décompresser le kit

1. Téléchargez [`kit-dinum-snum-v5-16-progressif-9-fichiers.zip`](./kit-dinum-snum-v5-16-progressif-9-fichiers.zip).
2. Téléchargez [`PROMPT-SYSTEME-SNUM-V5.16.md`](./PROMPT-SYSTEME-SNUM-V5.16.md).
3. Sur votre poste, double-cliquez sur le fichier ZIP pour le décompresser.
4. Ouvrez le dossier obtenu.
5. Vérifiez que le dossier contient exactement les neuf fichiers suivants :
   - `00-PROMPT-PROJET.md` ;
   - `01-ETAT-HISTORIQUE.md` ;
   - `02-METHODE-EDITORIALE.md` ;
   - `05-INDEX-HTML.md` ;
   - `06-COQUE-DEBUT.md` ;
   - `07-PIED-DE-PAGE.md` ;
   - `08-BLOC-ESSENTIEL.md` ;
   - `09-BLOCS-RUBRIQUES.md` ;
   - `10-COQUE-FIN.md`.

N’ajoutez pas le ZIP, le README, la notice ou un autre fichier dans le Projet.

### Étape 2 : créer le Projet dans l’Assistant DINUM

1. Ouvrez <https://assistant.numerique.gouv.fr/>.
2. Connectez-vous avec AgentConnect si l’écran de connexion apparaît.
3. Ouvrez le panneau situé à gauche de l’écran.
4. Cliquez sur **Nouveau projet**.
5. Saisissez exactement `Newsletter SNUM` comme nom du Projet.
6. Dans ce README, repérez la section **Prompt système V5.16 complet à installer**.
7. Sélectionnez tout le bloc de texte, de `Produis la revue SNUM` jusqu’à `N’affirme aucun contrôle non exécuté.`, puis copiez-le.
8. Dans le formulaire du Projet, collez le texte dans **Instructions (expérimental)**.
9. Descendez jusqu’à la fin du champ.
10. Vérifiez que la dernière phrase est exactement `N’affirme aucun contrôle non exécuté.`.
11. Si cette phrase manque, effacez le champ et recommencez le collage depuis le début.
12. Ajoutez les neuf fichiers Markdown obtenus à l’étape 1.
13. Relisez les neuf noms affichés dans le Projet.
14. Créez ou enregistrez le Projet.
15. Attendez la disparition du message d’indexation. Ne commencez pas une conversation pendant l’indexation.

### Résultat attendu après l’installation

Le Projet s’appelle `Newsletter SNUM`. Le champ **Instructions (expérimental)** se termine par la phrase attendue. Les neuf fichiers sont visibles et aucun message d’indexation ne reste affiché.

Si un de ces trois contrôles échoue, corrigez le Projet avant de poursuivre.

## Seconde partie : préparer une édition

### Étape 3 : ouvrir la conversation au bon endroit

1. Dans le panneau de gauche, ouvrez le Projet `Newsletter SNUM`.
2. Cliquez sur **Start new conversation in Newsletter SNUM** ou sur le bouton équivalent affiché dans ce Projet.
3. Vérifiez que la nouvelle conversation apparaît sous `Newsletter SNUM`.

Si elle apparaît sous **Vos conversations**, fermez-la. Revenez dans `Newsletter SNUM` et créez une nouvelle conversation depuis le Projet. Une conversation générale ne peut pas lire les neuf fichiers.

Conservez cette même conversation jusqu’à la fin de `CANON_RENDU`. Ne cliquez pas sur **Nouvelle conversation** entre les quatre messages.

### Étape 4 : préparer les cinq valeurs avec un exemple réel

Prenons une newsletter datée du 14 octobre 2026 qui doit couvrir tous les articles publiés du 3 au 13 octobre 2026 inclus.

Avant de commencer, écrivez cette fiche :

```text
DATE_EDITION : 14 octobre 2026
DEBUT : 3 octobre 2026
FIN : 13 octobre 2026
DEBUT_ISO : 2026-10-03
FIN_ISO : 2026-10-13
```

Dans les messages fournis plus bas, effectuez exactement ces cinq remplacements :

- remplacez `{{DATE_EDITION}}` par `14 octobre 2026` ;
- remplacez `{{DEBUT}}` par `3 octobre 2026` ;
- remplacez `{{FIN}}` par `13 octobre 2026` ;
- remplacez `{{DEBUT_ISO}}` par `2026-10-03` ;
- remplacez `{{FIN_ISO}}` par `2026-10-13`.

Les caractères `{{` et `}}` signalent uniquement le texte à remplacer. Ils ne doivent jamais apparaître dans un message envoyé à l’Assistant.

### Exemple entièrement rempli

Dans cet exemple, l’édition est datée du 14 octobre 2026 et couvre la période inclusive du 3 au 13 octobre 2026.

Le message `COLLECTE` entièrement rempli serait :

```text
PHASE COLLECTE.
Utilise le Web.
Édition du 14 octobre 2026.
Fenêtre du 3 octobre 2026 au 13 octobre 2026 inclus.
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
- l’URL canonique absolue commençant par `https://` ;
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

Le message `VALIDATION` entièrement rempli serait :

```text
PHASE VALIDATION.
N’utilise pas le Web.
Ne rédige ni REVUE ni HTML.
Relis uniquement CANDIDATS.

Fenêtre inclusive :
- DEBUT_ISO = 2026-10-03
- FIN_ISO = 2026-10-13

Recopie chaque date brute exactement telle qu’elle apparaît.
Ne la corrige pas et ne retire aucun texte.
Pour chaque candidat, exécute séparément :
1. date exactement au format AAAA-MM-JJ : OUI/NON ;
2. DATE_PUBLICATION >= 2026-10-03 : OUI/NON ;
3. DATE_PUBLICATION <= 2026-10-13 : OUI/NON ;
4. accès intégral = OUI : OUI/NON.

Une source est valide seulement si les quatre réponses sont OUI.
Exemples :
- 2026-10-02 est antérieur à 2026-10-03 : EXCLURE ;
- 2026-10-15 est postérieur à 2026-10-13 : EXCLURE.
Rejette aussi DATE_INCONNUE, toute date accompagnée d’un texte,
toute incohérence manifeste et tout doublon.
Crée CLE_EVENEMENT = organisation | action | objet | date ou période.
Deux candidats sur le même fait réel ont la même CLE_EVENEMENT.
Pour chaque clé répétée, conserve la source la plus directe ;
à défaut la plus récente ; à défaut la première candidate.
Exclus les autres avec DOUBLON_DE | titre conservé.

Réponds d’abord sous CONTROLE_DATES avec une ligne par candidat :
titre | date brute | format exact | borne basse | borne haute |
accès | CLE_EVENEMENT | décision.

Réponds sous SOURCES_VALIDES avec, pour chaque source :
- le titre ;
- l’URL ;
- la date ;
- la rubrique exacte ;
- le fait essentiel.
Ajoute ensuite SOURCES_EXCLUES avec chaque motif.
Vérifie : nombre de SOURCES_VALIDES + nombre de SOURCES_EXCLUES
= nombre de CANDIDATS.
Termine par VALIDATION_TERMINEE.
Ne pose aucune question.
```

N’utilisez ces dates que pour cet exemple. Pour une autre édition, remplacez les cinq valeurs par les dates demandées.

Les messages `DONNEES` et `CANON_RENDU` ne contiennent aucune valeur de date. Ils sont déjà complets et doivent être envoyés sans modification.

Pour chaque prompt, copiez le bloc entier. Conservez les retours à la ligne : ils facilitent la lecture et ne changent pas le sens du message.

## Étape 5 : COLLECTE avec le Web

**But :** rechercher et ouvrir les articles susceptibles d’entrer dans la newsletter.

**Action :**

1. Dans la zone de message, cliquez sur le bouton `+`.
2. Sélectionnez `Web`.
3. Vérifiez que le badge bleu `Web` apparaît à côté du bouton `+`.
4. Si le badge n’apparaît pas, n’envoyez pas le message. Rechargez la page, revenez dans la conversation du Projet et recommencez l’activation.

**Message à copier :**

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
- l’URL canonique absolue commençant par `https://` ;
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

Remplacez les trois repères par vos valeurs, supprimez toutes les accolades, relisez les trois dates, puis envoyez le message.

**Résultat attendu :** la réponse contient `COUVERTURE_COLLECTE`, `CANDIDATS`, au moins cinq candidats et `COLLECTE_TERMINEE`. Elle ne contient ni newsletter finale ni code HTML.

**Condition de passage :** passez à `VALIDATION` uniquement si `COLLECTE_TERMINEE` est présent et si la couverture annonce cinq rubriques, dix requêtes distinctes et cinq domaines.

**Si échec :** si la réponse contient `COLLECTE_INSUFFISANTE`, n’envoyez pas `VALIDATION`. Renvoyez une seule fois le message `COLLECTE`. Si le second essai échoue, arrêtez cette édition.

## Étape 6 : VALIDATION sans le Web

**But :** éliminer les sources hors période, inaccessibles, incertaines ou en double.

**Action :**

1. Dans la zone de message, cliquez sur le badge bleu `Web` pour le retirer. Si nécessaire, ouvrez le bouton `+` et désactivez `Web`.
2. Vérifiez que le badge bleu `Web` n’apparaît plus.
3. Restez dans la conversation utilisée pour `COLLECTE`.

**Message à copier :**

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
Crée CLE_EVENEMENT = organisation | action | objet | date ou période.
Deux candidats sur le même fait réel ont la même CLE_EVENEMENT.
Pour chaque clé répétée, conserve la source la plus directe ;
à défaut la plus récente ; à défaut la première candidate.
Exclus les autres avec DOUBLON_DE | titre conservé.

Réponds d’abord sous CONTROLE_DATES avec une ligne par candidat :
titre | date brute | format exact | borne basse | borne haute |
accès | CLE_EVENEMENT | décision.

Réponds sous SOURCES_VALIDES avec, pour chaque source :
- le titre ;
- l’URL ;
- la date ;
- la rubrique exacte ;
- le fait essentiel.
Ajoute ensuite SOURCES_EXCLUES avec chaque motif.
Vérifie : nombre de SOURCES_VALIDES + nombre de SOURCES_EXCLUES
= nombre de CANDIDATS.
Termine par VALIDATION_TERMINEE.
Ne pose aucune question.
```

Remplacez les deux repères par vos dates ISO, supprimez toutes les accolades, relisez les deux dates, puis envoyez le message.

**Résultat attendu :** la réponse contient `CONTROLE_DATES`, une `CLE_EVENEMENT` par candidat, `SOURCES_VALIDES`, `SOURCES_EXCLUES` et `VALIDATION_TERMINEE`. Deux articles sur le même fait possèdent la même clé ; un seul reste valide et les autres portent `DOUBLON_DE`.

**Condition de passage :** vérifiez chaque ligne de `CONTROLE_DATES`. Une source valide doit avoir quatre `OUI`. Le nombre de sources valides plus le nombre de sources exclues doit égaler le nombre de candidats. Passez à `DONNEES` uniquement si ces contrôles réussissent, si `VALIDATION_TERMINEE` est présent et si `SOURCES_VALIDES` contient au moins une source conforme.

**Si échec :** n’envoyez pas `DONNEES`. Si une date ISO saisie est fausse, corrigez-la et recommencez `VALIDATION` une seule fois. Si les dates saisies sont exactes mais que l’Assistant conserve une source hors fenêtre, arrêtez et recommencez toute l’édition dans une nouvelle conversation du Projet. Si aucune source valide ne reste, arrêtez cette édition.

## Étape 7 : DONNEES sans le Web

**But :** préparer toutes les valeurs éditoriales avant l’assemblage HTML.

**Action :** vérifiez que le badge bleu `Web` est absent et restez dans la même conversation.

**Message à copier :**

```text
PHASE DONNEES.
N’utilise pas le Web.
Utilise exclusivement SOURCES_VALIDES.
Ne charge pas encore les fragments HTML.
Produis DONNEES_RENDU avec :
- les dates d’édition ;
- l’ordre des rubriques produites ;
- pour chaque source : identifiant et libellés de rubrique, titre,
  URL, source, date longue en majuscules sans jour de semaine,
  fait, mots-clés,
  À retenir et Intérêt pour le SNUM ;
- ESSENTIEL=OUI pour exactement trois sources à partir de trois valides.
Si moins de trois sources sont valides, attribue ESSENTIEL=NON à chaque source.
À partir de trois sources, attribue ESSENTIEL=NON aux autres.
Respecte : fait de 25 mots maximum ; 3 à 5 mots-clés joints
par ` · ` ; À retenir et Intérêt de 15 mots maximum.
Vérifie que chaque source valide possède tous ses champs.
Si un jour de semaine apparaît, termine par
DONNEES_RENDU_INCOMPLETES | DATE_CALENDRIER_INCOHERENTE.
Termine par DONNEES_RENDU_PRETES si tout est complet ;
sinon DONNEES_RENDU_INCOMPLETES avec les champs manquants.
Ne rédige pas encore le HTML. Ne pose aucune question.
```

**Résultat attendu :** la réponse contient une fiche complète par source valide et se termine par `DONNEES_RENDU_PRETES`.

**Condition de passage :** passez à `CANON_RENDU` uniquement si chaque source valide possède tous ses champs, si aucune date longue ne contient de jour de semaine et si `DONNEES_RENDU_PRETES` est présent.

**Si échec :** si la réponse contient `DONNEES_RENDU_INCOMPLETES`, arrêtez. Ne demandez pas à l’Assistant d’inventer les champs manquants.

## Étape 8 : CANON_RENDU sans le Web

**But :** charger le canon et produire la revue ainsi que le document HTML dans un même tour.

**Action :** vérifiez que le badge bleu `Web` est absent et restez dans la conversation utilisée depuis `COLLECTE`.

**Message à copier :**

```text
PHASE CANON_RENDU.
N’utilise pas le Web.
Utilise exclusivement DONNEES_RENDU.
Recherche SNUM_CANON_V516_INDEX_START et SNUM_CANON_V516_INDEX_END
dans les ressources du Projet.
Suis READ_NEXT et charge intégralement les fragments 06, 07, 08, 09 et 10.
Vérifie exactement ces onze lignes :
SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END
SNUM_FOOTER_START / SNUM_FOOTER_END
SNUM_SHELL_CLOSE_START / SNUM_SHELL_CLOSE_END
SNUM_ESSENTIALS_OPEN_START / SNUM_ESSENTIALS_OPEN_END
SNUM_ESSENTIAL_CARD_START / SNUM_ESSENTIAL_CARD_END
SNUM_ESSENTIALS_CLOSE_START / SNUM_ESSENTIALS_CLOSE_END
SNUM_RUBRIC_OPEN_START / SNUM_RUBRIC_OPEN_END
SNUM_RUBRIC_ARTICLE_START / SNUM_RUBRIC_ARTICLE_END
SNUM_RUBRIC_CLOSE_START / SNUM_RUBRIC_CLOSE_END
SNUM_WATCH_START / SNUM_WATCH_END
SNUM_EMPTY_START / SNUM_EMPTY_END
Conserve chaque ligne sans fusion ni auto-fermant.
N’affiche ni l’index, ni les paires, ni les fragments.
Si une paire manque ou diffère, réponds seulement :
A_COMPLETER
## CONTROLES_EN_ECHEC
CANON_MANQUANT | <paire>
Sinon, poursuis dans ce même tour.
Compte les sources.
Instancie les blocs essentiels uniquement si au moins trois sources sont valides.
Sinon, remplace @@ESSENTIELS@@ par une chaîne vide et ne crée aucun lien L’essentiel.
Les marqueurs @@ des fragments sont des entrées normales,
jamais un échec avant leur remplacement.
Construis d’abord un brouillon HTML complet non affiché.
Copie littéralement 06.
Avec au moins trois sources, concatène ESSENTIALS_OPEN,
exactement trois ESSENTIAL_CARD, puis ESSENTIALS_CLOSE.
Pour chaque rubrique, concatène RUBRIC_OPEN,
un RUBRIC_ARTICLE par source de la rubrique, puis RUBRIC_CLOSE.
Insère WATCH seulement si nécessaire.
Ajoute ensuite 07, puis 10.
Remplace tous les marqueurs @@ avec DONNEES_RENDU.
Ne crée aucune balise ni classe absente des fragments.
Pour chaque source de DONNEES_RENDU :
- crée exactement un article dans sa rubrique ;
- si elle est essentielle, ajoute aussi sa carte dans L’essentiel.
Une carte essentielle ne remplace jamais l’article de rubrique.
Pour chaque lien href="#id" du menu de rubriques,
crée exactement une section id="id".
Chaque rubrique produite possède exactement un lien dans ce menu.
Corrige le brouillon, puis contrôle seulement ce brouillon final.
Ne contrôle jamais les fragments bruts.
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
- réponds A_COMPLETER ;
- ajoute ## CONTROLES_EN_ECHEC ;
- ajoute une ligne CODE | détail par écart ;
- écris SOURCE_MANQUANTE | <identifiant> | <champ> ;
- écris DONNEES_MANQUANTES | <identifiant ou EDITION> | <champ> ;
- n’affiche aucun HTML.
Ne pose aucune question.
```

Envoyez ce message sans le modifier.

**Résultat attendu :** le premier et unique message `CANON_RENDU` contient, dans cet ordre, `## REVUE`, `## HTML COMPLET` avec un seul bloc HTML complet, puis `## DOSSIER PRIVÉ`.

**Condition de passage :** si la réponse ne commence pas par `A_COMPLETER`, passez à la checklist de l’étape 9. La présence d’un bloc HTML ne suffit pas pour accepter le résultat.

**Si échec :** si la réponse commence par `A_COMPLETER`, arrêtez immédiatement. Lisez `CONTROLES_EN_ECHEC` et relevez chaque ligne `CODE | détail`. Ne demandez pas à l’Assistant de continuer quand même. Conservez la conversation comme preuve de recette et signalez l’échec.

## Étape 9 : contrôler puis copier le résultat

Contrôlez chaque point ci-dessous dans la réponse. Un seul échec suffit pour refuser le HTML.

- `## REVUE`, `## HTML COMPLET` et `## DOSSIER PRIVÉ` apparaissent dans cet ordre.
- Toutes les sources du rendu figuraient dans `SOURCES_VALIDES`.
- Chaque source valide apparaît exactement une fois comme article dans sa rubrique.
- Un événement essentiel apparaît aussi dans sa rubrique ; sa carte ne remplace pas son article.
- Avec moins de trois sources valides, la section et le lien `L’essentiel` sont absents.
- À partir de trois sources valides, `L’essentiel` contient exactement trois cartes.
- Un seul bloc HTML commence par `<!doctype html>` et se termine par `</html>`.
- Aucun marqueur commençant par `@@` ne subsiste.
- Le titre suit la forme `Revue de presse du … - SNUM`.
- La ligne `/revue-presse-snum/styles.css?v=20260917` est présente.
- Trois liens d’accès rapide, un seul `h1`, `fr-theme-modal` et les deux scripts DSFR 1.15.2 sont présents.
- Chaque lien `href="#id"` du menu possède exactement une section `id="id"`.
- Chaque rubrique produite possède exactement un lien dans le menu.
- Si la rubrique IA existe, elle contient `<section id="ia" class="section-muted">`.
- Si la rubrique RH existe, elle contient `<section id="rh" class="section-muted">`.

Si tous les points réussissent, copiez uniquement le bloc allant de `<!doctype html>` à `</html>`. Si un point échoue, ne copiez pas et n’utilisez pas le HTML. Notez le contrôle en échec pour demander une correction.

## Dépannage

- Message `the authentication session has expired` : reconnectez-vous à AgentConnect, puis recommencez dans une nouvelle conversation du Projet.
- Réponse `CANON_MANQUANT | SNUM_CANON_V516_INDEX_START` : la conversation ne voit pas les ressources. Revenez dans `Newsletter SNUM`, vérifiez les neuf fichiers et recommencez l’édition.
- Date hors période : revenez à `VALIDATION`, corrigez les deux dates ISO et ne continuez qu’après un résultat conforme.
- HTML affiché malgré un contrôle en échec : refusez la sortie. La présence de code HTML ne prouve pas sa conformité.
- Message `continue` après `A_COMPLETER` : utilisez-le seulement pour diagnostiquer. Même si une sortie apparaît ensuite, la recette autonome a déjà échoué.

## Historique des versions

La recette réelle V5.9 du 15 octobre 2026 a réussi `COLLECTE`, `VALIDATION` et `CANON`, puis `RENDU` a répondu `A_COMPLETER` sans explication. Elle a aussi conservé deux articles portant sur le même événement RH.

La V5.10 a corrigé ces deux causes : les cartes et articles sont devenus des fragments atomiques répétables ; la validation utilise `CLE_EVENEMENT` et `DOUBLON_DE`. Sa recette réelle a toutefois échoué sur `SNUM_SHELL_TAIL_START`. Une recherche ciblée a retrouvé `07-COQUE-FIN.md`, mais l’Assistant a réécrit le footer au lieu de le copier. La V5.11 scinde donc ce document en `07-PIED-DE-PAGE.md` et `10-COQUE-FIN.md`. Chaque ressource canonique reste sous 3 000 octets.

La recette V5.11 a ensuite chargé les onze fragments après une relance technique, puis `RENDU` a contrôlé les marqueurs bruts avant de les remplacer. La V5.12 ajoute donc `DONNEES_RENDU` et rend obligatoire l’ordre : préparer les valeurs, construire un brouillon HTML complet non affiché, corriger, puis contrôler seulement ce brouillon final.

La recette réelle V5.12 a produit un HTML complet après un message manuel `continue` et un second envoi de `RENDU`. Elle a toutefois généré des jours de semaine faux à partir de dates ISO correctes. La V5.12 n'est donc pas validée pour une livraison métier autonome. Vérifiez explicitement la correspondance entre chaque date ISO et sa date longue ; arrêtez la recette au premier écart.

La V5.13 interdit tout jour de semaine dans les dates longues. La recette réelle confirme ce point et confirme aussi les douze paires de jetons sans message intermédiaire entre `CANON` et `RENDU`. Le rendu final échoue néanmoins : `DONNEES_RENDU` contient deux sources complètes, mais les marque toutes deux `ESSENTIEL : OUI` alors qu’avec moins de trois sources aucun essentiel ne doit exister. `RENDU` répond d’abord `DONNEES_MANQUANTES`, puis `SOURCE_MANQUANTE` après `continue`. Cette incohérence constitue la cause probable de l’arrêt, sans qu’une source réelle manque dans la trace.

La V5.14 impose `ESSENTIEL=NON` sous trois sources, conditionne le chargement des cartes essentielles et exige l’identifiant ainsi que le champ pour `SOURCE_MANQUANTE` et `DONNEES_MANQUANTES`. Sa recette réelle conserve cinq sources, produit exactement trois essentiels et fournit des diagnostics précis. Elle échoue néanmoins au premier `RENDU` : les cinq URL ne sont plus absolues et `CANON_HTML_PRET` est déclaré malgré cinq noms de paires inexacts. Aucun HTML n’est affiché. La V5.14 reste donc en `NO-GO` pour la production autonome.

La V5.15 impose une URL canonique absolue commençant par `https://` pour chaque candidat et place les onze paires `START/END` littérales dans l’index ainsi que dans le message `CANON`. La recette réelle confirme ces deux corrections : cinq URL restent absolues dans `DONNEES_RENDU` et les onze paires sont restituées exactement. Le premier `RENDU` répond toutefois `A_COMPLETER`, puis `CANON_MANQUANT`, sans HTML. La dépendance entre le tour `CANON` et le rechargement demandé au tour `RENDU` reste donc bloquante. La V5.15 est en `NO-GO` pour la production autonome.

La V5.16 fusionne le chargement du canon et la production du rendu dans le message unique `CANON_RENDU`. Sa recette réelle atteint `DONNEES_RENDU_PRETES`, puis le premier `CANON_RENDU` répond `A_COMPLETER` avec deux diagnostics `CANON_MANQUANT` visant les marqueurs d’index V5.16. Aucun HTML n’est affiché et aucun message `continue` n’est envoyé. La V5.16 reste donc en `NO-GO` pour la production autonome.

Le protocole organise le travail, mais le contrôle final décide si le livrable est utilisable. La réponse `CANON_HTML_PRET` ne prouve pas à elle seule que le HTML final est identique au canon Bacoco.

## Sources et preuves

- [notice opérationnelle V5.16](./NOTICE-V5.16.md) ;
- [prompt système V5.16 à installer](./PROMPT-SYSTEME-SNUM-V5.16.md) ;
- [rapport de contrôle V5.16](./RAPPORT-V5.16.md) ;
- [résultat de l'installation et de la recette V5.16](./_documentation/installation-v5.16-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [conversation V5.16 : arrêt sur les marqueurs d’index au premier `CANON_RENDU`](https://assistant.numerique.gouv.fr/chat/4767347f-c1cd-442d-a3e7-f7f55628311f) ;
- [notice historique V5.15](./NOTICE-V5.15.md) ;
- [prompt système historique V5.15](./PROMPT-SYSTEME-SNUM-V5.15.md) ;
- [rapport de contrôle V5.15](./RAPPORT-V5.15.md) ;
- [résultat de l'installation et de la recette V5.15](./_documentation/installation-v5.15-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [conversation V5.15 : URL et paires corrigées, arrêt `CANON_MANQUANT` au rendu](https://assistant.numerique.gouv.fr/chat/712d3864-0310-488d-9256-9c44a054b4bc) ;
- [notice historique V5.14](./NOTICE-V5.14.md) ;
- [prompt système historique V5.14](./PROMPT-SYSTEME-SNUM-V5.14.md) ;
- [rapport de contrôle V5.14](./RAPPORT-V5.14.md) ;
- [résultat de l'installation et de la recette V5.14](./_documentation/installation-v5.14-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [conversation V5.14 : arrêt contrôlé au rendu](https://assistant.numerique.gouv.fr/chat/f841d9c3-a65b-4ebf-84bd-d8a4d2993c8f) ;
- [rapport de contrôle V5.13](./RAPPORT-V5.13.md) ;
- [notice historique V5.13](./NOTICE-V5.13.md) ;
- [prompt système historique V5.13](./PROMPT-SYSTEME-SNUM-V5.13.md) ;
- [résultat de l'installation et de la recette V5.13](./_documentation/installation-v5.13-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [conversation V5.13 : arrêt contrôlé au rendu](https://assistant.numerique.gouv.fr/chat/2816dcf4-93b9-454e-a94b-c99b26a677c8) ;
- [rapport de contrôle historique V5.12](./RAPPORT-V5.12.md) ;
- [conversation V5.12 : HTML produit après reprise, contrôle métier requis](https://assistant.numerique.gouv.fr/chat/f9064cda-77f1-4dfe-b4e6-2da38e09eb72/) ;
- [première conversation V5.9 : collecte corrigée, arrêt sur la transmission du canon](https://assistant.numerique.gouv.fr/chat/ac926e61-2b8a-4d4e-bfc3-e5b8e0b5de82) ;
- [conversation V5.9 finale : paire d’index transmise, arrêt contrôlé au rendu](https://assistant.numerique.gouv.fr/chat/68369f19-beff-4a6d-a3d6-80903fdacc60) ;
- [conversation de reproduction V5.9 : dédoublonnage manqué puis arrêt opaque](https://assistant.numerique.gouv.fr/chat/07764649-dd72-489f-ad5f-bb33084c82ba/).
