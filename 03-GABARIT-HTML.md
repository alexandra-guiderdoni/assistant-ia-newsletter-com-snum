# Gabarit HTML Loïc - V5.7

<!-- PDG-LARGE-FILE-JUSTIFICATION: la coque, ses modèles et son contrat doivent rester dans un seul document récupérable par le Projet DINUM. -->

## CONTRAT-DE-SORTIE

Le bloc `HTML COMPLET` doit être un document unique depuis `<!doctype html>` jusqu’à `</html>`. Copier `GABARIT-COMPLET`, remplacer tous les marqueurs `@@...@@`, puis dupliquer `MODELE-ESSENTIEL` et `MODELE-RUBRIQUE` selon la sélection. Supprimer les commentaires de modèle et tout marqueur restant.

Conserver sans réécriture le doctype, `lang`, le `title`, les trois accès rapides, le header, le footer, les liens réglementaires, la mention « Accessibilité : non conforme », le modal et les scripts DSFR 1.15.2 `module` et `nomodule`. Conserver la feuille de style absolue : elle permet aussi l’aperçu local du fichier isolé.

Les rubriques vides et leurs liens de navigation sont omis. Les identifiants de rubriques sont uniquement `numerique`, `ia`, `commande`, `rh` et `bercy`. Les liens externes d’articles ont `target="_blank"`, `rel="noopener noreferrer"` et la mention masquée « nouvelle fenêtre ». Un tag non interactif utilise toujours `p.fr-tag`.

`@@ESSENTIELS@@` vaut une chaîne vide avec moins de trois événements. À partir de trois événements, il contient exactement trois cartes issues des rubriques. `@@A_SURVEILLER@@` vaut une chaîne vide si aucun suivi précis n’est utile.

## GABARIT-COMPLET

```html
<!doctype html>
<html lang="fr" data-fr-scheme="system">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Revue de presse du @@DATE_EDITION@@ - SNUM</title>
  <meta name="description" content="Revue de presse du SNUM du @@DATE_EDITION_LONGUE@@.">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/utility/icons/icons.min.css">
  <link rel="stylesheet" href="https://bacoco.github.io/revue-presse-snum/styles.css?v=20260917">
</head>
<body>
  <div class="fr-skiplinks"><nav class="fr-container" aria-label="Accès rapide"><ul class="fr-skiplinks__list">
    <li><a class="fr-link" href="#main">Accéder au contenu</a></li>
    <li><a class="fr-link" href="#navigation">Accéder au menu des rubriques</a></li>
    <li><a class="fr-link" href="#footer">Accéder au pied de page</a></li>
  </ul></nav></div>
  <header class="fr-header" role="banner"><div class="fr-header__body"><div class="fr-container"><div class="fr-header__body-row">
    <div class="fr-header__brand fr-enlarge-link"><div class="fr-header__brand-top"><div class="fr-header__logo"><p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p></div></div>
      <div class="fr-header__service"><a href="/revue-presse-snum/" title="Accueil - Revue de presse du SNUM"><p class="fr-header__service-title">Service du numérique</p></a><p class="fr-header__service-tagline">Secrétariat général - Revue de presse</p></div>
    </div>
  </div></div></div></header>
  <main id="main">
    <section class="issue-head"><div class="fr-container">
      <p class="eyebrow">ÉDITION DU @@DATE_EDITION_LONGUE_MAJUSCULES@@</p>
      <h1>Revue de presse du SNUM</h1>
      <p class="lead">Période : @@DATE_DEBUT_COLLECTE@@ - @@DATE_FIN_COLLECTE@@.</p>
      <nav id="navigation" class="topic-nav" aria-label="Rubriques">@@NAVIGATION@@<a class="fr-link" href="/revue-presse-snum/editions/">Archives</a></nav>
    </div></section>
    @@ESSENTIELS@@
    @@RUBRIQUES@@
    @@A_SURVEILLER@@
  </main>
  <footer id="footer" class="fr-footer" role="contentinfo"><div class="fr-container">
    <div class="fr-footer__body"><div class="fr-footer__brand fr-enlarge-link"><a href="/revue-presse-snum/" title="Accueil - Revue de presse du SNUM"><p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p></a></div>
      <div class="fr-footer__content"><p class="fr-footer__content-desc">Équipe Communication / Événementiel du SNUM - Bureau aide à la gouvernance et fonctions support.</p></div>
    </div>
    <div class="fr-footer__bottom"><ul class="fr-footer__bottom-list">
      <li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/accessibilite/">Accessibilité : non conforme</a></li>
      <li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/mentions-legales/#donnees-personnelles">Données personnelles</a></li>
      <li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/mentions-legales/#cookies">Gestion des cookies</a></li>
      <li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/mentions-legales/">Mentions légales</a></li>
      <li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/plan-du-site/">Plan du site</a></li>
      <li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/editions/">Archives</a></li>
      <li class="fr-footer__bottom-item"><button type="button" class="fr-footer__bottom-link fr-btn fr-btn--tertiary-no-outline fr-btn--display" aria-controls="fr-theme-modal" data-fr-opened="false">Paramètres d’affichage</button></li>
    </ul><div class="fr-footer__bottom-copy"><p>Sélection éditoriale établie à partir de sources publiques. Les droits des articles appartiennent à leurs éditeurs.</p></div></div>
  </div></footer>
  <dialog id="fr-theme-modal" class="fr-modal" aria-labelledby="fr-theme-modal-title"><div class="fr-container fr-container--fluid fr-container-md"><div class="fr-grid-row fr-grid-row--center"><div class="fr-col-12 fr-col-md-6 fr-col-lg-4"><div class="fr-modal__body">
    <div class="fr-modal__header"><button aria-controls="fr-theme-modal" title="Fermer" type="button" class="fr-btn--close fr-btn">Fermer</button></div>
    <div class="fr-modal__content"><h2 id="fr-theme-modal-title" class="fr-modal__title">Paramètres d’affichage</h2><div id="fr-display" class="fr-display"><fieldset class="fr-fieldset" id="display-fieldset"><legend class="fr-fieldset__legend fr-fieldset__legend--regular" id="display-fieldset-legend">Choisissez un thème pour personnaliser l’apparence du site.</legend>
      <div class="fr-fieldset__element"><div class="fr-radio-group"><input value="light" type="radio" id="fr-radios-theme-light" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-light">Thème clair</label></div></div>
      <div class="fr-fieldset__element"><div class="fr-radio-group"><input value="dark" type="radio" id="fr-radios-theme-dark" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-dark">Thème sombre</label></div></div>
      <div class="fr-fieldset__element"><div class="fr-radio-group"><input value="system" type="radio" id="fr-radios-theme-system" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-system">Système</label></div></div>
    </fieldset></div></div>
  </div></div></div></div></dialog>
  <script type="module" src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.module.min.js"></script>
  <script nomodule src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.nomodule.min.js"></script>
</body>
</html>
```

## MODÈLE-ESSENTIEL

Insérer les trois cartes dans une unique section. Les trois événements restent aussi dans leur rubrique : ils ne comptent pas comme des événements supplémentaires.

```html
<section id="essentiel" class="section-block"><div class="fr-container">
  <div class="section-title"><p class="section-number">00</p><div><h2>L’essentiel</h2></div></div>
  <div class="fr-grid-row top-grid">
    <div class="fr-col-12 fr-col-md-4"><article class="fr-card fr-card--shadow top-card"><div class="fr-card__body"><div class="fr-card__content">
      <div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">@@RUBRIQUE@@</p></li></ul></div>
      <p class="meta">@@SOURCE_MAJUSCULES@@ · @@DATE_PUBLICATION_LONGUE_MAJUSCULES@@</p>
      <h3 class="fr-card__title">@@TITRE@@</h3>
      <p class="fr-card__desc">@@FAIT@@<br><strong>Mots-clés :</strong> @@MOTS_CLES@@</p>
      <p class="takeaway"><strong>À retenir :</strong> @@A_RETENIR@@</p>
      <p class="impact"><strong>Intérêt pour le SNUM :</strong> @@INTERET_SNUM@@</p>
      <div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="@@URL@@" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : @@TITRE@@ - nouvelle fenêtre</span></a></div>
    </div></div></article></div>
  </div>
</div></section>
```

## MODÈLE-RUBRIQUE

Dupliquer la section seulement pour une rubrique non vide. Incrémenter `01`, `02`, etc. Dupliquer uniquement l’élément `article` pour chaque événement de cette rubrique.

```html
<section id="@@ID_RUBRIQUE@@" class="section-block @@SECTION_MUTED_SI_ALTERNEE@@"><div class="fr-container">
  <div class="section-title"><p class="section-number">@@NUMERO@@</p><div><h2>@@TITRE_RUBRIQUE@@</h2></div></div>
  <div class="article-list fr-grid-row">
    <article class="fr-col-12">
      <div class="article-body"><p class="meta">@@SOURCE_MAJUSCULES@@ · @@DATE_PUBLICATION_LONGUE_MAJUSCULES@@</p><h3>@@TITRE@@</h3>
        <p class="summary">@@FAIT@@<br><strong>Mots-clés :</strong> @@MOTS_CLES@@</p>
        <p class="takeaway"><strong>À retenir :</strong> @@A_RETENIR@@</p>
        <p class="snum"><strong>Intérêt pour le SNUM :</strong> @@INTERET_SNUM@@</p>
      </div>
      <a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="@@URL@@" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : @@TITRE@@ - nouvelle fenêtre</span></a>
    </article>
  </div>
</div></section>
```

Pour `À surveiller`, utiliser seulement si nécessaire :

```html
<section class="section-block"><div class="fr-container"><div class="watch"><h2>À surveiller</h2><ul><li>@@SUIVI_COURT@@</li></ul></div></div></section>
```

Avec zéro événement admissible, remplacer `@@ESSENTIELS@@`, `@@RUBRIQUES@@` et `@@A_SURVEILLER@@` par cette section unique et conserver le reste du gabarit :

```html
<section class="section-block"><div class="fr-container"><div class="section-title"><p class="section-number">00</p><div><h2>Collecte à compléter</h2><p>Aucun événement n’a pu être établi à partir d’une source publique intégrale dans la fenêtre.</p></div></div></div></section>
```
