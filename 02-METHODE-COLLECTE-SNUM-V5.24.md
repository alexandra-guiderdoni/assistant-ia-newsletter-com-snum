`SNUM_COLLECTE_V524_METHODE_START`
## 1. Préparer les requêtes
Une seule recherche est demandée par message. Produis `REQUETE_A_ENVOYER=<texte>`
avec dates et code exact, puis demande explicitement une recherche sur le Web.
Ordre immuable : `RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→`RECHERCHE_RH`→`RECHERCHE_BERCY`→`COLLECTE_TERMINEE_BEST_EFFORT`; suivant≠reçu.
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
date n’est pas exacte. Pour `2026-10-03..2026-10-13`, le `2026-10-01` vaut
`NON` ; `2026-10-04` et `2026-10-11` valent `OUI`. Termine par
`VALIDATION_METIER_REQUISE`. Tout résultat avance, même `DANS_FENETRE=NON`.
Sans source visible, rends `RESULTATS_RECHERCHE=AUCUNE_SOURCE_PROUVEE`, recopie
`REGISTRE_CUMULATIF` avec le registre inchangé, puis rends
`RECHERCHE_SANS_SOURCE_PROUVEE | <rubrique>` et `VALIDATION_METIER_REQUISE`.
Avance à la requête suivante de l’ordre immuable ; ne relance jamais la même rubrique.
## 3. Terminer la collecte en best effort
Après chacune des quatre premières recherches, affiche la requête suivante de
l’ordre immuable. Après `RECHERCHE_BERCY`, recopie le registre, rends
`COLLECTE_TERMINEE_BEST_EFFORT`, désactive le Web et affiche
`REQUETE_A_ENVOYER=VALIDER`. Aucun compteur ni seuil ne bloque cette transition.
## 4. Valider
Pendant `VALIDATION`, n’utilise pas le Web. Pour chaque entrée du registre, produis
`CONTROLE_DATES` : titre, dates brute/ISO, bornes, accès, `CLE_EVENEMENT` et décision.
À `VALIDER`, recalcule `DANS_FENETRE` depuis la date ISO et les bornes ;
ignore `OUI`/`NON` mémorisé. Pour
`2026-09-17..2026-10-16`, `2026-09-09` vaut `NON`. Une source est valide si le
`DANS_FENETRE` recalculé et l’accès valent `OUI`.
À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; ne demande rien à
l’utilisateur et ne bloque jamais sur un nombre minimal de sources.
Même fait=même clé: source directe, sinon récente, sinon première; autres dans
`SOURCES_EXCLUES` avec `DOUBLON_DE`. Garde une seule source valide par rubrique :
date ISO la plus récente, puis le plus petit `Uxx`; exclus les autres avec
`AUTRE_SOURCE_RUBRIQUE`.
Vérifie `valides + exclues = registre` avant `VALIDATION_TERMINEE`. Si moins de
cinq sources sont valides, signale l’insuffisance dans `watch` sans bloquer le JSON.
Un registre vide reste valide : rends les trois blocs vides puis
`VALIDATION_TERMINEE`. Le paquet contient `articles=[]` et `watch` signale les
rubriques sans source prouvée.
Après `VALIDATION_TERMINEE`, affiche `REQUETE_A_ENVOYER=GENERER_PAQUET`. Le paquet
reprend exactement le schéma et les marqueurs `SNUM_PAQUET_RENDU_V519` du contrat :
clés racines `schema_version`, `edition_date`, `edition_date_long`, `window_start`,
`window_end`, `articles`, `watch`; jamais `metadata` ni `sources`.
À la génération, renumérote les articles `U01…UN` sans trou, applique les essentiels
et émets directement le bloc final, sans brouillon.
`SNUM_COLLECTE_V524_METHODE_END`
