# Rapport de vérification du kit SNUM V5.7

## Verdict

Le kit V5.7 permet à l’Assistant DINUM de lancer lui-même la recherche Web et de livrer un bloc HTML complet, y compris avec zéro événement admissible.

La production autonome d’une newsletter remplie n’est toutefois pas démontrée. Lors du test réel du 14 octobre 2026, le service de recherche Web a renvoyé des résultats, puis une erreur serveur ; l’Assistant a déclaré n’avoir pu ouvrir ni lire intégralement aucune URL. Il a donc produit une revue vide avec l’état `A_COMPLETER`. Ce comportement est honnête, mais la définition de réussite éditoriale n’est pas atteinte.

## Configuration vérifiée

- Projet DINUM : `newsletter_BGS`.
- Cinq fichiers Markdown de connaissance, tous à la racine.
- Recherche Web activée.
- Prompt système V5.7 installé dans « Instructions (expérimental) ».
- Aucun lot de sources fourni dans la conversation.
- Aucun générateur local utilisé pour la production.
- Aucune publication, aucun envoi et aucune planification exécutés.

Le prompt système final contient 3 910 caractères Unicode, hors saut final. Il dépasse la cible prudente initiale de 1 200 caractères, mais reste sous la limite de 4 000 caractères affichée par l’instance. Ce choix résulte du premier test : avec un prompt de 1 189 caractères, la récupération par passages n’a pas restitué fidèlement la coque HTML.

## Tests réels dans DINUM

### Premier test

Conversation : https://assistant.numerique.gouv.fr/chat/27cdd3ef-39f0-4c41-9c1b-a94d5d478dbd

Le prompt court a bien déclenché la recherche et la production d’un HTML, mais l’Assistant a reconstruit la page : accès rapides, navigation, classes, scripts et footer ne respectaient pas le gabarit attendu. Ce test établit que la présence du modèle dans la connaissance ne garantit pas sa récupération intégrale.

### Test final

Conversation : https://assistant.numerique.gouv.fr/chat/570e13f2-d463-4c5a-a2cb-667cdbca1759

Commande utilisée : celle de `NOTICE-V5.7.md`.

Résultat observé :

- la recherche Web a été lancée et l’interface a affiché cinq sources ;
- aucune lecture intégrale n’a été établie ;
- l’Assistant a signalé une indisponibilité temporaire du service de recherche Web ;
- aucun événement n’a été retenu ;
- la revue a reçu l’état `A_COMPLETER` ;
- un unique bloc HTML complet a été livré.

Le nombre de sources affiché par l’interface ne prouve pas que leur corps a été lu.

## Contrôles du HTML réellement produit

Contrôle structurel effectué sur le bloc exact de la réponse, sans le réécrire :

- longueur : 3 431 caractères ;
- doctype présent au début et fermeture `</html>` présente ;
- aucun marqueur `@@...@@` restant ;
- un seul `h1` ;
- trois accès rapides vers `#main`, `#navigation` et `#footer` ;
- navigation `id="navigation"` et footer `id="footer"` présents ;
- DSFR 1.15.2 chargé avec les scripts `module` et `nomodule` ;
- feuille de style absolue du site de Loïc présente ;
- six liens réglementaires présents ;
- section « Collecte à compléter » présente.

Ce contrôle prouve la fidélité à la coque compacte intégrée au prompt, pas au gabarit complet de `03-GABARIT-HTML.md`. Le modal d’affichage et une édition remplie n’ont pas été exercés. Aucun validateur Nu, audit RGAA complet ou contrôle visuel à 200 % n’a été exécuté sur cette sortie.

## Contrôles locaux du kit

- l’archive contient exactement les cinq Markdown attendus à sa racine ;
- le gabarit de connaissance ne contient aucune newsletter préremplie ;
- les invariants statiques du gabarit sont présents : accès rapides, navigation, footer, DSFR 1.15.2, scripts `module` et `nomodule`, mention d’accessibilité, liens réglementaires, `p.fr-tag` et modèles de cartes ;
- les fichiers Markdown ont passé le contrôle local des accents ;
- l’ancien parcours V5.6 fondé sur un lot de sources et un générateur local a été retiré du dispositif actif.

## Limite établie

Dans la session testée, DINUM ne peut pas produire de revue remplie conforme à partir de sa seule recherche Web, car aucune preuve de lecture de corps intégral n’a pu être obtenue. Cette observation porte sur l’instance et la session testées ; elle ne prouve pas une impossibilité universelle ou permanente.

Le meilleur parcours autonome actuellement vérifié est donc : recherche par DINUM, sélection seulement des corps réellement lus, rédaction quand ils existent, et livraison systématique du HTML avec une limite précise sinon. Une newsletter non vide, la fidélité des cartes remplies et la validation factuelle des articles restent `NON_VERIFIEES`.
