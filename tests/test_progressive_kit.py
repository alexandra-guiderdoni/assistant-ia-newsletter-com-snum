import re
import subprocess
import unittest
from pathlib import Path
from zipfile import ZipFile


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "build_progressive_kit.py"
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
ARCHIVE = PROJECT / "kit-dinum-snum-v5-8-progressif-8-fichiers.zip"


def html_blocks(path):
    return re.findall(
        r"```html\n(.*?)\n```",
        path.read_text(encoding="utf-8"),
        re.DOTALL,
    )


class ProgressiveKitTests(unittest.TestCase):
    def test_prompt_fits_the_dinum_limit(self):
        prompt = (PROJECT / "PROMPT-SYSTEME-SNUM-V5.8.md").read_text(
            encoding="utf-8"
        )
        self.assertLessEqual(len(prompt), 4000)
        self.assertIn("SNUM_CANON_V58_INDEX_START", prompt)
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


if __name__ == "__main__":
    unittest.main()
