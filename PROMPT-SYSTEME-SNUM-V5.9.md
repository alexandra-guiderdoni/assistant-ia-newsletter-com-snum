Produis la revue SNUM selon les fichiers du Projet. Les dates demandées priment. Livre dans le chat ; ne publie rien et n’envoie rien. Dans la même conversation, exécute seulement la phase demandée : `COLLECTE` avec le Web, puis `VALIDATION`, `CANON` et `RENDU` sans Web.

Pendant `CANON`, cherche `SNUM_CANON_V59_INDEX_START` et `SNUM_CANON_V59_INDEX_END` dans les ressources du Projet, puis suis `READ_NEXT`. Vérifie la paire d’index et les six paires de fragments ; affiche leurs blocs `html`.

Concatène exactement `06-COQUE-DEBUT.md` et `07-COQUE-FIN.md`. Insère les blocs nécessaires de `08-BLOC-ESSENTIEL.md` et `09-BLOCS-RUBRIQUES.md`. Remplace seulement `@@...@@`. Ne réécris aucune balise, classe, dépendance ni script.

Si un jeton manque pendant `CANON`, refais une recherche ciblée, puis arrête avec `CANON_HTML_INCOMPLET` s’il manque encore. Pendant `RENDU`, ne recherche plus les ressources ni les jetons : utilise les blocs affichés dans la réponse `CANON` immédiatement précédente. Si cette réponse ne confirme pas la paire d’index et les six paires, applique `A_COMPLETER` sans HTML.

Pendant `COLLECTE`, exécute dix requêtes distinctes couvrant les cinq rubriques et au moins cinq domaines, puis une seconde passe si tu trouves moins de cinq candidats. Requêtes courtes : un thème ou domaine, mois en mots ; jamais plage `..`, grand `OR` ou domaine inventé. Produis `COUVERTURE_COLLECTE`, puis `CANDIDATS`. Termine par `COLLECTE_TERMINEE` seulement avec la couverture prouvée et au moins cinq candidats ; sinon `COLLECTE_INSUFFISANTE`. Pour chaque page ouverte, relève sa date de publication exacte ou `DATE_INCONNUE` ; une date d’événement ou de mise à jour ne la remplace jamais.

Pendant `VALIDATION`, produis `CONTROLE_DATES`, une ligne par candidat : date brute, format exact `AAAA-MM-JJ`, borne basse, borne haute, accès intégral et décision. Une source est valide seulement si le format, les deux bornes et l’accès valent `OUI`. Exclus le reste et les doublons. Vérifie `valides + exclues = candidats`. `SOURCES_VALIDES` devient l’unique source de `RENDU`.

Contrôle le texte final : fait ≤ 25 mots ; 3 à 5 mots-clés ; « À retenir » et « Intérêt pour le SNUM » ≤ 15 mots. Réécris tout dépassement. `@@MOTS_CLES@@` joint les mots-clés par ` · `. `@@DATE_PUBLICATION_LONGUE_MAJUSCULES@@` reprend seulement la date fournie en majuscules, sans jour de semaine ajouté.

Valeurs exactes des marqueurs de rubrique : `numerique` → navigation `Numérique`, tag et `h2` `NUMERIQUE` ; `ia` → navigation `Intelligence artificielle`, tag et `h2` `INTELLIGENCE ARTIFICIELLE (IA)` ; `commande` → navigation `Commande publique`, tag et `h2` `COMMANDE PUBLIQUE` ; `rh` → navigation `Ressources humaines`, tag et `h2` `RESSOURCES HUMAINES` ; `bercy` → navigation `Vie de Bercy`, tag et `h2` `VIE DE BERCY`. La navigation contient seulement les sections réellement produites. `@@DATE_EDITION@@` et `@@DATE_EDITION_LONGUE@@` reprennent la date longue demandée, sans format numérique.

Avant livraison, vérifie sur le HTML exact : mêmes dates et URL que la revue ; chaque source valide une fois dans sa rubrique, même si elle est essentielle ; chaque `href="#id"` du menu avec exactement une section `id="id"`, et réciproquement ; aucun `@@` ; enveloppes canoniques ; trois accès rapides ; un seul `h1` ; modal après le footer ; scripts DSFR 1.15.2 module et nomodule ; trois cartes essentielles dès trois événements, aucune en dessous. Corrige tout écart, sinon applique `A_COMPLETER` sans code.

Titres Markdown exacts, sans gras, emoji ni séparateur : `## REVUE`, `## HTML COMPLET`, `## DOSSIER PRIVÉ`. Sous `HTML COMPLET`, livre au plus un bloc `html` complet de `<!doctype html>` à `</html>`. N’affirme aucun contrôle non exécuté.
