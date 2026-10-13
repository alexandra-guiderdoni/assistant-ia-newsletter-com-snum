# Publication et diffusion - relais humain privé - V5.3.1

## Rôles et preuve

DINUM produit les textes et prépare le HTML depuis 04. Il fournit un fichier si une capacité réelle le permet, sinon un bloc HTML complet copiable ; aucune capacité générique de création de fichiers n’est supposée. Une personne dispose du dépôt et des outils de validation ; une personne dispose de la messagerie. Ce kit n’accorde aucun outil d’écriture GitHub ou d’envoi. Une demande de préparation ne vaut pas autorisation de publier. Les contrôles doivent être attribués à l’acteur réel ; Loïc est la référence du gabarit, pas automatiquement son contrôleur. Un état NON_EXECUTE n’est pas automatiquement une exigence préalable : distinguer ce qui est requis de ce qui documente une limite.

## Dépôt et publication

Dépôt : https://github.com/bacoco/revue-presse-snum ; site : https://bacoco.github.io/revue-presse-snum/ ; archives : https://bacoco.github.io/revue-presse-snum/editions/.

Avant production automatique, une édition déjà publiée ou diffusée pour la date cible impose ALREADY_COMPLETE. Avant publication, recouper les pages et le dépôt actuels ; une capture historique ne prouve pas l’état actuel. Ne pas transformer l’absence de preuve en preuve d’absence.

La personne chargée de publier crée `editions/YYYY-MM-DD/index.html` figée, remplace `index.html` par cette édition avec chemins adaptés, ajoute une entrée en tête de `editions/index.html` et conserve toutes les entrées antérieures. Garder `styles.css`, `.nojekyll`, `README.md`, `accessibilite/`, `mentions-legales/`, `plan-du-site/` et les autres ressources réglementaires. Ne jamais supprimer ni réécrire une édition précédente. Commit directement sur `main` et push après contrôles ; consigner le SHA réel. Aucun secret, destinataire, dossier privé ou article intégral dans le public.

Une correction d’une édition publiée exige demande explicite du propriétaire : conserver l’initiale, préparer editions/YYYY-MM-DD/revision-N/index.html, mettre à jour accueil et archives, vérifier publication et chercher les messages envoyés propres à cette révision avant au plus un message. Aucun renvoi spontané ni nouvelle collecte prétendue.

## HTML, DSFR et RGAA

Utiliser le gabarit vide de 04 ; conserver header, footer, composants, feuille publique et copie CSS intégrée permettant l’ouverture locale. CSS et scripts module/nomodule DSFR 1.15.2 ; langue fr, titre de page unique pertinent, un h1, structure et hiérarchie sémantiques. Trois skiplinks : contenu, menu des rubriques #navigation, footer ; cibles présentes et IDs uniques. Navigation clavier, focus visible, contrastes, redimensionnement sans débordement à 200 %, tableaux accessibles s’il y en a, alternatives pertinentes, aucune information seulement par couleur.

.top-grid : auto-fit/minmax, éléments min-width: 0 et rupture des mots ; fr-grid-row et fr-col-* ; p.fr-tag, jamais span.fr-tag. Utilitaires d’espacement DSFR prioritaires ; marges, paddings et gaps personnalisés calculés multiples de 4 px, rem équivalents à racine 16 px. Dans header et footer, tiret simple - uniquement. Tout lien en nouvelle fenêtre indique textuellement l’ouverture et utilise target=_blank avec rel=noopener noreferrer ; aucun besoin d’ouvrir tous les liens externes ainsi.

Footer : Accessibilité, Mentions légales, Données personnelles, Gestion des cookies, Plan du site, Archives. Sur chaque page, lien de déclaration et mention exacte du dernier audit valide. Conserver Accessibilité : non conforme. Un audit RGAA complet valide et publié est requis pour relever cette mention ; il n’est pas imposé avant chaque nouvelle édition. Nu vérifie le HTML, pas le RGAA. Les contrôles automatiques ne remplacent pas l’audit manuel. Aucun rapport de conformité fictif.

Avant commit : validité HTML, liens internes, skiplinks et cibles, h1 unique, footer complet, déclaration et mention d’accessibilité, indications de nouvelle fenêtre ; format court, mots-clés, absence de comptages et remplissage sous les titres. Contrôler les exigences affectées par les modifications, corriger les régressions connues. Consigner méthode, périmètre, acteur et résultat. L’absence de navigateur de prévisualisation ne bloque pas à elle seule ; ne jamais présenter un contrôle visuel comme exécuté s’il ne l’est pas. Les contrôles du gabarit ne valident pas le HTML rempli.

Après push : vérifier réellement la bonne date et le contenu à l’accueil, l’URL figée et son entrée d’archives, puis Accessibilité, Mentions légales, Plan du site et Archives. Une lecture actuelle ou confirmation humaine datée et précise peut établir ce contrôle ; aucune capture obligatoire, aucun code HTTP inventé. Le push ne prouve pas le déploiement. L’envoi attend cette vérification.

## Courriel privé

Une personne autorisée vérifie les messages envoyés, par date/identifiant, objet, lien et contenu, avant tout envoi ; un lien d’accueil seul ne distingue pas les éditions. Si un envoi est déjà fait ou incertain, ne pas renvoyer. Aucune preuve d’envoi n’est attendue avant l’envoi réel, aucun accusé des destinataires obligatoire.

```text
À : aurelie.tordjman@finances.gouv.fr
Cc : vlad.valica@finances.gouv.fr ; helene.larrere@finances.gouv.fr ; celia.blotiere@finances.gouv.fr ; loic.baconnier@finances.gouv.fr ; alexandra.guiderdoni@finances.gouv.fr
Objet : Revue de presse du SNUM - [date]

Bonjour,

La nouvelle revue de presse du SNUM est disponible.

• [Premier essentiel très court]
• [Deuxième essentiel très court]
• [Troisième essentiel très court]

https://bacoco.github.io/revue-presse-snum/
```

Un seul message, tous les destinataires visibles, aucun Cci, aucune newsletter HTML jointe. Le corps contient uniquement introduction, trois puces et lien. Conserver la preuve réelle d’envoi (date, identifiant, copie ou confirmation humaine précise) dans le dossier privé et 02. Un échec se décrit par l’étape et la cause ; ne jamais le déclarer réussi.
