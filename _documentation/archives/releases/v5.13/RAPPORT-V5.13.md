# Rapport de contrôle du kit SNUM V5.13

## Verdict

La V5.13 corrige les jours de semaine erronés et valide les douze paires canoniques sans relance intermédiaire. Elle ne produit toutefois aucun HTML au premier passage.

`RENDU` répond `A_COMPLETER | DONNEES_MANQUANTES`. Un message manuel `continue`, envoyé uniquement comme diagnostic, aboutit à `A_COMPLETER | SOURCE_MANQUANTE`.

Verdict : **NO-GO pour la production autonome**.

## Périmètre vérifié

- Projet Assistant DINUM : `Newsletter SNUM` ;
- prompt système V5.13 enregistré ;
- neuf ressources V5.13 indexées ;
- cinq phases exécutées dans une seule conversation ;
- Web activé seulement pour `COLLECTE` ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun projet ni conversation supprimé pendant la recette.

## Conversation de preuve

[Ouvrir la conversation V5.13](https://assistant.numerique.gouv.fr/chat/2816dcf4-93b9-454e-a94b-c99b26a677c8)

## Déroulé observé

### COLLECTE

La réponse annonce dix requêtes, couvre les cinq rubriques et au moins cinq domaines, liste neuf candidats puis se termine par `COLLECTE_TERMINEE`.

### VALIDATION

Deux sources sont conservées et sept sont exclues. L’égalité `2 + 7 = 9` est respectée. La réponse se termine par `VALIDATION_TERMINEE`.

### DONNEES

Deux fiches complètes sont produites : une pour `NUMERIQUE` et une pour `COMMANDE PUBLIQUE`. Les dates longues sont `6 OCTOBRE 2026` et `12 OCTOBRE 2026`, sans jour de semaine. La réponse se termine par `DONNEES_RENDU_PRETES`.

Anomalie : les deux sources sont marquées `ESSENTIEL : OUI`. Avec seulement deux sources valides, la règle exige pourtant l’absence de section et de lien `L’essentiel`.

### CANON

La réponse commence par `CANON_HTML_PRET`, cite la paire d’index V5.13 et les onze paires de fragments attendues. Aucun bloc HTML n’est affiché.

### RENDU

Le premier passage répond :

```text
A_COMPLETER
CONTROLES_EN_ECHEC
CODE | DONNEES_MANQUANTES
```

Aucun HTML n’est affiché.

Après un message manuel `continue`, utilisé comme diagnostic et non comme étape de production, la réponse devient :

```text
A_COMPLETER
CONTROLES_EN_ECHEC
CODE | SOURCE_MANQUANTE
```

Aucun HTML n’est affiché après cette reprise.

## Cause établie et cause probable

La trace établit qu’aucune des deux sources validées n’est réellement absente de `DONNEES_RENDU` : titre, URL, source, date, fait, mots-clés, synthèse et intérêt SNUM sont présents pour chacune.

La cause probable est une contradiction sur les essentiels. `DONNEES` marque deux sources comme essentielles, tandis que la règle finale impose zéro essentiel sous trois sources. Le prompt `RENDU` mentionne aussi l’assemblage de trois cartes avant d’énoncer l’exception applicable sous trois sources. L’Assistant semble alors rechercher une troisième source et classe l’échec comme `DONNEES_MANQUANTES`, puis `SOURCE_MANQUANTE`.

Cette explication reste une inférence : l’Assistant ne nomme ni le champ ni la source qu’il considère manquant.

## Contrôles locaux

- construction du kit : `KIT_PROGRESSIF_OK` ;
- tests unitaires : 27 réussis ;
- prompt système : 3 915 caractères, sous la limite de 4 000 ;
- prompt du README identique au fichier source ;
- ZIP V5.13 : SHA-256 `72c76ea64b85ce6c0dc913f8c235ba81854704eea6eb1d655f20b6f7c21c2293`.

Ces contrôles valident la cohérence déterministe du kit. Ils ne prouvent pas que l’Assistant DINUM réalise l’assemblage HTML.

## Preuve durable

La conversation V5.13 liée plus haut conserve les deux arrêts. Les captures locales ne sont pas publiées, car elles contiennent des éléments d’interface étrangers à la preuve.

## Décision

Conserver V5.13 comme preuve d’un garde-fou correct, pas comme version métier autonome. La prochaine correction devra rendre la règle des essentiels non contradictoire et exiger qu’un code `SOURCE_MANQUANTE` nomme la source concernée.
