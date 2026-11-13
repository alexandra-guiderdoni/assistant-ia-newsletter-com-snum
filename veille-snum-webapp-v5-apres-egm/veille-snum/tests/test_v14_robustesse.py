"""Robustesse du second temps : budget de durée, rapport déjà résumé, Albert saturé. Aucun appel réseau réel."""

import datetime as dt
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

from test_v13_deux_temps import (
    ALBERT,
    URLS,
    Albert,
    Site,
    selection,
)

from veille_snum.repecher import repecher
from veille_snum.resumer import publier_resumes

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


if __name__ == "__main__":
    unittest.main()
