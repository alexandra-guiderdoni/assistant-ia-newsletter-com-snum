import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]


class SplitProjectKitTests(unittest.TestCase):
    def test_technical_sources_are_kept_out_of_root(self):
        for name in ("03-GABARIT-HTML.md", "05-BLOCS-HTML-CANONIQUES.md"):
            self.assertFalse((PROJECT / name).exists(), name)
            self.assertTrue((PROJECT / "_source" / name).is_file(), name)

    def test_active_installation_files_are_available_at_root(self):
        expected = (
            "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md",
            "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md",
            "21-CANON-HTML-COQUE-A-V5.19.md",
            "22-CANON-HTML-COQUE-B-V5.19.md",
            "23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md",
            "24-CANON-HTML-SURVEILLER-VIDE-V5.19.md",
        )
        for name in expected:
            self.assertTrue((PROJECT / name).is_file(), name)

    def test_historical_release_v5_17_is_preserved(self):
        archive = PROJECT / "_documentation" / "archives" / "releases" / "v5.17"
        for name in (
            "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md",
            "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md",
            "kit-dinum-snum-v5-17-deux-projets-6-fichiers.zip",
        ):
            self.assertTrue((archive / name).exists(), name)

    def test_root_contains_only_the_active_versioned_release(self):
        inactive = []
        for path in PROJECT.iterdir():
            if path.is_file() and any(
                f"V5.{version}" in path.name or f"v5-{version}" in path.name
                for version in range(8, 19)
            ):
                inactive.append(path.name)
        self.assertEqual(inactive, [])

    def test_projects_have_isolated_responsibilities(self):
        collecte = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md").read_text(
            encoding="utf-8"
        )
        rendu = (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md").read_text(
            encoding="utf-8"
        )

        self.assertLessEqual(len(collecte), 4000)
        self.assertIn("PAQUET_RENDU", collecte)
        self.assertNotIn("HTML COMPLET", collecte)
        self.assertIn("Ne filtre aucun candidat selon sa date", collecte)
        self.assertIn("nombre exact d’entrées sous `CANDIDATS`", collecte)
        self.assertIn("date ISO >= DEBUT_ISO", collecte)
        self.assertIn("date ISO <= FIN_ISO", collecte)
        self.assertIn("`publication_date_iso`", collecte)
        self.assertIn("`publication_date_long`", collecte)
        self.assertNotIn("`publication_date`,", collecte)
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
            "21-CANON-HTML-COQUE-A-V5.19.md",
            "22-CANON-HTML-COQUE-B-V5.19.md",
            "23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md",
            "24-CANON-HTML-SURVEILLER-VIDE-V5.19.md",
        ):
            self.assertIn(resource, rendu)
        self.assertNotIn("`COLLECTE`", rendu)
        self.assertIn("navigation `L’essentiel` vers\n`#essentiel`", rendu)
        self.assertIn(
            "`@@TITRE_RUBRIQUE@@` reçoit le titre\ncanonique en capitales", rendu
        )
        self.assertIn("Sépare les mots-clés par\n` · `", rendu)
        self.assertIn("Ne recompte pas les mots", rendu)
        self.assertIn("Affiche seulement `publication_date_long`", rendu)
        self.assertIn("les deux désignent le même jour", rendu)

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

        coque_a = (PROJECT / "21-CANON-HTML-COQUE-A-V5.19.md").read_text(
            encoding="utf-8"
        )
        coque_b = (PROJECT / "22-CANON-HTML-COQUE-B-V5.19.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("<!doctype html>", coque_a)
        self.assertNotIn("<footer", coque_a)
        self.assertIn("<footer", coque_b)
        self.assertIn("</html>", coque_b)

    def test_split_shell_reassembles_byte_for_byte(self):
        def html_block(filename):
            content = (PROJECT / filename).read_bytes()
            match = re.search(rb"```html\n(.*?)\n```", content, re.DOTALL)
            self.assertIsNotNone(match, filename)
            return match.group(1)

        source = (PROJECT / "_source" / "05-BLOCS-HTML-CANONIQUES.md").read_bytes()
        expected = re.search(rb"```html\n(<!doctype html>.*?)\n```", source, re.DOTALL)
        self.assertIsNotNone(expected)

        assembled = html_block("21-CANON-HTML-COQUE-A-V5.19.md") + html_block(
            "22-CANON-HTML-COQUE-B-V5.19.md"
        )
        self.assertEqual(assembled, expected.group(1))

    def test_packet_contract_builds_reference_html(self):
        packet_path = PROJECT / "EXEMPLE-PAQUET-RENDU-V5.19.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))

        self.assertEqual(packet["schema_version"], "SNUM_PAQUET_RENDU_V519")
        self.assertEqual(packet["edition_date"], "2026-10-14")
        self.assertEqual(packet["edition_date_long"], "14 octobre 2026")
        for article in packet["articles"]:
            self.assertIn("publication_date_iso", article)
            self.assertIn("publication_date_long", article)
            self.assertNotIn("publication_date", article)
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
            self.assertIn(
                'href="https://bacoco.github.io/revue-presse-snum/'
                'styles.css?v=20260917"',
                html,
            )
            self.assertNotIn('href="/revue-presse-snum/styles.css', html)
            self.assertIn('href="#essentiel">L’essentiel</a>', html)
            self.assertIn("<h2>NUMERIQUE</h2>", html)
            self.assertIn("service public · démarches · simplification", html)

    def test_installation_archives_match_the_two_assistant_projects(self):
        collecte_folder = "Newsletter SNUM - Collecte"
        collecte_path = PROJECT / "Newsletter SNUM - Collecte.zip"
        with ZipFile(collecte_path) as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    f"{collecte_folder}/",
                    f"{collecte_folder}/01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md",
                ],
            )

        rendu_folder = "Newsletter SNUM - Rendu HTML"
        rendu_path = PROJECT / "Newsletter SNUM - Rendu HTML.zip"
        with ZipFile(rendu_path) as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    f"{rendu_folder}/",
                    f"{rendu_folder}/20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md",
                    f"{rendu_folder}/21-CANON-HTML-COQUE-A-V5.19.md",
                    f"{rendu_folder}/22-CANON-HTML-COQUE-B-V5.19.md",
                    f"{rendu_folder}/23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md",
                    f"{rendu_folder}/24-CANON-HTML-SURVEILLER-VIDE-V5.19.md",
                ],
            )

        self.assertFalse(
            (PROJECT / "kit-dinum-snum-v5-19-deux-projets-6-fichiers.zip").exists()
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
        notice = (PROJECT / "NOTICE-V5.19.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )
        rendu = (
            (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")
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
        self.assertIn("Newsletter SNUM - Collecte.zip", notice)
        self.assertIn("Newsletter SNUM - Rendu HTML.zip", notice)

    def test_readme_is_the_pedagogical_v519_entry_point(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )
        rendu = (
            (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )

        self.assertIn("# Configurer les deux Projets Newsletter SNUM V5.19", readme)
        self.assertIn(f"```text\n{collecte}\n```", readme)
        self.assertIn(f"```text\n{rendu}\n```", readme)
        self.assertIn("Newsletter SNUM - Collecte.zip", readme)
        self.assertIn("Newsletter SNUM - Rendu HTML.zip", readme)
        self.assertNotIn("kit-dinum-snum-v5-19-deux-projets-6-fichiers.zip", readme)
        self.assertNotIn("guide V5.17", readme)


if __name__ == "__main__":
    unittest.main()
