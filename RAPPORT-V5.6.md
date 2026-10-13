# Rapport de livraison du kit SNUM V5.6

## Résultat

La génération libre du HTML par DINUM est remplacée par un contrat simple : DINUM recherche, sélectionne et rédige la newsletter dans un JSON strict ; `generer_revue.py` valide ce JSON et produit la revue Markdown, le HTML fidèle au gabarit de Loïc et le dossier privé.

Une sortie réelle de l’Assistant DINUM a été obtenue le 14 octobre 2026 à partir du lot temporaire de cinq sources publiques intégrales déjà fourni dans la conversation. DINUM a sélectionné et rédigé trois événements, livré un JSON V5.6 de 3 286 caractères, puis le générateur l’a accepté sans correction manuelle. Les trois essentiels proviennent des mêmes trois événements de rubrique.

Cette preuve établit le chemin « rédaction DINUM vers livrables déterministes ». Elle ne certifie pas la qualité d’une collecte Web autonome sur une future fenêtre.

## Architecture livrée

Les cinq fichiers de connaissance sont :

1. `00-PROMPT-PROJET.md` : mission et progression ;
2. `01-ETAT-HISTORIQUE.md` : état daté, borne et événements déjà couverts ;
3. `02-METHODE-EDITORIALE.md` : collecte, admissibilité et format court ;
4. `03-FORMAT-SORTIE.md` : contrat JSON unique ;
5. `04-RELAIS-HUMAIN.md` : contrôles, publication, diffusion et historique.

Le prompt système est séparé. Le gabarit, le générateur, la commande et les tests restent hors connaissance. Aucun fichier de connaissance ne contient une édition préremplie.

## Capacités de l’Assistant examinées

Révision publique lue du dépôt `bacoco/conversations` : `febfb6f6b6f1fd904b2f82aed2971957d7a29ef4`.

Faits confirmés dans cette révision :

- les documents d’un Projet sont exposés comme outils et retrouvés par `document_search_rag` ;
- la récupération renvoie des passages, avec quatre résultats par défaut dans l’implémentation Albert ;
- la recherche Staan renvoie des blocs classés et non une garantie de corps intégral ; l’implémentation Brave peut récupérer davantage selon la configuration ;
- `PROJECT_FILES_MAX_COUNT` vaut dix par défaut et reste configurable ;
- aucune convention de chargement automatique d’un fichier `AGENTS.md` n’a été trouvée pour le mode Projet.

Faits observés dans l’instance le 14 octobre 2026 :

- le champ « Instructions (expérimental) » annonce une limite HTML de 4 000 caractères ; le prompt livré en utilise 1 188 hors saut final ;
- le sélecteur accepte notamment Markdown, texte, PDF, HTML et documents bureautiques, mais l’instance avait déjà refusé un CSS ;
- la recherche Web peut être activée dans la conversation ;
- DINUM a pu produire le JSON strict demandé depuis le contexte conversationnel et le lot fourni.

Inconnues : backend Web réellement activé sur cette instance, disponibilité constante du corps intégral, génération persistante de fichiers téléchargeables, réglage serveur exact du nombre de pièces et présence d’un ordonnanceur. Aucune planification automatique n’est supposée.

## Contrôles exécutés

- `ruff check` : réussi sur le générateur et les tests.
- `python3 -m unittest discover` : huit tests réussis.
- Cas négatifs : 26 mots, rubrique inventée, essentiels dupliqués, date hors fenêtre et URL non HTTPS sont refusés.
- Parcours réel : la sortie brute DINUM a produit quatre fichiers sans retouche.
- Nu : aucune erreur sur le HTML réel ; trois avertissements informatifs indiquent que les rôles explicites doublent les éléments sémantiques correspondants.
- Structure : doctype, fin HTML, h1 unique, trois accès rapides, rôles, trois cartes, trois articles, `p.fr-tag`, scripts DSFR, footer et absence de marqueurs vérifiés.
- CSS intégré : identique octet pour octet au `styles.css` de la révision Loïc épinglée ; SHA-256 `4ebf1634f57d2c6d04cb24a8995d0263e5714db649725c3d7503e39488db1bb8`.
- Accents : contrôle exécuté sur tous les Markdown livrés.

## Limites

Le générateur vérifie le contrat, les dates, les longueurs, la structure et l’échappement HTML. Il ne visite pas les sources et ne peut donc pas certifier leur accès public, leur lecture intégrale ni l’exactitude des faits.

Le contrôle visuel à 200 % et l’audit RGAA complet ne sont pas exécutés. Nu ne remplace pas un audit RGAA.

Le téléversement automatisé des cinq fichiers finaux dans le Projet de test a été refusé par l’extension Chrome, qui n’a pas l’accès aux fichiers locaux. Les anciens fichiers du Projet de test ont été retirés pendant le remplacement ; Alexandra doit donc importer manuellement les cinq Markdown du ZIP et coller le prompt final. Cette limite ne touche pas les fichiers locaux ni le dépôt.

Aucune publication GitHub Pages, aucun courriel et aucune planification n’ont été exécutés.

## PDG pass

Auto-vérification PDG, pas une revue indépendante.

- Décision de déclenchement : oui, car le contrat de sortie, le parcours d’installation et plus de trois fichiers changent.
- Compétence utilisée : `progressive-disclosure-guard`, puis contrôle d’applicabilité de `progressive-disclosure-doc` pour la documentation durable.
- Sources inspectées : cinq Markdown actifs, prompt système, gabarit, générateur, tests, HTML Loïc épinglé, CSS épinglé, sortie DINUM et fichiers pertinents de `bacoco/conversations` à la révision indiquée.
- Chevauchement : remplacement de la génération HTML existante ; aucun second générateur local préexistant à étendre.
- Affirmation confirmée : DINUM sait produire le JSON demandé ; preuve par la réponse réelle extraite et acceptée.
- Affirmation confirmée : le générateur produit le HTML attendu ; preuve par la commande réelle, Nu et les contrôles structurels.
- Affirmation partielle : la fidélité visuelle ; CSS et structure sont vérifiés, mais aucun contrôle visuel à 200 % n’est exécuté.
- Affirmation inconnue : autonomie future de la collecte Web intégrale ; le backend et sa configuration de production ne sont pas établis.
- Fichiers matériels non lus : aucun parmi ceux utilisés comme preuve ; l’inspection du dépôt `conversations` est bornée aux chemins qui implémentent pièces de Projet et recherche Web.
- Connu : limite de cinq fichiers visée, prompt séparé, sortie JSON, rendu déterministe, relais humain.
- Inconnu : accès constant aux corps intégraux, génération téléchargeable et ordonnanceur.
- Hypothèse auparavant cachée et désormais interdite : une longue coque récupérée par passages serait reproduite sans dérive.
- Risque résiduel : un JSON formellement valide peut encore contenir un fait ou une preuve de lecture inexacts.
- Mauvais chemin : laisser DINUM reconstruire, simplifier ou corriger directement le HTML.
- Garde-fou : clés exactes, valeurs fermées, longueurs, dates, URLs, échappement, empreinte du gabarit et tests négatifs.
- Comportement préservé : DINUM reste l’auteur de la sélection et de la rédaction ; le relais publication et courriel reste humain.
- Raccourcis interdits : édition préremplie, faux contrôle, article payant, correction manuelle silencieuse du JSON ou du HTML.
- Preuve de régression requise et exécutée : sortie réelle DINUM vers quatre livrables, huit tests, Nu et contrôle d’intégrité CSS.

Le moteur PDD n’est pas installé dans ce projet et aucun dossier `.pdd` n’y existe. Son installation aurait élargi la mission ; aucun inventaire ou reçu PDD n’est donc revendiqué.
