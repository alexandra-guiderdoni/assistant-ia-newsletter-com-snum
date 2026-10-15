import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]


class SplitProjectKitTests(unittest.TestCase):
    def test_projects_have_isolated_responsibilities(self):
        collecte = (PROJECT / "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md").read_text(
            encoding="utf-8"
        )
        rendu = (PROJECT / "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md").read_text(
            encoding="utf-8"
        )

        self.assertLessEqual(len(collecte), 4000)
        self.assertIn("PAQUET_RENDU", collecte)
        self.assertNotIn("HTML COMPLET", collecte)
        self.assertIn("Ne filtre aucun candidat selon sa date", collecte)
        self.assertIn("nombre exact d’entrées sous `CANDIDATS`", collecte)
        self.assertEqual(
            sorted(
                ("`COLLECTE`", "`VALIDATION`", "`PAQUET`"),
                key=collecte.index,
            ),
            ["`COLLECTE`", "`VALIDATION`", "`PAQUET`"],
        )

        self.assertLessEqual(len(rendu), 4000)
        self.assertIn("`RENDRE_EDITION`", rendu)
        self.assertIn("N’utilise pas le Web", rendu)
        for resource in (
            "CANON-HTML-01-COQUE-A-V5.17.md",
            "CANON-HTML-02-COQUE-B-V5.17.md",
            "CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md",
            "CANON-HTML-04-SURVEILLER-VIDE-V5.17.md",
        ):
            self.assertIn(resource, rendu)
        self.assertNotIn("`COLLECTE`", rendu)
        self.assertIn("navigation `L’essentiel` vers\n`#essentiel`", rendu)
        self.assertIn(
            "`@@TITRE_RUBRIQUE@@` reçoit le titre\ncanonique en capitales", rendu
        )
        self.assertIn("Sépare les mots-clés par\n` · `", rendu)
        self.assertIn("Ne recompte pas les mots", rendu)

    def test_renderer_uses_four_small_canonical_resources(self):
        expected = {
            "CANON-HTML-01-COQUE-A-V5.17.md": "SNUM_CANON_V517_COQUE_A",
            "CANON-HTML-02-COQUE-B-V5.17.md": "SNUM_CANON_V517_COQUE_B",
            "CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md": (
                "SNUM_CANON_V517_ESSENTIEL_RUBRIQUE"
            ),
            "CANON-HTML-04-SURVEILLER-VIDE-V5.17.md": (
                "SNUM_CANON_V517_SURVEILLER_VIDE"
            ),
        }

        for filename, marker in expected.items():
            resource = (PROJECT / filename).read_text(encoding="utf-8")
            self.assertLessEqual(len(resource), 4500, filename)
            self.assertTrue(resource.startswith(f"{marker}_START\n"), filename)
            self.assertTrue(resource.endswith(f"\n{marker}_END\n"), filename)

        coque_a = (PROJECT / "CANON-HTML-01-COQUE-A-V5.17.md").read_text(
            encoding="utf-8"
        )
        coque_b = (PROJECT / "CANON-HTML-02-COQUE-B-V5.17.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("<!doctype html>", coque_a)
        self.assertNotIn("<footer", coque_a)
        self.assertIn("<footer", coque_b)
        self.assertIn("</html>", coque_b)

    def test_packet_contract_builds_reference_html(self):
        packet_path = PROJECT / "EXEMPLE-PAQUET-RENDU-V5.17.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))

        self.assertEqual(packet["schema_version"], "SNUM_PAQUET_RENDU_V517")
        self.assertEqual(sum(article["essential"] for article in packet["articles"]), 3)
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
                    str(PROJECT / "05-BLOCS-HTML-CANONIQUES.md"),
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
            self.assertIn(
                'href="https://bacoco.github.io/revue-presse-snum/'
                'styles.css?v=20260917"',
                html,
            )
            self.assertNotIn('href="/revue-presse-snum/styles.css', html)
            self.assertIn('href="#essentiel">L’essentiel</a>', html)
            self.assertIn("<h2>NUMERIQUE</h2>", html)
            self.assertIn("service public · démarches · simplification", html)

    def test_installation_archive_contains_only_the_six_expected_files(self):
        archive_path = PROJECT / "kit-dinum-snum-v5-17-deux-projets-6-fichiers.zip"
        with ZipFile(archive_path) as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md",
                    "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md",
                    "CANON-HTML-01-COQUE-A-V5.17.md",
                    "CANON-HTML-02-COQUE-B-V5.17.md",
                    "CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md",
                    "CANON-HTML-04-SURVEILLER-VIDE-V5.17.md",
                ],
            )

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

    def test_notice_documents_the_complete_two_project_sequence(self):
        notice = (PROJECT / "NOTICE-V5.17.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )
        rendu = (
            (PROJECT / "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )

        self.assertIn(f"```text\n{collecte}\n```", notice)
        self.assertIn(f"```text\n{rendu}\n```", notice)
        for phase in (
            "PHASE COLLECTE.",
            "PHASE VALIDATION.",
            "PHASE PAQUET.",
            "PHASE RENDRE_EDITION.",
        ):
            self.assertEqual(notice.count(phase), 1, phase)
        self.assertIn("n’ajoutez aucune ressource", notice)
        self.assertIn("téléversez les quatre ressources `CANON-HTML-", notice)
        self.assertIn("copiez le bloc entier", notice)
        self.assertIn("A_COMPLETER", notice)

    def test_readme_is_the_pedagogical_v517_entry_point(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )
        rendu = (
            (PROJECT / "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )

        self.assertIn("# Configurer les deux Projets Newsletter SNUM V5.17", readme)
        self.assertIn(f"```text\n{collecte}\n```", readme)
        self.assertIn(f"```text\n{rendu}\n```", readme)
        self.assertIn("kit-dinum-snum-v5-17-deux-projets-6-fichiers.zip", readme)
        self.assertNotIn("guide V5.16", readme)


if __name__ == "__main__":
    unittest.main()
