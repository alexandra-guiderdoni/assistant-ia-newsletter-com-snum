# Rapport de recette V5.24 — Collecte et Rendu HTML

## Verdict

`GO` pour `Newsletter SNUM - Collecte` en mode best effort minimal. Après les cinq
recherches, `VALIDER` puis `GENERER_PAQUET` ont produit automatiquement un JSON V519
copiable à partir d’une seule source valide, sans demander au métier de fabriquer ou
de corriger le JSON.

`NO-GO` pour la chaîne complète avec ce paquet minimal dans l’Assistant. Dans une
conversation neuve de `Newsletter SNUM - Rendu HTML`, le paquet à un article et zéro
`essential=true` a été refusé à tort par `PAQUET_INVALIDE`, alors que le contrat de
rendu autorise explicitement zéro essentiel. Une tentative finale a rendu la règle
procédurale et prioritaire ; le même refus a persisté. Continuer à reformuler le prompt
ne constitue donc plus une correction prouvée.

La chaîne complète avait auparavant produit `HTML COMPLET` avec un paquet de cinq
articles. La régression restante est limitée au paquet minimal sans essentiel, mais
elle bloque un parcours métier garanti de bout en bout puisque le métier ne dispose
que de l’Assistant.

## Configuration testée

- édition : 14 octobre 2026 ;
- fenêtre inclusive : du 3 au 13 octobre 2026 ;
- Collecte : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` et ses deux ressources ;
- Rendu : `20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md` et ses quatre ressources ;
- preuve Collecte :
  `https://assistant.numerique.gouv.fr/chat/eee88268-0c06-4709-b59d-a2c3424c2931/` ;
- preuve du refus Rendu minimal :
  `https://assistant.numerique.gouv.fr/chat/0856a641-568f-43f2-863b-2078529e3330` ;
- preuve antérieure du Rendu à cinq articles :
  `https://assistant.numerique.gouv.fr/chat/b24a2832-15ea-4746-8189-931d5fead672/`.

## Résultat Collecte observé

La collecte a conservé une source Bercy datée du 3 octobre 2026, exclu une source
hors fenêtre et poursuivi les rubriques sans source prouvée. Après `VALIDER`, la
commande `GENERER_PAQUET` a émis un bloc unique contenant :

- les marqueurs `SNUM_PAQUET_RENDU_V519_START` et
  `SNUM_PAQUET_RENDU_V519_END` ;
- `schema_version=SNUM_PAQUET_RENDU_V519` ;
- les sept clés racine prévues, sans métadonnée parasite ;
- un seul article, avec `rubric=bercy`, une date dans la fenêtre et une URL unique ;
- `essential=false`, conformément au mode best effort pour une à deux sources ;
- la fin `PAQUET_RENDU_PRET`.

Le JSON est donc sorti automatiquement de la phase Collecte. Le métier n’a eu à
produire aucun champ manuellement.

## Résultat Rendu observé

Le bloc Collecte a été collé sans modification dans une conversation Rendu neuve,
Web désactivé. L’Assistant a terminé par :

```text
A_COMPLETER
CONTROLES_EN_ECHEC
PAQUET_INVALIDE | Le JSON ne contient aucun article avec essential=true.
```

Ce contrôle n’existe pas dans le contrat local. Le prompt Rendu contient désormais
la branche explicite : zéro `essential=true` remplace `@@ESSENTIELS@@` par vide et
continue le rendu. Le comportement réel n’a toutefois pas suivi cette instruction.

## Contrôles locaux

- 80 tests `unittest` exécutés avec succès ;
- Ruff exécuté avec succès ;
- `python3 scripts/build_split_kit.py --check` retourne `KIT_DECOUPLE_OK` ;
- `git diff --check` exécuté avec succès ;
- prompt Collecte : 4 000 caractères ;
- prompt Rendu : 3 998 caractères ;
- `README.md` et `NOTICE-V5.24.md` identiques ;
- les deux ZIP ont été régénérés depuis les sources actives.

Ces contrôles prouvent la cohérence du kit local. Ils ne prouvent pas à eux seuls le
respect des instructions par le modèle de l’Assistant ; la recette réelle ci-dessus
reste la preuve de cette limite.

## Consigne pour la présentation

La Collecte et la génération automatique du JSON sont présentables. Pour une
démonstration de la chaîne complète lundi, utiliser une période qui fournit au moins
trois sources valides et vérifier que le paquet contient exactement trois
`essential=true` avant de le transmettre au Rendu. Ne pas présenter le cas minimal à
zéro essentiel comme validé tant qu’une nouvelle recette réelle n’aboutit pas à
`HTML COMPLET`.
