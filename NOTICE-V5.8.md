# Utiliser le kit SNUM V5.8

1. Remplacer les anciens fichiers du Projet DINUM par les six Markdown du ZIP, dont `05-BLOCS-HTML-CANONIQUES.md`.
2. Coller `PROMPT-SYSTEME-SNUM-V5.8.md` dans « Instructions (expérimental) ».
3. Ouvrir une nouvelle conversation et activer « Rechercher sur le web ».
4. Remplacer les trois variables `{{DATE_EDITION_LONGUE}}`, `{{DATE_DEBUT}}` et `{{DATE_FIN}}`, puis envoyer cette unique commande. La date d’édition contient le jour de semaine vérifié, par exemple « mardi 13 octobre 2026 ». Ne jamais transmettre les accolades telles quelles :

> Prépare à partir de zéro la revue SNUM du {{DATE_EDITION_LONGUE}}, pour les informations publiées du {{DATE_DEBUT}} au {{DATE_FIN}} inclus, heure de Paris. Lance la recherche Web et réalise toute la production selon le Projet. Livre la revue, un unique bloc HTML complet strictement fidèle au gabarit de Loïc et le dossier privé. Ne reprends aucun ancien brouillon. Ne publie rien et n’envoie rien.

DINUM doit reformuler une recherche qui échoue et poursuivre les autres sources. Si aucun événement n’est finalement admissible, il livre le HTML vide et une limite précise sans inventer.

Le métier n’exécute aucun script. DINUM copie les cinq blocs de `05-BLOCS-HTML-CANONIQUES.md`, applique `RÈGLE-DE-COPIE` et réalise sa seconde passe avant d’afficher la réponse. `03-GABARIT-HTML.md` reste le contexte détaillé et la référence CSS.

Les deux passages du 14 octobre 2026 n’ont pas reproduit fidèlement le gabarit. Tant qu’une nouvelle recette n’a pas démontré le contraire, le kit reste en validation. Si DINUM laisse un marqueur `@@`, invente un identifiant de rubrique, produit moins de trois cartes essentielles à partir de trois événements ou ne retrouve pas intégralement les blocs, la seule sortie acceptable sous `HTML COMPLET` est `A_COMPLETER — HTML canonique non établi`. Ne pas publier ce résultat.

Après preuves réelles de publication et d’envoi, envoyer :

> Voici les preuves réelles de publication et d’envoi de l’édition [date] : [preuves]. Produis `01-ETAT-HISTORIQUE.md` complet actualisé, prêt à remplacer l’ancien fichier. Ne publie rien et n’envoie rien.
