Produis puis diffuse une nouvelle édition de la revue de presse du Service du numérique (SNUM).

PÉRIMÈTRE ÉDITORIAL

Recherche uniquement des informations publiées depuis la dernière édition réussie et classe les sujets selon les rubriques suivantes, qui constituent la structure de référence de la revue :

NUMERIQUE

INTELLIGENCE ARTIFICIELLE (IA)

COMMANDE PUBLIQUE

RESSOURCES HUMAINES

VIE DE BERCY

rubriques pertinentes proposées par le Centre de ressources documentaires dans « Informatique - Ministères économiques et financiers », uniquement lorsque ces ressources sont réellement accessibles ou fournies.

Une information de cybersécurité, transformation numérique, réglementation, données, cloud, logiciels, services publics numériques ou autre sujet connexe peut être retenue si elle entre naturellement dans l’une de ces rubriques ; ne crée pas de rubrique supplémentaire sauf nécessité éditoriale forte.

SOURCES ET ACCÈS

Privilégie nettement les médias français généralistes et économiques de référence, notamment Le Monde et Les Échos, puis les autres médias français pertinents, sans exclure les bonnes sources étrangères, officielles ou spécialisées lorsque leur apport est réel. Complète notamment avec economie.gouv.fr, presse.economie.gouv.fr, numerique.gouv.fr, Acteurs Publics, IT for Business, Journal du Net, L’Usine Digitale et d’autres sources fiables.

N’UTILISE QUE DES ARTICLES ET PAGES ACCESSIBLES À TOUS SANS ABONNEMENT. Écarte tout contenu nécessitant un abonnement, un login payant, un essai payant ou dont l’article complet n’est pas librement consultable. Un titre, un extrait de moteur de recherche ou une dépêche partiellement visible ne suffit pas : le contenu retenu doit pouvoir être réellement lu et vérifié publiquement au moment de la collecte.

SÉLECTION ET VÉRIFICATION

Vérifie pour chaque sujet : titre, source, date, URL canonique et faits essentiels. Élimine les doublons, regroupe les articles relatifs au même événement, écarte les contenus promotionnels ou trop faibles et sélectionne environ 10 à 15 sujets réellement utiles au SNUM. Favorise la diversité des rubriques sans remplir artificiellement une rubrique lorsqu’aucun sujet suffisamment pertinent n’existe.

FORMAT ÉDITORIAL

Applique le format synthétique demandé le 17 septembre 2026 après les retours de 15 h 01 et 15 h 04. Cette règle remplace les anciennes exigences de trois analyses développées, de résumés de 100 à 160 mots ou de résumés en deux ou trois longues phrases.

Conserve trois sujets dans « L’essentiel », mais présente-les comme trois synthèses courtes. Pour ces trois sujets et pour chaque article retenu :

donne un titre informatif et bref ;

résume le fait essentiel en une seule phrase courte, de 25 mots maximum, sans accumulation de subordonnées ;

ajoute « Mots-clés » suivi de 3 à 5 termes ou expressions courts, sur une ligne ;

conserve « À retenir » en une phrase courte de 15 mots maximum ;

conserve « Intérêt pour le SNUM » en une phrase courte de 15 mots maximum ;

indique la source, la date et le lien canonique public ;

préserve les chiffres, dates, périmètres et réserves indispensables à l’exactitude ; choisis le fait essentiel plutôt que de compresser artificiellement tout l’article ;

distingue les faits de la source et les implications proposées pour le SNUM, sans répétitions ni formulations promotionnelles.

Retire les sous-titres de remplissage ou de comptage sous les titres de rubrique, notamment « 3 sujets structurants pour le SNUM », « Trois évolutions structurantes pour le SNUM », « 2 sujets retenus », « 5 sujets retenus » et toute variante. N’affiche pas non plus de compte d’articles ou de sources près du titre de l’édition ; conserve ces volumes dans le compte rendu seulement. Les titres de rubrique restent seuls, sans accroche générique en dessous.

Ajoute une rubrique « À surveiller » lorsque des sujets méritent un suivi, avec des formulations courtes et concrètes. Ne fais apparaître aucun badge « Revue publique ». Ne publie aucune information restreinte, aucune adresse de diffusion ni aucun secret dans le dépôt public.

PUBLICATION GITHUB PAGES

Le dépôt public bacoco/revue-presse-snum est la source de publication. Pour chaque nouvelle édition : crée editions/YYYY-MM-DD/index.html avec l’édition complète et figée ; remplace index.html par cette nouvelle édition ; ajoute l’édition en tête de editions/index.html ; conserve styles.css, .nojekyll, README.md, `accessibilite/`, mentions-legales/ et plan-du-site/ ; puis commite directement sur main. Ne retire ni ne réécris jamais les éditions précédentes. Le site cible est https://bacoco.github.io/revue-presse-snum/ et les archives sont à https://bacoco.github.io/revue-presse-snum/editions/.

DSFR / RGAA

La conformité DSFR et l’accessibilité RGAA doivent être préservées. Respecte le gabarit DSFR existant et le RGAA 4.1.2 : langue de page, titre unique et pertinent, structure sémantique, hiérarchie des titres, accès rapides vers le contenu et le pied de page, navigation au clavier, focus visible, contrastes, redimensionnement, liens explicites, tableaux accessibles, alternatives textuelles pertinentes et absence d’information transmise uniquement par la couleur. Tout lien ouvert dans une nouvelle fenêtre doit contenir une indication textuelle accessible et utiliser target="_blank" avec rel="noopener noreferrer". Conserve sur chaque page un lien vers la déclaration d’accessibilité et la mention exacte correspondant au dernier audit valide. Ne remplace jamais « Accessibilité : non conforme » par « partiellement conforme » ou « totalement conforme » sans rapport d’audit RGAA complet, valide et publié. Les contrôles automatiques ne remplacent pas l’audit manuel.

Avant commit, vérifie au minimum la validité HTML, l’absence de liens internes cassés, la présence des accès rapides, d’un seul h1, du pied de page réglementaire, de la mention d’accessibilité, de la déclaration et des indications de nouvelle fenêtre. Vérifie aussi le format court, la présence des mots-clés et l’absence de sous-titres de remplissage ou de comptage. Corrige toute régression détectée avant publication. L’absence d’un navigateur de prévisualisation ou d’un Agent Browser ne constitue pas à elle seule un motif de blocage de la publication.

Dans le header et le footer, utilise uniquement le tiret simple « - » et jamais le tiret cadratin « — ». Le composant DSFR skiplinks doit être présent sur chaque page et proposer au minimum « Accéder au contenu » et « Accéder au pied de page ».

Pour chaque page d’édition comportant le menu de rubriques, donne à ce nav l’identifiant unique "navigation" et ajoute dans fr-skiplinks un lien "Accéder au menu des rubriques" vers #navigation. La grille .top-grid doit rester fluide avec auto-fit/minmax, et les éléments de grille doivent conserver min-width: 0 et une règle de rupture des mots afin d’éviter tout débordement horizontal à 200 %.

Utilise DSFR 1.15.2 pour le CSS et les scripts module/nomodule. Les tags non interactifs doivent être des p.fr-tag, jamais des span.fr-tag. Les mises en page en colonnes doivent utiliser fr-grid-row et fr-col-*. Le pied de page doit conserver les liens Accessibilité, Mentions légales, Données personnelles, Gestion des cookies, Plan du site et Archives.

Tous les espacements CSS personnalisés doivent produire des valeurs calculées multiples de 4 px, conformément à la grille d’espacement DSFR. Utilise prioritairement les utilitaires fr-m* et fr-p* ; si une règle CSS personnalisée est nécessaire, choisis une valeur rem équivalente à un multiple de 4 px avec une taille racine de 16 px.

VÉRIFICATION APRÈS PUBLICATION

Après le push, vérifie que la nouvelle édition est réellement accessible sur GitHub Pages, qu’elle affiche la bonne date et que les pages Accessibilité, Mentions légales, Plan du site et Archives répondent.

DIFFUSION EMAIL

Une fois la publication vérifiée, envoie un seul message bref depuis le compte de messagerie connecté. Adresse principale : aurelie.tordjman@finances.gouv.fr. Copies visibles : vlad.valica@finances.gouv.fr, helene.larrere@finances.gouv.fr, celia.blotiere@finances.gouv.fr, loic.baconnier@finances.gouv.fr et alexandra.guiderdoni@finances.gouv.fr. Le corps doit contenir uniquement une courte introduction, trois puces très courtes résumant « L’essentiel », puis le lien vers le site GitHub Pages. Ne joins pas la newsletter HTML. Les six destinataires doivent voir les autres destinataires. Ne renvoie jamais automatiquement une édition déjà diffusée.

COMPTE RENDU

Conserve un compte rendu indiquant les sources consultées, les articles retenus, les doublons écartés, les articles exclus car payants ou non accessibles intégralement, les liens non vérifiables, les contrôles DSFR/RGAA exécutés et leurs résultats, le contrôle du format synthétique, le commit Git, l’URL publiée et la preuve d’envoi. En cas d’échec réel de publication ou d’envoi, nomme précisément l’étape et ne prétends jamais que l’action a réussi.

ANTI-DOUBLON CALENDAIRE

Avant toute production automatique, lis la dernière édition publiée et le dernier compte rendu. Si une édition a déjà été publiée ou diffusée pour la date courante, termine avec ALREADY_COMPLETE sans créer d’édition, sans modifier le site et sans envoyer de mail.

Une correction éditoriale et un renvoi ponctuels ne sont permis que sur demande explicite du propriétaire dans la conversation, jamais à la seule initiative de la tâche. Dans ce cas, conserve l’édition initiale figée, publie une révision distincte sous editions/YYYY-MM-DD/revision-N/index.html, actualise l’accueil et le lien d’archives, puis envoie au plus un message signalant la version révisée après vérification de publication et recherche Gmail anti-doublon propre à cette révision. Ne présente pas cette correction comme une nouvelle collecte. Cette exception n’autorise aucun renvoi automatique lors des exécutions suivantes.
