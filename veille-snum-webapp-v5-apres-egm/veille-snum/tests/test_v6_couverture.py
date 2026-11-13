"""Couverture réelle : grandes pages d'accueil, pages récentes d'abord, budget Albert distinct."""

import datetime as dt
from unittest import TestCase, main, mock
from urllib.parse import urlsplit

from veille_snum import core
from veille_snum.core import collect, discover_source, parse_page, sources

START, END = dt.date(2026, 11, 3), dt.date(2026, 11, 10)
PARAGRAPH = (
    "Cette publication officielle décrit un service public numérique, son déploiement "
    "et les besoins concrets des administrations. "
)


def article(day):
    return (
        f'<html><head><meta property="article:published_time" content="{day}T09:00:00+01:00">'
        '<meta property="og:title" content="Un article de veille SNUM et services numériques"></head>'
        f"<body><article><p>{PARAGRAPH * 2}</p><p>{PARAGRAPH * 2}</p></article></body></html>"
    )


class SiteHttp:
    """Faux site qui respecte max_bytes comme le vrai client."""

    def __init__(
        self, homepage="", sitemap="", children=None, articles=None, clock=None
    ):
        self.homepage, self.sitemap = homepage, sitemap
        self.children = children or {}
        self.articles = articles or {}
        self.clock = clock
        self.calls = []

    def get(self, url, domain, max_bytes=600_000, timeout=7):
        self.calls.append(url)
        path = urlsplit(url).path
        if path == "/robots.txt":
            body = "User-agent: *\nAllow: /\n"
        elif path == "/":
            body = self.homepage or "<html><body></body></html>"
        elif path == "/sitemap.xml":
            body = self.sitemap or "<urlset></urlset>"
        elif path in self.children:
            body = self.children[path]
        elif path in self.articles:
            body = article(self.articles[path])
            if self.clock is not None:
                self.clock[0] += 185
        else:
            raise AssertionError(f"URL inattendue {url}")
        if len(body.encode()) > max_bytes:
            raise ValueError("Réponse trop volumineuse")
        return url, body


def source():
    return next(x for x in sources() if x["id"] == "next")


def urlset(entries):
    rows = "".join(
        f"<url><loc>https://next.ink{path}</loc><lastmod>{day}</lastmod></url>"
        for path, day in entries
    )
    return f"<urlset>{rows}</urlset>"


class CouvertureTests(TestCase):
    def test_page_accueil_volumineuse_acceptee(self):
        homepage = (
            '<html><body><a href="/2026/11/08/actu">Actualité numérique publique</a>'
            + "<p>"
            + "x" * 1_200_000
            + "</p></body></html>"
        )
        http = SiteHttp(homepage=homepage, articles={"/2026/11/08/actu": "2026-11-08"})
        candidates, _, state = discover_source(source(), START, END, http)
        self.assertNotEqual(state["status"], "error", state["notes"])
        self.assertEqual(len(candidates), 1)

    def test_pages_recentes_visitees_avant_les_anciennes(self):
        old = [(f"/article/numerique-public-{i}", "2025-01-15") for i in range(30)]
        recent = [
            ("/article/recent-a", "2026-11-08"),
            ("/article/recent-b", "2026-11-06"),
        ]
        http = SiteHttp(
            sitemap=urlset(old + recent), articles={path: day for path, day in recent}
        )
        candidates, _, _ = discover_source(source(), START, END, http)
        self.assertEqual(
            {urlsplit(c["url"]).path for c in candidates},
            {"/article/recent-a", "/article/recent-b"},
        )
        self.assertGreaterEqual(core.MAX_ARTICLES_PER_SITE, 15)

    def test_sitemaps_enfants_les_plus_recents_d_abord(self):
        index = (
            "<sitemapindex>"
            + "".join(
                f"<sitemap><loc>https://next.ink/sitemap-{n}.xml</loc><lastmod>{day}</lastmod></sitemap>"
                for n, day in (
                    (1, "2024-01-01"),
                    (2, "2024-06-01"),
                    (3, "2025-01-01"),
                    (4, "2026-11-09"),
                )
            )
            + "</sitemapindex>"
        )
        children = {f"/sitemap-{n}.xml": "<urlset></urlset>" for n in (1, 2, 3)}
        children["/sitemap-4.xml"] = urlset([("/article/recent-a", "2026-11-08")])
        http = SiteHttp(
            sitemap=index,
            children=children,
            articles={"/article/recent-a": "2026-11-08"},
        )
        candidates, _, _ = discover_source(source(), START, END, http)
        self.assertIn("https://next.ink/sitemap-4.xml", http.calls)
        self.assertEqual(len(candidates), 1)

    def test_albert_dispose_de_son_propre_budget(self):
        clock = [1000.0]
        http = SiteHttp(
            sitemap=urlset([("/article/recent-a", "2026-11-08")]),
            articles={"/article/recent-a": "2026-11-08"},
            clock=clock,
        )
        only_next = [x for x in sources() if x["id"] in ("next", "source-interne")]
        summary = {
            "relevant": True,
            "rubric": "numerique",
            "fact": "Le service public présente une évolution de ses outils numériques.",
            "keywords": ["numérique", "service public", "administration"],
            "takeaway": "Une évolution des outils publics est décrite.",
            "snum_interest": "À examiner pour les services numériques du ministère.",
        }
        with (
            mock.patch.object(core.time, "monotonic", lambda: clock[0]),
            mock.patch.object(core, "sources", lambda: only_next),
        ):
            report = collect(
                {
                    "edition_date": "2026-11-11",
                    "window_start": "2026-11-03",
                    "window_end": "2026-11-10",
                },
                client=http,
                summarize=lambda item: summary,
            )
        self.assertFalse(
            any(e.get("reason") == "BUDGET_DUREE_ALBERT" for e in report["excluded"])
        )
        self.assertIsNotNone(report["packet"])
        self.assertEqual(len(report["packet"]["articles"]), 1)



def body(head_date_html):
    return (f"<html><head><title>Un article de veille SNUM et services numériques</title></head><body>"
            f"{head_date_html}<article><p>{PARAGRAPH * 2}</p><p>{PARAGRAPH * 2}</p></article></body></html>")


class DateVisibleTests(TestCase):
    def page_date(self, raw):
        return parse_page(raw).publication_date("https://next.ink/a", "https://next.ink/a")

    def test_publie_le_unique_dans_la_page(self):
        raw = body("<h1>Titre</h1><p>Contenu</p><span>Publié le vendredi 6 novembre 2026 | DINUM</span>")
        self.assertEqual(self.page_date(raw), "2026-11-06")

    def test_date_juste_sous_le_titre(self):
        raw = body("<h1><span>Sanctions</span></h1><p class='ctn-gen-auteur'>09 novembre 2026</p>")
        self.assertEqual(self.page_date(raw), "2026-11-09")

    def test_plusieurs_publie_le_sans_date_sous_le_titre_rejete(self):
        cards = "".join(f"<div>Publié le {d} novembre 2026</div>" for d in (2, 5, 8))
        raw = body("<h1>Titre</h1>" + "<p>" + "Texte d'introduction assez long. " * 6 + "</p>" + cards)
        self.assertIsNone(self.page_date(raw))

    def test_date_lointaine_du_titre_ignoree(self):
        raw = body("<h1>Titre</h1><p>" + "Texte sans date. " * 20 + "</p><p>Le 3 novembre 2026, un événement.</p>")
        self.assertIsNone(self.page_date(raw))

    def test_metadonnee_prioritaire_sur_le_texte(self):
        raw = body("<h1>Titre</h1><p>09 novembre 2026</p>").replace(
            "<head>", '<head><meta property="article:published_time" content="2026-11-04T08:00:00+01:00">')
        self.assertEqual(self.page_date(raw), "2026-11-04")


class LienCourtTests(TestCase):
    def test_lien_court_wordpress_n_est_pas_une_autre_page(self):
        ld = ('<script type="application/ld+json">{"@graph":[{"@type":"Article",'
              '"@id":"https://presse.economie.gouv.fr/?p=186781#article",'
              '"mainEntityOfPage":{"@id":"https://presse.economie.gouv.fr/?p=186781"},'
              '"datePublished":"2026-11-05T10:00:00+00:00"},{"@type":"WebPage",'
              '"@id":"https://presse.economie.gouv.fr/?p=186781","url":"https://presse.economie.gouv.fr/?p=186781"}]}'
              "</script>")
        page = ('<html><head><link rel="canonical" href="https://presse.economie.gouv.fr/?p=186781">' + ld +
                '<meta property="article:published_time" content="2026-11-05T10:00:00+01:00">'
                '<meta property="og:title" content="Rencontres des centres de données à Bercy"></head>'
                f"<body><article><p>{PARAGRAPH * 2}</p><p>{PARAGRAPH * 2}</p></article></body></html>")
        src = next(x for x in sources() if x["id"] == "presse-economie")

        class Http(SiteHttp):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if urlsplit(url).path == "/ip-rencontres":
                    return url, page
                return super().get(url, domain, max_bytes, timeout)

        http = Http(homepage='<html><body><a href="/ip-rencontres">Centres de données numériques</a></body></html>')
        candidates, excluded, _ = discover_source(src, START, END, http)
        self.assertEqual([e["reason"] for e in excluded], [])
        self.assertEqual(len(candidates), 1)
        self.assertEqual(urlsplit(candidates[0]["url"]).path, "/ip-rencontres")


class TitreTests(TestCase):
    def test_titre_h1_si_og_title_est_le_nom_du_site(self):
        page = ('<html><head><meta property="og:title" content="numerique.gouv.fr">'
                '<title>numerique.gouv.fr</title></head><body>'
                "<h1>Achats publics : un guide pratique pour l'IA</h1>"
                "<span>Publié le vendredi 6 novembre 2026</span>"
                f"<article><p>{PARAGRAPH * 2}</p><p>{PARAGRAPH * 2}</p></article></body></html>")
        src = next(x for x in sources() if x["id"] == "numerique")

        class Http(SiteHttp):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if urlsplit(url).path == "/actualites/guide-ia/":
                    return url, page
                return super().get(url, domain, max_bytes, timeout)

        http = Http(homepage='<html><body><a href="/actualites/guide-ia/">Guide IA</a></body></html>')
        candidates, _, _ = discover_source(src, START, END, http)
        self.assertEqual(candidates[0]["title"], "Achats publics : un guide pratique pour l'IA")


CHALLENGE = ("<html><head><meta http-equiv='Content-Security-Policy' content=\"default-src 'self'\"></head>"
             "<body><script>window.location.href='/redirect_ABC/';</script>"
             "<noscript>This website requires JS enabled and cookies</noscript></body></html>")


class AntiRobotTests(TestCase):
    def test_refus_403_signale_comme_protection(self):
        from urllib.error import HTTPError

        class Http(SiteHttp):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                raise HTTPError(url, 403, "Forbidden", {}, None)

        _, _, state = discover_source(source(), START, END, Http())
        self.assertEqual(state["status"], "blocked")
        self.assertIn("anti-robot", " ".join(state["notes"]))

    def test_page_accueil_de_verification_javascript(self):
        _, _, state = discover_source(source(), START, END, SiteHttp(homepage=CHALLENGE))
        self.assertEqual(state["status"], "blocked")
        self.assertIn("anti-robot", " ".join(state["notes"]))

    def test_articles_tous_remplaces_par_une_verification(self):
        class Http(SiteHttp):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if urlsplit(url).path.startswith("/2026/"):
                    return url, CHALLENGE
                return super().get(url, domain, max_bytes, timeout)

        homepage = "".join(f'<a href="/2026/11/0{d}/actu">Actualité numérique {d}</a>' for d in range(4, 8))
        homepage = f"<html><body><p>{PARAGRAPH * 3}</p>{homepage}</body></html>"
        candidates, excluded, state = discover_source(source(), START, END, Http(homepage=homepage))
        self.assertEqual(candidates, [])
        self.assertEqual({e["reason"] for e in excluded}, {"PAGE_VERIFICATION_OU_CAPTCHA"})
        self.assertEqual(state["status"], "blocked")


class ClientChallengeTests(TestCase):
    def test_page_client_challenge_type_le_monde(self):
        from veille_snum.core import is_bot_wall
        raw = ("<html><head><title>Client Challenge</title><script src='/x.js'></script></head><body>"
               "<p>Client Challenge</p><p>A required part of this site couldn’t load. This may be due to a "
               "browser extension, network issues, or browser settings. Please check your connection, disable "
               "any ad blockers, or try using a different browser.</p></body></html>")
        self.assertTrue(is_bot_wall(raw))
        self.assertFalse(is_bot_wall(article("2026-11-08")))


class NotesTests(TestCase):
    def test_notes_identiques_regroupees(self):
        entries = [(f"/article/ancien-{i}", "2025-01-15") for i in range(400)]
        _, _, state = discover_source(source(), START, END, SiteHttp(sitemap=urlset(entries)))
        skipped = [n for n in state["notes"] if "plafond de liens sitemap" in n]
        self.assertEqual(len(skipped), 1)
        self.assertIn("(×100)", skipped[0])
        self.assertEqual(state["sitemap_skipped"], 100)

if __name__ == "__main__":
    main()
