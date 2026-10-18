SNUM_COLLECTE_V523_CONTRAT_START

# Contrat Paquet repris de la V5.19

Après la recherche Web du message initial, transforme uniquement les sources
ouvertes et vérifiées en un bloc JSON strict placé entre
`SNUM_PAQUET_RENDU_V519_START` et `SNUM_PAQUET_RENDU_V519_END`. Produis le paquet
dans cette même réponse, sans commande intermédiaire. `\"` et `\\` doivent être
échappés dans les chaînes ; vérifie que le bloc est analysable comme JSON. Aucun
commentaire.

Le JSON contient exactement : `schema_version`=`SNUM_PAQUET_RENDU_V519`, `edition_date`,
`edition_date_long`, `window_start`, `window_end`, `articles`, `watch`. Chaque article
contient : `id`, `rubric`, `title`, `source`, `publication_date_iso`,
`publication_date_long`, `url`, `fact`, `keywords`, `takeaway`, `snum_interest`,
`essential`. `rubric` vaut seulement `numerique`, `ia`, `commande`, `rh` ou `bercy`.
`keywords` contient 3 à 5 chaînes. `fact` contient au plus 25 mots ; `takeaway` et
`snum_interest` au plus 15 mots. `publication_date_iso` suit `AAAA-MM-JJ`.
`edition_date`, `window_start` et `window_end` suivent aussi `AAAA-MM-JJ` ;
`edition_date_long` écrit la date d’édition avec le mois en lettres.
`publication_date_long` écrit la même date avec le mois en lettres, par exemple
`6 octobre 2026`, sans jour de semaine, zéro initial ni barre oblique.
Sous trois articles, tous portent `essential=false`. À partir de trois articles,
exactement trois portent `essential=true`. `watch` contient seulement des objets `title`
et `summary`, ou une liste vide. `id` vaut exactement `U01…UN` sans trou. Une URL ne peut
apparaître qu’une fois dans `articles`. Une recherche exécutée sans source valide
produit `articles=[]` et des alertes `watch` ; elle ne bloque pas le paquet.

Avant de répondre, vérifie chaque champ, les URL, les limites de mots et le nombre
d’essentiels. Si le nombre d’URL uniques diffère du nombre d’articles, réponds
`PAQUET_INCOMPLET | URL_DUPLIQUEE | <URL>`, sans JSON. Pour tout autre échec, réponds
`PAQUET_INCOMPLET | <identifiant> | <champ>`, sans JSON. Sinon termine après le marqueur
de fin par `PAQUET_RENDU_PRET`.

Stabilisation : si nécessaire, raccourcis les trois textes avant la validation, sans
ajouter de fait. Écris `watch=[]` s’il n’y a aucune alerte, jamais une chaîne. Avant de
répondre, valide en silence. `SORTIE_PAQUET=START→JSON_UNIQUE→END→PAQUET_RENDU_PRET`;
unique, rien avant START. Première ligne visible : START; sans bloc de code, aucun
brouillon, préambule ou doublon.

SNUM_COLLECTE_V523_CONTRAT_END
