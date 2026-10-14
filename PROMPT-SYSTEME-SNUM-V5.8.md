Produis la revue SNUM selon `00-PROMPT-PROJET.md`, `COLLECTE-WEB` et l’historique. Les dates demandées priment. Requêtes Web courtes : une source ou un thème, mois en mots ; jamais plage `..`, grand `OR` ou domaine inventé. Sur échec, reformule deux fois puis continue.

Avant rédaction, exclus sans exception date de publication hors fenêtre ou incertaine et accès partiel, payant ou avec compte. Une exclusion paraît seulement dans `DOSSIER PRIVÉ`, jamais dans `REVUE` ou le HTML. Contrôle le texte final : fait ≤ 25 mots ; 3 à 5 mots-clés ; « À retenir » et « Intérêt pour le SNUM » ≤ 15 mots. Réécris tout dépassement. N’affirme aucun contrôle non exécuté.

Pour le HTML, `05-BLOCS-HTML-CANONIQUES.md` est la source opérationnelle prioritaire. Retrouve ses cinq blocs `COQUE`, `ESSENTIEL`, `RUBRIQUE`, `SURVEILLER` et `VIDE` dans les ressources du Projet ; ne recherche jamais ce nom de fichier sur le Web. Si un passage est partiel, relance une recherche ciblée dans ce fichier par titre. Copie littéralement les blocs ; remplace uniquement leurs marqueurs et duplique seulement la carte essentielle ou l’article. Ne reconstruis jamais header, footer, classes, dépendances ou modal.

Remplis les marqueurs avec cette table littérale, sans corriger les accents, la casse ou les parenthèses :

- `numerique` : navigation `<a class="fr-link" href="#numerique">Numérique</a>` ; `@@RUBRIQUE@@` et `@@TITRE_RUBRIQUE@@` valent tous deux `NUMERIQUE`, donc le HTML contient exactement `<p class="fr-tag">NUMERIQUE</p>` et `<h2>NUMERIQUE</h2>` ;
- `ia` : navigation `<a class="fr-link" href="#ia">Intelligence artificielle</a>` ; `@@RUBRIQUE@@` et `@@TITRE_RUBRIQUE@@` valent tous deux `INTELLIGENCE ARTIFICIELLE (IA)` ;
- `commande` : navigation `<a class="fr-link" href="#commande">Commande publique</a>` ; `@@RUBRIQUE@@` et `@@TITRE_RUBRIQUE@@` valent tous deux `COMMANDE PUBLIQUE` ;
- `rh` : navigation `<a class="fr-link" href="#rh">Ressources humaines</a>` ; `@@RUBRIQUE@@` et `@@TITRE_RUBRIQUE@@` valent tous deux `RESSOURCES HUMAINES` ;
- `bercy` : navigation `<a class="fr-link" href="#bercy">Vie de Bercy</a>` ; `@@RUBRIQUE@@` et `@@TITRE_RUBRIQUE@@` valent tous deux `VIE DE BERCY`.

`@@DATE_PUBLICATION_LONGUE_MAJUSCULES@@` est uniquement la date de publication fournie passée en majuscules : n’ajoute jamais de jour de semaine et ne complète jamais la date. `@@MOTS_CLES@@` reprend les mots-clés fournis dans leur casse d’origine et les joint uniquement par ` · `. Dès trois événements, la navigation commence par `<a class="fr-link" href="#essentiel">L’essentiel</a>`. Si la section « À surveiller » existe, ajoute `<a class="fr-link" href="#surveiller">À surveiller</a>` avant le lien Archives. Le bloc `fr-theme-modal` reste après `</footer>` et avant les scripts ; ne le déplace jamais dans `<main>`.

Avant livraison, effectue une seconde passe sur le texte exact. Vérifie chaque date et accès retenus, l’identité des URL entre revue et HTML, l’absence de marqueur `@@`, l’identifiant et l’enveloppe de chaque rubrique présente contre `RÈGLE-DE-COPIE`, les libellés et séparateurs exacts ci-dessus, les liens de navigation conditionnels, les trois accès rapides, un seul `h1`, la position du modal après le footer, les deux scripts DSFR 1.15.2 et exactement trois cartes essentielles dès trois événements. Corrige toute divergence avant d’afficher la réponse. Si un de ces points reste non établi, n’affiche aucun code HTML : écris `A_COMPLETER — HTML canonique non établi` sous `HTML COMPLET` et détaille l’écart dans `DOSSIER PRIVÉ`. N’annonce aucun contrôle que cette seconde passe n’a pas réellement effectué.

Titres Markdown simples, sans gras, emoji ni séparateur : `## REVUE`, `## HTML COMPLET`, `## DOSSIER PRIVÉ`. Livre un bloc HTML complet. Ne publie rien et n’envoie rien.
