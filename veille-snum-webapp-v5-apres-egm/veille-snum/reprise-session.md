# Reprise de session Veille SNUM

État au 15 novembre 2026. Prototype expérimental (`COLLECTOR_VERSION="6.0-experimental"`).

## Où en est le prototype

Deux façons de s'en servir, à partir du même code :

- **En ligne, sans Python** : https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/. La collecte et Albert passent par GitHub Actions ; la page affiche les titres trouvés, la personne garde ceux à faire résumer, puis trie le paquet et exporte le JSON V519. C'est l'usage prévu pour l'équipe.
- **En local** : `python3 -m veille_snum.web`, pour travailler hors ligne ou sur le code.

Le mode d'emploi de la page est dans [README.md](README.md), section « Sans Python ». Le jeton GitHub partagé par l'équipe est décrit dans [docs/jeton-github.md](docs/jeton-github.md).

## Chaîne complète de la revue de presse

1. Collecte et sélection : la page ci-dessus, qui exporte le paquet V519.
2. Conversion en courriel : https://alexandra-guiderdoni.github.io/builder-mail-dsfr/snum.html (dépôt `builder-mail-dsfr`).
3. Retouche et copie : https://alexandra-guiderdoni.github.io/builder-mail-dsfr/.

## Changements des 14 et 15 novembre

Veille SNUM (PR #39 et #40) :

- **Phase titres** : titres groupés par rubrique probable, d'après un mot-clé du titre (`pages/rubriques-probables.js`), puis « Rubrique non reconnue ». Indicatif : mesuré sur 245 titres réels de la revue, un mot-clé est reconnu pour 81 % des titres et la rubrique est alors juste pour 74 % d'entre eux.
- **Repêchage** : « Laisser Albert choisir » par défaut ; la valeur `albert` traverse la page, le workflow, `repecher.py` et l'appel à Albert.
- **Titre coché ou repêché** : jamais écarté comme hors thématique (`keep=True`) ; Albert choisit seulement la rubrique. Un refus malgré la consigne devient un échec repêchable.
- **Consigne d'Albert** : « en cas de doute, garder » ; cas ajoutés : agents publics, cybercriminalité, entreprises, régulation et enjeux géopolitiques de l'IA et du numérique.
- **Découverte** : 40 pages par source au lieu de 15 ; la visite des articles reçoit la part du temps restant entre les sources restantes.

Builder (PR #225 à #228) : modèle SNUM au format de la revue, identité réelle (en-tête, signature, trois liens mailto repris des envois de l'équipe), pied Marianne qui referme le cadre avec la mention et « Nous contacter », abonnements sous le cadre, aperçu à la hauteur du courriel sans défilement interne. Issues #223 et #224 fermées.

## État Git

- Tout est dans `main` des deux dépôts publics, sans changement local en attente, sauf ce fichier s'il n'a pas été commité.
- Veille SNUM : deux branches sur GitHub, `main` et `donnees-veille` (archives des collectes et résultats de repêchage). Ne pas supprimer `donnees-veille`.
- Builder : quatre branches locales déjà fusionnées par squash (`feature/modele-snum`, `fix/pied-snum-identite`, `fix/pied-snum-modele-valide`, `fix/pied-snum-marianne`). Leur suppression demande `git branch -D` : seulement avec l'accord d'Alex.
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
python3 -m unittest discover -s tests            # 253 tests
node --test tests/test_pages_*.cjs               # 90 tests de la page en ligne
node --test tests/test_storage.cjs               # 19 tests du stockage local
```

Parcours de bout en bout de la page dans Chromium, GitHub simulé et vrai code serveur : [tests/navigateur/](tests/navigateur/README.md) (90 vérifications, plus 10 scénarios de défauts). Playwright n'est pas une dépendance du dépôt : `PLAYWRIGHT=<dossier>/node_modules/playwright`.

## Vérifié sur le vrai service

Le 14 novembre 2026, chaque parcours a été joué une fois, depuis la vraie page, dans Chromium :

- premier temps : 43 titres, environ trois minutes ;
- second temps : 94 secondes pour 5 titres gardés ;
- repêchage : 42 secondes ;
- collecte complète : 7 minutes 46 secondes pour 43 candidats, 25 articles ;
- republication « page seule » : moins d'une minute.

Collecte complète du 14 novembre au soir, avant la PR #40 : 22 candidats, 5 articles dans 2 rubriques, 17 titres jugés hors thématique dont plusieurs pertinents ; 9 296 adresses repérées non analysées (plafond de 15 pages par source). C'est ce constat qui a motivé la PR #40. Repêchage « Laisser Albert choisir » vérifié sur le vrai service le même soir.

## Reste à faire

1. **Mesurer la PR #40 sur une vraie collecte** : nombre de titres, d'articles et de rubriques, durée de la collecte, part des titres en « Rubrique non reconnue » (11 sur 22 sur les titres bruts du 14 novembre).
2. Les résumés Albert sont publiés sur une page publique avant relecture : décision éditoriale à prendre. Un résumé réel indiquait « 11 M$ » au lieu de 11 milliards.
3. Quatre sources refusent les robots (Ministères économiques et financiers, Vie publique, Légifrance, Le Monde) : à couvrir autrement.
4. Builder : casse de l'en-tête à trancher (le courriel d'origine écrit « SERVICE DU NUMÉRIQUE (SNUM) » et « REVUE DE PRESSE » en capitales) ; rendu dans Mélissa après collage non vérifié.
5. Audit RGAA avec décisions humaines et lecteur d'écran réel ; essais dans Firefox et Safari. Le pied de page affiche « Accessibilité : non conforme ».
6. Déclaration d'accessibilité et mentions légales, avant tout usage institutionnel.
7. Les cas d'échec (Albert en panne, archivage en échec, deux personnes en même temps) ne sont vérifiés qu'en simulation.
8. Renouveler le jeton partagé à son expiration ou au départ d'une personne de l'équipe.

## Ne pas oublier

- Ne pas faire écrire, lire ni charger la clé Albert par l'agent.
- Aucun tiret cadratin, ni dans le produit ni dans les réponses.
- Ne pas parler de conformité DSFR ou RGAA sans audit.
- Les dépôts sont publics : aucun contenu des envois internes de l'équipe, aucune adresse personnelle.
- `veille_snum/core.py` et `veille_snum/web.py` servent aussi le serveur local : toute modification touche les deux usages.
- Une page publiée peut rester en cache dix minutes : faire recharger avec Cmd + Maj + R avant de conclure à un défaut.
