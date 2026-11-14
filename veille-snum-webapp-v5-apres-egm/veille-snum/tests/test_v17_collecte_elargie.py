"""Collecte élargie : consigne d'Albert plus inclusive, 40 pages par source, budget partagé entre les sources."""

import unittest
from unittest import mock

from veille_snum import core


def ligne(debut):
    """Ligne des consignes d'Albert qui commence par debut."""
    return next(
        ligne for ligne in core.ALBERT_PROMPT.split("\n") if ligne.startswith(debut)
    )


class ConsigneTests(unittest.TestCase):
    def test_cas_manques_retenus(self):
        retenus = ligne("relevant=true")
        for attendu in (
            "agents publics",
            "rémunération",
            "déontologie",
            "rubrique rh",
            "cybercriminalité",
            "arrestations",
            "intelligence artificielle et du numérique",
            "géopolitiques",
            "rubriques ia et economie",
        ):
            with self.subTest(attendu=attendu):
                self.assertIn(attendu, retenus)
        self.assertIn("l'emportent sur les exclusions", retenus)

    def test_en_cas_de_doute_garder(self):
        self.assertIn("En cas de doute, relevant=true", ligne("relevant=false"))
        self.assertNotIn("En cas de doute, relevant=false", core.ALBERT_PROMPT)


class Horloge:
    def __init__(self):
        self.t = 0.0


class ReseauLent:
    """Source lente : 40 articles en page d'accueil, 30 s chacun ; tout le reste répond en 1 s."""

    def __init__(self, horloge, lente):
        self.horloge, self.lente = horloge, lente
        self.departs, self.domaines = [], []

    def get(self, url, domain, max_bytes=600_000, timeout=7, deadline=None):
        self.departs.append(self.horloge.t)
        self.domaines.append(domain)
        article = "/actualites/article-" in url
        self.horloge.t += 30.0 if (domain == self.lente and article) else 1.0
        if url.endswith("/robots.txt"):
            return url, "User-agent: *\nAllow: /\n"
        if url.endswith(".xml"):
            return url, "<urlset></urlset>"
        if domain == self.lente and not article:
            liens = "".join(
                f'<a href="https://{domain}/actualites/article-{n}">Actualité {n}</a>'
                for n in range(40)
            )
            return url, f"<html><body>{liens}</body></html>"
        return url, "<html><body></body></html>"


class BudgetTests(unittest.TestCase):
    def test_quarante_pages_par_source(self):
        self.assertEqual(core.MAX_ARTICLES_PER_SITE, 40)

    def test_une_source_lente_ne_prive_pas_les_dernieres(self):
        publiques = [s for s in core.sources() if not s["internal"]]
        horloge = Horloge()
        reseau = ReseauLent(horloge, publiques[0]["domain"])
        with mock.patch.object(core.time, "monotonic", side_effect=lambda: horloge.t):
            rapport = core.collect(
                {
                    "edition_date": "2026-11-11",
                    "window_start": "2026-11-01",
                    "window_end": "2026-11-10",
                },
                client=reseau,
                summarize=lambda _: None,
            )
        etats = {s["id"]: s["status"] for s in rapport["sources"]}
        derniere = publiques[-1]
        self.assertNotEqual(etats[derniere["id"]], "skipped_budget")
        self.assertIn(derniere["domain"], reseau.domaines)
        self.assertLess(max(reseau.departs), core.MAX_RUN_SECONDS)


if __name__ == "__main__":
    unittest.main()
