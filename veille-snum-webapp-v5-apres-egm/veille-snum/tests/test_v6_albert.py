"""Albert : appels parallèles, seconde tentative, périmètre SNUM et alertes exactes."""

import datetime as dt
import threading
import time
from unittest import TestCase, main, mock

from tests.test_v6_couverture import SiteHttp, urlset
from veille_snum import core
from veille_snum.core import collect, packet_for, sources

PAYLOAD = {
    "edition_date": "2026-11-11",
    "window_start": "2026-11-03",
    "window_end": "2026-11-10",
}
DAYS = [f"2026-11-0{d}" for d in range(3, 10)] + ["2026-11-10"]
SUMMARY = {
    "relevant": True,
    "rubric": "administration",
    "fact": "Le service public présente une évolution de ses outils numériques.",
    "keywords": ["numérique", "service public", "administration"],
    "takeaway": "Une évolution des outils publics est décrite.",
    "snum_interest": "À examiner pour les services numériques du ministère.",
}


def eight_articles():
    paths = [(f"/article/actu-{i}", day) for i, day in enumerate(DAYS)]
    return SiteHttp(sitemap=urlset(paths), articles=dict(paths))


def only_next():
    return [x for x in sources() if x["id"] in ("next", "source-interne")]


class ParallelismeTests(TestCase):
    def test_appels_albert_en_parallele(self):
        active, peak, lock = [0], [0], threading.Lock()

        def slow(item):
            with lock:
                active[0] += 1
                peak[0] = max(peak[0], active[0])
            time.sleep(0.15)
            with lock:
                active[0] -= 1
            return SUMMARY

        with mock.patch.object(core, "sources", only_next):
            began = time.monotonic()
            report = collect(PAYLOAD, client=eight_articles(), summarize=slow)
            elapsed = time.monotonic() - began
        self.assertEqual(len(report["packet"]["articles"]), 8)
        self.assertGreaterEqual(peak[0], 2)
        self.assertLess(elapsed, 8 * 0.15)
        self.assertEqual(
            [a["publication_date_iso"] for a in report["packet"]["articles"]],
            sorted(DAYS, reverse=True),
        )


class SecondeTentativeTests(TestCase):
    def test_reponse_invalide_puis_valide(self):
        calls = {}

        def flaky(item, feedback=None):
            calls[item["url"]] = calls.get(item["url"], 0) + 1
            if calls[item["url"]] == 1:
                return {**SUMMARY, "fact": "mot " * 40}
            return SUMMARY

        with mock.patch.object(core, "sources", only_next):
            report = collect(PAYLOAD, client=eight_articles(), summarize=flaky)
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["packet"]["articles"]), 8)
        self.assertTrue(all(n == 2 for n in calls.values()))

    def test_delai_depasse_puis_reussite(self):
        calls = {}

        def slow_once(item, feedback=None):
            calls[item["url"]] = calls.get(item["url"], 0) + 1
            if calls[item["url"]] == 1:
                raise TimeoutError("timed out")
            return SUMMARY

        with mock.patch.object(core, "sources", only_next):
            report = collect(PAYLOAD, client=eight_articles(), summarize=slow_once)
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["packet"]["articles"]), 8)

    def test_deux_echecs_restent_signales(self):
        def broken(item, feedback=None):
            return {"relevant": "oui"}

        with mock.patch.object(core, "sources", only_next):
            report = collect(PAYLOAD, client=eight_articles(), summarize=broken)
        self.assertEqual(len(report["errors"]), 8)
        self.assertIsNone(report["packet"])

    def test_motif_du_rejet_transmis_a_la_seconde_tentative(self):
        feedbacks = []

        def flaky(item, feedback=None):
            feedbacks.append(feedback)
            return SUMMARY if feedback else {**SUMMARY, "rubric": "culture"}

        with mock.patch.object(core, "sources", only_next):
            collect(PAYLOAD, client=eight_articles(), summarize=flaky)
        self.assertIn("RUBRIQUE_INVALIDE", " ".join(f for f in feedbacks if f))


class PerimetreTests(TestCase):
    def test_consigne_decrit_le_perimetre_et_les_exclusions(self):
        prompt = core.ALBERT_PROMPT.lower()
        for expected in (
            "service du numérique",
            "fonction publique",
            "commande publique",
            "commerce",
            "marchés financiers",
            "emploi privé",
            "relevant=false",
        ):
            self.assertIn(expected, prompt)


class AlertesTests(TestCase):
    def state(self, sid, status):
        label = next(x["label"] for x in sources() if x["id"] == sid)
        return {"id": sid, "label": label, "status": status, "not_visited": 0, "opened": 15 if status == "partial" else 0}

    def packet(self, states):
        articles = [
            {
                "title": "Un article de veille SNUM",
                "source": "Next",
                "publication_date_iso": "2026-11-05",
                "url": "https://next.ink/a",
                **{k: v for k, v in SUMMARY.items() if k != "relevant"},
            }
        ]
        return packet_for(
            dt.date(2026, 11, 11),
            dt.date(2026, 11, 3),
            dt.date(2026, 11, 10),
            articles,
            states,
        )

    def test_sources_partielles_non_declarees_non_couvertes(self):
        watch = self.packet(
            [self.state("next", "partial"), self.state("01net", "partial")]
        )["watch"]
        self.assertFalse(
            any(
                "Next" in w["summary"] or "01net" in w["summary"]
                for w in watch
                if w["title"] == "Sources non couvertes"
            )
        )

    def test_sources_protegees_et_interne_signalees_a_part(self):
        watch = self.packet(
            [
                self.state("le-monde", "blocked"),
                self.state("source-interne", "skipped_internal"),
                self.state("cnil", "error"),
            ]
        )["watch"]
        titles = {w["title"]: w["summary"] for w in watch}
        self.assertIn("Le Monde", titles["Sources protégées contre les robots"])
        self.assertIn("CNIL", titles["Sources non couvertes"])
        self.assertNotIn(
            "Source métier interne", titles.get("Sources non couvertes", "")
        )



class LimitationDebitTests(TestCase):
    def http_error(self, code, retry_after=None):
        from email.message import Message
        from urllib.error import HTTPError
        headers = Message()
        if retry_after is not None:
            headers["Retry-After"] = str(retry_after)
        return HTTPError("https://albert.api.etalab.gouv.fr/v1/chat/completions", code, "x", headers, None)

    def test_code_http_consigne_sans_secret(self):
        def refused(item, feedback=None):
            raise self.http_error(401)

        with mock.patch.object(core, "sources", only_next):
            report = collect(PAYLOAD, client=eight_articles(), summarize=refused)
        self.assertEqual({e["reason"] for e in report["errors"]}, {"Albert : HTTP 401"})

    def test_attente_puis_reprise_apres_429(self):
        calls, waits = {}, []

        def limited(item, feedback=None):
            calls[item["url"]] = calls.get(item["url"], 0) + 1
            if calls[item["url"]] <= 2:
                raise self.http_error(429, retry_after=1)
            return SUMMARY

        with mock.patch.object(core, "sources", only_next), \
                mock.patch.object(core.time, "sleep", lambda s: waits.append(s)):
            report = collect(PAYLOAD, client=eight_articles(), summarize=limited)
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["packet"]["articles"]), 8)
        self.assertTrue(waits and all(w >= 1 for w in waits))

    def test_deux_appels_simultanes_au_plus(self):
        self.assertLessEqual(core.ALBERT_WORKERS, 2)

    def test_consigne_classe_les_annonces_ia_en_ia(self):
        prompt = core.ALBERT_PROMPT.lower()
        self.assertIn("annonces de modèles", prompt)
        self.assertIn("relèvent de ia", prompt)


ENGLISH_SUMMARY = {**SUMMARY,
           "fact": "The CNIL will attend the Salon des maires 2026 to advise local officials on data protection.",
           "takeaway": "Public agents need guidance on data protection and AI.",
           "snum_interest": "Supports the mission on digital transformation and data governance."}


class LangueTests(TestCase):

    def test_resume_en_anglais_rejete(self):
        with self.assertRaises(ValueError) as ctx:
            core.validate_summary(ENGLISH_SUMMARY)
        self.assertIn("LANGUE", str(ctx.exception))

    def test_resume_francais_accepte_meme_avec_noms_anglais(self):
        french = {**SUMMARY, "fact": "OpenAI publie GPT-6 et Google lance Gemini 4 for Workspace pour les entreprises."}
        self.assertIsNotNone(core.validate_summary(french))

    def test_anglais_puis_francais_apres_seconde_tentative(self):
        def answer(item, feedback=None):
            return SUMMARY if feedback else ENGLISH_SUMMARY

        with mock.patch.object(core, "sources", only_next):
            report = collect(PAYLOAD, client=eight_articles(), summarize=answer)
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["packet"]["articles"]), 8)

    def test_consigne_impose_le_francais(self):
        self.assertIn("en français", core.ALBERT_PROMPT)

if __name__ == "__main__":
    main()
