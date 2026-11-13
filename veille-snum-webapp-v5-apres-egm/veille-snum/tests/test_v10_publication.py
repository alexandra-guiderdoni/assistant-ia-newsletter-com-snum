"""Publication du paquet V519 pour GitHub Pages : seul un paquet complet ou partiel est écrit."""

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_veille_snum import FakeHttp, good_summary
from veille_snum.core import collect
from veille_snum.publier import (
    ECARTES,
    FICHIER,
    RAPPORT_PUBLIE,
    ecartes,
    fenetre,
    main,
    publier,
)

TOKEN = "JETON-FACTICE-NE-PAS-PUBLIER"
PAYLOAD = {
    "edition_date": "2026-11-11",
    "window_start": "2026-11-01",
    "window_end": "2026-11-10",
}


def fake_collect(payload):
    return collect(payload, client=FakeHttp(), summarize=good_summary)


class FenetreTests(unittest.TestCase):
    def test_sept_jours_jusqua_la_date_d_edition(self):
        self.assertEqual(
            fenetre(dt.date(2026, 11, 13)),
            {
                "edition_date": "2026-11-13",
                "window_start": "2026-11-06",
                "window_end": "2026-11-13",
            },
        )

    def periode(self, *argv):
        with mock.patch("veille_snum.publier.publier", return_value=0) as appel:
            main(["--sortie", "x", *argv])
        return appel.call_args.args[0]

    def test_periode_calculee_depuis_l_edition_saisie(self):
        self.assertEqual(
            self.periode("--edition", "2026-11-20"),
            {
                "edition_date": "2026-11-20",
                "window_start": "2026-11-13",
                "window_end": "2026-11-20",
            },
        )

    def test_bornes_saisies_prioritaires(self):
        payload = self.periode(
            "--edition", "2026-11-20", "--debut", "2026-11-01", "--fin", "2026-11-19"
        )
        self.assertEqual(payload["window_start"], "2026-11-01")
        self.assertEqual(payload["window_end"], "2026-11-19")

    def test_dates_au_format_francais(self):
        self.assertEqual(
            self.periode(
                "--edition",
                "20/11/2026",
                "--debut",
                "01/11/2026",
                "--fin",
                "19/11/2026",
            ),
            {
                "edition_date": "2026-11-20",
                "window_start": "2026-11-01",
                "window_end": "2026-11-19",
            },
        )

    def test_edition_francaise_seule(self):
        payload = self.periode("--edition", " 20/11/2026 ")
        self.assertEqual(payload["window_start"], "2026-11-13")
        self.assertEqual(payload["window_end"], "2026-11-20")

    def test_date_impossible_refusee_avant_la_collecte(self):
        for valeur in ("31/02/2026", "20-11-2026", "2026/11/20", "lundi"):
            with (
                self.subTest(valeur=valeur),
                mock.patch("veille_snum.publier.publier") as appel,
                mock.patch("sys.stderr"),
                self.assertRaises(SystemExit) as fin,
            ):
                main(["--edition", valeur])
            self.assertEqual(fin.exception.code, 2)
            appel.assert_not_called()


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp())

    def test_paquet_ecrit_sans_le_jeton(self):
        with mock.patch.dict(
            "os.environ", {"ALBERT_API_KEY": TOKEN, "ALBERT_MODEL": "modele-test"}
        ):
            code = publier(PAYLOAD, self.dossier, collecter=fake_collect)
        self.assertEqual(code, 0)
        texte = (self.dossier / FICHIER).read_text(encoding="utf-8")
        paquet = json.loads(texte)
        self.assertEqual(paquet["edition_date"], "2026-11-11")
        self.assertEqual(len(paquet["articles"]), 13)
        self.assertNotIn(TOKEN, texte)

    def test_sans_albert_rien_n_est_ecrit(self):
        def sans_albert(payload):
            with mock.patch.dict(
                "os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}
            ):
                return collect(payload, client=FakeHttp())

        code = publier(PAYLOAD, self.dossier, collecter=sans_albert)
        self.assertEqual(code, 1)
        self.assertFalse((self.dossier / FICHIER).exists())

    def test_collecte_incomplete_rien_n_est_ecrit(self):
        rapport = {
            "status": "incomplete",
            "packet": None,
            "errors": [{"url": "u", "reason": "Albert : HTTP 401"}],
        }
        code = publier(PAYLOAD, self.dossier, collecter=lambda payload: rapport)
        self.assertEqual(code, 1)
        self.assertFalse((self.dossier / FICHIER).exists())
        self.assertFalse((self.dossier / ECARTES).exists())

    def test_candidats_ecartes_publies_a_cote_du_paquet(self):
        with mock.patch.dict(
            "os.environ", {"ALBERT_API_KEY": TOKEN, "ALBERT_MODEL": "modele-test"}
        ):
            publier(PAYLOAD, self.dossier, collecter=fake_collect)
        texte = (self.dossier / ECARTES).read_text(encoding="utf-8")
        publie = json.loads(texte)
        self.assertEqual(publie["schema_version"], "SNUM_CANDIDATS_ECARTES_V1")
        self.assertEqual(
            [publie["edition_date"], publie["window_start"], publie["window_end"]],
            ["2026-11-11", "2026-11-01", "2026-11-10"],
        )
        self.assertEqual(publie["candidates"], [])
        self.assertNotIn(TOKEN, texte)

    def test_rapport_publie_sans_paquet_ni_listes_d_adresses(self):
        with mock.patch.dict(
            "os.environ", {"ALBERT_API_KEY": TOKEN, "ALBERT_MODEL": "modele-test"}
        ):
            publier(PAYLOAD, self.dossier, collecter=fake_collect)
        texte = (self.dossier / RAPPORT_PUBLIE).read_text(encoding="utf-8")
        rapport = json.loads(texte)
        self.assertEqual(rapport["status"], "ready")
        self.assertNotIn("packet", rapport)
        self.assertEqual(len(rapport["sources"]), 14)
        self.assertEqual(len(rapport["candidates"]), 13)
        for source in rapport["sources"]:
            self.assertNotIn("not_visited_urls", source)
            self.assertNotIn("sitemap_skipped_urls", source)
            self.assertIn("not_visited", source)
        self.assertNotIn(TOKEN, texte)
        self.assertNotIn('"content"', texte)


def candidat(nom):
    return {
        "title": f"Titre {nom}",
        "source": "DINUM",
        "publication_date_iso": "2026-11-05",
        "url": f"https://exemple.gouv.fr/{nom}",
    }


RAPPORT = {
    "candidates": [candidat(n) for n in "abcd"],
    "packet": {"articles": [{"url": "https://exemple.gouv.fr/a"}]},
    "excluded": [
        {
            "url": "https://exemple.gouv.fr/b",
            "reason": "HORS_THEMATIQUE",
            "source": "numerique",
        },
        {
            "url": "https://exemple.gouv.fr/d",
            "reason": "BUDGET_DUREE_ALBERT",
            "source": "numerique",
        },
    ],
    "errors": [{"url": "https://exemple.gouv.fr/c", "reason": "Albert : HTTP 500"}],
}


class EcartesTests(unittest.TestCase):
    def test_candidats_non_retenus_avec_leur_motif(self):
        self.assertEqual(
            [(c["url"][-1], c["reason"]) for c in ecartes(RAPPORT)],
            [
                ("b", "HORS_THEMATIQUE"),
                ("c", "ECHEC_ALBERT"),
                ("d", "BUDGET_DUREE_ALBERT"),
            ],
        )

    def test_champs_publies_sans_extrait_d_article(self):
        premier = ecartes(
            {**RAPPORT, "candidates": [{**candidat("b"), "content": "Extrait."}]}
        )[0]
        self.assertEqual(
            sorted(premier),
            [
                "publication_date_iso",
                "publication_date_long",
                "reason",
                "source",
                "title",
                "url",
            ],
        )
        self.assertEqual(premier["publication_date_long"], "5 novembre 2026")


if __name__ == "__main__":
    unittest.main()
