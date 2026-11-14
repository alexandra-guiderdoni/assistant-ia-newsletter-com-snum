"""Repêchage sans thématique choisie : Albert garde l'article et choisit la rubrique la plus proche."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_v11_repechage import DEBUT, FIN, URL, Resumeur
from test_veille_snum import FakeHttp, good_summary

from veille_snum import core
from veille_snum.repecher import ALBERT_CHOISIT, main, repecher


class AlbertChoisitTests(unittest.TestCase):
    def lancer(self, rubrique, resumer):
        return repecher(URL, rubrique, DEBUT, FIN, FakeHttp(), resumer)

    def test_albert_choisit_la_rubrique(self):
        resumer = Resumeur({**good_summary(None), "rubric": "securite"})
        resultat = self.lancer(ALBERT_CHOISIT, resumer)
        self.assertEqual(resultat["status"], "ok")
        self.assertEqual(resultat["article"]["rubric"], "securite")
        self.assertIsNone(resumer.appels[0]["forced_rubric"])
        self.assertTrue(resumer.appels[0]["keep"])
        self.assertIn("securite", resultat["message"])

    def test_rubrique_inconnue_d_albert_rejetee_puis_reprise(self):
        resumer = Resumeur({**good_summary(None), "rubric": "sport"})
        resultat = self.lancer(ALBERT_CHOISIT, resumer)
        self.assertEqual(len(resumer.appels), 2)
        self.assertIsNotNone(resumer.appels[1]["feedback"])
        self.assertEqual(resultat["article"]["rubric"], "administration")

    def test_albert_juge_hors_sujet_malgre_la_consigne(self):
        resumer = Resumeur({"relevant": False}, {"relevant": False})
        resultat = self.lancer(ALBERT_CHOISIT, resumer)
        self.assertEqual(resultat["status"], "erreur")
        self.assertIsNone(resultat["article"])

    def test_rubrique_vide_toujours_refusee(self):
        resultat = self.lancer("", Resumeur())
        self.assertEqual(resultat["status"], "erreur")
        self.assertIn("Rubrique", resultat["message"])


class LigneDeCommandeTests(unittest.TestCase):
    def test_albert_choisit_transmis_avec_la_consigne_de_garder(self):
        sortie = Path(tempfile.mkdtemp()) / "repechage.json"
        arguments = [
            f"--url={URL}",
            "--rubrique",
            ALBERT_CHOISIT,
            "--debut",
            "01/11/2026",
            "--fin",
            "2026-11-10",
            "--sortie",
            str(sortie),
        ]
        environnement = {
            "ALBERT_API_KEY": "JETON-FACTICE",
            "ALBERT_MODEL": "modele-test",
        }
        with (
            mock.patch.dict("os.environ", environnement),
            mock.patch("veille_snum.repecher.HttpClient", return_value=FakeHttp()),
            mock.patch(
                "veille_snum.repecher.albert_summary",
                side_effect=lambda c, *a, **k: {**good_summary(c), "rubric": "droit"},
            ) as appel,
            mock.patch("sys.stdout"),
        ):
            code = main(arguments)
        self.assertEqual(code, 0)
        self.assertIsNone(appel.call_args.kwargs["forced_rubric"])
        self.assertTrue(appel.call_args.kwargs["keep"])
        self.assertEqual(
            json.loads(sortie.read_text(encoding="utf-8"))["article"]["rubric"], "droit"
        )


class ConsigneAlbertTests(unittest.TestCase):
    def messages(self, **options):
        corps = {}

        class Reponse:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self, _taille):
                contenu = json.dumps(good_summary(None), ensure_ascii=False)
                return json.dumps(
                    {"choices": [{"message": {"content": contenu}}]}
                ).encode()

        class Ouvreur:
            def open(self, requete, timeout):
                corps.update(json.loads(requete.data))
                return Reponse()

        with mock.patch("veille_snum.core.build_opener", return_value=Ouvreur()):
            core.albert_summary({"url": URL}, "cle", "modele", **options)
        return [m["content"] for m in corps["messages"][2:]]

    def test_garder_sans_rubrique_impose_relevant_et_laisse_choisir(self):
        consigne = " ".join(self.messages(keep=True))
        self.assertIn("relevant=true", consigne)
        self.assertIn("la plus proche", consigne)

    def test_rubrique_imposee_prime_sur_garder(self):
        consigne = " ".join(self.messages(keep=True, forced_rubric="ia"))
        self.assertIn("rubric=ia", consigne)
        self.assertNotIn("la plus proche", consigne)

    def test_collecte_ordinaire_sans_consigne_supplementaire(self):
        self.assertEqual(self.messages(), [])


if __name__ == "__main__":
    unittest.main()
