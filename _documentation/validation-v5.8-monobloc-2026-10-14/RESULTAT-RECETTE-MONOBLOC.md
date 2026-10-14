# Résultat de la recette V5.8 monobloc

## Verdict

La variante qui place directement les blocs HTML canoniques dans les instructions du Projet est `NO-GO` dans l’Assistant DINUM testé le 14 octobre 2026.

Le champ **Instructions (expérimental)** impose une limite de 4 000 caractères. Le prompt V5.8 monobloc généré en comptait 14 466. L’interface a conservé exactement les 4 000 premiers caractères et a supprimé toute la suite, avant le début de la coque HTML canonique.

Cette limite empêche de tester loyalement trois conversations avec cette variante : le modèle ne reçoit jamais le gabarit annoncé. Le Projet tronqué a donc été fermé sans être créé.

## Objectif de la tentative

La tentative devait vérifier si l’intégration littérale de `05-BLOCS-HTML-CANONIQUES.md` dans le prompt système suffisait à produire, directement dans le chat, un HTML identique au gabarit Bacoco.

Le critère de réussite était le suivant : trois conversations neuves devaient livrer un HTML validé contre les blocs canoniques, sans correction manuelle ni script sur le poste métier.

## Méthode exécutée

1. Génération locale d’un prompt réunissant `PROMPT-SYSTEME-SNUM-V5.8.md` et les cinq blocs de `05-BLOCS-HTML-CANONIQUES.md`.
2. Vérification locale de la présence littérale des blocs `COQUE`, `ESSENTIEL`, `RUBRIQUE`, `SURVEILLER` et `VIDE`.
3. Ouverture d’un Projet neuf dans l’Assistant DINUM.
4. Collage du prompt intégral dans **Instructions (expérimental)**.
5. Lecture du champ après collage depuis le DOM de la page.
6. Fermeture de la modale sans créer le Projet invalide.

## Preuves observées

- taille du prompt monobloc : 14 466 caractères ;
- attribut HTML du champ : `maxlength="4000"` ;
- contenu effectivement conservé : 4 000 caractères ;
- présence de `<!doctype html>` après collage : non ;
- présence de `</html>` après collage : non ;
- fin du texte conservé : `Pour l’assemb` ;
- taille de la seule coque canonique : 5 713 caractères, ou 5 464 après compactage des blancs ;
- taille compacte des cinq blocs canoniques : 8 228 caractères.

Même la coque seule reste donc supérieure de 1 464 caractères à la capacité du champ après compactage. Une optimisation de mise en forme ne peut pas rendre cette stratégie viable sans supprimer des éléments canoniques.

## Ce que la recette prouve

La recette prouve que le prompt système monobloc ne tient pas dans le champ d’instructions de l’Assistant DINUM observé. Elle explique pourquoi le gabarit complet doit rester dans les fichiers du Projet plutôt que dans ce champ.

Elle ne prouve pas que l’Assistant exploitera toujours correctement les fichiers téléversés. Les recettes précédentes montrent au contraire que la récupération du bloc `COQUE` peut échouer malgré la présence de `05-BLOCS-HTML-CANONIQUES.md`.

## Ce qui n’a pas été exécuté

- aucun Projet monobloc n’a été enregistré ;
- aucune conversation monobloc n’a été lancée ;
- aucun HTML issu de cette variante n’a été déclaré conforme ;
- aucune publication GitHub Pages et aucun envoi de courriel n’ont été réalisés.

## Conséquence pour la V5.8

La V5.8 Assistant-only reste la version livrée. Elle utilise le prompt système de moins de 4 000 caractères et six fichiers de connaissance, dont `05-BLOCS-HTML-CANONIQUES.md`.

Son état de validation ne change pas : le canal de livraison dans le chat fonctionne, mais la fidélité autonome au gabarit Bacoco reste `NO-GO`. En cas de bloc canonique introuvable, la seule sortie sûre reste :

```text
A_COMPLETER — HTML canonique non établi
```

## Suite recommandée, non exécutée

Demander à l’équipe de l’Assistant DINUM soit d’augmenter la capacité du champ d’instructions, soit de fournir un mécanisme déterministe pour injecter un gabarit long dans la réponse. Sans l’une de ces capacités, promettre un HTML littéralement identique reste plus fort que ce que l’outil permet de garantir.

## Relecture PDG

`PDG self-check, not independent review` : le rapport réutilise les blocs canoniques existants comme source de vérité, n’ajoute aucun second gabarit et distingue les mesures observées des comportements non vérifiés.
