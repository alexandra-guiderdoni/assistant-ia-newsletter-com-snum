# Format de sortie JSON SNUM - V5.6

## Contrat obligatoire

La réponse contient uniquement un bloc de code `json` avec l’objet ci-dessous. Aucun texte, tableau, HTML ou seconde version avant ou après. Remplacer les valeurs, conserver exactement les clés et produire du JSON valide en UTF-8.

```json
{
  "version": "snum-v5.6",
  "date_edition": "AAAA-MM-JJ",
  "date_debut_collecte": "AAAA-MM-JJ",
  "date_fin_collecte": "AAAA-MM-JJ",
  "etat_assistant": "A_COMPLETER",
  "evenements": [],
  "essentiels": [],
  "a_surveiller": [],
  "collecte": {
    "domaines_consultes": [],
    "requetes": [],
    "exclusions": []
  },
  "limites": []
}
```

Chaque entrée de `evenements` possède exactement ces clés :

```json
{
  "id": "E01",
  "rubrique": "NUMERIQUE",
  "titre": "Titre rédigé",
  "fait": "Une phrase factuelle courte.",
  "mots_cles": ["terme 1", "terme 2", "terme 3"],
  "a_retenir": "Une phrase courte.",
  "interet_snum": "Une phrase courte.",
  "titre_original": "Titre exact de la source",
  "source": "Nom de la source",
  "date_publication": "AAAA-MM-JJ",
  "url": "https://adresse-publique-exacte",
  "lecture": "INTEGRAL_LU",
  "preuve_lecture": "Outil et élément observable établissant la lecture du corps complet."
}
```

`rubrique` vaut uniquement `NUMERIQUE`, `INTELLIGENCE_ARTIFICIELLE_IA`, `COMMANDE_PUBLIQUE`, `RESSOURCES_HUMAINES` ou `VIE_DE_BERCY`. `lecture` vaut uniquement `INTEGRAL_LU` ou `INTEGRAL_FOURNI`.

`essentiels` contient zéro identifiant si moins de trois événements, sinon exactement trois identifiants distincts présents dans `evenements`. Ne pas répéter leur contenu.

Chaque exclusion contient `url` et `raison`. Une URL inconnue peut être une chaîne vide seulement si la raison explique précisément l’absence. `a_surveiller`, `domaines_consultes`, `requetes` et `limites` sont des listes de chaînes.

## Interdictions

- Aucun champ supplémentaire ni clé omise.
- Aucun commentaire JSON, virgule finale, balise HTML ou syntaxe Markdown dans les valeurs.
- Aucun article payant, extrait ou source hors fenêtre dans `evenements`.
- Aucune affirmation `PREPAREE`, `COMPLETE`, publication, envoi ou contrôle extérieur.
- Aucune duplication d’un événement ou d’un essentiel.

Le générateur refuse la sortie si le contrat, les dates, rubriques, identifiants, limites de mots, mots-clés, URL ou preuves de lecture sont invalides. Il échappe lui-même tout contenu avant de produire le HTML.
