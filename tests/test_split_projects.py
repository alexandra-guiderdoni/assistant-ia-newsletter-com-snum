import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]
COLLECTE_FILES = (
    "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md",
    "02-METHODE-COLLECTE-SNUM-V5.23.md",
    "03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md",
)
RENDU_FILES = (
    "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md",
    "21-CANON-HTML-COQUE-A-V5.19.md",
    "22-CANON-HTML-COQUE-B-V5.19.md",
    "23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md",
    "24-CANON-HTML-SURVEILLER-VIDE-V5.19.md",
)


class SplitProjectKitTests(unittest.TestCase):
    def test_active_installation_files_are_available_at_root(self):
        for name in (*COLLECTE_FILES, *RENDU_FILES):
            self.assertTrue((PROJECT / name).is_file(), name)
        self.assertFalse(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md").exists()
        )

    def test_v523_is_the_only_active_collecte_release(self):
        for version in ("5.20", "5.21", "5.22"):
            for stem in (
                "01-PROMPT-SYSTEME-COLLECTE-SNUM",
                "02-METHODE-COLLECTE-SNUM",
                "03-CONTRAT-PAQUET-RENDU-SNUM",
                "NOTICE",
                "RAPPORT",
            ):
                name = f"{stem}-V{version}.md"
                self.assertFalse((PROJECT / name).exists(), name)
                self.assertTrue(
                    (
                        PROJECT
                        / "_documentation"
                        / "archives"
                        / "releases"
                        / f"v{version}"
                        / name
                    ).is_file(),
                    name,
                )
        self.assertTrue((PROJECT / "NOTICE-V5.23.md").is_file())

    def test_historical_release_v5_17_is_preserved(self):
        archive = PROJECT / "_documentation" / "archives" / "releases" / "v5.17"
        for name in (
            "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md",
            "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md",
            "kit-dinum-snum-v5-17-deux-projets-6-fichiers.zip",
        ):
            self.assertTrue((archive / name).exists(), name)

    def test_projects_have_isolated_responsibilities(self):
        collecte = (PROJECT / COLLECTE_FILES[0]).read_text(encoding="utf-8")
        rendu = (PROJECT / RENDU_FILES[0]).read_text(encoding="utf-8")

        self.assertIn("recherche Web composite", collecte)
        self.assertIn("produis le paquet dans cette\nmême réponse", collecte)
        self.assertIn("PAQUET_RENDU", collecte)
        self.assertNotIn("HTML COMPLET", collecte)
        self.assertNotIn("REQUETE_COMPOSITE_A_COPIER", collecte)
        self.assertNotIn("NORMALISER_V519", collecte)
        self.assertNotIn("`VALIDER`", collecte)
        self.assertNotIn("`GENERER_PAQUET`", collecte)

        self.assertIn("`RENDRE_EDITION`", rendu)
        self.assertIn("sans Web ni\nréécriture", rendu)
        self.assertIn("`## HTML COMPLET`", rendu)
        self.assertNotIn("`COLLECTE`", rendu)
        for resource in RENDU_FILES[1:]:
            self.assertIn(resource, rendu)

    def test_renderer_uses_four_small_canonical_resources(self):
        expected = {
            "21-CANON-HTML-COQUE-A-V5.19.md": "SNUM_CANON_V519_COQUE_A",
            "22-CANON-HTML-COQUE-B-V5.19.md": "SNUM_CANON_V519_COQUE_B",
            "23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md": (
                "SNUM_CANON_V519_ESSENTIEL_RUBRIQUE"
            ),
            "24-CANON-HTML-SURVEILLER-VIDE-V5.19.md": (
                "SNUM_CANON_V519_SURVEILLER_VIDE"
            ),
        }
        for filename, marker in expected.items():
            resource = (PROJECT / filename).read_text(encoding="utf-8")
            self.assertLessEqual(len(resource), 4500, filename)
            self.assertTrue(resource.startswith(f"{marker}_START\n"), filename)
            self.assertTrue(resource.endswith(f"\n{marker}_END\n"), filename)

    def test_split_shell_reassembles_byte_for_byte(self):
        def html_block(filename):
            content = (PROJECT / filename).read_bytes()
            match = re.search(rb"```html\n(.*?)\n```", content, re.DOTALL)
            self.assertIsNotNone(match, filename)
            return match.group(1)

        source = (PROJECT / "_source" / "05-BLOCS-HTML-CANONIQUES.md").read_bytes()
        expected = re.search(rb"```html\n(<!doctype html>.*?)\n```", source, re.DOTALL)
        self.assertIsNotNone(expected)
        assembled = html_block(RENDU_FILES[1]) + html_block(RENDU_FILES[2])
        self.assertEqual(assembled, expected.group(1))

    def test_packet_contract_builds_reference_html(self):
        packet_path = PROJECT / "EXEMPLE-PAQUET-RENDU-V5.19.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))

        self.assertEqual(packet["schema_version"], "SNUM_PAQUET_RENDU_V519")
        self.assertEqual(
            set(packet),
            {
                "schema_version",
                "edition_date",
                "edition_date_long",
                "window_start",
                "window_end",
                "articles",
                "watch",
            },
        )
        self.assertEqual(sum(a["essential"] for a in packet["articles"]), 3)
        self.assertEqual(
            len({a["url"] for a in packet["articles"]}), len(packet["articles"])
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "index.html"
            result = subprocess.run(
                [
                    "python3",
                    str(PROJECT / "scripts" / "newsletter_html.py"),
                    "build",
                    "--input",
                    str(packet_path),
                    "--output",
                    str(output),
                    "--template",
                    str(PROJECT / "_source" / "05-BLOCS-HTML-CANONIQUES.md"),
                ],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertTrue(html.startswith("<!doctype html>"))
            self.assertNotIn("@@", html)
            self.assertEqual(html.count('class="fr-card fr-card--shadow top-card"'), 3)
            self.assertIn('href="#essentiel">L’essentiel</a>', html)
            self.assertIn("<h2>NUMERIQUE</h2>", html)

    def test_installation_archives_match_the_two_assistant_projects(self):
        projects = (
            ("Newsletter SNUM - Collecte", COLLECTE_FILES),
            ("Newsletter SNUM - Rendu HTML", RENDU_FILES),
        )
        for project_name, filenames in projects:
            with ZipFile(PROJECT / f"{project_name}.zip") as archive:
                self.assertEqual(
                    archive.namelist(),
                    [
                        f"{project_name}/",
                        *(f"{project_name}/{name}" for name in filenames),
                    ],
                )
                for name in filenames:
                    archived = archive.read(f"{project_name}/{name}").decode("utf-8")
                    self.assertEqual(
                        archived,
                        (PROJECT / name).read_text(encoding="utf-8"),
                        name,
                    )

    def test_generated_kit_has_no_drift(self):
        result = subprocess.run(
            ["python3", str(PROJECT / "scripts" / "build_split_kit.py"), "--check"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("KIT_DECOUPLE_OK", result.stdout)

    def test_documentation_describes_the_two_project_workflow(self):
        for name in ("README.md", "NOTICE-V5.23.md"):
            content = (PROJECT / name).read_text(encoding="utf-8")

            for required_file in (*COLLECTE_FILES, *RENDU_FILES):
                self.assertIn(required_file, content)
            self.assertRegex(content, r"recherch\w* (?:sur le )?Web")
            self.assertIn("deux conversations", content)
            self.assertIn("PAQUET_RENDU_PRET", content)
            self.assertIn("## HTML COMPLET", content)
            self.assertNotIn("nouveau chat Assistant ordinaire", content)
            self.assertNotIn("REQUETE_COMPOSITE_A_COPIER", content)
            self.assertNotIn("RESULTATS_COMPOSITES_ENREGISTRES", content)
            self.assertNotIn("NORMALISER_V519", content)
            self.assertNotIn("```text\nVALIDER\n```", content)
            self.assertNotIn("```text\nGENERER_PAQUET\n```", content)

    def test_readme_is_the_active_entry_point(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# Configurer les deux Projets Newsletter SNUM", readme)
        self.assertIn("Newsletter SNUM - Collecte.zip", readme)
        self.assertIn("Newsletter SNUM - Rendu HTML.zip", readme)
        self.assertNotIn("kit-dinum-snum-v5-19-deux-projets-6-fichiers.zip", readme)


if __name__ == "__main__":
    unittest.main()
