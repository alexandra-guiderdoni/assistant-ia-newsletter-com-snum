# Rapport de contrôle du kit SNUM V5.15

## Verdict

La V5.15 corrige les deux défauts ciblés de la V5.14 : les URL restent absolues avec `https://` et la phase `CANON` restitue les onze paires `START/END` attendues.

Le premier `RENDU` répond néanmoins `A_COMPLETER` avec le motif `CANON_MANQUANT`. Aucun HTML n’est affiché et aucun message `continue` n’a été envoyé.

Verdict : **NO-GO pour la production autonome**.

## Périmètre vérifié

- Projet Assistant DINUM : `Newsletter SNUM` ;
- prompt système V5.15 enregistré ;
- neuf ressources V5.15 indexées ;
- cinq phases exécutées dans une seule conversation vierge ;
- Web activé seulement pour `COLLECTE` ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun commit ni push pendant cette recette.

## Conversation de preuve

[Ouvrir la conversation V5.15](https://assistant.numerique.gouv.fr/chat/712d3864-0310-488d-9256-9c44a054b4bc)

## Déroulé observé

### COLLECTE

La réponse annonce dix requêtes réparties sur les cinq rubriques, couvre cinq domaines, liste dix candidats et se termine par `COLLECTE_TERMINEE`.

Les URL des candidats commencent par `https://`. La première correction visée par la V5.15 est confirmée.

### VALIDATION

Cinq sources sont conservées et cinq sont exclues. L’égalité `5 + 5 = 10` est respectée et la réponse se termine par `VALIDATION_TERMINEE`.

### DONNEES

Cinq fiches complètes sont produites dans quatre rubriques. Les URL restent absolues, les dates longues sont en majuscules sans jour de semaine et exactement trois fiches portent `ESSENTIEL : OUI`.

La réponse se termine par `DONNEES_RENDU_PRETES`.

### CANON

La réponse commence par `CANON_HTML_PRET`, cite la paire `SNUM_CANON_V515_INDEX_START / SNUM_CANON_V515_INDEX_END`, puis restitue exactement les onze lignes attendues :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_FOOTER_START / SNUM_FOOTER_END` ;
- `SNUM_SHELL_CLOSE_START / SNUM_SHELL_CLOSE_END` ;
- `SNUM_ESSENTIALS_OPEN_START / SNUM_ESSENTIALS_OPEN_END` ;
- `SNUM_ESSENTIAL_CARD_START / SNUM_ESSENTIAL_CARD_END` ;
- `SNUM_ESSENTIALS_CLOSE_START / SNUM_ESSENTIALS_CLOSE_END` ;
- `SNUM_RUBRIC_OPEN_START / SNUM_RUBRIC_OPEN_END` ;
- `SNUM_RUBRIC_ARTICLE_START / SNUM_RUBRIC_ARTICLE_END` ;
- `SNUM_RUBRIC_CLOSE_START / SNUM_RUBRIC_CLOSE_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

La seconde correction visée par la V5.15 est confirmée.

### RENDU

Le premier et unique passage répond :

```text
A_COMPLETER
## CONTROLES_EN_ECHEC
CANON_MANQUANT
```

Aucun HTML n’est affiché, conformément au garde-fou. Le motif ne respecte toutefois pas le format `CODE | détail` demandé par le message `RENDU`.

## Cause établie et limite

La trace établit une contradiction : la phase précédente prouve les onze paires et répond `CANON_HTML_PRET`, puis `RENDU` déclare immédiatement `CANON_MANQUANT` après avoir demandé le rechargement des fragments.

Elle ne permet pas d’établir le mécanisme interne exact de cet échec. L’inférence la plus prudente est que la récupération des fragments au nouveau tour reste non déterministe ou insuffisante. Une réponse `CANON_HTML_PRET` ne garantit donc pas que le tour suivant puisse réutiliser le canon.

## Preuves visuelles

Les captures de la phase `DONNEES`, des onze paires `CANON` et de l’arrêt `A_COMPLETER` ont été produites pendant la recette navigateur. Elles sont visibles dans la trace de session. La preuve durable et partageable reste la conversation liée ci-dessus ; aucune capture binaire n’a été ajoutée au dépôt pendant ce passage.

## Décision

Conserver V5.15 comme preuve que les URL absolues et le contrôle littéral des onze paires sont corrigés, mais ne pas la livrer comme version métier autonome.

La correction suivante devra éviter la dépendance entre deux tours pour le canon, par exemple en fusionnant le chargement du canon et la production du rendu dans un même message, puis en validant ce nouveau contrat dans une conversation vierge.

## PDG pass

- Déclenchement : oui, car ce rapport change le verdict durable de la version courante.
- Compétence lue : `progressive-disclosure-guard`. Une simple note dans le chat ne suffit pas, car le README pilote l’installation métier.
- Artefacts inspectés : conversation V5.15, README, notice V5.15, rapport et résultat V5.14, tests du kit, contrôle du générateur et contenu du ZIP V5.15.
- Chevauchement : `étendre` le README, la notice et la série de rapports existants ; `éviter` tout second mode opératoire.
- Matrice de preuve : « URL absolues préservées » est confirmé par `COLLECTE` et `DONNEES` ; « onze paires exactes » est confirmé par `CANON` ; « production autonome » est rejeté par le premier `RENDU` ; « cause interne exacte » reste inconnue.
- Fichiers matériels non relus ligne à ligne pendant ce passage : fragments 06 à 10. Leur présence et leur emballage sont contrôlés par les tests et le ZIP, mais leur fidélité visuelle complète au dépôt Bacoco n’est pas démontrée par cette recette sans HTML.
- Connu : le rendu s’arrête sans HTML avec `CANON_MANQUANT`.
- Inconnu connu : `CANON_HTML_PRET` décrit la réponse d’un tour, pas la disponibilité garantie des fragments au tour suivant.
- Inconnu : le mécanisme interne précis de perte ou de non-rechargement du canon et le comportement d’une autre exécution non déterministe.
- Mauvais chemin : envoyer `continue` et présenter une reprise comme un premier passage réussi.
- Garde-fou ajouté : le README et la notice affichent `NO-GO` avant les étapes d’installation.
- Comportement à préserver : arrêt sans HTML dès qu’un contrôle final échoue.
- Raccourcis interdits : publier, diffuser, copier un HTML absent ou interpréter `CANON_HTML_PRET` comme une réussite finale.
- Preuve de régression requise : conversation vierge, séquence documentée sans correction, puis HTML complet dès le premier rendu.
- Revue : auto-contrôle PDG, pas une revue indépendante.
