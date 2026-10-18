# Notice opérationnelle Newsletter SNUM V5.23

Cette version utilise deux Projets Assistant enregistrés et un chat Web ordinaire.
Le métier n’utilise aucun terminal.

> **GO au 18 octobre 2026.** La recette réelle a validé la recherche composite,
> l’enregistrement best effort, le paquet V519 produit par `NORMALISER_V519` et le
> HTML canonique. Le chat Web a nécessité une relance et deux rubriques sont restées
> sans résultat daté ; ces limites sont signalées dans `watch`.

## Installation

### Projet Newsletter SNUM - Collecte

1. Copiez `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` dans les instructions.
2. Téléversez `02-METHODE-COLLECTE-SNUM-V5.23.md`.
3. Téléversez `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.
4. Attendez l’indexation des deux ressources et enregistrez.

### Projet Newsletter SNUM - Rendu HTML

1. Copiez `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md` dans les instructions.
2. Téléversez séparément `21-CANON-HTML-COQUE-A-V5.19.md`.
3. Téléversez `22-CANON-HTML-COQUE-B-V5.19.md`.
4. Téléversez `23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md`.
5. Téléversez `24-CANON-HTML-SURVEILLER-VIDE-V5.19.md`.
6. Attendez l’indexation des quatre ressources et enregistrez.

Les archives `Newsletter SNUM - Collecte.zip` et
`Newsletter SNUM - Rendu HTML.zip` regroupent ces fichiers. Décompressez-les :
ne téléversez jamais les ZIP eux-mêmes.

## Parcours métier

### 1. Projet Collecte

Dans une nouvelle conversation, Web désactivé, envoyez :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
RECHERCHE_COMPOSITE
```

La réponse doit être encadrée par
`REQUETE_COMPOSITE_A_COPIER_START` et
`REQUETE_COMPOSITE_A_COPIER_END`.

### 2. Nouveau chat Assistant ordinaire

Ouvrez un nouveau chat Assistant ordinaire, activez le Web, copiez la requête située
entre les marqueurs et envoyez-la. Elle recherche en un seul passage les cinq
rubriques et demande des lignes :

```text
RESULTAT|rubrique|URL_HTTPS|date_iso|titre|source|fait_factuel
```

Attendez la fin de la recherche, puis copiez toute la réponse.

### 3. Retour dans le Projet Collecte

Collez toute la réponse Web dans le chat Collecte d’origine. N’envoyez ni
`VALIDER`, ni `RECOMPTER`, ni `GENERER_PAQUET`.

La réponse attendue est :

```text
RESULTATS_COMPOSITES_ENREGISTRES | VALIDES=<n> | RUBRIQUES_SANS_RESULTAT=<codes ou AUCUNE>
REQUETE_A_ENVOYER=NORMALISER_V519
```

Envoyez ensuite exactement :

```text
NORMALISER_V519
```

Cette commande unique produit un paquet qui commence par
`SNUM_PAQUET_RENDU_V519_START` et se termine par :

```text
SNUM_PAQUET_RENDU_V519_END
PAQUET_RENDU_PRET
```

Une rubrique vide ou moins de cinq articles crée une alerte `watch`, sans bloquer
le JSON. Les URL en double, dates hors fenêtre et lignes invalides sont exclues.
Lorsqu’une rubrique possède un résultat valide, Collecte ignore toute ligne
`AUCUN_RESULTAT_DATE_DANS_FENETRE` contradictoire.

### 4. Projet Rendu HTML

Dans une nouvelle conversation, Web désactivé, copiez le paquet depuis
`SNUM_PAQUET_RENDU_V519_START` jusqu’à
`SNUM_PAQUET_RENDU_V519_END` inclus et envoyez-le.

La première ligne doit être `## HTML COMPLET`. La réponse contient ensuite un
unique bloc HTML puis :

```text
## CONTROLES
État : HTML_CANONIQUE_PRODUIT - contrôle métier requis
```

Tout texte avant `## HTML COMPLET` constitue un échec de conformité.

## Arrêt en cas d’erreur

- Si Collecte ne fournit pas la requête composite, vérifiez ses instructions et ses
  deux ressources.
- Si le chat Web ne renvoie aucune ligne `RESULTAT|`, recommencez une seule fois
  dans un nouveau chat ordinaire.
- Si Collecte répond `A_COMPLETER` ou `PAQUET_INCOMPLET`, ne transmettez pas le
  résultat au Projet Rendu.
- Si Rendu répond `CANON_MANQUANT`, remplacez ses quatre ressources par celles du
  kit courant et attendez leur indexation.
- Après trois échecs identiques, arrêtez et conservez l’URL de la conversation.

## Contrôle final

Vérifiez les dates, titres, URL, cinq rubriques ou alertes `watch`, identifiants
`U01…UN`, trois essentiels, absence de marqueur `@@`, navigation, titre
d’édition, DSFR 1.15.2 et indication de nouvelle fenêtre.

Le guide détaillé et les commandes de maintenance figurent dans `README.md`.
