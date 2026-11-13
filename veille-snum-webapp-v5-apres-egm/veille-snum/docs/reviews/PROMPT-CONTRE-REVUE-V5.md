# Mission AlexDot : Contre-revue EGM indépendante de Veille SNUM V5

**Cible** : archive V5 à fournir avec `NOTE-V5-APRES-CONTRE-REVUE.md` et la contre-revue V4. Agis comme trois relecteurs Goldfish réellement isolés, puis consolide leurs constats. Ne traite aucune affirmation du développeur comme preuve. Si l'isolation est impossible, le signaler.

## Invariants non négociables

14 sources identiques (dont interne désactivée), cinq rubriques, Collecte V5.23 et paquet V519 inchangés, aucun changement des rendus ou du builder. Pas de clé réelle, ni donnée interne, ni publication.

## Zoom Out / YAGNI

Évalue si Web Locks, collecte directe, extraction, rapport et tests sont la solution la plus sobre ; détecte abstractions ajoutées sans besoin, complexité accidentelle et dépendances fragiles. N'ajoute pas de moteur Web payant sans mesure du rappel.

## Design Critic / sécurité et qualité des faits

Rejoue indépendamment F02/F03 : identités JSON-LD imbriquées/liste, alias valides, identités `WebPage` ambiguës ; paywalls sur pages principales ou recommandées ; alertes de vérification, citation du même texte dans un article, restrictions et extraits insuffisants. Rejoue F04/F05 : robots refusant sitemap, enfants en erreur, comptages, pertes et motifs. Rejoue F09 : redirections 301/302/303/307/308 avant/après échéance, budget dans robots, timeout restant. Vérifie que F01 refuse toujours tout redirect Albert ; ne charge jamais de vraie clé dans les sondes.

**S03** : tester dans un VRAI navigateur si possible deux onglets V5, suppression/rotation concurrentes, changement de modèle, anciennes pages V4 ouvertes, reprise du port, absence de Web Locks, politique serveur désactivée. La présence d'une Web Locks API ne prouve ni la bonne transaction ni la sécurité des anciens onglets. En défaut de navigateur, distinguer simulation et absence de recette. Considérer la persistance non approuvée sur poste institutionnel.

## Implementation Readiness

Vérifie les 40 tests Python et 16 Node fournis, **leurs assertions**, puis cherche des contre-exemples voisins. Vérifie la provenance des rapports R01 avec et sans Albert ; nom de fichier non dépendant des champs modifiés. Teste la compatibilité du JSON sur le convertisseur distribué, sans modifier le builder. Vérifie la cohérence README/design/code, délais d'exécution et états HTTP, les erreurs de stockage, les annonces/focus/zoom/lecteurs d'écran si l'environnement le permet.

## Rapport attendu

Produis `CONTRE-REVUE-EGM-VEILLE-SNUM-V5.md` avec : statut unique (REFUSÉ / EXPÉRIMENTAL UNIQUEMENT / PILOTE EXPLORATOIRE CONDITIONNEL / PILOTE EXPLORATOIRE AUTORISABLE), tableau F01-F09/S01-S03/R01 avec gravité, preuves précises (fichier/lignes, exécution ou simulation), nouveaux défauts, corrections minimales et tests de non-régression. Inclure les SHA des pièces examinées, les reproductions et les limites. Ne pas annoncer la production prête sans recette réelle de réseau, navigateur, sécurité, droits et accessibilité.

Ne rien modifier dans `main`, les 14 sources ni le builder. Les correctifs proposés restent sur copie de travail et doivent être identifiés comme proposés, non effectués.
