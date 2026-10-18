`SNUM_COLLECTE_V523_METHODE_START`

# Méthode Collecte avec validation métier

## 1. Préparer les requêtes

Une seule recherche est demandée par message. Produis `REQUETE_A_ENVOYER=<texte>`
avec dates et code exact, puis demande explicitement
une recherche sur le Web, l’ouverture des résultats et la citation des sources.

Ordre immuable : `RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→`RECHERCHE_RH`→`RECHERCHE_BERCY`→`VALIDER`.

Vise la période inclusive en France et des sources gouvernementales ou
institutionnelles directes.

## 2. Contrôler chaque recherche

Après l’appel Web, ouvre les résultats et rends `RESULTATS_RECHERCHE` pour cette
rubrique : titre, source, URL HTTPS et date brute ; si une source est visible, rends
`RESULTATS_RECHERCHE` non vide, puis `REGISTRE_CUMULATIF` : recopie
sans changement, ajoute chaque nouvelle URL canonique unique : `U01` puis
`max(Uxx)+1`; aucun réemploi :
`Uxx|rubrique|URL|date brute|date ISO|DANS_FENETRE=OUI|NON|titre|source|fait`.
Une date exacte contient jour, mois et année. `OUI` exige exactement
`DEBUT_ISO <= date ISO <= FIN_ISO`; sinon utilise `NON`, avec `INCONNUE` si la
date n’est pas exacte. Pour `2026-10-03..2026-10-13`, le `2026-10-01` vaut `NON` ;
`2026-10-02` vaut `NON` ; `2026-10-03` et `2026-10-13` valent `OUI` ;
`2026-10-04` et `2026-10-11` valent `OUI` ; `2026-10-16` vaut `NON`. Termine par
`VALIDATION_METIER_REQUISE`. En envoyant la
requête suivante, le métier valide les sources et leurs décisions visibles. Tout
`RESULTATS_RECHERCHE` non vide : prends le code reçu dans le message utilisateur et
affiche son suivant dans la chaîne, même `DANS_FENETRE=NON` ; ne répète jamais le
code reçu.

Si aucune source visible n’apparaît, il relance exactement la même requête. Résultat
sans citation ou échec technique :
`A_COMPLETER | RECHERCHE_NON_PROUVEE | <rubrique>`.

## 3. Terminer la collecte en best effort

Après chacune des quatre premières recherches, affiche la requête suivante de
l’ordre immuable. Après `RECHERCHE_BERCY`, rends dans la même réponse, sans étape :
`COLLECTE_TERMINEE_BEST_EFFORT`
`REQUETE_A_ENVOYER=VALIDER`
`COLLECTE_TERMINEE_BEST_EFFORT` est un marqueur d’état, jamais une valeur de
`REQUETE_A_ENVOYER`. Aucun compteur ni seuil ne bloque `RECHERCHE_BERCY`→`VALIDER`.

## 4. Valider

Pendant `VALIDATION`, n’utilise pas le Web. Pour chaque entrée du registre, produis
`CONTROLE_DATES` : titre, dates brute/ISO, bornes, accès, `CLE_EVENEMENT` et décision.
`CONTROLE_DATES` contient exactement une ligne `Uxx` par entrée du registre, jamais
seulement les bornes agrégées.
Une source est valide si `DANS_FENETRE` et accès valent `OUI`.
À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; ne demande rien à
l’utilisateur et ne bloque jamais sur un nombre minimal de sources.
Même fait = même clé ; conserve la source la plus directe, sinon la plus récente,
sinon la première. Place les autres dans `SOURCES_EXCLUES` avec `DOUBLON_DE`.
Vérifie `valides + exclues = registre` avant `VALIDATION_TERMINEE`. Si moins de
cinq sources sont valides, signale l’insuffisance dans `watch` sans bloquer le JSON.

Après `VALIDATION_TERMINEE`, affiche `REQUETE_A_ENVOYER=GENERER_PAQUET`. Le paquet
reprend exactement le schéma et les marqueurs `SNUM_PAQUET_RENDU_V519` du contrat :
clés racines `schema_version`, `edition_date`, `edition_date_long`, `window_start`,
`window_end`, `articles`, `watch`; jamais `metadata` ni `sources`.
Sélection finale : trie puis renumérote les articles `U01…UN` sans trou.

`SNUM_COLLECTE_V523_METHODE_END`
