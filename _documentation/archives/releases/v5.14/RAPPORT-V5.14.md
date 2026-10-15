# Rapport de contrôle du kit SNUM V5.14

## Verdict

La V5.14 corrige les deux défauts ciblés de la V5.13 : la règle des essentiels est respectée et les contrôles en échec sont nominatifs. Elle ne produit toutefois aucun HTML au premier passage.

`RENDU` répond `A_COMPLETER` avec huit lignes `DONNEES_MANQUANTES`. Aucun message `continue` n’a été envoyé.

Verdict : **NO-GO pour la production autonome**.

## Périmètre vérifié

- Projet Assistant DINUM : `Newsletter SNUM` ;
- prompt système V5.14 enregistré ;
- neuf ressources V5.14 indexées ;
- cinq phases exécutées dans une seule conversation vierge ;
- Web activé seulement pour `COLLECTE` ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun commit ni push pendant cette recette.

## Conversation de preuve

[Ouvrir la conversation V5.14](https://assistant.numerique.gouv.fr/chat/f841d9c3-a65b-4ebf-84bd-d8a4d2993c8f)

## Déroulé observé

### COLLECTE

La réponse annonce dix requêtes réparties sur les cinq rubriques, couvre au moins cinq domaines, liste onze candidats et se termine par `COLLECTE_TERMINEE`.

Les URL sont cependant restituées sous la forme `domaine/chemin`, sans schéma `https://`. Cette perte empêche ensuite l’Assistant d’établir leur caractère canonique exact.

### VALIDATION

Cinq sources sont conservées et six sont exclues. L’égalité `5 + 6 = 11` est respectée. La réponse se termine par `VALIDATION_TERMINEE`.

Le doublon du Mois de l’innovation publique est détecté, mais l’Assistant conserve la page générale du 6 octobre et écarte la page dédiée du 7 octobre. Ce choix ne suit pas clairement la priorité demandée à la source la plus directe, puis à la plus récente.

### DONNEES

Cinq fiches complètes sont produites dans trois rubriques. Les dates longues sont en majuscules et ne comportent aucun jour de semaine.

Exactement trois fiches portent `ESSENTIEL : OUI` et les deux autres `ESSENTIEL : NON`. La réponse se termine par `DONNEES_RENDU_PRETES`.

La correction principale de la V5.14 est donc confirmée.

### CANON

La réponse commence par `CANON_HTML_PRET` et cite la paire d’index V5.14. Les six premières paires sont nommées correctement.

Les cinq dernières entrées ne recopient pas les paires `START/END` attendues :

- `SNUM_RUBRIC_OPEN / SNUM_RUBRIC_CLOSE` remplace deux paires distinctes ;
- `SNUM_RUBRIC_ARTICLE`, `SNUM_WATCH` et `SNUM_EMPTY` sont déclarés « auto-fermants » ;
- `ESSENTIELS_OPEN / ESSENTIALS_CLOSE` est ajouté alors que cette paire n’existe pas dans les fragments.

Le jeton `CANON_HTML_PRET` est donc un faux positif : la trace ne prouve pas le chargement exact des onze paires.

### RENDU

Le premier et unique passage répond :

```text
A_COMPLETER
## CONTROLES_EN_ECHEC
DONNEES_MANQUANTES | EDITION | title
DONNEES_MANQUANTES | EDITION | fr-theme-modal
DONNEES_MANQUANTES | EDITION | scripts DSFR 1.15.2
DONNEES_MANQUANTES | CNCP_2026_10_12 | vérification de l'URL exacte
DONNEES_MANQUANTES | CNCP_2026_10_10 | vérification de l'URL exacte
DONNEES_MANQUANTES | JFC_2026_10_06 | vérification de l'URL exacte
DONNEES_MANQUANTES | MIP_2026_10_06 | vérification de l'URL exacte
DONNEES_MANQUANTES | OCDE_2026_10_12 | vérification de l'URL exacte
```

Aucun HTML n’est affiché, conformément au garde-fou.

## Causes établies

Le `title`, `fr-theme-modal` et les scripts DSFR 1.15.2 existent dans les fragments canoniques locaux. Leur absence déclarée au rendu, associée aux noms de paires inexacts pendant `CANON`, établit que l’Assistant n’a pas réutilisé le canon avec une fidélité suffisante.

Les cinq URL de `DONNEES_RENDU` sont dépourvues de schéma. Le contrôle final ne peut donc pas les reconnaître comme URL canoniques exactes.

La V5.14 améliore ainsi le diagnostic, mais ne corrige pas la transmission fiable du HTML canonique ni la conservation des URL absolues.

## Preuve durable

La conversation V5.14 liée plus haut conserve l’arrêt et ses contrôles nominatifs. Les captures locales ne sont pas publiées, car elles contiennent des éléments d’interface étrangers à la preuve.

## Décision

Conserver V5.14 comme preuve que les garde-fous et les diagnostics progressent, mais ne pas la livrer comme version métier autonome.

La correction suivante devra rendre le contrôle `CANON` strict sur les noms `START/END` et conserver des URL absolues avec `https://` dès `COLLECTE`.

## PDG pass

- Déclenchement : oui, car ce rapport met à jour un guide d’installation et un verdict de livraison durable.
- Compétence : `progressive-disclosure-guard`, appliquée pour séparer le verdict, les preuves, les causes établies et les limites.
- Artefacts inspectés : conversation V5.14, index canonique, jetons des fragments 06 à 10, README, notice, scripts de construction et tests.
- Chevauchement : mise à jour des documents V5.14 existants ; aucun guide parallèle ni second mode opératoire créé.
- Affirmation « règle des essentiels corrigée » : confirmée par les cinq fiches et les trois valeurs `ESSENTIEL=OUI` observées.
- Affirmation « canon chargé fidèlement » : rejetée par les cinq noms de paires inexacts et les trois éléments d’édition déclarés manquants.
- Affirmation « URL canoniques préservées » : rejetée, car les cinq URL de `DONNEES_RENDU` sont dépourvues de schéma.
- Connu : le premier `RENDU` s’arrête sans HTML et nomme huit écarts.
- Inconnu : le comportement d’une autre exécution non déterministe avec le même kit.
- Mauvais raccourci interdit : envoyer `continue` et présenter une reprise comme une génération autonome réussie.
- Comportement à préserver : arrêt sans HTML dès qu’un contrôle final échoue.
- Preuve de régression requise : nouvelle conversation vierge, cinq phases sans correction, puis HTML complet au premier `RENDU`.
- Revue : auto-contrôle PDG, pas une revue indépendante.
