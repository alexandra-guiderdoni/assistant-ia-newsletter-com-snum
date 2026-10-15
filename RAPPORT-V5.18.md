# Rapport de recette V5.18

## Verdict

La chaîne à deux Projets est validée sur un scénario réel exécuté le 15 octobre 2026.
Le Projet Collecte a produit un paquet V5.18 exploitable. Le Projet Rendu HTML a livré
le HTML canonique au premier message, sans correction intermédiaire.

## Scénario exécuté

- édition : 14 octobre 2026 ;
- fenêtre inclusive : du 3 au 13 octobre 2026 ;
- Projet Collecte : `COLLECTE`, puis `VALIDATION`, puis `PAQUET` dans la même
  conversation ;
- Projet Rendu HTML : `RENDRE_EDITION` dans une conversation neuve ;
- Web activé uniquement pendant `COLLECTE`.

## Résultats observés

- collecte : 10 requêtes, 5 rubriques, au moins 5 domaines et 10 candidats ;
- validation : 3 sources valides et 7 sources exclues, soit 10 candidats contrôlés ;
- contrôle des bornes : les comparaisons basse et haute sont libellées séparément et
  utilisent les valeurs réelles ;
- paquet : schéma `SNUM_PAQUET_RENDU_V518`, 3 articles et 3 essentiels ;
- dates d’articles : une valeur ISO de contrôle et une valeur longue avec le mois en
  lettres pour chaque article ;
- rendu : `HTML_CANONIQUE_PRODUIT - contrôle métier requis` dès le premier message.

## Vérification du HTML

Le paquet réel a aussi été rendu par l’outil déterministe local. Le validateur retourne
`HTML_CANONIQUE_OK`.

Une comparaison indépendante a transformé le HTML de l’Assistant et le HTML local en
une suite normalisée de balises, attributs et textes. Les deux suites contiennent 542
jetons et partagent l’empreinte `fc262d9d0172f9fd`. Cette preuve couvre la structure,
les attributs et le contenu textuel ; elle ignore seulement les différences de mise en
forme entre les balises.

Le dernier écart détecté concernait le `<title>` : l’outil local affichait auparavant
la date ISO. La V5.18 affiche désormais `14 octobre 2026`, comme l’Assistant et le
gabarit attendu. Un test empêche le retour de la date ISO dans le titre.

## Limites de la recette

- le scénario couvre une édition de trois articles ;
- aucune publication GitHub Pages ni diffusion par courriel n’a été exécutée ;
- le contrôle automatisé ne remplace pas une validation métier du choix des sources ;
- l’empreinte normalisée ne prouve pas l’identité octet par octet, car les retours à la
  ligne et l’indentation peuvent différer sans modifier le DOM rendu.

## Conclusion

La V5.18 corrige les deux défauts ciblés : les dates publiées sont en toutes lettres et
les traces de validation distinguent correctement la borne basse de la borne haute.
Elle produit en plus un HTML structurellement identique au canon local à partir du même
paquet.

La distribution finale utilise deux archives à la racine, chacune avec un dossier du
même nom que le Projet Assistant : `Newsletter SNUM - Collecte.zip` et
`Newsletter SNUM - Rendu HTML.zip`.
