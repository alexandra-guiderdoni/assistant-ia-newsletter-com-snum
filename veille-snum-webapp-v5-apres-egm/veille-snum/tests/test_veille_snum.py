import datetime as dt
from unittest import TestCase, main, mock
from urllib.parse import urlsplit

from veille_snum.core import (sources, normalized_url, iso_date, parse_page, sitemap_entries,
                             packet_for, validate_summary, discover_source, collect, RUBRICS)


class FakeHttp:
    def __init__(self, publication="2026-11-06", page_kind="published"):
        self.calls = []
        self.publication = publication
        self.page_kind = page_kind

    def get(self, url, domain, max_bytes=600_000, timeout=7):
        self.calls.append(url)
        path = urlsplit(url).path
        if path == "/robots.txt":
            return url, "User-agent: *\nAllow: /\n"
        if path == "/sitemap.xml":
            return url, f"<urlset><url><loc>https://{domain}/article/veille-snum</loc><lastmod>2026-11-11</lastmod></url></urlset>"
        if path == "/":
            return url, '<html><body><a href="/article/veille-snum">Transformation numérique publique et IA</a></body></html>'
        if path == "/article/veille-snum":
            meta = (f'<meta property="article:published_time" content="{self.publication}T09:10:00+01:00">'
                    if self.page_kind == "published" else
                    f'<meta property="article:modified_time" content="{self.publication}T09:10:00+01:00">')
            paragraph = "Cette publication officielle décrit un service public numérique, son déploiement et les besoins concrets des administrations. "
            return url, f'<html><head>{meta}<meta property="og:title" content="Un article de veille SNUM et services numériques"></head><body><article><p>{paragraph * 2}</p><p>{paragraph * 2}</p></article></body></html>'
        raise AssertionError(f"URL inattendue {url}")


def good_summary(candidate):
    return {"relevant": True, "rubric": "administration", "fact": "Le service public présente une évolution de ses outils numériques.",
            "keywords": ["numérique", "service public", "administration"],
            "takeaway": "Une évolution des outils publics est décrite.", "snum_interest": "À examiner pour les services numériques du ministère."}


class ConfigurationTests(TestCase):
    def test_quatorze_sources_et_interne(self):
        items = sources()
        self.assertEqual(len(items), 14)
        self.assertEqual(sum(x["internal"] for x in items), 1)
        self.assertEqual(len({x["domain"] for x in items if not x["internal"]}), 13)
        self.assertIsNone(next(x for x in items if x["internal"])["domain"])

    def test_domaines_stricts(self):
        self.assertEqual(normalized_url("https://www.numerique.gouv.fr/a?utm_source=x#part", "numerique.gouv.fr"), "https://www.numerique.gouv.fr/a")
        for url in ("http://numerique.gouv.fr/a", "https://evil-numerique.gouv.fr/a", "https://numerique.gouv.fr.evil.test/a", "https://numerique.gouv.fr:8080/a"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                normalized_url(url, "numerique.gouv.fr")

    def test_date_stricte(self):
        for value in ("2026-11-31", "11/11/2026", "2026-1-1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                iso_date(value)


class CollecteTests(TestCase):
    def test_date_de_mise_a_jour_ne_qualifie_pas(self):
        source = next(x for x in sources() if not x["internal"])
        c, ex, status = discover_source(source, dt.date(2026, 11, 1), dt.date(2026, 11, 10), FakeHttp(page_kind="modified"))
        self.assertEqual(c, [])
        self.assertEqual(status["status"], "checked")
        self.assertTrue(any("DATE_PUBLICATION_ABSENTE" in x["reason"] for x in ex))

    def test_lastmod_du_sitemap_ne_qualifie_pas(self):
        source = next(x for x in sources() if not x["internal"])
        c, ex, _ = discover_source(source, dt.date(2026, 11, 1), dt.date(2026, 11, 10), FakeHttp(publication="2026-10-20"))
        self.assertEqual(c, [])
        self.assertTrue(any("DATE_HORS_PERIODE" in x["reason"] for x in ex))

    def test_extraction_et_sources(self):
        src = next(x for x in sources() if not x["internal"])
        candidates, excluded, state = discover_source(src, dt.date(2026, 11, 1), dt.date(2026, 11, 10), FakeHttp())
        self.assertEqual(len(candidates), 1)
        self.assertEqual(state["eligible"], 1)
        self.assertEqual(excluded, [])

    def test_paquet_compatible_v519(self):
        source = next(x for x in sources() if not x["internal"])
        client = FakeHttp()
        with mock.patch.dict("os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}):
            report = collect({"edition_date": "2026-11-11", "window_start": "2026-11-01", "window_end": "2026-11-10"},
                             client=client, summarize=good_summary)
        self.assertEqual(report["status"], "ready")
        self.assertEqual(len(report["sources"]), 14)
        self.assertEqual(len(report["packet"]["articles"]), 13)
        self.assertEqual([a["id"] for a in report["packet"]["articles"]], [f"U{i:02d}" for i in range(1, 14)])
        self.assertEqual(sum(x["essential"] for x in report["packet"]["articles"]), 3)
        self.assertTrue(any("Source interne non traitée" in x["title"] for x in report["packet"]["watch"]))
        self.assertTrue(all(a["rubric"] in RUBRICS for a in report["packet"]["articles"]))
        self.assertFalse(any("source-interne" in url for url in client.calls))

    def test_sans_albert_pas_de_faux_paquet(self):
        with mock.patch.dict("os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}):
            report = collect({"edition_date": "2026-11-11", "window_start": "2026-11-01", "window_end": "2026-11-10"}, client=FakeHttp())
        self.assertEqual(report["status"], "needs_albert")
        self.assertIsNone(report["packet"])
        self.assertEqual(len(report["candidates"]), 13)
        self.assertTrue(all("content" not in c for c in report["candidates"]))

    def test_mauvaise_sortie_modele_bloque_export(self):
        def wrong(_):
            return {"relevant": True, "rubric": "administration", "fact": "ok", "keywords": [], "takeaway": "ok", "snum_interest": "ok"}
        report = collect({"edition_date": "2026-11-11", "window_start": "2026-11-01", "window_end": "2026-11-10"},
                         client=FakeHttp(), summarize=wrong)
        self.assertEqual(report["status"], "incomplete")
        self.assertIsNone(report["packet"])

    def test_paquet_vide_autorise_sous_recherche_executee(self):
        result = packet_for(dt.date(2026, 11, 11), dt.date(2026, 11, 1), dt.date(2026, 11, 10), [], [])
        self.assertEqual(result["articles"], [])
        self.assertEqual(len(result["watch"]), len(RUBRICS) + 1)  # une alerte par rubrique vide, plus « Collecte limitée »


class ExhaustionTests(TestCase):
    def test_aucun_site_accessible_ne_produit_pas_de_fausse_collecte(self):
        class OfflineClient:
            def get(self, *args, **kwargs):
                raise OSError('réseau non disponible')
        report = collect({"edition_date": "2026-11-11", "window_start": "2026-11-01", "window_end": "2026-11-10"},
                         client=OfflineClient(), summarize=good_summary)
        self.assertEqual(report["status"], "unavailable")
        self.assertIsNone(report["packet"])
        self.assertEqual(sum(s["status"] == "error" for s in report["sources"]), 13)

    def test_rejet_du_paquet_corrrompu(self):
        from veille_snum.core import validate_packet_v519
        result = packet_for(dt.date(2026, 11, 11), dt.date(2026, 11, 1), dt.date(2026, 11, 10), [], [])
        self.assertTrue(validate_packet_v519(result))
        result["watch"] = "pas une liste"
        with self.assertRaises(ValueError):
            validate_packet_v519(result)

class SecretTests(TestCase):
    def test_jeton_saisi_jamais_dans_le_rapport(self):
        token = "TEST-SECRET-TOKEN-DO-NOT-EXPOSE"
        report = collect({"edition_date": "2026-11-11", "window_start": "2026-11-01", "window_end": "2026-11-10",
                          "albert_api_key": token, "albert_model": "modele-test"}, client=FakeHttp(), summarize=good_summary)
        import json
        self.assertNotIn(token, json.dumps(report))
        self.assertEqual(report["status"], "ready")


if __name__ == "__main__":
    main()
