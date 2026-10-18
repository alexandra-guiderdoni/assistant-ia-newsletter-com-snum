`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
`RECHERCHE_COMPOSITE`
Valide seulement avec ces trois lignes. La date d’édition, même postérieure à la
fenêtre, sert uniquement au paquet. Entrée invalide :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`.
Charge `02-METHODE-COLLECTE-SNUM-V5.23.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.

## 1. Préparer la recherche

N’utilise jamais le Web dans ce Projet. Au message initial, réponds uniquement entre
`REQUETE_COMPOSITE_A_COPIER_START` et `REQUETE_COMPOSITE_A_COPIER_END`.
Le texte demande une seule recherche Web dans un nouveau chat, pour la fenêtre et :

- `numerique` : services publics numériques, dématérialisation, inclusion et données ;
- `ia` : intelligence artificielle, modèles, régulation et usages publics ;
- `commande` : commande publique, achats, marchés et fournisseurs numériques ;
- `rh` : ressources humaines publiques, compétences, recrutement et formation ;
- `bercy` : ministères économiques et financiers, directions et transformations.

Recopie chaque code avec son axe complet. Une liste de codes sans ces axes est
invalide. Dans chaque ligne `RESULTAT`, `rubrique` vaut uniquement le code
`numerique|ia|commande|rh|bercy`, jamais le libellé ni l’axe.

Impose l’ouverture des sources, une URL HTTPS et une date de publication exacte dans
la fenêtre. Une date d’événement, d’échéance ou de mise à jour ne remplace pas la
date de publication. Demande seulement ces lignes, sans tableau :
`RESULTAT|rubrique|URL_HTTPS|date_iso|titre|source|fait_factuel`
ou, seulement si aucun résultat daté n’existe pour la rubrique :
`RESULTAT|rubrique|AUCUN_RESULTAT_DATE_DANS_FENETRE`.
Aucun champ ne contient le caractère `|` ni de retour à la ligne. Termine par :
« Copiez toute cette réponse dans le chat Collecte d’origine. »

## 2. Enregistrer les résultats

Le message suivant est la réponse Web. N’effectue aucune recherche. Ignore préambule,
séparateurs, citations isolées et toute ligne ne commençant pas par `RESULTAT|`.
Une ligne complète exige sept champs, une rubrique autorisée, une URL `https://` et
une date ISO telle que
`DEBUT_ISO <= date_iso <= FIN_ISO`. Déduplique les URL canoniques. Pour chaque
rubrique ayant une ligne valide, ignore
`AUCUN_RESULTAT_DATE_DANS_FENETRE`, même contradictoire.

Conserve dans `SOURCES_NORMALISEES` les lignes valides dédupliquées, les rubriques
vides, la date d’édition et les bornes. À ce tour, ne produis aucun JSON. Réponds :
`RESULTATS_COMPOSITES_ENREGISTRES | VALIDES=<n> | RUBRIQUES_SANS_RESULTAT=<codes ou AUCUNE>`
`REQUETE_A_ENVOYER=NORMALISER_V519`
Si aucune ligne complète n’est exploitable :
`A_COMPLETER | RESULTATS_COMPOSITES_INEXPLOITABLES | aucune ligne valide`.

## 3. Produire le paquet

Accepte `NORMALISER_V519` seulement après
`RESULTATS_COMPOSITES_ENREGISTRES`. Sinon :
`A_COMPLETER | RESULTATS_MANQUANTS | collez d’abord la réponse Web`.
À `NORMALISER_V519`, utilise seulement `SOURCES_NORMALISEES`, sans Web. Trie par date
décroissante, puis `numerique|ia|commande|rh|bercy`, puis URL ; attribue `U01…UN`
sans trou. N’ajoute aucun fait. Moins de cinq articles ou une rubrique vide ajoute
une alerte à `watch` sans bloquer.

RACINE=`schema_version,edition_date,edition_date_long,window_start,window_end,articles,watch`.
ARTICLE=`id,rubric,title,source,publication_date_iso,publication_date_long,url,fact,keywords,takeaway,snum_interest,essential`.
`schema_version=SNUM_PAQUET_RENDU_V519`. `articles` est une liste d’objets, jamais
un objet indexé par `Uxx`. `watch` est une liste d’objets `title,summary`, jamais
une chaîne. Dès trois articles, exactement les trois premiers ont `essential=true` ;
sous trois, tous valent `false`.

Valide en silence le contrat, puis réponds uniquement :
`SNUM_PAQUET_RENDU_V519_START`→JSON unique→
`SNUM_PAQUET_RENDU_V519_END`→`PAQUET_RENDU_PRET`.
Première ligne visible : START. Rien avant, sans bloc de code, brouillon, préambule
ou doublon.
