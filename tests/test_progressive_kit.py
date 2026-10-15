import re
import subprocess
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "build_progressive_kit.py"
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
ARCHIVE = PROJECT / "kit-dinum-snum-v5-9-progressif-8-fichiers.zip"


def html_blocks(path):
    return re.findall(
        r"```html\n(.*?)\n```",
        path.read_text(encoding="utf-8"),
        re.DOTALL,
    )


class ProgressiveKitTests(unittest.TestCase):
    def test_prompt_fits_the_dinum_limit(self):
        prompt = (PROJECT / "PROMPT-SYSTEME-SNUM-V5.9.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(prompt), 4000)
        self.assertIn("SNUM_CANON_V59_INDEX_START", prompt)
        phases = ["`COLLECTE`", "`VALIDATION`", "`CANON`", "`RENDU`"]
        self.assertEqual(sorted(phases, key=prompt.index), phases)

    def test_fragments_recompose_the_canonical_blocks(self):
        source = html_blocks(SOURCE)
        head = html_blocks(PROJECT / "06-COQUE-DEBUT.md")
        tail = html_blocks(PROJECT / "07-COQUE-FIN.md")
        essential = html_blocks(PROJECT / "08-BLOC-ESSENTIEL.md")
        remaining = html_blocks(PROJECT / "09-BLOCS-RUBRIQUES.md")
        self.assertEqual(head[0] + "\n" + tail[0], source[0])
        self.assertEqual(essential + remaining, source[1:])

    def test_each_retrieval_document_stays_below_the_instruction_limit(self):
        for name in (
            "05-INDEX-HTML.md",
            "06-COQUE-DEBUT.md",
            "07-COQUE-FIN.md",
            "08-BLOC-ESSENTIEL.md",
            "09-BLOCS-RUBRIQUES.md",
        ):
            self.assertLessEqual(
                len((PROJECT / name).read_text(encoding="utf-8")),
                4000,
                name,
            )

    def test_archive_contains_only_the_eight_upload_files(self):
        with ZipFile(ARCHIVE) as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    "00-PROMPT-PROJET.md",
                    "01-ETAT-HISTORIQUE.md",
                    "02-METHODE-EDITORIALE.md",
                    "05-INDEX-HTML.md",
                    "06-COQUE-DEBUT.md",
                    "07-COQUE-FIN.md",
                    "08-BLOC-ESSENTIEL.md",
                    "09-BLOCS-RUBRIQUES.md",
                ],
            )

    def test_generated_kit_is_current(self):
        result = subprocess.run(
            ["python3", str(SCRIPT), "--check"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("KIT_PROGRESSIF_OK", result.stdout)

    def test_prompts_cover_date_and_navigation_failures(self):
        project_prompt = (PROJECT / "00-PROMPT-PROJET.md").read_text(encoding="utf-8")
        system_prompt = (PROJECT / "PROMPT-SYSTEME-SNUM-V5.9.md").read_text(
            encoding="utf-8"
        )
        index = (PROJECT / "05-INDEX-HTML.md").read_text(encoding="utf-8")
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        for content in (project_prompt, system_prompt, readme):
            self.assertIn("CONTROLE_DATES", content)
        for content in (project_prompt, system_prompt, index, readme):
            self.assertIn('href="#id"', content)
            self.assertIn('section `id="id"`', content)

    def test_collecte_requires_observable_coverage_before_completion(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "02-METHODE-EDITORIALE.md",
                "PROMPT-SYSTEME-SNUM-V5.9.md",
                "README.md",
            )
        ]
        for content in contents:
            self.assertIn("COUVERTURE_COLLECTE", content)
            self.assertIn("COLLECTE_INSUFFISANTE", content)
        for content in contents[1:]:
            self.assertIn("dix requêtes distinctes", content)
            self.assertIn("cinq domaines", content)
            self.assertIn("au moins cinq candidats", content)

    def test_canon_handoff_keeps_the_index_proof_for_render(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.9.md",
                "README.md",
                "NOTICE-V5.9.md",
            )
        ]
        for content in contents:
            self.assertIn("SNUM_CANON_V59_INDEX_END", content)
        for content in contents[:2]:
            self.assertIn("Pendant `RENDU`, ne recherche", content)


if __name__ == "__main__":
    unittest.main()
