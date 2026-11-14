# Accessibilité de la page Veille SNUM : relevé du 14 novembre 2026

## Ce que ce document est, et n'est pas

C'est un préaudit outillé, complété par des mesures dans le navigateur. Ce n'est pas un audit RGAA : aucun des 258 tests du RGAA 4.1.2 n'a reçu de décision humaine, aucun lecteur d'écran réel n'a été utilisé, et aucun taux de conformité n'est calculé.

En l'absence d'audit, la mention réglementaire est « non conforme ». C'est celle que porte maintenant le pied de page, à la place de « audit non réalisé ».

## Périmètre

- P01 : page de sélection, vue paquet (25 articles), site en ligne.
- P02 : page des archives, site en ligne.
- P03 : page de sélection, vue « Titres trouvés » (48 titres réels), servie localement depuis le dépôt.
- P04 : collecte archivée rouverte dans la page de sélection, site en ligne.

Navigateur : Chromium seulement. Firefox, Safari et les lecteurs d'écran (NVDA, JAWS, VoiceOver) ne sont pas couverts.

## Préaudit outillé

Outil : campagne `audit-rgaa-creator` du kit DSFR, sans le collecteur AY11 (absent du poste).

- 27 règles exécutables, qui couvrent 23 des 258 tests ; 235 tests n'ont aucune règle automatique.
- 14 signaux, pour 2 causes.

Cause 1, critère 8.7 (changement de langue), 11 signaux « à confirmer ». Qualification après lecture des passages :

- fondé pour les libellés anglais de GitHub cités dans l'aide du jeton (« fine-grained », « Actions : Read and write », « Contents : Read », « repo ») : corrigé, ils portent `lang="en"` ;
- fondé pour « sitemaps » dans les lignes d'état des sources écrites par la page : corrigé, le texte dit « plans de site » ;
- non retenu pour « newsletter » (mot d'usage courant en français), « GitHub » et « robots.txt » (noms propres ou techniques) ;
- corrigé ensuite : les notes de collecte produites par le serveur disent « plan de site », et les messages d'erreur du jeton ne citent plus de libellé anglais. Les collectes archivées avant ce changement gardent leurs anciennes notes.

Cause 2, critère 8.9 (balise utilisée à des fins de présentation), 3 signaux : un paragraphe vide servant de région d'état. Corrigé, c'est maintenant un `div`. Les quinze autres paragraphes vides servant de zones de messages ont été convertis de même ; la position et la taille de chaque élément de la page ont été comparées avant et après, zones vides puis remplies, à 1280 et 375 px : aucune différence, hors trois listes situées dans des accordéons repliés, dont la position relevée varie aussi d'un relevé à l'autre sans aucun changement.

Les fichiers de l'outil sont dans `preaudit/`.

## Mesures dans le navigateur, par thème du RGAA

Ces mesures décrivent le DOM rendu. Elles ne valent pas décision de conformité.

Thèmes sans objet constaté sur les trois vues : images (aucune image ni SVG), cadres (aucun), multimédia (aucun), tableaux (aucun).

Couleurs (thème 3)
- Contraste du texte : 108 textes mesurés en vue titres, minimum 5,74 pour 1 ; 101 en vue paquet, minimum 4,87 pour 1, article écarté compris (corrigé le 14 novembre, il était à 3,51).
- Un contrôle automatique tiers (AccessLint) annonce 1 pour 1 sur des liens et 4,23 sur un texte des archives : non confirmé par la mesure directe.
- Un article écarté se distingue par son titre barré et sa case décochée, pas par la seule couleur.

Liens (thème 6)
- Aucun lien sans nom. Tous les liens ouvrant une nouvelle fenêtre le disent.
- « Consulter la publication » se répétait à l'identique pour chaque article (43 à 48 fois) : corrigé, le nom du lien porte le titre de l'article.

Scripts (thème 7)
- Accordéons : `aria-expanded` et `aria-controls` présents.
- Messages d'état : 10 régions `role="status"`, 4 `role="alert"`. La remise à zéro de la page a sa propre région.
- Boutons pendant une tâche : marqués `aria-disabled` plutôt que désactivés, pour garder le focus.

Éléments obligatoires (thème 8)
- `doctype`, langue `fr` et titre de page présents ; aucun identifiant dupliqué.

Structure (thème 9)
- Un `h1` par page, aucun saut de niveau (42, 10 et 65 titres selon la vue).
- `header`, `main`, `footer` et navigation nommée présents ; aucune liste mal formée.

Présentation (thème 10)
- Focus visible sur chaque arrêt de tabulation mesuré. Le bouton calendrier interne des champs date est dessiné par le navigateur.
- Agrandissement à 200 % (640 px) et redistribution à 320 px : pas de défilement horizontal.
- Espacement du texte augmenté (interligne 1,5, lettres 0,12 em, mots 0,16 em) : aucun texte rogné.

Formulaires (thème 11)
- 73 à 101 champs selon la vue, tous étiquetés ; chaque case et chaque liste nomme son article.
- Groupes de champs avec légende ; erreurs reliées aux champs par `aria-describedby` et `aria-invalid`.
- Champ du jeton en `autocomplete="off"` : choix assumé, la page promettant de ne rien enregistrer. Il écarte les gestionnaires de mots de passe (critère 11.13 à arbitrer).

Navigation (thème 12)
- Liens d'évitement vers le contenu et le pied de page, cibles présentes.
- Ordre de tabulation conforme à l'ordre visuel sur le parcours mesuré ; aucun `tabindex` positif ; pas de piège au clavier rencontré.
- Parcours complet au clavier joué dans `tests/navigateur/parcours.cjs`.

Consultation (thème 13)
- Aucune limite de temps imposée à la personne ; le suivi d'une tâche s'arrête de lui-même après 45 minutes sans rien lui faire perdre.

## Ce qui reste à faire pour un audit

- Décider humainement les tests applicables parmi les 258, avec preuve.
- Essayer avec un lecteur d'écran réel : annonces des régions d'état pendant une collecte, lecture des 48 titres, accordéons.
- Essayer dans Firefox et Safari.
- Arbitrer le champ du jeton (11.13).
- Rédiger la déclaration d'accessibilité, avec le moyen de signaler un problème, avant tout usage institutionnel.
