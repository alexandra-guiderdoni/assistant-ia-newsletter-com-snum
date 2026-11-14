"""Périmètre des consignes d'Albert (#33) : sécurité informatique et logiciels de travail retenus."""

import unittest

from veille_snum.core import ALBERT_PROMPT


def ligne(debut):
    """Ligne des consignes qui commence par debut."""
    return next(ligne for ligne in ALBERT_PROMPT.split("\n") if ligne.startswith(debut))


class PerimetreTests(unittest.TestCase):
    def test_cyberattaques_retenues_quelle_que_soit_la_victime(self):
        retenus = ligne("relevant=true")
        for attendu in (
            "cyberattaques",
            "fuites de données",
            "vulnérabilités",
            "quelle que soit la victime",
            "entreprise comprise",
            "securite",
        ):
            with self.subTest(attendu=attendu):
                self.assertIn(attendu, retenus)

    def test_logiciels_de_travail_retenus(self):
        retenus = ligne("relevant=true")
        for attendu in (
            "systèmes d'exploitation",
            "messagerie",
            "bureautique",
            "navigateurs",
            "applications",
        ):
            with self.subTest(attendu=attendu):
                self.assertIn(attendu, retenus)

    def test_ces_cas_l_emportent_sur_les_exclusions(self):
        self.assertLess(
            ALBERT_PROMPT.index("relevant=true"), ALBERT_PROMPT.index("relevant=false")
        )
        self.assertIn("l'emportent sur les exclusions", ligne("relevant=true"))

    def test_autres_exclusions_conservees(self):
        exclus = ligne("relevant=false")
        for attendu in (
            "commerce et distribution",
            "faits divers",
            "marchés financiers",
            "produits grand public sans lien avec le travail",
            "offres d'emploi",
            "En cas de doute, relevant=false",
        ):
            with self.subTest(attendu=attendu):
                self.assertIn(attendu, exclus)
        self.assertNotIn("produits grand public hors IA", ALBERT_PROMPT)


if __name__ == "__main__":
    unittest.main()
