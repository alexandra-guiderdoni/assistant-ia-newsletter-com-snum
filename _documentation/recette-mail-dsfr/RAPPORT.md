# Recette du rendu de courriel DSFR

Date : 21 octobre 2026.

## État courant

**GO sur l’autonomie structurelle et aperçu confirmé par l’utilisateur ; qualification du poste de la collègue encore ouverte.** Le fichier [outil-rendu-dsfr.html](../../outil-rendu-dsfr.html) contient toutes ses ressources. Après remplacement du chargement de l’iframe par le fichier Blob utilisé pour le téléchargement, l’utilisateur confirme : « là ca marche ». Cette observation clôt le signalement d’aperçu absent sur son poste. La cause initiale reste inconnue ; le téléchargement natif, la réouverture et Outlook ne sont pas qualifiés par cette confirmation.

L’utilisateur a accepté ce parcours après trois essais non fidèles dans l’Assistant. Les instructions, ressources et archives des deux Projets historiques sont préservées.

**NO-GO pour le Projet Assistant expérimental.** `Newsletter SNUM - rendu DSFR` reste installé avec les neuf ressources, mais les trois essais réels ont altéré le logo. Aucun nouvel ajustement du prompt n’a été lancé.

Le choix métier reste un courriel autonome avec le logo original incorporé en base64. Le parcours accepté est désormais Collecte → fichier autonome → téléchargement du mail, sans terminal ni conversation de rendu supplémentaire.

## Validation du fichier seul sous le cadre ShipGuard

Demande : outil entièrement autonome, copiable seul sur le poste de la collègue. Le cadre `sg-mission-lock` a borné l’audit à cette demande ; il ne constitue pas un moteur de test ou une certification. Les preuves viennent de l’inspection de l’artefact et de sondes indépendantes. Le produit, les tests et les réglages des navigateurs n’ont pas été modifiés pour cette validation.

La relecture indépendante portait sur l’artefact de 43 752 octets, empreinte `bb091b9f0f60c4c53f74ae5b72476840b9cbebfd9144167c11774f4ba29e8083`. Après cet audit, une correction demandée par l’utilisateur a déplacé les alertes de Collecte hors du mail. La suite complète et la copie isolée ont été contrôlées de nouveau pour cette correction ; aucune nouvelle qualification de navigateur n’est acquise.

| Affirmation | Source | Verdict | Impact |
| --- | --- | --- | --- |
| Interface, styles, moteur, modèle et logo sont dans le HTML | Inventaire de l’artefact distribué | Confirmé par inspection | Un seul fichier à transmettre |
| Le poste métier a besoin du dépôt, de Python, de Node ou d’un serveur | Scripts intégrés et exécution isolée | Réfuté dans le périmètre inspecté | Aucun de ces éléments à installer chez la collègue |
| La génération charge des ressources techniques sur Internet | Inventaire de l’outil et des mails produits ; VM sans API réseau | Aucun chargement détecté | Autonomie des ressources ; les liens éditoriaux restent des liens |
| Le logo complet est conservé | Extraction et décodage de l’image produite | Confirmé, 12 032 caractères base64 et 9 024 octets | Pas d’image annexe à fournir |
| L’interface prépare le bon téléchargement | Événements DOM et contenu du Blob contrôlés | Confirmé en simulation | Préparation correcte ; téléchargement natif non exercé |
| L’aperçu s’affiche sur le poste de l’utilisateur | Confirmation humaine après le changement vers une URL Blob | Confirmé par l’utilisateur | Signalement d’aperçu absent clos sur ce poste |
| Le téléchargement et la réouverture fonctionnent sur le poste de la collègue | Aucun essai réel sur ce poste | Inconnu | Qualification du poste cible encore nécessaire |

### Preuve de portabilité exécutée

Une copie renommée du seul HTML a été placée dans un dossier temporaire vide, sans copie du dépôt ni fichier annexe. Son empreinte correspond à celle de l’original. Les scripts intégrés ont été exécutés avec Node depuis ce dossier, avec le harnais de test transmis en mémoire : paquet fourni et paquet vide, aperçu assigné, Blob exact, erreurs et invalidation de la sortie précédente. Résultat : succès. L’inventaire de l’application et des deux mails produits ne détecte aucune ressource technique externe et aucun script dans les mails exportés.

Une seconde sonde, exécutée par le relecteur en lecture seule depuis le répertoire `/`, a lu uniquement l’artefact. Les scripts ont été évalués dans une VM sans `require` ni `fetch`, avec des données synthétiques : paquet vide et article contenant du HTML hostile et une date hors fenêtre. Génération, échappement, logo complet, Blob exact et invalidation réussissent. Aucun défaut produit P0/P1/P2 n’a été prouvé dans ce périmètre.

L’artefact ne contient aucune référence au chemin du poste de développement, à `_source/`, à `scripts/`, à un serveur local ou à un stockage persistant du paquet. Le navigateur reste le moteur nécessaire à son utilisation ; les politiques du poste cible et le téléchargement natif n’ont pas été exercés. Les sondes Node ne constituent pas une installation ni une navigation réelle sur un autre poste.

### Condition restante pour la livraison

Sur le navigateur autorisé du poste cible, avec le seul fichier HTML et hors connexion :

1. Ouvrir le fichier, coller un paquet valide et cliquer sur « Prévisualiser le mail ».
2. Constater l’aperçu des articles et le logo visible.
3. Télécharger le mail, puis rouvrir le fichier obtenu et constater le contenu et le logo.

L’aperçu a été confirmé sur le poste de l’utilisateur ; l’essai sur celui de la collègue reste nécessaire. Aucun défaut CSP n’est établi comme cause initiale. Les textes normatifs [CSP](https://www.w3.org/TR/CSP3/), [iframe et srcdoc](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#attr-iframe-srcdoc), [sandbox](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#attr-iframe-sandbox) et [origine des URL](https://url.spec.whatwg.org/#origin) ont été consultés par le relecteur ; ils décrivent les mécanismes et ne prouvent pas leur exécution sur le poste.

## Outil autonome

Le fichier distribué contient le canon, le moteur JavaScript et l’interface. La génération ne fait aucun appel à un modèle ou à un service distant. Le paquet est conservé uniquement dans la mémoire de la page. Les données textuelles sont échappées et l’aperçu est isolé dans une iframe sans permission de script.

- Fichier : `outil-rendu-dsfr.html`, 44 363 octets.
- Empreinte SHA-256 : `4502a88d25c20def043aded4ed82512d83981e4c68db536315221d2221af9cad`.
- Génération : `python3 scripts/build_mail_tool.py` ; contrôle reproductible avec `--check`.
- Sources : `_source/mail-tool-shell.html`, `_source/mail-tool-render.js` et `_source/mail-tool-ui.js`, alimentées par `_source/30-BLOCS-MAIL-DSFR.md`.
- Dépendances du poste métier : navigateur avec JavaScript ; aucun paquet ni installation supplémentaire.

Les tests exécutent les scripts du fichier distribué dans Node.js. Dix variantes produisent un HTML identique, octet pour octet, au moteur Python de référence : le paquet fourni, des paquets de 0, 1, 2, 3, 18 et 60 articles, un paquet vide avec alertes, un paquet avec HTML hostile et textes longs, et une date d’édition avec jour de la semaine. Chaque variante passe avec JSON brut et avec marqueurs. Un bloc JSON entouré de clôtures Markdown est également accepté.

Le PNG de 9 024 octets est conservé exactement dans chacune de ces sorties. Les dates hors fenêtre restent normales. Les rubriques s’adaptent aux données et aucun article n’est dupliqué pour les essentiels.

La simulation du DOM exerce l’aperçu, le contenu exact du Blob à télécharger, son type et son nom de fichier, les erreurs, le retrait de l’ancienne sortie après modification, ainsi que le cycle de sortie et de retour sur la page. Vingt paquets non conformes et trois entrées incomplètes sont rejetés. Il s’agit de contrôles de scripts, pas d’un téléchargement natif ni d’une recette visuelle dans un navigateur.

### Alertes de Collecte réservées à l’expéditeur

Les rubriques sans article sont omises du mail. Les objets `watch` sont uniquement présentés sous « Commentaire sur la collecte (hors mail) », en dehors des deux panneaux de génération. Leurs textes sont affectés par `textContent` et ne sont jamais insérés dans l’aperçu, le fichier téléchargé ou ses commentaires HTML. Une modification de l’entrée retire également ces remarques pour éviter un commentaire périmé. Collecte et le Rendu HTML historique restent inchangés.

Le nouveau test a d’abord échoué sur « Alertes présentes dans le mail », puis réussi après la correction des deux moteurs mail. La simulation vérifie la présence des remarques dans l’outil et leur retrait lorsque l’entrée change. La copie renommée du seul HTML dans un dossier vide passe également avec le paquet fourni et un paquet vide.

### Affichage de l’aperçu confirmé par l’utilisateur

Le bouton Télécharger visible confirme que le chemin de génération atteint la préparation du fichier. Pour isoler le chargement de l’aperçu, l’iframe utilise désormais `src` avec exactement la même URL Blob que le téléchargement ; elle n’utilise plus `srcdoc`. À la remise à zéro, les anciens attributs sont retirés avant révocation de l’URL. L’isolation sandbox, la politique CSP et le fonctionnement hors connexion restent inchangés.

Le test du nouveau contrat vérifie l’identité entre l’URL de l’aperçu et celle du téléchargement, le contenu exact du Blob et le retrait de l’ancienne source après modification. Il a échoué sur la version précédente, puis réussi après le changement. La suite de 53 tests et les contrôles de génération passent.

Ce test ne reproduit pas le chargement réel d’une iframe dans le navigateur. Le changement est une variante ciblée de compatibilité, pas la preuve que `srcdoc` ou la CSP étaient la cause. La prise en main automatique du fichier local restant interdite, l’utilisateur a effectué l’essai et confirmé le fonctionnement après rechargement et nouvelle génération. Cette preuve humaine complète les tests simulés, sans les transformer en essai automatisé du navigateur.

## Essais dans l’Assistant

Pendant les essais, le service affichait « Trafic élevé – service dégradé ». Ce message ne permet pas d’attribuer la cause des altérations au service.

| Essai | Entrée et variante | Observation | Verdict |
| --- | --- | --- | --- |
| [01](https://assistant.numerique.gouv.fr/chat/34cadad4-708a-40af-a683-9840b4305c3c) | Les cinq articles fournis ; six fragments de coque contenant le logo | HTML réparti hors du bloc attendu ; logo réduit à 1 095 caractères base64 | Échec de la comparaison canonique |
| [02](https://assistant.numerique.gouv.fr/chat/4a620bd9-b12a-402d-b9bb-63fac01eb9c9) | Paquet vide ; trois fragments de coque et trois fragments dédiés au logo | Un bloc HTML complet ; état vide présent ; image de 904 octets au lieu de 9 024 | Échec : logo altéré |
| [03](https://assistant.numerique.gouv.fr/chat/fe3c3781-6753-4622-a581-97f84482d925) | Paquet vide ; mêmes données du logo réparties en lignes de 76 caractères, avec instruction de concaténation | Réponse terminée ; un bloc HTML complet ; image de 904 octets, avec les mêmes dimensions et la même empreinte que dans l’essai 02 | Échec : logo altéré |

Le PNG attendu mesure 142 × 63 pixels, occupe 9 024 octets et correspond à 12 032 caractères base64. Son empreinte SHA-256 est `848c52ae1b7ce86593bb10b6351beebcd74c5b90c63258c1b82ac740912012fb`.

La réponse du deuxième essai cite les neuf ressources, mais cela ne prouve pas que leur contenu intégral était disponible au modèle. La cause exacte de la mauvaise reproduction reste inconnue. Les mentions de réussite produites par l’Assistant lui-même ne constituent pas une preuve de fidélité.

### Captures conservées

- `essai-01.txt` : texte obtenu par le bouton Copier de la réponse ; la mise en forme Markdown peut différer de la présentation affichée.
- `essai-01.html` : document extrait de cette capture, rejeté par le comparateur canonique.
- `essai-01-kit.zip` et `essai-01-ressources/` : conservation de la première variante essayée.
- `essai-02-metriques.json` : mesures de la sortie affichée et empreinte de son image. Le HTML intégral de ce deuxième essai n’a pas été enregistré sur disque.
- `essai-03-metriques.json` : mesures de la troisième réponse terminée et comparaison de son image à l’original. Son HTML intégral n’a pas été enregistré sur disque.

## Preuves locales

- Suite complète : **53 tests réussis**, dont dix tests du canal mail et quatre tests de l’outil distribué. Les cas exercés comprennent le paquet fourni, les paquets vides avec et sans alertes, les cinq rubriques, les données HTML échappées et des valeurs longues.
- La date hors fenêtre est acceptée dans le mail et toujours rejetée dans le Rendu HTML historique.
- La coque et le logo sont reconstitués exactement à partir des fragments générés ; les retours à la ligne des ressources du logo sont retirés avant comparaison.
- Le comparateur rejette une modification de couleur, de logo, de masquage des flèches, la suppression du type de document, la perte d’une espace significative et un suffixe HTML incomplet.
- Ruff, `build_split_kit.py --check`, `build_mail_kit.py --check`, `build_mail_tool.py --check` et `git diff --check` réussissent.
- Les empreintes des onze artefacts historiques protégés correspondent à celles relevées avant les modifications.
- Les instructions installées correspondent au prompt local, après normalisation du saut de ligne final. Le prompt local contient 3 754 caractères ; chacune des neuf ressources reste sous 4 500 caractères.

Les espaces des fragments HTML, les captures et les instantanés de référence sont conservés sans nettoyage pour préserver leur identité. Les exceptions de contrôle des espaces sont limitées à ces fichiers de données dans `.gitattributes` ; les scripts ne bénéficient d’aucune exception.

## Relecture indépendante

Une relecture en lecture seule a signalé deux défauts de priorité P2 du comparateur : une espace significative supprimée pouvait passer, ainsi qu’un suffixe incomplet après la fermeture du document. Ces deux faux positifs ont été reproduits, corrigés et ajoutés aux cas négatifs du test public. La suite de 49 tests passe après correction. Aucun problème P0 ou P1 n’a été signalé par cette relecture.

Ce retour ne vaut pas approbation indépendante du comportement de l’Assistant : les sorties hébergées restent à comparer au canon.

La relecture complémentaire de l’outil autonome n’a signalé aucun P0/P1 et a relevé un P2 conditionnel : un lien visible pouvait pointer vers une URL révoquée après un retour depuis le cache de navigation. Un test rouge a reproduit le défaut ; le gestionnaire `pagehide` lance désormais la réinitialisation de la sortie et du statut. Le test vérifie aussi la préparation d’un nouveau téléchargement après le retour. Le relecteur a confirmé la clôture de ce constat en exécutant le test ciblé sur le fichier distribué. Cette confirmation reste limitée à la simulation Node, sans navigateur.

## Projets conservés pour la démonstration

Après confirmation de la suppression définitive, dix anciennes versions SNUM ont été retirées dans l’Assistant : huit variantes de Collecte et deux de Rendu HTML. La liste visible contient désormais ces trois projets SNUM :

- `Newsletter SNUM - Collecte - v5.23.6` : instructions identiques avant et après le ménage ; deux ressources présentes ;
- `Newsletter SNUM - Rendu HTML - v5.23.6` : instructions identiques ; quatre ressources canoniques présentes ;
- `Newsletter SNUM - rendu DSFR` : neuf ressources présentes ; candidat expérimental toujours non validé pour le rendu fidèle du logo.

Les deux autres projets sans lien avec la newsletter ont été préservés. Aucun nouveau message ni changement d’instructions n’a été effectué pendant ce ménage. Pour la démonstration DSFR, le parcours éprouvé reste Collecte → outil autonome.

## Décision et contrôles restants

- Les trois variantes essayées sont insuffisantes ; ne pas relancer de réglage du prompt sans nouvelle hypothèse étayée.
- L’utilisateur a accepté l’outil autonome recevant le même JSON. La notice et le README décrivent ce parcours ; les deux Projets historiques restent inchangés.
- Le logo original en base64 reste une contrainte ; aucune image distante ni substitution du logo n’est autorisée.
- L’aperçu est confirmé par l’utilisateur ; exercer encore le téléchargement natif et la réouverture sur le poste cible.
- Qualifier le transport du logo et le rendu dans l’Outlook de l’administration avant diffusion.
- Capitalisation proposée, à valider : une fiche `why-inbox` sur le choix d’un moteur déterministe après les trois échecs de reproduction du gabarit. Aucune fiche de décision n’a été créée.

## Limites

Les tests déterministes ne prouvent pas le comportement de l’Assistant. La comparaison des dix variantes ne couvre pas tous les paquets possibles et ne prouve pas la lisibilité visuelle des textes très longs. Aucun envoi ni rendu dans un message Outlook n’a été exercé.

La tentative antérieure d’ouverture d’un aperçu HTML local a été rejetée automatiquement par la politique du navigateur : seuls les protocoles HTTP et HTTPS sont autorisés. Aucun contournement n’a été tenté et aucune nouvelle tentative automatique d’ouverture locale n’a été faite pour l’outil. L’affichage a été confirmé par l’utilisateur. L’application réelle de la CSP, les interactions au clavier et le téléchargement natif restent non vérifiés par l’automatisation.

Aucun envoi de courriel ni changement des instructions des projets conservés n’a été effectué pendant cette recette. L’historique Git et le contexte de reprise du dépôt permettent de contrôler la publication des fichiers ; le nettoyage des projets hébergés est tracé ci-dessus.
