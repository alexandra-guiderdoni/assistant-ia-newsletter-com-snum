# Rapport de recette V5.24 — Collecte et Rendu HTML

## Verdict

`GO` pour obtenir un JSON V519 exploitable dans `Newsletter SNUM - Collecte` en
mode assisté borné. La recette la plus récente du 17 octobre 2026 a produit trois
articles, trois essentiels, des dates admissibles, des URL uniques et un bloc
passerelle analysable.

`NO-GO` pour promettre une chaîne entièrement automatique. Après une recherche
Commande sans source, l’Assistant a répété `RECHERCHE_COMMANDE` au lieu de proposer
`RECHERCHE_RH`. Le premier `GENERER_PAQUET` a ensuite produit un schéma invalide et
une commande `CORRIGER_PAQUET` a été nécessaire. Un renforcement local de la table
de transitions, testé dans le Projet, n’a pas supprimé la répétition et n’a pas été
conservé.

Le même paquet a ensuite produit un rendu complet avec `HTML COMPLET`, un bloc de
`<!doctype html>` à `</html>` et le marqueur exact `HTML_CANONIQUE_PRODUIT`. Le cas
minimal sans essentiel reste refusé à tort par le Projet Rendu et n’est pas validé.

## Configuration du test mensuel

- édition : 17 octobre 2026 ;
- fenêtre inclusive : du 17 septembre au 16 octobre 2026 ;
- Collecte : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` et ses deux ressources ;
- preuve la plus récente :
  `https://assistant.numerique.gouv.fr/chat/6adae394-eea1-43a4-8d67-25ff01fed340/` ;
- preuve Rendu HTML :
  `https://assistant.numerique.gouv.fr/chat/35104da3-8254-4bce-be7f-ea80f6ff8dfb/`.

## Résultat de la recette la plus récente

Les cinq lots ont été exécutés dans l’ordre. Le lot Commande n’a fourni aucune
source et l’Assistant a proposé de le rejouer ; la recette a continué en envoyant
manuellement `RECHERCHE_RH`. Le lot Bercy sans source a, lui, correctement terminé
la collecte et proposé `VALIDER`.

`VALIDER` a conservé une source Numérique, une source IA et une source RH, mais a
choisi la plus ancienne des deux sources IA. Le premier paquet utilisait une racine
`metadata`, des champs non contractuels et aucun article essentiel. La commande
`CORRIGER_PAQUET` a sélectionné la source IA la plus récente et produit un paquet
V519 conforme aux contrôles suivants :

- JSON analysable et sept clés racine exactes ;
- identifiants `U01`, `U02`, `U03` sans trou ;
- rubriques et URL uniques ;
- trois dates dans la fenêtre inclusive ;
- exactement trois `essential=true` ;
- `watch` non vide et marqueurs complets jusqu’à `PAQUET_RENDU_PRET`.

Le premier passage dans le Projet Rendu a mis en évidence deux coquilles dans sa
configuration active : `22-CANOON…` et `HTML_CANNIQUE_PRODUIT`. Le prompt versionné
contenait déjà les valeurs correctes. Après synchronisation du Projet, une conversation
neuve a produit directement le résultat attendu. Le contrôle du HTML copié confirme :

- un document de `<!doctype html>` à `</html>` sans marqueur `@@` ;
- un seul `h1`, trois cartes essentielles et les cinq sections attendues ;
- les trois accès rapides, les CSS et scripts DSFR 1.15.2 ;
- chacune des trois URL présente dans sa carte essentielle et sa rubrique ;
- un unique `## HTML COMPLET`, un unique `## CONTROLES` et le marqueur final exact.

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

Cette normalisation reste une garde documentaire et locale. La recette réelle montre
qu’une commande `CORRIGER_PAQUET` peut encore être nécessaire. Elle ne prétend pas
automatiser les tours de recherche Web : le métier reste responsable d’activer le
Web, d’envoyer chaque requête et de vérifier les sources visibles.

## Contrôles locaux

- test négatif ajouté puis rendu vert pour la normalisation du paquet ;
- 81 tests `unittest` réussis ;
- Ruff réussi sur `scripts` et `tests` ;
- kit régénéré, puis contrôle `KIT_DECOUPLE_OK` réussi ;
- contrôle `git diff --check` réussi ;
- prompt Collecte à 3 975 caractères, méthode à 3 590 et contrat à 3 499 ;
- `README.md` et `NOTICE-V5.24.md` identiques ;
- recette réelle postérieure à la correction : exécutée, avec un passage forcé et
  une commande `CORRIGER_PAQUET` ;
- recette Rendu HTML postérieure à la synchronisation : réussie dès le premier message.

Les contrôles locaux vérifient la cohérence du kit, pas l’obéissance du modèle dans
l’Assistant. La recette réelle confirme que les règles seules ne rendent pas cette
chaîne déterministe.

## Consigne pour la présentation

Présenter le dispositif comme un mode best effort assisté : cinq recherches validées
par le métier, puis `VALIDER` et `GENERER_PAQUET`. Vérifier avant le passage au Rendu
qu’il existe au plus un article par rubrique, des identifiants `U01…UN` sans trou et
exactement trois essentiels dès que le paquet contient au moins trois articles.
