# Configurer l’Assistant DINUM pour la revue SNUM V5.12

Cette notice décrit le parcours métier sans script ni terminal. La newsletter et son HTML restent dans le chat. Le dispositif ne publie rien et n’envoie aucun courriel.

## Pourquoi la V5.12

La V5.11 retrouve désormais les onze fragments canoniques, mais sa recette réelle s’arrête au début de `RENDU` : elle contrôle les marqueurs des fragments bruts avant de fabriquer le document. La V5.12 ajoute `DONNEES` pour préparer toutes les valeurs éditoriales et impose l’ordre fabrication, correction, puis contrôle du HTML final.

La V5.12 conserve aussi :

- `CLE_EVENEMENT` pour reconnaître deux articles relatifs au même fait ;
- `DOUBLON_DE` pour expliquer quelle source a été écartée ;
- `CONTROLES_EN_ECHEC` pour expliquer tout arrêt `A_COMPLETER` ;
- l’état réussi `PRODUITE - contrôle métier requis`, distinct du jeton d’échec.

## Fichiers à utiliser

Télécharger :

1. `kit-dinum-snum-v5-12-progressif-9-fichiers.zip` ;
2. `PROMPT-SYSTEME-SNUM-V5.12.md`.

Après extraction, le dossier doit contenir exactement :

1. `00-PROMPT-PROJET.md` ;
2. `01-ETAT-HISTORIQUE.md` ;
3. `02-METHODE-EDITORIALE.md` ;
4. `05-INDEX-HTML.md` ;
5. `06-COQUE-DEBUT.md` ;
6. `07-PIED-DE-PAGE.md` ;
7. `08-BLOC-ESSENTIEL.md` ;
8. `09-BLOCS-RUBRIQUES.md` ;
9. `10-COQUE-FIN.md`.

Ne pas téléverser le ZIP, le README, la notice ou le prompt système comme ressources du Projet.

## Installer le Projet une seule fois

1. Ouvrir <https://assistant.numerique.gouv.fr/>.
2. Ouvrir le panneau de gauche.
3. Cliquer sur **Nouveau projet**.
4. Nommer le Projet `Newsletter SNUM`.
5. Copier tout le contenu de `PROMPT-SYSTEME-SNUM-V5.12.md` dans **Instructions (expérimental)**.
6. Vérifier que la dernière phrase est `N’affirme aucun contrôle non exécuté.`.
7. Ajouter les neuf fichiers Markdown listés plus haut.
8. Vérifier les neuf noms avant de créer le Projet.
9. Attendre la fin de l’indexation.
10. Démarrer une conversation depuis `Newsletter SNUM`, pas depuis **Vos conversations**.

Le prompt système mesure au plus 4 000 caractères. Les cinq messages suivants doivent rester dans la même conversation.

## Préparer les cinq dates

Exemple pour l’édition du 14 octobre 2026 couvrant la période du 3 au 13 octobre 2026 inclus :

```text
DATE_EDITION : 14 octobre 2026
DEBUT : 3 octobre 2026
FIN : 13 octobre 2026
DEBUT_ISO : 2026-10-03
FIN_ISO : 2026-10-13
```

Les accolades des modèles ci-dessous doivent être remplacées et supprimées avant l’envoi.

## 1. COLLECTE avec le Web

Activer **Rechercher sur le web**, puis envoyer :

```text
PHASE COLLECTE.
Utilise le Web.
Édition du {{DATE_EDITION}}.
Fenêtre du {{DEBUT}} au {{FIN}} inclus.
Ne rédige ni REVUE ni HTML.
Exécute au moins dix requêtes distinctes : deux par rubrique,
dont une générale et une ciblée, sur au moins cinq domaines.
Si la première passe produit moins de cinq candidats,
effectue une seconde passe sur d’autres sources officielles
ou spécialisées.
Réponds d’abord sous COUVERTURE_COLLECTE avec une ligne par requête :
rubrique | requête | domaine | résultat | URL ouverte.
Réponds sous CANDIDATS avec une liste numérotée.
Pour chaque candidat, indique :
- le titre ;
- l’URL canonique ;
- la date de publication explicitement lue sur la page,
  au format AAAA-MM-JJ ou DATE_INCONNUE ;
- l’accès intégral OUI/NON ;
- la rubrique exacte ;
- le fait essentiel.
Ne décide pas encore si la date est dans la fenêtre.
Termine par COLLECTE_TERMINEE seulement si les cinq rubriques,
les dix requêtes, les cinq domaines et au moins cinq candidats
sont établis.
Sinon termine par COLLECTE_INSUFFISANTE avec les critères manquants.
Ne pose aucune question.
```

Continuer seulement si la réponse se termine par `COLLECTE_TERMINEE`.

## 2. VALIDATION sans le Web

Désactiver **Rechercher sur le web**, puis envoyer :

```text
PHASE VALIDATION.
N’utilise pas le Web.
Ne rédige ni REVUE ni HTML.
Relis uniquement CANDIDATS.

Fenêtre inclusive :
- DEBUT_ISO = {{DEBUT_ISO}}
- FIN_ISO = {{FIN_ISO}}

Recopie chaque date brute exactement telle qu’elle apparaît.
Ne la corrige pas et ne retire aucun texte.
Pour chaque candidat, exécute séparément :
1. date exactement au format AAAA-MM-JJ : OUI/NON ;
2. DATE_PUBLICATION >= {{DEBUT_ISO}} : OUI/NON ;
3. DATE_PUBLICATION <= {{FIN_ISO}} : OUI/NON ;
4. accès intégral = OUI : OUI/NON.

Une source est valide seulement si les quatre réponses sont OUI.
Rejette aussi DATE_INCONNUE et toute date accompagnée d’un texte.
Crée CLE_EVENEMENT = organisation | action | objet | date ou période.
Deux candidats sur le même fait réel ont la même CLE_EVENEMENT.
Pour chaque clé répétée, conserve la source la plus directe ;
à défaut la plus récente ; à défaut la première candidate.
Exclus les autres avec DOUBLON_DE | titre conservé.

Réponds sous CONTROLE_DATES avec une ligne par candidat :
titre | date brute | format exact | borne basse | borne haute |
accès | CLE_EVENEMENT | décision.
Réponds sous SOURCES_VALIDES avec titre, URL, date,
rubrique exacte et fait essentiel.
Ajoute SOURCES_EXCLUES avec chaque motif.
Vérifie : nombre de SOURCES_VALIDES + nombre de SOURCES_EXCLUES
= nombre de CANDIDATS.
Termine par VALIDATION_TERMINEE.
Ne pose aucune question.
```

Continuer seulement si `VALIDATION_TERMINEE` est présent, si le comptage est exact et si chaque clé répétée ne laisse qu’une source valide.

## 3. DONNEES sans le Web

Envoyer :

```text
PHASE DONNEES.
N’utilise pas le Web.
Utilise exclusivement SOURCES_VALIDES.
Ne charge pas encore les fragments HTML.
Produis DONNEES_RENDU avec :
- les dates d’édition ;
- l’ordre des rubriques produites ;
- pour chaque source : identifiant et libellés de rubrique, titre,
  URL, source, date longue en majuscules, fait, mots-clés,
  À retenir et Intérêt pour le SNUM ;
- ESSENTIEL=OUI pour exactement trois sources dès trois valides.
Respecte : fait de 25 mots maximum ; 3 à 5 mots-clés joints
par ` · ` ; À retenir et Intérêt de 15 mots maximum.
Vérifie que chaque source valide possède tous ses champs.
Termine par DONNEES_RENDU_PRETES si tout est complet ;
sinon DONNEES_RENDU_INCOMPLETES avec les champs manquants.
Ne rédige pas encore le HTML. Ne pose aucune question.
```

Continuer seulement si `DONNEES_RENDU_PRETES` est présent.

## 4. CANON sans le Web

Envoyer immédiatement avant `RENDU` :

```text
PHASE CANON.
N’utilise pas le Web.
Recherche SNUM_CANON_V512_INDEX_START et SNUM_CANON_V512_INDEX_END
dans les ressources du Projet.
Suis READ_NEXT.
Charge intégralement les fragments 06, 07, 08, 09 et 10.
Vérifie la paire d’index et les onze paires de fragments START/END.
Conserve littéralement les blocs html.
Ne rends pas encore la newsletter.
Réponds seulement :
- CANON_HTML_PRET, puis la paire d’index et les onze paires ;
- ou CANON_HTML_INCOMPLET, puis le jeton manquant.
```

Les onze paires attendues sont :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_FOOTER_START / SNUM_FOOTER_END` ;
- `SNUM_ESSENTIALS_OPEN_START / SNUM_ESSENTIALS_OPEN_END` ;
- `SNUM_ESSENTIAL_CARD_START / SNUM_ESSENTIAL_CARD_END` ;
- `SNUM_ESSENTIALS_CLOSE_START / SNUM_ESSENTIALS_CLOSE_END` ;
- `SNUM_RUBRIC_OPEN_START / SNUM_RUBRIC_OPEN_END` ;
- `SNUM_RUBRIC_ARTICLE_START / SNUM_RUBRIC_ARTICLE_END` ;
- `SNUM_RUBRIC_CLOSE_START / SNUM_RUBRIC_CLOSE_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END` ;
- `SNUM_SHELL_CLOSE_START / SNUM_SHELL_CLOSE_END`.

Ne pas envoyer `RENDU` si une paire manque.

## 5. RENDU sans le Web

Sans aucun message intermédiaire, envoyer :

```text
PHASE RENDU.
N’utilise pas le Web.
Utilise exclusivement DONNEES_RENDU et les fragments canoniques
chargés au tour précédent.
Ne recherche plus les ressources ni les jetons.
Les marqueurs @@ des fragments sont des entrées normales,
jamais un échec avant leur remplacement.
Construis d’abord un brouillon HTML complet non affiché.
Copie littéralement 06.
Pour L’essentiel, concatène ESSENTIALS_OPEN,
exactement trois ESSENTIAL_CARD, puis ESSENTIALS_CLOSE.
Pour chaque rubrique, concatène RUBRIC_OPEN,
un RUBRIC_ARTICLE par source de la rubrique, puis RUBRIC_CLOSE.
Insère WATCH seulement si nécessaire.
Ajoute ensuite 07, puis 10.
Remplace seulement les marqueurs @@.
Ne crée aucune balise ni classe absente des fragments.
Pour chaque source valide, crée exactement un article dans sa rubrique.
Une carte essentielle ne remplace jamais cet article.
Avec moins de trois sources, ne crée ni section ni lien L’essentiel.
À partir de trois sources, crée exactement trois cartes essentielles.
Pour chaque lien href="#id", crée exactement une section id="id".
Livre dans cet ordre :
1. ## REVUE
2. ## HTML COMPLET, avec un unique bloc html complet
3. ## DOSSIER PRIVÉ
Remplace tous les marqueurs @@ avec DONNEES_RENDU.
Corrige le brouillon, puis contrôle seulement ce brouillon final.
Ne contrôle jamais les fragments bruts.
Avant affichage, vérifie le title, la feuille styles.css?v=20260917,
l’absence de marqueur @@, chaque source dans sa rubrique,
la navigation, fr-theme-modal et les scripts DSFR 1.15.2.
Si un point échoue :
- réponds A_COMPLETER ;
- ajoute ## CONTROLES_EN_ECHEC ;
- ajoute une ligne CODE | détail par écart ;
- n’affiche aucun HTML.
Ne pose aucune question.
```

## Décider si le résultat est utilisable

Si la réponse commence par `A_COMPLETER`, arrêter. Lire chaque ligne de `CONTROLES_EN_ECHEC` et conserver la conversation comme preuve. Ne pas demander de contourner le garde-fou.

Sinon, vérifier :

- les trois titres Markdown dans l’ordre ;
- un seul bloc de `<!doctype html>` à `</html>` ;
- aucun marqueur `@@` ;
- chaque source valide exactement une fois dans sa rubrique ;
- exactement trois cartes essentielles dès trois sources ;
- un seul `h1`, trois accès rapides et `fr-theme-modal` ;
- les scripts DSFR 1.15.2 module et nomodule ;
- chaque lien interne avec une cible unique ;
- `État : PRODUITE - contrôle métier requis` dans le dossier privé.

Une recette réussie prouve seulement le scénario exécuté. Elle ne remplace pas un audit RGAA complet.

## État de la recette

La recette réelle du 15 octobre 2026 a atteint `État : PRODUITE - contrôle métier requis` après un message manuel `continue` et un second envoi de `RENDU`. L'assemblage HTML est donc démontré après reprise, pas au premier passage.

La sortie n'est pas livrable : `DONNEES` a associé de mauvais jours de semaine à des dates ISO correctes. Si une date longue contient un jour de semaine, vérifier sa correspondance avec la date ISO avant de poursuivre. Toute erreur impose l'arrêt et le signalement ; ne corrigez pas silencieusement le HTML final.

Le verdict V5.12 est `NO-GO` pour une production autonome. Voir le [rapport de contrôle](./RAPPORT-V5.12.md) et le [compte rendu de recette](./_documentation/installation-v5.12-2026-10-15/RESULTAT-INSTALLATION-ET-RECETTE.md).
