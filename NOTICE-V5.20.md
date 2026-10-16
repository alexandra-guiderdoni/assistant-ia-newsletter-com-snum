<!-- PDG-LARGE-FILE-JUSTIFICATION: notice autonome pour une installation métier sans terminal ; elle contient les deux prompts système et les quatre messages dans leur ordre d’exécution. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: les deux ZIP regroupent les fichiers nécessaires à l’installation manuelle de chaque Projet ; leurs sources et leur générateur restent versionnés. -->

# Configurer les deux Projets Newsletter SNUM

Le dispositif actif associe la Collecte V5.20 au Rendu HTML V5.19. La Collecte V5.20
remplace les trois anciens prompts métier par un message contenant les deux variables,
puis les commandes courtes `VALIDER` et `GENERER_PAQUET`.

- `Newsletter SNUM - Collecte` produit un `PAQUET_RENDU`.
- `Newsletter SNUM - Rendu HTML` transforme ce paquet en HTML canonique.

> **État de recette au 15 octobre 2026 : Collecte V5.20 `GO`.** Une conversation neuve
> a produit `COLLECTE_TERMINEE`, `VALIDATION_TERMINEE` et `PAQUET_RENDU_PRET` avec
> `VALIDER`, puis `GENERER_PAQUET`. Le JSON a été analysé avec cinq articles, cinq URL
> uniques et trois essentiels. Le Rendu V5.19 reste
> `NO-GO` : le rendu local retourne
> `HTML_CANONIQUE_OK`. Le Projet Rendu produit le gabarit complet, mais son dernier HTML
> mesure 18 781 octets contre 18 756 pour le canon local, avec une empreinte différente,
> un lien `#numerique` sans section cible et aucun saut de ligne final. L’identité à
> 100 % demandée n’est donc pas atteinte. Voir `RAPPORT-V5.19.md`.

## Pourquoi deux Projets

Le Projet Collecte utilise le Web et prend les décisions éditoriales. Le Projet Rendu
HTML ne reçoit que le paquet JSON validé et assemble les blocs Bacoco. Cette séparation
évite qu’une conversation de recherche longue fasse oublier le gabarit HTML.

Les quatre ressources canoniques restent chacune sous 4 500 caractères. L’Assistant
peut ainsi les récupérer intégralement malgré sa limite de contexte par ressource.
Les deux ressources Collecte suivent la même limite.

## Fichiers actifs disponibles à la racine

Pour `Newsletter SNUM - Collecte`, utilisez les fichiers dans cet ordre :

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md` : copiez tout son contenu dans
   **Instructions (expérimental)** ;
2. `02-METHODE-COLLECTE-SNUM-V5.20.md` : téléversez cette ressource ;
3. `03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md` : téléversez cette ressource.

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

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md` ;
2. `02-METHODE-COLLECTE-SNUM-V5.20.md` ;
3. `03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md`.

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
3. Téléversez `02-METHODE-COLLECTE-SNUM-V5.20.md` et
   `03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md` dans les ressources.
4. Vérifiez que les deux ressources sont visibles et que leur indexation est terminée.
5. Enregistrez le Projet.

```text
`Newsletter SNUM - Collecte` : sans HTML, publication ou courriel ; 3 tours.

## Entrées

`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`

Extrais silencieusement les dates en `AAAA-MM-JJ`. `DATE_EDITION=2026-10-14` avec
fenêtre `2026-10-03..2026-10-13` est valide : `DATE_EDITION` sert uniquement au
paquet. Ne compare jamais la date d’édition aux bornes ; poursuis `COLLECTE`.
Entrée manquante, ambiguë ou inversée :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`, puis arrêt.

Charge `02-METHODE-COLLECTE-SNUM-V5.20.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md` avec leurs marqueurs. Sinon :
`A_COMPLETER | RESSOURCE_MANQUANTE | <nom>`.

## COLLECTE — EXÉCUTION AVANT RENDU

Au tour du message initial, exécute seulement `COLLECTE` ; Web immédiat si valide.
Avant toute réponse, termine les appels Web exigés par la méthode. Ensuite, rends
une seule réponse complète commençant par `TRACE_RECHERCHE`.

Le tout premier caractère visible est le `T` de `TRACE_RECHERCHE`. N’affiche aucun
titre avant les appels Web. Affiche intégralement `TRACE_RECHERCHE`,
`COUVERTURE_COLLECTE`, puis `CANDIDATS`. Les trois titres seuls sont invalides.
Sans plan ni « continuer » ; atteins le terminal.

Zéro résultat reste `STATUT_WEB=EXECUTEE | URL_EXAMINEES=AUCUNE` et n’est pas
`OUTIL_WEB_INDISPONIBLE`. Poursuis toutes les requêtes. Échec technique :
`A_COMPLETER | OUTIL_WEB_INDISPONIBLE | <erreur exacte>`.

Après `CANDIDATS`, affiche `DANS_FENETRE=OUI|NON` par URL, puis une fois
`NB_DANS_FENETRE = N`. `N` compte seulement les URL uniques `OUI`, jamais tous les
candidats : 7 candidats dont 5 `OUI` donne `NB_DANS_FENETRE = 5`. Puis applique la
branche : `N >= 5` termine par `COLLECTE_TERMINEE`; sinon termine par
`A_COMPLETER | COLLECTE_INSUFFISANTE | NB_DANS_FENETRE=N`. Blocage : `2026-10-01` vaut `NON` pour
`2026-10-03..2026-10-13` ; un mois seul reste `INCONNUE` et `NON` ; si `OUI` != `N`,
corrige et recompte. Ne lance pas `VALIDATION`.

## Tours suivants

Au tour du message `VALIDER`, exécute seulement `VALIDATION`, sans Web :
`VALIDATION_TERMINEE`, puis `ETAPE_SUIVANTE | Envoyez GENERER_PAQUET`; sinon échec.
Ne lance pas `PAQUET`.

Au tour du message `GENERER_PAQUET`, exécute seulement `PAQUET`, sans Web : JSON
balisé puis `PAQUET_RENDU_PRET`, ou `PAQUET_INCOMPLET` sans JSON.

Toute autre commande : `A_COMPLETER | ETAT_INVALIDE | commande attendue : <VALIDER
ou GENERER_PAQUET>`. Ne lance jamais deux étapes dans le même tour.
```

## Installer Newsletter SNUM - Rendu HTML

1. Créez le Projet `Newsletter SNUM - Rendu HTML`.
2. Collez le bloc suivant dans **Instructions (expérimental)**.
3. Dans les ressources, téléversez les quatre ressources `CANON-HTML-*.md` listées
   dans la section précédente, dans l’ordre 21 à 24.
4. Vérifiez que les quatre noms sont visibles.
5. Attendez la fin de l’indexation et enregistrez le Projet.

```text
Tu es le Projet `Newsletter SNUM - Rendu HTML`. Transforme un `PAQUET_RENDU` validé en
HTML canonique, sans recherche, réécriture, publication ni courriel.

Exécute uniquement `RENDRE_EDITION`. N’utilise pas le Web. L’entrée doit contenir un
bloc JSON strict entre `SNUM_PAQUET_RENDU_V519_START` et `SNUM_PAQUET_RENDU_V519_END`,
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

Valeurs exactes : `numerique` donne navigation `Numérique`, titre et tag `NUMERIQUE`,
sans classe de section ; `ia` donne `Intelligence artificielle`, `INTELLIGENCE
ARTIFICIELLE (IA)`, classe `section-muted` ; `commande` donne `Commande publique`,
`COMMANDE PUBLIQUE`, sans classe ; `rh` donne `Ressources humaines`, `RESSOURCES
HUMAINES`, classe `section-muted` ; `bercy` donne `Vie de Bercy`, `VIE DE BERCY`, sans
classe.

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

Activez le Web dans l’interface, puis envoyez uniquement ces deux lignes après avoir
remplacé les dates. Ne saisissez aucun nom de phase.

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
```

Le résultat doit contenir `COUVERTURE_COLLECTE`, `CANDIDATS`,
`COLLECTE_TERMINEE` et `ETAPE_SUIVANTE | Envoyez VALIDER`.

Si la réponse commence par `A_COMPLETER`, arrêtez et n’envoyez pas le paquet au Projet
Rendu.

### Premier message de poursuite dans le Projet Collecte

Restez dans la même conversation et envoyez uniquement :

```text
VALIDER
```

Le résultat doit contenir `CONTROLE_DATES`, `SOURCES_VALIDES`, `SOURCES_EXCLUES`,
`VALIDATION_TERMINEE` et `ETAPE_SUIVANTE | Envoyez GENERER_PAQUET`. Si la réponse
commence par `A_COMPLETER`, arrêtez.

### Second message de poursuite dans le Projet Collecte

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
- `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md` : orchestration automatique ;
- `02-METHODE-COLLECTE-SNUM-V5.20.md` : collecte et validation ;
- `03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md` : paquet compatible V519 ;
- `_source/05-BLOCS-HTML-CANONIQUES.md` : source HTML ;
- `scripts/build_split_kit.py` : générateur du gabarit et du ZIP ;
- `tests/test_split_projects.py` : contrôles du découpage ;
- `RAPPORT-V5.19.md` : preuve de la recette réelle ;
- `RAPPORT-V5.20.md` : preuve des recettes Collecte avec `VALIDER` et
  `GENERER_PAQUET` ;
- `_documentation/archives/` : versions antérieures, conservées hors de la racine.

La racine contient uniquement la Collecte V5.20, le Rendu V5.19 et les sources
permanentes nécessaires à leur génération. Les 8 fichiers d’installation listés plus
haut doivent y rester.
N’installez aucun fichier depuis `_documentation/archives/`.
