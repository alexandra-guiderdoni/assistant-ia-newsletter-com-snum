import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def normalized(name):
    return " ".join((PROJECT / name).read_text(encoding="utf-8").split())


class StabilisationV523PreflightTests(unittest.TestCase):
    def test_b01_bercy_exposes_validation_as_the_next_input(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")
        direct_route = (
            "`RECHERCHE_NUMERIQUE`→`RECHERCHE_IA`→`RECHERCHE_COMMANDE`→"
            "`RECHERCHE_RH`→`RECHERCHE_BERCY`→`VALIDER`"
        )

        for text in (prompt, method):
            self.assertIn(direct_route, text)
            self.assertIn("`RECHERCHE_BERCY`→`VALIDER`", text)
            self.assertIn(
                "`COLLECTE_TERMINEE_BEST_EFFORT` est un marqueur d’état, "
                "jamais une valeur de `REQUETE_A_ENVOYER`",
                text,
            )
            self.assertNotIn(
                "`REQUETE_A_ENVOYER=COLLECTE_TERMINEE_BEST_EFFORT`",
                text,
            )

    def test_window_boundaries_are_explicit_on_both_sides(self):
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        self.assertIn("`2026-10-02` vaut `NON`", method)
        self.assertIn("`2026-10-03` et `2026-10-13` valent `OUI`", method)
        self.assertIn("`2026-10-16` vaut `NON`", method)

    def test_nonempty_results_advance_from_the_received_code_only(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for text in (prompt, method):
            self.assertIn(
                "prends le code reçu dans le message utilisateur et affiche son "
                "suivant dans la chaîne",
                text,
            )
            self.assertIn("ne répète jamais le code reçu", text)

    def test_validation_emits_one_control_line_per_registry_entry(self):
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        self.assertIn(
            "`CONTROLE_DATES` contient exactement une ligne `Uxx` par entrée du "
            "registre",
            method,
        )
        self.assertIn("jamais seulement les bornes agrégées", method)

    def test_b02_packet_has_one_unambiguous_output_grammar(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        contract = normalized("03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md")
        grammar = (
            "`SORTIE_PAQUET=START→JSON_UNIQUE→END→PAQUET_RENDU_PRET`; "
            "unique, rien avant START."
        )

        self.assertIn(grammar, prompt)
        self.assertIn(grammar, contract)
        for text in (prompt, contract):
            self.assertIn("Avant de répondre, valide en silence", text)
            self.assertIn("aucun brouillon, préambule ou doublon", text)
            self.assertIn("sans bloc de code", text)

    def test_packet_normalizes_lengths_and_watch_before_output(self):
        contract = normalized("03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md")

        self.assertIn("raccourcis les trois textes avant la validation", contract)
        self.assertIn("`watch=[]` s’il n’y a aucune alerte", contract)
        self.assertIn("jamais une chaîne", contract)

    def test_b03_packet_is_normalized_after_final_selection(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")
        contract = normalized("03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md")

        for text in (prompt, method):
            self.assertIn(
                "Sélection finale : trie puis renumérote les articles "
                "`U01…UN` sans trou",
                text,
            )
        self.assertIn("`id` vaut exactement `U01…UN` sans trou", contract)
        self.assertIn("`keywords` contient 3 à 5 chaînes", contract)
        self.assertIn(
            "`fact` contient au plus 25 mots ; `takeaway` et "
            "`snum_interest` au plus 15 mots",
            contract,
        )

    def test_b04_html_title_uses_the_long_edition_date(self):
        prompt = normalized("20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")

        self.assertIn(
            "`@@DATE_EDITION@@` reçoit exactement `edition_date_long`, "
            "jamais `edition_date` ni une date avec barre oblique",
            prompt,
        )


if __name__ == "__main__":
    unittest.main()
