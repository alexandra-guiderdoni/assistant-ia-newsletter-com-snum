# Méthode éditoriale SNUM - V5.8

## COLLECTE-WEB

Procéder par requêtes courtes et séparées : une source ou un thème par requête, avec le mois et l’année écrits en toutes lettres. Ne jamais utiliser une plage `AAAA-MM-JJ..AAAA-MM-JJ`, une longue chaîne de `OR` ou un domaine deviné.

Domaines canoniques : `lemonde.fr`, `lesechos.fr`, `economie.gouv.fr`, `presse.economie.gouv.fr`, `numerique.gouv.fr`, `acteurspublics.fr`, `itforbusiness.fr`, `journaldunet.com` et `usine-digitale.fr`. Compléter avec `cnil.fr`, `cyber.gouv.fr`, `legifrance.gouv.fr`, `data.gouv.fr` et d’autres sources pertinentes réellement trouvées.

Pour chaque rubrique, commencer sans filtre `site:`, puis cibler un domaine si nécessaire. Si une recherche échoue ou ne rend aucun résultat exploitable, la reformuler au plus deux fois : retirer le domaine, simplifier les mots ou chercher le titre présumé. Continuer les autres requêtes. Ne conclure à zéro événement qu’après avoir essayé plusieurs sources officielles et éditoriales distinctes.

À partir des résultats, ouvrir chaque URL exacte. Une page ouverte et datée peut être retenue seulement après lecture du corps intégral. Consigner séparément les erreurs techniques, les résultats vides, les URL ouvertes et les exclusions. Ne jamais transformer une requête exécutée en preuve de lecture.

## Collecter et prouver

Priorité nette aux médias français généralistes et économiques de référence, notamment Le Monde et Les Échos, puis aux sources françaises officielles et spécialisées pertinentes. Compléter avec economie.gouv.fr, presse.economie.gouv.fr, numerique.gouv.fr, Acteurs Publics, IT for Business, Journal du Net, L’Usine Digitale et de bonnes sources étrangères quand leur apport est réel.

Pour chaque candidat, ouvrir l’URL exacte. Retenir seulement un contenu éditorial intégral, public sans compte ni abonnement, daté dans la fenêtre et réellement lu. Un titre, un extrait, une page d’accueil, une archive, HTTP 200 ou une date dans la requête ne prouve ni le corps intégral ni la date de publication.

Filtre éliminatoire, à appliquer avant la sélection et la rédaction :

1. date de publication comprise entre les deux bornes incluses ;
2. corps complet effectivement accessible et lu ;
3. accès gratuit, sans compte ni abonnement ;
4. source éditoriale identifiable et URL exacte ;
5. pertinence directe pour une rubrique admise.

Si un seul critère échoue ou reste incertain, classer le candidat parmi les exclusions. La date de l’événement, une mise en œuvre ultérieure, un extrait jugé « suffisant » ou l’intérêt du sujet ne remplace jamais ces cinq critères.

Un article payant reste exclu même si une copie est fournie. Une source complète apportée par une personne ou un collecteur identifié peut être `INTEGRAL_FOURNI` seulement si son accès public gratuit est établi et attribué. Sinon elle reste candidate privée. Pour une source officielle, essayer la page directe, son ELI, ses articles ou son PDF avant de la déclarer inaccessible.

La date de publication est distincte de la date de l’événement et de la mise à jour d’un jeu de données. L’hébergement sur `data.gouv.fr` ne rend pas le producteur officiel. Exclure les sources promotionnelles, dates incertaines, lectures partielles et doublons. Regrouper les articles sur le même événement.

Avant de conclure à zéro événement, consigner les domaines, requêtes, URL exactes et causes d’exclusion. Ne jamais inventer une consultation, une capture, une balise canonique, une preuve ou un contrôle.

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

Avec au moins trois événements, choisir exactement trois essentiels, repris sans duplication depuis les rubriques. Avec moins de trois, aucun essentiel. « À surveiller » reste facultatif et contient seulement des suivis courts, précis et utiles.

## Assemblage HTML dans l’Assistant

Le métier n’exécute aucun script. L’Assistant assemble lui-même le bloc `HTML COMPLET` à partir de `05-BLOCS-HTML-CANONIQUES.md`, qui prime pour toute balise, classe, dépendance et enveloppe de rubrique. `03-GABARIT-HTML.md` conserve le contexte et le CSS de référence, mais ne sert pas à reconstruire librement la page.

La seconde passe se fait sur la sortie exacte avant affichage : comparer les dates et URL de la revue au HTML, rechercher tout marqueur `@@`, compter les cartes essentielles et vérifier littéralement l’identifiant et l’enveloppe de chaque rubrique présente contre `RÈGLE-DE-COPIE`. Une divergence détectée entraîne la correction du bloc HTML avant livraison. Si elle ne peut pas être corrigée, remplacer le bloc de code par `A_COMPLETER — HTML canonique non établi` et nommer l’écart dans le dossier privé. Cette autoévaluation ne devient jamais un contrôle extérieur.

## Contrôles de cohérence avant livraison

Vérifier sur le texte exact : dates de publication dans la fenêtre, accès intégral gratuit, unicité des événements et URL, rubriques admises, 3 à 5 mots-clés, limites de 25 et 15 mots, exactement trois essentiels à partir de trois événements et absence de fausse preuve. Comparer ensuite le tableau des retenus à la revue et au HTML : les trois ensembles d’URL doivent être identiques. Une vérification manuelle du modèle reste une autoévaluation : la décrire comme telle, sans la transformer en contrôle extérieur.

Dans la date longue du HTML, ne jamais inventer le jour de la semaine : utiliser seulement le jour, le mois et l’année si le calendrier n’a pas été calculé par un outil.

Le HTML doit reprendre exactement les mêmes faits, titres, dates, URL et essentiels que la revue. Toute modification ultérieure invalide les contrôles correspondants.

## État

DINUM livre la revue et la section `HTML COMPLET` même si l’état reste `A_COMPLETER`. Le code HTML n’est affiché que si la seconde passe établit sa conformité canonique ; sinon, la section contient uniquement le message d’arrêt prévu. `PREPAREE` exige un contenu terminé et contrôlé extérieurement. `COMPLETE` exige publication vérifiée et envoi confirmé. `ALREADY_COMPLETE` arrête le cycle si l’édition du jour est déjà publiée ou diffusée, sans certifier que les deux actions sont achevées.
