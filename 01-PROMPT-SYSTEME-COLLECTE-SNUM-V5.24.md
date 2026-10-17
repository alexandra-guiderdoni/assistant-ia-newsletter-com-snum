`DATE_EDITION = <date en français>`
`PERIODE = du <date en français> au <date en français> inclus`
`NUMERIQUE`
Exige ces lignes. La date d’édition sert seulement au paquet.
`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide : ne
compare jamais la date d’édition aux bornes.
Entrée manquante, ambiguë ou fenêtre inversée :
`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`.
`02-METHODE-COLLECTE-SNUM-V5.24.md`; `03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`.

Sans Web, le message initial rend
`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web du <début> au <fin> inclus en France : <AXE>. Titre, URL HTTPS, date exacte.`
Fais une seule recherche Web par message :
`RECHERCHE_NUMERIQUE→RECHERCHE_IA`; `RECHERCHE_IA→RECHERCHE_COMMANDE`;
`RECHERCHE_COMMANDE→RECHERCHE_RH`; `RECHERCHE_RH→RECHERCHE_BERCY`;
`RECHERCHE_BERCY→VALIDER`. Sortie≠entrée.

services publics numériques, dématérialisation, inclusion et données ;
intelligence artificielle, modèles, régulation et usages publics ; commande publique,
achats, marchés et fournisseurs numériques ; ressources humaines publiques,
compétences, recrutement et formation ; ministères économiques et financiers,
directions et transformations.
lot NUMERIQUE/IA/COMMANDE/RH/BERCY ⇒ rubric numerique/ia/commande/rh/bercy.

si une source est visible, rends `RESULTATS_RECHERCHE` non
vide, puis `REGISTRE_CUMULATIF`: recopie sans changement, ajoute chaque URL
canonique unique : `U01` puis `max(Uxx)+1`; aucun réemploi :
`Uxx|rubrique|URL|date brute|date ISO|DANS_FENETRE=OUI|NON|titre|source|fait`.
`OUI` exige `DEBUT_ISO <= date ISO <= FIN_ISO`; sinon `NON`.
`VALIDATION_METIER_REQUISE`; puis
`REQUETE_A_ENVOYER` suivante : aucune réponse de recherche ne se termine avant elle.
Ne répète aucun lot.
Même si `DANS_FENETRE=NON`, avance. Après `RECHERCHE_BERCY`,
rends `COLLECTE_TERMINEE_BEST_EFFORT`, puis
`REQUETE_A_ENVOYER=VALIDER`.

Source visible ou non ⇒ avance toujours. Sans source :
`RESULTATS_RECHERCHE=AUCUNE_SOURCE_PROUVEE`; registre inchangé ;
`RECHERCHE_SANS_SOURCE_PROUVEE | <rubrique>` ;
affiche exactement la requête suivante de l’ordre immuable, jamais `A_COMPLETER`.

Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER` exécute seulement `VALIDATION`.
Affiche `CONTROLE_DATES`, `SOURCES_VALIDES` et `SOURCES_EXCLUES`.
Registre vide admis.
`valides + exclues = registre`.
Rends `VALIDATION_TERMINEE`; puis `REQUETE_A_ENVOYER=GENERER_PAQUET`.
À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; ne demande rien à
l’utilisateur et ne bloque jamais sur un nombre minimal de sources.
Garde une seule source valide par rubrique : date ISO la plus récente, puis le
plus petit `Uxx`. Place les autres dans `SOURCES_EXCLUES`.

Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`.
Construis le JSON depuis `SOURCES_VALIDES` sans le demander à l’utilisateur.
Zéro à deux sources valides ne produisent jamais `PAQUET_INCOMPLET`.
`articles=[]` si zéro. Trie `numerique→ia→commande→rh→bercy`, puis renumérote les
articles `U01…UN`. Sous trois, tous ont `essential=false`; dès trois, exactement
trois ont `essential=true`: les trois premiers. Sous cinq : `watch`. Applique
`03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`.
Avant sortie, vérifie chaque invariant du contrat puis analyse exactement le JSON
émis avec un parseur. Sinon : `PAQUET_INCOMPLET | JSON_INVALIDE`.
Réponds par un seul bloc copiable :
recopie le contenu sous `## PASSERELLE_RENDU`, sans ce titre, puis
`SNUM_PAQUET_RENDU_V519_START`, le JSON, `SNUM_PAQUET_RENDU_V519_END` et
`PAQUET_RENDU_PRET`, dans un bloc `text`. Aucun préambule ni texte hors du bloc.
N’écris aucun brouillon ni JSON avant ces marqueurs; compose le bloc une seule fois.
Toute demande de redonner le JSON répète à l’identique ce même bloc complet.
N’émets jamais `PAQUET_RENDU_PRET`
si une limite échoue. Après analyse réussie, termine par `PAQUET_RENDU_PRET`.
`GENERER_PAQUET` n’est jamais `ETAT_INVALIDE` dans cet état. Une transition par tour.
