"""Repêchage d'un candidat écarté, lancé par la page de sélection via GitHub Actions.

La page relue est un article public d'une des 13 sources ; Albert le résume
dans la rubrique choisie par l'éditeur. Le jeton et le modèle Albert viennent
de l'environnement (ALBERT_API_KEY, ALBERT_MODEL). Le fichier de résultat est
écrit que le repêchage réussisse ou non : la page le lit ensuite sans jeton.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit

from .core import (
    ALBERT_THROTTLE_RETRIES,
    ALBERT_TIMEOUT,
    RUBRICS,
    HttpClient,
    _retry_delay,
    albert_summary,
    contains_challenge,
    date_long,
    is_bot_wall,
    iso_date,
    no_em_dash,
    normalized_url,
    parse_page,
    robots_allowed,
    sources,
    url_key,
    validate_summary,
)
from .publier import date_saisie

SCHEMA = "SNUM_REPECHAGE_V1"
CHAMPS_ARTICLE = (
    "rubric",
    "title",
    "source",
    "publication_date_iso",
    "publication_date_long",
    "url",
    "fact",
    "keywords",
    "takeaway",
    "snum_interest",
)
# Codes de rejet de validate_summary : seuls textes d'exception recopiés tels quels.
CODE_REJET = re.compile(r"[A-Z_]+(:[a-z_]+)?")


class Refus(ValueError):
    """Motif rédigé ici, sans donnée sensible, renvoyé tel quel à la page."""


def motif(exc):
    """Code de rejet connu, sinon le seul type : un texte d'exception peut porter le jeton."""
    texte = str(exc)
    if type(exc) is ValueError and CODE_REJET.fullmatch(texte):
        return texte
    return type(exc).__name__


def source_publique(url):
    """Source publique à laquelle l'adresse appartient, avec l'adresse normalisée."""
    for source in sources():
        if source["internal"]:
            continue
        try:
            return source, normalized_url(url, source["domain"])
        except ValueError:
            continue
    raise Refus("URL hors des 13 sources publiques ou non HTTPS.")


def lire_candidat(url, source, debut, fin, client):
    """Mêmes contrôles que la visite d'un article par discover_source, pour une seule page."""
    domaine = source["domain"]
    try:
        if not robots_allowed(client, source["homepage"], domaine, url):
            raise Refus("Page interdite aux robots par le site.")
        adresse, brut = client.get(url, domaine)
    except Refus:
        raise
    except HTTPError as exc:
        raise Refus(f"Page illisible : HTTP {exc.code}") from exc
    except Exception as exc:
        raise Refus(f"Page illisible : {type(exc).__name__}") from exc
    if is_bot_wall(brut):
        raise Refus("Page remplacée par une vérification anti-robot.")
    page = parse_page(brut)
    try:
        canonique = (
            normalized_url(urljoin(adresse, page.canonical), domaine)
            if page.canonical
            else adresse
        )
    except ValueError as exc:
        raise Refus("Adresse canonique hors du domaine de la source.") from exc
    identite = canonique
    # Lien court WordPress (/?p=123) : même page, l'adresse lisible est publiée.
    decoupe = urlsplit(canonique)
    if decoupe.path == "/" and re.fullmatch(r"p=\d+", decoupe.query):
        canonique = adresse
    if url_key(canonique) != url_key(adresse):
        raise Refus("Adresse canonique différente de la page lue.")
    publication = page.publication_date(adresse, identite)
    if not publication:
        raise Refus("Date de publication absente de la page.")
    if not debut <= iso_date(publication) <= fin:
        raise Refus(
            f"Article du {date_long(publication)}, hors de la période "
            f"du {date_long(debut.isoformat())} au {date_long(fin.isoformat())}."
        )
    if page.paywall:
        raise Refus("Contenu payant : extrait insuffisant.")
    if contains_challenge(page, brut):
        raise Refus("Page remplacée par une vérification anti-robot.")
    contenu = "\n".join(page.paragraphs)
    if len(page.paragraphs) < 2 or len(contenu) < 220:
        raise Refus("Texte de l'article trop court pour être résumé.")
    titre = " ".join((page.og_title or page.title).split())
    # Un og:title réduit au nom du site n'est pas un titre.
    if (
        " " not in titre or titre.lower().removeprefix("www.") == domaine
    ) and page.headings:
        titre = page.headings[0]
    if len(titre) < 12:
        raise Refus("Titre de l'article absent.")
    return {
        "title": no_em_dash(titre),
        "source": source["label"],
        "publication_date_iso": publication,
        "url": canonique,
        "content": contenu[:2400],
    }


def resumer_valide(candidat, rubrique, resumer, limite=None):
    """Comme analyze de la collecte : attente sur 429/503, une seconde tentative après un rejet.

    `limite` (horloge monotone) borne les attentes et la seconde tentative ; None : sans budget.
    """
    feedback, repris, attentes = None, False, 0
    while True:
        try:
            reponse = resumer(candidat, feedback=feedback, forced_rubric=rubrique)
            if not isinstance(reponse, dict):
                raise ValueError("SORTIE_ALBERT_INVALIDE")  # noqa: TRY004 -- ValueError déclenche la seconde tentative
            return validate_summary({**reponse, "relevant": True, "rubric": rubrique})
        except HTTPError as exc:
            if exc.code in (429, 503) and attentes < ALBERT_THROTTLE_RETRIES:
                delai = _retry_delay(exc, attentes)
                if limite is None or time.monotonic() + delai < limite:
                    attentes += 1
                    time.sleep(delai)
                    continue
            raise
        except Exception as exc:
            if repris or (limite is not None and time.monotonic() >= limite):
                raise
            repris = True
            feedback = motif(exc)


def resultat(url, message, article=None):
    return {
        "schema_version": SCHEMA,
        "url": url[:2048] if isinstance(url, str) else "",
        "status": "ok" if article else "erreur",
        "message": message,
        "article": article,
    }


def repecher(url, rubrique, debut, fin, client, resumer):
    """Résultat SNUM_REPECHAGE_V1 ; `debut` et `fin` sont des dates, `resumer` appelle Albert."""
    try:
        if not isinstance(rubrique, str) or rubrique not in RUBRICS:
            raise Refus("Rubrique inconnue : attendu " + ", ".join(RUBRICS) + ".")
        if debut > fin:
            raise Refus("Période invalide : le début suit la fin.")
        if (fin - debut).days > 60:
            raise Refus("Période invalide : 61 jours au plus, comme pour la collecte.")
        source, adresse = source_publique(url)
        candidat = lire_candidat(adresse, source, debut, fin, client)
    except Refus as exc:
        return resultat(url, str(exc))
    try:
        resume = resumer_valide(candidat, rubrique, resumer)
    except HTTPError as exc:
        return resultat(url, f"Albert : HTTP {exc.code}")
    except Exception as exc:  # noqa: BLE001 -- dernier recours, aucun détail exposé
        return resultat(url, f"Albert : {motif(exc)}")
    article = {
        **candidat,
        **resume,
        "publication_date_long": date_long(candidat["publication_date_iso"]),
    }
    return resultat(
        url,
        f"Article repêché dans la rubrique {rubrique}.",
        {champ: article[champ] for champ in CHAMPS_ARTICLE},
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Repêchage d'un candidat écarté : résumé Albert dans la rubrique choisie."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--rubrique", required=True)
    parser.add_argument("--debut", required=True, help="JJ/MM/AAAA ou AAAA-MM-JJ")
    parser.add_argument("--fin", required=True, help="JJ/MM/AAAA ou AAAA-MM-JJ")
    parser.add_argument("--sortie", required=True, help="fichier JSON de résultat")
    args = parser.parse_args(argv)
    cle = os.environ.get("ALBERT_API_KEY", "").strip()
    modele = os.environ.get("ALBERT_MODEL", "").strip()

    def resumer(candidat, feedback=None, forced_rubric=None):
        return albert_summary(
            candidat,
            cle,
            modele,
            timeout=ALBERT_TIMEOUT,
            feedback=feedback,
            forced_rubric=forced_rubric,
        )

    try:
        debut, fin = date_saisie(args.debut), date_saisie(args.fin)
    except argparse.ArgumentTypeError as exc:
        # Refus écrit dans le fichier, et non par argparse : la page doit pouvoir le lire.
        bilan = resultat(args.url, f"Période refusée : {exc}")
    else:
        if cle and modele:
            bilan = repecher(args.url, args.rubrique, debut, fin, HttpClient(), resumer)
        else:
            bilan = resultat(
                args.url, "Albert non configuré : impossible de résumer cet article."
            )
    sortie = Path(args.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(
        json.dumps(bilan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Repêchage {bilan['status']} : {bilan['message']}")
    return 0 if bilan["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
