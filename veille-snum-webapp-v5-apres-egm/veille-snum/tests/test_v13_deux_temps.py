"""Collecte en deux temps : titres sans Albert, puis résumés des seuls titres gardés. Aucun appel réseau réel."""

import datetime as dt
import io
import json
import os
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

from test_veille_snum import FakeHttp, good_summary
from veille_snum import publier as module_publier
from veille_snum.core import collect, validate_packet_v519
from veille_snum.publier import rapport_public
from veille_snum.resumer import main, publier_resumes

TOKEN = "JETON-FACTICE-NE-PAS-PUBLIER"
ALBERT = "https://albert.api.etalab.gouv.fr/v1/chat/completions"
URL_RAPPORT = "https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/rapport-collecte.json"
PAYLOAD = {
    "edition_date": "2026-11-11",
    "window_start": "2026-11-01",
    "window_end": "2026-11-10",
}
ETAT, PAQUET, ECARTES, RAPPORT = (
    "etat-collecte.json",
    "paquet-v519.json",
    "candidats-ecartes.json",
    "rapport-collecte.json",
)
DATES = ["--edition", "11/11/2026", "--debut", "01/11/2026", "--fin", "2026-11-10"]
ENVIRONNEMENT = {"ALBERT_API_KEY": TOKEN, "ALBERT_MODEL": "modele-test"}


def lire(dossier, nom):
    return json.loads((Path(dossier) / nom).read_text(encoding="utf-8"))


def fichiers(dossier):
    return sorted(p.name for p in Path(dossier).iterdir())


class Reseau(FakeHttp):
    """Remplace la classe HttpClient de la collecte, qui lui transmet son échéance."""

    def get(self, url, domain, max_bytes=600_000, timeout=7, deadline=None):
        return super().get(url, domain, max_bytes, timeout)


class HorsLigne(FakeHttp):
    """Aucune source ne répond."""

    def get(self, url, domain, max_bytes=600_000, timeout=7, deadline=None):
        raise HTTPError(url, 503, "Service Unavailable", {}, None)


class TitresTests(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp()) / "site"

    def titres(self, client):
        """Premier temps par la ligne de commande, jeton présent dans l'environnement."""
        with (
            mock.patch.dict("os.environ", ENVIRONNEMENT),
            mock.patch("veille_snum.core.HttpClient", new=client),
            mock.patch(
                "veille_snum.core.albert_summary",
                side_effect=AssertionError(
                    "Albert appelé pendant la collecte des titres"
                ),
            ) as albert,
            mock.patch("sys.stdout"),
            mock.patch("sys.stderr"),
        ):
            code = module_publier.main(
                [
                    "--mode",
                    "titres",
                    *DATES,
                    "--run-id",
                    "7",
                    "--sortie",
                    str(self.dossier),
                ]
            )
            # Le jeton n'est écarté que le temps de la collecte.
            self.assertEqual(os.environ["ALBERT_API_KEY"], TOKEN)
        self.albert = albert
        return code

    def test_etat_et_rapport_publies_sans_paquet_ni_ecartes(self):
        self.assertEqual(self.titres(Reseau), 0)
        self.assertEqual(fichiers(self.dossier), [ETAT, RAPPORT])
        self.assertEqual(
            lire(self.dossier, ETAT),
            {
                "schema_version": "SNUM_ETAT_V1",
                "phase": "titres",
                "edition_date": "2026-11-11",
                "window_start": "2026-11-01",
                "window_end": "2026-11-10",
                "run_id": 7,
                "candidats": 13,
                "articles": 0,
            },
        )

    def test_aucun_appel_albert_malgre_un_jeton_present(self):
        self.titres(Reseau)
        self.albert.assert_not_called()
        rapport = lire(self.dossier, RAPPORT)
        self.assertEqual(rapport["status"], "needs_albert")
        self.assertEqual(rapport["errors"], [])

    def test_rapport_des_titres_sans_extrait_ni_listes_d_adresses(self):
        self.titres(Reseau)
        texte = (self.dossier / RAPPORT).read_text(encoding="utf-8")
        rapport = json.loads(texte)
        self.assertNotIn("packet", rapport)
        self.assertEqual(len(rapport["sources"]), 14)
        self.assertEqual(len(rapport["candidates"]), 13)
        for candidat in rapport["candidates"]:
            self.assertEqual(
                sorted(candidat), ["publication_date_iso", "source", "title", "url"]
            )
        for source in rapport["sources"]:
            self.assertNotIn("not_visited_urls", source)
            self.assertNotIn("sitemap_skipped_urls", source)
        self.assertNotIn(TOKEN, texte)
        self.assertNotIn(TOKEN, (self.dossier / ETAT).read_text(encoding="utf-8"))

    def test_aucune_source_lue_rien_n_est_ecrit(self):
        self.assertEqual(self.titres(HorsLigne), 1)
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))


class CollecteCompleteTests(unittest.TestCase):
    def test_mode_collecte_ecrit_aussi_l_etat(self):
        dossier = Path(tempfile.mkdtemp())

        def collecter(payload):
            return collect(payload, client=FakeHttp(), summarize=good_summary)

        with mock.patch("sys.stdout"):
            code = module_publier.publier(
                PAYLOAD, dossier, collecter=collecter, run_id=9
            )
        self.assertEqual(code, 0)
        self.assertEqual(fichiers(dossier), [ECARTES, ETAT, PAQUET, RAPPORT])
        etat = lire(dossier, ETAT)
        self.assertEqual(
            [etat["phase"], etat["run_id"], etat["candidats"], etat["articles"]],
            ["collecte", 9, 13, 13],
        )
        self.assertEqual(etat["edition_date"], "2026-11-11")

    def test_mode_collecte_par_defaut(self):
        with mock.patch("veille_snum.publier.publier", return_value=0) as appel:
            module_publier.main(["--sortie", "x", "--run-id", "5", *DATES])
        self.assertEqual(appel.call_args.args[0], PAYLOAD)
        self.assertEqual(appel.call_args.kwargs.get("run_id"), 5)


def rapport_des_titres():
    """Rapport publié par le premier temps : collecte factice sans Albert."""
    with mock.patch.dict("os.environ", {"ALBERT_API_KEY": "", "ALBERT_MODEL": ""}):
        return rapport_public(collect(PAYLOAD, client=FakeHttp()))


PREMIER = rapport_des_titres()
URLS = [c["url"] for c in PREMIER["candidates"]]


class Site(FakeHttp):
    """Les 13 sources factices, plus le rapport du premier temps sur le site en ligne."""

    def __init__(self, rapport=PREMIER, illisibles=()):
        super().__init__()
        self.rapport = rapport if isinstance(rapport, str) else json.dumps(rapport)
        self.illisibles = set(illisibles)

    def get(self, url, domain, max_bytes=600_000, timeout=7):
        if url == URL_RAPPORT:
            self.calls.append(url)
            return url, self.rapport
        if url in self.illisibles:
            raise HTTPError(url, 404, "Not Found", {}, None)
        return super().get(url, domain, max_bytes, timeout)


class Albert:
    """Albert factice : note chaque appel et le nombre d'appels simultanés."""

    def __init__(self, hors=(), pannes=(), erreur=None, duree=0):
        self.hors, self.pannes = set(hors), set(pannes)
        self.erreur = erreur or HTTPError(ALBERT, 401, f"refus {TOKEN}", {}, None)
        self.duree = duree
        self.appels = []
        self.en_cours = self.maximum = 0
        self.verrou = threading.Lock()

    def __call__(self, candidat, feedback=None, forced_rubric=None):
        with self.verrou:
            self.appels.append({"candidat": candidat, "forced_rubric": forced_rubric})
            self.en_cours += 1
            self.maximum = max(self.maximum, self.en_cours)
        try:
            time.sleep(self.duree)
            if candidat["url"] in self.pannes:
                raise self.erreur
            if candidat["url"] in self.hors:
                return {"relevant": False}
            return good_summary(candidat)
        finally:
            with self.verrou:
                self.en_cours -= 1

    def rubriques(self):
        return {a["candidat"]["url"]: a["forced_rubric"] for a in self.appels}


def selection(*choix):
    return json.dumps(
        [{"url": url, "rubrique": rubrique} for url, rubrique in choix],
        separators=(",", ":"),
    )


class ResumesTests(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp()) / "site"
        self.sortie_standard, self.sortie_erreur = io.StringIO(), io.StringIO()

    def lancer(self, texte, client=None, albert=None, **options):
        self.client = client or Site()
        self.albert = albert or Albert()
        with (
            mock.patch("sys.stdout", self.sortie_standard),
            mock.patch("sys.stderr", self.sortie_erreur),
        ):
            return publier_resumes(
                texte, self.dossier, self.client, self.albert, **options
            )

    def refus(self, texte, attendu, **options):
        self.assertEqual(self.lancer(texte, **options), 1)
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))
        self.assertEqual(self.albert.appels, [])
        self.assertIn(attendu, self.sortie_erreur.getvalue())

    def test_cas_nominal(self):
        choix = selection((URLS[0], "ia"), (URLS[1], ""), (URLS[2], ""))
        self.assertEqual(self.lancer(choix, run_id=8), 0)
        self.assertEqual(fichiers(self.dossier), [ECARTES, ETAT, PAQUET, RAPPORT])
        paquet = lire(self.dossier, PAQUET)
        self.assertEqual({a["url"] for a in paquet["articles"]}, set(URLS[:3]))
        self.assertEqual(
            lire(self.dossier, ETAT),
            {
                "schema_version": "SNUM_ETAT_V1",
                "phase": "resumes",
                "edition_date": "2026-11-11",
                "window_start": "2026-11-01",
                "window_end": "2026-11-10",
                "run_id": 8,
                "candidats": 13,
                "articles": 3,
            },
        )
        rapport = lire(self.dossier, RAPPORT)
        self.assertEqual(rapport["status"], "ready")
        self.assertNotIn("packet", rapport)
        self.assertEqual(len(rapport["candidates"]), 13)
        self.assertEqual(len(rapport["sources"]), 14)
        self.assertEqual(rapport["errors"], [])
        # Albert n'a reçu que les trois articles gardés.
        self.assertEqual(set(self.albert.rubriques()), set(URLS[:3]))

    def test_paquet_valide_v519(self):
        self.lancer(selection(*[(url, "") for url in URLS[:6]]))
        paquet = lire(self.dossier, PAQUET)
        self.assertTrue(validate_packet_v519(paquet))
        self.assertEqual(paquet["schema_version"], "SNUM_PAQUET_RENDU_V519")
        self.assertEqual(len(paquet["articles"]), 6)
        self.assertEqual(sum(a["essential"] for a in paquet["articles"]), 3)

    def test_rubrique_imposee_transmise_a_albert(self):
        # Albert répond « numerique » : la rubrique choisie par l'éditeur prime.
        self.lancer(selection((URLS[0], "ia"), (URLS[1], "bercy")))
        self.assertEqual(self.albert.rubriques(), {URLS[0]: "ia", URLS[1]: "bercy"})
        rubriques = {
            a["url"]: a["rubric"] for a in lire(self.dossier, PAQUET)["articles"]
        }
        self.assertEqual(rubriques, {URLS[0]: "ia", URLS[1]: "bercy"})

    def test_classement_libre_sans_rubrique(self):
        self.lancer(selection((URLS[0], "")))
        self.assertEqual(self.albert.rubriques(), {URLS[0]: None})
        self.assertEqual(
            lire(self.dossier, PAQUET)["articles"][0]["rubric"], "numerique"
        )

    def test_candidat_transmis_avec_son_extrait_borne(self):
        self.lancer(selection((URLS[0], "")))
        candidat = self.albert.appels[0]["candidat"]
        self.assertEqual(
            set(candidat), {"title", "source", "publication_date_iso", "url", "content"}
        )
        self.assertLessEqual(len(candidat["content"]), 2400)

    def test_hors_thematique_vers_les_ecartes(self):
        choix = selection((URLS[0], ""), (URLS[1], ""))
        self.assertEqual(self.lancer(choix, albert=Albert(hors=[URLS[1]])), 0)
        self.assertEqual(
            [a["url"] for a in lire(self.dossier, PAQUET)["articles"]], [URLS[0]]
        )
        motifs = {
            c["url"]: c["reason"] for c in lire(self.dossier, ECARTES)["candidates"]
        }
        self.assertEqual(motifs[URLS[1]], "HORS_THEMATIQUE")
        self.assertNotIn(URLS[0], motifs)

    def test_titres_non_coches_ecartes_avec_leur_motif(self):
        self.lancer(selection((URLS[0], ""), (URLS[1], "rh")))
        publie = lire(self.dossier, ECARTES)
        self.assertEqual(publie["schema_version"], "SNUM_CANDIDATS_ECARTES_V1")
        self.assertEqual(
            [publie["edition_date"], publie["window_start"], publie["window_end"]],
            ["2026-11-11", "2026-11-01", "2026-11-10"],
        )
        self.assertEqual({c["url"] for c in publie["candidates"]}, set(URLS[2:]))
        self.assertEqual(
            {c["reason"] for c in publie["candidates"]}, {"NON_SELECTIONNE"}
        )
        self.assertEqual(
            sorted(publie["candidates"][0]),
            [
                "publication_date_iso",
                "publication_date_long",
                "reason",
                "source",
                "title",
                "url",
            ],
        )

    def test_url_hors_des_candidats_refusee(self):
        for url in (
            "https://www.numerique.gouv.fr/une-autre-page",
            "https://exemple.test/article/veille-snum",
            URLS[0] + "?page=2",
            "",
        ):
            with self.subTest(url=url):
                self.refus(selection((URLS[1], ""), (url, "")), "absente des titres")
                # Seul le rapport en ligne a été lu : aucune page d'article.
                self.assertEqual(self.client.calls, [URL_RAPPORT])

    def test_rubrique_inconnue_refusee(self):
        for rubrique in ("sport", "IA", None, 3, ["ia"]):
            with self.subTest(rubrique=rubrique):
                self.refus(selection((URLS[0], rubrique)), "Rubrique inconnue")

    def test_selection_vide_refusee(self):
        for texte in ("[]", "", "   "):
            with self.subTest(texte=texte):
                self.refus(texte, "Sélection")

    def test_selection_trop_longue_refusee(self):
        self.refus(selection(*[(URLS[0], "")] * 61), "60")

    def test_selection_mal_formee_refusee(self):
        for texte in (
            "pas du json",
            "{}",
            '"' + URLS[0] + '"',
            json.dumps([URLS[0]]),
            json.dumps([{"url": URLS[0], "rubrique": "", "autre": 1}]),
            # Relecture indépendante : une adresse non textuelle levait TypeError.
            json.dumps([{"url": [1], "rubrique": ""}]),
            json.dumps([{"url": {"a": 1}, "rubrique": ""}]),
            json.dumps([{"url": None, "rubrique": ""}]),
        ):
            with self.subTest(texte=texte):
                self.refus(texte, "Sélection")

    def test_adresse_en_double_refusee(self):
        self.refus(selection((URLS[0], ""), (URLS[0], "ia")), "en double")

    def test_periode_differente_de_celle_des_titres_refusee(self):
        self.refus(
            selection((URLS[0], "")), "ne correspond", debut=dt.date(2026, 11, 2)
        )

    def test_periode_identique_acceptee(self):
        code = self.lancer(
            selection((URLS[0], "")),
            edition=dt.date(2026, 11, 11),
            debut=dt.date(2026, 11, 1),
            fin=dt.date(2026, 11, 10),
        )
        self.assertEqual(code, 0)

    def test_rapport_en_ligne_illisible(self):
        for rapport in (
            "<html>404</html>",
            "[]",
            {**PREMIER, "candidates": "aucun"},
            {**PREMIER, "window_start": "01/11/2026"},
            {**PREMIER, "sources": [{"label": "X", "status": "inconnu"}]},
        ):
            with self.subTest(rapport=str(rapport)[:30]):
                self.refus(
                    selection((URLS[0], "")), "Rapport", client=Site(rapport=rapport)
                )

    def test_echec_albert_isole_paquet_partiel(self):
        choix = selection((URLS[0], ""), (URLS[1], ""))
        self.assertEqual(self.lancer(choix, albert=Albert(pannes=[URLS[1]])), 0)
        motifs = {
            c["url"]: c["reason"] for c in lire(self.dossier, ECARTES)["candidates"]
        }
        self.assertEqual(motifs[URLS[1]], "ECHEC_ALBERT")
        rapport = lire(self.dossier, RAPPORT)
        self.assertEqual(rapport["status"], "partial")
        self.assertEqual(
            rapport["errors"], [{"url": URLS[1], "reason": "Albert : HTTP 401"}]
        )
        titres = [w["title"] for w in lire(self.dossier, PAQUET)["watch"]]
        self.assertIn("Analyse partielle", titres)
        self.assertTrue(validate_packet_v519(lire(self.dossier, PAQUET)))

    def test_tous_les_resumes_en_echec_rien_n_est_ecrit(self):
        choix = selection((URLS[0], ""), (URLS[1], "ia"))
        self.assertEqual(self.lancer(choix, albert=Albert(pannes=URLS)), 1)
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))
        self.assertNotIn(TOKEN, self.sortie_erreur.getvalue())

    def test_page_qui_ne_se_relit_plus(self):
        choix = selection((URLS[0], ""), (URLS[1], ""))
        code = self.lancer(choix, client=Site(illisibles=[URLS[1]]))
        self.assertEqual(code, 0)
        motifs = {
            c["url"]: c["reason"] for c in lire(self.dossier, ECARTES)["candidates"]
        }
        self.assertEqual(motifs[URLS[1]], "PAGE_NON_RELUE")
        self.assertEqual(set(self.albert.rubriques()), {URLS[0]})
        self.assertEqual(lire(self.dossier, RAPPORT)["status"], "partial")

    def test_deux_appels_albert_simultanes_au_plus(self):
        albert = Albert(duree=0.03)
        self.lancer(selection(*[(url, "") for url in URLS[:8]]), albert=albert)
        self.assertEqual(len(albert.appels), 8)
        self.assertEqual(albert.maximum, 2)

    def test_budget_de_duree_epuise(self):
        with mock.patch("veille_snum.resumer.MAX_ALBERT_SECONDS", 0):
            code = self.lancer(selection((URLS[0], "")))
        self.assertEqual(code, 1)
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))

    def test_exception_portant_le_jeton_jamais_ecrite(self):
        fuite = ValueError(f"Invalid header value b'Bearer {TOKEN}'")
        choix = selection((URLS[0], ""), (URLS[1], "ia"), (URLS[2], ""))
        albert = Albert(pannes=URLS[1:3], erreur=fuite)
        self.assertEqual(self.lancer(choix, albert=albert), 0)
        for nom in fichiers(self.dossier):
            self.assertNotIn(TOKEN, (self.dossier / nom).read_text(encoding="utf-8"))
        self.assertNotIn(TOKEN, self.sortie_standard.getvalue())
        self.assertNotIn(TOKEN, self.sortie_erreur.getvalue())
        self.assertEqual(
            {e["reason"] for e in lire(self.dossier, RAPPORT)["errors"]},
            {"Albert : ValueError"},
        )


class LigneDeCommandeTests(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp()) / "site"

    def executer(self, albert, arguments=(), *, cle=TOKEN, choix=None):
        environnement = {
            "ALBERT_API_KEY": cle,
            "ALBERT_MODEL": "modele-test",
            "SELECTION": choix or selection((URLS[0], "ia"), (URLS[1], "")),
        }
        self.sortie_standard, self.sortie_erreur = io.StringIO(), io.StringIO()
        with (
            mock.patch.dict("os.environ", environnement),
            mock.patch("veille_snum.resumer.HttpClient", return_value=Site()),
            mock.patch(
                "veille_snum.resumer.albert_summary", side_effect=albert
            ) as appel,
            mock.patch("sys.stdout", self.sortie_standard),
            mock.patch("sys.stderr", self.sortie_erreur),
        ):
            code = main(["--sortie", str(self.dossier), "--run-id", "12", *arguments])
        self.appel = appel
        return code

    def test_selection_lue_dans_l_environnement_et_jeton_jamais_ecrit(self):
        code = self.executer(lambda candidat, *a, **k: good_summary(candidat), DATES)
        self.assertEqual(code, 0)
        self.assertEqual(fichiers(self.dossier), [ECARTES, ETAT, PAQUET, RAPPORT])
        for nom in fichiers(self.dossier):
            texte = (self.dossier / nom).read_text(encoding="utf-8")
            self.assertNotIn(TOKEN, texte)
            self.assertTrue(texte.endswith("\n"))
        self.assertNotIn(TOKEN, self.sortie_standard.getvalue())
        self.assertEqual(lire(self.dossier, ETAT)["run_id"], 12)
        self.assertEqual(self.appel.call_count, 2)
        for appel in self.appel.call_args_list:
            self.assertEqual(appel.args[1:3], (TOKEN, "modele-test"))
        imposees = {
            a.args[0]["url"]: a.kwargs["forced_rubric"]
            for a in self.appel.call_args_list
        }
        self.assertEqual(imposees, {URLS[0]: "ia", URLS[1]: None})

    def test_sans_dates_la_periode_des_titres_est_reprise(self):
        code = self.executer(lambda candidat, *a, **k: good_summary(candidat))
        self.assertEqual(code, 0)
        self.assertEqual(lire(self.dossier, PAQUET)["window_start"], "2026-11-01")

    def test_sans_jeton_aucun_appel_ni_fichier(self):
        code = self.executer(AssertionError("Albert appelé sans jeton"), cle="")
        self.assertEqual(code, 1)
        self.appel.assert_not_called()
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))
        self.assertIn("Albert non configuré", self.sortie_erreur.getvalue())

    def test_echec_albert_general_sans_fuite_du_jeton(self):
        def refuse(*args, **kwargs):
            raise HTTPError(ALBERT, 401, f"refus {TOKEN}", {}, None)

        self.assertEqual(self.executer(refuse), 1)
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))
        self.assertNotIn(TOKEN, self.sortie_erreur.getvalue())
        self.assertNotIn(TOKEN, self.sortie_standard.getvalue())


if __name__ == "__main__":
    unittest.main()
