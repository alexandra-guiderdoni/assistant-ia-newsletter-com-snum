# Newsletter SNUM avec l’Assistant DINUM - guide V5.8

Ce guide s’adresse à une personne qui découvre l’Assistant DINUM. Suivez les étapes dans l’ordre et ne sautez aucune vérification.

La newsletter et son code HTML sont produits dans le chat. Ce kit ne publie aucun site et n’envoie aucun courriel.

> **Limite connue.** L’Assistant peut modifier le HTML canonique sans détecter son erreur. La V5.8 permet une recette assistée, mais ne garantit pas un rendu strictement identique au site Bacoco. N’utilisez jamais un résultat qui échoue au contrôle final.

## Parcours express

1. Une seule fois, créez le Projet `Newsletter SNUM`.
2. Une seule fois, installez le prompt système et les huit fichiers Markdown.
3. Pour une nouvelle édition, ouvrez une conversation depuis ce Projet.
4. Préparez les cinq valeurs de date demandées.
5. Activez le Web et envoyez `COLLECTE`.
6. Désactivez le Web et envoyez `VALIDATION`.
7. Sans le Web, envoyez `CANON`.
8. Sans le Web et sans message intermédiaire, envoyez `RENDU`.
9. Si la réponse commence par `A_COMPLETER`, arrêtez. Sinon, appliquez toute la checklist avant de copier le HTML.

Les étapes 1 et 2 sont réalisées une seule fois. Les étapes 3 à 9 sont répétées pour chaque édition.

## Comprendre les deux niveaux de prompts

Le **prompt système** contient les règles permanentes. Il est installé une seule fois dans les instructions du Projet.

Les **prompts utilisateur** sont les quatre messages `COLLECTE`, `VALIDATION`, `CANON` et `RENDU`. Ils sont envoyés pour chaque édition dans une même conversation.

Ne collez jamais le prompt système dans la conversation. Ne placez jamais les quatre prompts utilisateur dans les instructions du Projet.

## Première partie : installer le Projet une seule fois

### Étape 1 : télécharger et décompresser le kit

1. Téléchargez [`kit-dinum-snum-v5-8-progressif-8-fichiers.zip`](./kit-dinum-snum-v5-8-progressif-8-fichiers.zip).
2. Téléchargez [`PROMPT-SYSTEME-SNUM-V5.8.md`](./PROMPT-SYSTEME-SNUM-V5.8.md).
3. Sur votre poste, double-cliquez sur le fichier ZIP pour le décompresser.
4. Ouvrez le dossier obtenu.
5. Vérifiez que le dossier contient exactement les huit fichiers suivants :
   - `00-PROMPT-PROJET.md` ;
   - `01-ETAT-HISTORIQUE.md` ;
   - `02-METHODE-EDITORIALE.md` ;
   - `05-INDEX-HTML.md` ;
   - `06-COQUE-DEBUT.md` ;
   - `07-COQUE-FIN.md` ;
   - `08-BLOC-ESSENTIEL.md` ;
   - `09-BLOCS-RUBRIQUES.md`.

N’ajoutez pas le ZIP, le README, la notice ou un autre fichier dans le Projet.

### Étape 2 : créer le Projet dans l’Assistant DINUM

1. Ouvrez <https://assistant.numerique.gouv.fr/>.
2. Connectez-vous avec AgentConnect si l’écran de connexion apparaît.
3. Ouvrez le panneau situé à gauche de l’écran.
4. Cliquez sur **Nouveau projet**.
5. Saisissez exactement `Newsletter SNUM` comme nom du Projet.
6. Sur votre poste, ouvrez `PROMPT-SYSTEME-SNUM-V5.8.md` dans un éditeur de texte.
7. Sélectionnez tout le texte du fichier, puis copiez-le.
8. Dans le formulaire du Projet, collez le texte dans **Instructions (expérimental)**.
9. Descendez jusqu’à la fin du champ.
10. Vérifiez que la dernière phrase est exactement `N’affirme aucun contrôle non exécuté.`.
11. Si cette phrase manque, effacez le champ et recommencez le collage depuis le début.
12. Ajoutez les huit fichiers Markdown obtenus à l’étape 1.
13. Relisez les huit noms affichés dans le Projet.
14. Créez ou enregistrez le Projet.
15. Attendez la disparition du message d’indexation. Ne commencez pas une conversation pendant l’indexation.

### Résultat attendu après l’installation

Le Projet s’appelle `Newsletter SNUM`. Le champ **Instructions (expérimental)** se termine par la phrase attendue. Les huit fichiers sont visibles et aucun message d’indexation ne reste affiché.

Si un de ces trois contrôles échoue, corrigez le Projet avant de poursuivre.

## Seconde partie : préparer une édition

### Étape 3 : ouvrir la conversation au bon endroit

1. Dans le panneau de gauche, ouvrez le Projet `Newsletter SNUM`.
2. Cliquez sur **Start new conversation in Newsletter SNUM** ou sur le bouton équivalent affiché dans ce Projet.
3. Vérifiez que la nouvelle conversation apparaît sous `Newsletter SNUM`.

Si elle apparaît sous **Vos conversations**, fermez-la. Revenez dans `Newsletter SNUM` et créez une nouvelle conversation depuis le Projet. Une conversation générale ne peut pas lire les huit fichiers.

Conservez cette même conversation jusqu’à la fin de `RENDU`. Ne cliquez pas sur **Nouvelle conversation** entre les quatre messages.

### Étape 4 : préparer les cinq valeurs

Écrivez les cinq valeurs suivantes avant d’envoyer le premier message :

- `{{DATE_EDITION}}` : date affichée de la newsletter, par exemple `14 octobre 2026` ;
- `{{DEBUT}}` : début de la collecte en toutes lettres, par exemple `3 octobre 2026` ;
- `{{FIN}}` : fin de la collecte en toutes lettres, par exemple `13 octobre 2026` ;
- `{{DEBUT_ISO}}` : même date que `{{DEBUT}}`, au format `AAAA-MM-JJ`, par exemple `2026-10-03` ;
- `{{FIN_ISO}}` : même date que `{{FIN}}`, au format `AAAA-MM-JJ`, par exemple `2026-10-13`.

Les caractères `{{` et `}}` sont des repères à remplacer. Ils ne doivent jamais apparaître dans un message envoyé.

### Exemple entièrement rempli

Dans cet exemple, l’édition est datée du 14 octobre 2026 et couvre la période inclusive du 3 au 13 octobre 2026.

Le message `COLLECTE` entièrement rempli serait :

```text
PHASE COLLECTE. Utilise le Web. Édition du 14 octobre 2026, fenêtre du 3 octobre 2026 au 13 octobre 2026 inclus. Ne rédige ni REVUE ni HTML. Recherche et ouvre les sources publiques intégralement accessibles. Réponds sous CANDIDATS avec une liste numérotée ; pour chaque candidat : titre, URL canonique, date de publication explicitement lue sur la page au format AAAA-MM-JJ ou DATE_INCONNUE, accès intégral OUI/NON, rubrique exacte et fait essentiel. Ne décide pas encore si la date est dans la fenêtre. Termine par COLLECTE_TERMINEE, sans question.
```

Le message `VALIDATION` entièrement rempli serait :

```text
PHASE VALIDATION. N’utilise pas le Web et ne rédige ni REVUE ni HTML. Relis uniquement CANDIDATS. Applique exactement 2026-10-03 <= DATE_PUBLICATION <= 2026-10-13 et exige accès intégral OUI. Rejette DATE_INCONNUE, incohérence manifeste et doublon ; conserve une seule URL canonique par événement. Réponds sous SOURCES_VALIDES avec titre, URL, date, rubrique exacte et fait essentiel ; puis SOURCES_EXCLUES avec chaque motif ; termine par VALIDATION_TERMINEE. Ne pose aucune question.
```

N’utilisez ces dates que pour cet exemple. Pour une autre édition, remplacez les cinq valeurs par les dates demandées.

Les messages `CANON` et `RENDU` ne contiennent aucune valeur de date. Ils sont déjà complets et doivent être envoyés sans modification.

## Étape 5 : COLLECTE avec le Web

**But :** rechercher et ouvrir les articles susceptibles d’entrer dans la newsletter.

**Action :**

1. Dans la zone de message, cliquez sur le bouton `+`.
2. Sélectionnez `Web`.
3. Vérifiez que le badge bleu `Web` apparaît à côté du bouton `+`.
4. Si le badge n’apparaît pas, n’envoyez pas le message. Rechargez la page, revenez dans la conversation du Projet et recommencez l’activation.

**Message à copier :**

```text
PHASE COLLECTE. Utilise le Web. Édition du {{DATE_EDITION}}, fenêtre du {{DEBUT}} au {{FIN}} inclus. Ne rédige ni REVUE ni HTML. Recherche et ouvre les sources publiques intégralement accessibles. Réponds sous CANDIDATS avec une liste numérotée ; pour chaque candidat : titre, URL canonique, date de publication explicitement lue sur la page au format AAAA-MM-JJ ou DATE_INCONNUE, accès intégral OUI/NON, rubrique exacte et fait essentiel. Ne décide pas encore si la date est dans la fenêtre. Termine par COLLECTE_TERMINEE, sans question.
```

Remplacez les trois repères par vos valeurs, supprimez toutes les accolades, relisez les trois dates, puis envoyez le message.

**Résultat attendu :** la réponse contient le titre `CANDIDATS`, une liste numérotée et le mot `COLLECTE_TERMINEE`. Elle ne contient ni newsletter finale ni code HTML.

**Condition de passage :** passez à `VALIDATION` uniquement si `COLLECTE_TERMINEE` est présent.

**Si échec :** n’envoyez pas `VALIDATION`. Renvoyez une seule fois le message `COLLECTE`. Si le second essai échoue, arrêtez cette édition.

## Étape 6 : VALIDATION sans le Web

**But :** éliminer les sources hors période, inaccessibles, incertaines ou en double.

**Action :**

1. Dans la zone de message, cliquez sur le badge bleu `Web` pour le retirer. Si nécessaire, ouvrez le bouton `+` et désactivez `Web`.
2. Vérifiez que le badge bleu `Web` n’apparaît plus.
3. Restez dans la conversation utilisée pour `COLLECTE`.

**Message à copier :**

```text
PHASE VALIDATION. N’utilise pas le Web et ne rédige ni REVUE ni HTML. Relis uniquement CANDIDATS. Applique exactement {{DEBUT_ISO}} <= DATE_PUBLICATION <= {{FIN_ISO}} et exige accès intégral OUI. Rejette DATE_INCONNUE, incohérence manifeste et doublon ; conserve une seule URL canonique par événement. Réponds sous SOURCES_VALIDES avec titre, URL, date, rubrique exacte et fait essentiel ; puis SOURCES_EXCLUES avec chaque motif ; termine par VALIDATION_TERMINEE. Ne pose aucune question.
```

Remplacez les deux repères par vos dates ISO, supprimez toutes les accolades, relisez les deux dates, puis envoyez le message.

**Résultat attendu :** la réponse contient `SOURCES_VALIDES`, `SOURCES_EXCLUES` et `VALIDATION_TERMINEE`.

**Condition de passage :** vérifiez que chaque source valide possède une URL et une date comprise entre les deux bornes incluses. Passez à `CANON` uniquement si `VALIDATION_TERMINEE` est présent et si `SOURCES_VALIDES` contient au moins une source conforme.

**Si échec :** n’envoyez pas `CANON`. Corrigez les dates ISO et recommencez `VALIDATION`. Si aucune source valide ne reste, arrêtez cette édition.

## Étape 7 : CANON sans le Web

**But :** charger les fragments HTML de référence juste avant de produire le rendu.

**Action :**

Vérifiez que le badge bleu `Web` est absent et restez dans la même conversation.

**Message à copier :**

```text
PHASE CANON. N’utilise pas le Web. Recherche SNUM_CANON_V58_INDEX_START dans les ressources du Projet, suis READ_NEXT et charge intégralement les fragments 06, 07, 08 et 09. Vérifie les six paires START/END et conserve littéralement les blocs html. Ne rends pas encore la newsletter. Réponds seulement CANON_HTML_PRET puis les six paires, ou CANON_HTML_INCOMPLET puis le jeton manquant.
```

Envoyez ce message sans le modifier.

**Résultat attendu :** la réponse commence par `CANON_HTML_PRET` et contient les six paires suivantes :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_SHELL_TAIL_START / SNUM_SHELL_TAIL_END` ;
- `SNUM_ESSENTIAL_START / SNUM_ESSENTIAL_END` ;
- `SNUM_RUBRIC_START / SNUM_RUBRIC_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

**Condition de passage :** envoyez `RENDU` uniquement si `CANON_HTML_PRET` et les six paires sont présents. N’envoyez aucun autre message entre `CANON` et `RENDU`.

**Si échec :** n’envoyez pas `RENDU`. Vérifiez que la conversation appartient au Projet et que les huit fichiers sont présents. Recommencez ensuite toute l’édition dans une nouvelle conversation du Projet.

## Étape 8 : RENDU sans le Web

**But :** produire la revue et le document HTML à partir des seules sources validées et des fragments chargés.

**Action :**

Vérifiez que le badge bleu `Web` est absent, restez dans la même conversation et n’envoyez aucun message intermédiaire.

**Message à copier :**

```text
PHASE RENDU. N’utilise pas le Web. Utilise exclusivement SOURCES_VALIDES et les fragments canoniques chargés au tour précédent. Copie littéralement 06, insère les blocs 08 et 09 nécessaires, puis 07 ; remplace seulement les marqueurs @@. Ne crée aucune balise ni classe absente des fragments. Livre exactement ## REVUE, ## HTML COMPLET avec un unique bloc html de <!doctype html> à </html>, puis ## DOSSIER PRIVÉ. Avant affichage, vérifie le title, /revue-presse-snum/styles.css?v=20260917, l’absence de marqueur @@, fr-theme-modal et les scripts DSFR 1.15.2. Si un point n’est pas établi, commence ta réponse par A_COMPLETER et n’affiche aucun code. Ne pose aucune question.
```

Envoyez ce message sans le modifier.

**Résultat attendu :** la réponse contient, dans cet ordre, `## REVUE`, `## HTML COMPLET` avec un seul bloc HTML complet, puis `## DOSSIER PRIVÉ`.

**Condition de passage :** si la réponse ne commence pas par `A_COMPLETER`, passez à la checklist de l’étape 9. La présence d’un bloc HTML ne suffit pas pour accepter le résultat.

**Si échec :** si la réponse commence par `A_COMPLETER`, arrêtez immédiatement. Ne demandez pas à l’Assistant de continuer quand même. Recommencez à partir de `CANON` ou faites contrôler l’édition extérieurement.

## Étape 9 : contrôler puis copier le résultat

Contrôlez chaque point ci-dessous dans la réponse. Un seul échec suffit pour refuser le HTML.

- `## REVUE`, `## HTML COMPLET` et `## DOSSIER PRIVÉ` apparaissent dans cet ordre.
- Toutes les sources du rendu figuraient dans `SOURCES_VALIDES`.
- Un seul bloc HTML commence par `<!doctype html>` et se termine par `</html>`.
- Aucun marqueur commençant par `@@` ne subsiste.
- Le titre suit la forme `Revue de presse du … - SNUM`.
- La ligne `/revue-presse-snum/styles.css?v=20260917` est présente.
- Trois liens d’accès rapide, un seul `h1`, `fr-theme-modal` et les deux scripts DSFR 1.15.2 sont présents.
- La navigation contient uniquement les rubriques réellement produites.
- Si la rubrique IA existe, elle contient `<section id="ia" class="section-muted">`.
- Si la rubrique RH existe, elle contient `<section id="rh" class="section-muted">`.

Si tous les points réussissent, copiez uniquement le bloc allant de `<!doctype html>` à `</html>`. Si un point échoue, ne copiez pas et n’utilisez pas le HTML. Notez le contrôle en échec pour demander une correction.

## Dépannage

- Message `the authentication session has expired` : reconnectez-vous à AgentConnect, puis recommencez dans une nouvelle conversation du Projet.
- Réponse `CANON_HTML_INCOMPLET SNUM_CANON_V58_INDEX_START` : la conversation ne voit pas les ressources. Revenez dans `Newsletter SNUM`, vérifiez les huit fichiers et recommencez l’édition.
- Date hors période : revenez à `VALIDATION`, corrigez les deux dates ISO et ne continuez qu’après un résultat conforme.
- HTML affiché malgré un contrôle en échec : refusez la sortie. La présence de code HTML ne prouve pas sa conformité.

## Ce que la V5.8 ne garantit pas encore

Lors de la recette du 15 octobre 2026, `COLLECTE`, `VALIDATION` et `CANON` ont réussi. Le HTML final a pourtant perdu les classes `section-muted` des rubriques IA et RH sans déclencher l’arrêt attendu.

Le protocole organise le travail, mais le contrôle final décide si le livrable est utilisable. La réponse `CANON_HTML_PRET` ne prouve pas à elle seule que le HTML final est identique au canon Bacoco.

## Sources et preuves

- [notice opérationnelle complète](./NOTICE-V5.8.md) ;
- [prompt système à installer](./PROMPT-SYSTEME-SNUM-V5.8.md) ;
- [rapport de contrôle V5.8](./RAPPORT-V5.8.md) ;
- [résultat de l’installation et de la recette réelle](./_documentation/installation-v5.8-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md).
