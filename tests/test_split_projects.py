import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]


class SplitProjectKitTests(unittest.TestCase):
    def test_collecte_uses_a_small_execute_then_render_orchestrator(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())
        self.assertLessEqual(len(prompt), 2500)
        self.assertLessEqual(len(method), 3600)
        self.assertIn("EXÉCUTION AVANT RENDU", prompt_normalized)
        self.assertIn(
            "Avant toute réponse, termine les appels Web exigés par la méthode",
            prompt_normalized,
        )
        self.assertIn(
            "Ensuite, rends une seule réponse complète commençant par `TRACE_RECHERCHE`",
            prompt_normalized,
        )
        phases = ("## 1. EXÉCUTER", "## 2. CALCULER", "## 3. RENDRE")
        self.assertEqual(sorted(phases, key=method.index), list(phases))

    def test_v520_collecte_runs_from_dates_then_short_commands(self):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md"
        method_path = PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md"
        contract_path = PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md"

        for path in (prompt_path, method_path, contract_path):
            self.assertTrue(path.is_file(), path.name)
            self.assertLessEqual(len(path.read_text(encoding="utf-8")), 4500, path.name)

        prompt = prompt_path.read_text(encoding="utf-8")
        prompt_normalized = " ".join(prompt.split())
        self.assertLessEqual(len(prompt), 4000)
        self.assertIn(method_path.name, prompt)
        self.assertIn(contract_path.name, prompt)
        self.assertIn("message initial", prompt_normalized)
        self.assertIn("Au tour du message `VALIDER`", prompt)
        self.assertIn("Au tour du message `GENERER_PAQUET`", prompt)
        self.assertNotIn("`CONTINUE`", prompt)
        self.assertNotIn("marqueur attendu", prompt)
        self.assertIn(
            "Ne compare jamais la date d’édition aux bornes", prompt_normalized
        )
        method = method_path.read_text(encoding="utf-8")
        self.assertIn("`COLLECTE_TERMINEE`", method)
        self.assertIn("`VALIDATION_TERMINEE`", prompt)
        self.assertIn("`PAQUET_RENDU_PRET`", prompt)
        self.assertIn("Ne lance jamais deux étapes dans le même tour", prompt)
        self.assertIn("Entrée manquante, ambiguë ou inversée", prompt_normalized)
        self.assertNotIn("une seule réponse finale", prompt)
        self.assertNotIn("exécute uniquement la phase demandée", prompt.lower())

        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### Message initial dans le Projet Collecte", readme)
        self.assertIn("DATE_EDITION = 14 octobre 2026", readme)
        self.assertIn("PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus", readme)
        self.assertEqual(readme.count("```text\nVALIDER\n```"), 1)
        self.assertEqual(readme.count("```text\nGENERER_PAQUET\n```"), 1)
        self.assertNotIn("```text\nCONTINUE\n```", readme)
        self.assertNotIn("### Message 1 avec le Web", readme)
        self.assertNotIn("### Message 2 sans le Web", readme)
        self.assertNotIn("### Message 3 sans le Web", readme)

        with ZipFile(PROJECT / "Newsletter SNUM - Collecte.zip") as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    "Newsletter SNUM - Collecte/",
                    f"Newsletter SNUM - Collecte/{prompt_path.name}",
                    f"Newsletter SNUM - Collecte/{method_path.name}",
                    f"Newsletter SNUM - Collecte/{contract_path.name}",
                ],
            )

    def test_collecte_traces_both_search_passes_before_insufficiency(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("`TRACE_RECHERCHE`", prompt)
        self.assertIn("`TRACE_RECHERCHE`", method)
        self.assertIn("`PASSE_1`", method)
        self.assertIn("`PASSE_2`", method)
        self.assertIn("exactement cinq requêtes ciblées", method_normalized)
        self.assertIn("`REQUETE`", method)
        self.assertIn("`STATUT_WEB=EXECUTEE`", method)
        self.assertIn("`URL_EXAMINEES`", method)
        self.assertIn("`NB_DANS_FENETRE`", method)
        self.assertIn("10 requêtes `EXECUTEE`", method_normalized)
        self.assertIn("5 en `PASSE_2`", method_normalized)
        self.assertIn("Affiche intégralement `TRACE_RECHERCHE`", prompt)
        self.assertIn("Avant toute réponse, termine les appels Web", prompt)
        self.assertIn("OUTIL_WEB_INDISPONIBLE", prompt)
        self.assertIn("OUTIL_WEB_INDISPONIBLE", method)
        self.assertLessEqual(len(prompt), 4000)
        self.assertLessEqual(len(method), 4500)

    def test_collecte_prompt_forbids_false_success_and_invalid_query_shapes(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("une requête sans `site:`", method_normalized)
        self.assertIn("une avec `site:`", method_normalized)
        self.assertIn("domaines absents de `PASSE_1`", method_normalized)
        self.assertIn("moins de cinq candidats datés", method_normalized)
        self.assertIn("Branche terminale unique", method_normalized)
        self.assertIn("Sinon, après deux passes insuffisantes", method_normalized)
        self.assertIn("COLLECTE_INSUFFISANTE", method_normalized)
        self.assertIn("Avant toute réponse, termine les appels Web", prompt)

    def test_collecte_distinguishes_empty_results_from_web_failure(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("Zéro résultat reste", prompt_normalized)
        self.assertIn("n’est pas `OUTIL_WEB_INDISPONIBLE`", prompt_normalized)
        self.assertIn("URL_EXAMINEES=AUCUNE", prompt_normalized)
        self.assertIn("Poursuis toutes les requêtes", prompt_normalized)

    def test_collecte_response_starts_directly_with_search_trace(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("Le tout premier caractère visible", prompt_normalized)
        self.assertIn("Extrais silencieusement", prompt_normalized)
        self.assertIn(
            "Le tout premier caractère visible est le `T` de `TRACE_RECHERCHE`",
            prompt_normalized,
        )
        self.assertIn(
            "une seule réponse complète commençant par `TRACE_RECHERCHE`",
            prompt_normalized,
        )

    def test_collecte_accepts_an_edition_date_after_the_collection_window(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())
        valid_example = (
            "`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide"
        )

        self.assertIn(valid_example, prompt_normalized)
        self.assertLess(
            prompt_normalized.index(valid_example),
            prompt_normalized.index("Entrée manquante, ambiguë ou inversée"),
        )
        self.assertIn("poursuis `COLLECTE`", prompt_normalized)
        self.assertIn("`DATE_EDITION` sert uniquement au paquet", prompt_normalized)

    def test_collecte_forbids_stopping_after_empty_contract_headings(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("Les trois titres seuls sont invalides", prompt_normalized)
        self.assertIn(
            "N’affiche aucun titre avant les appels Web",
            prompt_normalized,
        )

    def test_collecte_reconciles_window_count_with_exact_candidate_dates(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("`DATE_ISO_PROVISOIRE`", method_normalized)
        self.assertIn("`DANS_FENETRE=OUI|NON`", method_normalized)
        self.assertIn("date exacte de publication", method_normalized)
        self.assertIn("jour, mois et année", method_normalized)
        self.assertIn("URL canoniques uniques marquées `OUI`", method_normalized)
        self.assertIn(
            "`NB_DANS_FENETRE` égale les URL canoniques uniques marquées `OUI`",
            method_normalized,
        )
        self.assertIn(
            "`CANDIDATS` et, une seule fois, `NB_DANS_FENETRE`",
            method_normalized,
        )
        self.assertNotIn(
            "Pour chaque passe, donne `NB_DANS_FENETRE`", method_normalized
        )
        self.assertIn("`NB_DANS_FENETRE >= 5`", method_normalized)
        self.assertIn("`ETAPE_SUIVANTE | Envoyez VALIDER`", method_normalized)
        self.assertIn("`COLLECTE_INSUFFISANTE | NB_DANS_FENETRE=N`", method_normalized)

    def test_collecte_never_counts_out_of_window_candidates(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("affiche `DANS_FENETRE=OUI|NON` par URL", prompt_normalized)
        self.assertIn(
            "`N` compte seulement les URL uniques `OUI`, jamais tous les candidats",
            prompt_normalized,
        )
        self.assertIn(
            "7 candidats dont 5 `OUI` donne `NB_DANS_FENETRE = 5`",
            prompt_normalized,
        )

    def test_collecte_rejects_observed_october_first_and_month_only_regression(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn(
            "`2026-10-01` vaut `NON` pour `2026-10-03..2026-10-13`",
            prompt_normalized,
        )
        self.assertIn("un mois seul reste `INCONNUE` et `NON`", prompt_normalized)
        self.assertIn("si `OUI` != `N`, corrige et recompte", prompt_normalized)

    def test_collecte_always_renders_the_terminal_branch_after_the_count(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn(
            "`N >= 5` termine par `COLLECTE_TERMINEE`; sinon termine par "
            "`A_COMPLETER | COLLECTE_INSUFFISANTE | NB_DANS_FENETRE=N`",
            prompt_normalized,
        )

    def test_collecte_rejects_dates_outside_the_inclusive_iso_bounds(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        predicate = "`DEBUT_ISO <= DATE_ISO_PROVISOIRE <= FIN_ISO`"
        self.assertIn(predicate, method_normalized)
        self.assertIn("date ISO `< DEBUT_ISO` ou `> FIN_ISO`", method_normalized)
        self.assertIn("corrige puis recompte avant d’afficher", method_normalized)
        self.assertLess(
            method_normalized.index("## 2. CALCULER"),
            method_normalized.index("## 3. RENDRE"),
        )

    def test_collecte_recomputes_final_window_statuses_from_scratch(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("recalcule chaque `DANS_FENETRE` depuis zéro", method_normalized)
        self.assertIn("`BORNE_BASSE_OK=OUI`", method_normalized)
        self.assertIn("`BORNE_HAUTE_OK=OUI`", method_normalized)
        self.assertIn(
            "Si l’un vaut `NON`, impose `DANS_FENETRE=NON`", method_normalized
        )
        self.assertIn("aucune date hors bornes n’est marquée `OUI`", method_normalized)
        self.assertIn("corrige puis recompte avant d’afficher", method_normalized)

    def test_technical_sources_are_kept_out_of_root(self):
        for name in ("03-GABARIT-HTML.md", "05-BLOCS-HTML-CANONIQUES.md"):
            self.assertFalse((PROJECT / name).exists(), name)
            self.assertTrue((PROJECT / "_source" / name).is_file(), name)

    def test_active_installation_files_are_available_at_root(self):
        expected = (
            "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md",
            "02-METHODE-COLLECTE-SNUM-V5.20.md",
            "03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md",
            "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md",
            "21-CANON-HTML-COQUE-A-V5.19.md",
            "22-CANON-HTML-COQUE-B-V5.19.md",
            "23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md",
            "24-CANON-HTML-SURVEILLER-VIDE-V5.19.md",
        )
        for name in expected:
            self.assertTrue((PROJECT / name).is_file(), name)
        self.assertFalse(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md").exists()
        )

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
        collecte = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        rendu = (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md").read_text(
            encoding="utf-8"
        )

        self.assertLessEqual(len(collecte), 4000)
        self.assertIn("PAQUET_RENDU", collecte)
        self.assertNotIn("HTML COMPLET", collecte)
        self.assertIn("DATE_EDITION", collecte)
        self.assertIn("PERIODE", collecte)
        operational_steps = (
            "Au tour du message initial, exécute seulement `COLLECTE`",
            "Au tour du message `VALIDER`, exécute seulement `VALIDATION`",
            "Au tour du message `GENERER_PAQUET`, exécute seulement `PAQUET`",
        )
        self.assertEqual(
            sorted(operational_steps, key=collecte.index), list(operational_steps)
        )

        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        contract = (PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md").read_text(
            encoding="utf-8"
        )
        legacy_collecte = (
            PROJECT
            / "_documentation"
            / "archives"
            / "releases"
            / "v5.19"
            / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.19.md"
        ).read_text(encoding="utf-8")
        collecte_start = legacy_collecte.index("Pendant `COLLECTE`")
        validation_start = legacy_collecte.index("Pendant `VALIDATION`")
        paquet_start = legacy_collecte.index("Pendant `PAQUET`")
        legacy_collecte_block = legacy_collecte[
            collecte_start:validation_start
        ].rstrip()
        legacy_contract = legacy_collecte[paquet_start:].rstrip()

        self.assertNotIn(legacy_collecte_block, method)
        self.assertIn(legacy_contract, contract)
        self.assertIn("Chaque requête cible explicitement la fenêtre", method)
        self.assertIn("moins de cinq candidats datés provisoirement", method)
        self.assertIn("après deux passes insuffisantes", method)
        self.assertIn("Ne filtre aucun candidat selon sa date", method)
        self.assertIn("seconde passe", method)
        self.assertIn("`NB_DANS_FENETRE >= 5`", method)
        self.assertIn("date ISO `>= DEBUT_ISO`", method)
        self.assertIn("date ISO `<= FIN_ISO`", method)
        self.assertIn("Déduplique d’abord par URL canonique", method)
        self.assertIn("`valides + exclues = candidats`", method)
        self.assertIn("SNUM_PAQUET_RENDU_V519", contract)
        self.assertIn("`publication_date_iso`", contract)
        self.assertIn("`publication_date_long`", contract)
        self.assertNotIn("`publication_date`,", contract)

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
                    f"{collecte_folder}/01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md",
                    f"{collecte_folder}/02-METHODE-COLLECTE-SNUM-V5.20.md",
                    f"{collecte_folder}/03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md",
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
        notice = (PROJECT / "NOTICE-V5.20.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md")
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
        self.assertNotIn("PHASE COLLECTE.", notice)
        self.assertNotIn("PHASE VALIDATION.", notice)
        self.assertNotIn("PHASE PAQUET.", notice)
        self.assertEqual(notice.count("PHASE RENDRE_EDITION."), 1)
        self.assertIn("02-METHODE-COLLECTE-SNUM-V5.20.md", notice)
        self.assertIn("03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md", notice)
        self.assertIn("téléversez les quatre ressources `CANON-HTML-", notice)
        self.assertIn("copiez le bloc entier", notice)
        self.assertIn("A_COMPLETER", notice)
        self.assertIn("Newsletter SNUM - Collecte.zip", notice)
        self.assertIn("Newsletter SNUM - Rendu HTML.zip", notice)

    def test_readme_is_the_pedagogical_active_entry_point(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )
        rendu = (
            (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")
            .read_text(encoding="utf-8")
            .rstrip("\n")
        )

        self.assertIn("# Configurer les deux Projets Newsletter SNUM", readme)
        self.assertIn(f"```text\n{collecte}\n```", readme)
        self.assertIn(f"```text\n{rendu}\n```", readme)
        self.assertIn("Newsletter SNUM - Collecte.zip", readme)
        self.assertIn("Newsletter SNUM - Rendu HTML.zip", readme)
        self.assertNotIn("kit-dinum-snum-v5-19-deux-projets-6-fichiers.zip", readme)
        self.assertNotIn("guide V5.17", readme)


if __name__ == "__main__":
    unittest.main()
