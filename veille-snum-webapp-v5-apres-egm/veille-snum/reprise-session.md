# Reprise de session Veille SNUM

État au 14 novembre 2026. Prototype expérimental (`COLLECTOR_VERSION="6.0-experimental"`).

## Où en est le prototype

Deux façons de s'en servir, à partir du même code :

- **En ligne, sans Python** : https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/. La collecte et Albert passent par GitHub Actions ; la page affiche les titres trouvés, la personne garde ceux à faire résumer, puis trie le paquet et exporte le JSON V519. C'est l'usage prévu pour l'équipe.
- **En local** : `python3 -m veille_snum.web`, pour travailler hors ligne ou sur le code.

Le mode d'emploi de la page est dans [README.md](README.md), section « Sans Python ». Le jeton GitHub partagé par l'équipe est décrit dans [docs/jeton-github.md](docs/jeton-github.md).

## État Git

- Tout est dans `main` du dépôt public `assistant-ia-newsletter-com-snum`, sans changement local en attente.
- Deux branches seulement existent sur GitHub : `main`, et `donnees-veille`, qui porte les archives des collectes et les résultats de repêchage. Ne pas supprimer `donnees-veille`.
- Reprendre : `git switch main && git pull`, puis créer une branche pour la suite.

## Reprendre depuis l'autre Mac

- Le code vient de GitHub : `git pull` suffit.
- L'historique de la conversation reste sur le Mac d'origine (`~/.claude/projects/`) : ouvrir une nouvelle session et lui faire lire ce fichier.
- La clé Albert du serveur local n'est pas dans Git. Celle des tâches GitHub est le secret `ALBERT_API_KEY` du dépôt.

## Lancer l'application locale

Port **8766**, car le 8765 est capturé par le service worker de l'« Atelier de courriels DSFR ». La clé Albert est chargée par l'utilisateur dans son terminal, jamais par l'agent :

```bash
cd ~/Claude/git-hors-workflow/assistant-ia-newsletter-com-snum/veille-snum-webapp-v5-apres-egm/veille-snum
# exporter ALBERT_API_KEY, puis :
export SNUM_PORT=8766  # modèle par défaut : openweight-large
python3 -m veille_snum.web
```

## Tests

```bash
python3 -m unittest discover -s tests            # 229 tests
node --test tests/test_pages_*.cjs               # 76 tests de la page en ligne
node --test tests/test_storage.cjs               # 19 tests du stockage local
```

Parcours de bout en bout de la page dans Chromium, GitHub simulé et vrai code serveur : [tests/navigateur/](tests/navigateur/README.md) (89 vérifications, plus 10 scénarios de défauts). Playwright n'est pas une dépendance du dépôt.

## Vérifié sur le vrai service le 14 novembre 2026

Chaque parcours a été joué une fois, depuis la vraie page, dans Chromium :

- premier temps : 43 titres, environ trois minutes ;
- second temps : 94 secondes pour 5 titres gardés ;
- repêchage : 42 secondes ;
- collecte complète : 7 minutes 46 secondes pour 43 candidats, 25 articles ;
- republication « page seule » : moins d'une minute.

## Documents à lire avant de reprendre

- [docs/reviews/2026-11-14-audit-shipguard/](docs/reviews/2026-11-14-audit-shipguard/README.md) : audit de code, contrôle de logique, ce qui a été corrigé et ce qui reste ouvert par choix.
- [docs/reviews/2026-11-14-accessibilite/](docs/reviews/2026-11-14-accessibilite/README.md) : préaudit d'accessibilité et mesures ; ce n'est pas un audit RGAA.
- [docs/designs/hebergement-github.md](docs/designs/hebergement-github.md) : pourquoi GitHub Actions et GitHub Pages.

## Reste à faire

1. Les résumés Albert sont publiés sur une page publique avant relecture : décision éditoriale à prendre. Un résumé réel indiquait « 11 M$ » au lieu de 11 milliards.
2. Audit RGAA avec décisions humaines et lecteur d'écran réel ; essais dans Firefox et Safari. Le pied de page affiche « Accessibilité : non conforme ».
3. Déclaration d'accessibilité et mentions légales, avant tout usage institutionnel.
4. Les cas d'échec (Albert en panne, archivage en échec, deux personnes en même temps) ne sont vérifiés qu'en simulation.
5. Renouveler le jeton partagé à son expiration ou au départ d'une personne de l'équipe.

## Ne pas oublier

- Ne pas faire écrire, lire ni charger la clé Albert par l'agent.
- Aucun tiret cadratin, ni dans le produit ni dans les réponses.
- Ne pas parler de conformité DSFR ou RGAA sans audit.
- `veille_snum/core.py` et `veille_snum/web.py` servent aussi le serveur local : toute modification touche les deux usages.
