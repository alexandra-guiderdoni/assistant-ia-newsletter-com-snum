# Rapport de recette V5.17

Date : 15 octobre 2026

## Verdict

GO pour la chaîne en deux Projets Assistant DINUM :

1. `Newsletter SNUM - Collecte` produit un paquet JSON validé ;
2. `Newsletter SNUM - Rendu HTML` livre le HTML canonique au premier message d’une
   conversation neuve ;
3. le HTML brut, ouvert hors de GitHub Pages, charge la feuille Bacoco publique et
   reproduit les styles calculés de la page de référence ;
4. la comparaison déterministe du DOM avec le canon Bacoco, alimenté par le même
   paquet éditorial, retourne `DOM_DIFF_COUNT=0`.

Le test réel a abouti sans `continue`, sans script côté métier, sans publication et
sans envoi de courriel.

## Recette réelle

### Collecte

- Le Web était activé uniquement pour `COLLECTE`.
- 10 candidats ont été produits après 10 requêtes couvrant les 5 rubriques et au
  moins 5 domaines.
- Aucun candidat n’a été filtré selon sa date pendant cette phase.

### Validation

- Le Web était désactivé.
- Les 10 candidats ont été contrôlés séparément.
- 4 sources ont été validées.
- 6 sources ont été exclues.
- Le contrôle `4 + 6 = 10` a réussi.
- Les exclusions couvraient les dates hors fenêtre et les dates imprécises.

### Paquet

- Le JSON strict était parseable.
- Le schéma était `SNUM_PAQUET_RENDU_V517`.
- Le paquet contenait 4 articles et exactement 3 essentiels.
- Chaque fait comptait au plus 25 mots.
- Chaque synthèse comptait au plus 15 mots.
- Chaque article comportait 5 mots-clés et une URL HTTPS.

### Rendu HTML

- La première tentative avec une ressource canonique unique de 11 122 octets a
  échoué avec `A_COMPLETER / CANON_MANQUANT`.
- Le canon a été réparti dans 4 ressources autonomes de 2 137, 3 779, 2 475 et
  878 octets.
- Une conversation RENDU neuve a alors livré le HTML complet au premier message.
- La réponse finale a cité exactement les 4 nouvelles ressources.
- Le HTML extrait mesurait 16 037 caractères.
- L’état final était `HTML_CANONIQUE_PRODUIT - contrôle métier requis`.
- Une correction de portabilité a ensuite été appliquée à la première ressource.
- Une conversation RENDU neuve a livré un HTML corrigé de 16 069 caractères.
- Le premier rendu strict a encore révélé 12 écarts au canon : le lien de navigation
  `L’essentiel` manquait, 4 titres de rubrique n’étaient pas en capitales et 7 listes
  de mots-clés utilisaient des virgules.
- Après correction du prompt Rendu, une nouvelle conversation a livré 16 154
  caractères sans aucun de ces écarts.
- Un faux rejet intermédiaire avait aussi recompté incorrectement une phrase de 16
  mots comme 26 mots. Le Projet Rendu valide désormais seulement la structure du
  paquet et délègue le contrôle des longueurs au Projet Collecte.

## Contrôles du HTML livré

Contrôles exécutés directement sur le HTML copié depuis l’Assistant :

- 0 marqueur `@@` ;
- 1 seul `h1` ;
- 3 accès rapides ;
- 3 cartes essentielles ;
- 0 `span.fr-tag` ;
- navigation et sections réciproques pour `numerique`, `ia`, `commande` et `bercy` ;
- header, footer, modale et enveloppes de rubrique conformes au canon ;
- footer placé avant la modale ;
- CSS et scripts DSFR 1.15.2 présents ;
- 7 liens externes avec `target="_blank"`, `rel="noopener noreferrer"` et
  l’indication `nouvelle fenêtre` ;
- titres, dates, faits et URL des 4 articles présents ;
- aucun tiret cadratin dans le header ou le footer.

### Comparaison déterministe avec le canon

Le HTML final de l’Assistant et une page de référence construite depuis
`05-BLOCS-HTML-CANONIQUES.md` ont reçu exactement le même paquet éditorial. Le
comparateur a normalisé les deux DOM, puis comparé les balises, les attributs, les
classes, les textes et l’ordre des nœuds.

Résultat final : `DOM_DIFF_COUNT=0`.

La comparaison couvre notamment la navigation `L’essentiel`, les cinq libellés de
rubrique, les séparateurs ` · ` des mots-clés, les cartes, les articles, le footer,
la modale et les dépendances.

### Contrôle visuel au même viewport

Le premier contrôle était insuffisant : il vérifiait la présence des classes et des
dépendances, mais pas le chargement réel de la feuille personnalisée. Le HTML brut
utilisait `/revue-presse-snum/styles.css?v=20260917`, chemin valide seulement après
publication sous ce préfixe.

La boucle de reproduction a ouvert le HTML brut sur un serveur local, sans modifier
son code. Avant correction, `.issue-head` avait un espacement calculé de `0px` et
`.top-grid` utilisait `flex`, ce qui reproduisait le rendu incorrect signalé.

Après remplacement par l’URL publique absolue, le nouveau HTML livré par l’Assistant
a été ouvert de la même manière, sans substitution. À 1 440 × 900 pixels, les valeurs
suivantes sont identiques à celles de la page Bacoco :

- espacement de `.issue-head` : `72px 0px 40px` ;
- affichage de `.top-grid` : `grid` ;
- colonnes de `.top-grid` : `392px 392px 392px` ;
- taille du `h1` : `72px`.

La feuille chargée est
`https://bacoco.github.io/revue-presse-snum/styles.css?v=20260917`.

## Défauts détectés et corrigés

### Préfiltrage pendant COLLECTE

Un premier essai avait produit 11 candidats, puis n’en avait transmis que 6 à la
validation. Le prompt interdit maintenant tout filtrage de date pendant `COLLECTE` et
impose de compter les entrées exactes sous `CANDIDATS` pendant `VALIDATION`.

### Ressource canonique trop longue

Le Projet Rendu voyait plusieurs fragments de la ressource unique sans pouvoir établir
la présence de l’enveloppe complète. Le générateur produit désormais 4 ressources de
moins de 4 500 caractères, avec des marqueurs propres et un ordre d’assemblage explicite.

### Feuille Bacoco relative

Le premier verdict GO était un faux positif structurel. La coque reprenait le chemin
relatif du dépôt publié, mais ce chemin ne fonctionne pas pour un fichier HTML copié
depuis le chat. La source canonique, les ressources générées et le ZIP utilisent
maintenant l’URL publique absolue. Un test de régression refuse le chemin relatif.

### Dérive d’assemblage malgré le bon canon

Le chargement des bons fragments ne garantissait pas encore leur instanciation exacte.
Le prompt Rendu fixe désormais l’ordre de navigation, la casse distincte du libellé de
navigation et du titre de section, ainsi que le séparateur des mots-clés. La recette
réelle suivante est passée de 12 écarts à `DOM_DIFF_COUNT=0`.

### Faux contrôle de longueur dans le Projet Rendu

Le même texte était contrôlé une seconde fois par le Projet Rendu, avec un comptage
erroné. Le contrôle éditorial reste la responsabilité du Projet Collecte ; le Projet
Rendu contrôle seulement le JSON, les champs, les URL, les rubriques, les tableaux de
mots-clés et le nombre d’essentiels.

## Limites de la preuve

- La recette prouve le scénario du 14 octobre 2026, fenêtre du 3 au 13 octobre 2026.
- Les contrôles automatiques et structurels ne remplacent pas un audit RGAA manuel.
- La comparaison des styles calculés couvre le viewport de bureau 1 440 × 900 pixels ;
  les ruptures responsives restent couvertes par les règles CSS Bacoco partagées.
- `DOM_DIFF_COUNT=0` prouve l’identité de structure pour le paquet de recette, pas
  l’identité du contenu éditorial entre deux éditions différentes.
- Aucune publication GitHub Pages et aucun courriel n’ont été exécutés pendant cette
  recette.
