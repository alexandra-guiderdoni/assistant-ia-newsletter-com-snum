# Reprise de session Veille SNUM

État au 13 novembre 2026. Prototype expérimental (`COLLECTOR_VERSION="6.0-experimental"`), non validé pour une vraie clé ministérielle.

## État Git

- Tout est dans `main` du dépôt public `assistant-ia-newsletter-com-snum`, sans changement local en attente. `main` est la seule branche, en local comme sur GitHub ; les branches fusionnées ont été supprimées.
- PR fusionnées :

  | PR | Contenu |
  | --- | --- |
  | #1 | 14 domaines prioritaires de la Collecte, tri des articles par date |
  | #2 | prototype Veille SNUM |
  | #3 | description du prototype dans le README racine |
  | #4 | mesures du prototype dans `_documentation/recette-collecte-domaines/RAPPORT.md` |
  | #5 | actualisation de ce fichier de reprise |

- Reprendre : `git switch main && git pull`, puis créer une nouvelle branche pour la suite des travaux.

## Reprendre depuis l'autre Mac

- Le code vient de GitHub : `git pull` suffit.
- L'historique de la conversation reste sur le Mac d'origine (`~/.claude/projects/`) : `claude --continue` ne le retrouve pas. Ouvrir une nouvelle session et lui faire lire ce fichier.
- Le fichier `~/Claude/projets-heberges/starter-kit-chatbox/.env`, qui contient la clé Albert, n'est pas dans Git : il doit exister sur ce Mac pour lancer une collecte avec résumés.

## Lancer l'application

Port **8766**, car le 8765 est capturé par le service worker de l'« Atelier de courriels DSFR ». La clé Albert est chargée par l'utilisateur dans son terminal, jamais par l'agent :

```bash
cd ~/Claude/git-hors-workflow/assistant-ia-newsletter-com-snum/veille-snum-webapp-v5-apres-egm/veille-snum
# exporter ALBERT_API_KEY depuis ~/Claude/projets-heberges/starter-kit-chatbox/.env, puis :
export ALBERT_MODEL=openweight-large SNUM_PORT=8766
python3 -m veille_snum.web
```

Redémarrer après toute modification : Ctrl + C, flèche haut, Entrée.

## Tests

```bash
python3 -m unittest discover -s tests     # 122 tests, OK
node --test tests/test_storage.cjs        # 16 tests, OK
```

## Fait

- Collecte : 15 articles par site, 60 au total, budget de 180 s pour la découverte et de 360 s pour Albert, 2 appels Albert en parallèle (4 provoquaient des HTTP 429), sites anti-robots signalés.
- Contrôle des résumés : détection de l'anglais champ par champ, suppression des tirets cadratins.
- Sélection éditoriale : garder ou écarter, changer de thématique, repêcher un candidat, revalider le paquet avant téléchargement.
- Interface réécrite avec les composants DSFR 1.15.4 embarqués hors ligne (`veille_snum/dsfr/`, `MANIFEST.json`), avec une CSP stricte.
- Grille et espacements vérifiés dans Chrome à 1280 px et à 606 px (statistiques sur 3 puis 2 colonnes, pas de défilement horizontal).
- Paquets réels validés par `newsletter_mail.py verify` (`HTML_MAIL_DSFR_CANONIQUE_OK`).
- Veille SNUM décrit dans le README racine et dans `_documentation/recette-collecte-domaines/RAPPORT.md`.

## Reste à faire

1. Redémarrer le serveur 8766 et repasser la page au validateur W3C : l'erreur `class="stats"` venait de l'ancien code encore servi.
2. Non vérifié : téléphone réel (375 px), zoom à 200 %, contrastes, mode sombre, lecteur d'écran réel.
3. Les résumés Albert restent à relire : un résumé réel indiquait « 11 M$ » au lieu de 11 milliards.
4. Le README du prototype indique encore `http://127.0.0.1:8765/` pour le lancement en ligne de commande, alors que le lanceur `.command` utilise le 8766.
5. Hébergement sur GitHub pour des collègues sans Python : paquet publié sur GitHub Pages depuis le 13 novembre 2026 (tâche « Publier le paquet Veille SNUM ») ; reste la sélection dans la page SNUM de l'atelier. Voir [docs/designs/hebergement-github.md](docs/designs/hebergement-github.md). Le secret `ALBERT_API_KEY` est enregistré dans le dépôt.

## Ne pas oublier

- Ne pas faire écrire, lire ni charger la clé Albert par l'agent.
- Aucun tiret cadratin, ni dans le produit ni dans les réponses.
- Ne pas parler de conformité DSFR ou RGAA sans audit. Formulation autorisée : « composants DSFR utilisés selon les sources lues ».
