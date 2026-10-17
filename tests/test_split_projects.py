import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

PROJECT = Path(__file__).resolve().parents[1]


class SplitProjectKitTests(unittest.TestCase):
    def test_v524_best_effort_reaches_json_without_recount_gate(self):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md"
        method_path = PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md"

        prompt = " ".join(prompt_path.read_text(encoding="utf-8").split())
        method = " ".join(method_path.read_text(encoding="utf-8").split())

        fixed_route = (
            "`RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→"
            "`RECHERCHE_RH`→`RECHERCHE_BERCY`→`COLLECTE_TERMINEE_BEST_EFFORT`"
        )
        self.assertIn(fixed_route, method)
        for transition in (
            "`RECHERCHE_NUMERIQUE→RECHERCHE_IA`",
            "`RECHERCHE_IA→RECHERCHE_COMMANDE`",
            "`RECHERCHE_COMMANDE→RECHERCHE_RH`",
            "`RECHERCHE_RH→RECHERCHE_BERCY`",
            "`RECHERCHE_BERCY→VALIDER`",
        ):
            self.assertIn(transition, prompt)
        self.assertIn("rends `COLLECTE_TERMINEE_BEST_EFFORT`", prompt)
        self.assertIn("`REQUETE_A_ENVOYER=VALIDER`", prompt)
        self.assertIn("l’insuffisance dans `watch` sans bloquer le JSON", prompt)
        for text in (prompt, method):
            self.assertNotIn("`RECOMPTER`", text)
            self.assertNotIn("COLLECTE_INSUFFISANTE", text)

    def test_v524_visible_out_of_window_result_still_advances(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Même si `DANS_FENETRE=NON`, avance", prompt)
        self.assertIn("`RECHERCHE_RH→RECHERCHE_BERCY`", prompt)
        self.assertIn("Après `RECHERCHE_BERCY`, rends", prompt)
        self.assertIn("`COLLECTE_TERMINEE_BEST_EFFORT`", prompt)

    def test_v524_packet_is_directly_compatible_with_the_html_project(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        contract = " ".join(
            (PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("`REQUETE_A_ENVOYER=GENERER_PAQUET`", prompt)
        self.assertIn("`03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`", prompt)
        self.assertIn("`SNUM_PAQUET_RENDU_V519_START`", contract)
        self.assertIn("`SNUM_PAQUET_RENDU_V519_END`", contract)
        self.assertIn(
            "`schema_version`=`SNUM_PAQUET_RENDU_V519`, `edition_date`, "
            "`edition_date_long`, "
            "`window_start`, `window_end`, `articles`, `watch`",
            contract,
        )
        self.assertIn(
            "`schema_version`=`SNUM_PAQUET_RENDU_V519`",
            contract,
        )
        self.assertIn(
            "`id`, `rubric`, `title`, `source`, `publication_date_iso`, "
            "`publication_date_long`, `url`, `fact`, `keywords`, `takeaway`, "
            "`snum_interest`, `essential`",
            contract,
        )
        self.assertIn(
            "`watch` contient seulement des objets `title` et `summary`",
            contract,
        )
        self.assertIn(
            "`rubric` vaut seulement `numerique`, `ia`, `commande`, `rh` ou `bercy`",
            contract,
        )
        self.assertIn("`snum_interest` au plus 15 mots", contract)
        self.assertIn("exactement trois portent `essential=true`", contract)
        self.assertIn(
            "Après analyse réussie, termine par `PAQUET_RENDU_PRET`",
            prompt,
        )
        self.assertNotIn("`metadata`", contract)
        self.assertNotIn("`sources`", contract)

    def test_v524_each_web_search_handles_results_and_business_validation(
        self,
    ):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md"
        method_path = PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md"

        self.assertTrue(prompt_path.is_file(), prompt_path.name)
        self.assertTrue(method_path.is_file(), method_path.name)
        prompt = " ".join(prompt_path.read_text(encoding="utf-8").split())
        method = " ".join(method_path.read_text(encoding="utf-8").split())

        self.assertIn("une seule recherche Web par message", prompt)
        self.assertIn("`VALIDATION_METIER_REQUISE`", prompt)
        self.assertIn("Source visible ou non ⇒ avance toujours", prompt)
        for transition in (
            "`RECHERCHE_NUMERIQUE→RECHERCHE_IA`",
            "`RECHERCHE_IA→RECHERCHE_COMMANDE`",
            "`RECHERCHE_COMMANDE→RECHERCHE_RH`",
            "`RECHERCHE_RH→RECHERCHE_BERCY`",
            "`RECHERCHE_BERCY→VALIDER`",
        ):
            self.assertIn(transition, prompt)
        self.assertNotIn("`PROCHAINE_COMMANDE=IA`", prompt)
        self.assertIn("Sans source visible", method)

    def test_v524_validated_searches_chain_to_the_json_packet(self):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md"
        contract_path = PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md"

        self.assertTrue(prompt_path.is_file(), prompt_path.name)
        self.assertTrue(contract_path.is_file(), contract_path.name)
        prompt = " ".join(prompt_path.read_text(encoding="utf-8").split())
        contract = " ".join(contract_path.read_text(encoding="utf-8").split())

        steps = (
            "`RECHERCHE_BERCY→VALIDER`",
            "rends `COLLECTE_TERMINEE_BEST_EFFORT`",
            "Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER`",
            "Rends `VALIDATION_TERMINEE`",
            "Après `VALIDATION_TERMINEE`, `GENERER_PAQUET`",
            "`PAQUET_RENDU_PRET`",
        )
        self.assertEqual(sorted(steps, key=prompt.index), list(steps))
        self.assertIn("`SNUM_PAQUET_RENDU_V519_START`", contract)
        self.assertIn("`SNUM_PAQUET_RENDU_V519_END`", contract)
        self.assertIn("vérifie que le bloc est analysable comme JSON", contract)

    def test_v524_search_turns_store_the_window_decision_in_the_registry(self):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md"
        method_path = PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md"

        self.assertTrue(prompt_path.is_file(), prompt_path.name)
        self.assertTrue(method_path.is_file(), method_path.name)
        prompt = " ".join(prompt_path.read_text(encoding="utf-8").split())
        method = " ".join(method_path.read_text(encoding="utf-8").split())

        self.assertIn(
            "Après chaque recherche, si une source est visible, rends "
            "`RESULTATS_RECHERCHE` non vide",
            prompt,
        )
        record = (
            "`Uxx|rubrique|URL|date brute|date ISO|"
            "DANS_FENETRE=OUI|NON|titre|source|fait`"
        )
        self.assertIn(record, prompt)
        self.assertIn(record, method)
        self.assertIn("valide les sources et décisions visibles", prompt)

    def test_v524_collecte_advances_one_rubric_per_turn(self):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md"
        method_path = PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md"

        self.assertTrue(prompt_path.is_file(), prompt_path.name)
        self.assertTrue(method_path.is_file(), method_path.name)

        prompt = " ".join(prompt_path.read_text(encoding="utf-8").split())
        method = " ".join(method_path.read_text(encoding="utf-8").split())
        commands = (
            "RECHERCHE_NUMERIQUE",
            "RECHERCHE_IA",
            "RECHERCHE_COMMANDE",
            "RECHERCHE_RH",
            "RECHERCHE_BERCY",
        )

        self.assertIn("message initial", prompt)
        self.assertIn("NUMERIQUE", prompt)
        for command in commands:
            self.assertIn(command, prompt)
        self.assertEqual(
            sorted(commands, key=prompt.index),
            list(commands),
        )
        self.assertIn("Une seule recherche est demandée par message", method)
        method_transition = (
            "`RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→"
            "`RECHERCHE_RH`→`RECHERCHE_BERCY`→"
            "`COLLECTE_TERMINEE_BEST_EFFORT`; suivant≠reçu"
        )
        self.assertIn(method_transition, method)
        for transition in (
            "`RECHERCHE_NUMERIQUE→RECHERCHE_IA`",
            "`RECHERCHE_IA→RECHERCHE_COMMANDE`",
            "`RECHERCHE_COMMANDE→RECHERCHE_RH`",
            "`RECHERCHE_RH→RECHERCHE_BERCY`",
            "`RECHERCHE_BERCY→VALIDER`",
        ):
            self.assertIn(transition, prompt)
        self.assertIn("Sortie≠entrée", prompt)
        self.assertIn("Ne répète aucun lot", prompt)
        self.assertIn("`VALIDATION_METIER_REQUISE`", prompt)

    def test_v524_collecte_exposes_the_exact_next_command(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("la `REQUETE_A_ENVOYER` suivante", prompt)
        self.assertIn("`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE", prompt)
        for transition in (
            "`RECHERCHE_NUMERIQUE→RECHERCHE_IA`",
            "`RECHERCHE_IA→RECHERCHE_COMMANDE`",
            "`RECHERCHE_COMMANDE→RECHERCHE_RH`",
            "`RECHERCHE_RH→RECHERCHE_BERCY`",
            "`RECHERCHE_BERCY→VALIDER`",
        ):
            self.assertIn(transition, prompt)
        self.assertIn("`REQUETE_A_ENVOYER=VALIDER`", prompt)
        self.assertNotIn("`PROCHAINE_COMMANDE=", prompt)
        self.assertNotIn("`RECOMPTER`", prompt)

    def test_v524_each_search_requires_web_evidence_before_transition(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Recherchez sur le Web du <début> au <fin> inclus", prompt)
        self.assertIn("Titre, URL HTTPS, date exacte", prompt)
        self.assertIn("`VALIDATION_METIER_REQUISE`", prompt)
        self.assertIn("`RECHERCHE_SANS_SOURCE_PROUVEE | <rubrique>`", prompt)

    def test_initial_message_requires_dates_and_numerique(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "`DATE_EDITION = <date en français>` "
            "`PERIODE = du <date en français> au <date en français> inclus` "
            "`NUMERIQUE`",
            prompt,
        )
        self.assertIn("Exige ces lignes", prompt)
        self.assertIn("`A_COMPLETER | PARAMETRES_INVALIDES | <détail>`", prompt)

    def test_initial_numerique_prepares_the_first_explicit_web_query(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Sans Web, le message initial rend", prompt)
        self.assertIn("`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE", prompt)
        self.assertIn(
            "`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web",
            prompt,
        )
        self.assertIn(
            "`REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE | Recherchez sur le Web du "
            "<début> au <fin> inclus en France : <AXE>. Titre, URL HTTPS, date exacte.`",
            prompt,
        )
        for search_axis in (
            "services publics numériques, dématérialisation, inclusion et données",
            "intelligence artificielle, modèles, régulation et usages publics",
            "commande publique, achats, marchés et fournisseurs numériques",
            "ressources humaines publiques, compétences, recrutement et formation",
            "ministères économiques et financiers, directions et transformations",
        ):
            self.assertIn(search_axis, prompt)
        self.assertNotIn("`PROCHAINE_COMMANDE=IA`", prompt)

    def test_v524_registry_requires_one_auditable_decision_per_unique_url(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "`Uxx|rubrique|URL|date brute|date ISO|"
            "DANS_FENETRE=OUI|NON|titre|source|fait`",
            prompt,
        )
        self.assertIn("`DEBUT_ISO <= date ISO <= FIN_ISO`", prompt)
        self.assertIn("chaque nouvelle URL canonique unique", prompt)
        self.assertIn("`VALIDATION_METIER_REQUISE`", prompt)

    def test_v524_is_the_only_active_collecte_release(self):
        active = (
            "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md",
            "02-METHODE-COLLECTE-SNUM-V5.24.md",
            "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md",
        )
        for name in active:
            self.assertTrue((PROJECT / name).is_file(), name)

        with ZipFile(PROJECT / "Newsletter SNUM - Collecte.zip") as archive:
            self.assertEqual(
                archive.namelist(),
                [
                    "Newsletter SNUM - Collecte/",
                    *(f"Newsletter SNUM - Collecte/{name}" for name in active),
                ],
            )

        for version in ("5.20", "5.21", "5.22", "5.23"):
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
        self.assertTrue((PROJECT / "NOTICE-V5.24.md").is_file())

    def test_collecte_uses_a_small_execute_then_render_orchestrator(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())
        self.assertLessEqual(len(prompt), 4000)
        self.assertLessEqual(len(method), 3600)
        self.assertIn("## Recherches validées par le métier", prompt_normalized)
        self.assertIn("une seule recherche Web par message", prompt_normalized)
        phases = (
            "## 1. Préparer les requêtes",
            "## 2. Contrôler chaque recherche",
            "## 3. Terminer la collecte en best effort",
            "## 4. Valider",
        )
        self.assertEqual(sorted(phases, key=method.index), list(phases))

    def test_collecte_explicitly_loads_its_method_before_execution(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(prompt.split())
        load = (
            "Charge `02-METHODE-COLLECTE-SNUM-V5.24.md` et "
            "`03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md`"
        )

        self.assertIn(load, normalized)
        self.assertLess(
            normalized.index(load),
            normalized.index("## Recherches validées par le métier"),
        )

    def test_v524_collecte_runs_from_dates_then_validated_queries(self):
        prompt_path = PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md"
        method_path = PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md"
        contract_path = PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md"

        for path in (prompt_path, method_path, contract_path):
            self.assertTrue(path.is_file(), path.name)
            self.assertLessEqual(len(path.read_text(encoding="utf-8")), 4500, path.name)

        prompt = prompt_path.read_text(encoding="utf-8")
        prompt_normalized = " ".join(prompt.split())
        self.assertLessEqual(len(prompt), 4000)
        self.assertIn(method_path.name, prompt)
        self.assertIn(contract_path.name, prompt)
        self.assertIn("message initial", prompt_normalized)
        self.assertIn("Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER`", prompt)
        self.assertIn("Après `VALIDATION_TERMINEE`, `GENERER_PAQUET`", prompt)
        self.assertNotIn("`CONTINUE`", prompt)
        self.assertIn(
            "ne compare jamais la date d’édition aux bornes", prompt_normalized
        )
        method = method_path.read_text(encoding="utf-8")
        self.assertIn("`COLLECTE_TERMINEE_BEST_EFFORT`", method)
        self.assertIn("`VALIDATION_TERMINEE`", prompt)
        self.assertIn("`PAQUET_RENDU_PRET`", prompt)
        self.assertIn("Une transition par tour", prompt)
        self.assertIn(
            "Entrée manquante, ambiguë ou fenêtre inversée", prompt_normalized
        )
        self.assertNotIn("une seule réponse finale", prompt)
        self.assertNotIn("exécute uniquement la phase demandée", prompt.lower())

        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### Message initial dans le Projet Collecte", readme)
        self.assertIn(
            "```text\n"
            "DATE_EDITION = 14 octobre 2026\n"
            "PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus\n"
            "NUMERIQUE\n"
            "```",
            readme,
        )
        self.assertEqual(readme.count("```text\nVALIDER\n```"), 1)
        self.assertEqual(readme.count("```text\nGENERER_PAQUET\n```"), 1)
        self.assertNotIn("```text\nCONTINUE\n```", readme)
        for command in (
            "REQUETE_A_ENVOYER=RECHERCHE_NUMERIQUE",
            "REQUETE_A_ENVOYER=RECHERCHE_IA",
            "REQUETE_A_ENVOYER=RECHERCHE_COMMANDE",
            "REQUETE_A_ENVOYER=RECHERCHE_RH",
            "REQUETE_A_ENVOYER=RECHERCHE_BERCY",
        ):
            self.assertIn(command, readme)
        readme_normalized = " ".join(readme.split())
        self.assertIn(
            "La séquence ci-dessus est la source de vérité", readme_normalized
        )
        self.assertIn("répète une rubrique", readme_normalized)
        self.assertIn("`COLLECTE_TERMINEE_BEST_EFFORT`", readme)

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

    def test_collecte_uses_five_search_lots_then_validation(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn(
            "Ordre immuable : `RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→"
            "`RECHERCHE_COMMANDE`→`RECHERCHE_RH`→`RECHERCHE_BERCY`→"
            "`COLLECTE_TERMINEE_BEST_EFFORT`; suivant≠reçu",
            method_normalized,
        )
        self.assertIn("Une seule recherche est demandée par message", method_normalized)
        self.assertIn("`REQUETE_A_ENVOYER=VALIDER`", method)
        self.assertNotIn("`RECOMPTER`", method)
        self.assertNotIn("`PASSE_2`", method)
        self.assertNotIn("`TRACE_RECHERCHE`", prompt)
        self.assertIn("RECHERCHE_SANS_SOURCE_PROUVEE", method)
        self.assertLessEqual(len(prompt), 4000)
        self.assertLessEqual(len(method), 4500)

    def test_collecte_prompt_forbids_false_success_and_invalid_query_shapes(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn(
            "demande explicitement une recherche sur le Web", method_normalized
        )
        self.assertIn(
            "sources gouvernementales ou institutionnelles", method_normalized
        )
        self.assertIn("Aucun compteur ni seuil ne bloque", method_normalized)
        self.assertNotIn("COLLECTE_INSUFFISANTE", method_normalized)
        self.assertIn("Source visible ou non ⇒ avance toujours", prompt)

    def test_collecte_advances_after_empty_web_results(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("Sans source visible", method_normalized)
        self.assertIn("registre inchangé", method_normalized)
        self.assertIn("Avance à la requête suivante", method_normalized)
        self.assertNotIn("relance exactement la même requête", method_normalized)

    def test_collecte_search_turns_do_not_render_intermediate_state(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("rends `RESULTATS_RECHERCHE` non vide", prompt_normalized)
        self.assertIn("Ne répète aucun lot", prompt_normalized)
        self.assertNotIn("`ETAT_COLLECTE`", prompt_normalized)

    def test_collecte_accepts_an_edition_date_after_the_collection_window(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())
        valid_example = (
            "`DATE_EDITION=2026-10-14` avec fenêtre `2026-10-03..2026-10-13` est valide"
        )

        self.assertIn(valid_example, prompt_normalized)
        self.assertLess(
            prompt_normalized.index(valid_example),
            prompt_normalized.index("Entrée manquante, ambiguë ou fenêtre inversée"),
        )
        self.assertIn(
            "ne compare jamais la date d’édition aux bornes", prompt_normalized
        )
        self.assertIn("La date d’édition sert seulement au paquet", prompt_normalized)

    def test_collecte_classifies_each_source_during_its_search_turn(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("DANS_FENETRE=OUI|NON", prompt_normalized)
        self.assertIn("`DEBUT_ISO <= date ISO <= FIN_ISO`", prompt_normalized)
        self.assertIn(
            "Après chaque recherche, si une source est visible", prompt_normalized
        )

    def test_collecte_validates_exact_dates_without_a_count_gate(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("DANS_FENETRE=OUI|NON", method_normalized)
        self.assertIn("Une date exacte contient jour, mois et année", method_normalized)
        self.assertIn("Aucun compteur ni seuil ne bloque", method_normalized)
        self.assertNotIn("`NB_DANS_FENETRE`", method_normalized)

    def test_validation_reuses_the_cumulative_registry_one_to_one(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        method = " ".join(
            (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Après chaque recherche", prompt)
        for text in (prompt, method):
            self.assertIn("`REGISTRE_CUMULATIF`", text)
            self.assertIn("`U01`", text)
            self.assertIn("recopie sans changement", text)
            self.assertIn("ajoute chaque nouvelle URL", text)
            self.assertIn(
                "`U01` puis `max(Uxx)+1`; aucun réemploi",
                text,
            )
            self.assertIn("DANS_FENETRE=OUI|NON", text)
        self.assertIn("depuis `REGISTRE_CUMULATIF`", method)
        self.assertIn(
            "`2026-10-04` et `2026-10-11` valent `OUI`",
            method,
        )

    def test_collecte_never_validates_out_of_window_sources(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("DANS_FENETRE=OUI|NON", method_normalized)
        self.assertIn(
            "Une source est valide si `DANS_FENETRE` et accès valent `OUI`",
            method_normalized,
        )

    def test_collecte_rejects_observed_october_first_and_month_only_regression(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn(
            "Pour `2026-10-03..2026-10-13`, le `2026-10-01` vaut `NON`",
            method_normalized,
        )
        self.assertIn("avec `INCONNUE` si la date n’est pas exacte", method_normalized)

    def test_collecte_skips_targeted_searches_in_minimal_best_effort(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        targeted_commands = tuple(
            f"RECHERCHE_CIBLEE_{rubric}"
            for rubric in ("NUMERIQUE", "IA", "COMMANDE", "RH", "BERCY")
        )

        for command in targeted_commands:
            self.assertNotIn(command, prompt)
            self.assertNotIn(command, method)
        self.assertIn("`COLLECTE_TERMINEE_BEST_EFFORT`", prompt)

    def test_collecte_always_renders_the_best_effort_terminal_branch(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn("`COLLECTE_TERMINEE_BEST_EFFORT`", prompt_normalized)
        self.assertIn("`REQUETE_A_ENVOYER=VALIDER`", prompt_normalized)
        self.assertIn("ne bloque jamais sur un nombre minimal", prompt_normalized)

    def test_validation_persists_its_full_outputs_for_the_packet_turn(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        self.assertIn(
            "Affiche `CONTROLE_DATES`, `SOURCES_VALIDES` et `SOURCES_EXCLUES`",
            prompt_normalized,
        )
        self.assertIn("Registre vide admis", prompt_normalized)

    def test_validation_cannot_reopen_the_search_completeness_guard(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; "
            "ne demande rien à l’utilisateur",
            prompt,
        )
        self.assertIn("ne bloque jamais sur un nombre minimal", prompt)

    def test_validation_builds_controls_without_requesting_more_user_data(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        method = " ".join(
            (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        guard = (
            "À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`; "
            "ne demande rien à l’utilisateur"
        )
        self.assertIn(guard, prompt)
        self.assertIn(guard, method)

    def test_visible_web_sources_cannot_render_an_empty_result_block(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        method = " ".join(
            (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        guard = "si une source est visible, rends `RESULTATS_RECHERCHE` non vide"
        self.assertIn(guard, prompt)
        self.assertIn(guard, method)
        self.assertIn("Source visible ou non ⇒ avance toujours", prompt)

    def test_best_effort_marks_validation_as_the_next_command(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        method = " ".join(
            (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        for text in (prompt, method):
            self.assertIn("`REQUETE_A_ENVOYER=VALIDER`", text)
            self.assertNotIn("`RECOMPTER`", text)

    def test_validation_success_requires_a_complete_control_line_per_candidate(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        method = " ".join(
            (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "Pour chaque entrée du registre, produis `CONTROLE_DATES` : titre, "
            "dates brute/ISO, bornes, accès, `CLE_EVENEMENT` et décision",
            method,
        )
        self.assertIn("`valides + exclues = registre`", prompt)
        self.assertIn("Rends `VALIDATION_TERMINEE`", prompt)

    def test_exact_packet_command_cannot_fall_through_to_invalid_state(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        prompt_normalized = " ".join(prompt.split())

        route = (
            "Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`"
        )
        guard = "`GENERER_PAQUET` n’est jamais `ETAT_INVALIDE` dans cet état"
        self.assertIn(route, prompt_normalized)
        self.assertIn(guard, prompt_normalized)
        self.assertIn(
            "À `VALIDER`, produis toi-même depuis `REGISTRE_CUMULATIF`",
            prompt_normalized,
        )

    def test_packet_success_requires_parsing_the_exact_emitted_json(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "analyse exactement le JSON émis avec un parseur",
            prompt,
        )
        self.assertIn("`PAQUET_INCOMPLET | JSON_INVALIDE`", prompt)
        self.assertIn(
            "Après analyse réussie, termine par `PAQUET_RENDU_PRET`",
            prompt,
        )

    def test_packet_success_is_one_immediately_copyable_marked_block(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )
        contract = (PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        contract_normalized = " ".join(contract.split())
        passerelle = " ".join(contract.split("## PASSERELLE_RENDU", 1)[1].split())

        self.assertIn(
            "réponds immédiatement par un seul bloc de code copiable",
            prompt,
        )
        self.assertIn("`PASSERELLE_RENDU`", prompt)
        self.assertIn("PHASE RENDRE_EDITION.", passerelle)
        self.assertIn(
            "Charge séparément les quatre ressources CANON-HTML V5.19", passerelle
        )
        self.assertIn(
            "Pour `numerique`, titre et tag valent exactement `NUMERIQUE`, sans accent",
            passerelle,
        )
        self.assertIn(
            "commence exactement par ces lignes, avant `SNUM_PAQUET_RENDU_V519_START`",
            contract_normalized,
        )
        self.assertIn(
            "termine après le marqueur de fin par `PAQUET_RENDU_PRET`",
            contract_normalized,
        )
        self.assertIn(
            "Aucun préambule ni texte hors du bloc",
            prompt,
        )

    def test_packet_repeat_preserves_the_complete_marked_packet(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "Toute demande de redonner le JSON répète à l’identique ce même bloc complet",
            prompt,
        )

    def test_packet_prompt_keeps_v519_schema_and_escapes_internal_quotes(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("`schema_version`=`SNUM_PAQUET_RENDU_V519`", prompt)
        self.assertIn('Échappe tout guillemet interne en `\\"`', prompt)

    def test_packet_ready_requires_all_word_limits_to_be_rechecked(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn(
            "compte les mots de chaque `fact` (≤25), `takeaway` et "
            "`snum_interest` (≤15)",
            prompt,
        )
        self.assertIn(
            "N’émets jamais `PAQUET_RENDU_PRET` si une limite échoue",
            prompt,
        )

    def test_packet_command_builds_its_own_json_without_user_input(self):
        prompt = " ".join(
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
            .read_text(encoding="utf-8")
            .split()
        )

        self.assertIn("Construis toi-même le JSON depuis `SOURCES_VALIDES`", prompt)
        self.assertIn("ne demande jamais de paquet à l’utilisateur", prompt)
        self.assertIn("analyse exactement le JSON émis", prompt)
        self.assertLess(
            prompt.index("Construis toi-même le JSON"),
            prompt.index("analyse exactement le JSON émis"),
        )

    def test_collecte_rejects_dates_outside_the_inclusive_iso_bounds(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        predicate = "`DEBUT_ISO <= date ISO <= FIN_ISO`"
        self.assertIn(predicate, method_normalized)
        self.assertIn("sinon utilise `NON`", method_normalized)
        self.assertLess(
            method_normalized.index("## 1. Préparer les requêtes"),
            method_normalized.index("## 3. Terminer la collecte en best effort"),
        )

    def test_collecte_does_not_recompute_window_statuses_at_the_end(self):
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method_normalized = " ".join(method.split())

        self.assertIn("DANS_FENETRE=OUI|NON", method_normalized)
        self.assertIn(
            "le métier valide les sources et leurs décisions", method_normalized
        )
        self.assertNotIn("`CANDIDATS`", method_normalized)
        self.assertNotIn("`BORNE_BASSE_OK`", method_normalized)

    def test_technical_sources_are_kept_out_of_root(self):
        for name in ("03-GABARIT-HTML.md", "05-BLOCS-HTML-CANONIQUES.md"):
            self.assertFalse((PROJECT / name).exists(), name)
            self.assertTrue((PROJECT / "_source" / name).is_file(), name)

    def test_active_installation_files_are_available_at_root(self):
        expected = (
            "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md",
            "02-METHODE-COLLECTE-SNUM-V5.24.md",
            "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md",
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
        collecte = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
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
            "Sans Web, le message initial rend",
            "`RECHERCHE_NUMERIQUE→RECHERCHE_IA`",
            "## Valider en best effort",
            "Après `COLLECTE_TERMINEE_BEST_EFFORT`, `VALIDER` exécute seulement `VALIDATION`",
            "Après `VALIDATION_TERMINEE`, `GENERER_PAQUET` exécute seulement `PAQUET`",
        )
        self.assertEqual(
            sorted(operational_steps, key=collecte.index), list(operational_steps)
        )

        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        contract = (PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md").read_text(
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
        self.assertIn("Vise la période inclusive en France", method)
        self.assertNotIn("`PASSE_2`", method)
        self.assertNotIn("`RECOMPTER`", collecte)
        self.assertIn("`DEBUT_ISO <= date ISO <= FIN_ISO`", method)
        self.assertIn("ajoute chaque nouvelle URL canonique unique", method)
        self.assertIn("`valides + exclues = registre`", method)
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
        self.assertIn("`L’essentiel` vers `#essentiel`", rendu)
        self.assertIn(
            "`@@TITRE_RUBRIQUE@@` reçoit le titre\ncanonique en capitales", rendu
        )
        self.assertIn("Sépare les mots-clés par\n` · `", rendu)
        rendu_normalized = " ".join(rendu.split())
        self.assertIn(
            "ne revalide ni URL, dates, espaces, champs, mots-clés, essentiels ni contenus",
            rendu_normalized,
        )
        self.assertIn("Utilise chaque valeur littéralement", rendu_normalized)

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

    def test_renderer_preserves_values_and_emits_only_the_deliverable(self):
        prompt = (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `\"`→`&quot;`, `'`→`&#x27;`",
            prompt,
        )
        self.assertIn("ni remplacer un caractère par un autre", prompt)
        self.assertIn("le premier caractère de la réponse est le `#`", prompt)
        self.assertIn("N’explique jamais l’assemblage", prompt)

    def test_renderer_accepts_a_direct_packet_and_scopes_url_duplicates(self):
        prompt = (PROJECT / "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md").read_text(
            encoding="utf-8"
        )
        prompt = " ".join(prompt.split())

        self.assertIn("Traite directement tout bloc valide", prompt)
        self.assertIn("`PAQUET_RENDU_PRET` atteste tous les contrôles Collecte", prompt)
        self.assertIn("vérifie seulement que le JSON", prompt)
        self.assertIn(
            "ne revalide ni URL, dates, espaces, champs, mots-clés, essentiels ni contenus",
            prompt,
        )
        self.assertIn("Utilise chaque valeur littéralement", prompt)
        self.assertIn("`@@...@@` des canons sont des emplacements attendus", prompt)
        self.assertIn("`CANON_MANQUANT` = ressource ou bloc", prompt)
        self.assertIn("Charge séparément, une par une", prompt)
        self.assertIn("`SNUM_CANON_V519_*_START` et `SNUM_CANON_V519_*_END`", prompt)
        self.assertIn("lecture est fragmentaire", prompt)
        self.assertIn("`@@ID_RUBRIQUE@@` reçoit la valeur brute de `rubric`", prompt)
        self.assertIn("jamais un slug du titre", prompt)
        self.assertIn("Le tag emploie toujours le titre/tag", prompt)
        self.assertIn("`NUMERIQUE` reste sans accent", prompt)

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
                    f"{collecte_folder}/01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md",
                    f"{collecte_folder}/02-METHODE-COLLECTE-SNUM-V5.24.md",
                    f"{collecte_folder}/03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md",
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
        notice = (PROJECT / "NOTICE-V5.24.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
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
        self.assertGreaterEqual(notice.count("PHASE RENDRE_EDITION."), 1)
        self.assertIn("Collez directement tout le bloc copié par Collecte", notice)
        self.assertIn("ne revalide ni les URL ni les dates", " ".join(notice.split()))
        self.assertIn("02-METHODE-COLLECTE-SNUM-V5.24.md", notice)
        self.assertIn("03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md", notice)
        self.assertIn("téléversez les quatre ressources `CANON-HTML-", notice)
        self.assertIn("cliquez sur **Copier le code**", notice)
        self.assertIn("marqueurs inclus", " ".join(notice.split()))
        self.assertIn("A_COMPLETER", notice)
        self.assertIn("Newsletter SNUM - Collecte.zip", notice)
        self.assertIn("Newsletter SNUM - Rendu HTML.zip", notice)
        self.assertIn("GO pour Collecte → JSON → Rendu HTML", notice)
        self.assertIn("## Démarrage express dans une nouvelle conversation", notice)
        self.assertIn("Web désactivé", notice)
        self.assertIn("Web activé uniquement pendant les cinq recherches", notice)
        self.assertIn(
            "envoyez `VALIDER`, puis `GENERER_PAQUET`", " ".join(notice.split())
        )
        self.assertIn(
            "`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `\"`→`&quot;`, `'`→`&#x27;`",
            notice,
        )

    def test_readme_is_the_pedagogical_active_entry_point(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        collecte = (
            (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md")
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
        self.assertIn("GO pour Collecte → JSON → Rendu HTML", readme)
        self.assertIn("## Démarrage express dans une nouvelle conversation", readme)
        self.assertIn("Web désactivé", readme)
        self.assertIn("Web activé uniquement pendant les cinq recherches", readme)
        self.assertIn("Collez directement tout le bloc copié par Collecte", readme)
        self.assertIn("ne revalide ni les URL ni les dates", " ".join(readme.split()))
        self.assertIn(
            "envoyez `VALIDER`, puis `GENERER_PAQUET`", " ".join(readme.split())
        )
        self.assertIn(
            "`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `\"`→`&quot;`, `'`→`&#x27;`",
            readme,
        )
        self.assertNotIn("kit-dinum-snum-v5-19-deux-projets-6-fichiers.zip", readme)
        self.assertNotIn("guide V5.17", readme)


if __name__ == "__main__":
    unittest.main()
