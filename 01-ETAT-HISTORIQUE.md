# État et historique SNUM - V5.6

## VERROU-ETAT - lire avant toute date

`DERNIERE_EDITION_REUSSIE` vaut `NON_ETABLIE`. `DERNIERE_FIN_COLLECTE_REUSSIE` vaut `INCONNUE`. L’édition publiée du 2 octobre ne prouve ni une réussite complète ni une fin de collecte au 2 octobre. Il est interdit d’en déduire une fenêtre commençant le 3 octobre.

Le brouillon actif du 13 octobre conserve sa fenêtre explicitement fixée du 2 au 12 octobre 2026 inclus, journées civiles Europe/Paris. Pour une nouvelle date postérieure, ne réutilise pas cette fenêtre et n’invente pas de borne : pose uniquement la question indispensable sur la fenêtre initiale, sauf si le propriétaire demande explicitement de reprendre ce brouillon.

```text
REGISTRE_VERSION : 8
DATE_EDITION_PARIS : 2026-10-13
FENETRE_DEMANDEE : 2026-10-02 au 2026-10-12 inclus
DERNIERE_EDITION_REUSSIE : NON_ETABLIE
DERNIERE_FIN_COLLECTE_REUSSIE : INCONNUE
DERNIERE_EDITION_PUBLIEE : 2026-10-02, documentée dans le dépôt
PUBLICATION_DU_JOUR : INCONNUE
DIFFUSION_DU_JOUR : INCONNUE
BROUILLON_ACTIF : 2026-10-13-brouillon-01 ; A_COMPLETER
PROCHAINE_ACTION : reprendre ce brouillon, collecter, rédiger et livrer le JSON V5.6
```

La date ci-dessus décrit le dernier état enregistré, pas une consigne perpétuelle « aujourd’hui ». Une preuve plus récente fournie par le propriétaire doit être conservée sans effacer les preuves antérieures.

## Sources historiques relues

Dépôt : https://github.com/bacoco/revue-presse-snum

Révision consultée pour l’initialisation : `dc3c87f4f4e7305de0cd9c71da25171252402a83`.

- Accueil : `index.html` à cette révision.
- Archives : `editions/index.html` à cette révision.
- Compte rendu : `comptes-rendus/2026-10-02.md`.
- Complément de diffusion : `comptes-rendus/2026-10-02-diffusion.md`.

Ces sources établissent une édition du 2 octobre comportant onze sujets et rapportent un envoi unique à 10 h 13 min 13 s, heure de Paris. Elles n’établissent pas ensemble une publication publique vérifiée et une diffusion confirmée. La borne de collecte réussie reste donc inconnue.

## Événements déjà couverts le 2 octobre

Un suivi est possible seulement avec une évolution nouvelle et datée.

- incidents ANSSI concernant la DGFiP ;
- réorganisation DINUM et DITSP ;
- activité et API de la DILA ;
- support CNIL pour les victimes de fuites ;
- correctifs de sécurité WordPress ;
- offre cloud IONOS-Softeam et qualification ;
- enquête BCG sur la valeur de l’IA ;
- webinaire public sur IA et apprentissage ;
- accompagnement managérial de l’IA ;
- mouvement social du 29 septembre ;
- projet budgétaire 2027.

## Constats historiques non normatifs

Les anciens brouillons, fiches, exemples et HTML ne sont ni publiés ni des sources à recopier. Ils ont notamment mélangé dates de publication et d’événement, retenu des extraits ou contenus payants, inventé des lectures intégrales et reconstruit le gabarit.

La tentative V5.6 de faire recopier une longue coque HTML par récupération de passages a aussi échoué : même après correction, l’assistant a réécrit le footer, omis des scripts et liens réglementaires et dépassé une limite de mots. Le format actif est donc le JSON structuré de `03-FORMAT-SORTIE.md`, assemblé ensuite par le générateur déterministe local.

Ces essais ne font avancer aucune borne de réussite. Ils servent uniquement à empêcher la répétition de leurs erreurs.
