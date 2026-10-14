# Rapport de contrôle du kit SNUM V5.8

## Verdict

Le gabarit compact local est fidèle au dépôt `bacoco/revue-presse-snum`, mais l’Assistant DINUM ne le reproduit pas encore de manière fiable. Verdict : **NO-GO pour une production ou une publication autonome**.

Le kit V5.8 reste utilisable en recette avec arrêt fermé : si l’Assistant ne peut pas établir la conformité canonique, il doit répondre `A_COMPLETER — HTML canonique non établi` et ne livrer aucun code HTML.

## Périmètre contrôlé

- nouveau Projet DINUM distinct : `Newsletter SNUM - Validation V5.8 - Blocs canoniques` ;
- prompt système V5.8 et six fichiers Markdown téléversés ;
- génération du 14 octobre 2026 sur la fenêtre du 3 au 13 octobre 2026 inclus ;
- correction dans la conversation du Projet, sans Web ;
- extraction des deux sorties HTML, rendu local, comparaison visuelle avec GitHub Pages et contrôles déterministes ;
- aucune publication de newsletter et aucun envoi d’e-mail pendant la recette.

## Résultats dans l’Assistant DINUM

### Premier passage

Le HTML contient quatre marqueurs `@@...@@`, des numéros de section incohérents et une enveloppe `ia` non canonique. Une source datée du 16 septembre 2026 est retenue hors de la fenêtre demandée, alors que le dossier privé affirme le contraire.

Le validateur retourne :

```text
SECTION_NUMBERS: les numéros de section ne sont pas continus
RUBRIC_WRAPPER_IA: l’enveloppe de la rubrique ia n’est pas canonique
UNRESOLVED_MARKER: un marqueur @@...@@ subsiste
```

Nu HTML Checker signale aussi des balises `div` non fermées.

### Second passage

La correction élimine les marqueurs et produit un HTML généralement valide, mais seulement deux cartes dans « L’essentiel », deux identifiants de rubrique inventés et une navigation réduite aux archives.

Le validateur retourne :

```text
ESSENTIALS_CARD_COUNT: L’essentiel doit contenir exactement trois cartes
UNKNOWN_RUBRIC_ID: identifiants de rubrique non canoniques : formation_continue, octobre_numerique
```

Nu HTML Checker ne remonte aucune erreur, seulement trois avertissements de rôles ARIA redondants. La validité générale ne démontre donc pas la fidélité au gabarit.

## Contrôles locaux

- six tests unitaires réussis ;
- le gabarit compact `05-BLOCS-HTML-CANONIQUES.md` génère localement le même HTML que `03-GABARIT-HTML.md` ;
- le validateur rejette désormais les identifiants de rubrique non canoniques ;
- le prompt système mesure 2 060 caractères, saut final inclus ;
- `ruff` n’était pas disponible dans le `PATH` ; les tests Python et la compilation restent exécutés séparément ;
- aucun audit RGAA complet n’a été réalisé.

## Évolution appliquée après la recette

Les instructions exigent maintenant une recherche des blocs dans les ressources du Projet, jamais sur le Web, une seconde passe explicite et un arrêt fermé dès qu’un marqueur, une enveloppe, un identifiant ou un compte de cartes reste incorrect.

Cette évolution est contrôlée localement mais **n’a pas été rejouée dans l’Assistant DINUM** : trois tentatives de génération ou de correction avaient déjà échoué. Une nouvelle recette devra repartir d’une conversation neuve dans le Projet.

## Preuves

- guide : `_documentation/validation-v5.8-assistant-only-2026-10-14/GUIDE-VALIDATION-ASSISTANT-DINUM-V5.8-ASSISTANT-ONLY.md` ;
- première sortie : `_documentation/validation-v5.8-assistant-only-2026-10-14/assistant-output.html` ;
- seconde sortie : `_documentation/validation-v5.8-assistant-only-2026-10-14/assistant-output-second-pass.html` ;
- captures : `_documentation/validation-v5.8-assistant-only-2026-10-14/captures/`.
