<!-- PDG-LARGE-FILE-JUSTIFICATION: notice autonome pour une installation métier sans terminal ; elle contient les deux prompts système et les quatre messages dans leur ordre d’exécution. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: le ZIP regroupe les six fichiers nécessaires à l’installation manuelle ; ses sources et son générateur restent versionnés. -->

# Configurer les deux Projets Newsletter SNUM V5.17

Cette version sépare la collecte éditoriale du rendu HTML.

- `Newsletter SNUM - Collecte` produit un `PAQUET_RENDU`.
- `Newsletter SNUM - Rendu HTML` transforme ce paquet en HTML canonique.

> **État de recette au 15 octobre 2026 : validé.** Une collecte réelle a produit
> 10 candidats, la validation en a retenu 4 et le premier message d’une conversation
> RENDU neuve a livré le HTML complet. Le HTML brut a ensuite chargé la feuille
> Bacoco publique, reproduit les styles calculés du site et obtenu
> `DOM_DIFF_COUNT=0` face au canon alimenté par le même paquet. Les détails sont
> dans `RAPPORT-V5.17.md`.

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

## Télécharger le kit

Téléchargez puis décompressez
`kit-dinum-snum-v5-17-deux-projets-6-fichiers.zip`.

Le dossier doit contenir exactement :

1. `PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md` ;
2. `PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md` ;
3. `CANON-HTML-01-COQUE-A-V5.17.md` ;
4. `CANON-HTML-02-COQUE-B-V5.17.md` ;
5. `CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md` ;
6. `CANON-HTML-04-SURVEILLER-VIDE-V5.17.md`.

N’ajoutez jamais le ZIP lui-même dans un Projet.

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
accès, `CLE_EVENEMENT`, décision. Une source est valide seulement si le format, les deux
bornes et l’accès valent `OUI`. Même fait réel = même clé. Garde la source la plus
directe, sinon la plus récente, sinon la première. Exclus chaque doublon avec
`DOUBLON_DE | titre conservé`. Compte le nombre exact d’entrées sous `CANDIDATS` et
contrôle-les toutes, sans utiliser de sous-liste préfiltrée. Vérifie
`valides + exclues = candidats`. Termine par
`VALIDATION_TERMINEE` seulement si l’égalité est exacte et au moins une source reste
valide.

Pendant `PAQUET`, n’utilise pas le Web. Transforme uniquement `SOURCES_VALIDES` en un
bloc JSON strict placé entre `SNUM_PAQUET_RENDU_V517_START` et
`SNUM_PAQUET_RENDU_V517_END`. N’ajoute aucun commentaire dans le bloc.

Le JSON contient exactement : `schema_version`=`SNUM_PAQUET_RENDU_V517`, `edition_date`,
`edition_date_long`, `window_start`, `window_end`, `articles`, `watch`. Chaque article
contient : `id`, `rubric`, `title`, `source`, `publication_date`,
`publication_date_iso`, `url`, `fact`, `keywords`, `takeaway`, `snum_interest`,
`essential`. `rubric` vaut seulement `numerique`, `ia`, `commande`, `rh` ou `bercy`.
`keywords` contient 3 à 5 chaînes. `fact` contient au plus 25 mots ; `takeaway` et
`snum_interest` au plus 15 mots. Les dates longues n’incluent aucun jour de semaine.
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
   dans la section précédente, dans l’ordre 01 à 04.
4. Vérifiez que les quatre noms sont visibles.
5. Attendez la fin de l’indexation et enregistrez le Projet.

```text
Tu es le Projet `Newsletter SNUM - Rendu HTML`. Tu transformes un `PAQUET_RENDU` validé
en HTML canonique. Tu ne recherches, ne sélectionnes et ne reformules aucune information
éditoriale. Tu ne publies rien et n’envoies aucun courriel.

Exécute uniquement `RENDRE_EDITION`. N’utilise pas le Web. L’entrée doit contenir un
bloc JSON strict entre `SNUM_PAQUET_RENDU_V517_START` et `SNUM_PAQUET_RENDU_V517_END`,
avec `schema_version`=`SNUM_PAQUET_RENDU_V517`.

Charge séparément les quatre ressources suivantes, toutes requises :
`CANON-HTML-01-COQUE-A-V5.17.md`, `CANON-HTML-02-COQUE-B-V5.17.md`,
`CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md` et
`CANON-HTML-04-SURVEILLER-VIDE-V5.17.md`. Retrouve chaque contenu par ses marqueurs
`SNUM_CANON_V517_*_START` et `SNUM_CANON_V517_*_END`. La troisième ressource contient
les blocs `SNUM_BLOC_V517_ESSENTIEL` et `SNUM_BLOC_V517_RUBRIQUE` ; la quatrième les
blocs `SNUM_BLOC_V517_SURVEILLER` et `SNUM_BLOC_V517_VIDE`. Assemble la coque en
concaténant littéralement `COQUE_A` puis `COQUE_B`. Copie tous les blocs littéralement.
N’ajoute, ne retire, ne reformule et ne réindente aucune balise, classe, dépendance,
enveloppe, modale ou script. L’absence d’un des huit marqueurs de ressource vaut
`CANON_MANQUANT`.

Valide uniquement la structure du paquet : JSON, schéma, champs obligatoires, URL
absolues `https://`, rubriques autorisées, tableaux de 3 à 5 mots-clés et exactement
trois essentiels à partir de trois articles. Sous trois articles, aucun essentiel. Le
Projet Collecte a déjà validé les textes. Ne recompte pas les mots, ne reformule aucun
champ et ne refuse jamais un paquet pour une longueur de texte supposée.

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
Valide séparément le format, les deux bornes
et l’accès intégral de chaque candidat.
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
Produis le JSON strict entre SNUM_PAQUET_RENDU_V517_START
et SNUM_PAQUET_RENDU_V517_END.
Vérifie les champs, les URL, les longueurs
et le nombre d’essentiels.
Ne rédige aucun HTML.
Ne pose aucune question.
```

Le résultat doit se terminer par `PAQUET_RENDU_PRET`. Après vérification, copiez le bloc entier,
du marqueur `SNUM_PAQUET_RENDU_V517_START` au marqueur
`SNUM_PAQUET_RENDU_V517_END` inclus.

Si la réponse contient `PAQUET_INCOMPLET`, arrêtez.

### Message 4 dans le Projet Rendu HTML, sans le Web

Créez une conversation neuve dans `Newsletter SNUM - Rendu HTML`. Remplacez la
dernière ligne par le bloc copié et envoyez :

```text
PHASE RENDRE_EDITION.
N’utilise pas le Web.
Utilise le PAQUET_RENDU ci-dessous sans modifier ses données.
Charge séparément les quatre ressources CANON-HTML V5.17.
Livre le HTML canonique au premier passage.
Ne pose aucune question.

COLLEZ ICI LE BLOC COMPLET SNUM_PAQUET_RENDU_V517
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
- chaque article dans sa rubrique ;
- exactement trois cartes essentielles à partir de trois articles ;
- la modale après le footer ;
- CSS et scripts DSFR 1.15.2 ;
- l’indication de nouvelle fenêtre sur les liens externes.

## Sources de vérité

- `EXEMPLE-PAQUET-RENDU-V5.17.json` : contrat d’exemple ;
- `05-BLOCS-HTML-CANONIQUES.md` : source HTML ;
- `CANON-HTML-01-COQUE-A-V5.17.md` à
  `CANON-HTML-04-SURVEILLER-VIDE-V5.17.md` : ressources à téléverser ;
- `scripts/build_split_kit.py` : générateur des ressources et du ZIP ;
- `tests/test_split_projects.py` : contrôles du découpage.
