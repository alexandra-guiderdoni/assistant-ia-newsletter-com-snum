# Installation du kit V5.8 et recette du 15 octobre 2026

## Résultat

Le Projet unique `Newsletter SNUM` a été configuré dans l’Assistant DINUM avec le kit progressif V5.8.

Après réactivation de la session AgentConnect, une recette complète a exécuté `COLLECTE`, `VALIDATION`, `CANON` et `RENDU`. L’Assistant a produit un HTML complet, mais ce HTML n’est pas identique au canon Bacoco. Verdict : **NO-GO pour une livraison autonome**.

Le défaut décisif porte sur les enveloppes de rubrique : les classes `section-muted` obligatoires manquent sur `ia` et `rh`. Le garde-fou aurait dû répondre `A_COMPLETER — HTML canonique non établi` ; il a pourtant affiché le HTML.

## Niveau 1 — Prompt système du Projet

Le fichier source est `PROMPT-SYSTEME-SNUM-V5.8.md`. Son contenu a été copié une seule fois dans **Instructions (expérimental)**.

Contrôles observés avant enregistrement :

- longueur : 3 715 caractères, sous la limite de 4 000 ;
- terminaison : `N’affirme aucun contrôle non exécuté.` ;
- huit ressources visibles après indexation :
  - `00-PROMPT-PROJET.md` ;
  - `01-ETAT-HISTORIQUE.md` ;
  - `02-METHODE-EDITORIALE.md` ;
  - `05-INDEX-HTML.md` ;
  - `06-COQUE-DEBUT.md` ;
  - `07-COQUE-FIN.md` ;
  - `08-BLOC-ESSENTIEL.md` ;
  - `09-BLOCS-RUBRIQUES.md`.

Le message `Le projet a été mis à jour.` a confirmé l’enregistrement.

## Niveau 2 — Prompts utilisateur de l’édition

Les prompts utilisateur ne remplacent pas le prompt système. Ils sont envoyés à chaque édition, dans une même conversation et dans cet ordre.

### Qualification — phase A

1. `COLLECTE`, Web activé : chercher et ouvrir les sources, relever leur date de publication et terminer par `COLLECTE_TERMINEE`.
2. `VALIDATION`, Web désactivé : appliquer la fenêtre ISO, l’accès intégral et le dédoublonnage, puis terminer par `VALIDATION_TERMINEE`.

### Production — phase B

3. `CANON`, Web désactivé : charger les fragments `06`, `07`, `08` et `09`, vérifier les six paires `START/END`, puis répondre `CANON_HTML_PRET` ou `CANON_HTML_INCOMPLET`.
4. `RENDU`, Web désactivé : utiliser seulement `SOURCES_VALIDES` et les fragments chargés au tour précédent ; livrer `REVUE`, `HTML COMPLET` et `DOSSIER PRIVÉ`, ou appliquer l’arrêt `A_COMPLETER`.

Les quatre textes copiables sont maintenus dans [`NOTICE-V5.8.md`](../../NOTICE-V5.8.md).

## Première tentative avant reconnexion

Paramètres utilisés :

- édition : 14 octobre 2026 ;
- fenêtre : 3 octobre 2026 au 13 octobre 2026 inclus ;
- première étape : `COLLECTE` ;
- Web : activé ;
- conversation : <https://assistant.numerique.gouv.fr/chat/07df2114-3b64-44c4-9f9b-b5850203e48b>.

La conversation a bien été créée dans `Newsletter SNUM`, mais l’Assistant a affiché `Désolé, une erreur s’est produite. Veuillez réessayer.` avant toute réponse métier.

Après deux échecs initiaux, le rechargement de la page et une nouvelle conversation du Projet ont produit le même résultat. Le journal navigateur a donné la cause : `the authentication session has expired`.

## Conversation générale écartée

Après reconnexion, la conversation fournie pour reprendre le test était intitulée `Test assistance` :

<https://assistant.numerique.gouv.fr/chat/da262a92-c15c-4584-9fd6-c71f29d8b95a>

Le panneau de gauche la classait sous **Vos conversations**, hors du Projet `Newsletter SNUM`. Elle ne pouvait donc pas consulter les huit ressources. La collecte y a produit des textes Legifrance hors sujet et `CANON` s’est arrêté avec `CANON_HTML_INCOMPLET SNUM_CANON_V58_INDEX_START`.

Cette conversation ne constitue pas une recette du kit.

## Recette complète dans le Projet

Une nouvelle conversation a été créée depuis **Start new conversation in Newsletter SNUM** :

<https://assistant.numerique.gouv.fr/chat/b549f1f0-5c1b-487b-aeb2-20a164ba157f>

Paramètres :

- édition : 14 octobre 2026 ;
- fenêtre inclusive : 3 octobre 2026 au 13 octobre 2026 ;
- Web activé uniquement pour `COLLECTE`.

Résultats observés :

1. `COLLECTE_TERMINEE` : trois candidats issus de numerique.gouv.fr, dont deux datés du 13 octobre et un du 1er octobre.
2. `VALIDATION_TERMINEE` : deux sources conservées ; la source du 1er octobre a été exclue comme hors fenêtre.
3. `CANON_HTML_PRET` : les six paires `START/END` ont été déclarées présentes.
4. `RENDU` : les sections `REVUE`, `HTML COMPLET` et `DOSSIER PRIVÉ` ont été affichées avec un document allant de `<!doctype html>` à `</html>`.

## Contrôles du rendu

Contrôles positifs observés dans la page :

- titre `Revue de presse du 14 octobre 2026 - SNUM` ;
- feuille `/revue-presse-snum/styles.css?v=20260917` ;
- modal `fr-theme-modal` ;
- script `dsfr.nomodule.min.js` ;
- aucun marqueur `@@` supplémentaire dans le HTML ;
- source Cybermois hors fenêtre absente du rendu ;
- un titre principal exact `<h1>Revue de presse du SNUM</h1>`.

Régressions observées :

- `<section id="ia" class="section-muted">` absent ; le rendu contient `<section id="ia">` ;
- `<section id="rh" class="section-muted">` absent ;
- le HTML a été livré malgré ces écarts, au lieu de l’arrêt `A_COMPLETER` ;
- aucun contenu n’était visible sous `DOSSIER PRIVÉ` dans l’état accessible observé.

Le contrôle a été réalisé sur le texte affiché et par recherche littérale dans la page. Le HTML n’a pas été exporté vers un fichier local ; le validateur Python n’a donc pas été exécuté sur cette sortie.

## Verdict

Verdict limité aux preuves observées :

- installation du kit : **RÉUSSIE** ;
- session AgentConnect : **RÉTABLIE** ;
- collecte et filtrage des dates : **EXÉCUTÉS** ;
- chargement des six fragments : **DÉCLARÉ RÉUSSI PAR L’ASSISTANT** ;
- génération d’un HTML complet : **RÉUSSIE** ;
- fidélité au canon Bacoco : **ÉCHEC OBSERVÉ** ;
- arrêt fermé en cas d’écart : **ÉCHEC OBSERVÉ** ;
- publication autonome : **NO-GO**.

Le test confirme la limite déjà documentée : l’Assistant retrouve le canon, mais ne garantit pas sa copie littérale dans une longue réponse.

## Limites des preuves

Les captures locales prises pendant l’incident montraient un autre onglet Chrome que l’onglet piloté ; elles ont été supprimées et ne sont pas utilisées comme preuve. Les captures d’interface déjà vérifiées restent dans `_documentation/validation-v5.8-2026-10-14/captures/`.

Le contrôle DOM prouve la présence du prompt et des huit fichiers au moment de l’installation. `CANON_HTML_PRET` reste une déclaration de l’Assistant, pas une preuve indépendante de fidélité du rendu.
