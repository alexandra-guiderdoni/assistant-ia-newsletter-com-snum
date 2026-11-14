"""Repêchage d'un candidat écarté par une tâche GitHub Actions : aucun appel réseau réel."""

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

from test_veille_snum import FakeHttp, good_summary
from veille_snum.core import packet_for
from veille_snum.repecher import CHAMPS_ARTICLE, SCHEMA, main, repecher

TOKEN = "JETON-FACTICE-NE-PAS-PUBLIER"
URL = "https://www.numerique.gouv.fr/article/veille-snum"
DEBUT, FIN = dt.date(2026, 11, 1), dt.date(2026, 11, 10)
ALBERT = "https://albert.api.etalab.gouv.fr/v1/chat/completions"
TROP_LONG = {**good_summary(None), "fact": "mot " * 30}


class Resumeur:
    """Résumé factice : rejoue les réponses données, puis la bonne, et note chaque appel."""

    def __init__(self, *reponses):
        self.reponses = list(reponses)
        self.appels = []

    def __call__(self, candidat, feedback=None, forced_rubric=None):
        self.appels.append(
            {"candidat": candidat, "feedback": feedback, "forced_rubric": forced_rubric}
        )
        reponse = self.reponses.pop(0) if self.reponses else good_summary(candidat)
        if isinstance(reponse, Exception):
            raise reponse
        return reponse


def erreur_http(code, entetes=None):
    return HTTPError(ALBERT, code, f"refus {TOKEN}", entetes or {}, None)


class RepechageTests(unittest.TestCase):
    def lancer(self, url=URL, rubrique="administration", client=None, resumer=None, **dates):
        self.client = client or FakeHttp()
        self.resumer = resumer or Resumeur()
        return repecher(
            url,
            rubrique,
            dates.get("debut", DEBUT),
            dates.get("fin", FIN),
            self.client,
            self.resumer,
        )

    def refus(self, attendu, **options):
        resultat = self.lancer(**options)
        self.assertEqual(resultat["schema_version"], SCHEMA)
        self.assertEqual(resultat["status"], "erreur")
        self.assertIsNone(resultat["article"])
        self.assertIn(attendu, resultat["message"])
        self.assertNotIn(TOKEN, json.dumps(resultat, ensure_ascii=False))
        return resultat

    def test_cas_nominal(self):
        resultat = self.lancer()
        self.assertEqual(
            set(resultat), {"schema_version", "url", "status", "message", "article"}
        )
        self.assertEqual(resultat["schema_version"], "SNUM_REPECHAGE_V1")
        self.assertEqual(resultat["status"], "ok")
        self.assertEqual(resultat["url"], URL)
        article = resultat["article"]
        self.assertEqual(
            list(article),
            [
                "rubric",
                "title",
                "source",
                "publication_date_iso",
                "publication_date_long",
                "url",
                "fact",
                "keywords",
                "takeaway",
                "snum_interest",
            ],
        )
        self.assertEqual(list(article), list(CHAMPS_ARTICLE))
        self.assertEqual(article["source"], "DINUM")
        self.assertEqual(
            article["title"], "Un article de veille SNUM et services numériques"
        )
        self.assertEqual(article["publication_date_iso"], "2026-11-06")
        self.assertEqual(article["publication_date_long"], "6 novembre 2026")
        self.assertEqual(article["url"], URL)
        # Le candidat transmis à Albert est celui de la collecte : extrait borné, rien d'autre.
        candidat = self.resumer.appels[0]["candidat"]
        self.assertEqual(
            set(candidat), {"title", "source", "publication_date_iso", "url", "content"}
        )
        self.assertLessEqual(len(candidat["content"]), 2400)

    def test_article_accepte_par_le_contrat_v519(self):
        article = self.lancer()["article"]
        paquet = packet_for(dt.date(2026, 11, 11), DEBUT, FIN, [article], [])
        self.assertEqual(
            paquet["articles"], [{"id": "U01", **article, "essential": False}]
        )

    def test_rubrique_forcee_transmise_et_imposee(self):
        # Albert répond « numerique » : la rubrique choisie par l'éditeur prime.
        resultat = self.lancer(rubrique="ia")
        self.assertEqual(self.resumer.appels[0]["forced_rubric"], "ia")
        self.assertEqual(resultat["status"], "ok")
        self.assertEqual(resultat["article"]["rubric"], "ia")

    def test_parametres_de_suivi_retires_de_l_adresse(self):
        resultat = self.lancer(url=URL + "?utm_source=lettre")
        self.assertEqual(resultat["status"], "ok")
        self.assertEqual(resultat["article"]["url"], URL)

    def test_url_hors_sources_ou_non_https(self):
        for url in (
            "http://www.numerique.gouv.fr/article/veille-snum",
            "https://exemple.test/article/veille-snum",
            "https://numerique.gouv.fr.exemple.test/article/veille-snum",
            "https://numerique.gouv.fr:8080/article/veille-snum",
            "",
            None,
        ):
            with self.subTest(url=url):
                self.refus("URL", url=url)
                self.assertEqual(self.client.calls, [])
                self.assertEqual(self.resumer.appels, [])

    def test_rubrique_inconnue(self):
        for rubrique in ("sport", "", None, ["ia"]):
            with self.subTest(rubrique=rubrique):
                self.refus("Rubrique", rubrique=rubrique)
                self.assertEqual(self.client.calls, [])
                self.assertEqual(self.resumer.appels, [])

    def test_date_hors_periode(self):
        self.refus("hors de la période", client=FakeHttp(publication="2026-10-01"))
        self.assertEqual(self.resumer.appels, [])

    def test_date_de_publication_absente(self):
        self.refus("Date de publication absente", client=FakeHttp(page_kind="modified"))
        self.assertEqual(self.resumer.appels, [])

    def test_periode_inversee(self):
        self.refus("Période", debut=FIN, fin=DEBUT)
        self.assertEqual(self.client.calls, [])

    def test_page_illisible_sans_detail(self):
        class Panne(FakeHttp):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if url.endswith("/robots.txt"):
                    return super().get(url, domain)
                raise HTTPError(url, 404, "Not Found", {}, None)

        self.refus("Page illisible : HTTP 404", client=Panne())
        self.assertEqual(self.resumer.appels, [])

    def test_reponse_rejetee_puis_acceptee(self):
        resultat = self.lancer(resumer=Resumeur(TROP_LONG))
        self.assertEqual(resultat["status"], "ok")
        self.assertEqual(
            [a["feedback"] for a in self.resumer.appels], [None, "CHAMP_INVALIDE:fact"]
        )
        self.assertEqual(
            [a["forced_rubric"] for a in self.resumer.appels], ["administration"] * 2
        )

    def test_deux_rejets(self):
        self.refus("CHAMP_INVALIDE:fact", resumer=Resumeur(TROP_LONG, TROP_LONG))
        self.assertEqual(len(self.resumer.appels), 2)

    def test_reponse_qui_n_est_pas_un_objet(self):
        self.refus("SORTIE_ALBERT_INVALIDE", resumer=Resumeur([], "texte"))
        self.assertEqual(len(self.resumer.appels), 2)

    def test_erreur_http_albert_sans_fuite_du_jeton(self):
        resultat = self.refus("Albert : HTTP 401", resumer=Resumeur(erreur_http(401)))
        self.assertEqual(resultat["message"], "Albert : HTTP 401")
        self.assertEqual(len(self.resumer.appels), 1)

    def test_exception_portant_le_jeton_reduite_a_son_type(self):
        fuite = ValueError(f"Invalid header value b'Bearer {TOKEN}'")
        resultat = self.refus("Albert : ValueError", resumer=Resumeur(fuite, fuite))
        self.assertEqual(resultat["message"], "Albert : ValueError")
        self.assertEqual(self.resumer.appels[1]["feedback"], "ValueError")

    def test_albert_sature_puis_disponible(self):
        sature = erreur_http(429, {"Retry-After": "3"})
        with mock.patch("veille_snum.repecher.time.sleep") as pause:
            resultat = self.lancer(resumer=Resumeur(sature))
        self.assertEqual(resultat["status"], "ok")
        pause.assert_called_once_with(3.0)


class LigneDeCommandeTests(unittest.TestCase):
    def setUp(self):
        self.sortie = Path(tempfile.mkdtemp()) / "resultats" / "repechage.json"

    def executer(
        self, albert, *, url=URL, debut="01/11/2026", fin="2026-11-10", cle=TOKEN
    ):
        environnement = {"ALBERT_API_KEY": cle, "ALBERT_MODEL": "modele-test"}
        arguments = [
            f"--url={url}",
            "--rubrique",
            "ia",
            "--debut",
            debut,
            "--fin",
            fin,
            "--sortie",
            str(self.sortie),
        ]
        with (
            mock.patch.dict("os.environ", environnement),
            mock.patch("veille_snum.repecher.HttpClient", return_value=FakeHttp()),
            mock.patch(
                "veille_snum.repecher.albert_summary", side_effect=albert
            ) as appel,
            mock.patch("sys.stdout"),
        ):
            code = main(arguments)
        self.appel = appel
        self.texte = self.sortie.read_text(encoding="utf-8")
        self.assertNotIn(TOKEN, self.texte)
        return code, json.loads(self.texte)

    def test_fichier_ecrit_sans_le_jeton(self):
        code, resultat = self.executer(lambda candidat, *a, **k: good_summary(candidat))
        self.assertEqual(code, 0)
        self.assertEqual(resultat["status"], "ok")
        self.assertEqual(resultat["article"]["rubric"], "ia")
        self.assertEqual(self.appel.call_args.args[1:3], (TOKEN, "modele-test"))
        self.assertEqual(self.appel.call_args.kwargs["forced_rubric"], "ia")
        self.assertTrue(self.texte.endswith("\n"))

    def test_echec_albert_fichier_ecrit_et_code_un(self):
        def refuse(*args, **kwargs):
            raise erreur_http(401)

        code, resultat = self.executer(refuse)
        self.assertEqual(code, 1)
        self.assertEqual(resultat["status"], "erreur")
        self.assertEqual(resultat["message"], "Albert : HTTP 401")
        self.assertIsNone(resultat["article"])

    def test_sans_jeton_aucun_appel(self):
        code, resultat = self.executer(
            AssertionError("Albert appelé sans jeton"), cle=""
        )
        self.assertEqual(code, 1)
        self.assertIn("Albert non configuré", resultat["message"])
        self.appel.assert_not_called()

    def test_date_invalide_fichier_ecrit_et_code_un(self):
        code, resultat = self.executer(
            AssertionError("Albert appelé"), debut="31/02/2026"
        )
        self.assertEqual(code, 1)
        self.assertEqual(resultat["status"], "erreur")
        self.assertIn("date invalide", resultat["message"])
        self.assertEqual(resultat["url"], URL)
        self.appel.assert_not_called()


if __name__ == "__main__":
    unittest.main()
