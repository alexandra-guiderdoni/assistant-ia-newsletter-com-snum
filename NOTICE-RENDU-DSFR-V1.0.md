# Newsletter SNUM - rendu DSFR

Cette troisième option transforme le paquet de Collecte V519 en **courriel HTML autonome**. Elle reprend le modèle de mail approuvé, ses flèches et son logo incorporé en base64.

Le rendu DSFR utilise désormais [outil-rendu-dsfr.html](outil-rendu-dsfr.html), un fichier autonome qui génère le mail sans réécriture par un modèle. Ce changement a été accepté après trois essais non fidèles dans l’Assistant. Le Projet Assistant expérimental reste non validé ; le [rapport de recette](_documentation/recette-mail-dsfr/RAPPORT.md) conserve les preuves.

Pour transmettre l’ensemble, utiliser le ZIP documenté du dossier `livraison/`.
Sa [notice d’installation](INSTALLATION-RENDU-DSFR.md) couvre le fichier autonome
et la réinstallation facultative du Projet expérimental. Le
[mode opératoire](MODE-OPERATOIRE.md) décrit le choix du gabarit et la recette
sur le poste cible. Ces documents sont inclus dans le ZIP documenté.

La Collecte V5.23 et le Projet `Newsletter SNUM - Rendu HTML` conservent leurs instructions et ressources. Après la Collecte, le métier choisit le Rendu HTML habituel ou cet outil de rendu de mail DSFR.

## Utilisation

1. Produire le paquet dans le Projet Collecte habituel.
2. Ouvrir `outil-rendu-dsfr.html` dans un navigateur, par double-clic sur le fichier enregistré.
3. Coller le paquet complet dans le champ. Les marqueurs et le suffixe `PAQUET_RENDU_PRET` sont acceptés, ainsi que le JSON seul ou entouré d’un bloc Markdown.
4. Cliquer sur **Prévisualiser le mail**, puis relire l’aperçu.
5. Cliquer sur **Télécharger le mail (.html)**. Le nom du fichier reprend la date d’édition du paquet.

Une erreur de structure est affichée sans correction silencieuse du contenu. Après toute modification du champ, le téléchargement précédent est retiré : il faut prévisualiser à nouveau pour obtenir le mail à jour.

Les rubriques présentes et leur numérotation s’adaptent au paquet. Les articles sont regroupés selon la première apparition de leur rubrique, puis conservent leur ordre dans celle-ci. Les essentiels reçoivent une mention dans leur article, sans duplication.

Les rubriques sans article ne sont pas affichées. Les alertes de `watch` apparaissent uniquement dans un encadré « Commentaire sur la collecte (hors mail) », séparé de l’aperçu. Elles sont exclues du mail téléchargé, y compris de ses commentaires HTML. Une liste vide ne montre aucun encadré. Un paquet entièrement vide conserve le message « Collecte à compléter ».

Les titres, faits, mots-clés, liens, dates et intérêts SNUM sont conservés. Une date hors fenêtre est présentée comme les autres, conformément au choix métier pour ce rendu ; le filtrage de Collecte et du Rendu HTML historique reste inchangé.

## Fichier autonome

Seul `outil-rendu-dsfr.html` est nécessaire au métier. Il peut être déplacé dans un autre dossier et fonctionne hors connexion, avec JavaScript activé. Il inclut les scripts, les styles, le modèle de mail et le logo original.

Le paquet reste en mémoire dans la page : aucun envoi, stockage persistant ou appel réseau n’est effectué. Le fichier HTML téléchargé est également autonome.

L’archive `Newsletter SNUM - rendu DSFR.zip` à la racine du dépôt contient
seulement le candidat Assistant qui a échoué en recette. Le ZIP du même nom dans
`livraison/` contient l’outil autonome, sa documentation et les fichiers du
candidat, dont le statut expérimental reste explicite.

## Maintenance

La source unique du mail est `_source/30-BLOCS-MAIL-DSFR.md`. L’interface et son moteur sont dans `_source/mail-tool-shell.html`, `_source/mail-tool-render.js` et `_source/mail-tool-ui.js`. Le fichier distribué est généré : ne pas le modifier directement.

Python et Node.js sont utilisés uniquement pour la maintenance et les tests ; ils ne sont pas nécessaires au métier. Aucune dépendance JavaScript externe n’est requise.

```bash
python3 scripts/build_mail_tool.py
python3 scripts/build_mail_tool.py --check
python3 scripts/build_mail_kit.py --check
python3 scripts/build_delivery.py
python3 scripts/build_delivery.py --check
python3 -m unittest discover -s tests -v
ruff check --no-cache scripts tests
python3 scripts/build_split_kit.py --check
git diff --check
```

Le moteur Python sert de référence indépendante du moteur JavaScript, sans étape supplémentaire pour le métier :

```bash
python3 scripts/newsletter_mail.py build --input paquet.json --output reference.html
python3 scripts/newsletter_mail.py verify --input paquet.json --html sortie-assistant.html
```

Le générateur de l’outil ne régénère ni les kits Assistant ni les deux ZIP historiques.

## Limites et preuves

Le statut réel de la recette figure dans [_documentation/recette-mail-dsfr/RAPPORT.md](_documentation/recette-mail-dsfr/RAPPORT.md).

La comparaison automatique prouve la fidélité des sorties pour les paquets exercés. Les événements de prévisualisation et de préparation du téléchargement ont été testés avec une simulation du DOM. L’utilisateur a ensuite confirmé l’affichage de l’aperçu sur son poste après le passage à une URL Blob. Le téléchargement effectif, la réouverture du mail et le poste de la collègue restent à contrôler manuellement ; l’automatisation de l’ouverture locale a été refusée par l’outil de navigation.

Aucun envoi ni rendu dans Outlook n’a été exercé. Le logo base64 reste une contrainte de transport à qualifier dans l’environnement de messagerie. L’outil ne vérifie pas les sources éditoriales.
