# Étude : faire tourner Veille SNUM sur GitHub

État : **publication du paquet en service** ; sélection dans l'atelier à construire. Date : 13 novembre 2026.
Complète la décision de portée 1 de [veille-snum.md](veille-snum.md) (serveur Python local).

## Besoin

Les collègues qui préparent la revue de presse n'ont pas Python sur leur poste. Ils doivent pouvoir utiliser Veille SNUM avec un simple navigateur, comme l'Atelier de courriels DSFR publié sur GitHub Pages.

## Pourquoi une page seule ne suffit pas

Une page publiée sur GitHub Pages, ou ouverte en fichier, ne peut ni lire les sources ni appeler Albert. Mesures du 13 novembre 2026 depuis le Mac Studio, avec une origine de test neutre :

- Albert (`/v1/chat/completions`) refuse la requête préalable d'un navigateur : HTTP 405, sans `Access-Control-Allow-Origin`.
- numerique.gouv.fr répond HTTP 200, mais sans `Access-Control-Allow-Origin` : le navigateur bloque la lecture.
- economie.gouv.fr répond HTTP 403.

S'y ajoute un risque propre à GitHub Pages : toutes les pages du compte partagent l'origine `alexandra-guiderdoni.github.io`. Un jeton mémorisé dans le navigateur y serait lisible par les scripts de l'atelier et des autres pages.

## Architecture proposée

1. **GitHub Actions** lance la collecte Python, résumés Albert compris, selon un calendrier ou à la main. Le jeton est le secret `ALBERT_API_KEY` du dépôt : aucun collègue n'en a besoin.
2. La tâche **publie le paquet V519** de la semaine.
3. Une **page statique** sur GitHub Pages affiche le paquet : cocher, changer de thématique, télécharger.
4. La **page SNUM de l'atelier** (`builder-mail-dsfr/app/distribution/snum.html`) convertit le paquet en composition, puis l'atelier l'importe. Ce parcours ne change pas.

## Preuves

Tâche `.github/workflows/test-acces-albert-github.yml`, branche `config/test-albert-github`.

1. **Albert joignable depuis GitHub** ([run 43504729773](https://github.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/actions/runs/43504729773)) : sans jeton, `GET /v1/models` et `POST /v1/chat/completions` répondent HTTP 401 en moins d'une demi-seconde. Pages d'accueil des sources : 11 sur 13 en HTTP 200, economie et legifrance en HTTP 403, comme depuis le Mac.
2. **Collecte complète identique au Mac** ([run 43505069961](https://github.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/actions/runs/43505069961)) : période du 6 au 13 novembre 2026, sans Albert, statut `needs_albert` attendu, en 175 s.
   - GitHub : 147/148 pages reçues, 45 candidats, 1 source sans réserve, 8 partielles, 9 298 adresses non visitées, 0 erreur de plan de site.
   - Mac, collecte du même soir à 21 h 29 : 147/148, 45, 1, 8, 9 297, 0.
   - Sources bloquées sur GitHub : Ministères économiques et financiers, Vie publique, Légifrance, Le Monde. Les totaux du Mac étant identiques, elles l'étaient très probablement aussi en local ; la comparaison source par source n'a pas été faite.
3. **Appel Albert authentifié** ([run 43506200123](https://github.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/actions/runs/43506200123)) : premier candidat DINUM de la période, « Achats publics : un premier guide pratique pour accompagner les administrations dans leurs achats d'IA ». Modèle `openweight-large`, réponse validée par `validate_summary` à la première tentative, en 11,8 s, thématique `commande`. Reproduit au [run 43506702724](https://github.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/actions/runs/43506702724) : 12,1 s, première tentative.

Témoins négatifs exécutés en local avant l'envoi : sans secret, la tâche s'arrête sur « secret ALBERT_API_KEY absent » ; avec un jeton factice, Albert répond HTTP 401.

## Limites de ces preuves

- Deux appels Albert seulement ont été faits depuis GitHub, sur le même candidat. Les quotas et le débit sur 45 candidats, environ cinq minutes en local, n'y sont pas mesurés.
- Une seule collecte complète a tourné sur GitHub. Un site peut filtrer plus tard les adresses de GitHub.
- GitHub a exécuté Python 3.14.4, le Mac Python 3.12. La version définitive doit fixer la version de Python.

## Décisions du 13 novembre 2026

- **Paquet public sur GitHub Pages**, choisi en connaissance de deux points : une page Pages reste publique même depuis un dépôt privé, et le point 7 de [veille-snum.md](veille-snum.md) demande une revue des droits de réutilisation avant diffusion institutionnelle.
- **Sélection dans la page SNUM de l'atelier**, plutôt qu'une page autonome : une page de moins pour les collègues.

## Publication en service

- Tâche « Publier le paquet Veille SNUM » (`.github/workflows/publier-paquet-snum.yml`, PR #15) : lancement à la main depuis l'onglet Actions, dates facultatives ; script `veille_snum/publier.py`.
- Adresse : https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/paquet-v519.json, servie avec `Access-Control-Allow-Origin: *` et un cache de dix minutes.
- Premier paquet ([run 43511462193](https://github.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/actions/runs/43511462193)) : 29 articles sur 45 candidats, aucun échec Albert, aucune trace de jeton.
- Un paquet ni complet ni partiel n'est pas publié : le précédent reste en ligne.

## Décisions restantes

- **Calendrier.** La tâche ne part qu'à la main ; un lancement planifié demande de fixer le jour et l'heure de l'édition.
- **Gestes à la demande.** Une collecte sur d'autres dates, ou le repêchage d'un candidat, passerait par un déclenchement manuel : quelques minutes d'attente, et un compte ayant les droits sur le dépôt.
- **Sécurité (issue #6).** Le secret `ALBERT_API_KEY` est enregistré dans le dépôt depuis le 13 novembre 2026, 20 h 56 UTC. Toute tâche poussée par une personne ayant les droits d'écriture peut l'utiliser. Le retirer : `gh secret delete ALBERT_API_KEY -R alexandra-guiderdoni/assistant-ia-newsletter-com-snum`.

## Travail restant

1. Page SNUM de l'atelier : charger le paquet publié, afficher la sélection (deux articles cochés par thématique), puis convertir.
2. Réécriture en JavaScript de la reconstruction du paquet après sélection, aujourd'hui côté serveur (`/api/packet`, `rebuild_packet`).
3. Repêchage (`/api/summarize`) remplacé par un déclenchement manuel, ou abandonné.
4. Retrait de la tâche de test et archivage de la branche `config/test-albert-github`.

## Suite au 14 novembre 2026

Les sections « Décisions restantes » et « Travail restant » ci-dessus décrivent l'état du 13 novembre. Depuis :

- **Sélection** : faite dans une page autonome du dépôt, publiée avec le paquet (`pages/`), et non dans la page SNUM de l'atelier. La reconstruction du paquet après sélection est en JavaScript (`pages/selection.js`).
- **Repêchage** : conservé, par la tâche « Repêcher un candidat Veille SNUM », lancée depuis la page.
- **Collecte en deux temps** : les titres d'abord, sans Albert, puis les résumés des seuls titres gardés. La collecte complète en une fois reste possible.
- **Archives** : chaque collecte résumée est archivée sur la branche `donnees-veille`, avant sa publication.
- **Lancement** : depuis la page, avec un jeton GitHub partagé par l'équipe ([jeton-github.md](../jeton-github.md)). Toujours pas de calendrier : la tâche ne part qu'à la demande.
- **Tâche de test** `test-acces-albert-github.yml` : conservée dans `main`, lancement manuel seulement ; la branche `config/test-albert-github` est supprimée.
- **Sécurité** : le secret `ALBERT_API_KEY` reste dans le dépôt ; le point de l'issue #6 est inchangé.

Mode d'emploi : section « Sans Python » du [README](../../README.md). État et reste à faire : [reprise-session.md](../../reprise-session.md).
