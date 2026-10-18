import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def text(name):
    return (PROJECT / name).read_text(encoding="utf-8")


def normalized(name):
    return " ".join(text(name).split())


class StabilisationV523PreflightTests(unittest.TestCase):
    def test_collecte_runs_web_and_emits_packet_in_the_initial_turn(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("Lance immédiatement une recherche Web composite", content)
            self.assertIn("produis le paquet dans cette même réponse", content)
            self.assertIn("N’affiche jamais de requête à recopier", content)
            self.assertNotIn("REQUETE_COMPOSITE_A_COPIER", content)
            self.assertNotIn("NORMALISER_V519", content)
        self.assertNotIn("N’utilise jamais le Web dans ce Projet", prompt)

    def test_initial_message_requires_only_the_two_dates(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")

        self.assertIn(
            "`DATE_EDITION = <date en français>` "
            "`PERIODE = du <date en français> au <date en français> inclus`",
            prompt,
        )
        self.assertIn("Valide seulement avec ces deux lignes", prompt)
        self.assertNotIn("`RECHERCHE_COMPOSITE`", prompt)

    def test_composite_search_covers_the_five_rubrics(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for rubric in ("numerique", "ia", "commande", "rh", "bercy"):
            self.assertIn(f"`{rubric}`", prompt)
            self.assertIn(rubric, method)
        self.assertIn("date de publication exacte", prompt)
        self.assertIn("date d’événement, d’échéance ou de mise à jour", prompt)
        for content in (prompt, method):
            self.assertIn("Ouvre", content)
            self.assertIn("URL canonique", content)

    def test_web_results_are_normalized_inside_collecte(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("URL canonique", content)
            self.assertIn("Déduplique", content)
            self.assertNotIn("RESULTAT|", content)
        self.assertIn("`DEBUT_ISO <= date_iso <= FIN_ISO`", prompt)
        self.assertIn("N’invente jamais une source, une date ou un fait", prompt)

    def test_window_boundaries_are_inclusive_and_explicit(self):
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for included in ("2026-10-11", "2026-10-17"):
            self.assertIn(included, method)
        for excluded in ("2026-10-10", "2026-10-18"):
            self.assertIn(excluded, method)

    def test_no_intermediate_user_action_is_required(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertNotIn("RESULTATS_COMPOSITES_ENREGISTRES", content)
            self.assertNotIn("NORMALISER_V519", content)
            self.assertNotIn("REQUETE_A_ENVOYER", content)
            self.assertNotIn("`VALIDER`", content)
            self.assertNotIn("`GENERER_PAQUET`", content)
            self.assertNotIn("`RECOMPTER`", content)
            self.assertNotIn("`CONTINUER`", content)

    def test_initial_turn_emits_one_strict_v519_packet(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("`SNUM_PAQUET_RENDU_V519_START`", content)
            self.assertIn("`SNUM_PAQUET_RENDU_V519_END`", content)
            self.assertIn("`PAQUET_RENDU_PRET`", content)
        self.assertIn(
            "`SNUM_PAQUET_RENDU_V519_START`→JSON unique→ "
            "`SNUM_PAQUET_RENDU_V519_END`→`PAQUET_RENDU_PRET`",
            prompt,
        )
        self.assertIn("Première ligne visible : START", prompt)
        self.assertIn("sans bloc de code, raisonnement", prompt)
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

    def test_packet_dates_use_strict_iso_and_long_formats(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")

        self.assertIn(
            "`edition_date`, `window_start` et `window_end` suivent `AAAA-MM-JJ`",
            prompt,
        )
        self.assertIn(
            "`edition_date_long` et `publication_date_long` utilisent le mois en "
            "lettres, sans jour de semaine",
            prompt,
        )

    def test_packet_selection_is_deterministic_and_best_effort(self):
        prompt = normalized("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md")
        method = normalized("02-METHODE-COLLECTE-SNUM-V5.23.md")

        for content in (prompt, method):
            self.assertIn("date décroissante", content)
            self.assertIn("`U01…UN` sans trou", content)
            self.assertIn("exactement les trois premiers", content)
            self.assertIn("moins de cinq", content.lower())
            self.assertIn("`watch`", content)
            self.assertIn("`articles=[]`", content)
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

        self.assertIn(
            "exécute `RENDRE_EDITION` sans Web ni réécriture, en silence", prompt
        )
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

    def test_html_renderer_accepts_an_empty_best_effort_packet(self):
        prompt = normalized("20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md")

        self.assertIn("`articles=[]` valide", prompt)
        self.assertIn("rends `VIDE`, puis `SURVEILLER` si `watch`", prompt)
        self.assertIn(
            '`@@NAVIGATION@@` vaut exactement `<a class="fr-link" '
            'href="#surveiller">À surveiller</a>',
            prompt,
        )
        self.assertIn("Jamais `DONNEES_MANQUANTES`", prompt)
        self.assertIn("ou `ESSENTIELS_INCORRECTS`", prompt)

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
