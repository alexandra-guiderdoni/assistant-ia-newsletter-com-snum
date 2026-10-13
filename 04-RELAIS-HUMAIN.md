# Relais humain, publication et diffusion - V5.6

Ce fichier ne sert pas à la production quotidienne. Le consulter seulement après génération locale réussie ou sur demande explicite du propriétaire. L’Assistant DINUM ne dispose d’aucun outil GitHub d’écriture, de messagerie ou de planification démontré.

## Contrôles avant relais

Le générateur local contrôle le JSON, le format court et la structure HTML. Il ne prouve ni l’accès public actuel aux sources ni l’exactitude factuelle, et Nu ne constitue pas un audit RGAA. Avant commit, vérifier sur le fichier produit : validité HTML, liens internes, trois accès rapides et leurs cibles, h1 unique, footer réglementaire, mention et déclaration d’accessibilité, nouvelles fenêtres, articles et dates.

Conserver `Accessibilité : non conforme` tant qu’aucun audit RGAA complet, valide et publié ne permet un autre niveau. Un contrôle visuel non exécuté reste `NON_EXECUTE` ; son absence ne devient ni une réussite ni une interdiction automatique de publication.

## Publication GitHub Pages

Une personne autorisée :

1. crée `editions/AAAA-MM-JJ/index.html` sans réécrire une édition antérieure ;
2. remplace l’accueil par cette édition avec les chemins adaptés ;
3. ajoute l’édition en tête des archives sans supprimer les entrées antérieures ;
4. conserve les styles et pages réglementaires ;
5. commite et pousse sur `main`, puis note le SHA réel ;
6. vérifie après déploiement l’accueil, l’URL figée, les archives, l’accessibilité, les mentions légales et le plan du site.

Un push ne prouve pas le déploiement. DINUM fournit les fichiers et le relais humain ; il ne prétend aucune action externe.

## Courriel privé

Après publication réellement vérifiée, une personne autorisée recherche d’abord l’édition dans les messages envoyés. Si un envoi existe ou si le résultat est incertain, aucun renvoi automatique.

Le message comporte un destinataire principal, les cinq autres destinataires visibles en copie, aucun Cci et aucune newsletter jointe. Son corps contient seulement une courte introduction, trois puces correspondant aux essentiels et le lien de l’accueil public. Les adresses restent privées et ne figurent jamais dans le HTML ou le dépôt public.

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

## Historique après preuves

Conserver pour chaque édition : identifiant, fenêtre réelle, événements publiés, regroupements et exclusions, contrôles exécutés, SHA, URL figée, vérification Pages datée, anti-doublon de messagerie et preuve d’envoi. La borne de collecte réussie n’avance qu’après publication vérifiée et envoi confirmé.

Après réception de ces preuves, DINUM produit `01-ETAT-HISTORIQUE.md` complet actualisé. L’utilisateur remplace manuellement l’ancienne pièce ; aucune preuve plus récente ne doit être perdue.

Une correction publiée exige une demande explicite : conserver l’initiale, créer `revision-N`, vérifier cette publication et effectuer un anti-doublon propre avant au plus un message. Ne pas traiter cette correction comme une nouvelle collecte.
