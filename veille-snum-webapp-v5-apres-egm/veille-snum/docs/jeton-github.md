# Jeton GitHub de la page Veille SNUM

Page : https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/

## À quoi sert le jeton

La page lance deux tâches GitHub Actions à votre place : « Publier le paquet Veille SNUM » (boutons « Lancer la collecte » et « Rédiger les résumés ») et « Repêcher un candidat Veille SNUM » (bouton « Repêcher avec Albert »). Pour cela, elle appelle l'API GitHub avec un jeton personnel.

Sans jeton, la page reste utilisable pour tout le reste : lire les titres trouvés, relire le paquet publié, garder ou écarter, changer de thématique, consulter le rapport et les archives, télécharger ou copier le JSON V519.

Le jeton Albert n'a rien à voir : il reste dans les secrets du dépôt (`ALBERT_API_KEY`) et n'apparaît jamais dans la page.

## Un jeton partagé par l'équipe

Choix du 14 novembre 2026 : le dépôt reste sur le compte personnel `alexandra-guiderdoni`, et l'équipe utilise un seul jeton, créé par la personne propriétaire du dépôt.

- **Pourquoi un seul jeton** : GitHub n'accepte pas de jeton « fine-grained » sur le dépôt d'un autre compte personnel. Un collaborateur ne pourrait créer qu'un jeton « classique », qui ouvre tous ses dépôts. Le jeton partagé, lui, est limité à ce seul dépôt.
- **Ce qu'il permet** : lancer et suivre les tâches de ce dépôt, lire son contenu. Il ne permet ni de modifier le code, ni d'accéder à un autre dépôt.
- **Ce que cela implique** : toutes les collectes apparaissent sur GitHub comme lancées par le compte propriétaire, sans distinguer les personnes. Quiconque détient le jeton peut lancer une collecte, donc consommer des appels Albert et remplacer ce que la page publie.
- **Le transmettre** : par un gestionnaire de mots de passe partagé, ou de vive voix. Jamais dans un courriel, une messagerie, un ticket ou un fichier du dépôt.
- **Le renouveler** : à son expiration, au départ d'une personne de l'équipe, ou au moindre doute. Créer le nouveau jeton, le transmettre, puis supprimer l'ancien (section « Révoquer »).

Alternative écartée pour l'instant : transférer le dépôt dans une organisation GitHub, où chaque membre crée son propre jeton limité au dépôt. Elle rendrait les lancements nominatifs, mais change l'adresse de la page.

## Créer le jeton (propriétaire)

Connecté à GitHub avec le compte propriétaire :

1. Ouvrir https://github.com/settings/personal-access-tokens/new
2. « Token name » : par exemple `Veille SNUM équipe` ; « Expiration » : 90 jours au plus, pour un jeton partagé.
3. « Resource owner » : `alexandra-guiderdoni`.
4. « Repository access » : « Only select repositories », puis `assistant-ia-newsletter-com-snum`.
5. « Permissions », « Repository permissions » :
   - « Actions » : « Read and write » (lancer les tâches et suivre leur progression) ;
   - « Contents » : « Read-only ».
   « Metadata » passe en lecture seule automatiquement. Aucune autre permission n'est nécessaire.
6. « Generate token », puis copier le jeton aussitôt : GitHub ne l'affiche qu'une fois. Le ranger dans un gestionnaire de mots de passe ; ne jamais le coller dans un message, un ticket ou un fichier du dépôt.

## L'utiliser

1. Ouvrir la page, section « Connexion à GitHub », coller le jeton partagé.
2. Section « Lancer une collecte » : vérifier les dates, puis « Lancer la collecte ». Laisser la page ouverte : la recherche des titres dure trois à quatre minutes, la progression s'affiche, puis les titres trouvés apparaissent.
3. Section « Titres trouvés » : cocher « Garder » pour chaque titre utile, puis « Rédiger les résumés ». Comptez une à deux minutes pour dix articles, puis environ deux minutes de publication ; le paquet, le rapport et les candidats écartés s'affichent ensuite.
4. Pour un candidat écarté : choisir la thématique, puis « Repêcher avec Albert » (une à deux minutes). L'article arrive coché dans la sélection.

La case « Collecte complète en une fois » enchaîne les deux temps sans tri des titres : cinq à neuf minutes.

Le jeton reste seulement en mémoire de la page : il n'est enregistré ni dans le navigateur, ni dans l'adresse, ni dans la console, et n'est envoyé qu'à `api.github.com`. Après un rechargement, il faut le coller de nouveau : ne rechargez donc pas la page pendant une collecte. Le bouton « Effacer le jeton » le retire de la page.

La recherche des titres n'appelle pas Albert. La rédaction consomme un à deux appels Albert par titre gardé sur le jeton du dépôt ; une collecte complète, environ 45 ; un repêchage, un ou deux.

## Révoquer

Effacer le jeton de la page ne le révoque pas. En fin d'usage, en cas de doute ou de fuite : https://github.com/settings/personal-access-tokens, choisir le jeton, puis « Delete ». Un jeton expiré se renouvelle depuis la même page.

## Dépannage

Messages affichés par la page :

- **Erreur 401** « GitHub a refusé le jeton » : jeton incomplet, expiré ou révoqué. Le coller de nouveau en entier ; s'il a été renouvelé, demander le jeton à jour à la personne qui gère le dépôt.
- **Erreur 403** « GitHub a refusé la demande » : la permission « Actions : Read and write » manque, ou GitHub limite les appels. Vérifier les permissions du jeton, sinon réessayer une heure plus tard.
- **Erreur 404** « GitHub ne trouve pas le dépôt avec ce jeton » : le jeton ne donne pas accès au dépôt (mauvais « Resource owner » ou dépôt non sélectionné).
- **Erreur 422** « GitHub a refusé la demande » : dates ou sélection refusées. Recharger la page puis réessayer.
- **« Une collecte ou une rédaction de résumés est déjà en cours »** : quelqu'un l'a lancée, ou vous-même avant un rechargement. Attendre sa fin, puis recharger la page. Activer de nouveau le bouton lance quand même : la demande attend son tour, puis remplace le résultat.
- **« Suivi interrompu »** : la page a perdu le contact avec GitHub (jeton expiré, réseau), mais la tâche continue. Recharger la page quelques minutes plus tard, sans relancer.
- **« Le site sert encore l'ancienne version »** : la tâche a réussi, GitHub Pages n'a pas encore mis la page à jour (dix minutes au plus). Recharger plus tard, sans relancer.
- **« Un paquet a déjà été publié pendant votre tri »** ou **« Une nouvelle collecte a remplacé les titres »** : une autre personne a avancé entre-temps ; la page affiche ce qui est publié.
- **« La rédaction des résumés n'a pas abouti »** : les titres gardés restent cochés, relancer. Si l'échec se répète, Albert est sans doute indisponible : réessayer plus tard.

En dernier recours, les deux tâches se lancent aussi depuis l'onglet Actions du dépôt, avec « Run workflow » ; le mode `resumes` exige la sélection que seule la page sait construire.
