# Première critique EGM : portée et limites

**Statut : revue analytique préparatoire, PAS une revue Goldfish indépendante.** Aucun sous-agent isolé n'a été exécuté ici. La revue doit être répétée avec `egm-review` dans un environnement offrant des sous-agents frais.

## Blocages et objections

- **Bloquant : fausse autonomie** : une page statique ne peut pas récupérer librement les HTML de sites tiers ni conserver secrète la clé Albert. Décision : serveur Python local lié à localhost ; l'autonomie est celle de l'application et de ses dépendances, non du réseau.
- **Bloquant : 14e source interne** : la découverte distante et l'externalisation du contenu ne sont pas autorisées par défaut. Décision : source représentée comme non traitée ; collecte interne hors périmètre du prototype public.
- **Majeur : couverture supposée** : sitemaps et pages d'accueil seuls manqueront des articles. Décision : comparer quatre semaines de publications de référence, puis seulement introduire un moteur secondaire.
- **Majeur : réutilisation** : reconstruire le JSON de composition `dsfr-mail/document` du builder créerait une seconde source de vérité. Décision : exporter V519, réutiliser `app/snum/adapter.js`.
- **Majeur : modèle halluciné** : Albert peut fabriquer des faits ou dates. Décision : date, URL, source et tri contrôlés par Python ; autres champs plafonnés et relecture humaine.
- **Majeur : droit et sécurité** : certains médias ont des conditions de réutilisation ; données de presse et données internes ne peuvent pas être traitées identiquement. Décision : pas de contournement, validation juridique et RSS non exigé.
- **Majeur : qualité des résultats** : date valide ne prouve pas la lisibilité du corps intégral, ni la pertinence. Décision : séparer candidats, exclusions, contenus vérifiables, limite du prototype explicitement déclarée.

## Fardeau d'entretien

Le collecteur généraliste évite 14 extracteurs, mais échouera sur certains sites JS ou anti-bot. Ne pas multiplier les exceptions avant des tests documentés. Une source en échec doit être signalée, jamais considérée « sans actualité ».

## Revue EGM à lancer ensuite

Inviter un Goldfish `zoom_out`, un `design_critic` et un `implementation_readiness`, en contexte neuf, avec le design seul et les liens des dépôts ; demander gravité, preuve et correction minimale. Deux passes de revue après modification de la spécification. Conserver le rapport des objections non résolues.

## Limite de livraison

Ce dépôt de travail n'est pas une recette sur les 14 sites ni une validation d'Albert en production. Un serveur local ne doit pas être publié directement sur GitHub Pages. Ne pas déployer sans validation de la sécurité et des conditions d'utilisation des éditeurs.
