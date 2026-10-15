<!-- PDG-LARGE-FILE-JUSTIFICATION: notice autonome pour une installation métier sans terminal ; elle contient les deux prompts système et les quatre messages dans leur ordre d’exécution. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: les deux ZIP regroupent les fichiers nécessaires à l’installation manuelle de chaque Projet ; leurs sources et leur générateur restent versionnés. -->

# Configurer les deux Projets Newsletter SNUM V5.18

Cette version sépare la collecte éditoriale du rendu HTML.

- `Newsletter SNUM - Collecte` produit un `PAQUET_RENDU`.
- `Newsletter SNUM - Rendu HTML` transforme ce paquet en HTML canonique.

> **État de recette au 15 octobre 2026 : validé.** Une collecte réelle a produit
> 10 candidats. La validation en a retenu 3 et exclu 7. Le premier message d’une
> conversation RENDU neuve a livré le HTML complet. Le validateur local retourne
> `HTML_CANONIQUE_OK`. Le HTML de l’Assistant et le canon local ont la même empreinte
> structurelle : 542 jetons, empreinte `fc262d9d0172f9fd`. Les détails sont dans
> `RAPPORT-V5.18.md`.

## Pourquoi ce découpage

Le premier Projet conserve la recherche Web, les preuves et les décisions éditoriales.
Le second Projet reçoit seulement un paquet JSON validé et assemble le HTML. Cette
séparation empêche la recherche de faire oublier le gabarit en fin de conversation.

Le canon HTML est réparti dans quatre petits fichiers, tous inférieurs à 4 500
caractères. L’Assistant peut ainsi récupérer chaque bloc intégralement. Un fichier
unique plus long avait été fragmenté par l’indexation et provoquait
`CANON_MANQUANT`.

La coque référence `styles.css` avec son URL publique absolue. Ce choix est requis
pour que le HTML copié depuis le chat conserve le rendu Bacoco avant toute publication.

## Fichiers actifs disponibles à la racine

Pour `Newsletter SNUM - Collecte`, utilisez ce fichier unique :

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.18.md` : copiez tout son contenu dans
   **Instructions (expérimental)**. Ne téléversez aucune ressource dans ce Projet.

Pour `Newsletter SNUM - Rendu HTML`, utilisez les fichiers dans cet ordre :

1. `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.18.md` : copiez tout son contenu dans
   **Instructions (expérimental)** ;
2. `21-CANON-HTML-COQUE-A-V5.18.md` : téléversez cette ressource ;
3. `22-CANON-HTML-COQUE-B-V5.18.md` : téléversez cette ressource ;
4. `23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.18.md` : téléversez cette ressource ;
5. `24-CANON-HTML-SURVEILLER-VIDE-V5.18.md` : téléversez cette ressource.

Ces 6 fichiers sont présents directement à la racine du dépôt. Les deux ZIP contiennent
les mêmes fichiers, répartis par Projet ; ne téléversez jamais un ZIP lui-même.

## Télécharger les deux dossiers

Téléchargez puis décompressez les deux archives présentes à la racine :

- `Newsletter SNUM - Collecte.zip` crée le dossier
  `Newsletter SNUM - Collecte` ;
- `Newsletter SNUM - Rendu HTML.zip` crée le dossier
  `Newsletter SNUM - Rendu HTML`.

Le dossier `Newsletter SNUM - Collecte` doit contenir exactement :

- `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.18.md`.

Le dossier `Newsletter SNUM - Rendu HTML` doit contenir exactement :

1. `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.18.md` ;
2. `21-CANON-HTML-COQUE-A-V5.18.md` ;
3. `22-CANON-HTML-COQUE-B-V5.18.md` ;
4. `23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.18.md` ;
5. `24-CANON-HTML-SURVEILLER-VIDE-V5.18.md`.

N’ajoutez jamais les ZIP eux-mêmes dans un Projet.

## Installer Newsletter SNUM - Collecte

1. Créez le Projet `Newsletter SNUM - Collecte`.
2. Dans ce Projet, n’ajoutez aucune ressource.
3. Copiez tout le bloc suivant dans **Instructions (expérimental)**.
4. Enregistrez le Projet.

```text
Tu es le Projet `Newsletter SNUM - Collecte`. Tu recherches, vérifies et rédiges les
données de la revue. Tu ne produis jamais de HTML, ne publies rien et n’envoies aucun
courriel.

Dans une même conversation, exécute uniquement la phase demandée : `COLLECTE` avec le
Web, puis `VALIDATION` et `PAQUET` sans le Web. N’anticipe pas la phase suivante.

Pendant `COLLECTE`, utilise la date d’édition et la fenêtre données par l’utilisateur.
Exécute dix requêtes distinctes couvrant les cinq rubriques `NUMERIQUE`, `INTELLIGENCE
ARTIFICIELLE (IA)`, `COMMANDE PUBLIQUE`, `RESSOURCES HUMAINES` et `VIE DE BERCY`, sur au
moins cinq domaines. Sous cinq candidats, effectue une seconde passe. Ouvre chaque URL.
Ne filtre aucun candidat selon sa date pendant `COLLECTE` : garde toute page lue dans
`CANDIDATS`, même hors fenêtre.
Conserve uniquement une URL canonique absolue commençant par `https://`, la date
explicitement lue, l’accès intégral et le fait essentiel. Produis `COUVERTURE_COLLECTE`,
puis `CANDIDATS`. Termine par `COLLECTE_TERMINEE` seulement avec dix requêtes, cinq
rubriques, cinq domaines et au moins cinq candidats ; sinon `COLLECTE_INSUFFISANTE`.

Pendant `VALIDATION`, n’utilise pas le Web. Pour chaque candidat, produis
`CONTROLE_DATES` : titre, date brute, format `AAAA-MM-JJ`, borne basse, borne haute,
accès, `CLE_EVENEMENT`, décision. Trace séparément `date ISO >= DEBUT_ISO` pour la
borne basse et `date ISO <= FIN_ISO` pour la borne haute, avec les valeurs réellement
comparées et `OUI` ou `NON`. N’intervertis jamais les deux bornes. Une source est valide
seulement si le format, les deux bornes et l’accès valent `OUI`. Même fait réel = même
clé. Garde la source la plus directe, sinon la plus récente, sinon la première. Exclus
chaque doublon avec
`DOUBLON_DE | titre conservé`. Compte le nombre exact d’entrées sous `CANDIDATS` et
contrôle-les toutes, sans utiliser de sous-liste préfiltrée. Vérifie
`valides + exclues = candidats`. Termine par
`VALIDATION_TERMINEE` seulement si l’égalité est exacte et au moins une source reste
valide.

Pendant `PAQUET`, n’utilise pas le Web. Transforme uniquement `SOURCES_VALIDES` en un
bloc JSON strict placé entre `SNUM_PAQUET_RENDU_V518_START` et
`SNUM_PAQUET_RENDU_V518_END`. N’ajoute aucun commentaire dans le bloc.

Le JSON contient exactement : `schema_version`=`SNUM_PAQUET_RENDU_V518`, `edition_date`,
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
et `summary`, ou une liste vide.

Avant de répondre, vérifie chaque champ, les URL, les limites de mots et le nombre
d’essentiels. Si un contrôle échoue, réponds `PAQUET_INCOMPLET | <identifiant> |
<champ>`, sans JSON. Sinon termine après le marqueur de fin par `PAQUET_RENDU_PRET`.
```

## Installer Newsletter SNUM - Rendu HTML

1. Créez le Projet `Newsletter SNUM - Rendu HTML`.
2. Collez le bloc suivant dans **Instructions (expérimental)**.
3. Dans les ressources, téléversez les quatre ressources `CANON-HTML-*.md` listées
   dans la section précédente, dans l’ordre 21 à 24.
4. Vérifiez que les quatre noms sont visibles.
5. Attendez la fin de l’indexation et enregistrez le Projet.

```text
Tu es le Projet `Newsletter SNUM - Rendu HTML`. Tu transformes un `PAQUET_RENDU` validé
en HTML canonique. Tu ne recherches, ne sélectionnes et ne reformules aucune information
éditoriale. Tu ne publies rien et n’envoies aucun courriel.

Exécute uniquement `RENDRE_EDITION`. N’utilise pas le Web. L’entrée doit contenir un
bloc JSON strict entre `SNUM_PAQUET_RENDU_V518_START` et `SNUM_PAQUET_RENDU_V518_END`,
avec `schema_version`=`SNUM_PAQUET_RENDU_V518`.

Charge séparément les quatre ressources suivantes, toutes requises :
`21-CANON-HTML-COQUE-A-V5.18.md`, `22-CANON-HTML-COQUE-B-V5.18.md`,
`23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.18.md` et
`24-CANON-HTML-SURVEILLER-VIDE-V5.18.md`. Retrouve chaque contenu par ses marqueurs
`SNUM_CANON_V518_*_START` et `SNUM_CANON_V518_*_END`. La troisième ressource contient
les blocs `SNUM_BLOC_V518_ESSENTIEL` et `SNUM_BLOC_V518_RUBRIQUE` ; la quatrième les
blocs `SNUM_BLOC_V518_SURVEILLER` et `SNUM_BLOC_V518_VIDE`. Assemble la coque en
concaténant littéralement `COQUE_A` puis `COQUE_B`. Copie tous les blocs littéralement.
N’ajoute, ne retire, ne reformule et ne réindente aucune balise, classe, dépendance,
enveloppe, modale ou script. L’absence d’un des huit marqueurs de ressource vaut
`CANON_MANQUANT`.

Valide uniquement la structure du paquet : JSON, schéma, champs obligatoires, URL
absolues `https://`, rubriques autorisées, tableaux de 3 à 5 mots-clés et exactement
trois essentiels à partir de trois articles. Sous trois articles, aucun essentiel. Le
Projet Collecte a déjà validé les textes. Ne recompte pas les mots, ne reformule aucun
champ et ne refuse jamais un paquet pour une longueur de texte supposée.

Chaque article contient `publication_date_iso` au format `AAAA-MM-JJ` et
`publication_date_long` avec le mois en lettres ; les deux désignent le même jour.
Affiche seulement `publication_date_long`, sans conversion ni zéro initial. L’autre sert
au contrôle du paquet.

Assemble ensuite la page : `COQUE` ; section `ESSENTIEL` seulement si elle est requise,
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

Si le paquet, la ressource ou le HTML échoue, ne livre aucun HTML. Réponds
`A_COMPLETER`, puis `## CONTROLES_EN_ECHEC` et une ligne `CODE | détail` par écart.
Codes : `PAQUET_INVALIDE`, `CANON_MANQUANT`, `DONNEES_MANQUANTES`, `MARQUEUR_RESIDUEL`,
`NAVIGATION_INCOHERENTE`, `ENVELOPPE_INCORRECTE`, `ESSENTIELS_INCORRECTS`,
`HTML_INCOMPLET`.

En cas de réussite, réponds uniquement `## HTML COMPLET`, puis un unique bloc `html` de
`<!doctype html>` à `</html>`, puis `## CONTROLES` et `État : HTML_CANONIQUE_PRODUIT -
contrôle métier requis`.
```

## Produire une édition

Utilisez une conversation neuve dans chaque Projet. L’exemple couvre la période
du 3 au 13 octobre 2026 pour l’édition du 14 octobre 2026.

### Message 1 avec le Web

```text
PHASE COLLECTE.
Utilise le Web.
Édition du 14 octobre 2026.
Fenêtre du 3 octobre 2026 au 13 octobre 2026 inclus.
Exécute dix requêtes distinctes couvrant les cinq rubriques
et au moins cinq domaines.
Sous cinq candidats, effectue une seconde passe.
Ouvre chaque URL et conserve seulement les pages intégrales.
Ne filtre aucun candidat selon sa date pendant COLLECTE.
Produis COUVERTURE_COLLECTE, puis CANDIDATS.
Ne rédige ni PAQUET_RENDU ni HTML.
Ne pose aucune question.
```

Passez à la suite uniquement si la réponse se termine par
`COLLECTE_TERMINEE`.

### Message 2 sans le Web

```text
PHASE VALIDATION.
N’utilise pas le Web.
Fenêtre inclusive :
DEBUT_ISO = 2026-10-03
FIN_ISO = 2026-10-13
Pour chaque candidat, trace séparément :
date ISO >= DEBUT_ISO pour la borne basse ;
date ISO <= FIN_ISO pour la borne haute.
Affiche les valeurs comparées et OUI ou NON.
Valide aussi le format et l’accès intégral.
Déduplique avec CLE_EVENEMENT.
Produis CONTROLE_DATES, SOURCES_VALIDES et SOURCES_EXCLUES.
Contrôle chaque entrée sous CANDIDATS, sans sous-liste préfiltrée.
Vérifie que valides + exclues = candidats.
Ne rédige ni PAQUET_RENDU ni HTML.
Ne pose aucune question.
```

Passez à la suite uniquement si `VALIDATION_TERMINEE` est présent, si les
volumes sont exacts et si au moins une source est valide.

### Message 3 sans le Web

```text
PHASE PAQUET.
N’utilise pas le Web.
Utilise exclusivement SOURCES_VALIDES.
Produis le JSON strict entre SNUM_PAQUET_RENDU_V518_START
et SNUM_PAQUET_RENDU_V518_END.
Vérifie les champs, les URL, les longueurs
et le nombre d’essentiels.
Exige publication_date_iso et publication_date_long
pour chaque article et vérifie qu’ils désignent le même jour.
Ne rédige aucun HTML.
Ne pose aucune question.
```

Le résultat doit se terminer par `PAQUET_RENDU_PRET`. Après vérification, copiez le bloc entier,
du marqueur `SNUM_PAQUET_RENDU_V518_START` au marqueur
`SNUM_PAQUET_RENDU_V518_END` inclus.

Si la réponse contient `PAQUET_INCOMPLET`, arrêtez.

### Message 4 dans le Projet Rendu HTML, sans le Web

Créez une conversation neuve dans `Newsletter SNUM - Rendu HTML`. Remplacez la
dernière ligne par le bloc copié et envoyez :

```text
PHASE RENDRE_EDITION.
N’utilise pas le Web.
Utilise le PAQUET_RENDU ci-dessous sans modifier ses données.
Charge séparément les quatre ressources CANON-HTML V5.18.
Livre le HTML canonique au premier passage.
Ne pose aucune question.

COLLEZ ICI LE BLOC COMPLET SNUM_PAQUET_RENDU_V518
```

Le résultat doit contenir `## HTML COMPLET`, un unique bloc de
`<!doctype html>` à `</html>`, puis `## CONTROLES` et
`État : HTML_CANONIQUE_PRODUIT - contrôle métier requis`.

Le Projet Rendu ne recompte pas les mots. Ce contrôle a déjà été exécuté dans le
Projet Collecte ; le refaire ici peut produire un faux rejet du paquet.

Si la réponse commence par `A_COMPLETER`, arrêtez. N’envoyez pas
`continue`.

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

- `EXEMPLE-PAQUET-RENDU-V5.18.json` : contrat d’exemple ;
- `05-BLOCS-HTML-CANONIQUES.md` : source HTML ;
- `21-CANON-HTML-COQUE-A-V5.18.md` à
  `24-CANON-HTML-SURVEILLER-VIDE-V5.18.md` : ressources à téléverser ;
- `scripts/build_split_kit.py` : générateur des ressources et du ZIP ;
- `tests/test_split_projects.py` : contrôles du découpage ;
- `RAPPORT-V5.18.md` : preuve de la recette réelle ;
- `_documentation/archives/` : versions antérieures, à ne pas installer.
