# Rapport de contrôle du kit SNUM V5.12

## Verdict

La V5.12 assemble désormais un HTML complet à partir des fragments canoniques. La recette réelle du 15 octobre 2026 a abouti à `État : PRODUITE - contrôle métier requis`.

Le livrable n'est toutefois pas validé pour une production autonome au premier passage. Un message manuel `continue` puis un second envoi de `RENDU` ont été nécessaires. Surtout, les dates ISO correctes ont été transformées en dates longues avec des jours de semaine faux.

Verdict : **NO-GO pour la livraison métier autonome en l'état**. Le mécanisme d'assemblage HTML est démontré après reprise, mais la chaîne éditoriale doit encore fiabiliser les dates longues et supprimer la reprise manuelle.

## Périmètre vérifié

- Projet Assistant DINUM : `Newsletter SNUM` ;
- prompt système V5.12 installé ;
- neuf ressources V5.12 indexées ;
- une seule conversation utilisée pour les cinq phases ;
- aucune publication GitHub Pages ni diffusion par courriel ;
- aucune suppression de projet ou de conversation.

## Recette réelle

[Conversation V5.12](https://assistant.numerique.gouv.fr/chat/f9064cda-77f1-4dfe-b4e6-2da38e09eb72/)

### 1. COLLECTE avec le Web

La réponse a annoncé dix requêtes, les cinq rubriques, au moins cinq domaines et dix candidats. Elle s'est terminée par `COLLECTE_TERMINEE`.

### 2. VALIDATION sans le Web

La réponse a conservé six sources et en a exclu quatre. L'égalité `6 + 4 = 10` est respectée et la réponse s'est terminée par `VALIDATION_TERMINEE`.

### 3. DONNEES sans le Web

La réponse a produit six fiches, désigné trois essentiels et s'est terminée par `DONNEES_RENDU_PRETES`.

Cette phase a introduit l'anomalie principale : les jours de semaine ne correspondent pas aux dates ISO. Par exemple, le 14 octobre 2026 est un mercredi, pas un lundi ; le 12 octobre 2026 est un lundi, pas un mardi ni un samedi.

### 4. CANON sans le Web

La réponse a annoncé `CANON_HTML_PRET`, la paire d'index V5.12 et les onze paires de fragments attendues.

### 5. RENDU sans le Web

Le premier rendu n'a pas terminé dans un délai raisonnable. Un message manuel `continue` a provoqué une nouvelle réponse `CANON_HTML_PRET`. Le prompt `RENDU` a donc été renvoyé.

Le second rendu a produit, dans l'ordre :

- `## REVUE` ;
- `## HTML COMPLET` avec un bloc commençant par `<!doctype html>` ;
- `## DOSSIER PRIVÉ` ;
- `État : PRODUITE - contrôle métier requis`.

L'arbre d'accessibilité de la page a permis d'observer le titre, la feuille de style canonique, les accès rapides, le menu, les trois cartes essentielles, les six articles, le pied de page, la modale de thème et les scripts DSFR 1.15.2. La copie automatique du bloc complet n'a pas alimenté le presse-papiers ; aucune comparaison octet par octet de cette sortie n'est donc revendiquée.

## Anomalies bloquantes

### Reprise manuelle

La recette n'est pas autonome au premier passage : elle nécessite `continue` puis un nouveau `RENDU`.

### Jours de semaine faux

Les correspondances calendaires vérifiées localement sont :

- 5 octobre 2026 : lundi ;
- 7 octobre 2026 : mercredi ;
- 11 octobre 2026 : dimanche ;
- 12 octobre 2026 : lundi ;
- 13 octobre 2026 : mardi ;
- 14 octobre 2026 : mercredi.

La sortie de l'Assistant attribue d'autres jours à ces dates. Le contrôle du format et des bornes ISO ne protège donc pas la date longue générée ensuite.

## Décision de correction

La correction minimale suivante doit être testée dans une version ultérieure :

1. transmettre les dates longues exactes dans le prompt utilisateur ou les données validées ;
2. interdire à `DONNEES` de calculer ou d'inventer un jour de semaine ;
3. ajouter un contrôle bloquant entre date ISO et date longue ;
4. considérer toute reprise manuelle du rendu comme un échec de l'autonomie au premier passage.

La V5.12 reste archivée comme preuve de l'amélioration de l'assemblage HTML, pas comme version métier autonome validée.

## Contrôles locaux

Les contrôles exécutés après la recette donnent :

- `python3 scripts/build_progressive_kit.py --check` : `KIT_PROGRESSIF_OK` ;
- `python3 -m unittest discover -s tests -v` : 23 tests réussis ;
- prompt système : 3 969 caractères, sous la limite de 4 000 ;
- bloc du prompt système dans le README : identique au fichier source ;
- `git diff --check` : aucune erreur ;
- ZIP V5.12 : SHA-256 `97880a8c29431cb29f908d5d41d5f982443540d32b2320fadf9c9cc357e17e7e`.

Ces contrôles couvrent le kit, les fragments, le ZIP et les tests déterministes. Ils ne prouvent ni le contenu des sources Web, ni l'identité octet par octet du HTML visible dans l'Assistant, ni la conformité RGAA complète.

## Preuves

- [notice V5.12](./NOTICE-V5.12.md) ;
- [compte rendu d'installation et de recette](./_documentation/installation-v5.12-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md) ;
- [prompt système V5.12](./PROMPT-SYSTEME-SNUM-V5.12.md) ;
- [source canonique](./05-BLOCS-HTML-CANONIQUES.md).
