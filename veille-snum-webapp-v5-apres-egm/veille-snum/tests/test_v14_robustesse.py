"""Robustesse du second temps : budget de durée, rapport déjà résumé, Albert saturé. Aucun appel réseau réel."""

import datetime as dt
import io
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
from veille_snum.core import validate_packet_v519
from veille_snum.repecher import repecher
from veille_snum.resumer import lire_rapport, publier_resumes

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


class AlbertSature(Albert):
    """Albert refuse par un 429 tout appel au-delà de deux simultanés."""

    def __init__(self, duree):
        super().__init__(duree=duree)
        self.refus = 0

    def __call__(self, candidat, feedback=None, forced_rubric=None):
        with self.verrou:
            if self.en_cours >= 2:
                self.refus += 1
                raise HTTPError(ALBERT, 429, "Too Many Requests", {}, None)
        return super().__call__(candidat, feedback, forced_rubric)


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
