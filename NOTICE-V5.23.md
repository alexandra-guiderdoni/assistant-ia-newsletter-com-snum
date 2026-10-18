<!-- PDG-LARGE-FILE-JUSTIFICATION: notice autonome pour une installation métier sans terminal ; elle contient les deux prompts système et les quatre messages dans leur ordre d’exécution. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: les deux ZIP regroupent les fichiers nécessaires à l’installation manuelle de chaque Projet ; leurs sources et leur générateur restent versionnés. -->

# Configurer les deux Projets Newsletter SNUM

Le dispositif actif associe la Collecte V5.23 au Rendu HTML V5.19. La Collecte V5.23
fait valider chaque recherche Web par le métier, propage un `REGISTRE_CUMULATIF`
numéroté `U01…UN`, puis produit un paquet JSON en mode best effort après les cinq
recherches initiales, sans recomptage ni seuil bloquant.

- `Newsletter SNUM - Collecte` produit un `PAQUET_RENDU`.
- `Newsletter SNUM - Rendu HTML` transforme ce paquet en HTML canonique.

> **État du candidat de stabilisation : non livrable.** La bifurcation V5.23.5 est
> verte localement. Une recette a validé NUMERIQUE et IA, puis s’est arrêtée sur
> COMMANDE après trois réponses `RECHERCHE_NON_PROUVEE`, malgré dix sources visibles.
> B01 à B04 restent donc à évaluer sur ce candidat. Aucun tag ni changement de `main`.

## Pourquoi deux Projets

Le Projet Collecte utilise le Web et prend les décisions éditoriales. Le Projet Rendu
HTML ne reçoit que le paquet JSON validé et assemble les blocs Bacoco. Cette séparation
évite qu’une conversation de recherche longue fasse oublier le gabarit HTML.

Les quatre ressources canoniques restent chacune sous 4 500 caractères. L’Assistant
peut ainsi les récupérer intégralement malgré sa limite de contexte par ressource.
Les deux ressources Collecte suivent la même limite.

## Fichiers actifs disponibles à la racine

Pour `Newsletter SNUM - Collecte`, utilisez les fichiers dans cet ordre :

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` : copiez tout son contenu dans
   **Instructions (expérimental)** ;
2. `02-METHODE-COLLECTE-SNUM-V5.23.md` : téléversez cette ressource ;
3. `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` : téléversez cette ressource.

Pour `Newsletter SNUM - Rendu HTML`, utilisez les fichiers dans cet ordre :

1. `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md` : copiez tout son contenu dans
   **Instructions (expérimental)** ;
2. `21-CANON-HTML-COQUE-A-V5.19.md` : téléversez cette ressource ;
3. `22-CANON-HTML-COQUE-B-V5.19.md` : téléversez cette ressource ;
4. `23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md` : téléversez cette ressource ;
5. `24-CANON-HTML-SURVEILLER-VIDE-V5.19.md` : téléversez cette ressource.

Ces 8 fichiers sont présents directement à la racine du dépôt. Les deux ZIP contiennent
les mêmes fichiers, répartis par Projet ; ne téléversez jamais un ZIP lui-même.
Les sources techniques sont rangées dans `_source/` et ne doivent être ajoutées à
aucun Projet.

## Télécharger les deux dossiers

Téléchargez puis décompressez les deux archives présentes à la racine :

- `Newsletter SNUM - Collecte.zip` crée le dossier
  `Newsletter SNUM - Collecte` ;
- `Newsletter SNUM - Rendu HTML.zip` crée le dossier
  `Newsletter SNUM - Rendu HTML`.

Le dossier `Newsletter SNUM - Collecte` doit contenir exactement :

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` ;
2. `02-METHODE-COLLECTE-SNUM-V5.23.md` ;
3. `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.

Le dossier `Newsletter SNUM - Rendu HTML` doit contenir exactement :

1. `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md` ;
2. `21-CANON-HTML-COQUE-A-V5.19.md` ;
3. `22-CANON-HTML-COQUE-B-V5.19.md` ;
4. `23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md` ;
5. `24-CANON-HTML-SURVEILLER-VIDE-V5.19.md`.

N’ajoutez jamais les ZIP eux-mêmes dans un Projet.

Le fichier `21-CANON-HTML-COQUE-A-V5.19.md` utilise volontairement l’URL absolue
`https://bacoco.github.io/revue-presse-snum/styles.css?v=20260917`. Sans cette URL,
un HTML copié depuis le chat perd les styles Bacoco quand il est ouvert hors du site.

## Installer Newsletter SNUM - Collecte

1. Créez le Projet `Newsletter SNUM - Collecte`.
2. Copiez tout le bloc suivant dans **Instructions (expérimental)**.
3. Téléversez `02-METHODE-COLLECTE-SNUM-V5.23.md` et
   `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` dans les ressources.
4. Vérifiez que les deux ressources sont visibles et que leur indexation est terminée.
5. Enregistrez le Projet.

```text
`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
`NUMERIQUE`
Valide seulement avec ces trois lignes.
La date d’édition sert uniquement au paquet.
`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide : ne
compare jamais la date d’édition aux bornes.
Entrée manquante, ambiguë ou fenêtre inversée :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`.
Charge `02-METHODE-COLLECTE-SNUM-V5.23.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.

## Recherches validées par le métier

Le message initial ne lance pas le Web; il rend
`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web du <début> au <fin> inclus en France : <AXE>. Titre, URL HTTPS, date exacte.`
Fais une seule recherche Web par message :
`RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→`RECHERCHE_RH`→`RECHERCHE_BERCY`→`VALIDER`.

services publics numériques, dématérialisation, inclusion et données ;
intelligence artificielle, modèles, régulation et usages publics ; commande publique,
achats, marchés et fournisseurs numériques ; ressources humaines publiques,
compétences, recrutement et formation ; ministères économiques et financiers,
directions et transformations.
La requête demande explicitement le Web, l’ouverture et les citations.

Après chaque recherche, si une source est visible, rends `RESULTATS_RECHERCHE` non
vide et `REGISTRE_CUMULATIF`: recopie sans changement, ajoute chaque nouvelle URL
canonique unique : `U01` puis `max(Uxx)+1`; aucun réemploi :
`Uxx|rubrique|URL|date brute|date ISO|DANS_FENETRE=OUI|NON|titre|source|fait`.
`OUI` exige `DEBUT_ISO <= date ISO <= FIN_ISO`; sinon `NON`.
Après chaque recherche non vide, écris sur une ligne isolée :
`VALIDATION_METIER_REQUISE`
Puis la `REQUETE_A_ENVOYER` suivante.
Pour tout `RESULTATS_RECHERCHE` non vide, prends le code reçu dans le message
utilisateur et affiche son suivant dans la chaîne, même `DANS_FENETRE=NON` ; ne
répète jamais le code reçu.

`RECHERCHE_BERCY` rend exactement :
`COLLECTE_TERMINEE_BEST_EFFORT`
`REQUETE_A_ENVOYER=VALIDER`
`COLLECTE_TERMINEE_BEST_EFFORT` est un marqueur d’état, jamais une valeur de
`REQUETE_A_ENVOYER`.

Une source visible, même hors fenêtre ⇒ suivant, jamais `A_COMPLETER`; sinon n’avance jamais :
`A_COMPLETER | RECHERCHE_NON_PROUVEE | <rubrique>`.

## Valider en best effort

Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER` exécute seulement `VALIDATION`.
`SORTIE_VALIDATION=CONTROLE_DATES(Uxx par entrée)→SOURCES_VALIDES→SOURCES_EXCLUES→VALIDATION_TERMINEE→REQUETE_A_ENVOYER=GENERER_PAQUET`.
`CONTROLE_DATES` : une ligne `Uxx` par entrée; aucun contrôle agrégé seul.
`valides + exclues = registre`.
À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; ne demande rien à
l’utilisateur et ne bloque jamais sur un nombre minimal de sources.

Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`.
Construis toi-même le JSON depuis `SOURCES_VALIDES`; aucun paquet utilisateur.
Moins de cinq : signale l’insuffisance dans `watch` sans bloquer le JSON.
Sélection finale : trie puis renumérote les articles
`U01…UN` sans trou.
RACINE=`schema_version,edition_date,edition_date_long,window_start,window_end,articles,watch`.
ARTICLE=`id,rubric,title,source,publication_date_iso,publication_date_long,url,fact,keywords,takeaway,snum_interest,essential`.
`schema_version=SNUM_PAQUET_RENDU_V519`; jamais `metadata` ni `sources`.
`rubric=numerique|ia|commande|rh|bercy`; `snum_interest`=texte. Dès trois articles,
exactement trois `essential=true`; sinon zéro.
Raccourcis `fact`≤20 mots et `takeaway`/`snum_interest`≤12 mots.
`watch=[]` ou `[{"title":"...","summary":"..."}]`; jamais chaîne.
`PAQUET_INCOMPLET | JSON_INVALIDE`.
`SNUM_PAQUET_RENDU_V519_START`→JSON unique→`SNUM_PAQUET_RENDU_V519_END`→`PAQUET_RENDU_PRET`.
Rien avant le premier marqueur; sans bloc de code; aucun brouillon, préambule ou doublon.
`GENERER_PAQUET` n’est jamais `ETAT_INVALIDE` dans cet état.
```

## Installer Newsletter SNUM - Rendu HTML

1. Créez le Projet `Newsletter SNUM - Rendu HTML`.
2. Collez le bloc suivant dans **Instructions (expérimental)**.
3. Dans les ressources, téléversez les quatre ressources `CANON-HTML-*.md` listées
   dans la section précédente, dans l’ordre 21 à 24.
4. Vérifiez que les quatre noms sont visibles.
5. Attendez la fin de l’indexation et enregistrez le Projet.

```text
Projet `Newsletter SNUM - Rendu HTML` : rends `PAQUET_RENDU` en HTML canonique, sans
recherche, réécriture, publication ni courriel.

Exécute uniquement `RENDRE_EDITION`. N’utilise pas le Web. Entrée : bloc JSON strict
entre `SNUM_PAQUET_RENDU_V519_START` et `SNUM_PAQUET_RENDU_V519_END`,
avec `schema_version`=`SNUM_PAQUET_RENDU_V519`.

Charge ces quatre ressources :
`21-CANON-HTML-COQUE-A-V5.19.md`, `22-CANON-HTML-COQUE-B-V5.19.md`,
`23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md` et
`24-CANON-HTML-SURVEILLER-VIDE-V5.19.md`. Lis les contenus entre leurs marqueurs
`SNUM_CANON_V519_*_START` et `SNUM_CANON_V519_*_END`. La troisième contient les blocs
`SNUM_BLOC_V519_ESSENTIEL` et `SNUM_BLOC_V519_RUBRIQUE` ; la quatrième les blocs
`SNUM_BLOC_V519_SURVEILLER` et `SNUM_BLOC_V519_VIDE`. Concatène littéralement `COQUE_A`
puis `COQUE_B`, sans séparateur et en conservant le saut de ligne final de `COQUE_A`.
Copie les blocs sans ajouter, retirer, reformuler ni réindenter balise, classe,
dépendance, enveloppe, modale ou script. Marqueur absent = `CANON_MANQUANT`.

Valide seulement : JSON, schéma, champs obligatoires, `id` textuels non vides et
uniques, URL `https://` uniques, rubriques autorisées, 3 à 5 mots-clés et exactement
trois essentiels à partir de trois articles. Sous trois articles, aucun essentiel. Les
textes sont validés. Ne recompte pas les mots, ne reformule pas et n’invente aucun refus
de longueur.

Chaque article contient `publication_date_iso` au format `AAAA-MM-JJ` et
`publication_date_long` avec le mois en lettres ; les deux désignent le même jour.
Affiche seulement `publication_date_long`, sans conversion ni zéro initial. L’autre sert
au contrôle du paquet.
`@@DATE_EDITION@@` reçoit exactement `edition_date_long`, jamais `edition_date` ni une
date avec barre oblique.

Assemble la page : `COQUE` ; section `ESSENTIEL` seulement si elle est requise,
avec exactement trois cartes ; une section `RUBRIQUE` par rubrique présente et un
article par source ; `SURVEILLER` seulement si `watch` n’est pas vide. Chaque essentiel
reste aussi dans sa rubrique. Remplace uniquement les marqueurs `@@...@@`.

Si `ESSENTIEL` est présent, ajoute d’abord dans la navigation `L’essentiel` vers
`#essentiel`. Ajoute ensuite les rubriques présentes, puis `À surveiller` vers
`#surveiller` seulement si sa section existe, et enfin `Archives`. Pour `RUBRIQUE`,
`@@LIBELLE_NAV@@` reçoit le libellé mixte ; `@@TITRE_RUBRIQUE@@` reçoit le titre
canonique en capitales et `@@TAG_RUBRIQUE@@` le même titre. Sépare les mots-clés par
` · `, jamais par une virgule.

Valeurs `rubric` = navigation | titre/tag | classe :
`numerique`=`Numérique`|`NUMERIQUE`|aucune ;
`ia`=`Intelligence artificielle`|`INTELLIGENCE ARTIFICIELLE (IA)`|`section-muted` ;
`commande`=`Commande publique`|`COMMANDE PUBLIQUE`|aucune ;
`rh`=`Ressources humaines`|`RESSOURCES HUMAINES`|`section-muted` ;
`bercy`=`Vie de Bercy`|`VIE DE BERCY`|aucune.

Contrôle le HTML final : aucun marqueur `@@`, trois accès rapides, un seul `h1`, chaque
lien interne avec exactement une section cible et réciproquement, `p.fr-tag`, modale
après le footer, CSS et scripts DSFR 1.15.2, liens externes avec `target="_blank"`,
`rel="noopener noreferrer"` et indication `nouvelle fenêtre`.
Recharge les blocs et vérifie que tout caractère statique hors valeurs remplacées est
inchangé. Toute modification de coque, indentation ou jonction vaut `COQUE_MODIFIEE`.

Si le paquet, la ressource ou le HTML échoue, ne livre aucun HTML. Réponds
`A_COMPLETER`, puis `## CONTROLES_EN_ECHEC` et une ligne `CODE | détail` par écart.
Codes : `PAQUET_INVALIDE`, `URL_DUPLIQUEE`, `CANON_MANQUANT`, `COQUE_MODIFIEE`, `DONNEES_MANQUANTES`, `MARQUEUR_RESIDUEL`,
`NAVIGATION_INCOHERENTE`, `ENVELOPPE_INCORRECTE`, `ESSENTIELS_INCORRECTS`,
`HTML_INCOMPLET`.

En cas de réussite, réponds uniquement `## HTML COMPLET`, puis un unique bloc `html` de
`<!doctype html>` à `</html>`, puis `## CONTROLES` et `État : HTML_CANONIQUE_PRODUIT -
contrôle métier requis`.
```

## Produire une édition

Utilisez une conversation neuve dans chaque Projet. L’exemple couvre la période
du 3 au 13 octobre 2026 pour l’édition du 14 octobre 2026.

### Message initial dans le Projet Collecte

Envoyez uniquement ces trois lignes après avoir remplacé les dates.

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
NUMERIQUE
```

Le résultat doit fournir une ligne complète
`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | ...`.

Si la réponse commence par `A_COMPLETER`, arrêtez et n’envoyez pas le paquet au Projet
Rendu.

### Recherches suivantes pendant la Collecte

Restez dans la même conversation et activez le Web. Copiez la ligne complète
`REQUETE_A_ENVOYER` fournie par l’Assistant. Après chaque réponse :

1. vérifiez qu’au moins une source est visible dans l’interface ;
2. vérifiez `RESULTATS_RECHERCHE`, `REGISTRE_CUMULATIF`, la date ISO,
   `DANS_FENETRE` et `VALIDATION_METIER_REQUISE` ;
3. copiez seulement alors la nouvelle ligne `REQUETE_A_ENVOYER`.

La chaîne couvre successivement `RECHERCHE_NUMERIQUE`, `RECHERCHE_IA`,
`RECHERCHE_COMMANDE`, `RECHERCHE_RH` et `RECHERCHE_BERCY`. Si aucune source n’est
visible ou si la réponse commence par `A_COMPLETER`, relancez la même requête et ne
passez pas à la suivante.

Après validation de `RECHERCHE_BERCY`, la réponse doit contenir
`COLLECTE_TERMINEE_BEST_EFFORT` et `REQUETE_A_ENVOYER=VALIDER`. Il n’y a ni
recomptage, ni recherche ciblée, ni seuil bloquant. Désactivez alors le Web et
envoyez `VALIDER`.

### Validation dans le Projet Collecte

Désactivez le Web, puis envoyez uniquement :

```text
VALIDER
```

Le résultat doit contenir `CONTROLE_DATES`, `SOURCES_VALIDES`, `SOURCES_EXCLUES`,
`VALIDATION_TERMINEE`, puis `GENERER_PAQUET`. Si la réponse
commence par `A_COMPLETER`, arrêtez. Moins de cinq sources valides reste acceptable :
l’insuffisance est signalée dans `watch` et ne bloque pas le paquet JSON.

### Génération du paquet dans le Projet Collecte

Restez dans la même conversation et envoyez uniquement :

```text
GENERER_PAQUET
```

Le résultat doit contenir le paquet entre `SNUM_PAQUET_RENDU_V519_START` et
`SNUM_PAQUET_RENDU_V519_END`, puis se terminer par `PAQUET_RENDU_PRET`. Après
vérification, copiez le bloc entier entre les deux marqueurs. Si la réponse contient
`PAQUET_INCOMPLET`, arrêtez.

### Message suivant dans le Projet Rendu HTML, sans le Web

Créez une conversation neuve dans `Newsletter SNUM - Rendu HTML`. Remplacez la
dernière ligne par le bloc copié et envoyez :

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
Échappe toute valeur injectée comme HTML ; un apostrophe ASCII devient &#x27;.
Termine le bloc par exactement un saut de ligne après </html>.
Livre le HTML canonique au premier passage.
Ne pose aucune question.

COLLEZ ICI LE BLOC COMPLET SNUM_PAQUET_RENDU_V519
```

Le résultat doit contenir `## HTML COMPLET`, un unique bloc de
`<!doctype html>` à `</html>`, puis `## CONTROLES` et
`État : HTML_CANONIQUE_PRODUIT - contrôle métier requis`.

Le Projet Rendu ne recompte pas les mots. Ce contrôle appartient au Projet Collecte ;
le refaire pendant l’assemblage HTML peut produire un faux rejet du paquet.

Si la réponse commence par `A_COMPLETER`, arrêtez. N’envoyez aucune autre commande.

## Contrôle métier minimal

Vérifiez :

- aucun marqueur `@@` ;
- un seul `h1` et trois accès rapides ;
- les mêmes dates, titres et URL que dans le paquet ;
- le `<title>` affiche `edition_date_long`, jamais la date ISO ;
- chaque date affichée vient de `publication_date_long` ;
- chaque article dans sa rubrique ;
- exactement trois cartes essentielles à partir de trois articles ;
- la modale après le footer ;
- CSS et scripts DSFR 1.15.2 ;
- l’indication de nouvelle fenêtre sur les liens externes.

## Sources de vérité

- `EXEMPLE-PAQUET-RENDU-V5.19.json` : contrat d’exemple ;
- `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` : machine d’état séquentielle ;
- `02-METHODE-COLLECTE-SNUM-V5.23.md` : collecte et validation ;
- `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` : paquet compatible V519 ;
- `_source/05-BLOCS-HTML-CANONIQUES.md` : source HTML ;
- `scripts/build_split_kit.py` : générateur du gabarit et du ZIP ;
- `tests/test_split_projects.py` : contrôles du découpage ;
- `RAPPORT-V5.19.md` : preuve de la recette réelle ;
- `RAPPORT-V5.23.md` : preuve de la recette séquentielle après son exécution ;
- `_documentation/archives/` : versions antérieures, conservées hors de la racine.

La racine contient uniquement la Collecte V5.23, le Rendu V5.19 et les sources
permanentes nécessaires à leur génération. Les 8 fichiers d’installation listés plus
haut doivent y rester.
N’installez aucun fichier depuis `_documentation/archives/`.
