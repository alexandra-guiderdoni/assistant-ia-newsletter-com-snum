# Gabarit vide SNUM - code de référence V5.2

## Utilisation

Ce document ne contient aucune newsletter préremplie. DINUM y insère uniquement sa sélection admissible et ses synthèses. Remplir les trois essentiels puis dupliquer le modèle d’article pour tous les événements de leur rubrique ; les essentiels sont également repris en rubrique. Le nombre de modèles visibles ne fixe aucun maximum de sujets. Supprimer les rubriques vides et leurs liens de menu. Supprimer À surveiller si aucun suivi concret. Remplacer tous les placeholders et href vides ; retirer data-url-a-remplir. Ne pas remplacer le gabarit par un HTML simplifié.

Conserver header, footer, classes, styles, trois skiplinks, nav navigation et scripts DSFR. Seuls les textes d’édition et les articles changent. Garder les numéros de sections comme repères du gabarit ; ce ne sont pas des comptes d’articles. Ne pas mettre de sous-titre de comptage sous les rubriques ni de volume près du titre. Échapper les textes et URL HTML.

Les chemins absolus /revue-presse-snum/ conviennent à l’accueil et à l’édition figée sur ce site. Le CSS réel est /revue-presse-snum/styles.css ; aucune ressource assets/css/styles.css ou assets/js/scripts.js à inventer. Un fichier HTML ouvert seul localement peut ne pas charger ce chemin ; ne pas confondre avec un défaut du code pour GitHub Pages. Pour chaque nouvelle édition, le code rempli doit être contrôlé ; le modèle ne constitue pas une validation de son contenu futur.

Source du modèle : captures du dépôt bacoco/revue-presse-snum au SHA dc3c87f4f4e7305de0cd9c71da25171252402a83, datées du 13 octobre. Header/footer identiques après normalisation, CSS inchangé ; Nu local sans erreur pour ce modèle avec placeholders. Ce contrôle ne porte pas sur la future édition, ni sur l’accessibilité complète. Pour publier les archives, recouper la capture ci-dessous avec la liste actuelle et préserver toute entrée plus récente.

## A - HTML vide à remplir

~~~~html
<!doctype html>
<html lang="fr" data-fr-scheme="system">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Revue de presse du {{DATE_EDITION}} - SNUM</title>
<meta name="description" content="Revue de presse du SNUM du {{DATE_EDITION}}.">
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
<header class="fr-header" role="banner"><div class="fr-header__body"><div class="fr-container"><div class="fr-header__body-row"><div class="fr-header__brand fr-enlarge-link">
<div class="fr-header__brand-top"><div class="fr-header__logo"><p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p></div></div>
<div class="fr-header__service">
<a href="/revue-presse-snum/" title="Accueil - Revue de presse du SNUM"><p class="fr-header__service-title">Service du numérique</p></a><p class="fr-header__service-tagline">Secrétariat général - Revue de presse</p>
</div>
</div></div></div></div></header><main id="main"><section class="issue-head"><div class="fr-container">
<p class="eyebrow">ÉDITION DU {{DATE_EDITION}}</p>
<h1>Revue de presse du SNUM</h1>
<nav id="navigation" class="topic-nav" aria-label="Rubriques"><a class="fr-link" href="#essentiel">L’essentiel</a><a class="fr-link" href="#numerique">Numérique</a><a class="fr-link" href="#ia">Intelligence artificielle</a><a class="fr-link" href="#commande">Commande publique</a><a class="fr-link" href="#rh">Ressources humaines</a><a class="fr-link" href="#bercy">Vie de Bercy</a><a class="fr-link" href="#surveiller">À surveiller</a><a class="fr-link" href="/revue-presse-snum/editions/">Archives</a></nav><p class="fr-mt-2w">Période : {{DEBUT_COLLECTE}} - {{FIN_COLLECTE}}.</p>
</div></section><section id="essentiel" class="fr-container section-block"><div class="section-title">
<p class="section-number">01</p>
<div><h2>L’essentiel</h2></div>
</div>
<div class="top-grid fr-grid-row fr-grid-row--gutters">
<div class="fr-col-12 fr-col-md-4"><article class="fr-card fr-card--shadow top-card"><div class="fr-card__body"><div class="fr-card__content">
<div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{{ESSENTIEL_1_RUBRIQUE}}</p></li></ul></div>
<p class="meta">{{ESSENTIEL_1_SOURCE}} · {{ESSENTIEL_1_DATE_PUBLICATION}}</p>
<h3 class="fr-card__title">{{ESSENTIEL_1_TITRE}}</h3>
<p class="fr-card__desc"><span class="summary-text">{{ESSENTIEL_1_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ESSENTIEL_1_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ESSENTIEL_1_A_RETENIR}}</p>
<p class="impact"><strong>Intérêt pour le SNUM :</strong> {{ESSENTIEL_1_INTERET_SNUM}}</p>
<div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ESSENTIEL_1_URL">Lire la source<span class="fr-sr-only"> : {{ESSENTIEL_1_TITRE}} - nouvelle fenêtre</span></a></div>
</div></div></article></div>
<div class="fr-col-12 fr-col-md-4"><article class="fr-card fr-card--shadow top-card"><div class="fr-card__body"><div class="fr-card__content">
<div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{{ESSENTIEL_2_RUBRIQUE}}</p></li></ul></div>
<p class="meta">{{ESSENTIEL_2_SOURCE}} · {{ESSENTIEL_2_DATE_PUBLICATION}}</p>
<h3 class="fr-card__title">{{ESSENTIEL_2_TITRE}}</h3>
<p class="fr-card__desc"><span class="summary-text">{{ESSENTIEL_2_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ESSENTIEL_2_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ESSENTIEL_2_A_RETENIR}}</p>
<p class="impact"><strong>Intérêt pour le SNUM :</strong> {{ESSENTIEL_2_INTERET_SNUM}}</p>
<div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ESSENTIEL_2_URL">Lire la source<span class="fr-sr-only"> : {{ESSENTIEL_2_TITRE}} - nouvelle fenêtre</span></a></div>
</div></div></article></div>
<div class="fr-col-12 fr-col-md-4"><article class="fr-card fr-card--shadow top-card"><div class="fr-card__body"><div class="fr-card__content">
<div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{{ESSENTIEL_3_RUBRIQUE}}</p></li></ul></div>
<p class="meta">{{ESSENTIEL_3_SOURCE}} · {{ESSENTIEL_3_DATE_PUBLICATION}}</p>
<h3 class="fr-card__title">{{ESSENTIEL_3_TITRE}}</h3>
<p class="fr-card__desc"><span class="summary-text">{{ESSENTIEL_3_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ESSENTIEL_3_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ESSENTIEL_3_A_RETENIR}}</p>
<p class="impact"><strong>Intérêt pour le SNUM :</strong> {{ESSENTIEL_3_INTERET_SNUM}}</p>
<div class="fr-card__end"><div>
<a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ESSENTIEL_3_URL">Lire la source<span class="fr-sr-only"> : {{ESSENTIEL_3_TITRE}} - nouvelle fenêtre</span></a><p><a class="fr-link" href="https://www.info.gouv.fr/conseil-des-ministres/compte-rendu-du-conseil-des-ministres-du-01-10-2026" target="_blank" rel="noopener noreferrer">Source officielle<span class="fr-sr-only"> : budget 2027 - nouvelle fenêtre</span></a></p>
</div></div>
</div></div></article></div>
</div></section><section id="numerique"><div class="fr-container section-block">
<div class="section-title">
<p class="section-number">02</p>
<div><h2>NUMERIQUE</h2></div>
</div>
<div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body">
<p class="meta">{{ARTICLE_NUMERIQUE_SOURCE}} · {{ARTICLE_NUMERIQUE_DATE_PUBLICATION}}</p>
<h3>{{ARTICLE_NUMERIQUE_TITRE}}</h3>
<p class="summary"><span class="summary-text">{{ARTICLE_NUMERIQUE_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ARTICLE_NUMERIQUE_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ARTICLE_NUMERIQUE_A_RETENIR}}</p>
<p class="snum"><strong>Intérêt pour le SNUM :</strong> {{ARTICLE_NUMERIQUE_INTERET_SNUM}}</p>
</div>
<a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ARTICLE_NUMERIQUE_URL">Lire la source<span class="fr-sr-only"> : {{ARTICLE_NUMERIQUE_TITRE}} - nouvelle fenêtre</span></a></article></div>
</div></section><section id="ia" class="section-muted"><div class="fr-container section-block">
<div class="section-title">
<p class="section-number">03</p>
<div><h2>INTELLIGENCE ARTIFICIELLE (IA)</h2></div>
</div>
<div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body">
<p class="meta">{{ARTICLE_IA_SOURCE}} · {{ARTICLE_IA_DATE_PUBLICATION}}</p>
<h3>{{ARTICLE_IA_TITRE}}</h3>
<p class="summary"><span class="summary-text">{{ARTICLE_IA_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ARTICLE_IA_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ARTICLE_IA_A_RETENIR}}</p>
<p class="snum"><strong>Intérêt pour le SNUM :</strong> {{ARTICLE_IA_INTERET_SNUM}}</p>
</div>
<a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ARTICLE_IA_URL">Lire la source<span class="fr-sr-only"> : {{ARTICLE_IA_TITRE}} - nouvelle fenêtre</span></a></article></div>
</div></section><section id="commande"><div class="fr-container section-block">
<div class="section-title">
<p class="section-number">04</p>
<div><h2>COMMANDE PUBLIQUE</h2></div>
</div>
<div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body">
<p class="meta">{{ARTICLE_COMMANDE_SOURCE}} · {{ARTICLE_COMMANDE_DATE_PUBLICATION}}</p>
<h3>{{ARTICLE_COMMANDE_TITRE}}</h3>
<p class="summary"><span class="summary-text">{{ARTICLE_COMMANDE_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ARTICLE_COMMANDE_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ARTICLE_COMMANDE_A_RETENIR}}</p>
<p class="snum"><strong>Intérêt pour le SNUM :</strong> {{ARTICLE_COMMANDE_INTERET_SNUM}}</p>
</div>
<a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ARTICLE_COMMANDE_URL">Lire la source<span class="fr-sr-only"> : {{ARTICLE_COMMANDE_TITRE}} - nouvelle fenêtre</span></a></article></div>
</div></section><section id="rh" class="section-muted"><div class="fr-container section-block">
<div class="section-title">
<p class="section-number">05</p>
<div><h2>RESSOURCES HUMAINES</h2></div>
</div>
<div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body">
<p class="meta">{{ARTICLE_RH_SOURCE}} · {{ARTICLE_RH_DATE_PUBLICATION}}</p>
<h3>{{ARTICLE_RH_TITRE}}</h3>
<p class="summary"><span class="summary-text">{{ARTICLE_RH_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ARTICLE_RH_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ARTICLE_RH_A_RETENIR}}</p>
<p class="snum"><strong>Intérêt pour le SNUM :</strong> {{ARTICLE_RH_INTERET_SNUM}}</p>
</div>
<a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ARTICLE_RH_URL">Lire la source<span class="fr-sr-only"> : {{ARTICLE_RH_TITRE}} - nouvelle fenêtre</span></a></article></div>
</div></section><section id="bercy"><div class="fr-container section-block">
<div class="section-title">
<p class="section-number">06</p>
<div><h2>VIE DE BERCY</h2></div>
</div>
<div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body">
<p class="meta">{{ARTICLE_BERCY_SOURCE}} · {{ARTICLE_BERCY_DATE_PUBLICATION}}</p>
<h3>{{ARTICLE_BERCY_TITRE}}</h3>
<p class="summary"><span class="summary-text">{{ARTICLE_BERCY_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ARTICLE_BERCY_MOTS_CLES}}</span></p>
<p class="takeaway"><strong>À retenir :</strong> {{ARTICLE_BERCY_A_RETENIR}}</p>
<p class="snum"><strong>Intérêt pour le SNUM :</strong> {{ARTICLE_BERCY_INTERET_SNUM}}</p>
</div>
<a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="" target="_blank" rel="noopener noreferrer" data-url-a-remplir="ARTICLE_BERCY_URL">Lire la source<span class="fr-sr-only"> : {{ARTICLE_BERCY_TITRE}} - nouvelle fenêtre</span></a></article></div>
</div></section><section id="surveiller" class="section-muted"><div class="fr-container section-block">
<div class="section-title">
<p class="section-number">07</p>
<div><h2>À surveiller</h2></div>
</div>
<div class="article-list fr-grid-row">
<article class="fr-col-12"><div class="article-body">
<h3>{{SUIVI_1_TITRE}}</h3>
<p class="summary">{{SUIVI_1_ACTION}}</p>
</div></article><article class="fr-col-12"><div class="article-body">
<h3>{{SUIVI_2_TITRE}}</h3>
<p class="summary">{{SUIVI_2_ACTION}}</p>
</div></article><article class="fr-col-12"><div class="article-body">
<h3>{{SUIVI_3_TITRE}}</h3>
<p class="summary">{{SUIVI_3_ACTION}}</p>
</div></article>
</div>
</div></section></main><footer id="footer" class="fr-footer" role="contentinfo"><div class="fr-container">
<div class="fr-footer__body">
<div class="fr-footer__brand fr-enlarge-link"><a href="/revue-presse-snum/" title="Accueil - Revue de presse du SNUM"><p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p></a></div>
<div class="fr-footer__content"><p class="fr-footer__content-desc">Équipe Communication / Événementiel du SNUM - Bureau aide à la gouvernance et fonctions support.</p></div>
</div>
<div class="fr-footer__bottom">
<ul class="fr-footer__bottom-list">
<li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/accessibilite/">Accessibilité : non conforme</a></li>
<li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/mentions-legales/#donnees-personnelles">Données personnelles</a></li>
<li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/mentions-legales/#cookies">Gestion des cookies</a></li>
<li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/mentions-legales/">Mentions légales</a></li>
<li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/plan-du-site/">Plan du site</a></li>
<li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="/revue-presse-snum/editions/">Archives</a></li>
<li class="fr-footer__bottom-item"><button type="button" class="fr-footer__bottom-link fr-btn fr-btn--tertiary-no-outline fr-btn--display" aria-controls="fr-theme-modal" data-fr-opened="false">Paramètres d’affichage</button></li>
</ul>
<div class="fr-footer__bottom-copy"><p>Sélection éditoriale établie à partir de sources publiques. Les droits des articles appartiennent à leurs éditeurs.</p></div>
</div>
</div></footer><dialog id="fr-theme-modal" class="fr-modal" aria-labelledby="fr-theme-modal-title"><div class="fr-container fr-container--fluid fr-container-md"><div class="fr-grid-row fr-grid-row--center"><div class="fr-col-12 fr-col-md-6 fr-col-lg-4"><div class="fr-modal__body">
<div class="fr-modal__header"><button aria-controls="fr-theme-modal" title="Fermer" type="button" class="fr-btn--close fr-btn">Fermer</button></div>
<div class="fr-modal__content">
<h2 id="fr-theme-modal-title" class="fr-modal__title">Paramètres d’affichage</h2>
<div id="fr-display" class="fr-display"><fieldset class="fr-fieldset" id="display-fieldset">
<legend class="fr-fieldset__legend fr-fieldset__legend--regular" id="display-fieldset-legend">Choisissez un thème pour personnaliser l’apparence du site.</legend>
<div class="fr-fieldset__element"><div class="fr-radio-group">
<input value="light" type="radio" id="fr-radios-theme-light" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-light">Thème clair</label>
</div></div>
<div class="fr-fieldset__element"><div class="fr-radio-group">
<input value="dark" type="radio" id="fr-radios-theme-dark" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-dark">Thème sombre</label>
</div></div>
<div class="fr-fieldset__element"><div class="fr-radio-group">
<input value="system" type="radio" id="fr-radios-theme-system" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-system">Système</label>
</div></div>
</fieldset></div>
</div>
</div></div></div></div></dialog><script type="module" src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.module.min.js"></script><script nomodule src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.nomodule.min.js"></script>
</body>
</html>

~~~~

## B - CSS de Loïc à conserver

~~~~css
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

~~~~

## C - Archives capturées, à actualiser avant publication

~~~~html
<!doctype html><html lang="fr" data-fr-scheme="system"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Archives - Revue de presse du SNUM</title><meta name="description" content="Archives des éditions de la revue de presse du SNUM."><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.min.css"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/utility/icons/icons.min.css"><link rel="stylesheet" href="../styles.css?v=20260917"></head><body><div class="fr-skiplinks"><nav class="fr-container" role="navigation" aria-label="Accès rapide"><ul class="fr-skiplinks__list"><li><a class="fr-link" href="#main">Accéder au contenu</a></li><li><a class="fr-link" href="#footer">Accéder au pied de page</a></li></ul></nav></div><header class="fr-header" role="banner"><div class="fr-header__body"><div class="fr-container"><div class="fr-header__body-row"><div class="fr-header__brand fr-enlarge-link"><div class="fr-header__brand-top"><div class="fr-header__logo"><p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p></div></div><div class="fr-header__service"><a href="../" title="Accueil - Revue de presse du SNUM"><p class="fr-header__service-title">Service du numérique</p></a><p class="fr-header__service-tagline">Secrétariat général - Revue de presse</p></div></div></div></div></div></header><main id="main"><section class="issue-head"><div class="fr-container"><p class="eyebrow">REVUE DE PRESSE DU SNUM</p><h1>Archives</h1><p class="lead">Toutes les éditions restent accessibles et sont conservées dans le dépôt GitHub.</p><p><a class="fr-link fr-icon-arrow-left-line fr-link--icon-left" href="../">Revenir à la dernière édition</a></p></div></section><section class="fr-container section-block"><div class="section-title"><p class="section-number">2026</p><div><h2>Éditions publiées</h2></div></div><div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body"><p class="meta">VENDREDI 2 OCTOBRE 2026</p><h3>Sécurité de la DGFiP, réorganisation numérique et budget 2027</h3><p>Rapport ANSSI, future DITSP, services publics numériques, gouvernance IA, formation et arbitrages budgétaires.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-10-02/">Consulter<span class="fr-sr-only"> l’édition du vendredi 2 octobre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">VENDREDI 25 SEPTEMBRE 2026</p><h3>Mutualisation de l’IA publique, résilience cloud et compétences</h3><p>Gouvernance IA, transformation numérique, cloud, RAG, commande publique, compétences et transmission à Bercy.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-25/">Consulter<span class="fr-sr-only"> l’édition du vendredi 25 septembre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">MARDI 22 SEPTEMBRE 2026</p><h3>Réinternalisation numérique, IA souveraine et agents offensifs</h3><p>Recrutements numériques de l’État, IA de la Cour des comptes, agents autonomes, centres de données, observabilité, emplois et services fiscaux.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-22/">Consulter<span class="fr-sr-only"> l’édition du mardi 22 septembre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">VENDREDI 18 SEPTEMBRE 2026</p><h3>Dépendances cloud, données pour agents IA et vie privée</h3><p>VMware, UN System Data Commons, lunettes connectées, cybersécurité, infrastructures et égalité professionnelle.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-18/">Consulter<span class="fr-sr-only"> l’édition du vendredi 18 septembre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">JEUDI 17 SEPTEMBRE 2026 - VERSION RÉVISÉE</p><h3>Commande publique numérique, souveraineté opérationnelle et IA agentique</h3><p>Une phrase courte et des mots-clés par sujet.</p><p><a class="fr-link" href="./2026-09-17/">Consulter la version initiale du 17 septembre 2026</a></p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-17/revision-1/">Consulter<span class="fr-sr-only"> la version révisée du jeudi 17 septembre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">MARDI 15 SEPTEMBRE 2026 · 13 ARTICLES · 6 SOURCES</p><h3>Cybersécurité interministérielle, souveraineté de l’IA et maîtrise des usages</h3><p>Réactiv et ANSSI, offre Numspot-Mistral, shadow AI, sécurité des agents IA, transformation des services publics, inclusion numérique et RH.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-15/">Consulter<span class="fr-sr-only"> l’édition du mardi 15 septembre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">VENDREDI 11 SEPTEMBRE 2026 · 11 ARTICLES · 3 SOURCES</p><h3>IA offensive, souveraineté industrielle et infrastructures critiques</h3><p>Usages malveillants des agents IA, financement de Mistral AI, évaluation européenne des modèles et dépendances énergétiques du calcul.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-11/">Consulter<span class="fr-sr-only"> l’édition du vendredi 11 septembre 2026</span></a></article><article class="fr-col-12"><div class="article-body"><p class="meta">MARDI 8 SEPTEMBRE 2026 · 10 ARTICLES · 6 SOURCES</p><h3>Intelligence artificielle, cybersécurité et souveraineté numérique</h3><p>Cloud européen, pression cyber sur la DGFiP et agents IA parmi les priorités industrielles européennes.</p></div><a class="fr-btn fr-btn--secondary source-btn" href="./2026-09-08/">Consulter<span class="fr-sr-only"> l’édition du mardi 8 septembre 2026</span></a></article></div></section></main><footer id="footer" class="fr-footer" role="contentinfo"><div class="fr-container"><div class="fr-footer__body"><div class="fr-footer__brand fr-enlarge-link"><a href="../" title="Accueil - Revue de presse du SNUM"><p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p></a></div><div class="fr-footer__content"><p class="fr-footer__content-desc">Équipe Communication / Événementiel du SNUM - Bureau aide à la gouvernance et fonctions support.</p></div></div><div class="fr-footer__bottom"><ul class="fr-footer__bottom-list"><li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="../accessibilite/">Accessibilité : non conforme</a></li><li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="../mentions-legales/#donnees-personnelles">Données personnelles</a></li><li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="../mentions-legales/#cookies">Gestion des cookies</a></li><li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="../mentions-legales/">Mentions légales</a></li><li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="../plan-du-site/">Plan du site</a></li><li class="fr-footer__bottom-item"><a class="fr-footer__bottom-link" href="../editions/">Archives</a></li><li class="fr-footer__bottom-item"><button type="button" class="fr-footer__bottom-link fr-btn fr-btn--tertiary-no-outline fr-btn--display" aria-controls="fr-theme-modal" data-fr-opened="false">Paramètres d’affichage</button></li></ul><div class="fr-footer__bottom-copy"><p>Sélection éditoriale établie à partir de sources publiques. Les droits des articles appartiennent à leurs éditeurs.</p></div></div></div></footer><dialog id="fr-theme-modal" class="fr-modal" aria-labelledby="fr-theme-modal-title"><div class="fr-container fr-container--fluid fr-container-md"><div class="fr-grid-row fr-grid-row--center"><div class="fr-col-12 fr-col-md-6 fr-col-lg-4"><div class="fr-modal__body"><div class="fr-modal__header"><button aria-controls="fr-theme-modal" title="Fermer" type="button" class="fr-btn--close fr-btn">Fermer</button></div><div class="fr-modal__content"><h2 id="fr-theme-modal-title" class="fr-modal__title">Paramètres d’affichage</h2><div id="fr-display" class="fr-display"><fieldset class="fr-fieldset" id="display-fieldset"><legend class="fr-fieldset__legend fr-fieldset__legend--regular" id="display-fieldset-legend">Choisissez un thème pour personnaliser l’apparence du site.</legend><div class="fr-fieldset__element"><div class="fr-radio-group"><input value="light" type="radio" id="fr-radios-theme-light" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-light">Thème clair</label></div></div><div class="fr-fieldset__element"><div class="fr-radio-group"><input value="dark" type="radio" id="fr-radios-theme-dark" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-dark">Thème sombre</label></div></div><div class="fr-fieldset__element"><div class="fr-radio-group"><input value="system" type="radio" id="fr-radios-theme-system" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-system">Système</label></div></div></fieldset></div></div></div></div></div></div></dialog><script type="module" src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.module.min.js"></script><script nomodule src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.nomodule.min.js"></script></body></html>
~~~~
