SNUM_COLLECTE_V524_CONTRAT_START

# Contrat Paquet repris de la V5.19

Pendant `PAQUET`, n’utilise pas le Web. Transforme uniquement `SOURCES_VALIDES` en un
bloc JSON strict placé entre `SNUM_PAQUET_RENDU_V519_START` et
`SNUM_PAQUET_RENDU_V519_END`. `\"` et `\\` doivent être échappés dans les chaînes ;
vérifie que le bloc est analysable comme JSON. Aucun commentaire.

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
et `summary`, ou une liste vide. `id` est une chaîne non vide et unique. Une URL ne peut
apparaître qu’une fois dans `articles`.

Avant de répondre, vérifie chaque champ, les URL, les limites de mots et le nombre
d’essentiels. Si le nombre d’URL uniques diffère du nombre d’articles, réponds
`PAQUET_INCOMPLET | URL_DUPLIQUEE | <URL>`, sans JSON. Pour tout autre échec, réponds
`PAQUET_INCOMPLET | <identifiant> | <champ>`, sans JSON. Sinon termine après le marqueur
de fin par `PAQUET_RENDU_PRET`.

## Normalisation V5.24

Une rubrique apparaît au plus une fois. Trie les articles dans l’ordre `numerique`,
`ia`, `commande`, `rh`, `bercy`, puis attribue les identifiants contigus `U01…UN`.
À partir de trois articles, les trois premiers sont les seuls `essential=true`.
N’émets ni brouillon, ni copie du JSON, ni second bloc.

## PASSERELLE_RENDU

En réussite, le bloc copiable commence exactement par ces lignes, avant
`SNUM_PAQUET_RENDU_V519_START` :

```text
PHASE RENDRE_EDITION.
N’utilise pas le Web.
Utilise le PAQUET_RENDU ci-dessous sans modifier ses données.
Charge séparément les quatre ressources CANON-HTML V5.19.
Respecte l’ordre immuable des rubriques et de la navigation :
numerique, ia, commande, rh, bercy.
Numérote les sections dans cet ordre après L’essentiel.
Remplace chaque marqueur sans supprimer les espaces placés avant lui.
Joins les sections avec un seul saut de ligne, sans ligne vide ajoutée.
Échappe toute valeur injectée sans l’altérer : &→&amp;, <→&lt;, >→&gt;, "→&quot;, '→&#x27;.
Termine le bloc par exactement un saut de ligne après </html>.
Dans toutes les cartes et sections, utilise les titres et tags canoniques en capitales.
Pour numerique, le titre et le tag valent exactement NUMERIQUE, sans accent.
Livre le HTML canonique au premier passage.
Ne pose aucune question.
```

Cette `PASSERELLE_RENDU` et le paquet forment un seul bloc de code `text`, afin que le
métier copie et colle une seule fois. Pour `numerique`, titre et tag valent exactement
`NUMERIQUE`, sans accent. Aucun texte ne précède ni ne suit ce bloc.

SNUM_COLLECTE_V524_CONTRAT_END
