# Publication et diffusion SNUM — relais humain privé

V5. Consulter ce fichier au moment de préparer le HTML ou le courriel. Les adresses et preuves ne doivent jamais entrer dans les fichiers publics. Le dépôt conserve uniquement les contenus destinés au public.

## Périmètre des actions

L'assistant fournit le Markdown, les modifications HTML si le gabarit actuel lui est effectivement accessible, et le message prêt à copier. Une personne chargée de publier dispose de GitHub et des outils de validation. Une personne chargée d'envoyer dispose de la messagerie et contrôle ses messages envoyés. Une même personne peut assurer ces deux rôles.

Avec les capacités limitées de ce kit, aucun commit, push, envoi ou test technique n'est exécuté par l'assistant. Un outil trouvé dans une branche de développement ne devient pas automatiquement disponible dans l'instance utilisée.

## GitHub Pages

- Dépôt public source : https://github.com/bacoco/revue-presse-snum
- Site : https://bacoco.github.io/revue-presse-snum/
- Archives : https://bacoco.github.io/revue-presse-snum/editions/

Répéter les URL utiles dans le message courant lorsqu'elles doivent être utilisées ou rendues. Ne jamais construire une nouvelle URL de source à partir d'un souvenir.

### Préparer les fichiers

Fournir dans la conversation, au besoin en textes ou pièces jointes temporaires, les sources courantes de `index.html`, `editions/index.html`, `styles.css` et de la déclaration d'accessibilité. Fournir aussi les pages réglementaires si elles doivent être contrôlées ou modifiées. Ne pas encombrer durablement le Projet avec tous ces fichiers.

L'assistant utilise le code réel, jamais une capture pour reconstruire la structure. Si une ressource est inaccessible, il désigne précisément la pièce manquante. L'édition Markdown peut être PREPAREE ; le HTML reste à intégrer. Aucun HTML générique ne doit être présenté comme fidèle au gabarit non lu.

### Publier une nouvelle édition

La personne chargée de publier :

1. Crée `editions/YYYY-MM-DD/index.html` avec l'édition complète et figée.
2. Remplace `index.html` par cette édition, avec les chemins adaptés à l'accueil.
3. Ajoute l'édition en tête de `editions/index.html`, sans compte d'articles près du titre.
4. Conserve `styles.css`, `.nojekyll`, `README.md`, `accessibilite/`, `mentions-legales/`, `plan-du-site/` et les autres pages réglementaires existantes. Conserver n'interdit pas une correction de régression strictement nécessaire, explicitée et contrôlée ; ne pas les supprimer ou les reconstruire sans nécessité.
5. Ne supprime ni ne réécrit aucune édition précédente.
6. Exécute les contrôles avant commit, corrige toute régression détectée et commite directement sur `main`, puis pousse.
7. Fournit le SHA et les URL finales. Le push seul ne prouve pas le déploiement GitHub Pages.

## Exigences DSFR et RGAA du cahier des charges

Ce kit conserve DSFR 1.15.2 et RGAA 4.1.2 demandés ; il ne certifie pas la conformité du site.

| Élément | Exigence à conserver |
| --- | --- |
| Ressources DSFR | CSS et scripts module/nomodule en version 1.15.2 ; gabarit existant |
| Page | Langue française ; title unique et pertinent ; un seul h1 ; structure sémantique et hiérarchie de titres |
| Accès rapides | `fr-skiplinks` sur chaque page avec « Accéder au contenu » et « Accéder au pied de page » ; cibles présentes et identifiants uniques |
| Menu de rubriques | Sur chaque édition qui en comporte un : nav avec identifiant unique `navigation` ; skiplink « Accéder au menu des rubriques » vers `#navigation` |
| Clavier et rendu | Navigation clavier, focus visible, contrastes, redimensionnement et absence de débordement horizontal à 200 % |
| Informations | Pas d'information uniquement par la couleur ; alternatives textuelles pertinentes ; tableaux accessibles s'il y en a |
| Liens | Intitulés explicites ; tout lien en nouvelle fenêtre indique textuellement cette ouverture et utilise `target="_blank"` avec `rel="noopener noreferrer"` |
| Header et footer | Tiret simple `-` uniquement ; jamais de tiret cadratin `—` |
| Grille spécifique | `.top-grid` fluide avec `auto-fit`/`minmax` ; éléments avec `min-width: 0` et règle de rupture des mots |
| Colonnes | Classes `fr-grid-row` et `fr-col-*` |
| Tags non interactifs | `p.fr-tag`, jamais `span.fr-tag` |
| Espacements | Utilitaires `fr-m*` et `fr-p*` prioritaires ; espacements personnalisés calculés multiples de 4 px ; rem équivalents avec racine de 16 px |
| Footer | Liens Accessibilité, Mentions légales, Données personnelles, Gestion des cookies, Plan du site et Archives |
| Déclaration | Sur chaque page : lien vers la déclaration d'accessibilité et mention exacte correspondant au dernier audit valide |
| Statut d'accessibilité | Ne jamais remplacer « Accessibilité : non conforme » par « partiellement conforme » ou « totalement conforme » sans rapport RGAA complet, valide et publié |

Les contrôles automatiques ne remplacent pas l'audit manuel. Une vérification éditoriale, une relecture HTML ou cette table n'établit aucune conformité RGAA complète.

### Avant commit

Vérifier au minimum : validité HTML ; absence de liens internes cassés ; présence et cibles des accès rapides ; un seul h1 ; footer réglementaire ; mention et déclaration d'accessibilité ; indications des nouvelles fenêtres. Vérifier aussi le format court, les mots-clés et l'absence de sous-titres de remplissage ou comptage. Contrôler les autres exigences ci-dessus sur les éléments concernés par les changements.

La personne indique pour chaque contrôle méthode, périmètre et résultat. L'assistant peut relire le texte HTML disponible, mais ne doit pas présenter cette relecture comme l'exécution d'un validateur, d'un navigateur ou d'un test clavier. Les contrôles indisponibles restent NON_EXECUTE ou NON_VERIFIABLE.

L'absence d'un navigateur de prévisualisation ou d'un Agent Browser ne constitue pas, à elle seule, un motif de blocage. Les contrôles minimums doivent toutefois avoir été exécutés avec des moyens appropriés et les régressions détectées corrigées. Ne pas reporter une régression connue en annonçant la publication prête.

### Après push

Vérifier que l'accueil affiche effectivement la nouvelle date et le bon contenu ; que l'édition figée est accessible ; qu'elle apparaît en tête des archives ; que les pages Accessibilité, Mentions légales et Plan du site sont accessibles avec leur contenu attendu.

Une lecture directe actuelle par l'assistant est utilisable si cette capacité existe. Une réponse indexée, un extrait ou une URL ne suffit pas. Sans cette capacité, une personne fournit une vérification explicite, datée, indiquant les pages contrôlées et leur résultat ; la noter comme vérification humaine. Ne pas inventer de code HTTP.

L'email attend cette vérification. Si publication ou envoi échoue, nommer exactement l'étape et la cause observée ; ne jamais annoncer une réussite fictive.

## Courriel — configuration privée

Envoi unique depuis le compte de messagerie prévu, une fois la publication vérifiée et après contrôle humain anti-doublon des messages envoyés.

```text
À : aurelie.tordjman@finances.gouv.fr
Cc : vlad.valica@finances.gouv.fr ; helene.larrere@finances.gouv.fr ; celia.blotiere@finances.gouv.fr ; loic.baconnier@finances.gouv.fr ; alexandra.guiderdoni@finances.gouv.fr
Objet : Revue de presse du SNUM - [date]

Bonjour,

La nouvelle revue de presse du SNUM est disponible.

• [Premier sujet de L'essentiel en très peu de mots.]
• [Deuxième sujet de L'essentiel en très peu de mots.]
• [Troisième sujet de L'essentiel en très peu de mots.]

https://bacoco.github.io/revue-presse-snum/
```

Les six destinataires doivent voir les autres destinataires : utiliser À et Cc, aucun Cci. Le corps contient uniquement la courte introduction, les trois puces et le lien ; aucune newsletter HTML jointe, aucun compte rendu ni information interne. Il reste un brouillon jusqu'à confirmation d'envoi.

Rechercher dans les messages envoyés l'identifiant/date de l'édition, l'objet et le lien, puis comparer les contenus ; le lien de l'accueil seul ne distingue pas les éditions. Un message envoyé sans réponse visible n'autorise pas un renvoi. Si le résultat est incertain, faire vérifier avant toute tentative. Consigner date, résultat anti-doublon et preuve d'envoi (identifiant réel si fourni, copie ou confirmation humaine explicite). Ne pas demander des secrets de messagerie.

## Anti-doublon et reprises

Une édition publiée ou diffusée pour la date courante impose ALREADY_COMPLETE pour une nouvelle production, sans modification ni nouveau mail. Ce statut ne signifie pas que publication ET envoi sont achevés ; détailler les deux dans le compte rendu. Un brouillon non publié se reprend avec le même identifiant.

Une demande explicite peut autoriser de terminer la diffusion d'une édition publiée : aucune nouvelle collecte, aucune modification de l'édition ; publication vérifiée et contrôle humain prouvant l'absence d'envoi ; au plus un message. Ne pas renouveler cette autorisation aux exécutions suivantes.

### Révision éditoriale explicitement demandée

Conserver l'édition initiale figée. Déterminer N depuis les révisions réellement existantes et préparer `editions/YYYY-MM-DD/revision-N/index.html`. Actualiser l'accueil et le lien d'archives, conserver l'accès à l'initiale et aux révisions précédentes. Ce travail est une correction, pas une nouvelle collecte.

Après contrôles et vérification de publication, la personne recherche un éventuel envoi propre à cette révision et envoie au plus un message signalant la version révisée. Enregistrer un identifiant distinct `YYYY-MM-DD-revision-N`, sa preuve et son envoi. Les éditions suivantes n'autorisent aucun renvoi automatique.
