# Blocs HTML canoniques - V5.9 Assistant-only

Ce fichier est la source opérationnelle unique du bloc `HTML COMPLET` dans l’Assistant DINUM. Il contient seulement les cinq blocs à copier. Pour l’assemblage HTML, il prime sur toute autre description.

## RÈGLE-DE-COPIE

1. Retrouver dans ce fichier les cinq titres `COQUE`, `ESSENTIEL`, `RUBRIQUE`, `SURVEILLER` et `VIDE`.
2. Copier les blocs littéralement. Remplacer uniquement les marqueurs `@@...@@`.
3. Dans `ESSENTIEL`, dupliquer uniquement la carte `fr-col-12 fr-col-md-4`.
4. Dans `RUBRIQUE`, dupliquer uniquement l’élément `article`.
5. Appliquer exactement les enveloppes suivantes :
   - `numerique` : `<section id="numerique">`
   - `ia` : `<section id="ia" class="section-muted">`
   - `commande` : `<section id="commande">`
   - `rh` : `<section id="rh" class="section-muted">`
   - `bercy` : `<section id="bercy">`
6. Ne jamais reformuler, simplifier, traduire ou réindenter la coque, le header, le footer, le modal, les classes ou les scripts.
7. Chaque source valide figure une fois dans sa rubrique. Une carte essentielle est une mise en avant supplémentaire et ne remplace jamais l’article de rubrique. Avec moins de trois sources valides, ne produire ni section ni lien `L’essentiel`. À partir de trois sources valides, produire exactement trois cartes essentielles.
8. Pour chaque lien `href="#id"` du menu de rubriques, le HTML contient exactement une section `id="id"`. Chaque rubrique produite possède exactement un lien dans ce menu.
9. Avant de livrer, relire le HTML produit et vérifier littéralement : les trois accès rapides, un seul `h1`, le modal `fr-theme-modal`, les deux scripts DSFR 1.15.2, aucun marqueur `@@`, exactement trois cartes essentielles à partir de trois événements et l’enveloppe exacte de chaque rubrique présente.
10. Si un bloc est partiel, refaire une recherche ciblée dans ce fichier par son titre, dans les ressources du Projet et jamais sur le Web. Ne jamais reconstruire la partie manquante de mémoire.
11. Si la seconde passe ne peut pas établir tous les points précédents, ne livrer aucun code HTML : écrire `A_COMPLETER — HTML canonique non établi` sous `HTML COMPLET` et décrire l’écart dans `DOSSIER PRIVÉ`.

## COQUE

```html
<!doctype html>
<html lang="fr" data-fr-scheme="system">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Revue de presse du @@DATE_EDITION@@ - SNUM</title>
  <meta name="description" content="Revue de presse du SNUM du @@DATE_EDITION_LONGUE@@.">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/utility/icons/icons.min.css">
  <link rel="stylesheet" href="https://bacoco.github.io/revue-presse-snum/styles.css?v=20260917">
</head>
<body>
  <div class="fr-skiplinks"><nav class="fr-container" role="navigation" aria-label="Accès rapide"><ul class="fr-skiplinks__list">
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

## ESSENTIEL

```html
<section id="essentiel" class="fr-container section-block">
  <div class="section-title"><p class="section-number">01</p><div><h2>L’essentiel</h2></div></div>
  <div class="top-grid fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-4"><article class="fr-card fr-card--shadow top-card"><div class="fr-card__body"><div class="fr-card__content">
      <div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">@@RUBRIQUE@@</p></li></ul></div>
      <p class="meta">@@SOURCE_MAJUSCULES@@ · @@DATE_PUBLICATION_LONGUE_MAJUSCULES@@</p>
      <h3 class="fr-card__title">@@TITRE@@</h3>
      <p class="fr-card__desc"><span class="summary-text">@@FAIT@@</span><br><strong>Mots-clés :</strong> <span class="keywords">@@MOTS_CLES@@</span></p>
      <p class="takeaway"><strong>À retenir :</strong> @@A_RETENIR@@</p>
      <p class="impact"><strong>Intérêt pour le SNUM :</strong> @@INTERET_SNUM@@</p>
      <div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="@@URL@@" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : @@TITRE@@ - nouvelle fenêtre</span></a></div>
    </div></div></article></div>
  </div>
</section>
```

## RUBRIQUE

```html
<section id="@@ID_RUBRIQUE@@"@@SECTION_MUTED_ATTR@@><div class="fr-container section-block">
  <div class="section-title"><p class="section-number">@@NUMERO@@</p><div><h2>@@TITRE_RUBRIQUE@@</h2></div></div>
  <div class="article-list fr-grid-row">
    <article class="fr-col-12">
      <div class="article-body"><p class="meta">@@SOURCE_MAJUSCULES@@ · @@DATE_PUBLICATION_LONGUE_MAJUSCULES@@</p><h3>@@TITRE@@</h3>
        <p class="summary"><span class="summary-text">@@FAIT@@</span><br><strong>Mots-clés :</strong> <span class="keywords">@@MOTS_CLES@@</span></p>
        <p class="takeaway"><strong>À retenir :</strong> @@A_RETENIR@@</p>
        <p class="snum"><strong>Intérêt pour le SNUM :</strong> @@INTERET_SNUM@@</p>
      </div>
      <a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="@@URL@@" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : @@TITRE@@ - nouvelle fenêtre</span></a>
    </article>
  </div>
</div></section>
```

## SURVEILLER

```html
<section id="surveiller" class="section-muted"><div class="fr-container section-block"><div class="section-title"><p class="section-number">@@NUMERO@@</p><div><h2>À surveiller</h2></div></div><div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body"><h3>@@TITRE_SUIVI@@</h3><p class="summary">@@SUIVI_COURT@@</p></div></article></div></div></section>
```

## VIDE

```html
<section><div class="fr-container section-block"><div class="section-title"><p class="section-number">01</p><div><h2>Collecte à compléter</h2><p>Aucun événement n’a pu être établi à partir d’une source publique intégrale dans la fenêtre.</p></div></div></div></section>
```
