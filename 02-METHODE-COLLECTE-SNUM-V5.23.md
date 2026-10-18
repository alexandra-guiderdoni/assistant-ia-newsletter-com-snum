`SNUM_COLLECTE_V523_METHODE_START`

# Méthode Collecte en deux chats

## 1. Produire la requête composite

Le Projet Collecte ne navigue pas sur le Web. À partir de `DATE_EDITION`, de
`PERIODE` et de `RECHERCHE_COMPOSITE`, il prépare une requête unique à copier
dans un nouveau chat Assistant ordinaire avec le Web activé.

La requête couvre `numerique`, `ia`, `commande`, `rh` et `bercy`. Elle recopie
chaque code avec l’axe complet défini dans le prompt. Une liste de codes sans ces
axes est invalide. Les axes servent à chercher. Dans chaque ligne `RESULTAT`,
`rubrique` vaut uniquement le code, jamais le libellé ni l’axe.

Elle exige l’ouverture des sources, leur URL HTTPS et la date de publication exacte.
Elle exclut les contenus publiés hors fenêtre, même si leur événement ou leur mise à
jour est dans la fenêtre. Grammaire demandée :
`RESULTAT|rubrique|URL_HTTPS|date_iso|titre|source|fait_factuel`
ou `RESULTAT|rubrique|AUCUN_RESULTAT_DATE_DANS_FENETRE`.
Aucun champ ne contient le caractère `|` ni de retour à la ligne.

## 2. Enregistrer la réponse Web

Le métier copie toute la réponse du chat Web dans le chat Collecte d’origine. Cette
validation humaine unique confirme que la recherche a été lancée. Le Projet Collecte
n’appelle aucun outil Web et ne relance aucune recherche.

Analyse seulement les lignes `RESULTAT|`. Une ligne complète possède exactement
sept champs. Rejette une rubrique inconnue, une URL non HTTPS, une date non exacte ou
hors fenêtre. Pour `2026-10-03..2026-10-13`, `2026-10-03`, `2026-10-04`,
`2026-10-11` et `2026-10-13` sont incluses ; `2026-10-02` et `2026-10-14`
sont exclues.

Déduplique par URL canonique. Si une rubrique comporte au moins une ligne valide,
ignore `AUCUN_RESULTAT_DATE_DANS_FENETRE` pour cette rubrique. Sinon, conserve
l’absence comme future alerte. Les lignes invalides ne deviennent jamais des
articles.

Mémorise le résultat sous `SOURCES_NORMALISEES`, avec la date d’édition et les
bornes. Ce tour ne produis aucun JSON. Il répond seulement avec
`RESULTATS_COMPOSITES_ENREGISTRES`, le nombre de lignes valides, les rubriques sans
résultat, puis `REQUETE_A_ENVOYER=NORMALISER_V519`.

## 3. Produire le paquet sur commande

`NORMALISER_V519` est accepté seulement après
`RESULTATS_COMPOSITES_ENREGISTRES`. Il transforme uniquement les
`SOURCES_NORMALISEES` mémorisées ; il ne recherche rien et ne demande aucun autre
contenu au métier.

Trie par date décroissante, puis selon l’ordre
`numerique|ia|commande|rh|bercy`, puis par URL. Après déduplication et tri,
attribue `U01…UN` sans trou. Le nombre d’articles égale le nombre d’URL uniques.

Utilise uniquement les faits reçus. Génère de 3 à 5 mots-clés par article, un
`takeaway` et un `snum_interest` courts, sans inventer de fait. À partir de trois
articles, exactement les trois premiers portent `essential=true`. Sous trois,
aucun n’est essentiel. Moins de cinq articles ou une rubrique vide ajoute une alerte
à `watch`, mais ne bloque jamais le JSON.

Applique exactement le schéma du contrat V519. La sortie réussie commence au premier
caractère par `SNUM_PAQUET_RENDU_V519_START`, contient un seul JSON sans bloc de
code, puis `SNUM_PAQUET_RENDU_V519_END` et `PAQUET_RENDU_PRET`. N’affiche aucun
raisonnement, registre, compteur, contrôle intermédiaire ni préambule.

`SNUM_COLLECTE_V523_METHODE_END`
