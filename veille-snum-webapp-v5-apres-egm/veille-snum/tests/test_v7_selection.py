"""Sélection éditoriale : décocher, reclasser, repêcher, puis reconstruire un paquet V519 validé."""

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.test_v6_albert import PAYLOAD, SUMMARY, eight_articles, only_next
from veille_snum import core, web
from veille_snum.core import collect, rebuild_packet, summarize_selected

SOURCES = [
    {
        "id": "next",
        "label": "Next",
        "status": "partial",
        "opened": 15,
        "not_visited": 3,
    },
    {
        "id": "le-monde",
        "label": "Le Monde",
        "status": "blocked",
        "opened": 0,
        "not_visited": 0,
    },
]


def article(i, day, rubric="numerique"):
    return {
        "title": f"Un article de veille numéro {i}",
        "source": "Next",
        "publication_date_iso": day,
        "url": f"https://next.ink/article/{i}",
        "rubric": rubric,
        **{k: SUMMARY[k] for k in ("fact", "keywords", "takeaway", "snum_interest")},
    }


def selection(**changes):
    base = {
        "edition_date": "2026-11-11",
        "window_start": "2026-11-03",
        "window_end": "2026-11-10",
        "articles": [
            article(1, "2026-11-04"),
            article(2, "2026-11-09", "bercy"),
            article(3, "2026-11-06"),
        ],
        "sources": SOURCES,
    }
    base.update(changes)
    return base


class ReconstructionTests(unittest.TestCase):
    def test_paquet_renumerote_trie_et_valide(self):
        packet = rebuild_packet(selection())
        self.assertEqual(packet["schema_version"], "SNUM_PAQUET_RENDU_V519")
        self.assertEqual([a["id"] for a in packet["articles"]], ["U01", "U02", "U03"])
        self.assertEqual(
            [a["publication_date_iso"] for a in packet["articles"]],
            ["2026-11-09", "2026-11-06", "2026-11-04"],
        )
        self.assertEqual(sum(a["essential"] for a in packet["articles"]), 3)
        self.assertIn(
            "Sources protégées contre les robots", [w["title"] for w in packet["watch"]]
        )

    def test_article_decoche_et_rubrique_changee(self):
        chosen = [article(2, "2026-11-09", "commande")]
        packet = rebuild_packet(selection(articles=chosen))
        self.assertEqual(len(packet["articles"]), 1)
        self.assertEqual(packet["articles"][0]["rubric"], "commande")
        self.assertFalse(packet["articles"][0]["essential"])

    def test_refus_des_articles_non_conformes(self):
        bad = [
            {**article(1, "2026-11-04"), "url": "https://example.com/hors-liste"},
            {**article(1, "2026-11-04"), "url": "http://next.ink/a"},
            {**article(1, "2026-10-01")},
            {**article(1, "2026-11-04"), "rubric": "economie"},
            {**article(1, "2026-11-04"), "fact": "mot " * 30},
            {k: v for k, v in article(1, "2026-11-04").items() if k != "title"},
        ]
        for item in bad:
            with self.subTest(item=item.get("url")), self.assertRaises(ValueError):
                rebuild_packet(selection(articles=[item]))

    def test_paquet_vide_admis(self):
        packet = rebuild_packet(selection(articles=[]))
        self.assertEqual(packet["articles"], [])


class RepechageTests(unittest.TestCase):
    def test_collecte_garde_le_texte_des_candidats_cote_serveur(self):
        cache = {}
        with mock.patch.object(core, "sources", only_next):
            report = collect(
                PAYLOAD,
                client=eight_articles(),
                summarize=lambda item: {"relevant": False},
                cache=cache,
            )
        self.assertEqual(len(cache), 8)
        self.assertTrue(all("content" in item for item in cache.values()))
        self.assertTrue(all("content" not in c for c in report["candidates"]))

    def test_resume_force_dans_la_thematique_choisie(self):
        cache = {
            "https://next.ink/a": {
                "title": "Un article repêché par l'éditeur",
                "source": "Next",
                "publication_date_iso": "2026-11-05",
                "url": "https://next.ink/a",
                "content": "Texte de l'article.",
            }
        }
        seen = {}

        def answer(item, forced_rubric=None):
            seen["rubric"] = forced_rubric
            return {**SUMMARY, "relevant": False, "rubric": "ia"}

        result = summarize_selected(
            "https://next.ink/a", "bercy", cache, summarize=answer
        )
        self.assertEqual(seen["rubric"], "bercy")
        self.assertEqual(result["rubric"], "bercy")
        self.assertEqual(result["url"], "https://next.ink/a")
        self.assertEqual(result["fact"], SUMMARY["fact"])

    def test_repechage_inconnu_refuse(self):
        with self.assertRaises(ValueError):
            summarize_selected(
                "https://next.ink/absent",
                "ia",
                {},
                summarize=lambda item, forced_rubric=None: SUMMARY,
            )
        with self.assertRaises(ValueError):
            summarize_selected(
                "https://next.ink/a",
                "economie",
                {"https://next.ink/a": {}},
                summarize=None,
            )


class ReglagesTests(unittest.TestCase):
    def test_budget_albert_suffisant_pour_deux_appels(self):
        self.assertGreaterEqual(core.MAX_ALBERT_SECONDS, 360)

    def test_anglais_avec_peu_de_mots_outils(self):
        english = {
            **SUMMARY,
            "fact": "Anthropic's Claude Fable 5.2 redirects risky queries to weaker models, enabling jailbreaks.",
            "takeaway": "Safety routing remains easy to bypass.",
            "snum_interest": "Monitor model safety claims.",
        }
        with self.assertRaises(ValueError):
            core.validate_summary(english)
        french = {
            **SUMMARY,
            "fact": "Anthropic publie Claude Fable 5.2 ; ses garde-fous restent contournables selon 01net.",
        }
        self.assertIsNotNone(core.validate_summary(french))


class LangueParChampTests(unittest.TestCase):
    def test_fait_anglais_parmi_des_champs_francais_rejete(self):
        mixed = {**SUMMARY, "fact": "The CNIL will attend the Salon des maires to advise local officials on data protection.",
                 "takeaway": "Le succès passe d’abord par la gouvernance, pas seulement par le choix des outils.",
                 "snum_interest": "Partage d’expérience pour guider les collectivités dans leurs projets de migration."}
        with self.assertRaises(ValueError):
            core.validate_summary(mixed)

    def test_reconstruction_refuse_un_fait_anglais(self):
        item = {**article(1, "2026-11-04"), "fact": "The CNIL will attend the Salon des maires to advise local officials on data protection."}
        with self.assertRaises(ValueError):
            rebuild_packet(selection(articles=[item]))


class SelectionHttpTests(unittest.TestCase):
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

    def post(self, path, payload):
        req = Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=json.dumps(payload).encode(),
            method="POST",
            headers={
                "Host": f"127.0.0.1:{self.port}",
                "Content-Type": "application/json",
                "Origin": f"http://127.0.0.1:{self.port}",
            },
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            return exc.code, json.loads(exc.read() or b"{}")

    def test_point_d_acces_paquet(self):
        code, body = self.post("/api/packet", selection())
        self.assertEqual(code, 200)
        self.assertEqual(len(body["packet"]["articles"]), 3)

    def test_point_d_acces_paquet_refuse_un_article_invalide(self):
        code, body = self.post(
            "/api/packet",
            selection(
                articles=[{**article(1, "2026-11-04"), "url": "https://example.com/x"}]
            ),
        )
        self.assertEqual(code, 400)
        self.assertIn("error", body)

    def test_repechage_sans_collecte_prealable(self):
        with mock.patch.dict(web.LAST_CANDIDATES, {}, clear=True):
            code, _ = self.post(
                "/api/summarize", {"url": "https://next.ink/a", "rubric": "ia"}
            )
        self.assertEqual(code, 400)

    def test_page_propose_la_selection(self):
        root = Path(web.__file__).parent
        script = (root / "app.js").read_text(encoding="utf-8")
        page = (root / "index.html").read_text(encoding="utf-8")
        for expected in ("/api/packet", "/api/summarize", "Mettre à jour le paquet"):
            self.assertIn(expected, script + page)
        self.assertIn('id="rejected-list"', page)



class ConfortTests(unittest.TestCase):
    def setUp(self):
        self.script = (Path(web.__file__).parent / "app.js").read_text(encoding="utf-8")

    def test_repechage_des_candidats_non_resumes_ou_en_echec(self):
        for reason in ("HORS_THEMATIQUE", "BUDGET_DUREE_ALBERT"):
            self.assertIn(reason, self.script)
        self.assertIn("result.errors", self.script)
        for label in ("hors thématique", "non résumé faute de temps", "échec Albert"):
            self.assertIn(label, self.script)

    def test_resultat_conserve_dans_l_onglet_sans_cle(self):
        self.assertIn("sessionStorage", self.script)
        saved = self.script[self.script.index("function saveResult"):]
        saved = saved[:saved.index("\n}") + 2]
        self.assertNotIn("albert", saved.lower())
        self.assertIn("not_visited_urls", saved)

if __name__ == "__main__":
    unittest.main()


class TiretCadratinTests(unittest.TestCase):
    def test_aucun_tiret_cadratin_dans_le_prototype(self):
        root = Path(web.__file__).parents[1]
        for path in [*root.glob("veille_snum/*"), *root.glob("*.md"), *root.glob("docs/**/*.md")]:
            # sources.json est figé octet pour octet (test_v4) : son libellé est normalisé au chargement.
            if path.is_file() and path.suffix in {".py", ".js", ".html", ".json", ".md"} and path.name != "sources.json":
                with self.subTest(path=path.name):
                    self.assertNotIn("\u2014", path.read_text(encoding="utf-8"))

    def test_libelles_des_sources_sans_tiret_cadratin(self):
        self.assertFalse(any("\u2014" in s["label"] for s in core.sources()))
        self.assertIn("Source métier interne, configuration privée requise", [s["label"] for s in core.sources()])

    def test_resumes_albert_sans_tiret_cadratin(self):
        dashed = {**SUMMARY, "fact": "Le service public \u2014 en ligne \u2014 présente une évolution de ses outils.",
                  "keywords": ["numérique\u2014public", "service public", "administration"]}
        accepted = core.validate_summary(dashed)
        self.assertNotIn("\u2014", json.dumps(accepted, ensure_ascii=False))
        self.assertEqual(accepted["fact"], "Le service public, en ligne, présente une évolution de ses outils.")

    def test_titres_sans_tiret_cadratin(self):
        self.assertEqual(core.no_em_dash("Rencontres \u2014 2nde édition"), "Rencontres, 2nde édition")
        self.assertEqual(core.no_em_dash("A\u2014B"), "A-B")

    def test_consigne_interdit_le_tiret_cadratin(self):
        self.assertIn("tiret cadratin", core.ALBERT_PROMPT)
