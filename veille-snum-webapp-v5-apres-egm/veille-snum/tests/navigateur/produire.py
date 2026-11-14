"""Joue une étape de la tâche GitHub avec le VRAI code serveur (lignes de commande publier, resumer,
repecher, archiver), sources et Albert factices. Usage : produire.py <prototype> <consigne.json>.
La consigne décrit le mode, les entrées du lancement, l'état en ligne et le comportement d'Albert.
Code de sortie : celui du vrai module."""

import html
import io
import json
import sys
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.parse import urlsplit

proto, consigne = sys.argv[1], json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
sys.path[:0] = [proto, proto + "/tests"]
from test_veille_snum import FakeHttp, good_summary
from veille_snum import archiver, publier, repecher, resumer
from veille_snum.core import url_key

ALBERT = "https://albert.api.etalab.gouv.fr/v1/chat/completions"
JETON_ALBERT = "JETON-ALBERT-FACTICE-NE-PAS-PUBLIER"
mode, entrees, sortie = consigne["mode"], consigne.get("inputs", {}), consigne["sortie"]
en_ligne = Path(consigne["en_ligne"]) if consigne.get("en_ligne") else None
albert_cfg = consigne.get("albert", {})
PARAGRAPHE = "Cette publication décrit un service public numérique, son déploiement et les besoins concrets des administrations. "


class Reseau(FakeHttp):
    """Treize sources factices pour la collecte (jeu synthétique)."""

    def get(self, url, domain, max_bytes=600_000, timeout=7, deadline=None):
        return super().get(url, domain, max_bytes, timeout)


class SiteEnLigne(FakeHttp):
    """Site en ligne (rapport des titres) et pages d'articles : factices, ou fabriquées pour des titres réels."""

    def __init__(self):
        super().__init__()
        self.rapport = (
            (en_ligne / "rapport-collecte.json").read_text(encoding="utf-8")
            if en_ligne and (en_ligne / "rapport-collecte.json").exists()
            else None
        )
        candidats = (
            json.loads(self.rapport).get("candidates", []) if self.rapport else []
        )
        candidats += consigne.get("pages", [])
        self.pages = {
            url_key(c["url"]): c
            for c in candidats
            if isinstance(c, dict) and isinstance(c.get("url"), str)
        }
        self.illisibles = {url_key(u) for u in consigne.get("illisibles", [])}

    def get(self, url, domain, max_bytes=600_000, timeout=7):
        if url == resumer.RAPPORT_EN_LIGNE:
            if self.rapport is None:
                raise HTTPError(url, 404, "Not Found", {}, None)
            return url, self.rapport
        if urlsplit(url).path == "/robots.txt":
            return url, "User-agent: *\nAllow: /\n"
        if url_key(url) in self.illisibles:
            raise HTTPError(url, 403, "Forbidden", {}, None)
        c = self.pages.get(url_key(url))
        if c and consigne.get("jeu") == "reel":
            date = c.get("publication_relue") or c["publication_date_iso"]
            return url, (
                f'<html><head><meta property="article:published_time" content="{date}T09:10:00+01:00">'
                f'<meta property="og:title" content="{html.escape(c["title"], quote=True)}"></head>'
                f"<body><article><p>{PARAGRAPHE * 2}</p><p>{PARAGRAPHE * 2}</p></article></body></html>"
            )
        return super().get(url, domain, max_bytes, timeout)


def albert(candidat, cle, modele, timeout=30, feedback=None, forced_rubric=None):
    assert cle == JETON_ALBERT, "jeton Albert inattendu"
    url = candidat["url"]
    if albert_cfg.get("panne") == "tout" or url in albert_cfg.get("pannes", []):
        raise HTTPError(
            ALBERT, albert_cfg.get("code", 401), f"refus {JETON_ALBERT}", {}, None
        )
    if url in albert_cfg.get("hors", []) and not forced_rubric:
        return {"relevant": False}
    resume = good_summary(candidat)
    rubriques = albert_cfg.get("rubriques", {})
    return {**resume, "rubric": forced_rubric or rubriques.get(url, resume["rubric"])}


def dates():
    args = []
    for nom in ("edition", "debut", "fin"):
        if entrees.get(nom):
            args += [f"--{nom}", entrees[nom]]
    return args


env = {
    "ALBERT_API_KEY": JETON_ALBERT,
    "ALBERT_MODEL": "modele-factice",
    "SELECTION": entrees.get("selection", ""),
}
journal = io.StringIO()
with (
    mock.patch.dict("os.environ", env),
    mock.patch("sys.stdout", journal),
    mock.patch("sys.stderr", journal),
):
    if mode == "titres":
        if consigne.get("jeu") == "reel":
            # Premier temps à partir de titres réels : le rapport est écrit par le vrai ecrire_site.
            rapport = json.loads(
                Path(consigne["rapport_reel"]).read_text(encoding="utf-8")
            )
            parse = publier.main.__globals__["date_saisie"]
            rapport.update(
                edition_date=parse(entrees["edition"]).isoformat(),
                window_start=parse(entrees["debut"]).isoformat(),
                window_end=parse(entrees["fin"]).isoformat(),
            )
            publier.ecrire_site(rapport, sortie, "titres", int(consigne["run_id"]))
            code = 0
        else:
            with mock.patch("veille_snum.core.HttpClient", new=Reseau):
                code = publier.main(
                    [
                        "--mode",
                        "titres",
                        "--sortie",
                        sortie,
                        "--run-id",
                        str(consigne["run_id"]),
                        *dates(),
                    ]
                )
    elif mode == "collecte":
        with (
            mock.patch("veille_snum.core.HttpClient", new=Reseau),
            mock.patch("veille_snum.core.albert_summary", side_effect=albert),
        ):
            code = publier.main(
                ["--sortie", sortie, "--run-id", str(consigne["run_id"]), *dates()]
            )
    elif mode == "resumes":
        with (
            mock.patch("veille_snum.resumer.HttpClient", return_value=SiteEnLigne()),
            mock.patch("veille_snum.resumer.albert_summary", side_effect=albert),
        ):
            code = resumer.main(
                ["--sortie", sortie, "--run-id", str(consigne["run_id"]), *dates()]
            )
    elif mode == "repechage":
        with (
            mock.patch("veille_snum.repecher.HttpClient", return_value=SiteEnLigne()),
            mock.patch("veille_snum.repecher.albert_summary", side_effect=albert),
        ):
            code = repecher.main(
                [
                    f"--url={entrees['url']}",
                    f"--rubrique={entrees['rubrique']}",
                    f"--debut={entrees['debut']}",
                    f"--fin={entrees['fin']}",
                    f"--sortie={sortie}",
                ]
            )
    elif mode == "archive":
        # Entrée d'index puis fusion, comme les tâches « Préparer l'archive » et « Archiver la collecte ».
        code = archiver.main(
            [
                "entree",
                "--site",
                consigne["site"],
                "--run-id",
                str(consigne["run_id"]),
                "--sortie",
                sortie + "/entree.json",
            ]
        )
        code = code or archiver.main(
            [
                "fusion",
                "--ancien",
                consigne["ancien"],
                "--entree",
                sortie + "/entree.json",
                "--sortie",
                sortie + "/index.json",
            ]
        )
    else:
        raise SystemExit(f"mode inconnu : {mode}")
texte = journal.getvalue()
assert JETON_ALBERT not in texte, "le jeton Albert apparaît dans le journal"
sys.stdout.write(texte)
sys.exit(code)
