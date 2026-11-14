# Comparaison avant/après

dbabaa5 -> a13adfa, mode hybride. {'units_checked': 8, 'behavior_changes': 7, 'new_errors': 0, 'surprises': 0, 'evidence_mix': {'reasoned': 4, 'measured': 10}, 'by_verdict': {'unchanged': 1, 'behavior-changed': 7, 'new-error': 0}}

## Mesuré
- publier.main sans --mode (nominal) : output-changed. Le mode par défaut de publier.main écrit en plus etat-collecte.json (phase collecte) ; paquet, écartés et rapport inchangés.
- publier.main sans --mode (tout hors thématique) : output-changed. Le mode par défaut de publier.main écrit en plus etat-collecte.json (phase collecte) ; paquet, écartés et rapport inchangés.
- publier.main sans --mode (aucune source lue) : identical. Le mode par défaut de publier.main écrit en plus etat-collecte.json (phase collecte) ; paquet, écartés et rapport inchangés.
- publier.main --mode titres (nominal) : now-recovers. Nouveau mode titres : état et rapport seulement, sans paquet. L'ancienne version refusait l'option.
- repecher.repecher (nominal) : identical. Repêchage inchangé : mêmes attentes (trois fois 20 s sur 429), même seconde tentative.
- repecher.repecher (Albert sature (429)) : identical. Repêchage inchangé : mêmes attentes (trois fois 20 s sur 429), même seconde tentative.
- repecher.repecher (rejet puis réponse valide) : identical. Repêchage inchangé : mêmes attentes (trois fois 20 s sur 429), même seconde tentative.
- archiver.entree (rapport avec started_at_utc) : output-changed. L'entrée d'archive porte en plus titres_started_at quand le rapport a started_at_utc ; inchangée sinon.
- archiver.entree (rapport sans started_at_utc) : identical. L'entrée d'archive porte en plus titres_started_at quand le rapport a started_at_utc ; inchangée sinon.
- archiver.entree (dossier vide) : identical. L'entrée d'archive porte en plus titres_started_at quand le rapport a started_at_utc ; inchangée sinon.

## Raisonné
- tâche publier-paquet-snum.yml, lancement sans entrée mode : output-changed. collecte complète avec Albert, paquet publié et archivé. -> mode titres, sans Albert, état et rapport seulement ; l'ancien paquet quitte le site. Changement voulu par le contrat ; une page restée ouverte avec l'ancien script lance donc des titres sans savoir les afficher, jusqu'au rechargement.
- tâche publier-paquet-snum.yml, mode collecte : output-changed. archivage et déploiement en parallèle après la collecte. -> archivage, puis déploiement seulement si l'archivage a réussi ; paquet sans article publié sans archive. Un archivage en échec empêche désormais la publication : la page l'annonce comme un échec, à relancer. La publication arrive plus tard d'environ la durée de l'archivage.
- tâche publier-paquet-snum.yml, mode page seule : output-changed. paquet exigé, écartés et rapport facultatifs. -> état repris ; en phase titres seul le rapport est exigé ; chaque lecture retentée trois fois. Mesuré séparément en bash -eo pipefail avec le vrai curl (preuves 03) : états titres, resumes, collecte, site antérieur, 503 passagers.
- tâche repecher-candidat.yml, publication du résultat : now-recovers. un git fetch en échec arrêtait la tâche. -> nouvel essai, cinq au plus. Mesuré séparément avec le vrai git contre un dépôt nu local (preuves 10).

## Non couvert
- resumer.publier_resumes : module nouveau, sans version antérieure à comparer (couvert par le contrôle de logique)
- exécution réelle des tâches sur GitHub Actions : non lancée
