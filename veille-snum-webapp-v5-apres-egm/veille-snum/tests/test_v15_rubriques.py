"""Onze rubriques de la revue de presse (#32) : liste, consignes d'Albert, refus des autres valeurs."""

import unittest
from pathlib import Path

from test_veille_snum import good_summary
from veille_snum.core import ALBERT_PROMPT, RUBRICS, validate_summary

RACINE = Path(__file__).resolve().parents[1]
ONZE = (
    "ia",
    "administration",
    "dsi",
    "economie",
    "infrastructure",
    "securite",
    "applications",
    "droit",
    "commande",
    "rh",
    "bercy",
)


class RubriquesTests(unittest.TestCase):
    def test_onze_rubriques_dans_l_ordre_du_courriel(self):
        self.assertEqual(RUBRICS, ONZE)

    def test_consignes_d_albert_enumerent_et_definissent_chaque_rubrique(self):
        self.assertIn("rubric (" + "|".join(ONZE) + ")", ALBERT_PROMPT)
        for rubrique in ONZE:
            with self.subTest(rubrique=rubrique):
                self.assertIn(f"{rubrique} = ", ALBERT_PROMPT)
        self.assertNotIn("numerique", ALBERT_PROMPT)

    def test_ancienne_thematique_refusee_en_sortie_d_albert(self):
        with self.assertRaisesRegex(ValueError, "RUBRIQUE_INVALIDE"):
            validate_summary({**good_summary({}), "rubric": "numerique"})
        for rubrique in ONZE:
            with self.subTest(rubrique=rubrique):
                self.assertEqual(
                    validate_summary({**good_summary({}), "rubric": rubrique})[
                        "rubric"
                    ],
                    rubrique,
                )

    def test_tache_de_repechage_propose_les_onze_rubriques(self):
        texte = (
            RACINE.parents[1] / ".github/workflows/repecher-candidat.yml"
        ).read_text(encoding="utf-8")
        bloc = texte.split("options:", 1)[1].split("debut:", 1)[0]
        options = [
            ligne.strip()[2:]
            for ligne in bloc.splitlines()
            if ligne.strip().startswith("- ")
        ]
        self.assertEqual(tuple(options), ONZE)

    def test_page_et_application_locale_partagent_la_liste(self):
        page = (RACINE / "pages/selection.js").read_text(encoding="utf-8")
        locale = (RACINE / "veille_snum/app.js").read_text(encoding="utf-8")
        attendu = "[" + ", ".join(f"'{r}'" for r in ONZE) + "]"
        self.assertIn(f"const RUBRICS = {attendu};", page)
        for rubrique in ONZE:
            with self.subTest(rubrique=rubrique):
                self.assertIn(f"{rubrique}:", locale)


if __name__ == "__main__":
    unittest.main()
