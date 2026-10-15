import re
import subprocess
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "build_progressive_kit.py"
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
ARCHIVE = PROJECT / "kit-dinum-snum-v5-16-progressif-9-fichiers.zip"


def html_blocks(path):
    return re.findall(
        r"```html\n(.*?)\n```",
        path.read_text(encoding="utf-8"),
        re.DOTALL,
    )


class ProgressiveKitTests(unittest.TestCase):
    def test_historical_v516_merges_canon_and_render_in_one_user_message(self):
        prompt_path = PROJECT / "PROMPT-SYSTEME-SNUM-V5.16.md"
        self.assertTrue(prompt_path.exists(), prompt_path.name)
        prompt = prompt_path.read_text(encoding="utf-8")
        self.assertIn("`CANON_RENDU`", prompt)
        self.assertNotIn("`CANON`, puis `RENDU`", prompt)

    def test_historical_release_v5_16_is_preserved(self):
        expected = (
            "PROMPT-SYSTEME-SNUM-V5.16.md",
            "NOTICE-V5.16.md",
            "kit-dinum-snum-v5-16-progressif-9-fichiers.zip",
        )
        for name in expected:
            self.assertTrue((PROJECT / name).exists(), name)
        index = (PROJECT / "05-INDEX-HTML.md").read_text(encoding="utf-8")
        self.assertIn("SNUM_CANON_V516_INDEX_START", index)
        self.assertIn("SNUM_CANON_V516_INDEX_END", index)

    def test_prompt_fits_the_dinum_limit(self):
        prompt = (PROJECT / "PROMPT-SYSTEME-SNUM-V5.16.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(prompt), 4000)
        self.assertIn("SNUM_CANON_V516_INDEX_START", prompt)
        phases = ["`COLLECTE`", "`VALIDATION`", "`DONNEES`", "`CANON_RENDU`"]
        self.assertEqual(sorted(phases, key=prompt.index), phases)

    def test_notice_v516_references_the_preserved_system_prompt(self):
        notice = (PROJECT / "NOTICE-V5.16.md").read_text(encoding="utf-8")
        self.assertIn("PROMPT-SYSTEME-SNUM-V5.16.md", notice)
        self.assertIn("NO-GO", notice)

    def test_render_prepares_data_before_checking_the_final_html(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
                "NOTICE-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("DONNEES_RENDU_PRETES", content)
            self.assertIn("brouillon HTML complet non affiché", content)
            self.assertIn("contrôle seulement ce brouillon final", content)
            self.assertIn(
                "Les marqueurs @@ des fragments sont des entrées normales", content
            )

    def test_fragments_recompose_the_canonical_blocks(self):
        source = html_blocks(SOURCE)
        head = html_blocks(PROJECT / "06-COQUE-DEBUT.md")
        footer = html_blocks(PROJECT / "07-PIED-DE-PAGE.md")
        tail = html_blocks(PROJECT / "10-COQUE-FIN.md")
        essential = html_blocks(PROJECT / "08-BLOC-ESSENTIEL.md")
        remaining = html_blocks(PROJECT / "09-BLOCS-RUBRIQUES.md")
        self.assertEqual(head[0] + "\n" + footer[0] + "\n" + tail[0], source[0])
        self.assertEqual("\n".join(essential), source[1])
        self.assertEqual("\n".join(remaining[:3]), source[2])
        self.assertEqual(remaining[3:], source[3:])

    def test_repeatable_content_has_atomic_canonical_fragments(self):
        essential = (PROJECT / "08-BLOC-ESSENTIEL.md").read_text(encoding="utf-8")
        rubrics = (PROJECT / "09-BLOCS-RUBRIQUES.md").read_text(encoding="utf-8")
        for marker in (
            "SNUM_ESSENTIALS_OPEN_START",
            "SNUM_ESSENTIAL_CARD_START",
            "SNUM_ESSENTIALS_CLOSE_START",
        ):
            self.assertIn(marker, essential)
        for marker in (
            "SNUM_RUBRIC_OPEN_START",
            "SNUM_RUBRIC_ARTICLE_START",
            "SNUM_RUBRIC_CLOSE_START",
        ):
            self.assertIn(marker, rubrics)
        footer = (PROJECT / "07-PIED-DE-PAGE.md").read_text(encoding="utf-8")
        tail = (PROJECT / "10-COQUE-FIN.md").read_text(encoding="utf-8")
        self.assertIn("SNUM_FOOTER_START", footer)
        self.assertIn("SNUM_FOOTER_END", footer)
        self.assertIn("SNUM_SHELL_CLOSE_START", tail)
        self.assertIn("SNUM_SHELL_CLOSE_END", tail)

    def test_each_retrieval_document_stays_below_the_instruction_limit(self):
        for name in (
            "05-INDEX-HTML.md",
            "06-COQUE-DEBUT.md",
            "07-PIED-DE-PAGE.md",
            "08-BLOC-ESSENTIEL.md",
            "09-BLOCS-RUBRIQUES.md",
            "10-COQUE-FIN.md",
        ):
            self.assertLessEqual(
                len((PROJECT / name).read_text(encoding="utf-8")),
                4000,
                name,
            )

    def test_each_canonical_resource_is_short_enough_for_literal_retrieval(self):
        for name in (
            "05-INDEX-HTML.md",
            "06-COQUE-DEBUT.md",
            "07-PIED-DE-PAGE.md",
            "08-BLOC-ESSENTIEL.md",
            "09-BLOCS-RUBRIQUES.md",
            "10-COQUE-FIN.md",
        ):
            self.assertLess(
                len((PROJECT / name).read_bytes()),
                3000,
                name,
            )

    def test_archive_contains_only_the_nine_upload_files(self):
        with ZipFile(ARCHIVE) as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    "00-PROMPT-PROJET.md",
                    "01-ETAT-HISTORIQUE.md",
                    "02-METHODE-EDITORIALE.md",
                    "05-INDEX-HTML.md",
                    "06-COQUE-DEBUT.md",
                    "07-PIED-DE-PAGE.md",
                    "08-BLOC-ESSENTIEL.md",
                    "09-BLOCS-RUBRIQUES.md",
                    "10-COQUE-FIN.md",
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
        system_prompt = (PROJECT / "PROMPT-SYSTEME-SNUM-V5.16.md").read_text(
            encoding="utf-8"
        )
        index = (PROJECT / "05-INDEX-HTML.md").read_text(encoding="utf-8")
        for content in (project_prompt, system_prompt):
            self.assertIn("CONTROLE_DATES", content)
        for content in (project_prompt, system_prompt, index):
            self.assertIn('href="#id"', content)
            self.assertIn('section `id="id"`', content)

    def test_collecte_requires_observable_coverage_before_completion(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "02-METHODE-EDITORIALE.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("COUVERTURE_COLLECTE", content)
            self.assertIn("COLLECTE_INSUFFISANTE", content)
        for content in contents[1:]:
            self.assertIn("dix requêtes distinctes", content)
            self.assertIn("cinq domaines", content)
            self.assertIn("au moins cinq candidats", content)

    def test_collection_preserves_absolute_https_urls(self):
        contents = [
            (PROJECT / "00-PROMPT-PROJET.md").read_text(encoding="utf-8"),
            (PROJECT / "02-METHODE-EDITORIALE.md").read_text(encoding="utf-8"),
            (PROJECT / "PROMPT-SYSTEME-SNUM-V5.16.md").read_text(encoding="utf-8"),
        ]
        requirement = "URL canonique absolue commençant par `https://`"
        for content in contents:
            self.assertIn(requirement, content)

    def test_canon_render_uses_the_v5_16_index(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
                "NOTICE-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("SNUM_CANON_V516_INDEX_END", content)

    def test_canon_and_render_share_one_message(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
                "NOTICE-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("CANON_RENDU", content)
            self.assertIn("même tour", content)

    def test_canon_prompt_requires_all_exact_start_end_pairs(self):
        pairs = (
            "SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END",
            "SNUM_FOOTER_START / SNUM_FOOTER_END",
            "SNUM_SHELL_CLOSE_START / SNUM_SHELL_CLOSE_END",
            "SNUM_ESSENTIALS_OPEN_START / SNUM_ESSENTIALS_OPEN_END",
            "SNUM_ESSENTIAL_CARD_START / SNUM_ESSENTIAL_CARD_END",
            "SNUM_ESSENTIALS_CLOSE_START / SNUM_ESSENTIALS_CLOSE_END",
            "SNUM_RUBRIC_OPEN_START / SNUM_RUBRIC_OPEN_END",
            "SNUM_RUBRIC_ARTICLE_START / SNUM_RUBRIC_ARTICLE_END",
            "SNUM_RUBRIC_CLOSE_START / SNUM_RUBRIC_CLOSE_END",
            "SNUM_WATCH_START / SNUM_WATCH_END",
            "SNUM_EMPTY_START / SNUM_EMPTY_END",
        )
        index = (PROJECT / "05-INDEX-HTML.md").read_text(encoding="utf-8")
        for pair in pairs:
            self.assertIn(pair, index)
        for content in (
            (PROJECT / "00-PROMPT-PROJET.md").read_text(encoding="utf-8"),
            (PROJECT / "PROMPT-SYSTEME-SNUM-V5.16.md").read_text(encoding="utf-8"),
        ):
            self.assertIn("sans fusion ni auto-fermant", content)

    def test_long_dates_never_add_a_weekday(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
                "NOTICE-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("sans jour de semaine", content)
            self.assertIn("DATE_CALENDRIER_INCOHERENTE", content)

    def test_under_three_sources_never_selects_essentials(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("moins de trois sources", content)
            self.assertIn("ESSENTIEL=NON", content)
            self.assertTrue(
                "Instancie les blocs essentiels uniquement si au moins trois" in content
                or "Sous trois sources, remplace `@@ESSENTIELS@@` par vide" in content
            )

    def test_validation_contract_deduplicates_by_event(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "02-METHODE-EDITORIALE.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("CLE_EVENEMENT", content)
            self.assertIn("DOUBLON_DE", content)

    def test_render_failure_is_diagnostic_and_has_no_success_state_collision(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "02-METHODE-EDITORIALE.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn("CONTROLES_EN_ECHEC", content)
            self.assertIn("PRODUITE - contrôle métier requis", content)
        self.assertIn("CANON_MANQUANT", contents[0])
        self.assertIn("CANON_MANQUANT", contents[2])

    def test_missing_data_diagnostics_name_the_source_and_field(self):
        contents = [
            (PROJECT / name).read_text(encoding="utf-8")
            for name in (
                "00-PROMPT-PROJET.md",
                "PROMPT-SYSTEME-SNUM-V5.16.md",
            )
        ]
        for content in contents:
            self.assertIn(
                "SOURCE_MANQUANTE | <identifiant> | <champ>",
                content,
            )
            self.assertIn(
                "DONNEES_MANQUANTES | <identifiant ou EDITION> | <champ>",
                content,
            )


if __name__ == "__main__":
    unittest.main()
