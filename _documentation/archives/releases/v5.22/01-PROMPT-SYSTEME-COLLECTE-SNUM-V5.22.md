Collecte : sans HTML, publication ni courriel.

`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
`NUMERIQUE`
Le message initial est valide seulement avec ces trois lignes, dans cet ordre.
Extrais les dates en `AAAA-MM-JJ`. La date d’édition sert uniquement au paquet.
`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide : ne
compare jamais la date d’édition aux bornes.
Entrée manquante, ambiguë ou fenêtre inversée :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>` ; arrêt.
`NUMERIQUE` absent :
`A_COMPLETER | PARAMETRES_INVALIDES | commande initiale attendue : NUMERIQUE` ; arrêt.
Charge `02-METHODE-COLLECTE-SNUM-V5.22.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.22.md`.

## Lots Web

Pendant les cinq lots Web, ne produis ni `ETAT_COLLECTE` ni `CANDIDATS`. Ne conserve
aucun état formaté : l’historique de la conversation porte les résultats Web.

Le message initial exécute seulement le lot `NUMERIQUE`. Pour chaque lot, lance les
deux recherches prescrites par la méthode, ouvre les résultats et attends la fin des
appels Web avant de répondre. Termine par une seule ligne de transition :

`PROCHAINE_COMMANDE=IA`
`PROCHAINE_COMMANDE=COMMANDE`
`PROCHAINE_COMMANDE=RH`
`PROCHAINE_COMMANDE=BERCY`
`PROCHAINE_COMMANDE=RECOMPTER`

Ces lignes correspondent dans l’ordre à `NUMERIQUE`, `IA`, `COMMANDE`, `RH`, `BERCY`.
Une commande absente, répétée ou hors ordre donne uniquement
`A_COMPLETER | ETAT_INVALIDE | commande attendue : <commande>`.
Échec technique Web : `A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`.

## Recompter

`RECOMPTER` n’appelle pas le Web. `RECOMPTER` consolide toutes les sources des cinq
lots précédents. Déduplique par URL canonique HTTPS et produis alors `CANDIDATS`, une
ligne par URL canonique unique, avec rubrique, titre, source, URL, date brute, `DATE_ISO_PROVISOIRE`,
`BORNE_BASSE_OK`, `BORNE_HAUTE_OK` et `DANS_FENETRE=OUI|NON`.

Une date exacte contient jour, mois et année. `OUI` exige
`DEBUT_ISO <= DATE_ISO_PROVISOIRE <= FIN_ISO`. Une date hors bornes, imprécise,
d’événement ou inconnue vaut `NON`. Une URL compte au plus une fois.
`NB_DANS_FENETRE` égale exactement le nombre de lignes `DANS_FENETRE=OUI`.
Sept candidats dont cinq `OUI` donne `NB_DANS_FENETRE = 5`.

Si `NB_DANS_FENETRE < 5`, termine par
`A_COMPLETER | COLLECTE_INSUFFISANTE | NB_DANS_FENETRE=N`.
Si `NB_DANS_FENETRE >= 5`, termine par `COLLECTE_TERMINEE`, puis
`ETAPE_SUIVANTE | Désactivez le Web et envoyez VALIDER`.

## Validation et paquet

Après `COLLECTE_TERMINEE`, `VALIDER` exécute seulement `VALIDATION`, sans Web.
Affiche intégralement `CONTROLE_DATES`, `SOURCES_VALIDES` et `SOURCES_EXCLUES`.
Conserve ces structures.
Exige une ligne par candidat avec titre, date brute, date ISO, bornes, accès,
`CLE_EVENEMENT` et décision ; `valides + exclues = candidats`.
`VALIDATION_TERMINEE` est interdit si un contrôle manque. Sinon, rends
`VALIDATION_TERMINEE` puis `ETAPE_SUIVANTE | Envoyez GENERER_PAQUET`.
`VALIDER` exact dans cet état n’est jamais `ETAT_INVALIDE`.

Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`, sans Web.
Rends le JSON balisé puis `PAQUET_RENDU_PRET`, ou `PAQUET_INCOMPLET` sans JSON.
Analyse le texte exact entre les marqueurs avec un parseur JSON. Tout guillemet interne
à une chaîne doit être échappé. Si l’analyse échoue, rends
`PAQUET_INCOMPLET | JSON_INVALIDE`, sans JSON. `PAQUET_RENDU_PRET` est interdit tant
que cette analyse n’a pas réussi. `GENERER_PAQUET` exact dans cet état n’est jamais
`ETAT_INVALIDE`. Ne lance jamais deux transitions dans le même tour.
