# Résultat de l’installation et de la recette V5.9

## Périmètre

Le 15 octobre 2026, le pack V5.9 a été installé dans le Projet unique `Newsletter SNUM` de l’Assistant DINUM. Le test porte sur l’édition du 14 octobre 2026 et la fenêtre inclusive du 3 au 13 octobre 2026.

Aucune publication GitHub Pages et aucun courriel n’ont été produits.

## Installation vérifiée

- prompt système : 3 740 caractères ;
- huit ressources Markdown présentes ;
- jetons `SNUM_CANON_V59_INDEX_START` et `SNUM_CANON_V59_INDEX_END` présents ;
- conversation créée depuis le Projet `Newsletter SNUM`.

## Première recette V5.9

La phase `COLLECTE` a exécuté dix requêtes couvrant les cinq rubriques et plus de cinq domaines. Elle a produit douze candidats et `COLLECTE_TERMINEE`.

La phase `VALIDATION` a contrôlé les douze candidats : six sources valides et six sources exclues. Les dates antérieures au 3 octobre et postérieures au 13 octobre ont été rejetées.

La phase `CANON` a retrouvé les six paires de fragments. La phase `RENDU` a toutefois recherché de nouveau le jeton d’index et s’est arrêtée avec `A_COMPLETER`.

Preuve : [conversation de la première recette](https://assistant.numerique.gouv.fr/chat/ac926e61-2b8a-4d4e-bfc3-e5b8e0b5de82).

## Correction appliquée

Le contrat a été précisé : `CANON` confirme la paire d’index et les six paires de fragments ; `RENDU` utilise les blocs affichés au tour précédent et ne recherche plus les ressources ni les jetons.

Le test de régression correspondant échoue avant la correction et réussit après celle-ci.

## Recette finale V5.9

La seconde phase `COLLECTE` a de nouveau satisfait le seuil de couverture et produit onze candidats.

La phase `VALIDATION` a conservé quatre sources et exclu sept candidats. Le total correspond aux onze candidats et aucune date hors fenêtre n’a été conservée.

La première exécution de `CANON` a rencontré une erreur technique générique de l’Assistant. Le bouton natif `Réessayer` a été utilisé une seule fois, sans nouveau message. La réponse suivante a confirmé la paire d’index et les six paires de fragments avec leurs blocs HTML.

La phase `RENDU` n’a plus signalé le jeton d’index comme introuvable. Elle a néanmoins répondu `A_COMPLETER` sans produire de HTML. Conformément au README, aucune demande de continuation forcée n’a été envoyée.

Preuve : [conversation de la recette finale](https://assistant.numerique.gouv.fr/chat/68369f19-beff-4a6d-a3d6-80903fdacc60).

## Contrôles locaux

- dix-huit tests unitaires réussis ;
- `KIT_PROGRESSIF_OK` ;
- Ruff sans erreur ;
- compilation Python réussie ;
- `git diff --check` sans erreur ;
- ZIP composé exactement des huit ressources ;
- empreinte SHA-256 : `8cda46828aa4ea249d359f3609175b4651573c56dec886e6168b6918d21f7ca4`.

## Verdict

La V5.9 corrige la collecte trop courte, la validation des dates et la transmission explicite du canon. Ces points sont observés dans l’Assistant.

Le résultat reste **NO-GO pour une livraison autonome du HTML identique à Bacoco**. Le garde-fou évite désormais de livrer un HTML non établi, mais l’assemblage final par l’Assistant reste non déterministe.
