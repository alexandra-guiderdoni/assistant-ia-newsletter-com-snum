"""Modèle Albert par défaut : openweight-large, remplacé par ALBERT_MODEL, puis par le champ du formulaire."""

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from test_veille_snum import FakeHttp, good_summary
from veille_snum import core, web
from veille_snum.core import collect

PAYLOAD = {
    "edition_date": "2026-11-11",
    "window_start": "2026-11-01",
    "window_end": "2026-11-10",
}
TOKEN = "JETON-FACTICE-NE-PAS-EXPOSER"


def recording_albert(seen):
    """Remplace l'appel réseau à Albert et note le modèle demandé."""

    def fake(candidate, api_key, model, timeout=30, feedback=None, forced_rubric=None):
        seen.append(model)
        summary = good_summary(candidate)
        return {**summary, "rubric": forced_rubric} if forced_rubric else summary

    return fake


class CollecteModeleTests(unittest.TestCase):
    def models_used(self, env_model, supplied_model=None):
        seen = []
        payload = {**PAYLOAD, "albert_api_key": TOKEN}
        if supplied_model is not None:
            payload["albert_model"] = supplied_model
        with (
            mock.patch.dict(
                "os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": env_model}
            ),
            mock.patch.object(core, "albert_summary", recording_albert(seen)),
        ):
            report = collect(payload, client=FakeHttp())
        return report, set(seen)

    def test_jeton_seul_suffit_avec_openweight_large(self):
        report, models = self.models_used("")
        self.assertEqual(report["status"], "ready")
        self.assertEqual(models, {"openweight-large"})

    def test_variable_albert_model_remplace_le_defaut(self):
        _, models = self.models_used("modele-du-poste")
        self.assertEqual(models, {"modele-du-poste"})

    def test_champ_du_formulaire_prime_sur_la_variable(self):
        _, models = self.models_used("modele-du-poste", "modele-saisi")
        self.assertEqual(models, {"modele-saisi"})

    def test_sans_jeton_toujours_pas_de_paquet(self):
        with mock.patch.dict("os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}):
            report = collect(PAYLOAD, client=FakeHttp())
        self.assertEqual(report["status"], "needs_albert")
        self.assertIsNone(report["packet"])


class ServeurModeleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
        cls.port = cls.server.server_address[1]
        cls.patch = mock.patch.object(web, "PORT", cls.port)
        cls.patch.start()
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)
        cls.patch.stop()

    def request(self, path, payload=None):
        headers = {"Host": f"127.0.0.1:{self.port}"}
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")
        req = Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=data,
            headers=headers,
            method="POST" if data else "GET",
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_info_annonce_openweight_large(self):
        with mock.patch.dict("os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}):
            code, info = self.request("/api/info")
        self.assertEqual(code, 200)
        self.assertEqual(info["albert_model"], "openweight-large")
        self.assertFalse(info["albert_configured"])

    def test_info_reprend_albert_model_du_poste(self):
        with mock.patch.dict(
            "os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": "modele-du-poste"}
        ):
            _, info = self.request("/api/info")
        self.assertEqual(info["albert_model"], "modele-du-poste")

    def test_jeton_du_poste_suffit_a_configurer_albert(self):
        with mock.patch.dict(
            "os.environ", {"ALBERT_API_KEY": TOKEN, "ALBERT_MODEL": ""}
        ):
            _, info = self.request("/api/info")
        self.assertTrue(info["albert_configured"])
        self.assertNotIn(TOKEN, json.dumps(info))

    def test_repechage_sans_modele_utilise_openweight_large(self):
        url = "https://www.numerique.gouv.fr/article/veille-snum"
        item = {
            "title": "Un article de veille SNUM",
            "source": "DINUM",
            "publication_date_iso": "2026-11-06",
            "url": url,
            "content": "Extrait public.",
        }
        seen = []
        with (
            mock.patch.dict("os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}),
            mock.patch.dict(web.LAST_CANDIDATES, {url: item}),
            mock.patch.object(core, "albert_summary", recording_albert(seen)),
        ):
            code, body = self.request(
                "/api/summarize",
                {"url": url, "rubric": "numerique", "albert_api_key": TOKEN},
            )
        self.assertEqual(code, 200, body)
        self.assertEqual(seen, ["openweight-large"])
        self.assertNotIn(TOKEN, json.dumps(body))


if __name__ == "__main__":
    unittest.main()
