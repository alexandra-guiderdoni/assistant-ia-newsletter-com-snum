# Rapport de recette Newsletter SNUM V5.21

Date de recette : 16 octobre 2026.

## Verdict

**NO-GO.** Les contrôles locaux sont verts, mais la recette réelle s’arrête au premier
tour de Collecte. Avec le Web activé et `NUMERIQUE` dans le message initial,
l’Assistant exécute deux recherches et annonce 13 sources. Il ne transforme pourtant
aucune source en candidat et omet le marqueur terminal du lot.

La chaîne `COLLECTE → VALIDATION → PAQUET → RENDU` n’a donc pas été transmise au-delà
de ce premier échec terminal.

## Périmètre vérifié

- édition : 14 octobre 2026 ;
- période inclusive : du 3 octobre 2026 au 13 octobre 2026 ;
- projet modifié : `Newsletter SNUM - Collecte` ;
- projet préservé : `Newsletter SNUM - Rendu HTML` ;
- ressources Collecte visibles : méthode V5.21 et contrat V5.21 ;
- prompt Collecte persistant : 3 988 caractères dans le formulaire, soit la source de
  3 989 caractères avec son saut de ligne terminal.

## Preuves locales

- `python3 -m unittest discover -s tests -v` : 52 tests réussis ;
- `ruff check --no-cache scripts tests` : aucun écart ;
- `python3 scripts/build_split_kit.py --check` : `KIT_DECOUPLE_OK` ;
- `git diff --check` : aucun écart ;
- prompt système Collecte : 3 927 caractères, sous la limite de 4 000 ;
- ZIP Collecte régénéré depuis les trois fichiers V5.21.

Les tests de régression couvrent notamment : les trois lignes obligatoires du message
initial, deux appels Web avant le premier rendu, deux requêtes par lot de `PASSE_1`,
recomptage par URL et bornes, contrôle complet par candidat et analyse du JSON exact
avant `PAQUET_RENDU_PRET`.

## Preuve Assistant

Conversation terminale :
`https://assistant.numerique.gouv.fr/chat/72410fa6-7a0a-438f-9f0d-1c313dce2b77`

État observé avec le bouton `Rechercher sur le web` activé :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
NUMERIQUE

ETAT_COLLECTE
DATE_EDITION=2026-10-14
PERIODE=2026-10-03..2026-10-13
PASSE=1
RUBRIQUES_TERMINEES=
TRACE_RECHERCHE=REQUETE=NUMERIQUE après:2026-10-03 avant:2026-10-13
REQUETE=NUMERIQUE site:gouv.fr après:2026-10-03 avant:2026-10-13
CANDIDATS=
PROCHAINE_COMMANDE=IA
```

L’interface propose `Afficher 13 sources`, ce qui confirme l’exécution Web. La réponse
insère toutefois un premier `ETAT_COLLECTE` vide puis le préambule « Action requise »
avant cet état final. Elle ne contient aucun candidat et omet
`LOT_TERMINE=NUMERIQUE | PROCHAINE_COMMANDE=IA`.

Le parcours exige d’attendre ce marqueur avant `IA`. La chaîne est donc arrêtée au
premier échec terminal, sans masquer l’écart par une commande de poursuite.

## Non vérifié

Sur la configuration finale V5.21, les étapes `IA`, `COMMANDE`, `RH`, `BERCY`,
`RECOMPTER`, `VALIDER`, `GENERER_PAQUET` et `RENDU` ne sont pas vérifiées. Les franchir
aurait masqué l’échec du premier tour.

Un essai antérieur à cette configuration avait atteint `GENERER_PAQUET`, mais le JSON
était invalide à cause de guillemets internes non échappés. Cette preuve historique ne
valide pas la configuration finale.

## Suite recommandée, non exécutée

Réduire encore la sortie intermédiaire : une seule réponse après les appels Web,
contenant les candidats dérivés des sources et le marqueur terminal du lot. Toute
nouvelle correction devra conserver le contrat métier désormais vérifié : le premier
message contient `DATE_EDITION`, `PERIODE` et `NUMERIQUE`.
