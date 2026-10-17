import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


class CollecteV524Tests(unittest.TestCase):
    def test_empty_web_result_advances_instead_of_looping(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )

        for text in (prompt, method):
            self.assertIn("`RESULTATS_RECHERCHE=AUCUNE_SOURCE_PROUVEE`", text)
            self.assertIn("`RECHERCHE_SANS_SOURCE_PROUVEE | <rubrique>`", text)
            self.assertIn("registre inchangé", text)
            self.assertNotIn("A_COMPLETER | RECHERCHE_NON_PROUVEE", text)
            self.assertNotIn("relance exactement la même requête", text)

        self.assertIn(
            "affiche exactement la requête suivante de l’ordre immuable",
            prompt,
        )

    def test_empty_registry_still_reaches_the_json_packet(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Registre vide admis", prompt)
        self.assertIn("Un registre vide reste valide", method)
        self.assertIn("`VALIDATION_TERMINEE`", method)
        self.assertIn("`articles=[]`", method)
        self.assertIn("`watch`", method)

    def test_every_search_response_must_expose_the_next_request(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "aucune réponse de recherche ne se termine avant elle",
            prompt,
        )

        for transition in (
            "`RECHERCHE_NUMERIQUE→RECHERCHE_IA`",
            "`RECHERCHE_IA→RECHERCHE_COMMANDE`",
            "`RECHERCHE_COMMANDE→RECHERCHE_RH`",
            "`RECHERCHE_RH→RECHERCHE_BERCY`",
            "`RECHERCHE_BERCY→VALIDER`",
        ):
            self.assertIn(transition, prompt)

    def test_packet_is_normalized_without_a_correction_turn(self):
        prompt = (PROJECT / "01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        method = (PROJECT / "02-METHODE-COLLECTE-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )
        contract = (PROJECT / "03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md").read_text(
            encoding="utf-8"
        )

        for text in (prompt, method):
            normalized = " ".join(text.split())
            self.assertIn("une seule source valide par rubrique", normalized)
            self.assertIn(
                "date ISO la plus récente, puis le plus petit `Uxx`", normalized
            )

        prompt = " ".join(prompt.split())
        contract = " ".join(contract.split())
        self.assertIn("renumérote les articles `U01…UN`", prompt)
        self.assertIn("exactement trois ont `essential=true`", prompt)
        self.assertIn("N’écris aucun brouillon ni JSON avant ces marqueurs", prompt)
        self.assertIn("Une rubrique apparaît au plus une fois", contract)
        self.assertIn("ordre `numerique`, `ia`, `commande`, `rh`, `bercy`", contract)


if __name__ == "__main__":
    unittest.main()
