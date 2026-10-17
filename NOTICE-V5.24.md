<!-- PDG-LARGE-FILE-JUSTIFICATION: notice autonome pour une installation métier sans terminal ; elle contient les deux prompts système et les quatre messages dans leur ordre d’exécution. -->
<!-- PDG-BINARY-ASSET-JUSTIFICATION: les deux ZIP regroupent les fichiers nécessaires à l’installation manuelle de chaque Projet ; leurs sources et leur générateur restent versionnés. -->

# Configurer les deux Projets Newsletter SNUM

Le dispositif actif associe la Collecte V5.24 au Rendu HTML V5.19. La Collecte V5.24
fait valider chaque recherche Web par le métier, propage un `REGISTRE_CUMULATIF`
numéroté `U01…UN`, puis produit un paquet JSON en mode best effort après les cinq
recherches initiales, sans recomptage ni seuil bloquant.

- `Newsletter SNUM - Collecte` produit un `PAQUET_RENDU`.
- `Newsletter SNUM - Rendu HTML` transforme ce paquet en HTML canonique.

> **État de recette V5.24 : GO pour Collecte → JSON → Rendu HTML.**
> Le 17 octobre 2026, la recette réelle a produit automatiquement un paquet V519
> copiable et stable à la relance, puis un HTML canonique sans préambule ni altération
> des caractères contrôlés.

## Démarrage express dans une nouvelle conversation

1. Ouvrez une conversation neuve dans `Newsletter SNUM - Collecte`, avec le Web
   désactivé, puis envoyez `DATE_EDITION`, `PERIODE` et `NUMERIQUE` comme dans
   l’exemple ci-dessous.
2. Activez le Web lorsque l’Assistant affiche la première `REQUETE_A_ENVOYER`. Gardez
   le Web activé uniquement pendant les cinq recherches et envoyez une requête complète
   par message, dans l’ordre `NUMERIQUE → IA → COMMANDE → RH → BERCY`.
3. Après `COLLECTE_TERMINEE_BEST_EFFORT`, désactivez le Web et envoyez `VALIDER`, puis
   `GENERER_PAQUET`.
4. Cliquez sur **Copier le code** pour conserver le bloc JSON entier, marqueurs inclus.
5. Ouvrez une conversation neuve dans `Newsletter SNUM - Rendu HTML`, Web désactivé,
   puis utilisez le message complet de la section « Message suivant dans le Projet
   Rendu HTML » avec le bloc JSON à la place de la dernière ligne.

## Pourquoi deux Projets

Le Projet Collecte utilise le Web et prend les décisions éditoriales. Le Projet Rendu
HTML ne reçoit que le paquet JSON validé et assemble les blocs Bacoco. Cette séparation
évite qu’une conversation de recherche longue fasse oublier le gabarit HTML.

Les quatre ressources canoniques restent chacune sous 4 500 caractères. L’Assistant
peut ainsi les récupérer intégralement malgré sa limite de contexte par ressource.
Les deux ressources Collecte suivent la même limite.

## Fichiers actifs disponibles à la racine

Pour `Newsletter SNUM - Collecte`, utilisez les fichiers dans cet ordre :

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` : copiez tout son contenu dans
   **Instructions (expérimental)** ;
2. `02-METHODE-COLLECTE-SNUM-V5.24.md` : téléversez cette ressource ;
3. `03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md` : téléversez cette ressource.

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

1. `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` ;
2. `02-METHODE-COLLECTE-SNUM-V5.24.md` ;
3. `03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`.

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
3. Téléversez `02-METHODE-COLLECTE-SNUM-V5.24.md` et
   `03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md` dans les ressources.
4. Vérifiez que les deux ressources sont visibles et que leur indexation est terminée.
5. Enregistrez le Projet.

```text
`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
`NUMERIQUE`
Exige ces lignes. La date d’édition sert seulement au paquet.
`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide : ne
compare jamais la date d’édition aux bornes.
Entrée manquante, ambiguë ou fenêtre inversée :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`.
Charge `02-METHODE-COLLECTE-SNUM-V5.24.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`.

## Recherches validées par le métier

Sans Web, le message initial rend
`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web du <début> au <fin> inclus en France : <AXE>. Titre, URL HTTPS, date exacte.`
Fais une seule recherche Web par message :
`RECHERCHE_NUMERIQUE→RECHERCHE_IA`; `RECHERCHE_IA→RECHERCHE_COMMANDE`;
`RECHERCHE_COMMANDE→RECHERCHE_RH`; `RECHERCHE_RH→RECHERCHE_BERCY`;
`RECHERCHE_BERCY→VALIDER`. Sortie≠entrée.

services publics numériques, dématérialisation, inclusion et données ;
intelligence artificielle, modèles, régulation et usages publics ; commande publique,
achats, marchés et fournisseurs numériques ; ressources humaines publiques,
compétences, recrutement et formation ; ministères économiques et financiers,
directions et transformations.

Après chaque recherche, si une source est visible, rends `RESULTATS_RECHERCHE` non
vide, puis `REGISTRE_CUMULATIF`: recopie sans changement, ajoute chaque nouvelle URL
canonique unique : `U01` puis `max(Uxx)+1`; aucun réemploi :
`Uxx|rubrique|URL|date brute|date ISO|DANS_FENETRE=OUI|NON|titre|source|fait`.
`OUI` exige `DEBUT_ISO <= date ISO <= FIN_ISO`; sinon `NON`.
Affiche `VALIDATION_METIER_REQUISE`, puis obligatoirement la
`REQUETE_A_ENVOYER` suivante : aucune réponse de recherche ne se termine avant elle.
Son envoi valide les sources et décisions visibles. Ne répète aucun lot.
Même si `DANS_FENETRE=NON`, avance. Après `RECHERCHE_BERCY`,
rends `COLLECTE_TERMINEE_BEST_EFFORT`, désactive le Web et affiche
`REQUETE_A_ENVOYER=VALIDER`.

Source visible ou non ⇒ avance toujours. Sans source :
`RESULTATS_RECHERCHE=AUCUNE_SOURCE_PROUVEE`; registre inchangé ;
`RECHERCHE_SANS_SOURCE_PROUVEE | <rubrique>` ; `VALIDATION_METIER_REQUISE` ;
affiche exactement la requête suivante de l’ordre immuable, jamais `A_COMPLETER`.

## Valider en best effort

Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER` exécute seulement `VALIDATION`.
Affiche `CONTROLE_DATES`, `SOURCES_VALIDES` et `SOURCES_EXCLUES`.
Registre vide admis.
`valides + exclues = registre`.
Rends `VALIDATION_TERMINEE`; puis `REQUETE_A_ENVOYER=GENERER_PAQUET`.
À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; ne demande rien à
l’utilisateur et ne bloque jamais sur un nombre minimal de sources.

Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`.
Construis toi-même le JSON depuis `SOURCES_VALIDES`; ne demande jamais de paquet à
l’utilisateur. Si moins de cinq sources sont valides, signale l’insuffisance dans
`watch` sans bloquer le JSON. Applique exactement le schéma et tous les contrôles de
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`.
`schema_version`=`SNUM_PAQUET_RENDU_V519`; `watch`=`[]` ou objets `title`/`summary`.
Échappe tout guillemet interne en `\"`. Avant sortie, compte
les mots de chaque `fact` (≤25), `takeaway` et `snum_interest` (≤15), puis analyse
exactement le JSON émis avec un parseur. Sinon : `PAQUET_INCOMPLET | JSON_INVALIDE`.
`GENERER_PAQUET` réussi : réponds immédiatement par un seul bloc de code copiable :
bloc Markdown multiligne ` ```json `, lignes :
`SNUM_PAQUET_RENDU_V519_START`, le JSON, `SNUM_PAQUET_RENDU_V519_END`, puis
`PAQUET_RENDU_PRET`, fermé par ` ``` `. Aucun préambule ni texte hors du bloc.
Toute demande de redonner le JSON répète à l’identique ce même bloc complet, sans le
régénérer. N’émets jamais `PAQUET_RENDU_PRET`
si une limite échoue. Après analyse réussie, termine par `PAQUET_RENDU_PRET`.
`GENERER_PAQUET` n’est jamais `ETAT_INVALIDE` dans cet état. Une transition par tour.
```

## Installer Newsletter SNUM - Rendu HTML

1. Créez le Projet `Newsletter SNUM - Rendu HTML`.
2. Collez le bloc suivant dans **Instructions (expérimental)**.
3. Dans les ressources, téléversez les quatre ressources `CANON-HTML-*.md` listées
   dans la section précédente, dans l’ordre 21 à 24.
4. Vérifiez que les quatre noms sont visibles.
5. Attendez la fin de l’indexation et enregistrez le Projet.

```text
Tu es le Projet `Newsletter SNUM - Rendu HTML`. Rends tout `PAQUET_RENDU` validé en
HTML canonique, sans recherche ni réécriture.

Exécute uniquement `RENDRE_EDITION`. N’utilise pas le Web. Entrée : bloc JSON strict
entre `SNUM_PAQUET_RENDU_V519_START` et `SNUM_PAQUET_RENDU_V519_END`,
avec `schema_version`=`SNUM_PAQUET_RENDU_V519`.

Charge `21-CANON-HTML-COQUE-A-V5.19.md`, `22-CANON-HTML-COQUE-B-V5.19.md`,
`23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md` et
`24-CANON-HTML-SURVEILLER-VIDE-V5.19.md`. Lis entre leurs marqueurs
`SNUM_CANON_V519_*_START` et `SNUM_CANON_V519_*_END`. Elles définissent `COQUE_A`,
`COQUE_B`, `ESSENTIEL`, `RUBRIQUE`, `SURVEILLER` et `VIDE`. Concatène littéralement
`COQUE_A` puis `COQUE_B`, sans séparateur, avec le saut final de `COQUE_A`.
Copie les blocs sans ajouter, retirer, reformuler ni réindenter balise, classe,
dépendance, enveloppe, modale ou script. Marqueur absent = `CANON_MANQUANT`.

Valide seulement : JSON, schéma, champs obligatoires, `id` textuels non vides et
uniques, URL `https://` uniques, rubriques autorisées, 3 à 5 mots-clés et exactement
trois essentiels à partir de trois articles. Sous trois articles, aucun essentiel. Les
textes sont validés. Ne recompte pas les mots, ne reformule pas et n’invente aucun refus
de longueur.

`publication_date_iso` suit `AAAA-MM-JJ` et `publication_date_long` écrit le mois en
lettres ; les deux désignent le même jour.
Affiche seulement `publication_date_long`, sans conversion ni zéro initial. L’autre sert
au contrôle du paquet.

Assemble la page : `COQUE` ; section `ESSENTIEL` seulement si elle est requise,
avec exactement trois cartes ; une section `RUBRIQUE` par rubrique présente et un
article par source ; `SURVEILLER` seulement si `watch` n’est pas vide. Chaque essentiel
reste aussi dans sa rubrique. Remplace uniquement les marqueurs `@@...@@`. Échappe les
valeurs sans les altérer ni remplacer un caractère par un autre, dans cet ordre :
`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`, `'`→`&#x27;`.

Navigation : si `ESSENTIEL` existe, ajoute d’abord `L’essentiel` vers `#essentiel`, puis
les rubriques présentes, `À surveiller` vers `#surveiller` si sa section existe, enfin
`Archives`. Pour `RUBRIQUE`,
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

En cas de réussite, le premier caractère de la réponse est le `#` de `## HTML COMPLET`.
N’explique jamais l’assemblage. Rends uniquement ce titre, un unique bloc `html` de
`<!doctype html>` à `</html>`, puis `## CONTROLES` et `État :
HTML_CANONIQUE_PRODUIT - contrôle métier requis`.
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

Restez dans la même conversation. Ouvrez `+`, activez **Rechercher sur le web**, puis
envoyez exactement une requête par tour dans cet ordre :

```text
REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web du <début> au <fin> inclus en France : services publics numériques, dématérialisation, inclusion et données. Titre, URL HTTPS, date exacte.
REQUETE_A_ENVOYER=RECHERCHE_IA | Recherchez sur le Web du <début> au <fin> inclus en France : intelligence artificielle, modèles, régulation et usages publics. Titre, URL HTTPS, date exacte.
REQUETE_A_ENVOYER=RECHERCHE_COMMANDE | Recherchez sur le Web du <début> au <fin> inclus en France : commande publique, achats, marchés et fournisseurs numériques. Titre, URL HTTPS, date exacte.
REQUETE_A_ENVOYER=RECHERCHE_RH | Recherchez sur le Web du <début> au <fin> inclus en France : ressources humaines publiques, compétences, recrutement et formation. Titre, URL HTTPS, date exacte.
REQUETE_A_ENVOYER=RECHERCHE_BERCY | Recherchez sur le Web du <début> au <fin> inclus en France : ministères économiques et financiers, directions et transformations. Titre, URL HTTPS, date exacte.
```

Remplacez `<début>` et `<fin>` par les dates du message initial. La séquence ci-dessus
est la source de vérité. Après chaque réponse :

1. si une source est visible, vérifiez `RESULTATS_RECHERCHE`,
   `REGISTRE_CUMULATIF`, la date ISO et `DANS_FENETRE` ;
2. sinon, vérifiez `RESULTATS_RECHERCHE=AUCUNE_SOURCE_PROUVEE` et
   `RECHERCHE_SANS_SOURCE_PROUVEE` ;
3. vérifiez `VALIDATION_METIER_REQUISE` ;
4. envoyez la ligne suivante de la séquence fixe, même si la
   `REQUETE_A_ENVOYER` proposée par l’Assistant répète une rubrique.

Une recherche sans source ne bloque plus : le registre reste inchangé. N’envoyez
jamais deux fois la même rubrique. Si les résultats ou le registre ne sont pas
contrôlables, arrêtez la collecte au lieu de valider le paquet.

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
vérification, cliquez sur **Copier le code** et transmettez le bloc entier, marqueurs
inclus, au Projet Rendu HTML. Si vous redemandez le JSON, la réponse doit répéter ce
bloc complet. Si elle contient `PAQUET_INCOMPLET`, arrêtez.

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
Échappe toute valeur injectée sans l’altérer : &→&amp;, <→&lt;, >→&gt;, "→&quot;, '→&#x27;.
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
- `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` : machine d’état séquentielle ;
- `02-METHODE-COLLECTE-SNUM-V5.24.md` : collecte et validation ;
- `03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md` : paquet compatible V519 ;
- `_source/05-BLOCS-HTML-CANONIQUES.md` : source HTML ;
- `scripts/build_split_kit.py` : générateur du gabarit et du ZIP ;
- `tests/test_split_projects.py` : contrôles du découpage ;
- `RAPPORT-V5.19.md` : preuve de la recette réelle ;
- `RAPPORT-V5.24.md` : preuve de la recette séquentielle après son exécution ;
- `_documentation/archives/` : versions antérieures, conservées hors de la racine.

La racine contient uniquement la Collecte V5.24, le Rendu V5.19 et les sources
permanentes nécessaires à leur génération. Les 8 fichiers d’installation listés plus
haut doivent y rester.
N’installez aucun fichier depuis `_documentation/archives/`.
