<!-- PDG-LARGE-FILE-JUSTIFICATION: guide autonome d’installation et d’usage métier des deux Projets Assistant. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: les ZIP générés regroupent les fichiers à installer dans chaque Projet. -->

# Configurer les deux Projets Newsletter SNUM

Le kit transforme une recherche d’actualité en newsletter HTML dans l’Assistant
DINUM. Le métier utilise deux Projets enregistrés et un chat Web ordinaire :

1. `Newsletter SNUM - Collecte` prépare la recherche puis normalise ses résultats ;
2. un nouveau chat Assistant ordinaire exécute une recherche Web composite ;
3. `Newsletter SNUM - Rendu HTML` transforme le paquet JSON en HTML canonique.

Le chat Web n’est pas un troisième Projet. Cette séparation évite qu’une longue
conversation de recherche perturbe le calcul des dates ou le format JSON.

> **État de recette du 18 octobre 2026 : GO.** La chaîne réelle a produit une
> requête composite, enregistré six sources après une relance du chat Web, généré
> un paquet V519 valide avec `NORMALISER_V519`, puis obtenu le HTML canonique au
> premier passage dans Rendu. Les rubriques IA et Ressources humaines, sans résultat
> daté, sont signalées dans `watch` sans bloquer le parcours.

## Fichiers actifs

### Projet Collecte V5.23

- `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` : instructions du Projet ;
- `02-METHODE-COLLECTE-SNUM-V5.23.md` : méthode à téléverser ;
- `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` : contrat V519 à téléverser.

### Projet Rendu HTML V5.19

- `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md` : instructions du Projet ;
- `21-CANON-HTML-COQUE-A-V5.19.md` ;
- `22-CANON-HTML-COQUE-B-V5.19.md` ;
- `23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md` ;
- `24-CANON-HTML-SURVEILLER-VIDE-V5.19.md`.

Les deux archives de la racine contiennent exactement ces fichiers :
`Newsletter SNUM - Collecte.zip` et `Newsletter SNUM - Rendu HTML.zip`.
Décompressez-les avant l’installation. Ne téléversez jamais un ZIP dans l’Assistant.

## Installer les Projets

### Newsletter SNUM - Collecte

1. Créez ou ouvrez le Projet `Newsletter SNUM - Collecte`.
2. Remplacez ses instructions par le contenu complet du fichier
   `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md`.
3. Supprimez les anciennes ressources Collecte.
4. Téléversez les fichiers `02` et `03` listés ci-dessus.
5. Attendez que les deux ressources soient visibles et indexées, puis enregistrez.

Le Web peut rester désactivé dans ce Projet : il ne doit jamais y effectuer la
recherche.

### Newsletter SNUM - Rendu HTML

1. Créez ou ouvrez le Projet `Newsletter SNUM - Rendu HTML`.
2. Remplacez ses instructions par le contenu complet du fichier
   `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md`.
3. Supprimez les anciennes ressources HTML.
4. Téléversez les quatre fichiers `21` à `24`, séparément et dans cet ordre.
5. Attendez que les quatre ressources soient visibles et indexées, puis enregistrez.

Le Web doit rester désactivé dans ce Projet.

## Produire une édition

L’exemple ci-dessous produit l’édition du 14 octobre 2026 avec les publications du
3 au 13 octobre 2026 inclus.

### 1. Demander la requête au Projet Collecte

Ouvrez une nouvelle conversation dans `Newsletter SNUM - Collecte` et envoyez :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
RECHERCHE_COMPOSITE
```

La réponse attendue commence par `REQUETE_COMPOSITE_A_COPIER_START` et finit par
`REQUETE_COMPOSITE_A_COPIER_END`. Elle couvre dans une seule requête les rubriques
Numérique, Intelligence artificielle, Commande publique, Ressources humaines et Vie
de Bercy.

### 2. Lancer la recherche dans un chat Web ordinaire

Ouvrez un nouveau chat Assistant ordinaire, hors des deux Projets, puis activez le
Web. Copiez le texte situé entre les deux marqueurs de la réponse précédente et
envoyez-le.

La recherche doit fournir des lignes de cette forme :

```text
RESULTAT|rubrique|URL_HTTPS|date_iso|titre|source|fait_factuel
```

Une rubrique réellement vide peut produire :

```text
RESULTAT|rubrique|AUCUN_RESULTAT_DATE_DANS_FENETRE
```

Attendez la fin de la réponse. Une introduction, des citations ou même une ligne
`AUCUN_RESULTAT_DATE_DANS_FENETRE` contradictoire ne bloquent pas l’étape suivante.

### 3. Enregistrer les résultats dans Collecte

Copiez toute la réponse du chat Web, puis collez-la telle quelle dans la conversation
Collecte d’origine.

La réponse attendue ne contient pas encore de JSON. Elle confirme l’enregistrement :

```text
RESULTATS_COMPOSITES_ENREGISTRES | VALIDES=<n> | RUBRIQUES_SANS_RESULTAT=<codes ou AUCUNE>
REQUETE_A_ENVOYER=NORMALISER_V519
```

Cette étape normalise la fenêtre et déduplique les URL. Elle conserve les résultats
dans le chat Collecte d’origine.

### 4. Produire le paquet JSON

Dans cette même conversation Collecte, envoyez exactement :

```text
NORMALISER_V519
```

La réponse doit commencer immédiatement par
`SNUM_PAQUET_RENDU_V519_START`. Elle contient un seul objet JSON, puis :

```text
SNUM_PAQUET_RENDU_V519_END
PAQUET_RENDU_PRET
```

Il n’existe pas de commandes `VALIDER`, `RECOMPTER` ou `GENERER_PAQUET`.
`NORMALISER_V519` est l’unique commande entre la recherche et le paquet.

### 5. Produire le HTML

Ouvrez une nouvelle conversation dans `Newsletter SNUM - Rendu HTML`, sans le Web.
Copiez depuis `SNUM_PAQUET_RENDU_V519_START` jusqu’à
`SNUM_PAQUET_RENDU_V519_END` inclus, puis envoyez ce bloc sans autre instruction.

La première ligne attendue est `## HTML COMPLET`. Elle est suivie d’un unique bloc
`html`, puis de :

```text
## CONTROLES
État : HTML_CANONIQUE_PRODUIT - contrôle métier requis
```

La présence d’un plan, d’un préambule ou de texte avant `## HTML COMPLET` est un
échec de conformité.

## Mode best effort

- Une rubrique sans source valide devient une alerte dans `watch`.
- Moins de cinq articles devient une alerte dans `watch`.
- Ces insuffisances ne bloquent pas le JSON.
- Une URL ne peut apparaître qu’une fois.
- Une ligne hors fenêtre, sans date exacte ou sans URL HTTPS ne devient pas un
  article.
- Si une rubrique possède une ligne valide, toute ligne
  `AUCUN_RESULTAT_DATE_DANS_FENETRE` de cette rubrique est ignorée.
- Sans aucune ligne valide, Collecte répond une seule fois
  `A_COMPLETER | RESULTATS_COMPOSITES_INEXPLOITABLES | aucune ligne valide`.

## En cas d’échec

- Pas de marqueurs `REQUETE_COMPOSITE_A_COPIER_*` : vérifiez les instructions et
  les deux ressources du Projet Collecte.
- Pas de ligne `RESULTAT|` après la recherche : ouvrez un nouveau chat Web et
  relancez une seule fois la même requête composite.
- Pas de `RESULTATS_COMPOSITES_ENREGISTRES` après le collage : ne lancez pas
  `NORMALISER_V519` ; ouvrez une conversation Collecte neuve et recommencez.
- `PAQUET_INCOMPLET` ou `A_COMPLETER` dans Collecte : ne transmettez rien au
  Projet Rendu.
- `CANON_MANQUANT` dans Rendu : remplacez les quatre ressources `21` à `24`
  par celles du kit courant et attendez leur indexation.
- `A_COMPLETER` dans Rendu : corrigez la cause indiquée ; ne demandez pas une
  réécriture libre du HTML.

Après trois échecs identiques, arrêtez la recette et conservez l’URL de la
conversation pour le diagnostic.

## Contrôle métier minimal

Vérifiez :

- les dates, titres et URL du paquet ;
- les cinq rubriques présentes ou signalées dans `watch` ;
- des identifiants `U01…UN` continus et des URL uniques ;
- exactement trois articles essentiels à partir de trois articles ;
- aucun marqueur `@@` dans le HTML ;
- un seul `h1`, trois accès rapides et une navigation cohérente ;
- le titre d’édition en toutes lettres ;
- la modale après le footer ;
- les CSS et scripts DSFR 1.15.2 ;
- l’indication de nouvelle fenêtre sur chaque lien externe.

## Maintenance

Les scripts Python ne sont pas utilisés par le métier. Ils servent à régénérer les
ressources et les ZIP puis à vérifier le kit :

```bash
python3 scripts/build_split_kit.py
python3 -m unittest discover -s tests -v
ruff check --no-cache scripts tests
python3 scripts/build_split_kit.py --check
git diff --check
```

La source HTML unique reste `_source/05-BLOCS-HTML-CANONIQUES.md`. Ne modifiez pas
directement les fichiers `21` à `24` ni les ZIP.
