`SNUM_COLLECTE_V520_METHODE_START`

# Contrat Collecte et Validation repris de la V5.19

Pendant `COLLECTE`, utilise la date d’édition et la fenêtre données par l’utilisateur.
Exécute une première passe de dix requêtes distinctes couvrant les cinq rubriques
`NUMERIQUE`, `INTELLIGENCE ARTIFICIELLE (IA)`, `COMMANDE PUBLIQUE`, `RESSOURCES
HUMAINES` et `VIE DE BERCY`, sur au moins cinq domaines. Chaque requête cible explicitement la fenêtre :
mentionne ses deux bornes ou son mois et son année, une rubrique et un domaine pertinent.
Ouvre chaque URL.
Ne filtre aucun candidat selon sa date pendant `COLLECTE` : garde toute page lue dans
`CANDIDATS`, même hors fenêtre.
Conserve uniquement une URL canonique absolue commençant par `https://`, la date
explicitement lue, l’accès intégral et le fait essentiel. Après la première passe,
compte les candidats dont la date précise est convertible en ISO et comprise entre
`DEBUT_ISO` et `FIN_ISO`. Ce compte provisoire contrôle seulement la couverture ; la
décision formelle reste réservée à `VALIDATION`.

Si tu n’as pas au moins cinq candidats datés provisoirement dans la fenêtre, effectue
une seconde passe ciblée sur les rubriques, domaines et dates insuffisamment couverts.
Ajoute à `CANDIDATS` toutes les nouvelles pages lues, y compris hors fenêtre.
Après deux passes insuffisantes, termine par `COLLECTE_INSUFFISANTE`.

Produis `COUVERTURE_COLLECTE`, puis `CANDIDATS`. Termine par `COLLECTE_TERMINEE`
seulement avec dix requêtes de première passe, cinq rubriques, cinq domaines, au moins
cinq candidats au total et au moins cinq candidats datés provisoirement dans la
fenêtre ; sinon `COLLECTE_INSUFFISANTE`.

Pendant `VALIDATION`, n’utilise pas le Web. Pour chaque candidat, produis
`CONTROLE_DATES` : titre, date brute, format `AAAA-MM-JJ`, borne basse, borne haute,
accès, `CLE_EVENEMENT`, décision. Trace séparément `date ISO >= DEBUT_ISO` pour la
borne basse et `date ISO <= FIN_ISO` pour la borne haute, avec les valeurs réellement
comparées et `OUI` ou `NON`. N’intervertis jamais les deux bornes. Déduplique d’abord
par URL canonique : même URL = doublon, même si `CLE_EVENEMENT` diffère. Une source est
valide seulement si le format, les deux bornes et l’accès valent `OUI`. Même fait réel = même
clé. Garde la source la plus directe, sinon la plus récente, sinon la première. Exclus
chaque doublon avec
`DOUBLON_DE | titre conservé`. Compte le nombre exact d’entrées sous `CANDIDATS` et
contrôle-les toutes, sans utiliser de sous-liste préfiltrée. Vérifie
`valides + exclues = candidats`. Termine par
`VALIDATION_TERMINEE` seulement si l’égalité est exacte et au moins une source reste
valide.

## Sorties persistantes entre les tours

La réponse `COLLECTE` affiche intégralement `COUVERTURE_COLLECTE` et `CANDIDATS` pour
que le tour `VALIDATION` puisse les relire. La réponse `VALIDATION` affiche
intégralement `CONTROLE_DATES`, `SOURCES_VALIDES` et `SOURCES_EXCLUES` pour que le tour
`PAQUET` puisse les relire. Ne remplace jamais ces structures par un résumé.

`SNUM_COLLECTE_V520_METHODE_END`
