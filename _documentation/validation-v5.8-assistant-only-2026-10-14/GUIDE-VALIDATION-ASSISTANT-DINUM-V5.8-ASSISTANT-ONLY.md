# Validation du kit Newsletter SNUM V5.8 Assistant-only

## Résultat

Le parcours métier fonctionne entièrement dans l’Assistant DINUM, sans script sur le poste de travail. Le nouveau Projet contient le prompt système et les six fichiers du kit.

Verdict de la recette du 14 octobre 2026 : **NO-GO pour une production ou une publication autonome**. Le premier HTML est invalide et incomplet ; le second est valide au sens général, mais ne respecte toujours pas les blocs canoniques. Le rendu n’est donc pas identique à celui du dépôt Bacoco.

[Ouvrir la conversation du Projet](https://assistant.numerique.gouv.fr/chat/a62ca910-0a58-452a-af0d-cfea5364f066/)

[Ouvrir la première sortie HTML](./assistant-output.html)

[Ouvrir la seconde sortie HTML](./assistant-output-second-pass.html)

Rendus locaux pendant la recette : <http://127.0.0.1:8767/> et <http://127.0.0.1:8767/second-pass/>.

## Ce que le métier doit préparer

- le ZIP `kit-dinum-snum-v5-8-assistant-only-6-fichiers.zip` ;
- le texte de `PROMPT-SYSTEME-SNUM-V5.8.md` ;
- la date d’édition et les deux bornes incluses de la fenêtre de collecte.

Le métier n’exécute aucune commande et aucun script local.

## Pas à pas dans l’Assistant DINUM

### 1. Créer un Projet distinct

Depuis <https://assistant.numerique.gouv.fr/>, choisir **Nouveau projet** et donner un nom explicite, par exemple :

```text
Newsletter SNUM - Validation V5.8 - Blocs canoniques
```

Cette séparation préserve le Projet précédent et évite de mélanger les anciennes instructions.

### 2. Ajouter les instructions

Ouvrir les paramètres du Projet. Copier intégralement `PROMPT-SYSTEME-SNUM-V5.8.md` dans **Instructions (expérimental)**.

Ne pas utiliser `_documentation/prompt-loic.md` comme prompt système : ce fichier archive le prompt du planificateur ChatGPT de Loïc.

### 3. Téléverser les six fichiers

Ajouter exactement :

1. `00-PROMPT-PROJET.md`
2. `01-ETAT-HISTORIQUE.md`
3. `02-METHODE-EDITORIALE.md`
4. `03-GABARIT-HTML.md`
5. `04-RELAIS-HUMAIN.md`
6. `05-BLOCS-HTML-CANONIQUES.md`

Vérifier les six noms dans les paramètres, attendre leur disponibilité, puis enregistrer.

### 4. Ouvrir la conversation depuis le Projet

Créer la conversation depuis le Projet et vérifier que son titre reste affiché sous ce Projet dans le panneau latéral. Une conversation autonome n’accède pas aux fichiers du Projet.

### 5. Activer le Web pour la collecte

Activer **Web**, puis envoyer une demande où les trois dates sont déjà remplacées :

```text
Prépare à partir de zéro la revue SNUM du mercredi 14 octobre 2026, pour les informations publiées du 3 octobre 2026 au 13 octobre 2026 inclus, heure de Paris. Lance la recherche Web et réalise toute la production selon le Projet. Livre la revue, un unique bloc HTML complet strictement fidèle au gabarit de Loïc et le dossier privé. Ne reprends aucun ancien brouillon. Ne publie rien et n’envoie rien.
```

### 6. Contrôler la réponse dans l’Assistant

La réponse doit présenter, dans cet ordre : `REVUE`, `HTML COMPLET`, `DOSSIER PRIVÉ`.

Avant toute utilisation, rechercher visuellement ces signaux d’arrêt :

- un marqueur `@@` dans le code ;
- moins de trois cartes dans « L’essentiel » lorsqu’au moins trois événements sont retenus ;
- un identifiant de rubrique différent de `numerique`, `ia`, `commande`, `rh` ou `bercy` ;
- une rubrique absente de la navigation ou un lien de navigation sans rubrique correspondante ;
- une source publiée hors de la fenêtre ;
- une affirmation de contrôle contredite par la revue ou le HTML.

Si un signal apparaît, ne pas publier. La sortie conforme attendue est alors :

```text
A_COMPLETER — HTML canonique non établi
```

### 7. Faire contrôler avant diffusion

Le statut reste `A_COMPLETER` tant qu’un contrôle extérieur n’a pas vérifié le contenu et le HTML. Le métier ne doit jamais transformer une autoévaluation de l’Assistant en preuve de conformité.

## Résultats observés

### Premier passage

La sortie contient des marqueurs non remplacés, une enveloppe `ia` incorrecte, des numéros de section incohérents et des balises non fermées. Une source du 16 septembre est retenue hors de la fenêtre du 3 au 13 octobre.

Empreinte SHA-256 :

```text
0a9677a45d2c3312a409019a7f771a06653afb67daf011544ca3a5d447834b2f
```

### Second passage

La correction retire les marqueurs et produit un HTML généralement valide. Elle conserve seulement deux cartes essentielles, invente `formation_continue` et `octobre_numerique`, et limite la navigation aux archives.

Empreinte SHA-256 :

```text
295d041beeed4b041ad8c5350110ff74e8dc313946e984e73af132fd1881adfd
```

## Comparaison visuelle

La première capture montre le rendu DINUM brut : la structure DSFR est proche, mais la date reste un marqueur et la navigation est incomplète.

![Rendu de la sortie DINUM brute](./captures/01-sortie-dinum-brute.png)

La référence Bacoco présente une date résolue, les rubriques canoniques et leur navigation complète.

![Rendu de référence Bacoco](./captures/02-reference-bacoco.png)

Le second passage résout la date, mais conserve seulement deux cartes essentielles, des rubriques inventées et une navigation vide hors archives.

![Rendu de la seconde sortie DINUM](./captures/03-sortie-dinum-second-passage.png)

## Contrôles techniques réservés à l’équipe de validation

Ces contrôles ne font pas partie du parcours métier. Le validateur canonique retourne, au premier passage :

```text
SECTION_NUMBERS
RUBRIC_WRAPPER_IA
UNRESOLVED_MARKER
```

Au second passage :

```text
ESSENTIALS_CARD_COUNT
UNKNOWN_RUBRIC_ID
```

Nu HTML Checker signale des erreurs de fermeture au premier passage. Le second passage n’a aucune erreur générale, mais trois avertissements de rôles ARIA redondants. Un HTML généralement valide peut donc rester non canonique.

## Évolution après la recette

Le kit local impose maintenant un arrêt fermé et interdit de rechercher `05-BLOCS-HTML-CANONIQUES.md` sur le Web. Cette modification a réussi les contrôles locaux, mais n’a pas été rejouée dans DINUM après les trois échecs observés. La prochaine recette doit repartir d’une conversation neuve dans le Projet.

## Captures et vidéo

Les deux captures de comparaison sont conservées dans `captures/`. Les captures d’interface et la vidéo de 45 secondes de l’essai précédent restent dans `../validation-v5.8-2026-10-14/` à titre historique. Aucune nouvelle vidéo continue n’a été enregistrée pendant cette recette.

## Limites

- aucune publication GitHub Pages ;
- aucun envoi d’e-mail ;
- aucun commit ni push ;
- aucun audit RGAA manuel complet ;
- aucune preuve que les nouvelles règles d’arrêt fermé sont déjà respectées par DINUM.
