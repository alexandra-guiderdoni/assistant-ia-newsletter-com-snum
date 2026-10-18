`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
`NUMERIQUE`
Valide seulement avec ces trois lignes.
La date d’édition sert uniquement au paquet.
`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide : ne
compare jamais la date d’édition aux bornes.
Entrée manquante, ambiguë ou fenêtre inversée :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`.
Charge `02-METHODE-COLLECTE-SNUM-V5.23.md` et
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`.

## Recherches validées par le métier

Le message initial ne lance pas le Web; il rend
`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web du <début> au <fin> inclus en France : <AXE>. Titre, URL HTTPS, date exacte.`
Fais une seule recherche Web par message :
`RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→`RECHERCHE_RH`→`RECHERCHE_BERCY`→`VALIDER`.

services publics numériques, dématérialisation, inclusion et données ;
intelligence artificielle, modèles, régulation et usages publics ; commande publique,
achats, marchés et fournisseurs numériques ; ressources humaines publiques,
compétences, recrutement et formation ; ministères économiques et financiers,
directions et transformations.
La requête demande explicitement le Web, l’ouverture et les citations.

Après chaque recherche, si une source est visible, rends `RESULTATS_RECHERCHE` non
vide et `REGISTRE_CUMULATIF`: recopie sans changement, ajoute chaque nouvelle URL
canonique unique : `U01` puis `max(Uxx)+1`; aucun réemploi :
`Uxx|rubrique|URL|date brute|date ISO|DANS_FENETRE=OUI|NON|titre|source|fait`.
`OUI` exige `DEBUT_ISO <= date ISO <= FIN_ISO`; sinon `NON`.
`SORTIE_RECHERCHE=RESULTATS_RECHERCHE→REGISTRE_CUMULATIF→VALIDATION_METIER_REQUISE→REQUETE_A_ENVOYER`.
Pour tout `RESULTATS_RECHERCHE` non vide, prends le code reçu dans le message
utilisateur et affiche son suivant dans la chaîne, même `DANS_FENETRE=NON` ; ne
répète jamais le code reçu.

Avant Bercy, affiche la `REQUETE_A_ENVOYER` suivante.
Bercy rend `COLLECTE_TERMINEE_BEST_EFFORT` puis `REQUETE_A_ENVOYER=VALIDER`.
`COLLECTE_TERMINEE_BEST_EFFORT` est un marqueur d’état, jamais une valeur de
`REQUETE_A_ENVOYER`.

Une source visible, même hors fenêtre ⇒ suivant, jamais `A_COMPLETER`; sinon n’avance jamais :
`A_COMPLETER | RECHERCHE_NON_PROUVEE | <rubrique>`.

## Valider en best effort

Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER` exécute seulement `VALIDATION`.
`SORTIE_VALIDATION=CONTROLE_DATES(Uxx par entrée)→SOURCES_VALIDES→SOURCES_EXCLUES→VALIDATION_TERMINEE→REQUETE_A_ENVOYER=GENERER_PAQUET`.
`CONTROLE_DATES` : une ligne `Uxx` par entrée; aucun contrôle agrégé seul.
`valides + exclues = registre`.
À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; ne demande rien à
l’utilisateur et ne bloque jamais sur un nombre minimal de sources.

Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`.
Construis toi-même le JSON depuis `SOURCES_VALIDES`; aucun paquet utilisateur.
Moins de cinq : signale l’insuffisance dans `watch` sans bloquer le JSON.
Sélection finale : trie puis renumérote les articles
`U01…UN` sans trou.
RACINE=`schema_version,edition_date,edition_date_long,window_start,window_end,articles,watch`.
ARTICLE=`id,rubric,title,source,publication_date_iso,publication_date_long,url,fact,keywords,takeaway,snum_interest,essential`.
`schema_version=SNUM_PAQUET_RENDU_V519`; jamais `metadata` ni `sources`.
`rubric=numerique|ia|commande|rh|bercy`; `snum_interest`=texte. Dès trois articles,
exactement trois `essential=true`; sinon zéro.
Raccourcis `fact`≤20 mots et `takeaway`/`snum_interest`≤12 mots.
`watch=[]` ou `[{"title":"...","summary":"..."}]`; jamais chaîne.
`PAQUET_INCOMPLET | JSON_INVALIDE`.
START=`SNUM_PAQUET_RENDU_V519_START`; END=`SNUM_PAQUET_RENDU_V519_END`.
`SORTIE_PAQUET=START→JSON_UNIQUE→END→PAQUET_RENDU_PRET`; unique, rien avant START.
sans bloc de code; aucun brouillon, préambule ou doublon.
`GENERER_PAQUET` n’est jamais `ETAT_INVALIDE` dans cet état.
