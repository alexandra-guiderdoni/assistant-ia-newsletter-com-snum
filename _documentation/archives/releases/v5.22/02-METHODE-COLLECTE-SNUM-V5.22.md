`SNUM_COLLECTE_V522_METHODE_START`

# Méthode Collecte sans état intermédiaire

## 1. Rechercher

Ordre immuable : `NUMERIQUE`, `IA`, `COMMANDE`, `RH`, `BERCY`, `RECOMPTER`.

Chaque lot de rubrique exécute exactement deux requêtes Web : une recherche française
large sans `site:`, puis une recherche ciblée avec `site:`. Chaque requête mentionne
la rubrique, la période et ses bornes ou son mois et son année. Ouvre les résultats
utiles ; ne simule jamais un appel Web.

Les cinq lots servent uniquement à constituer l’historique de sources de la
conversation. N’extrais les candidats qu’au tour `RECOMPTER`. Un résultat vide reste
un appel exécuté ; poursuis le lot suivant. Un échec technique réel donne
`A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`.

Axes de recherche :

- `NUMERIQUE` : services publics numériques, dématérialisation, inclusion, données ;
- `IA` : intelligence artificielle, modèles, régulation, usages publics ;
- `COMMANDE` : commande publique, achats, marchés et fournisseurs numériques ;
- `RH` : ressources humaines publiques, compétences, recrutement et formation ;
- `BERCY` : ministères économiques et financiers, directions et transformations.

## 2. Recompter

Relis toutes les sources Web citées pendant les cinq lots. Déduplique par URL canonique
HTTPS. Pour chaque URL, conserve : rubrique, titre, source, URL, date brute, date ISO
provisoire ou `INCONNUE`, accès intégral et fait essentiel.

Recalcule tous les candidats depuis zéro. Une date exacte contient jour, mois et année. Affiche pour
chaque URL `DATE_ISO_PROVISOIRE`, `BORNE_BASSE_OK`, `BORNE_HAUTE_OK` et
`DANS_FENETRE=OUI|NON`. `OUI` exige exactement
`DEBUT_ISO <= DATE_ISO_PROVISOIRE <= FIN_ISO`. Une date hors bornes, imprécise,
d’événement ou inconnue vaut `NON`.

`NB_DANS_FENETRE` égale uniquement le nombre d’URL canoniques uniques marquées `OUI`.
Sept candidats dont cinq `OUI` donne `NB_DANS_FENETRE = 5`.
Pour `2026-10-03..2026-10-13`, `2026-10-01` vaut `NON` et un mois seul reste
`INCONNUE` et `NON`. Si le nombre diffère du nombre de lignes `OUI`, corrige et
recompte. Moins de cinq donne
`A_COMPLETER | COLLECTE_INSUFFISANTE | NB_DANS_FENETRE=N` ; cinq ou plus donne
`COLLECTE_TERMINEE`.

## 3. Valider

Pendant `VALIDATION`, n’utilise pas le Web. Déduplique par URL canonique. Pour chaque
candidat, produis `CONTROLE_DATES` : titre, date brute, date ISO, bornes, accès,
`CLE_EVENEMENT` et décision. Une source est valide seulement si date, bornes et accès
valent `OUI`. Même fait réel = même clé ; conserve la source la plus directe, sinon la
plus récente, sinon la première. Place les autres dans `SOURCES_EXCLUES` avec
`DOUBLON_DE`. Vérifie `valides + exclues = candidats` avant
`VALIDATION_TERMINEE`.

`SNUM_COLLECTE_V522_METHODE_END`
