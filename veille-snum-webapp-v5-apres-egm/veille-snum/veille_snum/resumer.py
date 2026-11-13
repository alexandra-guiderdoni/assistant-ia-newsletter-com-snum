"""Second temps de la collecte : Albert ne résume que les titres gardés par l'éditeur.

Le premier temps (publier.py, mode « titres ») a publié la liste des candidats
dans rapport-collecte.json. Ce module relit ce rapport sur le site en ligne,
refuse toute adresse qui n'y figure pas, relit chaque page gardée comme le
repêchage, puis demande le résumé à Albert : rubrique imposée si l'éditeur en
a choisi une, classement libre sinon. Le jeton et le modèle Albert viennent de
l'environnement (ALBERT_API_KEY, ALBERT_MODEL). Rien n'est écrit si la
sélection est refusée ou si aucun résumé n'aboutit : le site reste en place.
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from urllib.error import HTTPError

from .core import (
    ALBERT_THROTTLE_RETRIES,
    ALBERT_TIMEOUT,
    ALBERT_WORKERS,
    MAX_ALBERT_SECONDS,
    MAX_ARTICLES,
    RUBRICS,
    STATE_STATUSES,
    HttpClient,
    _retry_delay,
    albert_summary,
    iso_date,
    packet_for,
    validate_packet_v519,
    validate_summary,
)
from .publier import CHAMPS_CANDIDAT, date_saisie, ecrire_site
from .repecher import Refus, lire_candidat, motif, resumer_valide, source_publique

DOMAINE_SITE = "alexandra-guiderdoni.github.io"
RAPPORT_EN_LIGNE = (
    f"https://{DOMAINE_SITE}/assistant-ia-newsletter-com-snum/rapport-collecte.json"
)
NON_SELECTIONNE = "NON_SELECTIONNE"
PAGE_NON_RELUE = "PAGE_NON_RELUE"


def lire_selection(texte):
    """Sélection de la page : liste JSON de 1 à 60 couples adresse et rubrique (vide : Albert choisit)."""
    try:
        choix = json.loads(texte)
    except (TypeError, ValueError) as exc:
        raise Refus("Sélection illisible : liste JSON attendue.") from exc
    if not isinstance(choix, list) or not 1 <= len(choix) <= MAX_ARTICLES:
        raise Refus(f"Sélection refusée : 1 à {MAX_ARTICLES} articles attendus.")
    retenus = []
    for rang, element in enumerate(choix, 1):
        if (
            not isinstance(element, dict)
            or "url" not in element
            or not isinstance(element["url"], str)
            or not set(element) <= {"url", "rubrique"}
        ):
            raise Refus(
                f"Sélection refusée : l'élément {rang} doit porter « url » et « rubrique »."
            )
        rubrique = element.get("rubrique", "")
        if not isinstance(rubrique, str) or (rubrique and rubrique not in RUBRICS):
            raise Refus(
                f"Rubrique inconnue à l'élément {rang} : attendu "
                + ", ".join(RUBRICS)
                + ", ou vide."
            )
        retenus.append({"url": element["url"], "rubrique": rubrique})
    return retenus


def lire_rapport(client, adresse=RAPPORT_EN_LIGNE):
    """Rapport du premier temps, lu sur le site en ligne et contrôlé avant tout usage."""
    try:
        _, texte = client.get(adresse, DOMAINE_SITE, max_bytes=3_000_000, timeout=30)
    except HTTPError as exc:
        raise Refus(
            f"Rapport des titres introuvable en ligne : HTTP {exc.code}."
        ) from exc
    except Exception as exc:
        raise Refus(
            f"Rapport des titres introuvable en ligne : {type(exc).__name__}."
        ) from exc
    try:
        rapport = json.loads(texte)
        if iso_date(rapport["window_start"]) > iso_date(rapport["window_end"]):
            raise ValueError("période inversée")
        iso_date(rapport["edition_date"])
        sources, candidats = rapport["sources"], rapport["candidates"]
        valide = (
            isinstance(sources, list)
            and isinstance(candidats, list)
            and isinstance(rapport.get("excluded") or [], list)
            and all(
                isinstance(s, dict)
                and isinstance(s.get("label"), str)
                and s.get("status") in STATE_STATUSES
                and type(s.get("opened", 0)) is int
                and type(s.get("not_visited", 0)) is int
                for s in sources
            )
            and all(
                isinstance(c, dict)
                and all(isinstance(c.get(champ), str) for champ in CHAMPS_CANDIDAT)
                for c in candidats
            )
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise Refus("Rapport des titres illisible : relancer la collecte.") from exc
    if not valide:
        raise Refus("Rapport des titres incomplet : relancer la collecte.")
    return rapport


def classer_valide(candidat, resumer, limite):
    """Classement libre, comme analyze de la collecte : None signifie hors thématique."""
    feedback, repris, attentes = None, False, 0
    while True:
        try:
            return validate_summary(resumer(candidat, feedback=feedback))
        except HTTPError as exc:
            if exc.code in (429, 503) and attentes < ALBERT_THROTTLE_RETRIES:
                delai = _retry_delay(exc, attentes)
                if time.monotonic() + delai < limite:
                    attentes += 1
                    time.sleep(delai)
                    continue
            raise
        except Exception as exc:
            if repris or time.monotonic() >= limite:
                raise
            repris = True
            # Jamais le texte brut de l'exception : il peut porter le jeton.
            feedback = motif(exc)


def resumer_gardes(choix, premier, edition, client, resumer):
    """Rapport du second temps, de même forme que celui de collect, paquet compris s'il existe."""
    debut, fin = iso_date(premier["window_start"]), iso_date(premier["window_end"])
    limite = time.monotonic() + MAX_ALBERT_SECONDS

    def traiter(element):
        source, adresse = source_publique(element["url"])
        candidat = lire_candidat(adresse, source, debut, fin, client)
        if element["rubrique"]:
            return candidat, resumer_valide(
                candidat, element["rubrique"], resumer, limite
            )
        return candidat, classer_valide(candidat, resumer, limite)

    issues = {}
    pool = ThreadPoolExecutor(max_workers=ALBERT_WORKERS)
    taches = {pool.submit(traiter, element): element["url"] for element in choix}
    en_attente = set(taches)
    while en_attente:
        reste = limite - time.monotonic()
        if reste <= 0:
            break
        finies, en_attente = wait(
            en_attente, timeout=reste, return_when=FIRST_COMPLETED
        )
        for tache in finies:
            try:
                issues[taches[tache]] = ("ok", tache.result())
            except Refus:
                issues[taches[tache]] = ("page", None)
            except Exception as exc:  # noqa: BLE001 -- dernier recours, aucun détail exposé
                issues[taches[tache]] = ("albert", exc)
    pool.shutdown(wait=False, cancel_futures=True)

    articles, relus, exclus, erreurs = [], {}, [], []
    gardes = {element["url"] for element in choix}
    for candidat in premier["candidates"]:
        url = candidat["url"]
        ecart = {"url": url, "source": candidat["source"]}
        if url not in gardes:
            exclus.append({**ecart, "reason": NON_SELECTIONNE})
            continue
        nature, valeur = issues.get(url, ("budget", None))
        if nature == "budget":
            exclus.append({**ecart, "reason": "BUDGET_DUREE_ALBERT"})
        elif nature == "page":
            exclus.append({**ecart, "reason": PAGE_NON_RELUE})
        elif nature == "albert":
            code = (
                f"HTTP {valeur.code}"
                if isinstance(valeur, HTTPError)
                else motif(valeur)
            )
            erreurs.append({"url": url, "reason": f"Albert : {code}"})
        else:
            relu, resume = valeur
            # La page relue fait foi : titre, date et adresse du jour remplacent ceux du premier temps.
            relus[url] = {champ: relu[champ] for champ in CHAMPS_CANDIDAT}
            if resume is None:
                exclus.append(
                    {
                        "url": relu["url"],
                        "source": relu["source"],
                        "reason": "HORS_THEMATIQUE",
                    }
                )
            else:
                articles.append({**relus[url], **resume})

    non_analyses = sum(1 for e in exclus if e["reason"] == "BUDGET_DUREE_ALBERT")
    non_relues = sum(1 for e in exclus if e["reason"] == PAGE_NON_RELUE)
    limites = dict(premier.get("limits") or {}) | {
        "unanalyzed_due_to_time": non_analyses
    }
    rapport = {
        **premier,
        "edition_date": edition.isoformat(),
        "candidates": [relus.get(c["url"], c) for c in premier["candidates"]],
        "excluded": [*(premier.get("excluded") or []), *exclus],
        "errors": erreurs,
        "limits": limites,
        "packet": None,
        "status": "incomplete",
    }
    incidents = bool(erreurs or non_analyses or non_relues)
    if incidents and not articles:
        return rapport
    paquet = packet_for(edition, debut, fin, articles, premier["sources"])
    laisses = limites.get("global_candidates_dropped") or 0
    if laisses:
        paquet["watch"].append(
            {
                "title": "Plafond global atteint",
                "summary": f"{laisses} candidat(s) admissibles n'ont pas été proposés à la sélection.",
            }
        )
    if incidents:
        paquet["watch"].append(
            {
                "title": "Analyse partielle",
                "summary": f"{len(erreurs)} échec(s) Albert, {non_relues} page(s) non relue(s) "
                f"et {non_analyses} article(s) non résumé(s) par manque de temps.",
            }
        )
    validate_packet_v519(paquet)
    degradees = any(
        s["status"] in ("error", "blocked", "partial", "skipped_budget")
        for s in premier["sources"]
    )
    rapport["packet"] = paquet
    rapport["status"] = "partial" if degradees or laisses or incidents else "ready"
    return rapport


def publier_resumes(
    selection, sortie, client, resumer, edition=None, debut=None, fin=None, run_id=0
):
    """Code de sortie 0 si le paquet est écrit ; `edition`, `debut` et `fin` sont des dates ou None."""
    try:
        choix = lire_selection(selection)
        premier = lire_rapport(client)
        for saisie, champ in ((debut, "window_start"), (fin, "window_end")):
            if saisie and saisie.isoformat() != premier[champ]:
                raise Refus(
                    "La période demandée ne correspond pas à celle des titres en ligne : "
                    "recharger la page, puis refaire la sélection."
                )
        connus = {c["url"] for c in premier["candidates"]}
        vus = set()
        for rang, element in enumerate(choix, 1):
            if element["url"] not in connus:
                raise Refus(
                    f"Adresse absente des titres collectés (élément {rang}) : "
                    "seuls les titres en ligne peuvent être résumés."
                )
            if element["url"] in vus:
                raise Refus(f"Adresse en double dans la sélection (élément {rang}).")
            vus.add(element["url"])
    except Refus as exc:
        print(f"Résumés refusés. {exc}", file=sys.stderr)
        return 1
    rapport = resumer_gardes(
        choix,
        premier,
        edition or iso_date(premier["edition_date"]),
        client,
        resumer,
    )
    paquet = rapport["packet"]
    if not paquet:
        print(
            f"Aucun paquet publiable : {len(rapport['errors'])} échec(s) Albert "
            f"sur {len(choix)} article(s) gardé(s).",
            file=sys.stderr,
        )
        return 1
    ecrire_site(rapport, sortie, "resumes", run_id)
    print(
        f"Paquet {rapport['status']} : {len(paquet['articles'])} article(s) "
        f"sur {len(choix)} gardé(s), {len(rapport['errors'])} échec(s) Albert."
    )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Résumés Albert des titres gardés, puis écriture du paquet V519."
    )
    parser.add_argument(
        "--selection",
        help="liste JSON des articles gardés ; variable SELECTION par défaut",
    )
    parser.add_argument(
        "--edition",
        type=date_saisie,
        help="JJ/MM/AAAA ; celle des titres par défaut",
    )
    parser.add_argument(
        "--debut", type=date_saisie, help="JJ/MM/AAAA ; contrôlé contre les titres"
    )
    parser.add_argument(
        "--fin", type=date_saisie, help="JJ/MM/AAAA ; contrôlé contre les titres"
    )
    parser.add_argument("--sortie", default="site")
    parser.add_argument(
        "--run-id", type=int, default=0, help="numéro du run GitHub, écrit dans l'état"
    )
    args = parser.parse_args(argv)
    cle = os.environ.get("ALBERT_API_KEY", "").strip()
    modele = os.environ.get("ALBERT_MODEL", "").strip()
    if not cle or not modele:
        print("Albert non configuré : impossible de résumer.", file=sys.stderr)
        return 1
    selection = (
        os.environ.get("SELECTION", "") if args.selection is None else args.selection
    )

    def resumer(candidat, feedback=None, forced_rubric=None):
        return albert_summary(
            candidat,
            cle,
            modele,
            timeout=ALBERT_TIMEOUT,
            feedback=feedback,
            forced_rubric=forced_rubric,
        )

    return publier_resumes(
        selection,
        args.sortie,
        HttpClient(),
        resumer,
        edition=args.edition,
        debut=args.debut,
        fin=args.fin,
        run_id=args.run_id,
    )


if __name__ == "__main__":
    sys.exit(main())
