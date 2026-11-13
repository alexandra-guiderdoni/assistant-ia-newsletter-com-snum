# Jeton GitHub de la page Veille SNUM

Page : https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/

## À quoi sert le jeton

La page lance deux tâches GitHub Actions à votre place : « Publier le paquet Veille SNUM » (bouton « Lancer la collecte ») et « Repêcher un candidat Veille SNUM » (bouton « Repêcher avec Albert »). Pour cela, elle appelle l'API GitHub avec un jeton personnel.

Sans jeton, la page reste utilisable pour tout le reste : relire le paquet publié, garder ou écarter, changer de thématique, consulter le rapport, télécharger ou copier le JSON V519.

Le jeton Albert n'a rien à voir : il reste dans les secrets du dépôt (`ALBERT_API_KEY`) et n'apparaît jamais dans la page.

## Qui peut créer quel jeton

- **Propriétaire du dépôt** (compte `alexandra-guiderdoni`) : jeton « fine-grained », limité à ce seul dépôt. C'est la procédure ci-dessous.
- **Collaborateur d'un dépôt personnel** : GitHub n'accepte pas de jeton « fine-grained » sur le dépôt d'un autre compte personnel (limitation documentée). Il ne reste que le jeton « classique », de portée `repo`, qui donne accès à tous les dépôts de la personne : à éviter. La solution propre est de transférer le dépôt dans une organisation GitHub, dont les membres peuvent alors créer un jeton « fine-grained » limité à ce dépôt. L'adresse de la page devient alors `<organisation>.github.io/assistant-ia-newsletter-com-snum/`.

## Créer le jeton (propriétaire)

Connecté à GitHub avec le compte propriétaire :

1. Ouvrir https://github.com/settings/personal-access-tokens/new
2. « Token name » : par exemple `Veille SNUM page` ; « Expiration » : une durée courte, par exemple 30 jours.
3. « Resource owner » : `alexandra-guiderdoni`.
4. « Repository access » : « Only select repositories », puis `assistant-ia-newsletter-com-snum`.
5. « Permissions », « Repository permissions » :
   - « Actions » : « Read and write » (lancer les tâches et suivre leur progression) ;
   - « Contents » : « Read-only ».
   « Metadata » passe en lecture seule automatiquement. Aucune autre permission n'est nécessaire.
6. « Generate token », puis copier le jeton aussitôt : GitHub ne l'affiche qu'une fois. Le ranger dans un gestionnaire de mots de passe ; ne jamais le coller dans un message, un ticket ou un fichier du dépôt.

## L'utiliser

1. Ouvrir la page, section « Connexion à GitHub », coller le jeton.
2. Section « Lancer une collecte » : vérifier les dates, puis « Lancer la collecte ». Laisser la page ouverte : une collecte dure environ huit minutes, la progression s'affiche, puis le paquet, le rapport et les candidats écartés se rechargent.
3. Pour un candidat écarté : choisir la thématique, puis « Repêcher avec Albert » (une à deux minutes). L'article arrive coché dans la sélection.

Le jeton reste seulement en mémoire de la page : il n'est enregistré ni dans le navigateur, ni dans l'adresse, ni dans la console, et n'est envoyé qu'à `api.github.com`. Après un rechargement, il faut le coller de nouveau. Le bouton « Effacer le jeton » le retire de la page.

Chaque collecte consomme environ 45 appels Albert sur le jeton du dépôt ; chaque repêchage, un ou deux.

## Révoquer

Effacer le jeton de la page ne le révoque pas. En fin d'usage, en cas de doute ou de fuite : https://github.com/settings/personal-access-tokens, choisir le jeton, puis « Delete ». Un jeton expiré se renouvelle depuis la même page.

## Dépannage

Messages affichés par la page :

- **Erreur 401** « GitHub a refusé le jeton » : jeton incomplet, expiré ou révoqué. Le recréer.
- **Erreur 403** « GitHub a refusé l'accès » : la permission « Actions : Read and write » manque, ou la limite d'appels de l'API est atteinte. Vérifier les permissions du jeton.
- **Erreur 404** « Dépôt ou workflow introuvable » : le jeton ne donne pas accès au dépôt (mauvais « Resource owner » ou dépôt non sélectionné), ou la tâche n'est pas sur `main`.
- **Erreur 422** « GitHub a refusé le lancement » : dates invalides, ou déclenchement manuel absent sur `main`.

En dernier recours, les deux tâches se lancent aussi depuis l'onglet Actions du dépôt, avec « Run workflow ».
