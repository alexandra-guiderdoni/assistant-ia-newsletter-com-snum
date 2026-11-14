"""Robustesse du second temps : budget de durée, rapport déjà résumé, Albert saturé. Aucun appel réseau réel."""

import datetime as dt
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

from test_v13_deux_temps import (
    ALBERT,
    ECARTES,
    PAQUET,
    PREMIER,
    RAPPORT,
    URL_RAPPORT,
    URLS,
    Albert,
    Site,
    fichiers,
    lire,
    selection,
)
from test_veille_snum import good_summary
from veille_snum import archiver
from veille_snum.core import validate_packet_v519
from veille_snum.repecher import repecher
from veille_snum.resumer import lire_rapport, publier_resumes
from veille_snum.resumer import main as resumer_main

DEBUT, FIN = dt.date(2026, 11, 1), dt.date(2026, 11, 10)


class Horloge:
    """Temps factice : chaque attente avance l'horloge au lieu de suspendre le test."""

    def __init__(self):
        self.instant = 1000.0
        self.attentes = []

    def monotonic(self):
        return self.instant

    def sleep(self, duree):
        self.attentes.append(duree)
        self.instant += duree


def sature(_candidat, feedback=None, forced_rubric=None):
    raise HTTPError(ALBERT, 429, "Too Many Requests", {"Retry-After": "20"}, None)


class Cas(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp()) / "site"
        self.sortie_erreur = io.StringIO()

    def lancer(self, texte, client=None, albert=None, **options):
        with mock.patch("sys.stdout"), mock.patch("sys.stderr", self.sortie_erreur):
            return publier_resumes(
                texte, self.dossier, client or Site(), albert or Albert(), **options
            )


class BudgetTests(Cas):
    """Risque relevé en relecture : la rubrique imposée ignorait le budget de durée."""

    def attentes(self, rubrique, albert=sature, budget=30):
        horloge = Horloge()
        with (
            mock.patch("time.monotonic", horloge.monotonic),
            mock.patch("time.sleep", horloge.sleep),
            mock.patch("veille_snum.resumer.MAX_ALBERT_SECONDS", budget),
        ):
            code = self.lancer(selection((URLS[0], rubrique)), albert=albert)
        return code, horloge

    def test_rubrique_imposee_aucune_attente_au_dela_du_budget(self):
        code, horloge = self.attentes("ia")
        self.assertEqual(code, 1)
        # Budget de 30 s, Albert demande 20 s d'attente : une seule attente tient dans le budget.
        self.assertEqual(horloge.attentes, [20.0])

    def test_classement_libre_meme_regle(self):
        code, horloge = self.attentes("")
        self.assertEqual(code, 1)
        self.assertEqual(horloge.attentes, [20.0])

    def test_rubrique_imposee_pas_de_seconde_tentative_apres_l_echeance(self):
        appels = []
        horloge = Horloge()

        def lent_et_rejete(candidat, feedback=None, forced_rubric=None):
            appels.append(feedback)
            horloge.instant += 40
            return {"relevant": True}

        with (
            mock.patch("time.monotonic", horloge.monotonic),
            mock.patch("time.sleep", horloge.sleep),
            mock.patch("veille_snum.resumer.MAX_ALBERT_SECONDS", 30),
        ):
            code = self.lancer(selection((URLS[0], "ia")), albert=lent_et_rejete)
        self.assertEqual(code, 1)
        self.assertEqual(appels, [None])

    def test_repechage_sans_budget_inchange(self):
        # Le repêchage n'a pas de budget global : ses trois attentes restent possibles.
        horloge = Horloge()
        with (
            mock.patch("time.monotonic", horloge.monotonic),
            mock.patch("time.sleep", horloge.sleep),
        ):
            bilan = repecher(URLS[0], "ia", DEBUT, FIN, Site(), sature)
        self.assertEqual(bilan["message"], "Albert : HTTP 429")
        self.assertEqual(horloge.attentes, [20.0, 20.0, 20.0])


class RapportDejaResumeTests(Cas):
    """Deux personnes lancent la rédaction : la seconde demande ne refait pas le travail."""

    def test_rapport_d_un_paquet_deja_publie_refuse(self):
        for statut in ("ready", "partial", "incomplete", "unavailable"):
            with self.subTest(statut=statut):
                albert = Albert()
                client = Site(rapport={**PREMIER, "status": statut})
                code = self.lancer(selection((URLS[0], "")), client, albert)
                self.assertEqual(code, 1)
                self.assertEqual(albert.appels, [])
                self.assertEqual(client.calls, [URL_RAPPORT])
                self.assertFalse(self.dossier.exists() and fichiers(self.dossier))
                self.assertIn("déjà", self.sortie_erreur.getvalue())

    def test_seconde_demande_apres_une_premiere_publiee(self):
        choix = selection((URLS[0], ""), (URLS[1], "ia"))
        self.assertEqual(self.lancer(choix), 0)
        publie = lire(self.dossier, RAPPORT)
        premier_paquet = (self.dossier / PAQUET).read_text(encoding="utf-8")
        albert = Albert()
        autre = selection((URLS[2], ""), (URLS[3], ""))
        self.assertEqual(self.lancer(autre, Site(rapport=publie), albert), 1)
        self.assertEqual(albert.appels, [])
        # Le paquet de la première demande reste en place, octet pour octet.
        self.assertEqual(
            (self.dossier / PAQUET).read_text(encoding="utf-8"), premier_paquet
        )


class RapportIndisponibleTests(Cas):
    """GitHub Pages répond parfois 503 un court instant : le rapport est redemandé."""

    def site_capricieux(self, pannes, code=503):
        etat = {"reste": pannes}

        class Capricieux(Site):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if url == URL_RAPPORT and etat["reste"]:
                    etat["reste"] -= 1
                    self.calls.append(url)
                    raise HTTPError(url, code, "indisponible", {}, None)
                return super().get(url, domain, max_bytes, timeout)

        return Capricieux()

    def test_deux_reponses_503_puis_le_rapport(self):
        client = self.site_capricieux(2)
        with mock.patch("time.sleep") as attente:
            rapport = lire_rapport(client)
        self.assertEqual(rapport["status"], "needs_albert")
        self.assertEqual(client.calls, [URL_RAPPORT] * 3)
        self.assertEqual(attente.call_count, 2)

    def test_panne_durable_refus_lisible(self):
        client = self.site_capricieux(9)
        with mock.patch("time.sleep"):
            code = self.lancer(selection((URLS[0], "")), client)
        self.assertEqual(code, 1)
        self.assertEqual(client.calls, [URL_RAPPORT] * 3)
        self.assertIn("HTTP 503", self.sortie_erreur.getvalue())

    def test_rapport_absent_404_sans_nouvelle_tentative(self):
        client = self.site_capricieux(9, code=404)
        with mock.patch("time.sleep") as attente:
            code = self.lancer(selection((URLS[0], "")), client)
        self.assertEqual(code, 1)
        self.assertEqual(client.calls, [URL_RAPPORT])
        attente.assert_not_called()


class SelectionHostileTests(Cas):
    def test_imbrication_profonde_refusee_sans_trace(self):
        code = self.lancer("[" * 100_000)
        self.assertEqual(code, 1)
        self.assertIn("Sélection illisible", self.sortie_erreur.getvalue())

    def test_selection_volumineuse_de_soixante_adresses_longues(self):
        # 60 éléments de 1 000 caractères : proche du plafond GitHub de 65 535 caractères.
        texte = selection(
            *[(URLS[0] + "?" + "a" * 1000 + str(i), "") for i in range(60)]
        )
        self.assertGreater(len(texte), 60_000)
        self.assertEqual(self.lancer(texte), 1)
        self.assertIn("absente des titres", self.sortie_erreur.getvalue())


class RapportMalFormeTests(Cas):
    """Audit du 14 novembre : un rapport en ligne mal formé plantait après les appels Albert."""

    def test_limits_ou_excluded_mal_formes_refuses_avant_tout_appel(self):
        for champ, valeur in (
            ("limits", "aucune"),
            ("limits", [1, 2]),
            ("excluded", [{"url": URLS[0], "source": "X"}]),
            ("excluded", ["texte"]),
            ("excluded", [{"url": 3, "reason": "X"}]),
        ):
            with self.subTest(champ=champ, valeur=valeur):
                albert = Albert()
                client = Site(rapport={**PREMIER, champ: valeur})
                code = self.lancer(selection((URLS[0], "")), client, albert)
                self.assertEqual(code, 1)
                self.assertEqual(albert.appels, [])
                self.assertIn("Rapport des titres", self.sortie_erreur.getvalue())
                self.assertFalse(self.dossier.exists() and fichiers(self.dossier))

    def test_rapport_reel_du_premier_temps_toujours_accepte(self):
        self.assertEqual(self.lancer(selection((URLS[0], ""))), 0)


class DejaArchiveTests(Cas):
    """Le cache de GitHub Pages peut servir un rapport périmé : l'index des archives, lu par git, fait foi."""

    def archives(self, instant):
        return {
            "schema_version": "SNUM_ARCHIVES_V1",
            "collectes": [
                {
                    "id": "2026-11-10_5",
                    "titres_started_at": "2026-11-09T08:00:00+00:00",
                },
                {"id": "2026-11-11_8", "titres_started_at": instant},
                {"id": "2026-11-01_2"},
                "entrée illisible",
            ],
        }

    def test_titres_deja_archives_refuses_sans_appel_albert(self):
        albert = Albert()
        code = self.lancer(
            selection((URLS[0], "")),
            albert=albert,
            archives=self.archives(PREMIER["started_at_utc"]),
        )
        self.assertEqual(code, 1)
        self.assertEqual(albert.appels, [])
        self.assertIn("déjà été résumés", self.sortie_erreur.getvalue())
        self.assertIn("2026-11-11_8", self.sortie_erreur.getvalue())
        self.assertFalse(self.dossier.exists() and fichiers(self.dossier))

    def test_autres_archives_ou_index_illisible_sans_effet(self):
        for archives in (
            self.archives("2026-11-10T08:00:00+00:00"),
            None,
            {},
            {"collectes": "aucune"},
            [],
            "texte",
        ):
            with self.subTest(archives=str(archives)[:30]):
                self.dossier = Path(tempfile.mkdtemp()) / "site"
                code = self.lancer(selection((URLS[0], "")), archives=archives)
                self.assertEqual(code, 0)

    def test_l_archive_note_l_instant_de_la_collecte_des_titres(self):
        self.assertEqual(self.lancer(selection((URLS[0], "")), run_id=8), 0)
        entree = archiver.entree(self.dossier, 8, dt.datetime.now(dt.timezone.utc))
        self.assertEqual(entree["titres_started_at"], PREMIER["started_at_utc"])
        self.assertEqual(entree["id"], "2026-11-11_8")

    def test_ligne_de_commande_index_lu_dans_un_fichier_absent_tolere(self):
        index = Path(tempfile.mkdtemp()) / "archives.json"
        environnement = {
            "ALBERT_API_KEY": "JETON-FACTICE",
            "ALBERT_MODEL": "modele-test",
            "SELECTION": selection((URLS[0], "")),
        }

        def executer():
            with (
                mock.patch.dict("os.environ", environnement),
                mock.patch("veille_snum.resumer.HttpClient", return_value=Site()),
                mock.patch(
                    "veille_snum.resumer.albert_summary",
                    side_effect=lambda c, *a, **k: good_summary(c),
                ) as appel,
                mock.patch("sys.stdout"),
                mock.patch("sys.stderr", self.sortie_erreur),
            ):
                code = resumer_main(
                    ["--sortie", str(self.dossier), "--archives", str(index)]
                )
            return code, appel.call_count

        self.assertEqual(executer(), (0, 1))
        index.write_text(
            json.dumps(self.archives(PREMIER["started_at_utc"])), encoding="utf-8"
        )
        self.assertEqual(executer(), (1, 0))


class BudgetEnCoursDeTacheTests(Cas):
    """Contrôle de logique : une tâche déjà lancée appelait Albert après la fin du budget."""

    def test_page_relue_apres_l_echeance_aucun_appel_albert(self):
        horloge = Horloge()

        class Lent(Site):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if url in URLS:
                    horloge.instant += 40
                return super().get(url, domain, max_bytes, timeout)

        albert = Albert()
        with (
            mock.patch("time.monotonic", horloge.monotonic),
            mock.patch("time.sleep", horloge.sleep),
            mock.patch("veille_snum.resumer.MAX_ALBERT_SECONDS", 30),
        ):
            code = self.lancer(
                selection((URLS[0], ""), (URLS[1], "ia")), Lent(), albert
            )
        self.assertEqual(code, 1)
        self.assertEqual(albert.appels, [])
        self.assertIn("Aucun paquet publiable", self.sortie_erreur.getvalue())


class DoublonApresRelectureTests(Cas):
    """Contrôle de logique : deux titres gardés relus vers la même adresse, l'un disparaissait sans trace."""

    def test_second_titre_ecarte_avec_son_motif(self):
        ancien = URLS[0].replace("/article/veille-snum", "/article/ancien-slug")
        modele = next(c for c in PREMIER["candidates"] if c["url"] == URLS[0])
        premier = {
            **PREMIER,
            "candidates": [
                *PREMIER["candidates"],
                {**modele, "url": ancien, "title": "Ancien titre du même article"},
            ],
        }

        class Redirige(Site):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if url == ancien:
                    self.calls.append(url)
                    return super().get(URLS[0], domain, max_bytes, timeout)
                return super().get(url, domain, max_bytes, timeout)

        code = self.lancer(
            selection((URLS[0], ""), (ancien, "ia")), Redirige(rapport=premier)
        )
        self.assertEqual(code, 0)
        paquet = lire(self.dossier, PAQUET)
        self.assertEqual([a["url"] for a in paquet["articles"]], [URLS[0]])
        motifs = {
            c["url"]: c["reason"] for c in lire(self.dossier, ECARTES)["candidates"]
        }
        self.assertEqual(motifs[ancien], "DOUBLON_APRES_RELECTURE")
        # Chaque candidat du rapport est dans le paquet ou dans les écartés, une seule fois.
        rapport = lire(self.dossier, RAPPORT)
        presents = [a["url"] for a in paquet["articles"]] + list(motifs)
        self.assertEqual(
            sorted(presents), sorted(c["url"] for c in rapport["candidates"])
        )
        self.assertEqual(len(rapport["candidates"]), 14)


class MessagesEtRefusTests(Cas):
    """Constats faibles de l'audit : messages inexacts, refus sans trace Python."""

    def test_echec_total_par_pages_non_relues_message_exact(self):
        code = self.lancer(
            selection((URLS[0], ""), (URLS[1], "")), Site(illisibles=URLS)
        )
        self.assertEqual(code, 1)
        message = self.sortie_erreur.getvalue()
        self.assertIn("2 page(s) non relue(s)", message)
        self.assertIn("0 échec(s) Albert", message)

    def test_rubrique_facultative_dans_le_message_de_refus(self):
        self.assertEqual(self.lancer(json.dumps([{"rubrique": "ia"}])), 1)
        self.assertIn("« url »", self.sortie_erreur.getvalue())
        self.assertIn("facultative", self.sortie_erreur.getvalue())

    def test_periode_inversee_ou_trop_longue_refus_en_francais_sans_trace(self):
        from veille_snum import publier

        for mode in ("collecte", "titres"):
            for dates in (
                ["--debut", "10/11/2026", "--fin", "01/11/2026"],
                ["--debut", "01/01/2026", "--fin", "10/11/2026"],
            ):
                with self.subTest(mode=mode, dates=dates):
                    with (
                        mock.patch("sys.stdout"),
                        mock.patch("sys.stderr", self.sortie_erreur),
                    ):
                        code = publier.main(
                            [
                                "--mode",
                                mode,
                                "--edition",
                                "11/11/2026",
                                *dates,
                                "--sortie",
                                str(self.dossier),
                            ]
                        )
                    self.assertEqual(code, 1)
                    self.assertIn("Collecte refusée", self.sortie_erreur.getvalue())
                    self.assertFalse(self.dossier.exists() and fichiers(self.dossier))

    def test_repechage_periode_de_plus_de_61_jours_refusee(self):
        bilan = repecher(URLS[0], "ia", dt.date(2026, 1, 1), FIN, Site(), Albert())
        self.assertEqual(bilan["status"], "erreur")
        self.assertIn("61 jours", bilan["message"])
        self.assertEqual(
            repecher(URLS[0], "ia", DEBUT, FIN, Site(), Albert())["status"], "ok"
        )


class IndexDesArchivesTests(unittest.TestCase):
    """Contrôle de logique : un index distant tronqué faisait perdre toutes les entrées existantes."""

    def test_index_present_mais_illisible_rien_n_est_ecrit(self):
        dossier = Path(tempfile.mkdtemp())
        (dossier / "ancien.json").write_text('{"collectes": [', encoding="utf-8")
        (dossier / "entree.json").write_text(
            json.dumps({"id": "2026-11-14_9"}), encoding="utf-8"
        )
        erreur = io.StringIO()
        with mock.patch("sys.stderr", erreur):
            code = archiver.main(
                [
                    "fusion",
                    "--ancien",
                    str(dossier / "ancien.json"),
                    "--entree",
                    str(dossier / "entree.json"),
                    "--sortie",
                    str(dossier / "index.json"),
                ]
            )
        self.assertEqual(code, 1)
        self.assertFalse((dossier / "index.json").exists())
        self.assertIn("illisible", erreur.getvalue())

    def test_index_absent_premiere_archive(self):
        dossier = Path(tempfile.mkdtemp())
        (dossier / "entree.json").write_text(
            json.dumps({"id": "2026-11-14_9"}), encoding="utf-8"
        )
        code = archiver.main(
            [
                "fusion",
                "--ancien",
                str(dossier / "absent.json"),
                "--entree",
                str(dossier / "entree.json"),
                "--sortie",
                str(dossier / "index.json"),
            ]
        )
        self.assertEqual(code, 0)
        self.assertEqual(
            json.loads((dossier / "index.json").read_text())["collectes"],
            [{"id": "2026-11-14_9"}],
        )


class DelaiAlbertTests(unittest.TestCase):
    """Audit : le délai de chaque appel Albert du second temps restait de 30 s, quel que soit le temps restant."""

    def test_delai_reduit_au_temps_restant(self):
        dossier = Path(tempfile.mkdtemp()) / "site"
        environnement = {
            "ALBERT_API_KEY": "JETON-FACTICE",
            "ALBERT_MODEL": "modele-test",
            "SELECTION": selection((URLS[0], ""), (URLS[1], "ia")),
        }
        delais = []

        def albert(
            candidat, cle, modele, timeout=30, feedback=None, forced_rubric=None
        ):
            delais.append(timeout)
            return good_summary(candidat)

        for budget, attendu in ((360, lambda d: d == 30), (12, lambda d: 1 <= d <= 12)):
            delais.clear()
            with (
                mock.patch.dict("os.environ", environnement),
                mock.patch("veille_snum.resumer.HttpClient", return_value=Site()),
                mock.patch("veille_snum.resumer.albert_summary", side_effect=albert),
                mock.patch("veille_snum.resumer.MAX_ALBERT_SECONDS", budget),
                mock.patch("sys.stdout"),
                mock.patch("sys.stderr"),
            ):
                self.assertEqual(resumer_main(["--sortie", str(dossier)]), 0)
            self.assertEqual(len(delais), 2)
            self.assertTrue(all(attendu(d) for d in delais), (budget, delais))


class AlbertSature(Albert):
    """Albert refuse par un 429 tout appel au-delà de deux simultanés."""

    def __init__(self, duree):
        super().__init__(duree=duree)
        self.refus = 0
        self.places = 0

    def __call__(self, candidat, feedback=None, forced_rubric=None):
        # Contrôle et réservation sous le même verrou : jamais trois appels admis ensemble.
        with self.verrou:
            if self.places >= 2:
                self.refus += 1
                raise HTTPError(ALBERT, 429, "Too Many Requests", {}, None)
            self.places += 1
        try:
            return super().__call__(candidat, feedback, forced_rubric)
        finally:
            with self.verrou:
                self.places -= 1


class TroisAppelsSimultanesTests(Cas):
    """Risque relevé en relecture : un repêchage pendant la rédaction porte les appels à trois."""

    def test_repechage_pendant_la_redaction_degrade_sans_casser(self):
        albert = AlbertSature(duree=0.02)
        choix = selection(*[(url, "") for url in URLS[:10]])
        bilans = []

        def repecher_en_boucle():
            for url in URLS[10:13] * 4:
                bilans.append(repecher(url, "ia", DEBUT, FIN, Site(), albert))

        with (
            mock.patch("veille_snum.resumer._retry_delay", return_value=0.03),
            mock.patch("veille_snum.repecher._retry_delay", return_value=0.03),
        ):
            concurrent = threading.Thread(target=repecher_en_boucle)
            concurrent.start()
            code = self.lancer(choix, albert=albert)
            concurrent.join()
        # La saturation a bien eu lieu, et jamais plus de deux appels n'ont été servis ensemble.
        self.assertGreater(albert.refus, 0)
        self.assertEqual(albert.maximum, 2)
        # Chaque titre gardé finit résumé, ou écarté avec un motif lisible et repêchable.
        self.assertEqual(code, 0)
        paquet = lire(self.dossier, PAQUET)
        self.assertTrue(validate_packet_v519(paquet))
        resumes = {a["url"] for a in paquet["articles"]}
        echecs = {
            c["url"]
            for c in lire(self.dossier, ECARTES)["candidates"]
            if c["reason"] == "ECHEC_ALBERT"
        }
        self.assertEqual(resumes | echecs, set(URLS[:10]))
        self.assertFalse(resumes & echecs)
        for erreur in lire(self.dossier, RAPPORT)["errors"]:
            self.assertEqual(erreur["reason"], "Albert : HTTP 429")
        # Chaque repêchage se termine par un article ou par un message lisible.
        self.assertEqual(len(bilans), 12)
        for bilan in bilans:
            self.assertIn(
                bilan["message"],
                ("Article repêché dans la rubrique ia.", "Albert : HTTP 429"),
            )
            if bilan["status"] == "ok":
                self.assertEqual(
                    bilan["article"]["fact"], good_summary(bilan["article"])["fact"]
                )


if __name__ == "__main__":
    unittest.main()


class NotesDeCollecteTests(unittest.TestCase):
    """Relevé d'accessibilité : les notes de collecte lues par la page étaient en partie en anglais."""

    def test_notes_sur_le_plan_de_site_en_francais(self):
        from veille_snum.core import discover_source, sources

        class SansPlan(Site):
            def get(self, url, domain, max_bytes=600_000, timeout=7):
                if url.endswith("/sitemap.xml"):
                    raise HTTPError(url, 503, "Service Unavailable", {}, None)
                return super().get(url, domain, max_bytes, timeout)

        source = next(s for s in sources() if not s["internal"])
        _, _, etat = discover_source(source, DEBUT, FIN, SansPlan())
        notes = " ".join(etat["notes"])
        self.assertIn("Plan de site indisponible : HTTP 503", notes)
        self.assertNotIn("itemap", notes)
        # Les noms de champs du rapport ne changent pas : la page et les archives les lisent.
        self.assertIn("sitemap_skipped", etat)
