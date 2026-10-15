# Gabarit HTML Loïc - V5.9

<!-- PDG-LARGE-FILE-JUSTIFICATION: la coque, ses modèles et son contrat doivent rester dans un seul document récupérable par le Projet DINUM. -->

Dans l’Assistant DINUM, utiliser `05-BLOCS-HTML-CANONIQUES.md` comme source opérationnelle prioritaire : ses cinq blocs reproduisent ceux-ci à l’identique dans un fichier plus court. Le présent fichier conserve le contrat détaillé et le CSS de référence.

## CONTRAT-DE-SORTIE

Source de vérité : `index.html` et `styles.css` du dépôt `bacoco/revue-presse-snum`, SHA `dc3c87f4f4e7305de0cd9c71da25171252402a83`.

Le bloc `HTML COMPLET` doit être un document unique depuis `<!doctype html>` jusqu’à `</html>`. Copier `GABARIT-COMPLET`, remplacer tous les marqueurs `@@...@@`, puis dupliquer `MODELE-ESSENTIEL` et `MODELE-RUBRIQUE` selon la sélection. Supprimer les commentaires de modèle et tout marqueur restant. Les parties invariantes doivent rester identiques à la source ; seules les dates, la navigation, les sections éditoriales, les textes et les URL d’articles varient.

Conserver sans réécriture le doctype, `lang`, le `title`, les trois accès rapides, le header, le footer, les liens réglementaires, la mention « Accessibilité : non conforme », le modal et les scripts DSFR 1.15.2 `module` et `nomodule`. Conserver exactement `/revue-presse-snum/styles.css?v=20260917`. Un fichier ouvert isolément en local peut donc perdre cette feuille de style : cela ne justifie jamais de modifier le chemin du gabarit.

Les rubriques vides et leurs liens de navigation sont omis. Les identifiants de rubriques sont uniquement `numerique`, `ia`, `commande`, `rh` et `bercy`. Les liens externes d’articles ont `target="_blank"`, `rel="noopener noreferrer"` et la mention masquée « nouvelle fenêtre ». Un tag non interactif utilise toujours `p.fr-tag`.

`@@DATE_EDITION_LONGUE_MAJUSCULES@@` reprend le jour de semaine fourni dans la demande. S’il n’est pas fourni, ne jamais l’inventer : écrire seulement le jour, le mois et l’année. Séparer les mots-clés par ` · ` comme dans la source.

`@@ESSENTIELS@@` vaut une chaîne vide avec moins de trois événements. À partir de trois événements, il contient exactement trois cartes issues des rubriques. `@@A_SURVEILLER@@` vaut une chaîne vide si aucun suivi précis n’est utile.

## GABARIT-COMPLET

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
  <link rel="stylesheet" href="/revue-presse-snum/styles.css?v=20260917">
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

## MODÈLE-ESSENTIEL

Insérer les trois cartes dans une unique section. Les trois événements restent aussi dans leur rubrique : ils ne comptent pas comme des événements supplémentaires.

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

## MODÈLE-RUBRIQUE

Dupliquer la section seulement pour une rubrique non vide. Incrémenter `01`, `02`, etc. Dupliquer uniquement l’élément `article` pour chaque événement de cette rubrique.

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

Pour une rubrique alternée, `@@SECTION_MUTED_ATTR@@` vaut ` class="section-muted"` ; sinon il vaut une chaîne vide. Pour `À surveiller`, utiliser seulement si nécessaire et reprendre exactement cette structure. Dupliquer seulement l’élément `article` pour plusieurs suivis :

```html
<section id="surveiller" class="section-muted"><div class="fr-container section-block"><div class="section-title"><p class="section-number">@@NUMERO@@</p><div><h2>À surveiller</h2></div></div><div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body"><h3>@@TITRE_SUIVI@@</h3><p class="summary">@@SUIVI_COURT@@</p></div></article></div></div></section>
```

Avec zéro événement admissible, remplacer `@@ESSENTIELS@@`, `@@RUBRIQUES@@` et `@@A_SURVEILLER@@` par cette section unique et conserver le reste du gabarit :

```html
<section><div class="fr-container section-block"><div class="section-title"><p class="section-number">01</p><div><h2>Collecte à compléter</h2><p>Aucun événement n’a pu être établi à partir d’une source publique intégrale dans la fenêtre.</p></div></div></div></section>
```

## CSS-DE-RÉFÉRENCE

Ce bloc reproduit exactement `styles.css` au SHA indiqué. Il sert à contrôler les classes et le rendu attendu ; ne pas l’insérer dans le HTML ni le réécrire.

```css
:root { --ink:var(--text-default-grey, #161616); --blue:var(--text-action-high-blue-france, #000091); --pale:var(--background-contrast-blue-france, #ececfe); --line:var(--border-default-grey, #ddd); }
html { scroll-behavior:smooth; }
body { color:var(--ink); background:var(--background-default-grey, #fff); }
.fr-header__body-row { min-height:8rem; }
.fr-header__tools { align-self:center; }
.issue-head { padding:4.5rem 0 2.5rem; background:linear-gradient(115deg,var(--background-contrast-blue-france, #ececfe) 0%,var(--background-default-grey, #fff) 62%); border-bottom:1px solid var(--border-action-low-blue-france, #e3e3fd); }
.eyebrow,.meta { color:var(--text-mention-grey, #666); font-size:.78rem; font-weight:700; letter-spacing:.06em; }
.issue-head h1 { max-width:800px; margin:.5rem 0 1rem; color:var(--blue); font-size:clamp(2.4rem,6vw,4.5rem); line-height:1.02; }
.lead { max-width:780px; font-size:1.25rem; line-height:1.55; }
.topic-nav { display:flex; flex-wrap:wrap; gap:.5rem 1.5rem; margin-top:2rem; padding-top:1.25rem; }
.topic-nav a { font-weight:600; }
.section-block { padding-top:4rem; padding-bottom:4rem; }
.section-muted { background:var(--background-alt-grey, #f6f6f6); }
.section-title { display:grid; grid-template-columns:minmax(3rem,max-content) minmax(0,1fr); gap:1rem; align-items:start; margin-bottom:2rem; }
.section-title h2 { margin:0 0 .5rem; color:var(--blue); }
.section-title p { margin:0; }
.section-number { min-width:3rem; white-space:nowrap; font-size:1.5rem; line-height:2rem; font-weight:700; color:var(--blue); border-top:3px solid var(--blue); padding-top:.5rem; }
.top-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr)); gap:1.5rem; }
.top-grid > .fr-col-12.fr-col-md-4 { width:auto !important; max-width:none !important; min-width:0; flex:none !important; overflow-wrap:anywhere; word-break:break-word; }
.top-card, .article-list article, .article-body { min-width:0; }
.top-card .fr-card__start { order:1; }
.top-card .meta { order:2; }
.top-card .fr-card__title { order:3; }
.top-card .fr-card__desc { order:4; }
.top-card .takeaway { order:5; }
.top-card .impact { order:6; }
.top-card .fr-card__end { order:7; }
.top-card { min-height:28rem; border-top:5px solid var(--blue); overflow-wrap:anywhere; }
.fr-card__end .fr-link { align-self:flex-start; }
.impact { order:3; margin-top:1.5rem; padding-top:1rem; border-top:1px solid var(--border-default-grey, #ddd); }
.article-list { border-top:1px solid var(--border-default-grey, #bbb); }
.article-list article { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,10rem); gap:2rem; align-items:start; padding:2.25rem 0; border-bottom:1px solid var(--border-default-grey, #ccc); }
.article-list h3 { margin:.25rem 0 .5rem; font-size:1.25rem; }
.article-list p { max-width:850px; }
.article-body > p:last-child { margin-bottom:0; }
.takeaway { margin-top:1rem; padding:1rem 1.25rem; background:var(--background-raised-grey, #fff); border-left:4px solid var(--blue); }
.section-muted .takeaway { background:var(--background-contrast-blue-france, #ececfe); }
.snum { color:var(--text-default-grey, #3a3a3a); }
.source-btn { white-space:nowrap; justify-self:end; }
.watch { margin-top:3rem; padding:1.75rem 2rem; background:var(--background-contrast-blue-france, #ececfe); border-left:6px solid var(--blue); }
.watch h2 { margin-top:0; }
.external-note { margin-top:2rem; color:var(--text-mention-grey, #666); font-size:.9rem; }
@media (max-width:48rem) {
  .fr-header__tools { display:none; }
  .issue-head { padding:3rem 0 2rem; }
  .top-card { min-height:auto; }
  .article-list article { grid-template-columns:1fr; gap:1rem; }
  .source-btn { justify-self:start; }
}

/* Accessibilité : la vue mobile évite les colonnes trop étroites sans masquer de données. */
.actions-mobile { display:none; }
@media (max-width:30rem) {
  .legal-page .fr-table { display:none; }
  .legal-page .actions-mobile { display:block; }
  .actions-mobile__list { list-style:none; margin:1rem 0 2rem; padding-left:0; }
  .actions-mobile__item { border-top:1px solid var(--border-default-grey, #ddd); padding:1rem 0; }
  .actions-mobile__item:last-child { border-bottom:1px solid var(--border-default-grey, #ddd); }
  .actions-mobile__item dl { margin:0; }
  .actions-mobile__item dt { margin-top:1rem; font-weight:700; }
  .actions-mobile__item dt:first-child { margin-top:0; }
  .actions-mobile__item dd { margin-left:0; margin-bottom:0; }
}

/* Accessibilité : le focus ne doit jamais être masqué par les styles éditoriaux. */
:focus-visible { outline: 2px solid var(--border-plain-blue-france, #000091); outline-offset: 2px; }
.legal-page { max-width: 52rem; }
.legal-page h2 { margin-top: 2.5rem; }

html, body { max-width:100%; overflow-wrap:break-word; }
```
