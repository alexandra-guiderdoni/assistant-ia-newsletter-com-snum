import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def text(name):
    return (PROJECT / name).read_text(encoding="utf-8")


def normalized(name):
    return " ".join(text(name).split())


class StabilisationV523PreflightTests(unittest.TestCase):
    def test_initial_message_prepares_one_composite_web_query(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")

        self.assertIn(
            "`DATE_EDITION = <date en français>` "
            "`PERIODE = du <date en français> au <date en français> inclus` "
            "`RECHERCHE_COMPOSITE`",
            prompt,
        )
        self.assertIn("`REQUETE_COMPOSITE_A_COPIER_START`", prompt)
        self.assertIn("`REQUETE_COMPOSITE_A_COPIER_END`", prompt)
        self.assertIn("une seule recherche Web dans un nouveau chat", prompt)
        self.assertIn("N’utilise jamais le Web dans ce Projet", prompt)

    def test_composite_query_covers_the_five_rubrics(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for rubric in ("numerique", "ia", "commande", "rh", "bercy"):
            self.assertIn(f"`{rubric}`", prompt)
            self.assertIn(rubric, method)
        self.assertIn(
            "`RESULTAT|rubrique|URL_HTTPS|date_iso|titre|source|fait_factuel`",
            prompt,
        )
        self.assertIn(
            "`RESULTAT|rubrique|AUCUN_RESULTAT_DATE_DANS_FENETRE`",
            prompt,
        )
        self.assertIn("date de publication exacte", prompt)
        self.assertIn("date d’événement, d’échéance ou de mise à jour", prompt)
        for content in (prompt, method):
            self.assertIn(
                "Une liste de codes sans ces axes est invalide",
                content,
            )
            self.assertIn(
                "Dans chaque ligne `RESULTAT`, `rubrique` vaut uniquement le code",
                content,
            )
            self.assertIn(
                "jamais le libellé ni l’axe",
                content,
            )

    def test_composite_result_fields_cannot_contain_the_separator(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn(
                "Aucun champ ne contient le caractère `|` ni de retour à la ligne",
                content,
            )

    def test_pasted_web_response_is_normalized_without_a_new_search(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("sept champs", content)
            self.assertIn("URL canonique", content)
            self.assertIn("ignore `AUCUN_RESULTAT_DATE_DANS_FENETRE`", content)
            self.assertIn("ligne valide", content)
        self.assertIn("Ignore préambule, séparateurs, citations isolées", prompt)
        self.assertIn("`DEBUT_ISO <= date_iso <= FIN_ISO`", prompt)
        self.assertIn("Le Projet Collecte n’appelle aucun outil Web", method)

    def test_window_boundaries_are_inclusive_and_explicit(self):
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for included in ("2026-10-03", "2026-10-04", "2026-10-11", "2026-10-13"):
            self.assertIn(f"`{included}`", method)
        for excluded in ("2026-10-02", "2026-10-14"):
            self.assertIn(f"`{excluded}`", method)

    def test_pasted_results_are_stored_before_packet_generation(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("`RESULTATS_COMPOSITES_ENREGISTRES`", content)
            self.assertIn("`REQUETE_A_ENVOYER=NORMALISER_V519`", content)
            self.assertIn("ne produis aucun JSON", content)
            self.assertNotIn("`VALIDER`", content)
            self.assertNotIn("`GENERER_PAQUET`", content)
            self.assertNotIn("`RECOMPTER`", content)

    def test_normalize_command_emits_one_strict_v519_packet(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("`NORMALISER_V519`", content)
            self.assertIn("`SOURCES_NORMALISEES`", content)
            self.assertIn("seulement après", content)
        self.assertIn(
            "`SNUM_PAQUET_RENDU_V519_START`→JSON unique→ "
            "`SNUM_PAQUET_RENDU_V519_END`→`PAQUET_RENDU_PRET`",
            prompt,
        )
        self.assertIn("Première ligne visible : START", prompt)
        self.assertIn("sans bloc de code, brouillon, préambule ou doublon", prompt)
        self.assertIn(
            "RACINE=`schema_version,edition_date,edition_date_long,window_start,"
            "window_end,articles,watch`",
            prompt,
        )
        self.assertIn(
            "ARTICLE=`id,rubric,title,source,publication_date_iso,"
            "publication_date_long,url,fact,keywords,takeaway,snum_interest,essential`",
            prompt,
        )
        self.assertIn("jamais un objet indexé par `Uxx`", prompt)

    def test_packet_selection_is_deterministic_and_best_effort(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("date décroissante", content)
            self.assertIn("`U01…UN` sans trou", content)
            self.assertIn("exactement les trois premiers", content)
            self.assertIn("Moins de cinq", content)
            self.assertIn("`watch`", content)
        self.assertIn("Le nombre d’articles égale le nombre d’URL uniques", method)

    def test_packet_contract_has_one_strict_schema(self):
        contract = normalized("03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md")

        self.assertIn(
            "`SORTIE_PAQUET=START→JSON_UNIQUE→END→PAQUET_RENDU_PRET`",
            contract,
        )
        self.assertIn("`id` vaut exactement `U01…UN` sans trou", contract)
        self.assertIn("`keywords` contient 3 à 5 chaînes", contract)
        self.assertIn("Une URL ne peut apparaître qu’une fois", contract)
        self.assertIn("Première ligne visible : START", contract)
        self.assertIn("sans bloc de code", contract)

    def test_html_renderer_enforces_a_silent_first_line_contract(self):
        prompt = normalized("20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")

        self.assertIn("Prépare, charge, assemble et valide en silence", prompt)
        self.assertIn(
            "Première ligne visible en réussite : `## HTML COMPLET` ; "
            "en échec : `A_COMPLETER`",
            prompt,
        )
        self.assertIn(
            "N’affiche jamais plan, étapes, raisonnement ou contrôle intermédiaire",
            prompt,
        )
        self.assertIn(
            "`@@DATE_EDITION@@` reçoit exactement `edition_date_long`",
            prompt,
        )

    def test_assistant_file_limits_are_respected(self):
        self.assertLessEqual(
            len(text("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")), 4000
        )
        self.assertLessEqual(
            len(text("20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")), 4000
        )
        for name in (
            "02-METHODE-COLLECTE-SNUM-V5.23.md",
            "03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md",
        ):
            self.assertLessEqual(len(text(name)), 4500, name)


if __name__ == "__main__":
    unittest.main()
