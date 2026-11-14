"""Collecte puis écriture des fichiers publiés sur GitHub Pages.

Mode « collecte » : collecte complète avec Albert et paquet V519. Le jeton et
le modèle Albert viennent de l'environnement (ALBERT_API_KEY, ALBERT_MODEL).
Seul un paquet complet ou partiel est écrit : sinon le code de sortie vaut 1
et le site déjà publié reste en place.

Mode « titres » : premier temps de la collecte en deux temps. Les sites sont
explorés sans Albert ; seuls l'état et le rapport (liste des titres) sont
écrits. Le second temps est dans resumer.py.
"""

import argparse
import contextlib
import datetime as dt
import json
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from .core import collect, date_long

FICHIER = "paquet-v519.json"
ECARTES = "candidats-ecartes.json"
RAPPORT_PUBLIE = "rapport-collecte.json"
ETAT = "etat-collecte.json"
SCHEMA_ETAT = "SNUM_ETAT_V1"
# Listes de milliers d'adresses non visitées : seuls leurs nombres sont publiés.
LISTES_SOURCE = ("not_visited_urls", "sitemap_skipped_urls")
PUBLIABLES = ("ready", "partial")
CHAMPS_CANDIDAT = ("title", "source", "publication_date_iso", "url")


def rapport_public(rapport):
    """Rapport de collecte de la page : sans le paquet, publié à part, ni listes d'adresses."""
    sources = [
        {k: v for k, v in s.items() if k not in LISTES_SOURCE}
        for s in rapport.get("sources") or []
    ]
    return {k: v for k, v in rapport.items() if k != "packet"} | {"sources": sources}


def ecartes(rapport):
    """Candidats trouvés mais absents du paquet, avec leur motif, sans extrait d'article."""
    retenus = {a["url"] for a in (rapport.get("packet") or {}).get("articles", [])}
    motifs = {e["url"]: e["reason"] for e in rapport.get("excluded") or []}
    motifs.update({e["url"]: "ECHEC_ALBERT" for e in rapport.get("errors") or []})
    return [
        {k: c[k] for k in CHAMPS_CANDIDAT}
        | {
            "publication_date_long": date_long(c["publication_date_iso"]),
            "reason": motifs.get(c["url"], "NON_RETENU"),
        }
        for c in rapport.get("candidates") or []
        if c["url"] not in retenus
    ]


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


def etat(phase, rapport, run_id):
    """État lu par la page pour savoir quoi afficher : titres à cocher ou paquet à trier."""
    return {
        "schema_version": SCHEMA_ETAT,
        "phase": phase,
        "edition_date": rapport["edition_date"],
        "window_start": rapport["window_start"],
        "window_end": rapport["window_end"],
        "run_id": run_id,
        "candidats": len(rapport.get("candidates") or []),
        "articles": len((rapport.get("packet") or {}).get("articles") or []),
    }


def ecrire_site(rapport, sortie, phase, run_id):
    """État et rapport toujours ; paquet et candidats écartés si le rapport porte un paquet."""
    sortie = Path(sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    contenus = {
        RAPPORT_PUBLIE: rapport_public(rapport),
        ETAT: etat(phase, rapport, run_id),
    }
    paquet = rapport.get("packet")
    if paquet:
        contenus[FICHIER] = paquet
        contenus[ECARTES] = {
            "schema_version": "SNUM_CANDIDATS_ECARTES_V1",
            "edition_date": paquet["edition_date"],
            "window_start": paquet["window_start"],
            "window_end": paquet["window_end"],
            "candidates": ecartes(rapport),
        }
    for nom, contenu in contenus.items():
        (sortie / nom).write_text(
            json.dumps(contenu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


def collecte_ou_refus(collecter, payload):
    """Rapport de collecte, ou None après un refus lisible : période inversée ou de plus de 61 jours."""
    try:
        return collecter(payload)
    except ValueError as exc:
        print(f"Collecte refusée : {exc}.", file=sys.stderr)
        return None


def publier(payload, sortie, collecter=collect, run_id=0):
    rapport = collecte_ou_refus(collecter, payload)
    if rapport is None:
        return 1
    paquet = rapport.get("packet")
    if rapport["status"] not in PUBLIABLES or not paquet:
        erreurs = len(rapport.get("errors") or [])
        print(
            f"Aucun paquet publiable : statut {rapport['status']}, {erreurs} échec(s) Albert.",
            file=sys.stderr,
        )
        return 1
    ecrire_site(rapport, sortie, "collecte", run_id)
    print(
        f"Paquet {rapport['status']} : {len(paquet['articles'])} article(s), "
        f"{len(rapport.get('candidates') or [])} candidat(s), {len(rapport.get('errors') or [])} échec(s) Albert."
    )
    return 0


@contextlib.contextmanager
def sans_albert():
    """Jeton et modèle retirés de l'environnement le temps du bloc : collect ne peut pas appeler Albert."""
    retires = {
        nom: os.environ.pop(nom, None) for nom in ("ALBERT_API_KEY", "ALBERT_MODEL")
    }
    try:
        yield
    finally:
        os.environ.update({n: v for n, v in retires.items() if v is not None})


def publier_titres(payload, sortie, collecter=collect, run_id=0):
    """Premier temps : « needs_albert » est le statut attendu, pas un échec."""
    with sans_albert():
        rapport = collecte_ou_refus(collecter, payload)
    if rapport is None:
        return 1
    if rapport["status"] != "needs_albert":
        print(f"Aucun titre publiable : statut {rapport['status']}.", file=sys.stderr)
        return 1
    ecrire_site(rapport, sortie, "titres", run_id)
    print(
        f"Titres publiés : {len(rapport.get('candidates') or [])} candidat(s), sans appel Albert."
    )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Collecte puis écriture des fichiers publiés : paquet V519 ou titres seuls."
    )
    parser.add_argument(
        "--mode",
        choices=("collecte", "titres"),
        default="collecte",
        help="collecte : complète, avec Albert ; titres : exploration seule, sans Albert",
    )
    parser.add_argument(
        "--run-id", type=int, default=0, help="numéro du run GitHub, écrit dans l'état"
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
    if args.mode == "titres":
        return publier_titres(payload, args.sortie, run_id=args.run_id)
    return publier(payload, args.sortie, run_id=args.run_id)


if __name__ == "__main__":
    sys.exit(main())
