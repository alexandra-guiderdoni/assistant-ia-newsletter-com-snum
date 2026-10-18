# Rapport de recette Newsletter SNUM V5.23

## Verdict

`GO` pour la chaîne réelle
`Collecte → chat Web ordinaire → JSON V519 → Rendu HTML`.

Le parcours métier ne requiert que l’Assistant DINUM. Une relance de la recherche
Web a été nécessaire, puis Collecte a produit un paquet V519 valide sur la commande
explicite `NORMALISER_V519`. Rendu a généré le HTML canonique au premier passage.

## Configuration testée

- date de recette : 18 octobre 2026 ;
- branche : `stabilisation/v5.23` ;
- période : du 3 octobre 2026 au 13 octobre 2026 inclus ;
- date d’édition : 14 octobre 2026 ;
- Projet Collecte :
  `Newsletter SNUM - Collecte - Stabilisation v5.23.5` ;
- Projet Rendu :
  `Newsletter SNUM - Rendu HTML - Stabilisation` ;
- Web activé uniquement dans un chat Assistant ordinaire.

Les instructions et les ressources du Projet Collecte ont été remplacées par les
fichiers du worktree. Leur indexation a été attendue avant la conversation neuve.
Le Projet Rendu utilisait déjà les instructions et les quatre ressources canoniques
du candidat.

## Parcours réel exécuté

1. Envoi de `DATE_EDITION`, `PERIODE` et `RECHERCHE_COMPOSITE` dans Collecte.
2. Copie de la requête générée dans un chat ordinaire avec le Web activé.
3. Première recherche sans résultat exploitable, puis une unique relance à
   l’identique dans un nouveau chat Web.
4. Copie de toute la seconde réponse Web dans le chat Collecte d’origine.
5. Vérification du marqueur d’enregistrement, sans JSON prématuré.
6. Envoi de `NORMALISER_V519` et audit déterministe du paquet obtenu.
7. Envoi du paquet dans une conversation neuve du Projet Rendu.
8. Audit du HTML et des contrôles affichés.

## Preuves observées

### Recherche et enregistrement

La requête composite couvrait les cinq axes métier et imposait le format
`RESULTAT|rubrique|URL_HTTPS|date_iso|titre|source|fait_factuel`.

La première recherche a rendu cinq absences. La relance a rendu six sources valides :

- une source `numerique` ;
- trois sources `commande` ;
- deux sources `bercy` ;
- aucune source datée pour `ia` et `rh`.

La réponse Web entourait les lignes de marqueurs Markdown et contenait une absence
`numerique` contradictoire. Collecte a néanmoins conservé les six lignes valides,
ignoré l’absence contradictoire et répondu exactement :

```text
RESULTATS_COMPOSITES_ENREGISTRES | VALIDES=6 | RUBRIQUES_SANS_RESULTAT=ia,rh
REQUETE_A_ENVOYER=NORMALISER_V519
```

Aucun JSON n’a été produit avant la commande explicite.

### Paquet V519

Après `NORMALISER_V519`, la réponse a commencé par
`SNUM_PAQUET_RENDU_V519_START` et s’est terminée par
`SNUM_PAQUET_RENDU_V519_END`, puis `PAQUET_RENDU_PRET`.

L’audit du JSON copié a confirmé :

- analyse JSON réussie ;
- sept clés racine exactes du contrat V519 ;
- `schema_version=SNUM_PAQUET_RENDU_V519` ;
- six articles sous forme de liste ;
- douze clés article exactes pour chaque article ;
- six URL uniques ;
- six dates comprises dans la fenêtre ;
- trois articles `essential=true` ;
- `watch` sous forme de liste d’objets ;
- alerte explicite pour les rubriques `ia` et `rh`.

### Rendu HTML

Dans une conversation neuve du Projet Rendu, le paquet a produit au premier passage :

- un unique titre sémantique `HTML COMPLET`, sans préambule ;
- un unique bloc de code HTML ;
- un document commençant par `<!doctype html>` avec `lang="fr"` ;
- la date d’édition du 14 octobre 2026 ;
- les six URL du paquet ;
- les sections `numerique`, `commande`, `bercy` et `surveiller` ;
- aucun `A_COMPLETER` ni `CONTROLES_EN_ECHEC` ;
- `État : HTML_CANONIQUE_PRODUIT - contrôle métier requis`.

## Limites constatées

- La recherche Web reste non déterministe : le premier chat n’a rien trouvé alors
  que la relance à l’identique a fourni six sources.
- Deux rubriques n’ont aucun résultat daté dans cette fenêtre. Le mode best effort
  les signale dans `watch` et poursuit la chaîne, conformément au contrat.
- La conformité structurelle ne remplace pas la validation éditoriale métier des
  titres, faits et sources retenus.

## Contrôles locaux

- 37 tests `unittest` réussis ;
- Ruff réussi ;
- `python3 scripts/build_split_kit.py --check` retourne `KIT_DECOUPLE_OK` ;
- `git diff --check` réussi ;
- prompt Collecte : 3 969 caractères ;
- prompt Rendu : 3 986 caractères ;
- six ressources téléversables sous 4 500 caractères ;
- ZIP Collecte : trois fichiers attendus ;
- ZIP Rendu : cinq fichiers attendus.

Les contrôles statiques et la recette réelle sont tous deux verts. La recherche Web
reste la couche non déterministe du parcours et conserve sa règle d’une seule relance.

## Décision

La séparation en deux temps est retenue : le collage enregistre les lignes valides,
puis `NORMALISER_V519` produit le paquet. Elle évite de parser, filtrer, enrichir et
sérialiser dans la même réponse.

La recette réelle lève le `NO-GO` précédent. La version peut être commitée, poussée
sur la branche de stabilisation et taguée après réussite des contrôles locaux finaux.
