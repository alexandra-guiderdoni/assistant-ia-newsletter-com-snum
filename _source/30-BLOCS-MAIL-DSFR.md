# Courriel SNUM — blocs canoniques DSFR

Source unique du nouveau rendu de courriel ; les deux kits existants restent indépendants.
HTML autonome, logo base64 inchangé, flèches décoratives et styles en ligne.
<!-- PDG-BINARY-ASSET-JUSTIFICATION: le logo du prototype reste incorporé pour l’autonomie demandée. -->

## PAGE

```html
<!doctype html>
<!-- Courriel DSFR SNUM autonome ; logo incorporé et flèches décoratives.
Le rendu navigateur ne constitue pas une recette Outlook. -->
<html lang="fr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>Revue de presse du SNUM — @@EDITION_LONG@@</title>
  <!--[if mso]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
  <style>
    :root { color-scheme: light dark; supported-color-schemes: light dark; }
    body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    td { mso-line-height-rule: at-least; }
    img { border: 0; display: block; }
    a { text-decoration: underline; text-underline-offset: 3px; }
    a:focus-visible { outline: 2px solid #000091; outline-offset: 3px; }
    @media only screen and (max-width: 600px) {
      .outer-pad { padding: 0 !important; }
      .content-pad { padding-left: 20px !important; padding-right: 20px !important; }
      .mail-title { font-size: 28px !important; line-height: 36px !important; }
      .signature-image, .signature-text { display: block !important; width: 100% !important; }
      .signature-image { padding-bottom: 20px !important; }
      .signature-text { padding-left: 0 !important; }
    }
    @media only screen and (max-width: 360px) {
      .content-pad { padding-left: 16px !important; padding-right: 16px !important; }
    }
    @media (prefers-color-scheme: dark) {
      body, .outer-bg { background-color: #161616 !important; }
      .surface { background-color: #1e1e1e !important; }
      .title-bg, .section-bg, .footer-bg { background-color: #1b1b35 !important; }
      .text-main, .mail-title { color: #ffffff !important; }
      .text-muted { color: #cecece !important; }
      .text-brand, a.mail-link { color: #8585f6 !important; }
      .mail-border { border-color: #353535 !important; }
      .brand-rule { border-color: #8585f6 !important; }
      a:focus-visible { outline-color: #8585f6; }
    }
    [data-ogsc] .outer-bg { background-color: #161616 !important; }
    [data-ogsc] .surface { background-color: #1e1e1e !important; }
    [data-ogsc] .title-bg, [data-ogsc] .section-bg, [data-ogsc] .footer-bg { background-color: #1b1b35 !important; }
    [data-ogsc] .text-main, [data-ogsc] .mail-title { color: #ffffff !important; }
    [data-ogsc] .text-muted { color: #cecece !important; }
    [data-ogsc] .text-brand, [data-ogsc] a.mail-link { color: #8585f6 !important; }
    [data-ogsc] .mail-border { border-color: #353535 !important; }
    [data-ogsc] .brand-rule { border-color: #8585f6 !important; }
    @media (forced-colors: active) { a { text-decoration: underline !important; } }
  </style>
</head>
<body class="outer-bg" style="margin:0; padding:0; background-color:#f6f6f6; color:#161616; font-family:'Marianne',Arial,Helvetica,sans-serif;">
  <div role="article" aria-roledescription="courriel" lang="fr" style="font-family:'Marianne',Arial,Helvetica,sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f6f6f6" class="outer-bg" style="width:100%; background-color:#f6f6f6;">
      <tr><td align="center" class="outer-pad" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:32px 16px;">
        <!--[if mso]><table role="presentation" width="600" align="center" cellspacing="0" cellpadding="0" border="0"><tr><td style="font-family:'Marianne',Arial,Helvetica,sans-serif;"><![endif]-->
        <table role="presentation" width="600" align="center" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" class="surface mail-border" style="width:100%; max-width:600px; margin:0 auto; background-color:#ffffff; border:1px solid #e5e5e5;">
          <tr><td class="surface content-pad brand-rule" bgcolor="#ffffff" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:24px 40px; border-top:3px solid #000091; background-color:#ffffff;">
            <p class="text-main" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#161616; font-size:14px; line-height:22px; font-weight:700;">SERVICE DU NUMÉRIQUE (SNUM)</p>
          </td></tr>
          <tr><td class="title-bg content-pad" bgcolor="#ececfe" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:28px 40px 30px; background-color:#ececfe;">
            <h1 class="mail-title text-main" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 12px; color:#161616; font-size:32px; line-height:40px; font-weight:700;">REVUE DE PRESSE</h1>
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#3a3a3a; font-size:14px; line-height:22px;">Édition du @@EDITION_LONG@@</p>
          </td></tr>
          <tr><td class="surface content-pad" bgcolor="#ffffff" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:28px 40px 20px; background-color:#ffffff;">
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 8px; color:#3a3a3a; font-size:16px; line-height:24px;">@@INTRO@@</p>
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 8px; color:#3a3a3a; font-size:16px; line-height:24px;">Bonne lecture&nbsp;!</p>
          </td></tr>

@@RUBRICS@@
@@WATCH@@
          <tr><td class="footer-bg content-pad" bgcolor="#f5f5fe" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:24px 40px; background-color:#f5f5fe;">
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 6px; color:#666666; font-size:13px; line-height:21px; font-weight:700;">Revue de presse · Diffusion deux fois par semaine</p>
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#666666; font-size:13px; line-height:21px;">Document à usage interne</p>
          </td></tr>
          <tr><td class="surface content-pad" bgcolor="#ffffff" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:28px 40px; background-color:#ffffff;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;">
              <tr>
                <td class="signature-image" width="147" valign="top" style="font-family:'Marianne',Arial,Helvetica,sans-serif; width:147px; vertical-align:top;">
                  <div style="font-family:'Marianne',Arial,Helvetica,sans-serif; display:inline-block; padding:8px; background-color:#ffffff;"><img src="data:image/png;base64,@@LOGO@@" alt="Ministères économiques et financiers — Secrétariat général" width="147" style="display:block; width:147px; max-width:100%; height:auto; border:0; background-color:#ffffff;"></div>
                </td>
                <td class="signature-text" valign="top" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding-left:24px; vertical-align:top;">
                  <p class="text-main" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 6px; color:#161616; font-size:13px; line-height:20px; font-weight:700;">Équipe Communication / Événementiel du SNUM</p>
                  <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 6px; color:#666666; font-size:13px; line-height:20px;">Secteur relations bénéficiaires, gouvernance interne, communication</p>
                  <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 6px; color:#666666; font-size:13px; line-height:20px;">Bureau aide à la gouvernance et fonctions support (BGS)</p>
                  <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 6px; color:#666666; font-size:13px; line-height:20px;">Service du numérique (SNUM) du SG</p>
                </td>
              </tr>
            </table>
          </td></tr>
          <tr><td class="footer-bg content-pad mail-border" bgcolor="#f5f5fe" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:24px 40px; border-top:1px solid #e5e5e5; background-color:#f5f5fe;">
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 12px; color:#666666; font-size:14px; line-height:22px;">Vous souhaitez gérer votre abonnement&nbsp;? Vous avez des questions&nbsp;?</p>
            <p class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#000091; font-size:14px; line-height:26px;"><span aria-hidden="true" style="font-family:'Marianne',Arial,Helvetica,sans-serif;">→ </span><a class="mail-link" href="mailto:agents-snum-subscribe@listes.finances.gouv.fr?subject=Je%20souhaite%20m&#x27;abonner%20à%20la%20revue%20de%20presse%20du%20SNUM" target="_blank" rel="noopener noreferrer" style="font-family:'Marianne',Arial,Helvetica,sans-serif; color:#000091; text-decoration:underline; font-weight:700;">S’abonner</a> / <span aria-hidden="true" style="font-family:'Marianne',Arial,Helvetica,sans-serif;">→ </span><a class="mail-link" href="mailto:agents-snum-unsubscribe@listes.finances.gouv.fr?subject=Je%20souhaite%20me%20désabonner%20de%20la%20revue%20de%20presse%20du%20SNUM" target="_blank" rel="noopener noreferrer" style="font-family:'Marianne',Arial,Helvetica,sans-serif; color:#000091; text-decoration:underline; font-weight:700;">Se désabonner</a> / <span aria-hidden="true" style="font-family:'Marianne',Arial,Helvetica,sans-serif;">→ </span><a class="mail-link" href="mailto:gouvernance.sg-snum@finances.gouv.fr?subject=Des%20questions%20sur%20la%20revue%20de%20presse%20du%20SNUM%20?" target="_blank" rel="noopener noreferrer" style="font-family:'Marianne',Arial,Helvetica,sans-serif; color:#000091; text-decoration:underline; font-weight:700;">Nous contacter</a></p>
          </td></tr>
        </table>
        <!--[if mso]></td></tr></table><![endif]-->
      </td></tr>
    </table>
  </div>
</body>
</html>


```

## ARTICLE

```html
              <tr><td data-article-id="@@ID@@" class="mail-border" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:24px 0; border-bottom:1px solid #e5e5e5;">
                @@ESSENTIAL@@
                <h3 style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 10px; font-size:20px; line-height:28px; font-weight:700;"><span aria-hidden="true" class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; color:#000091; font-size:16px; font-weight:400;">→&nbsp;</span><a class="mail-link" data-article-link="@@ID@@" href="@@URL@@" target="_blank" rel="noopener noreferrer" style="font-family:'Marianne',Arial,Helvetica,sans-serif; color:#000091; text-decoration:underline;">@@TITLE@@</a></h3>
                <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 16px; color:#666666; font-size:13px; line-height:21px;">@@SOURCE@@ · <time datetime="@@DATE_ISO@@" style="font-family:'Marianne',Arial,Helvetica,sans-serif;">@@DATE_LONG@@</time></p>
                <p class="text-main" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 12px; color:#161616; font-size:16px; line-height:24px; ">@@FACT@@</p>
                <p class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 12px; color:#000091; font-size:16px; line-height:24px;"><strong style="font-family:'Marianne',Arial,Helvetica,sans-serif;">À retenir&nbsp;:</strong> @@TAKEAWAY@@</p>
                <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 12px; color:#666666; font-size:14px; line-height:22px;"><strong style="font-family:'Marianne',Arial,Helvetica,sans-serif;">Intérêt pour le SNUM&nbsp;:</strong> @@INTEREST@@</p>
                <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#666666; font-size:12px; line-height:20px;"><strong style="font-family:'Marianne',Arial,Helvetica,sans-serif;">Mots-clés&nbsp;:</strong> @@KEYWORDS@@</p>
              </td></tr>
```

## ESSENTIAL

```html
<p class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 8px; color:#000091; font-size:12px; line-height:20px; font-weight:700; letter-spacing:0.5px;">ESSENTIEL</p>
```

## RUBRIC

```html
          <tr><td class="surface content-pad" bgcolor="#ffffff" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:8px 40px 24px; background-color:#ffffff;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;">
              <tr><td class="section-bg" bgcolor="#f5f5fe" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:14px 16px; background-color:#f5f5fe;">
                <h2 class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#000091; font-size:18px; line-height:26px; font-weight:700;">@@NUMBER@@ · @@LABEL@@</h2>
                
              </td></tr>
              
@@ARTICLES@@
            </table>
          </td></tr>
```

## WATCH

```html
          <tr><td class="section-bg content-pad" bgcolor="#f5f5fe" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:24px 40px; background-color:#f5f5fe;">
            <h2 class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 16px; color:#000091; font-size:18px; line-height:26px; font-weight:700;">À surveiller</h2>
@@WATCH_ITEMS@@
          </td></tr>
```

## WATCH_ITEM

```html
            <h3 class="text-main" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 6px; color:#161616; font-size:16px; line-height:24px; font-weight:700;">@@WATCH_TITLE@@</h3>
            <p class="text-muted" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 16px; color:#666666; font-size:14px; line-height:22px;">@@WATCH_SUMMARY@@</p>
```

## EMPTY

```html
          <tr><td class="surface content-pad" bgcolor="#ffffff" style="font-family:'Marianne',Arial,Helvetica,sans-serif; padding:16px 40px 32px; background-color:#ffffff;">
            <h2 class="text-brand" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0 0 12px; color:#000091; font-size:18px; line-height:26px;">Collecte à compléter</h2>
            <p class="text-main" style="font-family:'Marianne',Arial,Helvetica,sans-serif; margin:0; color:#161616; font-size:16px; line-height:24px;">Aucun article transmis dans ce paquet.</p>
          </td></tr>
```


## LOGO

```html
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
```
