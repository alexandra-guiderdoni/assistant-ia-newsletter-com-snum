# Gabarit HTML vide SNUM - V5.3.1

## Source et usage

Source technique figée : dépôt `bacoco/revue-presse-snum`, révision `dc3c87f4f4e7305de0cd9c71da25171252402a83`. Le header, le footer, les classes, les scripts DSFR 1.15.2 et le CSS ci-dessous proviennent de cette révision.

Ce document sert uniquement après la sélection et la rédaction de la revue. Il ne contient aucune actualité à recopier. Les valeurs entre doubles accolades sont des emplacements, jamais du contenu publiable.

La page conserve le lien public vers `/revue-presse-snum/styles.css?v=20260917`. Elle embarque aussi la même feuille dans `<style id="styles-snum-figes">` : le fichier HTML reste lisible lorsqu’il est ouvert seul sur un ordinateur. Ne pas supprimer ce bloc dans le livrable remis au propriétaire.

## Procédure de remplissage

1. Copier la coque HTML complète sans réécrire le header, le footer, le bloc de styles, les classes ni les scripts.
2. Remplacer tous les champs `{{...}}`. Aucun champ ni commentaire `EMPLACEMENT_...` ne doit rester dans le livrable.
3. Avec au moins trois événements, remplir exactement les trois cartes de L’essentiel avec trois événements déjà présents dans les rubriques. Avec un ou deux événements, supprimer entièrement le lien `#essentiel` et la section `#essentiel` ; ne conserver aucune carte vide.
4. Pour chaque événement de rubrique, dupliquer le fragment ARTICLE dans l’emplacement correspondant. Le nombre de fragments n’est pas limité par le modèle.
5. Retirer entièrement une rubrique vide et son lien de navigation. Ne jamais afficher une phrase de remplissage. Numéroter les rubriques visibles à partir de 02 lorsque L’essentiel existe, sinon à partir de 01.
6. Ne pas créer une rubrique Cybersécurité, Régulation ou Données : classer naturellement dans les cinq rubriques de référence, sauf nécessité forte documentée.
7. Ajouter À surveiller seulement avec le fragment optionnel prévu et un suivi précis.
8. Utiliser `p.fr-tag`, jamais `span.fr-tag`. Pour chaque nouvelle fenêtre, conserver `target="_blank"`, `rel="noopener noreferrer"` et l’indication textuelle masquée.
9. Livrer un document commençant par `<!doctype html>` et finissant par `</html>`, sans clôture de code Markdown dans le HTML.

## Coque HTML complète

```html
<!doctype html>
<html lang="fr" data-fr-scheme="system">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Revue de presse du {{DATE_EDITION}} - SNUM</title>
  <meta name="description" content="Revue de presse du SNUM du {{DATE_EDITION_LONGUE}}.">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/utility/icons/icons.min.css">
  <link rel="stylesheet" href="/revue-presse-snum/styles.css?v=20260917">
  <style id="styles-snum-figes">
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
  </style>
</head>
<body>
  <div class="fr-skiplinks">
    <nav class="fr-container" aria-label="Accès rapide">
      <ul class="fr-skiplinks__list">
        <li><a class="fr-link" href="#main">Accéder au contenu</a></li>
        <li><a class="fr-link" href="#navigation">Accéder au menu des rubriques</a></li>
        <li><a class="fr-link" href="#footer">Accéder au pied de page</a></li>
      </ul>
    </nav>
  </div>

  <header class="fr-header">
    <div class="fr-header__body">
      <div class="fr-container">
        <div class="fr-header__body-row">
          <div class="fr-header__brand fr-enlarge-link">
            <div class="fr-header__brand-top">
              <div class="fr-header__logo">
                <p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p>
              </div>
            </div>
            <div class="fr-header__service">
              <a href="/revue-presse-snum/" title="Accueil - Revue de presse du SNUM">
                <p class="fr-header__service-title">Service du numérique</p>
              </a>
              <p class="fr-header__service-tagline">Secrétariat général - Revue de presse</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main id="main">
    <section class="issue-head">
      <div class="fr-container">
        <p class="eyebrow">ÉDITION DU {{DATE_EDITION_LONGUE_MAJUSCULES}}</p>
        <h1>Revue de presse du SNUM</h1>
        <p class="lead">Période : {{DATE_DEBUT_COLLECTE}} - {{DATE_FIN_COLLECTE}}.</p>
        <nav id="navigation" class="topic-nav" aria-label="Rubriques">
          <a class="fr-link" href="#essentiel">L’essentiel</a>
          <!-- EMPLACEMENT_LIENS_RUBRIQUES : un lien par rubrique réellement présente -->
          <a class="fr-link" href="/revue-presse-snum/editions/">Archives</a>
        </nav>
      </div>
    </section>

    <section id="essentiel" class="fr-container section-block">
      <div class="section-title">
        <p class="section-number">01</p>
        <div><h2>L’essentiel</h2></div>
      </div>
      <div class="top-grid fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-4">
          <article class="fr-card fr-card--shadow top-card">
            <div class="fr-card__body"><div class="fr-card__content">
              <div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{{ESSENTIEL_1_RUBRIQUE}}</p></li></ul></div>
              <p class="meta">{{ESSENTIEL_1_SOURCE}} · {{ESSENTIEL_1_DATE}}</p>
              <h3 class="fr-card__title">{{ESSENTIEL_1_TITRE}}</h3>
              <p class="fr-card__desc"><span class="summary-text">{{ESSENTIEL_1_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ESSENTIEL_1_MOTS_CLES}}</span></p>
              <p class="takeaway"><strong>À retenir :</strong> {{ESSENTIEL_1_A_RETENIR}}</p>
              <p class="impact"><strong>Intérêt pour le SNUM :</strong> {{ESSENTIEL_1_INTERET}}</p>
              <div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="https://example.invalid/essentiel-1-url-a-remplacer" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : {{ESSENTIEL_1_TITRE}} - nouvelle fenêtre</span></a></div>
            </div></div>
          </article>
        </div>
        <div class="fr-col-12 fr-col-md-4">
          <article class="fr-card fr-card--shadow top-card">
            <div class="fr-card__body"><div class="fr-card__content">
              <div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{{ESSENTIEL_2_RUBRIQUE}}</p></li></ul></div>
              <p class="meta">{{ESSENTIEL_2_SOURCE}} · {{ESSENTIEL_2_DATE}}</p>
              <h3 class="fr-card__title">{{ESSENTIEL_2_TITRE}}</h3>
              <p class="fr-card__desc"><span class="summary-text">{{ESSENTIEL_2_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ESSENTIEL_2_MOTS_CLES}}</span></p>
              <p class="takeaway"><strong>À retenir :</strong> {{ESSENTIEL_2_A_RETENIR}}</p>
              <p class="impact"><strong>Intérêt pour le SNUM :</strong> {{ESSENTIEL_2_INTERET}}</p>
              <div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="https://example.invalid/essentiel-2-url-a-remplacer" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : {{ESSENTIEL_2_TITRE}} - nouvelle fenêtre</span></a></div>
            </div></div>
          </article>
        </div>
        <div class="fr-col-12 fr-col-md-4">
          <article class="fr-card fr-card--shadow top-card">
            <div class="fr-card__body"><div class="fr-card__content">
              <div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{{ESSENTIEL_3_RUBRIQUE}}</p></li></ul></div>
              <p class="meta">{{ESSENTIEL_3_SOURCE}} · {{ESSENTIEL_3_DATE}}</p>
              <h3 class="fr-card__title">{{ESSENTIEL_3_TITRE}}</h3>
              <p class="fr-card__desc"><span class="summary-text">{{ESSENTIEL_3_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ESSENTIEL_3_MOTS_CLES}}</span></p>
              <p class="takeaway"><strong>À retenir :</strong> {{ESSENTIEL_3_A_RETENIR}}</p>
              <p class="impact"><strong>Intérêt pour le SNUM :</strong> {{ESSENTIEL_3_INTERET}}</p>
              <div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="https://example.invalid/essentiel-3-url-a-remplacer" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : {{ESSENTIEL_3_TITRE}} - nouvelle fenêtre</span></a></div>
            </div></div>
          </article>
        </div>
      </div>
    </section>

    <!-- EMPLACEMENT_RUBRIQUES : insérer uniquement les rubriques non vides -->
    <!-- EMPLACEMENT_A_SURVEILLER : facultatif -->
  </main>

  <footer id="footer" class="fr-footer">
    <div class="fr-container">
      <div class="fr-footer__body">
        <div class="fr-footer__brand fr-enlarge-link">
          <a href="/revue-presse-snum/" title="Accueil - Revue de presse du SNUM">
            <p class="fr-logo">RÉPUBLIQUE<br>FRANÇAISE</p>
          </a>
        </div>
        <div class="fr-footer__content">
          <p class="fr-footer__content-desc">Équipe Communication / Événementiel du SNUM - Bureau aide à la gouvernance et fonctions support.</p>
        </div>
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
    </div>
  </footer>

  <dialog id="fr-theme-modal" class="fr-modal" aria-labelledby="fr-theme-modal-title">
    <div class="fr-container fr-container--fluid fr-container-md">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-6 fr-col-lg-4">
          <div class="fr-modal__body">
            <div class="fr-modal__header"><button aria-controls="fr-theme-modal" title="Fermer" type="button" class="fr-btn--close fr-btn">Fermer</button></div>
            <div class="fr-modal__content">
              <h2 id="fr-theme-modal-title" class="fr-modal__title">Paramètres d’affichage</h2>
              <div id="fr-display" class="fr-display">
                <fieldset class="fr-fieldset" id="display-fieldset">
                  <legend class="fr-fieldset__legend fr-fieldset__legend--regular" id="display-fieldset-legend">Choisissez un thème pour personnaliser l’apparence du site.</legend>
                  <div class="fr-fieldset__element"><div class="fr-radio-group"><input value="light" type="radio" id="fr-radios-theme-light" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-light">Thème clair</label></div></div>
                  <div class="fr-fieldset__element"><div class="fr-radio-group"><input value="dark" type="radio" id="fr-radios-theme-dark" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-dark">Thème sombre</label></div></div>
                  <div class="fr-fieldset__element"><div class="fr-radio-group"><input value="system" type="radio" id="fr-radios-theme-system" name="fr-radios-theme"><label class="fr-label" for="fr-radios-theme-system">Système</label></div></div>
                </fieldset>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </dialog>

  <script type="module" src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.module.min.js"></script>
  <script nomodule src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.nomodule.min.js"></script>
</body>
</html>
```

## Fragment RUBRIQUE

Dupliquer ce bloc une fois par rubrique non vide. Utiliser seulement `numerique`, `ia`, `commande`, `rh` ou `bercy` comme identifiant. Alterner la classe `section-muted` entre les rubriques visibles.

```html
<section id="{{RUBRIQUE_ID}}" class="{{CLASSE_FOND_OPTIONNELLE}}">
  <div class="fr-container section-block">
    <div class="section-title">
      <p class="section-number">{{NUMERO_RUBRIQUE}}</p>
      <div><h2>{{RUBRIQUE_TITRE}}</h2></div>
    </div>
    <div class="article-list fr-grid-row">
      <!-- EMPLACEMENT_ARTICLES : dupliquer le fragment ARTICLE pour chaque événement -->
    </div>
  </div>
</section>
```

## Fragment ARTICLE

```html
<article class="fr-col-12">
  <div class="article-body">
    <p class="meta">{{ARTICLE_SOURCE}} · {{ARTICLE_DATE}}</p>
    <h3>{{ARTICLE_TITRE}}</h3>
    <p class="summary"><span class="summary-text">{{ARTICLE_RESUME}}</span><br><strong>Mots-clés :</strong> <span class="keywords">{{ARTICLE_MOTS_CLES}}</span></p>
    <p class="takeaway"><strong>À retenir :</strong> {{ARTICLE_A_RETENIR}}</p>
    <p class="snum"><strong>Intérêt pour le SNUM :</strong> {{ARTICLE_INTERET}}</p>
  </div>
  <a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="{{ARTICLE_URL}}" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : {{ARTICLE_TITRE}} - nouvelle fenêtre</span></a>
</article>
```

## Fragment À SURVEILLER, facultatif

```html
<section id="surveiller" class="section-muted">
  <div class="fr-container section-block">
    <div class="watch">
      <h2>À surveiller</h2>
      <ul>
        <li>{{SUIVI_COURT_PRECIS}}</li>
      </ul>
    </div>
  </div>
</section>
```

## Fragment d’entrée pour les archives

Ne jamais reconstruire toute la page d’archives depuis une copie conservée dans le Projet. La personne chargée de publier fournit ou récupère la version actuelle de `editions/index.html`, puis ajoute seulement cette entrée en tête de la liste sans supprimer les précédentes.

```html
<article class="fr-col-12">
  <div class="article-body">
    <p class="meta">{{DATE_EDITION_LONGUE_MAJUSCULES}}</p>
    <h3>{{TITRE_COURT_EDITION}}</h3>
    <p>{{RESUME_TRES_COURT_EDITION}}</p>
  </div>
  <a class="fr-btn fr-btn--secondary source-btn" href="./{{AAAA-MM-JJ}}/">Consulter<span class="fr-sr-only"> l’édition du {{DATE_EDITION_LONGUE}}</span></a>
</article>
```

## Contrôles propres au HTML produit

- Aucun `{{...}}`, `example.invalid` ni commentaire `EMPLACEMENT_...` restant.
- Un seul `h1` ; avec au moins trois événements, exactement trois cartes dans `.top-grid` ; avec un ou deux événements, aucun lien ni section `#essentiel` ; autant d’articles de rubrique que d’événements uniques.
- Trois skiplinks et leurs cibles `#main`, `#navigation`, `#footer` ; identifiants uniques.
- Rubriques vides absentes ; liens de navigation strictement cohérents avec les rubriques présentes.
- Deux scripts DSFR 1.15.2 présents ; bloc `styles-snum-figes` conservé ; ouverture locale lisible.
- Footer réglementaire complet et mention `Accessibilité : non conforme` inchangée.
- Aucun `span.fr-tag`, aucun contenu privé, aucun cadratin dans le header ou le footer.
- Validation Nu et contrôle sans débordement horizontal à 200 % à exécuter sur le fichier rempli, pas seulement sur cette coque.
