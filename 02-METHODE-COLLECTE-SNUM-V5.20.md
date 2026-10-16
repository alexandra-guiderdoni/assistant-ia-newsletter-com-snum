`SNUM_COLLECTE_V520_METHODE_START`

# Contrat Collecte et Validation

Pendant `COLLECTE`, suis ces trois étapes dans l’ordre. N’écris rien avant la fin des
appels Web requis.

## 1. EXÉCUTER

`PASSE_1` : dix requêtes, deux par rubrique (`NUMERIQUE`, `INTELLIGENCE ARTIFICIELLE
(IA)`, `COMMANDE PUBLIQUE`, `RESSOURCES HUMAINES`, `VIE DE BERCY`). Pour chacune :
une requête sans `site:`, puis une avec `site:` ; couvre au moins cinq domaines.
Chaque requête cible explicitement la fenêtre par ses bornes, ou son mois et son
année. Ouvre les résultats ; `EXECUTEE` exige un appel Web examiné.

Ne filtre aucun candidat selon sa date. Garde chaque page lue : titre, URL canonique
HTTPS, date de publication, accès intégral, fait essentiel. Si le premier calcul
trouve moins de cinq candidats datés provisoirement, exécute une seconde passe
(`PASSE_2`) : exactement cinq requêtes ciblées, une par rubrique, avec synonymes et
domaines absents de `PASSE_1`. Ouvre les résultats. Pas de
`COLLECTE_INSUFFISANTE` après la seule première passe.

## 2. CALCULER

Fige la liste et recalcule chaque `DANS_FENETRE` depuis zéro. Affiche par candidat
`DATE_ISO_PROVISOIRE` (`AAAA-MM-JJ` ou `INCONNUE`) et `DANS_FENETRE=OUI|NON`. Pour
la date exacte de publication (jour, mois et année) :
`BORNE_BASSE_OK=OUI` si date ISO `>= DEBUT_ISO`, sinon `NON` ;
`BORNE_HAUTE_OK=OUI` si date ISO `<= FIN_ISO`, sinon `NON`.
Si l’un vaut `NON`, impose `DANS_FENETRE=NON`. `OUI` exige
`DEBUT_ISO <= DATE_ISO_PROVISOIRE <= FIN_ISO`. Une date ISO `< DEBUT_ISO` ou
`> FIN_ISO`, d’événement, imprécise ou inconnue vaut `NON`.

Audit bloquant : aucune date hors bornes n’est marquée `OUI` ; `NB_DANS_FENETRE`
égale les URL canoniques uniques marquées `OUI`. Sinon, corrige puis recompte avant
d’afficher. Recompte après `PASSE_1`, puis après la dernière passe.

## 3. RENDRE

Rends une seule réponse complète : `TRACE_RECHERCHE` avec `PASSE_1`, puis `PASSE_2`
si requise. Chaque ligne donne `REQUETE`, `STATUT_WEB=EXECUTEE` et
`URL_EXAMINEES` ou `AUCUNE`. Jamais `EXECUTEE` sans appel Web examiné.
`COLLECTE_INSUFFISANTE` exige 10 requêtes `EXECUTEE` en `PASSE_1` et 5 en `PASSE_2`.
Un échec Web impose
`A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`.

Puis `COUVERTURE_COLLECTE`, `CANDIDATS` et, une seule fois, `NB_DANS_FENETRE`.
Branche terminale unique : si `NB_DANS_FENETRE >= 5`, rends `COLLECTE_TERMINEE`, puis
`ETAPE_SUIVANTE | Envoyez VALIDER`. Sinon, après deux passes insuffisantes, rends
`A_COMPLETER`, `## CONTROLES_EN_ECHEC`, puis
`COLLECTE_INSUFFISANTE | NB_DANS_FENETRE=N`.

Pendant `VALIDATION`, pas de Web. Pour chaque candidat, produis `CONTROLE_DATES` :
titre, date brute, format `AAAA-MM-JJ`, deux bornes, accès, `CLE_EVENEMENT`, décision.
Trace séparément `date ISO >= DEBUT_ISO` et `date ISO <= FIN_ISO`, valeurs comparées
et verdict `OUI|NON`. Déduplique d’abord par URL canonique. Une source est valide si
format, bornes et accès valent `OUI`. Même fait réel = même clé. Garde la source la
plus directe, sinon la plus récente, sinon la première ; exclus chaque doublon avec
`DOUBLON_DE | titre conservé`. Contrôle toutes les entrées de `CANDIDATS`, vérifie
`valides + exclues = candidats`, puis rends `VALIDATION_TERMINEE` seulement si
l’égalité est exacte et qu’une source reste valide.

## Sorties persistantes entre les tours

`COLLECTE` conserve intégralement `COUVERTURE_COLLECTE` et `CANDIDATS` pour
`VALIDATION`. Celle-ci conserve `CONTROLE_DATES`, `SOURCES_VALIDES` et
`SOURCES_EXCLUES` pour `PAQUET`. Aucun résumé ne les remplace.

`SNUM_COLLECTE_V520_METHODE_END`
