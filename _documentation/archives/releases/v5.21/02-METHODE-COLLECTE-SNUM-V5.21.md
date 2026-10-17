`SNUM_COLLECTE_V521_METHODE_START`

# Méthode Collecte séquentielle

## 1. État persistant visible

Pendant `COLLECTE`, exécute une seule rubrique par tour et deux requêtes Web au maximum
par tour. Réaffiche intégralement `ETAT_COLLECTE` après chaque lot. Il contient :
`DATE_EDITION_ISO`, `DEBUT_ISO`, `FIN_ISO`, `PASSE`, `RUBRIQUES_TERMINEES`, toutes les
lignes de `TRACE_RECHERCHE`, tous les `CANDIDATS` et `PROCHAINE_COMMANDE`.

Ne remplace, ne résume et ne retire aucune donnée antérieure. Déduplique seulement
par URL canonique HTTPS ; enrichis alors l’entrée existante. Si l’état antérieur est
indisponible ou contradictoire, rends `A_COMPLETER | ETAT_PERDU` sans poursuivre.

## 2. Lots de recherche

Ordre immuable : `NUMERIQUE`, `IA`, `COMMANDE`, `RH`, `BERCY`, `RECOMPTER`.

En `PASSE_1`, chaque lot de rubrique exécute exactement deux requêtes : une sans
`site:`, puis une avec `site:`. La requête mentionne la rubrique, la période et ses
bornes ou son mois et son année. Ouvre les résultats. Une ligne `EXECUTEE` exige un
appel Web réellement examiné et donne `REQUETE`, `STATUT_WEB=EXECUTEE` et
`URL_EXAMINEES`, ou `AUCUNE` si aucun résultat n’existe.
`AUCUNE` reste un lot exécuté et n’est pas `OUTIL_WEB_INDISPONIBLE` ; poursuis avec
la commande suivante.

Après le premier `RECOMPTER`, démarre `PASSE_2` seulement si moins de cinq URL uniques
sont admissibles. Chaque lot de rubrique exécute alors exactement une requête ciblée,
avec synonymes et domaines absents de `PASSE_1`. Après ses cinq lots, `RECOMPTER`
effectue le verdict final. Un échec technique donne
`A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`.

Pour chaque page lue, conserve : rubrique, titre, URL canonique, source, date brute,
date ISO provisoire ou `INCONNUE`, accès intégral et fait essentiel. Ne filtre aucun
candidat avant `RECOMPTER`.

## 3. Recompter

Recalcule tous les candidats depuis zéro. Une date exacte doit contenir jour, mois et
année. Pour chaque URL, affiche `DATE_ISO_PROVISOIRE`, `BORNE_BASSE_OK`,
`BORNE_HAUTE_OK` et `DANS_FENETRE=OUI|NON`. `OUI` exige exactement
`DEBUT_ISO <= DATE_ISO_PROVISOIRE <= FIN_ISO`. Une date hors bornes, imprécise,
d’événement ou inconnue vaut `NON`.

`NB_DANS_FENETRE` égale uniquement le nombre d’URL canoniques uniques marquées `OUI`.
Exemple bloquant : sept candidats dont cinq `OUI` donne
`NB_DANS_FENETRE = 5`. Pour la fenêtre `2026-10-03..2026-10-13`, `2026-10-01` vaut
`NON` ; un mois seul reste `INCONNUE` et `NON`. Si le nombre affiché diffère du nombre
de lignes `OUI`, corrige et recompte.

Après `PASSE_1`, un résultat inférieur à cinq déclenche `PASSE_2`, jamais
`COLLECTE_INSUFFISANTE`. Après `PASSE_2`, moins de cinq donne l’échec terminal. Cinq ou
plus donne `COLLECTE_TERMINEE`.

## 4. Validation

Pendant `VALIDATION`, n’utilise pas le Web. Déduplique d’abord par URL canonique. Pour
chaque candidat, produis `CONTROLE_DATES` : titre, date brute, date ISO, bornes, accès,
`CLE_EVENEMENT` et décision. Une source est valide seulement si date, bornes et accès
valent `OUI`. Même fait réel = même clé ; conserve la source la plus directe, sinon la
plus récente, sinon la première. Place les autres dans `SOURCES_EXCLUES` avec
`DOUBLON_DE`. Vérifie `valides + exclues = candidats` avant
`VALIDATION_TERMINEE`.

Conserve intégralement `CONTROLE_DATES`, `SOURCES_VALIDES` et `SOURCES_EXCLUES` pour
`PAQUET`. Aucun résumé ne les remplace.

`SNUM_COLLECTE_V521_METHODE_END`
