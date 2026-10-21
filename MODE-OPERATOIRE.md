# Newsletter SNUM - mode opératoire

Ce guide accompagne chacun des trois ZIP du dossier `livraison/`. Extraire le
ZIP puis suivre sa notice `INSTALLATION-*.md`. Les autres fichiers Markdown ne
sont jamais téléversés en bloc dans un Projet Assistant.

## Choisir le bon parcours

| Besoin | Parcours | Résultat et limite |
| --- | --- | --- |
| Rechercher les actualités | Projet Collecte, Web activé | JSON à relire ; pas de mise en page |
| Produire le gabarit Web habituel | JSON → Projet Rendu HTML, Web désactivé | HTML pour le Web ; gabarit historique conservé |
| Produire le mail DSFR | JSON → `outil-rendu-dsfr.html` | Mail autonome avec PNG original ; Outlook à qualifier |
| Reproduire le troisième Projet Assistant | JSON → Projet rendu DSFR, Web désactivé | Expérimental ; copie du logo non validée |

Les noms installés sont Collecte **v5.23.6**, Rendu HTML **v5.23.6** et
**Newsletter SNUM - rendu DSFR**. Les versions des fichiers V5.23 et V5.19 sont
volontaires. La Collecte ne change pas selon le gabarit choisi.

## 1. Obtenir le contenu

Dans une nouvelle conversation du Projet Collecte, avec le Web activé, envoyer
seulement les deux lignes suivantes, avec les dates de l’édition :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
```

La réponse commence par `SNUM_PAQUET_RENDU_V519_START` et contient un seul JSON,
puis `SNUM_PAQUET_RENDU_V519_END` et `PAQUET_RENDU_PRET`. Copier le paquet entier
et conserver le contenu source dans un fichier autorisé. Une recherche sans
article admissible produit un paquet vide avec des alertes ; ce n’est pas une
panne de l’outil Web.

Relire les dates, les sources et les liens. Une réponse commençant par
`A_COMPLETER` n’est pas un paquet exploitable : arrêter avant le rendu.

## 2. Choisir une sortie

**Gabarit Web habituel.** Ouvrir une conversation du Projet Rendu HTML, sans Web,
coller le paquet entre ses marqueurs et l’envoyer sans autre consigne. La réponse
commence par `## HTML COMPLET`, puis contient un seul bloc `html` et
`## CONTROLES`. Conserver seulement le document de `<!doctype html>` à `</html>`
dans un fichier `.html` en UTF-8, sans les clôtures Markdown ni les contrôles.
Ce gabarit conserve « À surveiller » quand `watch` est rempli.

**Mail DSFR.** Ouvrir `outil-rendu-dsfr.html`, coller le même paquet et cliquer sur
**Prévisualiser le mail**. JSON seul, marqueurs et bloc Markdown JSON sont
acceptés. Relire les articles, puis cliquer sur **Télécharger le mail (.html)**.
Le nom du fichier reprend la date d’édition. Toute modification du JSON impose
une nouvelle prévisualisation avant téléchargement.

Les rubriques sans article sont absentes du mail. Les alertes `watch` apparaissent
uniquement sous « Commentaire sur la collecte (hors mail) » ; ne pas les copier
dans le courriel. Un paquet entièrement vide affiche « Collecte à compléter ».
Une date hors fenêtre reste présentée normalement dans ce gabarit mail ; la
Collecte et le gabarit Web conservent leur filtrage historique.

L’Assistant DSFR est une option expérimentale documentée dans son ZIP. Pour la
démonstration du mail et le logo exact, utiliser l’outil autonome.

## 3. Contrôler le poste de destination

Avec le seul fichier de l’outil copié dans un dossier, sans connexion :

1. Ouvrir l’outil et coller un paquet valide conservé à l’étape 1.
2. Prévisualiser : vérifier le logo, les flèches, les articles et les liens.
3. Télécharger le mail, puis rouvrir ce fichier dans le navigateur.
4. Vérifier à nouveau le logo et le contenu ; vérifier l’absence d’alertes dans
   le mail et la présence des commentaires uniquement dans l’outil.
5. Refaire l’essai avec un paquet vide : le message d’état vide doit apparaître.

Noter la date, le navigateur, sa version et le résultat de chaque étape. Ne pas
confondre la présence du bouton Télécharger avec un fichier effectivement
enregistré et rouvert. Si une politique du poste bloque le fichier, contacter le
support local sans modifier les protections du navigateur.

## 4. Qualifier Outlook administration

La version d’Outlook et la méthode d’insertion autorisée doivent être confirmées
sur le poste cible. Ouvrir un brouillon de recette et y insérer le contenu du mail
selon cette méthode. Vérifier le logo, les flèches, les liens, les accents, les
espacements et l’absence de défilement horizontal dans les vues utilisées.

Un envoi à une boîte de test exige l’autorisation habituelle du service. Comparer
alors le message reçu au fichier HTML, notamment le logo base64 après transport
et les versions d’Outlook effectivement utilisées. Noter les écarts avant toute
diffusion. Ce guide n’affirme aucune compatibilité Outlook acquise et ne fournit
aucun envoi automatique. Ne pas remplacer le logo par une image distante.

## Dépannage

| Symptôme | Action |
| --- | --- |
| Collecte ne produit pas le paquet | Vérifier le Web, le Projet choisi et ses deux ressources |
| `OUTIL_WEB_INDISPONIBLE` | Refaire une seule fois dans une nouvelle conversation avec les mêmes dates |
| `A_COMPLETER` ou `PAQUET_INCOMPLET` | Corriger la cause indiquée ; ne pas transmettre au rendu |
| `CANON_MANQUANT` dans un rendu | Vérifier les ressources et leur indexation avec la notice d’installation |
| L’outil indique une erreur de JSON | Recoller le paquet entier, sans tronquer les marqueurs ou corriger les faits silencieusement |
| Pas d’aperçu dans l’outil | Vérifier le fichier reçu et JavaScript, recoller le paquet, puis signaler le résultat au support |
| Logo altéré dans la sortie de l’Assistant DSFR | Utiliser le même JSON dans l’outil autonome |
| Téléchargement bloqué ou mail différent dans Outlook | Conserver le JSON, le HTML et les observations ; ne pas diffuser |

Après trois échecs identiques, arrêter et transmettre au support le code d’erreur
et les étapes, sans publier le contenu métier dans un canal non autorisé.
