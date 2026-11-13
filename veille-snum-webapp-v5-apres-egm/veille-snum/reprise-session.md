# Reprise de session Veille SNUM

État au 13 novembre 2026. Prototype expérimental (`COLLECTOR_VERSION="6.0-experimental"`), non validé pour une vraie clé ministérielle.

## État Git

- Le prototype est dans `main` du dépôt public `assistant-ia-newsletter-com-snum`, fusionné par la PR #2 depuis la branche `feature/prototype-veille-snum`.
- Reprendre : `git switch main && git pull`, puis créer une nouvelle branche pour la suite des travaux.
- La branche `feat/collecte-domaines-prioritaires`, fusionnée par la PR #1, a été supprimée en local et sur GitHub.

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

## Ne pas oublier

- Ne pas faire écrire, lire ni charger la clé Albert par l'agent.
- Aucun tiret cadratin, ni dans le produit ni dans les réponses.
- Ne pas parler de conformité DSFR ou RGAA sans audit. Formulation autorisée : « composants DSFR utilisés selon les sources lues ».
