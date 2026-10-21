# Contexte de session - Newsletter SNUM et rendu DSFR
> Sauvegarde du 21 octobre 2026. Lire l’état Git avant toute reprise.

## INVARIANTS

- working directory : `/Users/alex/Claude/git-hors-workflow/assistant-ia-newsletter-com-snum` ; branch : `main`.
- Dernier jalon antérieur à la livraison documentée : `ff2bbdaa0b2b7fb27181b63f4e686f159cd018f4`, publié ; divergence `0/0` vérifiée avant les écritures. Identifier le commit de la livraison présente avec `git log -1` et comparer son SHA au distant.
- Documentation et wiki : dépôt parent `/Users/alex/Claude`, commit `6cabc7486d10d92528333fa53f154bb307618208` publié sur sa branche `main` ; SHA distant relu.
- Préserver les onze artefacts historiques Collecte V5.23 et Rendu HTML V5.19 : empreintes inchangées.
- Le titre demandé est `Newsletter SNUM - rendu DSFR`, avec un tiret simple.
- Le mail reste autonome, avec logo original en base64, signature et flèches. Les articles hors fenêtre restent présentés normalement dans ce rendu seulement.
- Les trois adresses métier déjà présentes dans le pied de page peuvent être publiées dans ce dépôt : exception explicitement autorisée par l’utilisateur le 21 octobre, documentée dans `AGENTS.md`. Aucune autre adresse ou donnée personnelle n’est couverte.
- Préserver les autres worktrees et tous les fichiers étrangers au chantier. Le contexte global du workspace, consacré à un autre projet, n’a pas été remplacé.

## STATE

- [x] completed : outil `outil-rendu-dsfr.html` autonome, sans réseau ni stockage persistant du paquet ; prévisualisation et téléchargement préparés depuis le même Blob.
- [x] completed : les alertes `watch` sont affichées dans un commentaire réservé à l’expéditeur, hors aperçu et hors mail, sans commentaire HTML caché ; les rubriques sans article sont omises.
- [x] completed : 56 tests réussis, dont trois contrôles des livraisons ; contrôles des trois générateurs techniques réussis. L’outil HTML, son logo et les onze artefacts historiques sont préservés.
- [x] completed : aperçu confirmé par l’utilisateur après le passage de `srcdoc` à `src` avec URL Blob. La cause initiale n’est pas établie.
- [x] completed : dix anciennes versions SNUM supprimées dans l’Assistant après confirmation. Restent Collecte v5.23.6, Rendu HTML v5.23.6 et rendu DSFR ; instructions des deux premiers identiques, ressources présentes : 2, 4 et 9. Les deux projets sans lien avec la newsletter restent conservés.
- [x] completed : README, notice, rapport, notes de décisions et copies des trois pièces de départ versionnés ; commit produit publié et arbre propre.
- [x] completed : étude mail DSFR/Outlook et fiche workers publiées dans le dépôt parent ; compilation wiki et vues OKF actualisées.
- [x] completed : trois notices `INSTALLATION-*.md` et `MODE-OPERATOIRE.md` inclus dans les trois ZIP du dossier `livraison/`, avec exemple JSON ; le ZIP DSFR contient aussi l’outil et le candidat expérimental.
- [x] completed : prompt DSFR corrigé sur `watch`, ZIP technique DSFR régénéré et consigne enregistrée dans le Projet DSFR installé ; relecture après réouverture identique au texte préparé, neuf ressources présentes. Aucune nouvelle génération par le modèle.
- [x] completed : génération et contrôles des ZIP finaux ; relecture indépendante sans P0/P1/P2, GO limité au packaging. Pour la preuve de publication, comparer le commit contenant ce contexte au SHA de `origin/main`.
- [ ] pending : installation sur le poste de la collègue, téléchargement natif, réouverture et essai Outlook restent non vérifiés ; protocole inclus dans `MODE-OPERATOIRE.md`.

## DECISIONS

1. Après trois essais Assistant altérant le logo, conserver un rendu déterministe local : Collecte produit le JSON, l’outil applique le gabarit. Le Projet Assistant DSFR reste expérimental et non validé pour une reproduction fidèle du logo.
2. Le ménage a conservé les trois Projets SNUM sans changer leurs instructions. Le complément demandé ensuite porte uniquement sur la consigne `watch` du Projet DSFR, dans ses instructions locales et installées. Les deux Projets historiques et les deux projets étrangers restent préservés. Cela ne valide pas la reproduction du logo par le modèle.
3. Aucun Service Worker : le livrable fonctionne déjà hors connexion en fichier HTML. Aucun Web Worker : aucun calcul bloquant n’a été établi. La fiche wiki documente les mécanismes, sans ajouter de worker au produit.
4. Préserver les espaces littéraux des fragments HTML et des captures. Les exceptions `.gitattributes` sont limitées aux fichiers de données concernés ; les scripts restent contrôlés.
5. Le dossier builder initial n’a pas de dépôt autonome. Les deux études sont sauvegardées dans `docs/` du parent ; l’entrée et les deux HTML de travail sont copiés à l’identique dans `_documentation/reference-mail-dsfr/` du dépôt newsletter. Le modèle initial fourni par la collègue et le clone amont restent locaux et intacts.

## ARTIFACTS

- `outil-rendu-dsfr.html` : 44 363 octets, SHA-256 `4502a88d25c20def043aded4ed82512d83981e4c68db536315221d2221af9cad`.
- `_source/30-BLOCS-MAIL-DSFR.md` et `_source/mail-tool-*` : sources de maintenance ; scripts `build_mail_tool.py` et `build_mail_kit.py` pour les dérivés.
- `NOTICE-RENDU-DSFR-V1.0.md`, `README.md`, `_documentation/recette-mail-dsfr/RAPPORT.md` : parcours, preuves et limites.
- `livraison/` : les trois ZIP complets et `SHA256SUMS.txt`, assemblés par `scripts/build_delivery.py` et contrôlés avec `--check`. Les ZIP de la racine restent des archives techniques ; transmettre ceux de `livraison/`.
- `INSTALLATION-COLLECTE.md`, `INSTALLATION-RENDU-HTML.md`, `INSTALLATION-RENDU-DSFR.md`, `MODE-OPERATOIRE.md` : installation et usage sans terminal, distinction du candidat expérimental et recette du poste cible.
- `_documentation/recette-mail-dsfr/` : échecs Assistant et métriques ; ce sont des preuves conservées, pas les livrables métier.
- `_documentation/reference-mail-dsfr/` : entrée du 14 octobre et deux instantanés HTML issus du dossier builder.
- `/Users/alex/Claude/docs/recherche-mails-dsfr-outlook.md` et son annexe `recherche-mails-dsfr-outlook-sources.md` : étude initiale publiée.
- `/Users/alex/Claude/wiki/raw/veille/workers-service-workers-et-hors-ligne-2026-10-21.md` : fiche de 103 lignes, transcription synthétisée et documentation primaire citée ; neuf articles et trois connexions compilés, index et export actualisés.
- Contrôle wiki dans le worktree de recherche : PDD et OKF cohérents, aucune erreur de régression ou article sans source ; 183 avertissements de couverture conservés. Le reçu précédent en avait 171 ; les 12 supplémentaires correspondent à trois lacunes d’index déjà présentes dans les sources du dépôt et neuf références locales absentes de ce worktree. Aucun de ces avertissements ne vise les nouveaux articles workers. Le corpus ancien n’a pas été nettoyé.
- `/Users/alex/Claude-worktrees/recherche-mails-dsfr-outlook-20261021` : worktree documentaire conservé ; branche intégrée par avance rapide au parent, sans supprimer le worktree.
- Modifications étrangères préservées dans le parent : contrat ShipGuard, backlog et ses deux contrôles, présentation PDF non suivie, journal du jour et fiche PDF non suivis. Ne pas les inclure dans une sauvegarde newsletter.

## ERRORS FIXED

1. L’Assistant a produit trois logos non fidèles. Les deux derniers contenaient 904 octets au lieu des 9 024 attendus ; le moteur local insère le PNG original sans génération de la chaîne par un modèle.
2. L’aperçu restait absent malgré le bouton de téléchargement visible. Une URL Blob partagée entre l’iframe et le téléchargement a été adoptée ; le test de ce contrat est passé de rouge à vert, puis l’utilisateur a confirmé l’aperçu. Aucun défaut CSP n’est établi comme cause.
3. Les alertes de rubriques vides étaient dans le mail. Elles sont désormais réservées à l’opérateur, avec tests d’absence dans l’export.
4. Un lien pouvait rester visible après révocation au retour du cache de navigation : `pagehide` retire la sortie et son statut. Deux faux positifs du comparateur ont aussi été corrigés, pour les espaces significatives et les suffixes après le document.
5. Le contrôle final du diff indexé a révélé des espaces littéraux des captures et des fragments. Les données ont été préservées et les exceptions Git explicitées ; aucun script n’est exempté. Les fichiers Markdown compilés ont seulement perdu une ligne vide supplémentaire en fin de fichier.
6. L’audit final a révélé des ZIP sans notice, l’absence de livraison de l’outil autonome et une consigne `watch` obsolète dans le candidat DSFR. Les paquets documentés et la correction des instructions répondent à ces trois écarts ; le défaut de logo du candidat n’est pas déclaré résolu.

## NEXT

1. Vérifier `git status`, le dernier commit et `git ls-remote origin refs/heads/main` avant toute nouvelle action. Le présent contexte est sauvegardé après le commit produit mentionné plus haut.
2. Pour la démonstration DSFR : Collecte v5.23.6 → copie du paquet → ouverture de `outil-rendu-dsfr.html` → prévisualisation → téléchargement. Aucun terminal métier requis.
3. Qualifier le téléchargement et la réouverture sur le poste cible, puis le transport et le rendu dans Outlook avant de déclarer cette compatibilité acquise. Aucun envoi n’a été effectué.
4. Ne pas relancer le prompt expérimental sans nouvelle hypothèse. Ne pas réessayer l’ouverture automatique du fichier local refusée par la politique du navigateur, ni la contourner avec un serveur ou un autre outil.
5. À la prochaine modification fonctionnelle, lancer les tests et contrôles indiqués dans `AGENTS.md`. Aucun nettoyage des fichiers étrangers ou des anciens worktrees n’est autorisé par cette clôture.
