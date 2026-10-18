`SNUM_COLLECTE_V523_METHODE_START`

# Méthode Collecte autonome

## 1. Exécuter le cycle Web

Lance immédiatement une recherche Web composite dans le Projet Collecte à partir de
`DATE_EDITION` et de `PERIODE`. Termine la recherche et produis le paquet dans cette
même réponse. N’affiche jamais de requête à recopier, de plan, de trace ou de commande
intermédiaire.

La recherche couvre ensemble `numerique`, `ia`, `commande`, `rh` et `bercy`, avec
les cinq axes complets du prompt. Ouvre les résultats avant de les retenir. Le Web
reste actif pendant tout ce cycle ; le métier ne copie aucune réponse entre deux
chats et n’envoie aucune commande de continuation ou de normalisation.

## 2. Vérifier et normaliser les sources

Une source valide possède une URL canonique HTTPS, un titre, un éditeur et une date
de publication exacte. Pour `2026-10-11..2026-10-17`, les deux bornes sont incluses ;
`2026-10-10` et `2026-10-18` sont exclues. Une date d’événement, d’échéance, de mise
à jour ou un mois sans jour ne prouve pas la date de publication.

Déduplique par URL canonique. Trie les sources valides par date décroissante, puis
selon l’ordre `numerique|ia|commande|rh|bercy`, puis par URL. Attribue ensuite
`U01…UN` sans trou. Le nombre d’articles égale le nombre d’URL uniques.

Utilise uniquement les faits lus dans les sources. Génère de 3 à 5 mots-clés par
article, un `takeaway` et un `snum_interest` courts, sans inventer de fait. À partir
de trois articles, exactement les trois premiers portent `essential=true`. Sous
trois articles, aucun n’est essentiel.

## 3. Appliquer le best effort et rendre le paquet

Une rubrique vide ajoute une alerte `watch`. Moins de cinq articles ajoute aussi une
alerte. Ces insuffisances ne bloquent jamais le JSON. Si la recherche Web s’est
exécutée mais ne fournit aucune source valide, produis tout de même le paquet avec
`articles=[]`, aucun essentiel et les alertes nécessaires.

Seule une indisponibilité technique réelle du Web arrête le parcours avec
`A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`. Une recherche vide n’est
pas une indisponibilité et ne déclenche jamais `A_COMPLETER`.

Applique exactement le schéma du contrat V519. La réponse réussie commence au premier
caractère par `SNUM_PAQUET_RENDU_V519_START`, contient un seul JSON sans bloc de
code, puis `SNUM_PAQUET_RENDU_V519_END` et `PAQUET_RENDU_PRET`. N’affiche aucun
raisonnement, registre, compteur, contrôle intermédiaire, résultat brut ni préambule.

`SNUM_COLLECTE_V523_METHODE_END`
