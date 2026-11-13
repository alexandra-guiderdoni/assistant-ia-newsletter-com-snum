"""Collecte complète puis écriture du paquet V519 publié sur GitHub Pages.

Le jeton et le modèle Albert viennent de l'environnement (ALBERT_API_KEY,
ALBERT_MODEL). Seul un paquet complet ou partiel est écrit : sinon le code
de sortie vaut 1 et le paquet déjà publié reste en place.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from .core import collect

FICHIER = "paquet-v519.json"
PUBLIABLES = ("ready", "partial")


def fenetre(aujourdhui, jours=7):
    """Même période par défaut que la page : les sept jours précédant l'édition."""
    debut = aujourdhui - dt.timedelta(days=jours)
    return {
        "edition_date": aujourdhui.isoformat(),
        "window_start": debut.isoformat(),
        "window_end": aujourdhui.isoformat(),
    }


def date_saisie(texte):
    """Date du formulaire GitHub : JJ/MM/AAAA, ou AAAA-MM-JJ par compatibilité."""
    valeur = texte.strip()
    for forme in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            paris = ZoneInfo("Europe/Paris")
            return dt.datetime.strptime(valeur, forme).replace(tzinfo=paris).date()
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(
        f"date invalide « {valeur} » : attendu JJ/MM/AAAA, par exemple 20/11/2026"
    )


def publier(payload, sortie, collecter=collect):
    rapport = collecter(payload)
    paquet = rapport.get("packet")
    if rapport["status"] not in PUBLIABLES or not paquet:
        erreurs = len(rapport.get("errors") or [])
        print(
            f"Aucun paquet publiable : statut {rapport['status']}, {erreurs} échec(s) Albert.",
            file=sys.stderr,
        )
        return 1
    sortie = Path(sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    texte = json.dumps(paquet, ensure_ascii=False, indent=2) + "\n"
    (sortie / FICHIER).write_text(texte, encoding="utf-8")
    print(
        f"Paquet {rapport['status']} : {len(paquet['articles'])} article(s), "
        f"{len(rapport.get('candidates') or [])} candidat(s), {len(rapport.get('errors') or [])} échec(s) Albert."
    )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Collecte complète puis écriture du paquet V519."
    )
    parser.add_argument(
        "--edition",
        type=date_saisie,
        help="JJ/MM/AAAA ; aujourd'hui, heure de Paris, par défaut",
    )
    parser.add_argument(
        "--debut",
        type=date_saisie,
        help="JJ/MM/AAAA ; sept jours avant l'édition par défaut",
    )
    parser.add_argument(
        "--fin", type=date_saisie, help="JJ/MM/AAAA ; date d'édition par défaut"
    )
    parser.add_argument("--sortie", default="site")
    args = parser.parse_args(argv)
    edition = args.edition or dt.datetime.now(ZoneInfo("Europe/Paris")).date()
    payload = fenetre(edition)
    if args.debut:
        payload["window_start"] = args.debut.isoformat()
    if args.fin:
        payload["window_end"] = args.fin.isoformat()
    return publier(payload, args.sortie)


if __name__ == "__main__":
    sys.exit(main())
