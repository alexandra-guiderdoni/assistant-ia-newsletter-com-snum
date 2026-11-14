# Audit du 14 novembre 2026 : collecte en deux temps

Trois contrôles menés sur la collecte en deux temps après sa fusion (PR 22), puis sur ses corrections (PR 23).

## Fichiers

- `audit-results.json` : audit de code, 41 constats (0 critique, 0 élevé, 11 moyens, 30 faibles). Audité sur le commit `01e42cb`.
- `logic-report.md` et `logic-results.json` : contrôle de logique de trois procédures (lancement sur la page, second temps côté serveur, tâches GitHub). 63 obligations, 6 défauts confirmés, 10 risques, 4 conflits de contrat, 18 questions, 13 zones non couvertes. Analysé sur `d708965`.
- `process-report.md` et `process-results.json` : comparaison avant/après, `dbabaa5` vers `a13adfa`. Aucune nouvelle erreur ; le repêchage est inchangé.

Les rapports décrivent l'état du code à ces commits. Les chemins locaux ont été retirés.

## Ce qui a été corrigé depuis

- PR 23 : les 11 constats moyens réparables et les 6 défauts de logique confirmés.
- PR suivante : les constats faibles réparables sans arbitrage (données inattendues, messages techniques, refus sans trace Python, index d'archives illisible, résultat de repli du repêchage).

## Vérifié sur le vrai service le 14 novembre 2026

- Premier temps : 43 titres trouvés, environ trois minutes.
- Republication « page seule » : site à jour 25 secondes après la fin de la tâche.
- Second temps lancé depuis la page : 94 secondes pour 5 titres gardés, 3 articles publiés, 2 jugés hors thématique, archivage avant déploiement, champ `titres_started_at` présent dans l'archive.

## Restent ouverts, par choix

- Texte de pages tierces résumé par Albert puis publié sans relecture préalable : décision éditoriale. La page demande de vérifier chaque source avant diffusion.
- Après confirmation du numéro de run, rapport, paquet et candidats écartés sont relus sans contrôle croisé de version.
- Une page restée ouverte sur d'anciens titres peut demander leur rédaction si le cache du site sert encore leur rapport ; la page relit l'état avant l'envoi, le serveur n'a pas d'autre moyen de le savoir.
- « Page seule » lancée juste après une publication peut republier d'anciens fichiers si le cache du site les sert encore.
- Repêchage : la tâche reste verte quand le script échoue (le refus doit pouvoir être publié) ; son jeton d'écriture couvre tout le dépôt ; au-delà de dix minutes, aucun résultat n'est publié.
- Groupe de concurrence `pages` : GitHub ne garde qu'une demande en attente et annule la précédente. La page prévient avant tout second envoi.
- Appel Albert du second temps : délai fixe de 30 secondes, non réduit au temps restant.
- Balises `og` et `canonical` absentes : sans objet pour un outil interne.
- Accessibilité : aucun audit n'a été réalisé ; le pied de page le dit.
