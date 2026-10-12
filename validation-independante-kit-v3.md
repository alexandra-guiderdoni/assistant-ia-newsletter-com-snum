# Validation indépendante du kit SNUM V3 pour l'Assistant DINUM

Revue réalisée le 13 octobre 2026 à partir du prompt de validation fourni (annexe B, kit V3 intégral) et des sources publiques citées. Document privé : il reprend des éléments du kit qui ne doivent pas être publiés dans le dépôt de revue.

## Cadre et preuves

Ce que j'ai vérifié moi-même, par lecture directe :

- Le code de `bacoco/conversations` au SHA `febfb6f6b6f1fd904b2f82aed2971957d7a29ef4`, qui est encore la tête de `main` du fork au 13 octobre 2026 ; l'amont `suitenumerique/conversations` est toujours à `fbf18e579e5cbbefed5e6f954f8a0ded0239d068`, le fork a zéro commit propre et trois commits de retard. Fichiers lus : clients `pydantic_ai.py`, `document_context_builder.py`, `document_search_rag.py`, `document_summarize.py`, `web_search_brave.py`, `web_search_staan.py`, `agents/conversation.py`, `conversations/settings.py`, `chat/models.py`, `chat/serializers.py`, `chat/tokens.py`, `chat/constants.py`, `agent_rag/document_rag_backends/*.py`, `docs/project-file-indexing.md`, plus le formulaire de Projet du frontend au SHA amont.
- L'arbre complet de l'amont (1 245 chemins) pour la question AGENTS.md et les branches de lecture d'URL.
- Le site publié, ses cinq pages réglementaires, l'arbre du dépôt `bacoco/revue-presse-snum` et ses comptes rendus publics, dont ceux du 2 octobre 2026.
- Les guides DINUM cités (assistant, recherche Web, documents, automatisations et API).
- L'annexe B du prompt : identique ligne pour ligne aux sept fichiers du kit tels qu'ils étaient au début de la revue ; `PROMPT-PROJET.md` fait 899 mots au comptage par espaces.

Ce que je n'ai pas fait : aucune session sur l'instance DINUM, aucune recette, aucune collecte, aucune lecture du modèle ou de la configuration déployée, aucun contact, aucune modification des dépôts. Les observations sur le code prouvent ce que le code fait à ce SHA, pas ce que l'instance fait. Le moteur Web réellement configuré sur l'instance (Brave classique, Brave LLM context, Brave avec backend documentaire ou Staan) est inconnu : il se choisit par configuration de modèle.

## 0. Changement observé pendant la revue : passage à une V4, puis une V5

Entre 00:13 et 00:23 le 13 octobre, pendant cette revue, les fichiers du kit sur disque ont été réécrits en V4 par un autre agent. Faits observés :

- Nouveau fichier `INSTRUCTIONS-COURTES.txt` (760 octets) destiné au champ d'instructions du Projet.
- `PROMPT-PROJET.md` devient un document importé dans le Projet, découpé en sections P0 à P6 avec une « carte de chargement progressif » ; quatre fichiers importés au lieu de trois.
- Motif déclaré dans le nouveau lisez-moi : « corrige la troncature du champ d'instructions signalée par le propriétaire ».

Ce que j'ai vérifié à ce sujet : la troncature est expliquée par le code. Le modèle `llm_instructions` est un `TextField` sans limite, mais le serializer d'API borne le champ à `LLM_INSTRUCTIONS_MAX_LENGTH = 4000` caractères (`chat/serializers.py`, lignes 370 à 378, commentaire « prevent too large prompts »), et le composant de saisie du frontend porte `maxLength={4000}` avec un renvoi à cette constante (`ModalProjectForm.tsx`, ligne 755, au SHA amont). Un texte collé dans ce champ est coupé à 4 000 caractères par le navigateur ; un texte plus long envoyé à l'API serait refusé. Le prompt V3 mesure 6 229 caractères pour 899 mots : collé tel quel, il perd ses 2 200 derniers caractères, soit la fin de FORMAT, puis LIVRAISON, RELAIS, MAIL et FIN. Le propriétaire a observé un comportement codé, pas un incident.

Conséquence sur ce rapport : il évalue la V3, comme demandé. La V3 n'est pas installable telle quelle, son hypothèse d'injection complète est fausse pour plus d'un tiers du prompt. Le motif de la V4 est fondé. Sa forme observée à 00:23, un noyau de 760 caractères dans le champ et le manuel entier déplacé vers la recherche documentaire, qui renvoie au plus quatre passages par requête avec un seuil de score de 0,6, va plus loin que nécessaire : le champ accepte 4 000 caractères, de quoi loger les règles critiques condensées. À 00:27, le dossier a été remplacé une seconde fois : huit fichiers à plat, dossier `projet/` supprimé, noyau renommé `INSTRUCTIONS-COURTES.md` (762 caractères), et disparition du `CLAUDE.md` du projet ainsi que de la compilation V2 `assistant-dinum-revue-snum-kit-projet.md`. À 00:54, troisième remplacement : dix fichiers, dont `LOT-SOURCES-MODELE.md` et `VERIFICATION-LOCALE.md`, ce dernier annonçant un « kit V5 » avec un prompt court sous 1 500 caractères et quatre références permanentes ; ce remplacement a aussi supprimé le présent rapport, réécrit ensuite depuis le contexte de session. Ni la V4 ni la V5 ne sont évaluées ici. Les défauts majeurs M1 à M6 ci-dessous restent valables quelle que soit la version, car ils ne dépendent pas de l'emplacement des règles.

## 1. Verdict

**Non adaptée telle quelle ; utilisable après une correction structurelle bornée et des corrections ciblées.** Le prompt V3 dépasse de 2 229 caractères le plafond codé du champ d'instructions. Il faut d'abord ramener les règles critiques sous 4 000 caractères en déplaçant le reste vers les documents déjà prévus (correctif 0), puis appliquer les correctifs de la section 6.

**Note de conception : 12 sur 20.** Grille en cinq dimensions sur quatre points :

- Fidélité au cahier des charges et adaptations : 3 sur 4. Les adaptations sont explicites et honnêtes ; deux écarts non déclarés (compte gratuit, URL canonique) et une rupture de pratique non discutée (compte rendu public).
- Faisabilité dans l'Assistant DINUM : 1,5 sur 4. Le champ d'instructions est le bon mécanisme, mais le kit a été écrit sans vérifier son plafond de 4 000 caractères, pourtant visible dans le dépôt que son rédacteur a lu ; la lecture intégrale par l'outil Web n'existe pas ; les dates ne sont pas transmises par Brave ; le résumé automatique de l'historique n'est pas pris en compte.
- Qualité éditoriale : 3 sur 4. Règle d'arrêt, exemple fictif, essentiels non recomptés, exclusions typées. La dépendance aux textes fournis et le contrôle des mots par le modèle restent fragiles.
- Continuité et cas limites : 2,5 sur 4. Anti-doublon et états séparés bien conçus ; initialisation non guidée alors que les données existent ; perte de contexte dans une conversation longue non traitée.
- Coût et simplicité : 2 sur 4. Trois fichiers, mais quatre tableaux à maintenir à la main dans l'historique, trois tableaux dans chaque dossier privé, et dix à quinze textes à fournir par édition.

**Confiance : moyenne.** Le code est vérifié à un SHA daté ; l'instance, le modèle et le comportement réel ne sont pas observés.

**Fonctionnement sur l'instance : NON ÉVALUÉ.** Aucune preuve de pilote n'existe.

### Réponse à la question AGENTS.md

Non, un AGENTS.md n'apporte rien dans cet environnement. Vérifié : aucun fichier de ce nom dans les 1 245 chemins de l'arbre amont ; aucune mention dans les modules d'instructions, de contexte documentaire et d'outils ; le constructeur de contexte traite tous les fichiers de Projet de la même manière, en `tool_call_only`, sans reconnaissance de nom. Un AGENTS.md importé serait un document de plus, consulté seulement si l'assistant le cherche, et à quatre passages par requête. Le seul lecteur pour lequel ce nom a un mécanisme établi est un agent de codage travaillant sur le dossier du kit, pas l'Assistant DINUM. Les instructions de Projet remplissent ce rôle ; dupliquer les règles sous un second nom créerait deux versions concurrentes.

## 2. Points solides

- La séparation entre règles critiques dans les instructions et modèles dans les documents correspond au code : les instructions de Projet sont une instruction dynamique de l'agent, dans la limite de 4 000 caractères, et les fichiers de Projet ne sont jamais inclus en entier.
- Les codes de lecture des sources, la mention NON_EXECUTE partout où rien n'a été exécuté, l'attribution des preuves humaines et l'interdiction du succès fictif sont cohérents du prompt à la recette.
- L'anti-doublon distingue publication et diffusion, ce que l'ancien dispositif n'avait pas : le compte rendu public du 2 octobre montre une édition commitée, non vérifiée, puis envoyée sur demande explicite. Le kit aurait géré ce cas proprement.
- La fenêtre en journées complètes jusqu'à la veille est justifiée par le code : avec Brave, le modèle reçoit titre, URL et extraits, sans date. Elle correspond aussi à la pratique précédente : l'édition du 2 octobre couvrait les articles du 28 septembre au 1er octobre.
- La règle d'arrêt en deux passages avec demande groupée de cinq textes au plus empêche la boucle de recherche sans fin.
- L'exemple fictif sert de test de récupération documentaire : simple et vérifiable.
- Les exigences DSFR et RGAA correspondent au site réel : DSFR 1.15.2, trois accès rapides dont « Accéder au menu des rubriques » vers `#navigation`, mention « Accessibilité : non conforme », déclaration du 9 septembre 2026, aucun tiret cadratin sur l'accueil. La liste des pages à conserver est plus complète que le cahier des charges, et le dépôt contient bien un plan d'actions et un schéma pluriannuel.
- Répéter les URL dans le message courant est exactement ce qu'exige la politique d'URL de l'application.
- Trois fichiers sous le plafond de dix ; selon la documentation du dépôt, l'interface bloque l'envoi pendant l'indexation et signale les échecs, ce que le lisez-moi anticipe.

## 3. Matrice de conformité et d'adaptation

Présentée en liste, pas en tableau, pour une lecture linéaire. Pour chaque exigence : traitement V3, statut, conséquence.

- Rubriques fixes et classement des sujets connexes : conservé. Aucun écart.
- Ressources du Centre de ressources documentaires : conservé, conditionnel à l'accès réel. Aucun écart.
- Priorité à Le Monde et Les Echos : conservé. Conséquence non dite : sous la contrainte d'accès gratuit, cette priorité produit peu ; le compte rendu du 2 octobre n'a retenu aucun article de ces deux titres, tous marqués abonnés ou en erreur. La priorité reste utile comme veille d'alerte pour chercher ensuite la source primaire.
- Accès sans abonnement : adapté, plus strict. Le cahier des charges exclut abonnement, login payant et essai payant ; le kit exclut aussi tout compte, donc une inscription gratuite. Lecture défendable de « librement consultable », cohérente avec les capacités, mais c'est une décision à écrire, pas un acquis.
- Lecture et vérification du contenu complet : adapté par la voie INTEGRAL_FOURNI avec confirmation humaine. Délégation nécessaire, pas perte d'intention. Conséquence : la charge se déplace sur la personne (voir M1).
- Sélection de dix à quinze sujets, dédoublonnage par événement : conservé, enrichi d'une règle d'arrêt. Amélioration.
- Format synthétique du 17 septembre : conservé intégralement, plafonds compris. Aucun écart.
- Publication GitHub Pages, édition figée, accueil, archives : adapté, confié à une personne, avec SHA et contrôles avant commit. Intention préservée.
- DSFR et RGAA : conservé. L'assistant ne fait qu'une relecture, ce que le kit dit clairement.
- Vérification après publication : adapté, humaine ou par lecture directe « si disponible ». Conséquence : aucune lecture directe d'URL n'existe dans le code lu ; la vérification sera humaine dans tous les cas. Le kit devrait le dire sans conditionnel.
- Diffusion email : adapté, humaine, six destinataires visibles, aucun Cci, un envoi. Intention préservée.
- Compte rendu : adapté, devient le dossier privé non publié. Conséquence : rupture avec la pratique existante, où dix comptes rendus sont publiés dans `comptes-rendus/` du dépôt public, sans adresses. Le cahier des charges ne fixe pas l'emplacement ; la série publique s'arrêterait sans décision explicite. Option : publier une version expurgée.
- Anti-doublon calendaire : conservé et renforcé (publication et diffusion séparées, brouillon par identifiant).
- Correction et révision explicites : conservé, avec `revision-N` et un message au plus.
- Décalage de la fenêtre à la veille : adapté. Conséquence : fraîcheur réduite d'un jour, aucune perte d'information, pas d'heure fictive.
- Scheduler et renvoi automatique : absent, assumé. Vérifié : les guides DINUM indiquent que l'assistant ne supporte pas les automatisations.
- Archives figées, pages réglementaires et `styles.css` : conservé, élargi.

## 4. Défauts classés

### Bloquant

**B1. Le prompt dépasse le plafond codé du champ d'instructions.** Passage : `00-LIRE-MOI.md`, « Copier PROMPT-PROJET.md dans les instructions personnalisées ». Preuve : `chat/serializers.py` borne `llm_instructions` à 4 000 caractères et le composant de saisie coupe à 4 000 ; le prompt V3 fait 6 229 caractères. Scénario : le texte collé est coupé au milieu de FORMAT ; LIVRAISON, RELAIS, MAIL et FIN n'existent pas pour l'assistant ; il produit une édition sans états de fin, sans séparation des deux livrables, sans règles de relais ni de courriel, en croyant suivre le Projet. Conséquence : le dispositif de preuves repose sur des règles absentes, et rien ne le signale. Correction minimale : ramener le champ sous 3 900 caractères pour garder une marge (stratégie au correctif 0), et ajouter au diagnostic de la commande 1 la question « cite le dernier mot de tes instructions de Projet », qui révèle une coupe en une ligne. La version déployée n'ayant pas été inspectée, confirmer le plafond sur l'instance en collant un texte de 4 100 caractères et en observant la coupe.

### Majeur

**M1. La lecture intégrale par l'outil Web n'existe pas dans le code lu.** Vérifié : Brave classique transmet au modèle titre, URL et extraits ; pour les résultats sans extrait, le serveur télécharge la page, extrait le texte et en fait un résumé par un autre modèle, qui devient l'unique extrait ; Brave LLM context transmet des extraits ; Brave avec backend documentaire stocke le texte extrait dans une collection temporaire et renvoie des passages ; Staan transmet des extraits de 300 à 1 800 caractères, dix au plus par URL, avec une date de publication. Dans aucun mode le texte complet n'atteint le modèle. Conséquence : INTEGRAL_LU est pratiquement inatteignable ; chaque édition repose sur INTEGRAL_FOURNI, donc dix à quinze textes à fournir par la personne. Le kit le laisse découvrir par le diagnostic au lieu de le dire. Correction : écrire dans le lisez-moi et dans SOURCES que le mode normal est la fourniture humaine des textes des sujets retenus, et organiser le flux en deux temps : liste de candidats classés sur extraits, puis fourniture des seuls textes retenus, puis finalisation.

**M2. Brave ne transmet aucune date au modèle.** Vérifié : la fonction de mise en forme des résultats ne conserve que l'URL, le titre et les extraits. Staan transmet une date fournie par le service. Scénario : un article du 27 septembre est daté du 30 par un extrait qui mentionne « mardi » ; il entre dans la fenêtre à tort ; ou un article valable est écarté. Correction : dans SOURCES, exiger la provenance de la date (URL datée, mention explicite dans l'extrait, texte fourni, métadonnée de l'outil) et classer « date non établie » en NON_VERIFIABLE au lieu de l'inférer.

**M3. Le résumé automatique de l'historique n'est pas pris en compte.** Vérifié : quand les messages précédents dépassent la moitié de la fenêtre du modèle moins 1 000 jetons, l'application les remplace par un résumé de 2 048 jetons au plus et ne garde qu'une dizaine de messages récents. Scénario : la personne colle cinq textes complets au début de la conversation ; après les recherches des cinq rubriques et les relectures, ces textes ne sont plus dans le contexte ; la vérification des faits et les repères de preuve portent sur un résumé, sans que l'assistant le sache. Correction : fournir les textes complets soit en pièces jointes de la conversation, soit dans le message même qui demande la finalisation ; une conversation de production par édition ; en cas de reprise, recoller les textes avec le brouillon.

**M4. Une pièce jointe ne vaut pas toujours un texte complet disponible.** Réponse à la question posée en B. Vérifié dans le constructeur de contexte : les fichiers de Projet sont toujours en `tool_call_only`, jamais inclus ; les pièces jointes de conversation sont incluses en entier tant qu'elles tiennent dans le budget documentaire, puis les plus anciennes sont évincées silencieusement vers `tool_call_only` ; une pièce trop grande pour le budget n'est jamais incluse. Le guide DINUM dit « moins d'une dizaine de pages » puis « environ 5 pages » pour le mode complet. Un texte collé dans un message est complet jusqu'au résumé d'historique (M3). L'assistant voit le mode d'accès de chaque pièce dans son listing, il peut donc dire s'il lit en contexte complet ou par passages ; il ne peut pas prouver qu'un texte fourni est intégral, la confirmation humaine reste nécessaire. Correction : dans la commande 3, demander de joindre les textes en fichiers texte à la conversation plutôt que de les coller, et exiger de l'assistant qu'il indique pour chaque pièce son mode d'accès avant de la qualifier INTEGRAL_FOURNI.

**M5. Les gestes les plus coûteux sont aussi les moins accessibles.** Passages : `02-HISTORIQUE.md` sections B3, C et D (quatre tableaux à maintenir à la main) ; modèle de dossier privé dans `01-MODELE-EDITORIAL.md` (trois tableaux, dont un contrôle par fiche sur six colonnes). Scénario : à chaque édition, la personne édite des tableaux Markdown avec un lecteur d'écran, et copie dix à quinze articles depuis des sites web. Conséquence : le temps humain dépasse probablement celui de l'ancien dispositif, hypothèse à mesurer au pilote. Correction : remplacer tous les tableaux par des listes à champs nommés, une entrée par bloc ; faire produire par l'assistant le fichier `02` complet à substituer, ce qui est déjà prévu ; réduire le contrôle éditorial à la liste des écarts constatés, pas une ligne par fiche.

**M6. L'initialisation de l'historique n'est pas guidée alors que les données sont publiques.** Passage : `00-LIRE-MOI.md`, « Initialiser 02-HISTORIQUE.md depuis la dernière revue et son compte rendu réels ». Les comptes rendus du 2 octobre dans le dépôt public donnent la fenêtre couverte (articles du 28 septembre au 1er octobre), les commits, l'heure d'envoi (2 octobre, 10:13 Europe/Paris) et les exclusions. Correction : fournir un bloc A pré-rempli (proposé en section 7) et indiquer de coller les deux derniers comptes rendus publics en B2 et C.

### Mineur

**m1. « URL canonique vérifiée ».** Sans lecture de page, l'assistant ne voit pas la balise canonique. Remplacer par « URL telle que renvoyée par l'outil ou fournie, sans paramètres de suivi ».

**m2. Exclusion de tout compte.** Écrire la décision dans « Adaptations assumées » : un article derrière inscription gratuite est exclu même fourni, parce qu'il n'est pas « accessible à tous ».

**m3. Date serveur en UTC.** Vérifié : `TIME_ZONE = "UTC"` et l'instruction « Today is … » utilise le fuseau serveur. Entre minuit et deux heures à Paris, la date serveur est la veille. Le kit fournit DATE_EDITION_PARIS ; ajouter dans DÉMARRAGE : « si la date injectée par l'application diffère, DATE_EDITION_PARIS prévaut ».

**m4. Anti-doublon fondé sur la section C par recherche documentaire.** La recherche renvoie quatre passages par requête ; une section C de vingt lignes peut n'être que partiellement retrouvée. Le kit interdit de coller tout l'historique, à raison ; ajouter au lancement la liste compacte des événements des deux dernières éditions (titre, date, URL), soit vingt à trente lignes.

**m5. Objet du courriel.** L'ancien dispositif envoyait « Revue de presse SNUM - 2 octobre 2026 » ; le kit prévoit « Revue de presse du SNUM - [date] ». La recherche anti-doublon dans les messages envoyés doit viser les deux formes.

**m6. Comptage des mots par le modèle.** Peu fiable ; la table de contrôle par fiche donne une assurance factice. Demander un contrôle humain des trois essentiels seulement et accepter une tolérance explicite, ou un outil réel quand il existe.

**m7. Version du registre dans la recette.** La recette simule « registre version 2 » alors que le fichier livré est en version 1 ; cohérent après initialisation, à dire en une ligne.

**m8. Vérification après publication « si une lecture actuelle est possible ».** Retirer le conditionnel : dans le code lu, l'assistant ne lit pas d'URL ; la vérification est humaine, point.

### Amélioration facultative

- Publier une version expurgée du dossier privé dans `comptes-rendus/`, pour ne pas interrompre la série publique sans décision.
- Extraire de `index.html` un gabarit de fiche et d'en-tête de quelques dizaines de lignes, à fournir à la place du fichier de 26 Ko, à condition de le maintenir.
- Prévoir dans COMMANDES un lancement pour fenêtre longue : au 13 octobre, la fenêtre depuis le 2 octobre couvre onze jours, donc probablement plus de quinze candidats solides ; l'arbitrage prévu suffit, mais le dire évite une sélection tronquée.

## 5. Plaidoyer de l'avocat du diable

Le meilleur argument contre ce dispositif tient dans le dépôt public lui-même. L'ancien dispositif, un agent ChatGPT avec connecteurs GitHub et Gmail, lisait les pages (« Page de publication lue intégralement », compte rendu du 2 octobre), commitait, et envoyait. Il n'a échoué que sur un point : vérifier la page publiée depuis son outil. La V3 remplace cet agent outillé par un assistant qui ne lit pas les pages, ne commite pas et n'envoie pas. Le gain est réel : hébergement SecNumCloud, aucun connecteur sur une messagerie professionnelle, aucun secret hors du poste. Le prix est intégralement payé par une personne : fournir dix à quinze textes, publier, vérifier cinq pages, contrôler les messages envoyés, envoyer, et réécrire l'historique.

Conditions où la V3 ne fait pas gagner de temps :

- Si plus de la moitié des sujets exigent un texte fourni, ce que M1 rend probable : la personne lit chaque article pour le copier, donc fait elle-même la découverte et la lecture ; l'assistant ne garde que la rédaction et le contrôle.
- Si la cadence reste bihebdomadaire : les gestes humains se répètent deux fois par semaine.
- Si la personne doit maintenir quatre tableaux Markdown avec un lecteur d'écran à chaque édition.

Hypothèse à vérifier au pilote : le temps humain par édition dépasse deux heures, contre quelques minutes de supervision avec l'ancien dispositif. Si elle se confirme, l'usage honnête de l'Assistant DINUM est la rédaction et le contrôle à partir de textes déjà collectés par un autre moyen, pas la découverte.

## 6. Correctifs prêts à appliquer

Remplacements locaux, sans refonte. Tous restent valables en V4, sauf indication.

**Correctif 0, `PROMPT-PROJET.md` entier : passer de 6 229 à moins de 3 900 caractères sans perdre une règle d'état.** Tailles mesurées par bloc, en caractères : ouverture 327 ; CONTEXTE 407 ; DÉMARRAGE 404 ; ANTI-DOUBLON 439 ; PÉRIODE 615 ; SOURCES 463 puis 612 ; SÉLECTION 636 ; FORMAT 695 ; LIVRAISON 322 ; RELAIS 610 ; MAIL 297 ; FIN 370. Procédure :

- Garder tels quels : ouverture, DÉMARRAGE, ANTI-DOUBLON, LIVRAISON, FIN, soit 1 862 caractères. Ce sont les règles d'état et de preuve ; elles ne vont pas dans un document lu par passages.
- Déplacer entièrement : FORMAT vers `01-MODELE-EDITORIAL.md`, section « Revue publique », qui porte déjà le modèle et une partie des interdits ; RELAIS et MAIL vers `03-PUBLICATION-DIFFUSION.md`, qui contient déjà chaque règle qu'ils énoncent. Les remplacer dans le champ par une ligne de renvoi d'environ 230 caractères : « FORMAT, RELAIS, MAIL : applique 01 pour le format (fait essentiel 25 mots, À retenir et Intérêt 15, 3 à 5 mots-clés, trois essentiels non recomptés) et 03 pour le HTML, la publication, la vérification et le courriel ; mail en brouillon, envoi humain. »
- Condenser, avec cibles : CONTEXTE à 250 (garder la liste des trois fichiers et « un résumé ne vaut pas lecture ») ; PÉRIODE à 420 ; SOURCES à 650 au total, en gardant la liste des médias sur une ligne, la règle d'accès et le renvoi aux codes de lecture de `01` ; SÉLECTION à 430 en gardant les cinq rubriques, la cible de dix à quinze et la demande groupée.
- Résultat attendu : environ 3 870 caractères avec les séparateurs. Mesurer avec `wc -m` avant de coller ; refuser tout collage au-dessus de 3 900.
- Garde-fou permanent : ajouter à la commande 1 « cite le dernier mot de tes instructions de Projet » ; le mot attendu est le dernier du fichier.

Ce correctif remplace la V4 observée pour ce qui concerne le champ d'instructions ; il ne touche pas à la V4 pour le reste.

**Correctif 1, `00-LIRE-MOI.md`, « Adaptations assumées », première puce.** Remplacer « Le texte complet et l'accès public de chaque source restent indispensables. Des extraits seuls produisent des candidats. » par : « Dans le code examiné, aucun mode de recherche Web ne transmet le texte complet d'un article : extraits, passages ou résumé seulement. Le mode normal est donc : l'assistant classe des candidats sur extraits, la personne fournit le texte des seuls sujets retenus, l'assistant finalise. Un article payant copié reste exclu. »

**Correctif 2, `PROMPT-PROJET.md`, section SOURCES.** Remplacer « Vérifie titre original, source, date, URL canonique et faits. Ne fabrique aucune URL. » par : « Vérifie titre original, source, date et faits. Note la provenance de la date : URL datée, mention explicite dans l'extrait ou le texte fourni, métadonnée de l'outil ; sans provenance, la date est non établie et le sujet reste NON_VERIFIABLE. Utilise l'URL telle que renvoyée par l'outil ou fournie, sans paramètres de suivi. Ne fabrique aucune URL. »

**Correctif 3, `PROMPT-PROJET.md`, section DÉMARRAGE.** Ajouter après « Ni date serveur ni URL seule ne suffit. » : « Si la date injectée par l'application diffère de DATE_EDITION_PARIS, DATE_EDITION_PARIS prévaut. »

**Correctif 4, `COMMANDES.md`, commande 3.** Remplacer « Texte intégral ou pièce jointe : [contenu] » par : « Texte intégral joint en fichier texte à cette conversation : [nom du fichier]. Avant de qualifier INTEGRAL_FOURNI, indique pour chaque fichier le mode d'accès que ton listing t'attribue, contexte complet ou passages ; en mode passages, dis-le et ne prétends pas avoir lu l'ensemble. » Ajouter en note sous la commande : « Fournir les textes dans la conversation qui finalise, pas plusieurs échanges plus tôt : l'application résume l'historique ancien. »

**Correctif 5, `COMMANDES.md`, commande 2.** Ajouter après le bloc A : « [COLLER ICI LA LISTE COMPACTE DES ÉVÉNEMENTS DES DEUX DERNIÈRES ÉDITIONS : titre, date, URL] ».

**Correctif 6, `projet/02-HISTORIQUE.md`, sections B3, C et D.** Remplacer chaque tableau par une liste à champs nommés. Exemple pour D :

```markdown
### Édition 2026-10-02
- Fenêtre réelle : articles publiés du 28 septembre au 1er octobre 2026
- URL figée : https://bacoco.github.io/revue-presse-snum/editions/2026-10-02/
- Preuve de publication : commit cbb60ee50ff539b49593c664625075e09f0dc426 ; vérification humaine à dater
- Preuve d'envoi : 2 octobre 2026, 10:13 Europe/Paris, un message, six destinataires, confirmation humaine
- État : COMPLETE
```

**Correctif 7, `projet/01-MODELE-EDITORIAL.md`, dossier privé, « Contrôles éditoriaux ».** Remplacer le tableau par : « Écarts constatés après relecture de chaque fiche et des trois essentiels (plafonds, une phrase par champ, trois à cinq mots-clés, source, date, URL, réserves) : [liste des écarts corrigés ou restants ; "aucun" si rien]. Méthode de comptage : [sans outil / outil réellement utilisé]. »

**Correctif 8, `projet/03-PUBLICATION-DIFFUSION.md`, « Après push ».** Remplacer « Une lecture directe actuelle par l'assistant est utilisable si cette capacité existe. » par : « L'assistant ne lit pas les pages publiées : la vérification est humaine. » Dans « Courriel », ajouter : « Rechercher aussi l'ancien objet "Revue de presse SNUM - [date]" dans les messages envoyés. »

**Correctif 9, `00-LIRE-MOI.md`, « Installer », étape 4.** Remplacer par : « Initialiser 02-HISTORIQUE.md avec le bloc A proposé ci-dessous après l'avoir vérifié, puis coller en B2 et C les deux derniers comptes rendus publics du dépôt (`comptes-rendus/2026-10-02.md`, `comptes-rendus/2026-10-02-diffusion.md`, `comptes-rendus/2026-09-25.md`). »

Aucune refonte n'est nécessaire : les défauts majeurs se corrigent par ces remplacements. La seule décision de structure, champ d'instructions condensé ou noyau V4 avec manuel en recherche documentaire, est tranchée par le correctif 0, pas par une réécriture.

## 7. Pilote minimal

Recette logique, à exécuter sur l'instance ; rien ci-dessous n'a été exécuté. Les durées sont des propositions à valider.

**Étape 0, plafond du champ d'instructions.** Coller un texte de 4 100 caractères, enregistrer, rouvrir : la coupe attendue est à 4 000. Puis coller le prompt condensé par le correctif 0 et demander à l'assistant de citer le dernier mot de ses instructions. Succès : le dernier mot est celui du fichier. Échec : la version déployée a un autre plafond ; l'ajuster avant toute suite.

**Étape 1, installation.** Créer le Projet, coller le prompt, importer les trois fichiers, attendre la fin de l'indexation (l'interface bloque l'envoi pendant l'indexation). Succès : aucune bannière d'échec d'indexation.

**Étape 2, diagnostic (commande 1).** Article de référence proposé : la publication ANSSI du 29 septembre 2026 sur la DGFiP, déjà utilisée par l'ancien dispositif comme page publique. Observations attendues : plafonds restitués, registre version 2, borne restituée, « 120 agents » et « trois mois » retrouvés dans `01`, description des capacités, et surtout le type de contenu Web réellement reçu : extraits, passages ou résumé. Échec : une donnée inventée, ou l'affirmation d'une lecture intégrale.

**Étape 3, initialisation de l'historique.** Bloc A proposé, à vérifier par le propriétaire avant usage ; les preuves sont tirées des comptes rendus publics et de ma lecture de l'accueil le 13 octobre, qui affiche « Revue de presse du 2 octobre 2026 » :

```text
REGISTRE_VERSION : 2
DATE_EDITION_PARIS : [date du lancement]
FENETRE_DEMANDEE : 2026-10-02 au [veille du lancement], journées civiles Europe/Paris
DERNIERE_EDITION_REUSSIE : 2026-10-02
DERNIERE_FIN_COLLECTE_REUSSIE : 2026-10-01 (articles publiés du 28 septembre au 1er octobre selon le compte rendu public)
PRECISION_BORNE : journées complètes
DERNIERE_EDITION_PUBLIEE : 2026-10-02 ; commit cbb60ee50ff539b49593c664625075e09f0dc426 ; accueil affichant cette date le 13 octobre 2026 (vérification du relecteur, à refaire par le propriétaire)
EDITION_DU_JOUR : aucune établie
PUBLICATION_DU_JOUR : non effectuée
DIFFUSION_DU_JOUR : non effectuée
BROUILLON_ACTIF : aucun
PROCHAINE_ACTION : première édition pilote sur la fenêtre déclarée
```

Preuve d'envoi du 2 octobre : compte rendu public de diffusion, un message à 10:13 Europe/Paris, six destinataires, libellé SENT, sur demande explicite. À attribuer à ce document, pas à une vérification de la messagerie.

**Étape 4, première édition pilote.** Lancer la commande 2 avec la fenêtre depuis le 2 octobre. Mesurer : candidats examinés ; sujets admissibles sans texte fourni ; textes demandés et fournis ; temps de fourniture ; dates sans provenance ; respect des plafonds ; événements doublonnés avec l'édition du 2 octobre. Succès : au moins trois sujets solides, aucune lecture intégrale affirmée sans texte, aucune date inférée, dossier privé complet. Échec : une source déclarée complète à tort, un doublon publié, un état inventé. Durée proposée à valider : une demi-journée, fourniture des textes comprise.

**Étape 5, relais humain.** HTML sur le gabarit réel, contrôles avant commit, publication, vérification des cinq pages, contrôle des messages envoyés, envoi. Mesurer le temps et les demandes de pièces manquantes. Succès : SHA fourni, pages vérifiées et datées, un message, preuves consignées.

**Étape 6, seconde édition pilote.** Reprendre avec le bloc A produit par la première. Succès : borne avancée à la fin de collecte, pas à l'heure d'envoi ; événements de la première édition dédoublonnés ; aucun second envoi. Échec : perte de borne, double production, renvoi.

Critère global, repris de la recette : une seule source faussement déclarée complète ou un seul succès fictif impose correction et nouvelle vérification du cas, sans généralisation.

## 8. Décision finale

Corriger d'abord, puis tester, puis arrêter d'écrire. L'ordre : ramener le champ d'instructions sous 3 900 caractères (correctif 0), appliquer les neuf correctifs locaux, puis lancer les deux pilotes avec les mesures ci-dessus. Une réécriture de fond n'est pas justifiée : le plafond impose une condensation du prompt, pas un changement d'architecture.

Recommandation sur la V4 en cours : son motif est fondé, sa forme ne l'est pas. Un noyau de quelques centaines de caractères qui renvoie à un manuel lu par recherche documentaire, quatre passages par requête, expose chaque règle critique au risque de non-récupération que la V3 voulait éviter. Préférer un champ d'instructions plein, proche de 3 900 caractères, qui garde toutes les règles d'état, d'anti-doublon, de période, de sources et de livraison, et ne déplacer vers les documents que le format détaillé, le relais HTML et le courriel, déjà présents dans `01` et `03`.

Ce qui manque pour une conception excellente : dire sans détour que le mode normal est la fourniture humaine des textes ; traiter la datation et le résumé d'historique ; remplacer les tableaux par des listes ; guider l'initialisation avec les données publiques ; décider du sort de la série des comptes rendus publics.

Ce qui manque pour une validation de fonctionnement : les deux pilotes, avec le temps humain mesuré, la proportion de sujets réellement lus en entier, et la fidélité de la reprise d'état. Tant que ces mesures n'existent pas, aucune note de fonctionnement n'est possible, et le temps humain réel est l'inconnue qui décidera si ce dispositif vaut mieux que l'ancien.

## Limites de cette revue

- Code lu à un SHA daté ; le frontend lu au SHA de l'amont ; l'instance et sa version ne sont pas inspectées.
- Le moteur Web configuré sur l'instance est inconnu ; la taille des passages renvoyés par Albert n'est pas visible dans le code lu.
- Le plafond de 4 000 caractères est vérifié dans le code au SHA cité ; la version déployée peut différer.
- Le comportement du modèle face aux consignes n'est pas observé ; l'obéissance n'est jamais déterministe.
- La V4 et la V5 n'ont pas été évaluées ; seuls leurs faits de structure sont décrits.

## Passe PDG, auto-vérification

Auto-vérification PDG, pas une revue indépendante.

PDG-LARGE-FILE-JUSTIFICATION: le prompt de validation exige huit sections dans un seul document autonome (verdict, matrice, défauts, correctifs, pilote) ; découper nuirait à la lecture linéaire demandée pour un usage au lecteur d'écran.

- Déclenchement : oui, revue avec note et correctifs destinés à être appliqués par une autre personne ou un autre agent.
- Artefacts inspectés : listés en « Cadre et preuves » ; `chat/serializers.py` et le composant de saisie ont été ajoutés pendant la passe.
- Correction apportée par la passe : la première version de ce rapport affirmait que la troncature n'était pas reproduite dans le code. Un grep sur plusieurs motifs, coupé après six lignes, avait masqué `maxLength={4000}` derrière des occurrences banales du mot « instructions ». La relecture ciblée a trouvé le plafond côté API et côté interface ; verdict et note ont été corrigés.
- Matrice des affirmations majeures, chacune avec sa source et son verdict :
  - instructions de Projet injectées en instruction dynamique : `pydantic_ai.py` lignes 400 à 411 et test dédié ; confirmé ;
  - plafond de 4 000 caractères : `chat/serializers.py` lignes 370 à 378, `ModalProjectForm.tsx` ligne 755 ; confirmé ;
  - prompt V3 de 6 229 caractères : annexe B extraite, comptage `wc -m` ; confirmé ;
  - fichiers de Projet jamais inclus en entier : `document_context_builder.py` lignes 50 à 53, 102 à 104, 123 et 124 ; confirmé ;
  - pièces jointes de conversation incluses sous budget FIFO : même fichier, lignes 159 à 199 ; confirmé ;
  - aucun mode Web ne transmet le texte complet : `web_search_brave.py` lignes 270 à 296, 298 à 335, 359 à 413 ; `web_search_staan.py` lignes 119 à 167 ; confirmé pour le code, moteur de l'instance inconnu ;
  - Brave sans date, Staan avec date : mêmes fichiers ; confirmé ;
  - résumé d'historique, seuil et fenêtre : `settings.py` lignes 574 à 600 et 768 à 792 ; confirmé ;
  - quatre passages, seuil 0,6 : `base_rag_backend.py` ligne 203, `albert_rag_backend.py` lignes 228 et 229 ; confirmé ;
  - aucun AGENTS.md ni mécanisme : arbre amont non tronqué, 1 245 chemins, modules lus ; confirmé ;
  - plafond de dix fichiers : `settings.py` lignes 646 à 650 ; confirmé ;
  - date serveur UTC : `settings.py` ligne 267 et `conversation.py` ; confirmé ;
  - site : DSFR 1.15.2, accès rapides, statut, déclaration : pages téléchargées le 13 octobre ; confirmé ;
  - ancien dispositif avec connecteurs GitHub et Gmail, fenêtre du 28 septembre au 1er octobre, envoi à 10:13 : comptes rendus publics du 2 octobre, `chatgpt-write-proof.txt`, commit `cbb60ee5` daté du 2 octobre à 08:07 UTC par l'API GitHub ; confirmé comme preuve rapportée par le dépôt, cohérente avec l'API ;
  - automatisations non supportées : guide DINUM ; confirmé ;
  - mode complet sous « environ 5 pages » : guide DINUM ; confirmé comme documentation, pas comme code.
- Inconnues restantes : version et configuration de l'instance ; moteur Web configuré ; taille des passages Albert ; comportement du modèle ; état final de la V4 et de la V5.
- Contraintes pour qui applique les correctifs : MUST attendre la stabilisation du kit et les appliquer sur la version active ; MUST NOT modifier les fichiers du kit pendant qu'un autre agent y écrit ; MUST mesurer le champ d'instructions avec `wc -m` avant de coller ; MUST NOT déplacer les règles d'état, d'anti-doublon, de période et de sources hors du champ d'instructions ; MUST NOT publier ce rapport ni les fichiers du kit dans le dépôt de revue.
- Preuve de régression requise : les deux pilotes de la section 7 ; aucun correctif n'est vérifié avant.
- Carte de validation humaine : fichier `validation-independante-kit-v3.md` ; à inspecter en priorité : section 0 et correctif 0 ; résultat attendu : décision entre V3 condensée et V4 ; risque accepté : revue fondée sur le code à un SHA daté, pas sur l'instance ; phrase d'approbation : « Approved after human validation. »

NOT VERIFIED : fonctionnement sur l'instance DINUM.
