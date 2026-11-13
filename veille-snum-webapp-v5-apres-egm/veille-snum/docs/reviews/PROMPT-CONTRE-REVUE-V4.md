# AlexDot : mission de contre-revue EGM V4 en contexte neuf

Évalue l'archive `veille-snum-webapp-v4-egm-correctifs.zip` sans accepter la note V4 comme preuve. Conserve les trois évaluations indépendantes Zoom Out/YAGNI, Design Critic/Security et Implementation Readiness. Réexécute les 28 tests Python et les 9 tests Node, puis crée tes propres contre-exemples. Tu peux améliorer les correctifs sur une copie, jamais sur `main` sans validation.

1. F02 : tester les contradictions de `url`, `@id`, `mainEntityOfPage`, la date d'article dans une annexe, les métadonnées dans des zones masquées, et vérifier que le vrai article conserve sa date.
2. F03 : tester challenges visibles, `isAccessibleForFree:false`, pages hybrides, vrais articles traitant de CAPTCHA; qualifier les faux négatifs et faux positifs sans contourner les restrictions.
3. F04/F05 : tester les 13 sitemaps en timeout, la découverte vide sans erreur, les plafonds locaux/globaux, la présence des URL non analysées et les alertes `watch`.
4. F09 : vérifier qu'aucune requête HTTP de collecte ne démarre après l'échéance simulée. Signaler les dépassements possibles durant une requête et les règles de transition des états.
5. S01/S03 : reproduire le scénario où A efface et B tente de réenregistrer sa copie périmée, avec et sans événement `storage`; ajouter les scénarios de collision simultanée, impossibilité de suppression et changement de clé. Ne pas considérer `localStorage` comme sécurisé.
6. S02 : vérifier CSP réellement délivrée par HTTP, interdiction d'exécuter du script injecté, absence de secret dans les rapports, Host/Origin, redirections Albert (301/302/303/307/308), proxies, risques de même origine après reprise du port.
7. Contrat : comparer les 14 sources bit à bit avec V3, vérifier V519 et le convertisseur distribué sans modifier `builder-mail-dsfr`.
8. Réaliser clavier/VoiceOver/NVDA, zoom/reflow et recette macOS seulement si l'environnement le permet; sinon indiquer explicitement « non exécuté ».

Pour chaque constat : ID, gravité, preuve/chemin/lignes, impact, correction minimale, test et statut. Distinguer code inspecté, simulations, tests réels et hypothèses. Conclure par **REFUSÉ / EXPÉRIMENTAL UNIQUEMENT / PILOTE EXPLORATOIRE CONDITIONNEL / PILOTE EXPLORATOIRE AUTORISABLE**, sans autoriser une vraie clé sur la seule réussite des tests. Aucun moteur payant n'est à ajouter sans mesure de quatre semaines.
