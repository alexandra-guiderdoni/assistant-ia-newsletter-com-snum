# Méthode éditoriale SNUM - V5.9

## COLLECTE-WEB

Procéder par requêtes courtes et séparées : une source ou un thème par requête, avec le mois et l’année écrits en toutes lettres. Ne jamais utiliser une plage `AAAA-MM-JJ..AAAA-MM-JJ`, une longue chaîne de `OR` ou un domaine deviné.

Domaines canoniques : `lemonde.fr`, `lesechos.fr`, `economie.gouv.fr`, `presse.economie.gouv.fr`, `numerique.gouv.fr`, `acteurspublics.fr`, `itforbusiness.fr`, `journaldunet.com` et `usine-digitale.fr`. Compléter avec `cnil.fr`, `cyber.gouv.fr`, `legifrance.gouv.fr`, `data.gouv.fr` et d’autres sources pertinentes réellement trouvées.

Pour chaque rubrique, commencer sans filtre `site:`, puis cibler un domaine si nécessaire. Exécuter au minimum dix requêtes distinctes : au moins deux par rubrique, dont une générale et une ciblée, réparties sur au moins cinq domaines réellement connus. Si une recherche échoue ou ne rend aucun résultat exploitable, la reformuler au plus deux fois : retirer le domaine, simplifier les mots ou chercher le titre présumé. Continuer les autres requêtes.

Si la première passe produit moins de cinq candidats, effectuer une seconde passe ciblée sur les sources officielles et spécialisées qui n’ont pas encore été interrogées. Ne jamais inventer un candidat pour atteindre ce seuil.

Avant `CANDIDATS`, produire `COUVERTURE_COLLECTE` avec une ligne par requête : rubrique, requête, domaine, résultat et URL effectivement ouverte. Répondre `COLLECTE_TERMINEE` seulement si les cinq rubriques, les dix requêtes distinctes, les cinq domaines et au moins cinq candidats sont établis. Sinon répondre `COLLECTE_INSUFFISANTE` avec les critères manquants ; ne pas présenter la collecte comme réussie.

À partir des résultats, ouvrir chaque URL exacte. Une page ouverte et datée peut être retenue seulement après lecture du corps intégral. Consigner séparément les erreurs techniques, les résultats vides, les URL ouvertes et les exclusions. Ne jamais transformer une requête exécutée en preuve de lecture.

## Collecter et prouver

Priorité nette aux médias français généralistes et économiques de référence, notamment Le Monde et Les Échos, puis aux sources françaises officielles et spécialisées pertinentes. Compléter avec economie.gouv.fr, presse.economie.gouv.fr, numerique.gouv.fr, Acteurs Publics, IT for Business, Journal du Net, L’Usine Digitale et de bonnes sources étrangères quand leur apport est réel.

Pour chaque candidat, ouvrir l’URL exacte. Retenir seulement un contenu éditorial intégral, public sans compte ni abonnement, daté dans la fenêtre et réellement lu. Un titre, un extrait, une page d’accueil, une archive, HTTP 200 ou une date dans la requête ne prouve ni le corps intégral ni la date de publication.

Filtre éliminatoire, à appliquer avant la sélection et la rédaction. La date de publication de la page est la seule date d’admissibilité : une date d’événement, de période d’activité ou de mise à jour ne la remplace jamais.

1. date de publication comprise entre les deux bornes incluses ;
2. corps complet effectivement accessible et lu ;
3. accès gratuit, sans compte ni abonnement ;
4. source éditoriale identifiable et URL exacte ;
5. pertinence directe pour une rubrique admise.

Si un seul critère échoue ou reste incertain, classer le candidat parmi les exclusions. La date de l’événement, une mise en œuvre ultérieure, un extrait jugé « suffisant » ou l’intérêt du sujet ne remplace jamais ces cinq critères.

Un article payant reste exclu même si une copie est fournie. Une source complète apportée par une personne ou un collecteur identifié peut être `INTEGRAL_FOURNI` seulement si son accès public gratuit est établi et attribué. Sinon elle reste candidate privée. Pour une source officielle, essayer la page directe, son ELI, ses articles ou son PDF avant de la déclarer inaccessible.

La date de publication est distincte de la date de l’événement et de la mise à jour d’un jeu de données. L’hébergement sur `data.gouv.fr` ne rend pas le producteur officiel. Exclure les sources promotionnelles, dates incertaines, lectures partielles et doublons. Regrouper les articles sur le même événement.

Avant de conclure à une collecte insuffisante, consigner les domaines, requêtes, URL exactes et causes d’exclusion. Ne jamais inventer une consultation, une capture, une balise canonique, une preuve ou un contrôle.

## Validation déterministe des dates

La phase `VALIDATION` travaille uniquement sur la valeur brute fournie dans `CANDIDATS`. Pour chaque candidat, elle affiche une ligne `CONTROLE_DATES` comportant : date brute, format exact `AAAA-MM-JJ`, test de borne basse, test de borne haute, accès intégral et décision.

Une source rejoint `SOURCES_VALIDES` seulement si le format, les deux bornes et l’accès valent tous `OUI`. Ne pas retirer une mention ajoutée à la date pour la rendre conforme : `2026-08-12 (modification)` n’est pas une date brute au format exact. `2026-10-02` est antérieur à `2026-10-03` ; `2026-10-15` est postérieur à `2026-10-13`.

Avant `VALIDATION_TERMINEE`, vérifier que le nombre de sources valides plus le nombre de sources exclues égale le nombre de candidats. Une erreur de comptage, une source présente dans les deux listes ou une date hors fenêtre conservée bloque la suite.

## Sélection

Viser environ 10 à 15 événements utiles, sans quota. Ne pas fabriquer de matière pour atteindre ce volume. Rubriques admises, dans cet ordre :

1. `NUMERIQUE`
2. `INTELLIGENCE_ARTIFICIELLE_IA`
3. `COMMANDE_PUBLIQUE`
4. `RESSOURCES_HUMAINES`
5. `VIE_DE_BERCY`

Cybersécurité, réglementation, données, cloud, logiciels et transformation numérique se classent dans ces rubriques. Omettre les rubriques vides. Les ressources du Centre de ressources documentaires « Informatique - Ministères économiques et financiers » ne s’utilisent que si elles sont réellement accessibles ou fournies.

## Rédaction courte

Chaque événement contient :

- un titre informatif et bref ;
- un fait essentiel en une phrase de 25 mots maximum ;
- 3 à 5 mots-clés ou expressions courtes ;
- « À retenir » en une phrase de 15 mots maximum ;
- « Intérêt pour le SNUM » en une phrase de 15 mots maximum ;
- titre original, source, date de publication et URL publique exacte ;
- statut et preuve de lecture dans le dossier privé.

Compter les mots par espaces sur chaque phrase finale avant de produire le HTML. Réécrire toute phrase trop longue ; ne jamais annoncer un contrôle réussi sans avoir effectué ce comptage sur le texte livré. Les chiffres, dates, périmètres et réserves indispensables restent exacts. Distinguer les faits de la source des implications proposées pour le SNUM. Aucun emoji, slogan, promotion, rubrique artificielle, volume près du titre ou remplissage.

Avec au moins trois événements, choisir exactement trois essentiels. Chaque essentiel est une mise en avant supplémentaire d’un événement qui reste aussi présent dans sa rubrique. Il ne compte pas comme un nouvel événement. Avec moins de trois, aucun essentiel. « À surveiller » reste facultatif et contient seulement des suivis courts, précis et utiles.

## Assemblage HTML dans l’Assistant

Le métier n’exécute aucun script. Après la collecte et la validation, dans une phase `CANON` sans Web qui précède immédiatement le rendu, l’Assistant lit `05-INDEX-HTML.md`, puis charge séparément les fragments `06`, `07`, `08` et `09` dans l’ordre `READ_NEXT`. Il vérifie pour chacun les jetons de début et de fin avant de poursuivre. Ces fragments générés depuis `05-BLOCS-HTML-CANONIQUES.md` priment pour toute balise, classe, dépendance et enveloppe de rubrique. `03-GABARIT-HTML.md` reste la référence locale détaillée, mais n’est pas téléversé dans le paquet progressif et ne sert jamais à reconstruire librement la page.

La seconde passe se fait sur la sortie exacte avant affichage : comparer les dates et URL de la revue au HTML, rechercher tout marqueur `@@`, compter les cartes essentielles et vérifier littéralement l’identifiant et l’enveloppe de chaque rubrique présente contre `05-INDEX-HTML.md`. Chaque source valide doit apparaître une fois dans sa rubrique, y compris lorsqu’elle est aussi essentielle. Chaque lien `href="#id"` du menu de rubriques doit viser exactement une section `id="id"`, et chaque rubrique produite doit posséder exactement un lien dans ce menu. Une divergence détectée entraîne la correction du bloc HTML avant livraison. Si elle ne peut pas être corrigée, remplacer le bloc de code par `A_COMPLETER — HTML canonique non établi` et nommer l’écart dans le dossier privé. Cette autoévaluation ne devient jamais un contrôle extérieur.

## Contrôles de cohérence avant livraison

Vérifier sur le texte exact : dates de publication dans la fenêtre, accès intégral gratuit, unicité des événements et URL, rubriques admises, 3 à 5 mots-clés, limites de 25 et 15 mots, exactement trois essentiels à partir de trois événements et absence de fausse preuve. Comparer ensuite le tableau des retenus à la revue et au HTML : les trois ensembles d’URL doivent être identiques. Une vérification manuelle du modèle reste une autoévaluation : la décrire comme telle, sans la transformer en contrôle extérieur.

Dans la date longue du HTML, ne jamais inventer le jour de la semaine : utiliser seulement le jour, le mois et l’année si le calendrier n’a pas été calculé par un outil.

Le HTML doit reprendre exactement les mêmes faits, titres, dates, URL et essentiels que la revue. Toute modification ultérieure invalide les contrôles correspondants.

## État

DINUM livre la revue et la section `HTML COMPLET` même si l’état reste `A_COMPLETER`. Le code HTML n’est affiché que si la seconde passe établit sa conformité canonique ; sinon, la section contient uniquement le message d’arrêt prévu. `PREPAREE` exige un contenu terminé et contrôlé extérieurement. `COMPLETE` exige publication vérifiée et envoi confirmé. `ALREADY_COMPLETE` arrête le cycle si l’édition du jour est déjà publiée ou diffusée, sans certifier que les deux actions sont achevées.
