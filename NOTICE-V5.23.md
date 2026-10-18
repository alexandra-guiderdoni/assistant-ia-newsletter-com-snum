# Notice opérationnelle Newsletter SNUM V5.23

Cette version utilise deux Projets Assistant enregistrés et deux conversations. Le
métier n’utilise aucun terminal ni chat Web intermédiaire.

> **Recette Assistant validée le 18 octobre 2026.** Collecte a lancé le Web et
> produit directement le JSON, puis Rendu a produit `## HTML COMPLET`. Le cas testé
> ne contenait aucun article validé et a été rendu en mode best effort avec les
> alertes `watch`.

## Installation

### Projet Newsletter SNUM - Collecte

1. Copiez `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` dans les instructions.
2. Téléversez `02-METHODE-COLLECTE-SNUM-V5.23.md`.
3. Téléversez `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.
4. Attendez l’indexation des deux ressources et enregistrez.
5. Activez le Web dans ce Projet.

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

Dans une nouvelle conversation, Web activé, envoyez seulement :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
```

Collecte lance la recherche Web, ouvre et filtre les sources, puis produit directement
un paquet qui commence par `SNUM_PAQUET_RENDU_V519_START` et se termine par :

```text
SNUM_PAQUET_RENDU_V519_END
PAQUET_RENDU_PRET
```

Il n’existe aucune requête à recopier ni commande intermédiaire. Une rubrique vide,
moins de cinq articles ou même zéro source valide crée des alertes `watch`, sans
bloquer le JSON. Les URL en double et dates hors fenêtre sont exclues.

### 2. Projet Rendu HTML

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

Un paquet `articles=[]` reste valide : le HTML contient `Collecte à compléter`,
puis `À surveiller` si des alertes `watch` sont présentes.

## Arrêt en cas d’erreur

- Si Collecte ne fournit pas le paquet, vérifiez que le Web est actif, ses
  instructions et ses deux ressources.
- Si Collecte répond `OUTIL_WEB_INDISPONIBLE`, recommencez une seule fois dans une
  conversation Collecte neuve avec les mêmes dates.
- Si Collecte répond `A_COMPLETER` ou `PAQUET_INCOMPLET`, ne transmettez pas le
  résultat au Projet Rendu.
- Si Rendu répond `CANON_MANQUANT`, remplacez ses quatre ressources par celles du
  kit courant et attendez leur indexation.
- Rendu ne doit pas répondre `A_COMPLETER` au seul motif que `articles=[]`.
- Après trois échecs identiques, arrêtez et conservez l’URL de la conversation.

## Contrôle final

Vérifiez les dates, titres, URL, cinq rubriques ou alertes `watch`, identifiants
`U01…UN`, trois essentiels, absence de marqueur `@@`, navigation, titre
d’édition, DSFR 1.15.2 et indication de nouvelle fenêtre.

Le guide détaillé et les commandes de maintenance figurent dans `README.md`.
