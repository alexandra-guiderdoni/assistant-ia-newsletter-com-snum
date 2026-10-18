# Fiche mémo — Newsletter SNUM

## Lundi 19 octobre 2026

### 1. Lancer la collecte

Ouvrir une nouvelle conversation dans `Newsletter SNUM - Collecte - v5.23.6`,
puis saisir exactement :

```text
DATE_EDITION = 19 octobre 2026
PERIODE = du 12 octobre 2026 au 18 octobre 2026 inclus
```

Attendre l’apparition de `PAQUET_RENDU_PRET`.

### 2. Copier le JSON

Copier la réponse complète comprise entre :

```text
SNUM_PAQUET_RENDU_V519_START
```

et :

```text
SNUM_PAQUET_RENDU_V519_END
```

Attention : ne pas renvoyer `PAQUET_RENDU_PRET` dans le chat Collecte.

### 3. Produire le HTML

Ouvrir une nouvelle conversation dans
`Newsletter SNUM - Rendu HTML - v5.23.6`.

Coller le paquet JSON complet, puis l’envoyer.

### 4. Récupérer le résultat

Attendre :

```text
HTML COMPLET
```

Cliquer sur **Copier le code** pour récupérer le HTML final.

Aucune recherche manuelle, aucun `CONTINUER` et aucune commande intermédiaire.
