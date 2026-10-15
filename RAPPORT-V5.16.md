# Rapport de contrôle du kit SNUM V5.16

## Verdict

La V5.16 fusionne le chargement du canon et la production du rendu dans un unique message `CANON_RENDU`. Le premier passage réel répond néanmoins `A_COMPLETER` avec deux diagnostics `CANON_MANQUANT`, l’un pour le marqueur de début de l’index V5.16 et l’autre pour son marqueur de fin.

Aucun HTML n’est affiché et aucun message `continue` n’a été envoyé.

Verdict : **NO-GO pour la production autonome**.

## Périmètre vérifié

- Projet Assistant DINUM : `Newsletter SNUM` ;
- prompt système V5.16 enregistré ;
- neuf ressources V5.16 visibles dans les paramètres du Projet ;
- quatre phases exécutées dans une seule conversation vierge ;
- Web activé seulement pour `COLLECTE` ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel.

## Conversation de preuve

[Ouvrir la conversation V5.16](https://assistant.numerique.gouv.fr/chat/4767347f-c1cd-442d-a3e7-f7f55628311f)

## Déroulé observé

### COLLECTE

La réponse couvre les cinq rubriques avec dix requêtes, liste dix candidats et se termine par `COLLECTE_TERMINEE`.

### VALIDATION

Trois sources sont conservées et sept sont exclues. L’égalité `3 + 7 = 10` est respectée et la réponse se termine par `VALIDATION_TERMINEE`.

### DONNEES

Trois fiches complètes sont produites dans deux rubriques. Les dates longues sont en majuscules sans jour de semaine et les trois fiches portent `ESSENTIEL : OUI`.

La réponse se termine par `DONNEES_RENDU_PRETES`.

### CANON_RENDU

Le premier et unique passage répond :

```text
A_COMPLETER
## CONTROLES_EN_ECHEC
CANON_MANQUANT | SNUM_CANON_V516_INDEX_START
CANON_MANQUANT | SNUM_CANON_V516_INDEX_END
```

Aucun HTML n’est affiché, conformément au garde-fou.

## Cause établie et limites

La trace établit que le tour fusionné ne retrouve pas les deux marqueurs de `05-INDEX-HTML.md` dans cette recette, alors que les neuf ressources V5.16 sont visibles dans les paramètres du Projet.

Le mécanisme interne exact n’est pas observable. Il est donc impossible de conclure si l’échec vient du délai d’indexation, du classement des ressources ou de la recherche effectuée par le modèle. La fusion `CANON_RENDU` élimine la dépendance entre deux tours, mais ne garantit pas la récupération initiale de l’index.

## RETEX

### Ce qui fonctionne

- l’installation du prompt système et des neuf ressources est visible dans le Projet ;
- la collecte respecte les dix requêtes et les cinq rubriques ;
- la validation conserve trois sources et justifie sept exclusions ;
- les trois fiches de rendu sont complètes et les dates n’inventent aucun jour de semaine ;
- le garde-fou bloque correctement la livraison d’un HTML dont le canon n’a pas été retrouvé.

### Ce qui ne fonctionne pas

Le Projet monolithique doit simultanément conserver les données éditoriales de trois phases et récupérer plusieurs ressources canoniques au moment du rendu. La V5.16 élimine le passage d’état entre `CANON` et `RENDU`, mais elle ne rend pas la récupération documentaire déterministe. Le HTML complet reste donc indisponible au premier passage.

### Pourquoi les itérations n’ont pas suffi

Les versions V5.13 à V5.16 ont corrigé successivement les dates, les essentiels, les URL absolues, les diagnostics, les paires canoniques et la dépendance entre deux tours. Chaque correction est vérifiable, mais aucune règle de prompt ne peut garantir que l’Assistant charge un fichier précis depuis les ressources du Projet. Le défaut restant relève de l’architecture du flux, pas d’une consigne éditoriale manquante.

### Enseignement

La collecte et le rendu HTML doivent être découplés. Le premier Projet doit produire un paquet de données stable sans HTML. Le second Projet doit recevoir ce paquet et n’avoir qu’une responsabilité : l’injecter dans un gabarit canonique unique, sans Web ni recherche éditoriale.

## Preuves visuelles

Une capture de l’arrêt `A_COMPLETER` a été produite pendant la recette navigateur. La conversation liée ci-dessus constitue la preuve durable et partageable ; aucune image binaire n’est ajoutée au dépôt.

## Décision

Conserver V5.16 comme preuve du test de la fusion `CANON_RENDU`, mais ne pas la livrer comme version métier autonome.

Clore la piste du Projet monolithique. La prochaine version séparera `Newsletter SNUM - Collecte` et `Newsletter SNUM - Rendu HTML`. Le passage entre les deux Projets utilisera un bloc structuré `PAQUET_RENDU`. Toute nouvelle solution devra être validée dans deux conversations vierges, sans `continue` ni correction intermédiaire, puis produire un HTML complet au premier rendu.

## Limites de la preuve

- un seul scénario réel V5.16 exécuté ;
- aucune sortie HTML à comparer au canon Bacoco ;
- aucun audit RGAA complet ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun mécanisme interne d’indexation observable dans l’interface.

## PDG pass

- Déclenchement : oui, car le RETEX fixe une décision d’architecture et prépare un nouveau mode opératoire métier.
- Compétence : `progressive-disclosure-guard`, utilisée après lecture du rapport, du README, de la notice, du prompt système, de l’index canonique, des jetons des fragments, du générateur et des tests.
- Deuxième contrôle d’utilité : une simple conclusion dans le chat ne suffit pas, car le dépôt est la source de vérité transmise aux collègues.
- Chevauchement : `étendre` le rapport V5.16 existant ; `éviter` un second document de RETEX concurrent.
- Affirmation « les phases éditoriales réussissent » : confirmée par la conversation réelle et le résultat d’installation ; impact : leur contrat peut être conservé dans le futur Projet de collecte.
- Affirmation « la fusion garantit le canon » : rejetée par les deux diagnostics `CANON_MANQUANT` ; impact : le Projet monolithique reste `NO-GO`.
- Affirmation « la cause interne exacte est connue » : inconnue, car l’indexation et le classement des ressources ne sont pas observables ; impact : aucune correction de prompt ne doit être présentée comme certaine sans recette réelle.
- Fichiers matériels non relus intégralement pendant ce passage : aucun fichier utilisé pour le verdict. La fidélité visuelle du HTML reste inconnue puisqu’aucun HTML n’a été produit.
- Connu : le garde-fou arrête le rendu sans HTML lorsque les marqueurs d’index manquent.
- Inconnu connu : la présence visible d’une ressource dans le Projet ne garantit pas sa récupération dans un tour donné.
- Inconnu : le comportement d’une autre exécution non déterministe du même kit.
- Mauvais chemin : poursuivre les micro-corrections du prompt monolithique ou envoyer `continue` après l’arrêt.
- Garde-fou : la V5.16 reste explicitement `NO-GO` dans le README, la notice et le rapport.
- Comportement à préserver : collecte vérifiable, dates bornées, URL absolues et arrêt sans HTML en cas d’échec.
- Raccourcis interdits : déclarer la version autonome, copier un HTML absent ou attribuer l’échec à une cause interne non observable.
- Preuve de régression requise : recette réelle dans deux Projets vierges, transfert du `PAQUET_RENDU`, HTML complet au premier rendu et comparaison au canon.
- Revue : auto-contrôle PDG, pas une revue indépendante.
