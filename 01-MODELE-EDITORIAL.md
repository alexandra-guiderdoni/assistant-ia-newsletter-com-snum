# Méthode et format SNUM - V5.3.1

## Admissibilité d’un événement

| Vérification | Condition pour retenir |
| --- | --- |
| Date de publication | Date établie dans la fenêtre ; l’année seule ne suffit pas |
| Article ou source primaire | Titre original, source et URL exacte ; accueil, archive ou page de recherche ne remplace pas le document |
| Accès | Contenu éditorial intégral libre sans compte, abonnement, essai payant ; signaler toute troncature |
| Lecture | Corps effectivement obtenu et exploité, ou fourni avec provenance et preuve datée d’accès public |
| Événement | Pas le même fait déjà couvert ; regrouper plusieurs articles sur le même événement |
| Rubrique et utilité | Rattachement naturel et conséquence concrète proposée pour le SNUM |

INTEGRAL_LU : lecture intégrale réellement effectuée par toi avec l’outil disponible, accès public établi. INTEGRAL_FOURNI : corps complet apporté par une personne ou un collecteur identifié, accès public daté documenté ; attribuer cette collecte, ta propre analyse étant distincte. EXTRAITS, A_DATER et NON_VERIFIABLE restent candidats privés, jamais retenus. PAYANT_OU_LOGIN et HORS_PERIODE sont exclus. Un article PAYANT_OU_LOGIN reste exclu même si son corps, sa copie ou sa capture est fourni. HTTP 200 et longueur ne démontrent pas l’intégralité.

Pour une source officielle, ouvrir la page exacte puis essayer son lien direct, ELI, ses articles ou son PDF public avant de conclure à l’absence du texte. Un identifiant erroné ou un échec sur une variante d’URL ne rend pas la source inaccessible. Vérifier la date affichée sur le document : une période écrite dans la requête de recherche n’est pas un filtre de dates.

Chercher Le Monde, Les Échos et les autres médias français pertinents, puis compléter avec economie.gouv.fr, presse.economie.gouv.fr, numerique.gouv.fr, Acteurs Publics, IT for Business, Journal du Net, L’Usine Digitale et de bonnes sources étrangères, officielles ou spécialisées utiles. Exclure promotion et faibles contenus. Les ressources du Centre de ressources documentaires « Informatique - Ministères économiques et financiers » ne s’utilisent que si réellement accessibles ou fournies. Ne pas privilégier une source faible simplement parce qu’elle est gratuite.

## Structure publique

Titre : Revue de presse du SNUM - [date]. Période de collecte. Avec au moins trois événements, L’essentiel contient exactement trois synthèses reprises des rubriques. Avec un ou deux événements, supprimer entièrement L’essentiel et commencer les rubriques au numéro 01. Ensuite, rubriques de référence dans cet ordre : NUMERIQUE ; INTELLIGENCE ARTIFICIELLE (IA) ; COMMANDE PUBLIQUE ; RESSOURCES HUMAINES ; VIE DE BERCY. Omettre les rubriques sans sujet admissible. À surveiller seulement pour un suivi concret. Rubriques complémentaires du Centre documentaire seulement avec ressources réellement disponibles ; aucune nouvelle rubrique sans nécessité forte.

Ne pas mettre de comptes près du titre ou sous les rubriques, pas de badge Revue publique, pas de sous-titres « 3 sujets prioritaires », « 4 fiches », « Rubriques de référence » ni d’émojis décoratifs. Dix à quinze sujets sont visés, sans quota. Un ou deux événements donnent une revue courte A_COMPLETER avec HTML et sans essentiel ; zéro événement ne donne ni revue ni HTML. À partir de trois événements, trois essentiels sont repris dans leurs rubriques et ne sont pas recomptés. Des angles tirés du même article ne créent pas automatiquement plusieurs événements.

## Fiche, également pour chaque essentiel

~~~markdown
### [Titre informatif bref]

[Fait essentiel en une phrase courte, 25 mots maximum.]

**Mots-clés :** [3 à 5 termes ou expressions courts, sur une ligne].

**À retenir :** [Une phrase factuelle, 15 mots maximum.]

**Intérêt pour le SNUM :** [Une phrase de conséquence proposée, 15 mots maximum.]

**Source :** [source]. **Date :** [date de publication].
[Lire « titre original » sur nom de la source](URL_DE_L_ARTICLE)
~~~

Préserver chiffres, dates, périmètres et réserves indispensables. Choisir un fait central plutôt que compresser tout l’article. À retenir donne une réserve ou conséquence factuelle distincte ; Intérêt propose une action utile, sans l’attribuer à la source. Ne pas transformer une proposition politique en réforme adoptée, un projet local en déploiement national, ni des règles du secteur privé en obligations de la fonction publique.

## Dossier privé bref

État, identifiant, fenêtre et son fondement ; limites des outils. Tableau des retenus : ID, événement, titre original, source, date avec certitude, URL, lecture, provenance et repère de preuve. Requêtes et sources consultées ; regroupements et exclusions motivées ; rubriques sans sujet ; candidats non retenus. Compter les événements uniques, sans recompter les essentiels.

Contrôles : texte exact contrôlé, méthode et acteur, date, résultat `VERIFIE` / `ECHEC` / `NON_EXECUTE` / `NON_VERIFIABLE`. Comptage par espaces hors libellés et Markdown, si outil ou contrôle externe disponible ; sinon `COMPTAGE_NON_VERIFIE`. Ne pas déclarer une réussite à partir de la version réécrite de la fiche utilisée dans un tableau de contrôle. Une modification invalide le contrôle correspondant. Ne pas conclure « toutes les dates sont dans la période » lorsque le tableau montre août, juin ou le 1er octobre hors de la fenêtre.

Brouillon du courriel selon 03 ; proposition d’état pour 02. Publication et envoi restent des états séparés. Les documents sources intégraux et le dossier privé ne vont pas dans le dépôt public.
