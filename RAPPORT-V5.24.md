# Rapport de recette V5.24 — Collecte et Rendu HTML

## Verdict

`GO` pour obtenir un JSON V519 complet dans `Newsletter SNUM - Collecte` en mode
assisté borné. Le test mensuel du 17 octobre 2026 a produit cinq articles, un par
rubrique, avec trois essentiels, des dates admissibles et des URL uniques.

`NO-GO` pour promettre une chaîne entièrement automatique. Deux recherches ciblées
et deux commandes `CORRIGER_PAQUET` ont été nécessaires. Les consignes actives ont
été renforcées après cette recette pour intégrer les deux corrections du paquet ;
leur effet dans l’Assistant reste à tester dans une conversation neuve.

Le rendu HTML de ce nouveau paquet n’a pas été exécuté. Une recette antérieure avait
produit `HTML COMPLET` avec cinq articles. Le cas minimal sans essentiel reste refusé
à tort par le Projet Rendu et n’est pas validé.

## Configuration du test mensuel

- édition : 17 octobre 2026 ;
- fenêtre inclusive : du 17 septembre au 16 octobre 2026 ;
- Collecte : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` et ses deux ressources ;
- preuve :
  `https://assistant.numerique.gouv.fr/chat/7f780b8c-04fe-44f9-95cb-48795916a6b8` ;
- Rendu HTML : non testé avec ce paquet.

## Résultat observé

Les cinq recherches initiales ont fourni quatre sources admissibles réparties dans
trois rubriques. Numérique était hors fenêtre et Bercy sans source prouvée. Une
recherche ciblée pour chacune de ces deux rubriques a ensuite trouvé une source
admissible.

Après `VALIDER`, le registre comportait six sources valides dans cinq rubriques. Le
premier `GENERER_PAQUET` présentait deux écarts : aucun article essentiel et une copie
du JSON avant le marqueur `SNUM_PAQUET_RENDU_V519_START`. Une première correction a
fixé ces écarts. Une seconde a supprimé le deuxième article IA pour respecter la
règle d’un article par rubrique.

Le paquet final contrôlé possède :

- le schéma `SNUM_PAQUET_RENDU_V519` et les sept clés racine attendues ;
- cinq articles dans l’ordre Numérique, IA, Commande, RH et Bercy ;
- une seule URL et un seul identifiant par article ;
- cinq dates comprises dans la fenêtre inclusive ;
- exactement trois `essential=true` ;
- un seul bloc délimité, suivi de `PAQUET_RENDU_PRET`.

## Correction intégrée aux consignes

`VALIDER` conserve désormais une seule source par rubrique : la date ISO la plus
récente, puis le plus petit identifiant en cas d’égalité. `GENERER_PAQUET` trie les
rubriques, renumérote les articles `U01…UN`, affecte les trois essentiels et interdit
tout brouillon ou deuxième JSON.

Cette correction vise uniquement les deux tours `CORRIGER_PAQUET`. Elle ne prétend
pas automatiser les tours de recherche Web : le métier reste responsable d’activer
le Web, d’envoyer chaque requête et de vérifier les sources visibles.

## Contrôles locaux

- test négatif ajouté puis rendu vert pour la normalisation du paquet ;
- 81 tests `unittest` réussis ;
- Ruff réussi sur `scripts` et `tests` ;
- kit régénéré, puis contrôle `KIT_DECOUPLE_OK` réussi ;
- contrôle `git diff --check` réussi ;
- prompt Collecte à 3 975 caractères, méthode à 3 590 et contrat à 3 499 ;
- `README.md` et `NOTICE-V5.24.md` identiques ;
- recette réelle postérieure à la correction : non exécutée.

Les contrôles locaux vérifient la cohérence du kit, pas l’obéissance du modèle dans
l’Assistant. Seule une nouvelle recette réelle pourra confirmer la suppression des
deux commandes de correction.

## Consigne pour la présentation

Présenter le dispositif comme un mode best effort assisté : cinq recherches validées
par le métier, puis `VALIDER` et `GENERER_PAQUET`. Vérifier avant le passage au Rendu
qu’il existe au plus un article par rubrique, des identifiants `U01…UN` sans trou et
exactement trois essentiels dès que le paquet contient au moins trois articles.
