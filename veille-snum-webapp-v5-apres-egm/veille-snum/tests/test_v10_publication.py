"""Publication du paquet V519 pour GitHub Pages : seul un paquet complet ou partiel est écrit."""

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_veille_snum import FakeHttp, good_summary
from veille_snum.core import collect
from veille_snum.publier import FICHIER, fenetre, main, publier

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


if __name__ == "__main__":
    unittest.main()
