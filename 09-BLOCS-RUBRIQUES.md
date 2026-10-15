# Bloc HTML canonique - rubrique

SNUM_RUBRIC_START

Copier uniquement le bloc HTML suivant, sans les jetons de contrôle.

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

SNUM_RUBRIC_END

# Bloc HTML canonique - à surveiller

SNUM_WATCH_START

Copier uniquement le bloc HTML suivant, sans les jetons de contrôle.

```html
<section id="surveiller" class="section-muted"><div class="fr-container section-block"><div class="section-title"><p class="section-number">@@NUMERO@@</p><div><h2>À surveiller</h2></div></div><div class="article-list fr-grid-row"><article class="fr-col-12"><div class="article-body"><h3>@@TITRE_SUIVI@@</h3><p class="summary">@@SUIVI_COURT@@</p></div></article></div></div></section>
```

SNUM_WATCH_END

# Bloc HTML canonique - collecte vide

SNUM_EMPTY_START

Copier uniquement le bloc HTML suivant, sans les jetons de contrôle.

```html
<section><div class="fr-container section-block"><div class="section-title"><p class="section-number">01</p><div><h2>Collecte à compléter</h2><p>Aucun événement n’a pu être établi à partir d’une source publique intégrale dans la fenêtre.</p></div></div></div></section>
```

SNUM_EMPTY_END
