"""Archives des collectes publiées, sur la branche donnees-veille.

`entree` résume une collecte à partir des trois fichiers publiés ; `fusionner`
l'ajoute en tête de l'index existant. La tâche GitHub recalcule la fusion sur
la version distante à chaque tentative d'envoi : aucune entrée n'est perdue.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

SCHEMA = "SNUM_ARCHIVES_V1"
FICHIERS = ("paquet-v519.json", "candidats-ecartes.json", "rapport-collecte.json")


def lire(chemin):
    return json.loads(Path(chemin).read_text(encoding="utf-8"))


def entree(site, run_id, maintenant):
    site = Path(site)
    paquet = lire(site / "paquet-v519.json")
    rapport = lire(site / "rapport-collecte.json")
    ecartes = lire(site / "candidats-ecartes.json")
    # Instant de la collecte des titres que cette archive résume : le second temps
    # s'en sert pour refuser de résumer deux fois les mêmes titres.
    origine = rapport.get("started_at_utc")
    return ({"titres_started_at": origine} if isinstance(origine, str) else {}) | {
        "id": f"{paquet['edition_date']}_{run_id}",
        "run_id": run_id,
        "edition_date": paquet["edition_date"],
        "window_start": paquet["window_start"],
        "window_end": paquet["window_end"],
        "status": rapport["status"],
        "articles": len(paquet["articles"]),
        "candidats": len(rapport.get("candidates") or []),
        "ecartes": len(ecartes.get("candidates") or []),
        "archived_at": maintenant.astimezone(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }


def fusionner(ancien, nouvelle):
    """Nouvelle collecte en tête ; même identifiant remplacé ; entrées illisibles écartées."""
    collectes = ancien.get("collectes") if isinstance(ancien, dict) else None
    valides = [
        c
        for c in (collectes if isinstance(collectes, list) else [])
        if isinstance(c, dict)
        and isinstance(c.get("id"), str)
        and c["id"] != nouvelle["id"]
    ]
    return {"schema_version": SCHEMA, "collectes": [nouvelle, *valides]}


def ecrire(chemin, contenu):
    Path(chemin).write_text(
        json.dumps(contenu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Archives des collectes Veille SNUM.")
    commandes = parser.add_subparsers(dest="commande", required=True)
    e = commandes.add_parser("entree", help="entrée d'index d'une collecte publiée")
    e.add_argument("--site", required=True)
    e.add_argument("--run-id", type=int, required=True)
    e.add_argument("--sortie", required=True)
    f = commandes.add_parser(
        "fusion", help="index existant (fichier absent admis) + entrée"
    )
    f.add_argument("--ancien", required=True)
    f.add_argument("--entree", required=True)
    f.add_argument("--sortie", required=True)
    args = parser.parse_args(argv)
    if args.commande == "entree":
        ecrire(
            args.sortie,
            entree(args.site, args.run_id, dt.datetime.now(dt.timezone.utc)),
        )
    else:
        try:
            ancien = lire(args.ancien)
        except (OSError, ValueError):
            ancien = None
        ecrire(args.sortie, fusionner(ancien, lire(args.entree)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
