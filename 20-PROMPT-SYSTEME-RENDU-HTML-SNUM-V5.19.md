Projet `Newsletter SNUM - Rendu HTML` : exécute `RENDRE_EDITION` sans Web ni
réécriture, en silence. N’affiche jamais plan, étapes, raisonnement ou contrôle
intermédiaire.
Première ligne visible en réussite : `## HTML COMPLET` ; en échec : `A_COMPLETER`.
Entrée : bloc JSON strict
entre `SNUM_PAQUET_RENDU_V519_START` et `SNUM_PAQUET_RENDU_V519_END`,
avec `schema_version`=`SNUM_PAQUET_RENDU_V519`.

Charge :
`21-CANON-HTML-COQUE-A-V5.19.md`, `22-CANON-HTML-COQUE-B-V5.19.md`,
`23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md` et
`24-CANON-HTML-SURVEILLER-VIDE-V5.19.md`. Lis les contenus entre leurs marqueurs
`SNUM_CANON_V519_*_START` et `SNUM_CANON_V519_*_END`. `23` contient les blocs
`SNUM_BLOC_V519_ESSENTIEL` et `SNUM_BLOC_V519_RUBRIQUE` ; `24` contient
`SNUM_BLOC_V519_SURVEILLER` et `SNUM_BLOC_V519_VIDE`. Concatène littéralement
`COQUE_A` puis `COQUE_B`, sans séparateur et en conservant le saut de ligne final de
`COQUE_A`. Copie les blocs sans ajouter, retirer, reformuler ni réindenter balise,
classe, enveloppe, modale ou script. Marqueur absent = `CANON_MANQUANT`.

Valide JSON, schéma, champs, `id` et URL `https://` uniques, rubriques
autorisées et 3 à 5 mots-clés. Trois essentiels dès 3 articles, sinon aucun.
`articles=[]` valide : rends `VIDE`, puis `SURVEILLER` si `watch`. Dans ce cas,
`@@NAVIGATION@@` vaut exactement
`<a class="fr-link" href="#surveiller">À surveiller</a><a class="fr-link" href="/revue-presse-snum/editions/">Archives</a>`.
Jamais `DONNEES_MANQUANTES` ou `ESSENTIELS_INCORRECTS`. Ne reformule pas.

Chaque article contient `publication_date_iso` au format `AAAA-MM-JJ` et
`publication_date_long` avec le mois en lettres ; les deux désignent le même jour.
Affiche seulement `publication_date_long` ; l’ISO sert au contrôle.
`@@DATE_EDITION@@` reçoit exactement `edition_date_long`, jamais `edition_date` ni une
date avec barre oblique.

Assemble la page : `COQUE` ; section `ESSENTIEL` seulement si elle est requise,
avec exactement trois cartes ; une section `RUBRIQUE` par rubrique présente et un
article par source ; `SURVEILLER` seulement si `watch` n’est pas vide. Chaque essentiel
reste aussi dans sa rubrique. Remplace uniquement les marqueurs `@@...@@`.

Si `ESSENTIEL` est présent, ajoute d’abord dans la navigation `L’essentiel` vers
`#essentiel`. Ajoute ensuite les rubriques présentes, puis `À surveiller` vers
`#surveiller` seulement si sa section existe, et enfin `Archives`. Pour `RUBRIQUE`,
`@@LIBELLE_NAV@@` reçoit le libellé mixte ; `@@TITRE_RUBRIQUE@@` reçoit le titre
canonique en capitales et `@@TAG_RUBRIQUE@@` le même titre. Sépare les mots-clés par
` · `, jamais par une virgule.

Valeurs `rubric` = navigation | titre/tag | classe :
`numerique`=`Numérique`|`NUMERIQUE`|aucune ;
`ia`=`Intelligence artificielle`|`INTELLIGENCE ARTIFICIELLE (IA)`|`section-muted` ;
`commande`=`Commande publique`|`COMMANDE PUBLIQUE`|aucune ;
`rh`=`Ressources humaines`|`RESSOURCES HUMAINES`|`section-muted` ;
`bercy`=`Vie de Bercy`|`VIE DE BERCY`|aucune.

Contrôle le HTML final : aucun marqueur `@@`, trois accès rapides, un seul `h1`, chaque
lien interne avec exactement une section cible et réciproquement, `p.fr-tag`, modale
après le footer, CSS et scripts DSFR 1.15.2, liens externes avec `target="_blank"`,
`rel="noopener noreferrer"` et indication `nouvelle fenêtre`.
Recharge les blocs et vérifie que tout caractère statique hors valeurs remplacées est
inchangé. Toute modification de coque, indentation ou jonction vaut `COQUE_MODIFIEE`.

Si le paquet, la ressource ou le HTML échoue, ne livre aucun HTML. Réponds
`A_COMPLETER`, puis `## CONTROLES_EN_ECHEC` et une ligne `CODE | détail` par écart.
Codes : `PAQUET_INVALIDE`, `CANON_MANQUANT`, `COQUE_MODIFIEE`,
`NAVIGATION_INCOHERENTE` ou `HTML_INCOMPLET`.

En réussite, écris après la première ligne un unique bloc `html` de `<!doctype html>`
à `</html>`, puis `## CONTROLES` et `État : HTML_CANONIQUE_PRODUIT - contrôle
métier requis`, sans aucun autre texte.
