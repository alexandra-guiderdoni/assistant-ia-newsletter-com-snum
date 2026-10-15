import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "newsletter_html.py"
TEMPLATE = PROJECT / "03-GABARIT-HTML.md"
COMPACT_TEMPLATE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"


def article(title, rubric, *, essential=False):
    return {
        "rubric": rubric,
        "title": title,
        "source": "Source & publique",
        "publication_date": "13 octobre 2026",
        "fact": "Un fait court, vérifié et utile au Service du numérique.",
        "keywords": ["numérique", "service public", "transformation"],
        "takeaway": "Le changement est confirmé.",
        "snum_interest": "Le SNUM peut anticiper sa mise en œuvre.",
        "url": f"https://example.org/{rubric}/{title.lower().replace(' ', '-')}",
        "essential": essential,
    }


class NewsletterHtmlCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )

    def payload(self):
        return {
            "edition_date": "14 octobre 2026",
            "edition_date_long": "mercredi 14 octobre 2026",
            "articles": [
                article("Numérique un", "numerique", essential=True),
                article("Numérique deux", "numerique"),
                article("IA un", "ia", essential=True),
                article("Commande un", "commande", essential=True),
            ],
            "watch": [
                {
                    "title": "Décision attendue",
                    "summary": "La publication officielle reste à surveiller.",
                }
            ],
        }

    def build_html(self, template=TEMPLATE):
        payload = self.payload()
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "newsletter.json"
            output_path = Path(temporary_directory) / "index.html"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            result = self.run_cli(
                "build",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--template",
                str(template),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return output_path.read_text(encoding="utf-8")

    def test_compact_assistant_template_matches_the_reference_template(self):
        self.assertEqual(self.build_html(COMPACT_TEMPLATE), self.build_html())

    def test_build_uses_the_canonical_bacoco_structure(self):
        html = self.build_html()
        self.assertIn('<nav class="fr-container" role="navigation" aria-label="Accès rapide">', html)
        self.assertIn(
            '<section id="essentiel" class="fr-container section-block">', html
        )
        self.assertIn('class="top-grid fr-grid-row fr-grid-row--gutters"', html)
        self.assertEqual(html.count('class="fr-card fr-card--shadow top-card"'), 3)
        self.assertNotIn('<p class="section-number">00</p>', html)
        self.assertIn('<p class="section-number">01</p>', html)
        self.assertIn('<section id="numerique"><div', html)
        self.assertIn('<section id="ia" class="section-muted"><div', html)
        self.assertIn('<section id="commande"><div', html)
        self.assertIn('href="#essentiel">L’essentiel</a>', html)
        self.assertIn('href="#surveiller">À surveiller</a>', html)
        self.assertNotIn('href="#rh"', html)
        self.assertIn('<p class="fr-tag">NUMERIQUE</p>', html)
        self.assertNotIn('<span class="fr-tag">', html)
        self.assertIn("numérique · service public · transformation", html)
        self.assertIn("SOURCE &amp; PUBLIQUE", html)
        self.assertIn('id="fr-theme-modal"', html)
        self.assertIn('src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.module.min.js"', html)
        self.assertIn('src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.nomodule.min.js"', html)
        self.assertIn('href="/revue-presse-snum/styles.css?v=20260917"', html)
        self.assertNotIn("@@", html)

    def test_validate_rejects_the_observed_dinum_drift(self):
        valid_html = re.sub(r">\s+<", "><", self.build_html()).strip()
        with tempfile.TemporaryDirectory() as temporary_directory:
            valid_path = Path(temporary_directory) / "valid.html"
            invalid_path = Path(temporary_directory) / "invalid.html"
            valid_path.write_text(valid_html, encoding="utf-8")
            invalid_html = (
                valid_html.replace(' role="navigation"', "", 1)
                .replace(
                    '<section id="essentiel" class="fr-container section-block">',
                    '<section class="essentials fr-container">',
                    1,
                )
                .replace(
                    'class="top-grid fr-grid-row fr-grid-row--gutters"',
                    'class="fr-grid-row"',
                    1,
                )
                .replace(
                    '<p class="section-number">01</p>',
                    '<p class="section-number">00</p>',
                    1,
                )
                .replace(
                    '<section id="ia" class="section-muted">',
                    '<section id="ia">',
                    1,
                )
                .replace('<dialog id="fr-theme-modal"', '<dialog id="theme-modal"', 1)
                .replace('<script type="module"', '<script', 1)
                .replace('<script nomodule', '<script', 1)
                .replace('<p class="fr-tag">', '<span class="fr-tag">', 1)
            )
            invalid_path.write_text(invalid_html, encoding="utf-8")
            valid_result = self.run_cli(
                "validate", "--input", str(valid_path), "--template", str(TEMPLATE)
            )
            invalid_result = self.run_cli(
                "validate", "--input", str(invalid_path), "--template", str(TEMPLATE)
            )

        self.assertEqual(valid_result.returncode, 0, valid_result.stderr)
        self.assertEqual(invalid_result.returncode, 1, invalid_result.stderr)
        for error_code in (
            "PAGE_SHELL",
            "SKIPLINKS_ROLE",
            "ESSENTIALS_STRUCTURE",
            "TOP_GRID",
            "SECTION_NUMBER_ZERO",
            "RUBRIC_WRAPPER_IA",
            "THEME_MODAL",
            "DSFR_MODULE",
            "DSFR_NOMODULE",
            "NONINTERACTIVE_TAG",
        ):
            self.assertIn(error_code, invalid_result.stderr)

    def test_validate_rejects_an_invented_rubric_id(self):
        valid_html = self.build_html()
        invalid_html = valid_html.replace(
            '<section id="ia" class="section-muted">',
            '<section id="formation_continue" class="section-muted">',
            1,
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            invalid_path = Path(temporary_directory) / "invalid-rubric.html"
            invalid_path.write_text(invalid_html, encoding="utf-8")
            result = self.run_cli(
                "validate", "--input", str(invalid_path), "--template", str(TEMPLATE)
            )

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("UNKNOWN_RUBRIC_ID", result.stderr)

    def test_validate_rejects_a_noncanonical_rubric_title(self):
        valid_html = self.build_html()
        invalid_html = valid_html.replace("<h2>NUMERIQUE</h2>", "<h2>Numérique</h2>", 1)
        with tempfile.TemporaryDirectory() as temporary_directory:
            invalid_path = Path(temporary_directory) / "invalid-rubric-title.html"
            invalid_path.write_text(invalid_html, encoding="utf-8")
            result = self.run_cli(
                "validate", "--input", str(invalid_path), "--template", str(TEMPLATE)
            )

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("RUBRIC_TITLE_NUMERIQUE", result.stderr)

    def test_validate_rejects_a_moved_theme_modal_without_hanging(self):
        valid_html = self.build_html()
        modal_start = valid_html.index('<dialog id="fr-theme-modal"')
        modal_end = valid_html.index("</dialog>", modal_start) + len("</dialog>")
        modal = valid_html[modal_start:modal_end]
        invalid_html = valid_html[:modal_start] + valid_html[modal_end:]
        invalid_html = invalid_html.replace("</main>", modal + "\n</main>", 1)
        with tempfile.TemporaryDirectory() as temporary_directory:
            invalid_path = Path(temporary_directory) / "moved-modal.html"
            invalid_path.write_text(invalid_html, encoding="utf-8")
            result = self.run_cli(
                "validate", "--input", str(invalid_path), "--template", str(TEMPLATE)
            )

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("PAGE_SHELL", result.stderr)

    def test_build_blocks_an_internally_invalid_page(self):
        payload = self.payload()
        payload["articles"] = []
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "newsletter.json"
            output_path = Path(temporary_directory) / "index.html"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            result = self.run_cli(
                "build",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--template",
                str(TEMPLATE),
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("SECTION_NUMBERS", result.stderr)
            self.assertFalse(output_path.exists())

    def test_build_rejects_a_fact_over_25_words(self):
        payload = self.payload()
        payload["articles"][0]["fact"] = " ".join(["mot"] * 26)
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "newsletter.json"
            output_path = Path(temporary_directory) / "index.html"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            result = self.run_cli(
                "build",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--template",
                str(TEMPLATE),
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("fait dépasse 25 mots", result.stderr)
            self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
