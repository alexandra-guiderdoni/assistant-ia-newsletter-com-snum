# Rapport de contrôle du kit SNUM V5.9

## Verdict

Le canon local est fidèle au dépôt `bacoco/revue-presse-snum`. La divulgation progressive contourne la limite de 4 000 caractères de l’Assistant DINUM et permet de retrouver les six fragments HTML.

L’Assistant ne recopie toutefois pas ces fragments de façon déterministe dans une longue sortie. Verdict : **NO-GO pour une production ou une publication autonome garantissant un HTML identique à Bacoco**.

Le kit reste utilisable en recette avec arrêt fermé : si la conformité n’est pas établie, l’Assistant doit répondre `A_COMPLETER — HTML canonique non établi` sans afficher de code.

## Solution progressive livrée

- prompt système inférieur à 4 000 caractères ;
- index `05-INDEX-HTML.md` ;
- coque répartie entre `06-COQUE-DEBUT.md` et `07-COQUE-FIN.md` ;
- carte essentielle dans `08-BLOC-ESSENTIEL.md` ;
- blocs de rubrique, surveillance et vide dans `09-BLOCS-RUBRIQUES.md` ;
- ZIP `kit-dinum-snum-v5-9-progressif-8-fichiers.zip` ;
- protocole en quatre messages : collecte, validation, canon, rendu ;
- validateur renforcé sur les titres exacts de rubrique.

Les fragments sont générés depuis `05-BLOCS-HTML-CANONIQUES.md`, qui reste la source unique.

## Recettes réelles du 14 octobre 2026

### Chargement progressif

Deux conversations distinctes ont retrouvé `SNUM_CANON_V58_INDEX_START` et les six paires de jetons avec la V5.8. La V5.9 utilise `SNUM_CANON_V59_INDEX_START` et conserve le même découpage progressif.

### Génération en deux phases

Le canon a été retrouvé, puis un HTML complet a été produit. Le contrôle a néanmoins relevé des sources hors fenêtre, des libellés de rubrique non canoniques et une navigation trop large.

[Conversation de recette](https://assistant.numerique.gouv.fr/chat/88b774da-c07b-4b78-a5bb-22739def300f)

### Durcissement des dates

Après renforcement, l’Assistant a d’abord déclaré à tort le 6 octobre hors d’une fenêtre allant du 3 au 13 octobre. Une phase d’audit a corrigé l’arithmétique, mais la revue visible est restée incomplète.

[Conversation de durcissement](https://assistant.numerique.gouv.fr/chat/066f718b-db2f-432c-a576-ec96104ebb57)

### Séparation collecte, validation, canon et rendu

La collecte structurée a produit cinq candidats. La validation sans Web a conservé trois sources et écarté une incohérence et un doublon. Un premier rendu, séparé de la collecte, a reconstruit un HTML non canonique.

Le canon a alors été rechargé juste avant un nouveau rendu. Le garde-fou a refusé la sortie et affiché :

```text
A_COMPLETER — HTML canonique non établi
```

Cet arrêt est préférable au HTML inventé. Il démontre cependant que l’Assistant ne garantit pas l’assemblage littéral, même quand les fragments sont indexés et retrouvés.

[Conversation en phases séparées](https://assistant.numerique.gouv.fr/chat/4dddefda-e5da-4736-b4ca-9464e8b5c9dd)

### Validation des dates et correspondance navigation-sections

Une recette complémentaire du 15 octobre 2026 a d’abord montré qu’une validation simple pouvait conserver une source datée du 2 octobre dans une fenêtre commençant le 3 octobre. Une nouvelle conversation a ensuite été créée explicitement dans le Projet `Newsletter SNUM`.

La validation renforcée y a contrôlé cinq candidats ligne par ligne, conservé la seule source datée du 8 octobre et exclu quatre sources. `CANON_HTML_PRET` a ensuite annoncé les six paires attendues. Le rendu a toutefois créé un lien `href="#numerique"` sans produire la section `id="numerique"`. La source valide apparaissait uniquement dans « L’essentiel », alors que cette section doit être absente avec moins de trois sources valides.

[Conversation de recette dans le Projet](https://assistant.numerique.gouv.fr/chat/0913097f-cef5-4367-823a-9d3e2c0bead4)

La V5.9 ajoute ces quatre garde-fous, une couverture de collecte observable et une transmission explicite de la paire d’index entre `CANON` et `RENDU`.

### Recettes V5.9 du 15 octobre 2026

La première recette V5.9 a produit douze candidats après dix requêtes couvrant les cinq rubriques et plus de cinq domaines. La validation a conservé six sources et exclu six dates hors fenêtre. `CANON` a chargé les six fragments, mais `RENDU` a recherché de nouveau le jeton d’index et s’est arrêté avec `A_COMPLETER`.

[Première conversation V5.9](https://assistant.numerique.gouv.fr/chat/ac926e61-2b8a-4d4e-bfc3-e5b8e0b5de82)

Après correction et réinstallation, une seconde recette a produit onze candidats, quatre sources valides et sept exclusions. Une erreur technique pendant `CANON` a été relancée une seule fois avec le bouton natif `Réessayer`. La réponse suivante a confirmé `SNUM_CANON_V59_INDEX_START / SNUM_CANON_V59_INDEX_END` et les six paires de fragments. `RENDU` n’a plus recherché le jeton, mais a répondu `A_COMPLETER` sans HTML.

[Conversation V5.9 finale](https://assistant.numerique.gouv.fr/chat/68369f19-beff-4a6d-a3d6-80903fdacc60)

## Contrôles locaux

- prompt système mesuré à 3 740 caractères, sous la limite de 4 000 caractères ;
- fragments recomposés et comparés au canon source ;
- contenu exact du ZIP contrôlé ;
- scripts Python compilés ;
- dix-huit tests unitaires réussis, dont les régressions de collecte, de dates, de navigation et de transmission du canon ;
- contrôle d’accents exécuté sur les Markdown modifiés ;
- `git diff --check` exécuté ;
- aucun audit RGAA complet réalisé.

Le ZIP final porte l’empreinte SHA-256 `8cda46828aa4ea249d359f3609175b4651573c56dec886e6168b6918d21f7ca4`.

## Limite et décision

La contrainte technique n’est plus la taille du prompt. La limite restante est comportementale : la recherche documentaire peut retrouver un fragment, mais la génération ne garantit ni sa conservation exacte dans le contexte ni sa copie littérale.

Sans outil déterministe externe à l’Assistant, l’identité HTML avec Bacoco ne peut pas être promise. Le métier peut utiliser la recette progressive pour préparer et contrôler une édition, mais doit conserver `A_COMPLETER` tant qu’un contrôle extérieur n’a pas validé le HTML.

## Preuves

- [notice et pas à pas](./NOTICE-V5.9.md) ;
- [compte rendu V5.9](./_documentation/installation-v5.9-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [compte rendu progressif](./_documentation/validation-v5.8-progressive-2026-10-14/RESULTAT-RECETTE-PROGRESSIVE.md) ;
- [source canonique](./05-BLOCS-HTML-CANONIQUES.md) ;
- [rapport du test monobloc](./_documentation/validation-v5.8-monobloc-2026-10-14/RESULTAT-RECETTE-MONOBLOC.md).
