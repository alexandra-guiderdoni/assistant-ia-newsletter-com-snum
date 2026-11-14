# Parcours navigateur de la page Veille SNUM

Ces scripts jouent la page GitHub Pages dans Chromium, de bout en bout, sans rien envoyer sur Internet :

- le site public, `api.github.com` et `raw.githubusercontent.com` sont simulés (`monde.cjs`) ; toute autre requête est bloquée et comptée ;
- chaque tâche lancée par la page exécute le vrai code serveur du dépôt (`produire.py` appelle les lignes de commande `publier`, `resumer`, `repecher`, `archiver`), avec les sources et l'Albert factices des tests ;
- le jeton utilisé est factice.

## Lancer

Playwright n'est pas une dépendance du dépôt. Indiquer son dossier, ou l'installer sur le poste (`npm install playwright`, puis `npx playwright install chromium`).

```bash
# depuis veille-snum-webapp-v5-apres-egm/veille-snum/
PLAYWRIGHT=/chemin/vers/node_modules/playwright node tests/navigateur/parcours.cjs
PLAYWRIGHT=/chemin/vers/node_modules/playwright node tests/navigateur/defauts.cjs
```

Code de sortie 0 si toutes les vérifications passent. Comptez trois minutes pour `parcours.cjs`, une pour `defauts.cjs`. Les attentes de plus d'une seconde de la page sont divisées par 25 pour tenir ce temps.

## Ce qui est couvert

`parcours.cjs` :

- les deux temps avec 48 titres réels (relevés sur le site public le 13 novembre 2026), au clavier pour les gestes clés ;
- soixante titres gardés ;
- jeton absent, mal formé, expiré, insuffisant, sans accès ; GitHub lent ; réseau coupé ;
- Albert indisponible, page protégée, paquet sans article, archivage en échec ;
- cache de GitHub Pages qui sert l'ancienne version ; deux personnes en même temps ;
- collecte complète, archives, repêchage, repêchage pendant la phase titres ;
- largeurs de 375, 640 et 320 px, ordre de tabulation, focus visible, contrastes, régions annoncées ;
- jeton absent du DOM, des adresses, de la console, du stockage et des fichiers publiés.

`defauts.cjs` : les scénarios qui échouaient avant les corrections de novembre 2026.

## Limites

Chromium seulement. GitHub et Albert sont simulés : ces parcours ne remplacent pas un essai sur le vrai service. `donnees/rapport-titres-60.json` complète les 48 titres réels par 12 titres dérivés, pour l'essai de volume.
