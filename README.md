<!-- PDG-LARGE-FILE-JUSTIFICATION: guide autonome d’installation et d’usage métier des deux Projets Assistant. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: les ZIP générés regroupent les fichiers à installer dans chaque Projet. -->

# Configurer les deux Projets Newsletter SNUM

Le kit transforme une recherche d’actualité en newsletter HTML dans l’Assistant
DINUM. Le métier utilise deux Projets enregistrés et deux conversations :

1. `Newsletter SNUM - Collecte` recherche sur le Web et produit le paquet JSON ;
2. `Newsletter SNUM - Rendu HTML` transforme ce paquet en HTML canonique.

Il n’existe aucun chat Web intermédiaire. Dans Collecte, le métier saisit seulement
les deux dates et reçoit directement le paquet à transmettre à Rendu HTML.

> **État du candidat : chaîne best effort validée le 18 octobre 2026.** Une
> conversation Collecte avec le Web a produit directement le JSON, puis une
> conversation Rendu a produit `## HTML COMPLET`. La recherche n’a retenu aucun
> article daté parmi 51 sources consultées : le paquet et le HTML signalent donc
> explicitement une collecte à compléter.

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

Le Web doit être activé dans ce Projet : Collecte effectue elle-même la recherche.

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

### 1. Produire le paquet dans Collecte

Ouvrez une nouvelle conversation dans `Newsletter SNUM - Collecte`, activez le Web
et envoyez seulement :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
```

Collecte lance la recherche, ouvre les sources, contrôle leurs dates, déduplique les
URL et produit le JSON sans autre intervention. La réponse doit commencer
immédiatement par `SNUM_PAQUET_RENDU_V519_START`. Elle contient un seul objet JSON,
puis :

```text
SNUM_PAQUET_RENDU_V519_END
PAQUET_RENDU_PRET
```

Il n’existe aucune requête à recopier ni commande intermédiaire.

### 2. Produire le HTML

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

Si `articles=[]`, Rendu ne bloque pas : il produit la section
`Collecte à compléter`, puis `À surveiller` à partir des alertes `watch`.

## Mode best effort

- Une rubrique sans source valide devient une alerte dans `watch`.
- Moins de cinq articles devient une alerte dans `watch`.
- Ces insuffisances ne bloquent pas le JSON.
- Une recherche exécutée sans source valide produit `articles=[]` et des alertes.
- Une URL ne peut apparaître qu’une fois.
- Une ligne hors fenêtre, sans date exacte ou sans URL HTTPS ne devient pas un
  article.
- Seule une indisponibilité technique réelle du Web produit `A_COMPLETER`.

## En cas d’échec

- Pas de `SNUM_PAQUET_RENDU_V519_START` : vérifiez que le Web est actif, les
  instructions et les deux ressources du Projet Collecte.
- `OUTIL_WEB_INDISPONIBLE` : ouvrez une conversation Collecte neuve et relancez une
  seule fois avec les mêmes dates.
- `PAQUET_INCOMPLET` ou tout autre `A_COMPLETER` dans Collecte : ne transmettez rien
  au Projet Rendu.
- `CANON_MANQUANT` dans Rendu : remplacez les quatre ressources `21` à `24`
  par celles du kit courant et attendez leur indexation.
- `A_COMPLETER` dans Rendu : corrigez la cause indiquée. Un paquet vide avec des
  alertes `watch` n’est pas une cause d’échec.

Après trois échecs identiques, arrêtez la recette et conservez l’URL de la
conversation pour le diagnostic.

## Contrôle métier minimal

Vérifiez :

- les dates, titres et URL du paquet ;
- les cinq rubriques présentes ou signalées dans `watch` ;
- des identifiants `U01…UN` continus et des URL uniques ;
- exactement trois articles essentiels à partir de trois articles, sinon aucun ;
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
