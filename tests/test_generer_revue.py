from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

import generer_revue as generator


def event(number: int, rubric: str = "NUMERIQUE") -> dict:
    return {
        "id": f"E{number:02d}",
        "rubrique": rubric,
        "titre": f"Événement technique {number}",
        "fait": "Cette phrase courte décrit un fait vérifié.",
        "mots_cles": ["service public", "numérique", f"sujet {number}"],
        "a_retenir": "Le fait principal reste précisément délimité.",
        "interet_snum": "Le SNUM peut examiner cette évolution documentée.",
        "titre_original": f"Titre source {number}",
        "source": "Source publique",
        "date_publication": "2026-10-08",
        "url": f"https://example.org/article-{number}",
        "lecture": "INTEGRAL_LU",
        "preuve_lecture": "Corps complet ouvert avec l’outil de lecture Web.",
    }


def valid_data() -> dict:
    return {
        "version": "snum-v5.6",
        "date_edition": "2026-10-13",
        "date_debut_collecte": "2026-10-02",
        "date_fin_collecte": "2026-10-12",
        "etat_assistant": "A_COMPLETER",
        "evenements": [
            event(1),
            event(2, "INTELLIGENCE_ARTIFICIELLE_IA"),
            event(3, "VIE_DE_BERCY"),
        ],
        "essentiels": ["E01", "E02", "E03"],
        "a_surveiller": ["Suivre la prochaine publication officielle sur ce sujet."],
        "collecte": {
            "domaines_consultes": ["example.org"],
            "requetes": ["requête de contrôle"],
            "exclusions": [
                {"url": "https://example.org/exclu", "raison": "Article hors période."}
            ],
        },
        "limites": ["Accès public non revérifié par le générateur."],
    }


class ValidationTests(unittest.TestCase):
    def assert_invalid(self, data: dict, fragment: str) -> None:
        with self.assertRaisesRegex(generator.ValidationError, fragment):
            generator.validate(data)

    def test_sortie_valide_et_html_fidele(self) -> None:
        data = generator.validate(valid_data())
        template = (PROJECT_DIR / "gabarit-loic.html").read_text(encoding="utf-8")
        rendered = generator.render_html(data, template)
        self.assertEqual(rendered.count('class="fr-card fr-card--shadow top-card"'), 3)
        self.assertEqual(rendered.count('<article class="fr-col-12">'), 3)
        self.assertEqual(rendered.count('<p class="fr-tag">'), 3)
        self.assertIn('href="#navigation"', rendered)
        self.assertIn('role="navigation"', rendered)
        self.assertIn('role="banner"', rendered)
        self.assertIn('role="contentinfo"', rendered)
        self.assertIn("Accessibilité : non conforme", rendered)
        self.assertIn('type="module"', rendered)
        self.assertIn("nomodule", rendered)
        self.assertNotIn("@@", rendered)
        self.assertNotIn("{{", rendered)

    def test_refuse_fait_de_26_mots(self) -> None:
        data = valid_data()
        data["evenements"][0]["fait"] = " ".join(["mot"] * 26)
        self.assert_invalid(data, "26 mots")

    def test_refuse_rubrique_inventee(self) -> None:
        data = valid_data()
        data["evenements"][0]["rubrique"] = "REGULATION"
        self.assert_invalid(data, "rubrique est interdite")

    def test_refuse_essentiels_dupliques(self) -> None:
        data = valid_data()
        data["essentiels"] = ["E01", "E01", "E03"]
        self.assert_invalid(data, "identifiant")

    def test_refuse_date_hors_fenetre(self) -> None:
        data = valid_data()
        data["evenements"][0]["date_publication"] = "2026-10-01"
        self.assert_invalid(data, "hors fenêtre")

    def test_refuse_url_non_https(self) -> None:
        data = valid_data()
        data["evenements"][0]["url"] = "http://example.org/article"
        self.assert_invalid(data, "URL publique HTTPS")

    def test_collecte_vide_documentee_reste_valide(self) -> None:
        data = valid_data()
        data["evenements"] = []
        data["essentiels"] = []
        generator.validate(data)

    def test_commande_cree_les_quatre_fichiers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "sortie.txt"
            source.write_text(
                "```json\n" + json.dumps(valid_data(), ensure_ascii=False) + "\n```\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_DIR / "generer_revue.py"),
                    str(source),
                    "--sortie",
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = root / "livrable-2026-10-13"
            self.assertEqual(
                {path.name for path in output.iterdir()},
                {
                    "dossier-prive-2026-10-13.md",
                    "revue-snum-2026-10-13.html",
                    "revue-snum-2026-10-13.md",
                    "source-dinum.json",
                },
            )


if __name__ == "__main__":
    unittest.main()
