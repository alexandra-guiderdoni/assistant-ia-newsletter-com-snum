# Coque HTML canonique - début

SNUM_SHELL_HEAD_START

Copier uniquement le bloc HTML suivant, sans les jetons de contrôle.

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
```

SNUM_SHELL_HEAD_END
