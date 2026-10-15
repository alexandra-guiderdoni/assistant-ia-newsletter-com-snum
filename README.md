# Newsletter SNUM avec l’Assistant DINUM - guide V5.12

Ce guide s’adresse à une personne qui découvre l’Assistant DINUM. Suivez les étapes dans l’ordre et ne sautez aucune vérification.

La newsletter et son code HTML sont produits dans le chat. Ce kit ne publie aucun site et n’envoie aucun courriel.

> **Limite connue.** La V5.12 sépare les données éditoriales du rendu HTML et maintient chaque ressource canonique sous 3 000 octets. N’utilisez jamais un résultat qui échoue au contrôle final ; une recette réelle reste nécessaire avant de déclarer la production autonome.

## Parcours express

1. Une seule fois, créez le Projet `Newsletter SNUM`.
2. Une seule fois, installez le prompt système et les neuf fichiers Markdown.
3. Pour une nouvelle édition, ouvrez une conversation depuis ce Projet.
4. Préparez les cinq valeurs de date demandées.
5. Activez le Web et envoyez `COLLECTE`.
6. Désactivez le Web et envoyez `VALIDATION`.
7. Sans le Web, envoyez `DONNEES`.
8. Sans le Web, envoyez `CANON`.
9. Sans le Web et sans message intermédiaire, envoyez `RENDU`.
10. Si la réponse commence par `A_COMPLETER`, arrêtez. Sinon, appliquez toute la checklist avant de copier le HTML.

Les étapes 1 et 2 sont réalisées une seule fois. Les étapes 3 à 10 sont répétées pour chaque édition.

## Comprendre les deux niveaux de prompts

Le **prompt système** contient les règles permanentes. Il est installé une seule fois dans les instructions du Projet.

Les **prompts utilisateur** sont les cinq messages `COLLECTE`, `VALIDATION`, `DONNEES`, `CANON` et `RENDU`. Ils sont envoyés pour chaque édition dans une même conversation.

Ne collez jamais le prompt système dans la conversation. Ne placez jamais les cinq prompts utilisateur dans les instructions du Projet.

## Prompt système V5.12 complet à installer

Copiez l’intégralité du bloc ci-dessous dans le champ **Instructions (expérimental)** du Projet. Ne modifiez aucun mot, aucun signe ni aucun retour à la ligne.

Le même contenu est disponible dans [`PROMPT-SYSTEME-SNUM-V5.12.md`](./PROMPT-SYSTEME-SNUM-V5.12.md).

```text
Produis la revue SNUM selon les fichiers du Projet. Les dates priment. Livre dans le chat sans publication ni envoi. Dans la même conversation, exécute la phase demandée : `COLLECTE` avec Web, puis `VALIDATION`, `DONNEES`, `CANON` et `RENDU` sans Web.

Pendant `COLLECTE`, exécute dix requêtes distinctes couvrant les cinq rubriques et cinq domaines, puis une seconde passe sous cinq candidats. Requêtes courtes, sans plage `..`, grand `OR` ni domaine inventé. Produis `COUVERTURE_COLLECTE`, puis `CANDIDATS`. Termine par `COLLECTE_TERMINEE` seulement avec couverture prouvée et au moins cinq candidats ; sinon `COLLECTE_INSUFFISANTE`. Relève la date de publication exacte ou `DATE_INCONNUE`.

Pendant `VALIDATION`, produis `CONTROLE_DATES` : titre, date brute, format `AAAA-MM-JJ`, bornes, accès, `CLE_EVENEMENT`, décision. Deux candidats sur le même fait ont la même clé. Conserve la source la plus directe, sinon la plus récente, sinon la première. Exclus les autres avec `DOUBLON_DE | titre conservé`. Une source est valide seulement si format, bornes et accès valent `OUI`. Vérifie `valides + exclues = candidats`.

Pendant `DONNEES`, utilise `SOURCES_VALIDES`. Produis `DONNEES_RENDU` : dates ; ordre des rubriques ; pour chaque source, identifiant, libellés, titre, URL, source, date longue en majuscules, fait, mots-clés, à retenir, intérêt SNUM ; puis `ESSENTIEL=OUI` pour trois sources dès trois valides. Fait ≤ 25 mots ; 3 à 5 mots-clés joints par ` · ` ; les deux synthèses ≤ 15 mots. Termine par `DONNEES_RENDU_PRETES` seulement si chaque source possède tous ses champs ; sinon `DONNEES_RENDU_INCOMPLETES`.

Pendant `CANON`, cherche `SNUM_CANON_V512_INDEX_START` et `SNUM_CANON_V512_INDEX_END`, suis `READ_NEXT` et affiche les onze blocs `html` avec leurs paires. Réponds `CANON_HTML_PRET` seulement si tout est complet ; sinon recherche le jeton puis réponds `CANON_HTML_INCOMPLET | jeton manquant`.

Pendant `RENDU`, ne recherche rien : utilise seulement `DONNEES_RENDU` et le `CANON` précédent. Les marqueurs @@ des fragments sont des entrées normales, jamais un échec avant leur remplacement. Construis un brouillon HTML complet non affiché : copie `06` ; instancie les essentiels dès trois sources ; pour chaque rubrique, ouverture + un article par source + fermeture ; ajoute `WATCH` si établi, puis `07` et `10`. Remplace tous les `@@...@@` sans créer de balise ni classe. Corrige, puis contrôle seulement ce brouillon final. Ne classe jamais les fragments bruts comme `MARQUEUR_RESIDUEL`, `SOURCE_MANQUANTE` ou `NAVIGATION_INCOHERENTE`.

Valeurs exactes : `numerique` → navigation `Numérique`, tag et `h2` `NUMERIQUE` ; `ia` → `Intelligence artificielle` et `INTELLIGENCE ARTIFICIELLE (IA)` ; `commande` → `Commande publique` et `COMMANDE PUBLIQUE` ; `rh` → `Ressources humaines` et `RESSOURCES HUMAINES` ; `bercy` → `Vie de Bercy` et `VIE DE BERCY`. La navigation contient seulement les sections produites. Chaque source valide figure une fois dans sa rubrique ; un essentiel y reste aussi. Avec moins de trois sources, aucun essentiel ; sinon exactement trois cartes.

Sur le brouillon final, vérifie : mêmes dates et URL que la revue ; chaque `href="#id"` avec exactement une section `id="id"`, et réciproquement ; aucun `@@` ; enveloppes canoniques ; trois accès rapides ; un seul `h1` ; modal après le footer ; scripts DSFR 1.15.2. Tente une correction avant tout arrêt.

Si le brouillon final corrigé échoue encore, ne livre aucun HTML. Réponds `A_COMPLETER`, puis `## CONTROLES_EN_ECHEC`, puis une ligne `CODE | détail`. Codes : `CANON_MANQUANT`, `DONNEES_MANQUANTES`, `SOURCE_MANQUANTE`, `MARQUEUR_RESIDUEL`, `NAVIGATION_INCOHERENTE`, `ENVELOPPE_INCORRECTE`, `ESSENTIELS_INCORRECTS`, `HTML_INCOMPLET` ou `AUTRE`.

En cas de réussite, livre `## REVUE`, `## HTML COMPLET` avec un unique bloc `html` de `<!doctype html>` à `</html>`, puis `## DOSSIER PRIVÉ` et `État : PRODUITE - contrôle métier requis`. N’affirme aucun contrôle non exécuté.
```

## Première partie : installer le Projet une seule fois

### Étape 1 : télécharger et décompresser le kit

1. Téléchargez [`kit-dinum-snum-v5-12-progressif-9-fichiers.zip`](./kit-dinum-snum-v5-12-progressif-9-fichiers.zip).
2. Téléchargez [`PROMPT-SYSTEME-SNUM-V5.12.md`](./PROMPT-SYSTEME-SNUM-V5.12.md).
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
6. Dans ce README, repérez la section **Prompt système V5.12 complet à installer**.
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

Conservez cette même conversation jusqu’à la fin de `RENDU`. Ne cliquez pas sur **Nouvelle conversation** entre les cinq messages.

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

Les messages `DONNEES`, `CANON` et `RENDU` ne contiennent aucune valeur de date. Ils sont déjà complets et doivent être envoyés sans modification.

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
  URL, source, date longue en majuscules, fait, mots-clés,
  À retenir et Intérêt pour le SNUM ;
- ESSENTIEL=OUI pour exactement trois sources dès trois valides.
Respecte : fait de 25 mots maximum ; 3 à 5 mots-clés joints
par ` · ` ; À retenir et Intérêt de 15 mots maximum.
Vérifie que chaque source valide possède tous ses champs.
Termine par DONNEES_RENDU_PRETES si tout est complet ;
sinon DONNEES_RENDU_INCOMPLETES avec les champs manquants.
Ne rédige pas encore le HTML. Ne pose aucune question.
```

**Résultat attendu :** la réponse contient une fiche complète par source valide et se termine par `DONNEES_RENDU_PRETES`.

**Condition de passage :** passez à `CANON` uniquement si chaque source valide possède tous ses champs et si `DONNEES_RENDU_PRETES` est présent.

**Si échec :** si la réponse contient `DONNEES_RENDU_INCOMPLETES`, arrêtez. Ne demandez pas à l’Assistant d’inventer les champs manquants.

## Étape 8 : CANON sans le Web

**But :** charger les fragments HTML de référence juste avant de produire le rendu.

**Action :**

Vérifiez que le badge bleu `Web` est absent et restez dans la même conversation.

**Message à copier :**

```text
PHASE CANON.
N’utilise pas le Web.
Recherche SNUM_CANON_V512_INDEX_START et SNUM_CANON_V512_INDEX_END
dans les ressources du Projet.
Suis READ_NEXT.
Charge intégralement les fragments 06, 07, 08, 09 et 10.
Vérifie la paire d’index et les onze paires de fragments START/END.
Conserve littéralement les blocs html.
Ne rends pas encore la newsletter.
Réponds seulement :
- CANON_HTML_PRET, puis la paire d’index et les onze paires de fragments ;
- ou CANON_HTML_INCOMPLET, puis le jeton manquant.
```

Envoyez ce message sans le modifier.

**Résultat attendu :** la réponse commence par `CANON_HTML_PRET`, contient la paire `SNUM_CANON_V512_INDEX_START / SNUM_CANON_V512_INDEX_END`, puis les onze paires suivantes :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_FOOTER_START / SNUM_FOOTER_END` ;
- `SNUM_ESSENTIALS_OPEN_START / SNUM_ESSENTIALS_OPEN_END` ;
- `SNUM_ESSENTIAL_CARD_START / SNUM_ESSENTIAL_CARD_END` ;
- `SNUM_ESSENTIALS_CLOSE_START / SNUM_ESSENTIALS_CLOSE_END` ;
- `SNUM_RUBRIC_OPEN_START / SNUM_RUBRIC_OPEN_END` ;
- `SNUM_RUBRIC_ARTICLE_START / SNUM_RUBRIC_ARTICLE_END` ;
- `SNUM_RUBRIC_CLOSE_START / SNUM_RUBRIC_CLOSE_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.
- `SNUM_SHELL_CLOSE_START / SNUM_SHELL_CLOSE_END`.

**Condition de passage :** envoyez `RENDU` uniquement si `CANON_HTML_PRET`, la paire d’index et les onze paires de fragments sont présents. N’envoyez aucun autre message entre `CANON` et `RENDU`.

**Si échec :** n’envoyez pas `RENDU`. Vérifiez que la conversation appartient au Projet et que les neuf fichiers sont présents. Recommencez ensuite toute l’édition dans une nouvelle conversation du Projet.

## Étape 9 : RENDU sans le Web

**But :** produire la revue et le document HTML à partir des seules sources validées et des fragments chargés.

**Action :**

Vérifiez que le badge bleu `Web` est absent, restez dans la même conversation et n’envoyez aucun message intermédiaire.

**Message à copier :**

```text
PHASE RENDU.
N’utilise pas le Web.
Utilise exclusivement DONNEES_RENDU et les fragments canoniques
chargés au tour précédent.
Ne recherche plus les ressources ni les jetons.
Utilise les blocs affichés dans la réponse CANON précédente.
Les marqueurs @@ des fragments sont des entrées normales,
jamais un échec avant leur remplacement.
Construis d’abord un brouillon HTML complet non affiché.
Copie littéralement 06.
Pour L’essentiel, concatène ESSENTIALS_OPEN,
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
Avec moins de trois sources valides, ne crée ni section ni lien
L’essentiel.
À partir de trois sources valides, crée exactement trois cartes
essentielles.
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
- n’affiche aucun HTML.
Ne pose aucune question.
```

Envoyez ce message sans le modifier.

**Résultat attendu :** la réponse contient, dans cet ordre, `## REVUE`, `## HTML COMPLET` avec un seul bloc HTML complet, puis `## DOSSIER PRIVÉ`.

**Condition de passage :** si la réponse ne commence pas par `A_COMPLETER`, passez à la checklist de l’étape 9. La présence d’un bloc HTML ne suffit pas pour accepter le résultat.

**Si échec :** si la réponse commence par `A_COMPLETER`, arrêtez immédiatement. Lisez `CONTROLES_EN_ECHEC` et relevez chaque ligne `CODE | détail`. Ne demandez pas à l’Assistant de continuer quand même. Corrigez l’installation si le code est `CANON_MANQUANT` ; pour les autres codes, conservez la conversation comme preuve de recette et signalez l’échec.

## Étape 10 : contrôler puis copier le résultat

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
- Réponse `CANON_HTML_INCOMPLET SNUM_CANON_V512_INDEX_START` : la conversation ne voit pas les ressources. Revenez dans `Newsletter SNUM`, vérifiez les neuf fichiers et recommencez l’édition.
- Date hors période : revenez à `VALIDATION`, corrigez les deux dates ISO et ne continuez qu’après un résultat conforme.
- HTML affiché malgré un contrôle en échec : refusez la sortie. La présence de code HTML ne prouve pas sa conformité.

## Limite actuelle et origine de la V5.12

La recette réelle V5.9 du 15 octobre 2026 a réussi `COLLECTE`, `VALIDATION` et `CANON`, puis `RENDU` a répondu `A_COMPLETER` sans explication. Elle a aussi conservé deux articles portant sur le même événement RH.

La V5.10 a corrigé ces deux causes : les cartes et articles sont devenus des fragments atomiques répétables ; la validation utilise `CLE_EVENEMENT` et `DOUBLON_DE`. Sa recette réelle a toutefois échoué sur `SNUM_SHELL_TAIL_START`. Une recherche ciblée a retrouvé `07-COQUE-FIN.md`, mais l’Assistant a réécrit le footer au lieu de le copier. La V5.11 scinde donc ce document en `07-PIED-DE-PAGE.md` et `10-COQUE-FIN.md`. Chaque ressource canonique reste sous 3 000 octets.

La recette V5.11 a ensuite chargé les onze fragments après une relance technique, puis `RENDU` a contrôlé les marqueurs bruts avant de les remplacer. La V5.12 ajoute donc `DONNEES_RENDU` et rend obligatoire l’ordre : préparer les valeurs, construire un brouillon HTML complet non affiché, corriger, puis contrôler seulement ce brouillon final.

La recette réelle V5.12 a produit un HTML complet après un message manuel `continue` et un second envoi de `RENDU`. Elle a toutefois généré des jours de semaine faux à partir de dates ISO correctes. La V5.12 n'est donc pas validée pour une livraison métier autonome. Vérifiez explicitement la correspondance entre chaque date ISO et sa date longue ; arrêtez la recette au premier écart.

Le protocole organise le travail, mais le contrôle final décide si le livrable est utilisable. La réponse `CANON_HTML_PRET` ne prouve pas à elle seule que le HTML final est identique au canon Bacoco.

## Sources et preuves

- [notice opérationnelle complète](./NOTICE-V5.12.md) ;
- [prompt système à installer](./PROMPT-SYSTEME-SNUM-V5.12.md) ;
- [rapport de contrôle V5.12](./RAPPORT-V5.12.md) ;
- [résultat de l'installation et de la recette V5.12](./_documentation/installation-v5.12-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [conversation V5.12 : HTML produit après reprise, contrôle métier requis](https://assistant.numerique.gouv.fr/chat/f9064cda-77f1-4dfe-b4e6-2da38e09eb72/) ;
- [première conversation V5.9 : collecte corrigée, arrêt sur la transmission du canon](https://assistant.numerique.gouv.fr/chat/ac926e61-2b8a-4d4e-bfc3-e5b8e0b5de82) ;
- [conversation V5.9 finale : paire d’index transmise, arrêt contrôlé au rendu](https://assistant.numerique.gouv.fr/chat/68369f19-beff-4a6d-a3d6-80903fdacc60) ;
- [conversation de reproduction V5.9 : dédoublonnage manqué puis arrêt opaque](https://assistant.numerique.gouv.fr/chat/07764649-dd72-489f-ad5f-bb33084c82ba/).
