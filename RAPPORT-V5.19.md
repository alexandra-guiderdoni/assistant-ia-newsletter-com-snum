# Rapport de recette V5.19

## Verdict

`NO-GO` pour une livraison autonome reposant uniquement sur l’Assistant.

Les contrôles déterministes du dépôt sont verts et le Projet Collecte produit un paquet
V5.19 valide. Le Projet Rendu HTML ne restitue toutefois pas le canon local à l’octet
près. La définition de fini « gabarit output HTML 100 % identique à celui de Bacoco »
n’est donc pas satisfaite.

## Scénario réel exécuté

- édition : 14 octobre 2026 ;
- fenêtre inclusive : du 3 au 13 octobre 2026 ;
- Projet Collecte : `COLLECTE`, `VALIDATION`, puis `PAQUET` dans la même conversation ;
- Projet Rendu HTML : `RENDRE_EDITION` dans une conversation neuve créée depuis le
  Projet ;
- Web activé uniquement pendant `COLLECTE` ;
- aucune publication GitHub Pages ni diffusion par courriel.

## Résultat du Projet Collecte

La première recette a révélé un JSON invalide : des guillemets internes n’étaient pas
échappés. Le prompt Collecte a été corrigé pour exiger un bloc analysable comme JSON et
l’échappement de `\"` et `\\` dans les chaînes.

La recette suivante a produit :

- 10 requêtes distinctes couvrant les 5 rubriques et au moins 5 domaines ;
- 10 candidats ;
- 6 sources valides et 4 sources exclues ;
- l’égalité vérifiée `6 + 4 = 10` ;
- un paquet `SNUM_PAQUET_RENDU_V519` de 6 articles ;
- 6 identifiants et 6 URL uniques ;
- exactement 3 articles essentiels ;
- des dates ISO et longues cohérentes.

Le paquet réel passe le moteur local strict. Le HTML canonique local contient 18 467
caractères et 18 756 octets. Son SHA-256 est
`a92c6a769d8e6bad932bd1da659e8be96d8c321bed6fe9792a167b000eaa798c` et le validateur
retourne `HTML_CANONIQUE_OK`.

## Résultat du Projet Rendu HTML

Le premier rendu dans le bon Projet avait la structure et l’apparence attendues, mais
pas l’identité exacte : 18 725 octets contre 18 756 pour le canon local. Les causes
observées comprenaient l’ordre des rubriques, les jonctions, l’indentation, l’échappement
des apostrophes et le saut de ligne final.

Le message RENDU a ensuite explicité l’ordre immuable
`numerique, ia, commande, rh, bercy`, la numérotation, la conservation des espaces,
l’absence de lignes vides ajoutées, l’échappement HTML et le saut de ligne final.

La recette corrigée, exécutée dans une nouvelle conversation du Projet Rendu, produit
encore un HTML différent :

- HTML Assistant : 18 491 caractères, 18 781 octets ;
- SHA-256 Assistant :
  `1bddedf193904ebf114e6150fd080383bb2d8c34be6e2fdefbaa227cf3bb89da` ;
- HTML canon local : 18 467 caractères, 18 756 octets ;
- SHA-256 canon local :
  `a92c6a769d8e6bad932bd1da659e8be96d8c321bed6fe9792a167b000eaa798c` ;
- aucun saut de ligne final dans la sortie Assistant ;
- ajout d’un lien de navigation `#numerique` alors qu’aucune section `numerique`
  n’existe ;
- suppression des quatre espaces placés avant les premières sections insérées.

Le statut textuel `HTML_CANONIQUE_PRODUIT` affiché par l’Assistant est donc faux au
regard des contrôles externes. Il ne constitue pas une preuve.

## Audit ShipGuard et contrôles locaux

L’audit ShipGuard initial a rendu `NO-GO` et relevé notamment : prompt Rendu trop long,
ZIP V5.18 obsolètes, validation V5.19 trop permissive, contrôles HTML incomplets,
`.DS_Store` présent et rapport de recette réutilisé sans preuve fraîche.

Les corrections déterministes apportées couvrent ces constats :

- prompt Collecte : 3 990 caractères ;
- prompt Rendu : 3 990 caractères ;
- chaque ressource Rendu reste sous 4 500 caractères ;
- schéma V5.19 strict, URL HTTPS et uniques, identifiants uniques, dates et fenêtre
  cohérentes, essentiels et mots-clés contrôlés ;
- sections, liens externes, scripts, `h1` et marqueurs HTML renforcés ;
- comparaison binaire de `COQUE_A + COQUE_B` avec la source canonique ;
- ZIP V5.19 régénérés ;
- versions antérieures sorties de la racine ;
- `.DS_Store` supprimés.

Après correction, les preuves locales sont : 26 tests unitaires réussis, Ruff réussi et
`KIT_DECOUPLE_OK`.

Le validateur HTML contrôle les invariants de structure, mais ne prouve pas seul
l’identité exacte de toute la zone dynamique. La recette compare donc aussi la taille et
le SHA-256 de la sortie Assistant avec ceux du canon local ; cette comparaison externe
fonde le verdict d’identité.

## Limite et suite recommandée

Le comportement restant n’est pas un défaut du générateur déterministe local : il vient
de la réécriture non déterministe du HTML par le modèle malgré les ressources et les
consignes. Ajouter une nouvelle règle au prompt après chaque différence déplacerait
l’écart sans garantir l’identité à 100 %.

La recommandation est de ne pas déclarer la V5.19 autonome. Pour garantir l’identité
octet par octet, il faut que l’étape Rendu exécute un transformateur déterministe ou
qu’elle restitue un artefact déjà rendu, capacité qui n’est pas disponible dans le seul
chat Assistant utilisé par les collègues.
