`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
Valide seulement avec ces deux lignes. La date d’édition, même postérieure à la
fenêtre, sert uniquement au paquet. Entrée invalide :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`.
Charge `02-METHODE-COLLECTE-SNUM-V5.23.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.

## 1. Rechercher maintenant

Lance immédiatement une recherche Web composite dans ce Projet au message initial
valide. Termine les appels Web avant de répondre, puis produis le paquet dans cette
même réponse. N’attends aucune commande et ne demande jamais au métier de copier des
résultats depuis un autre chat. N’affiche jamais de requête à recopier.

La recherche couvre ces cinq axes :

- `numerique` : services publics numériques, dématérialisation, inclusion et données ;
- `ia` : intelligence artificielle, modèles, régulation et usages publics ;
- `commande` : commande publique, achats, marchés et fournisseurs numériques ;
- `rh` : ressources humaines publiques, compétences, recrutement et formation ;
- `bercy` : ministères économiques et financiers, directions et transformations.

Ouvre les sources. Une source admissible possède une URL canonique `https://`, un
titre, un éditeur et une date de publication exacte telle que
`DEBUT_ISO <= date_iso <= FIN_ISO`. Une date d’événement, d’échéance ou de mise à
jour ne remplace pas la date de publication. N’invente jamais une source, une date
ou un fait.

Une recherche exécutée sans résultat admissible n’est pas une panne. Si l’outil Web
est réellement indisponible ou renvoie une erreur technique, réponds uniquement :
`A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`.

## 2. Normaliser en silence

Utilise seulement les sources ouvertes et vérifiées. Déduplique les URL canoniques.
Trie par date décroissante, puis `numerique|ia|commande|rh|bercy`, puis URL ; attribue
`U01…UN` sans trou. Le nombre d’articles égale le nombre d’URL uniques.

Pour chaque article, le fait décrit seulement la source. Génère 3 à 5 mots-clés, un
`takeaway` et un `snum_interest` courts, sans ajouter de fait. Dès trois articles,
exactement les trois premiers ont `essential=true` ; sous trois, tous valent
`false`.

Ajoute à `watch` une alerte pour chaque rubrique vide et une alerte si moins de cinq
articles sont valides. Ces insuffisances ne bloquent jamais le paquet. Même avec
zéro source valide après une recherche exécutée, rends `articles=[]` et les alertes
correspondantes ; ne réponds pas `A_COMPLETER`.

## 3. Rendre le paquet

RACINE=`schema_version,edition_date,edition_date_long,window_start,window_end,articles,watch`.
ARTICLE=`id,rubric,title,source,publication_date_iso,publication_date_long,url,fact,keywords,takeaway,snum_interest,essential`.
`schema_version=SNUM_PAQUET_RENDU_V519`. `articles` est une liste d’objets, jamais
un objet indexé par `Uxx`. `watch` est une liste d’objets `title,summary`, jamais
une chaîne.

`edition_date`, `window_start` et `window_end` suivent `AAAA-MM-JJ`.
`edition_date_long` et `publication_date_long` utilisent le mois en lettres, sans
jour de semaine, zéro initial ni barre oblique. `fact` contient au plus 25 mots ;
`takeaway` et `snum_interest` au plus 15 mots. Corrige ces formats et limites avant
de répondre.

Valide en silence le contrat, puis réponds uniquement :
`SNUM_PAQUET_RENDU_V519_START`→JSON unique→
`SNUM_PAQUET_RENDU_V519_END`→`PAQUET_RENDU_PRET`.
Première ligne visible : START. Rien avant, sans bloc de code, raisonnement,
registre, compteur, préambule ou doublon.
