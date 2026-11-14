"""Suivi de l'avancement : étapes de collecte et point d'accès local."""

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.test_veille_snum import FakeHttp, good_summary
from veille_snum import web
from veille_snum.core import collect

PAYLOAD = {
    "edition_date": "2026-11-11",
    "window_start": "2026-11-01",
    "window_end": "2026-11-10",
}


class ProgressionCollecteTests(unittest.TestCase):
    def test_etapes_sites_puis_albert_puis_termine(self):
        events = []
        collect(
            PAYLOAD,
            client=FakeHttp(),
            summarize=good_summary,
            progress=lambda **e: events.append(e),
        )
        phases = [e["phase"] for e in events]
        self.assertEqual(phases[0], "sites")
        self.assertEqual(phases[-1], "done")
        self.assertIn("albert", phases)
        self.assertLess(phases.index("sites"), phases.index("albert"))
        sites = [e for e in events if e["phase"] == "sites"]
        self.assertEqual(sites[0]["total"], 13)
        self.assertEqual(sites[-1]["done"], 13)
        self.assertTrue(all(e.get("current") for e in sites[:-1]))
        albert = [e for e in events if e["phase"] == "albert"]
        self.assertEqual(albert[-1]["done"], albert[-1]["total"])

    def test_sans_albert_pas_d_etape_albert(self):
        events = []
        collect(PAYLOAD, client=FakeHttp(), progress=lambda **e: events.append(e))
        self.assertNotIn("albert", [e["phase"] for e in events])
        self.assertEqual(events[-1]["phase"], "done")


class ProgressionHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
        cls.port = cls.server.server_address[1]
        cls.patch = mock.patch.object(web, "PORT", cls.port)
        cls.patch.start()
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.patch.stop()

    def get(self, host=None):
        req = Request(
            f"http://127.0.0.1:{self.port}/api/progress",
            headers={"Host": host or f"127.0.0.1:{self.port}"},
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            return exc.code, None

    def test_progression_exposee_sans_secret(self):
        web.update_progress(phase="albert", done=3, total=9, current="Next")
        code, body = self.get()
        self.assertEqual(code, 200)
        self.assertEqual(
            body, {"phase": "albert", "done": 3, "total": 9, "current": "Next"}
        )

    def test_progression_refuse_un_autre_hote(self):
        code, _ = self.get(host="www.example.com")
        self.assertEqual(code, 403)

    def test_page_interroge_la_progression(self):
        script = (Path(web.__file__).parent / "app.js").read_text(encoding="utf-8")
        self.assertIn("/api/progress", script)



class ThematiquesAffichageTests(unittest.TestCase):
    def test_articles_groupes_sous_leur_thematique(self):
        root = Path(web.__file__).parent
        script = (root / "app.js").read_text(encoding="utf-8")
        page = (root / "index.html").read_text(encoding="utf-8")
        for label in ("Intelligence artificielle (IA)", "Administration électronique", "DSI, méthode, métier",
                      "Économie numérique", "Infrastructure, réseaux", "Sécurité informatique",
                      "Applications et développement", "Droit, informatique et libertés", "Achat public",
                      "Ressources humaines et nominations", "Vie de Bercy"):
            self.assertIn(label, script)
        self.assertIn("RUBRIC_LABELS", script)
        self.assertNotIn("${a.rubric} ·", script)
        self.assertIn('<div id="article-list">', page)

if __name__ == "__main__":
    unittest.main()
