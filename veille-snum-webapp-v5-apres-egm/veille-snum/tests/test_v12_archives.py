"""Archives des collectes : entrée d'index calculée depuis le site publié, index fusionné sans perte."""

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

from veille_snum.archiver import SCHEMA, entree, fusionner, main

MAINTENANT = dt.datetime(2026, 11, 13, 22, 0, 45, tzinfo=dt.timezone.utc)


def site_publie():
    dossier = Path(tempfile.mkdtemp())
    paquet = {
        "edition_date": "2026-11-13",
        "window_start": "2026-11-03",
        "window_end": "2026-11-13",
        "articles": [{"url": f"https://exemple.gouv.fr/{i}"} for i in range(3)],
    }
    rapport = {"status": "partial", "candidates": [{}] * 5}
    ecartes = {"candidates": [{}] * 2}
    for nom, contenu in (
        ("paquet-v519.json", paquet),
        ("rapport-collecte.json", rapport),
        ("candidats-ecartes.json", ecartes),
    ):
        (dossier / nom).write_text(json.dumps(contenu), encoding="utf-8")
    return dossier


def collecte(identifiant):
    return {"id": identifiant, "edition_date": identifiant[:10]}


class EntreeTests(unittest.TestCase):
    def test_entree_calculee_depuis_les_trois_fichiers(self):
        self.assertEqual(
            entree(site_publie(), 43514452853, MAINTENANT),
            {
                "id": "2026-11-13_43514452853",
                "run_id": 43514452853,
                "edition_date": "2026-11-13",
                "window_start": "2026-11-03",
                "window_end": "2026-11-13",
                "status": "partial",
                "articles": 3,
                "candidats": 5,
                "ecartes": 2,
                "archived_at": "2026-11-13T22:00:45Z",
            },
        )


class FusionTests(unittest.TestCase):
    def test_premier_index(self):
        self.assertEqual(
            fusionner(None, collecte("2026-11-13_1")),
            {"schema_version": SCHEMA, "collectes": [collecte("2026-11-13_1")]},
        )

    def test_plus_recente_en_premier_sans_perte(self):
        ancien = {
            "schema_version": SCHEMA,
            "collectes": [collecte("2026-11-06_1"), collecte("2026-10-30_1")],
        }
        ids = [
            c["id"] for c in fusionner(ancien, collecte("2026-11-13_2"))["collectes"]
        ]
        self.assertEqual(ids, ["2026-11-13_2", "2026-11-06_1", "2026-10-30_1"])

    def test_meme_collecte_remplacee_une_seule_fois(self):
        ancien = {
            "schema_version": SCHEMA,
            "collectes": [collecte("2026-11-13_2"), collecte("2026-11-06_1")],
        }
        ids = [
            c["id"] for c in fusionner(ancien, collecte("2026-11-13_2"))["collectes"]
        ]
        self.assertEqual(ids, ["2026-11-13_2", "2026-11-06_1"])

    def test_index_abime_entrees_invalides_ignorees(self):
        for ancien in (
            "texte",
            [],
            {"collectes": "pas une liste"},
            {"collectes": [1, {"sans": "id"}]},
        ):
            with self.subTest(ancien=ancien):
                ids = [
                    c["id"]
                    for c in fusionner(ancien, collecte("2026-11-13_2"))["collectes"]
                ]
                self.assertEqual(ids, ["2026-11-13_2"])


class LigneDeCommandeTests(unittest.TestCase):
    def test_entree_puis_fusion_par_fichiers(self):
        dossier = Path(tempfile.mkdtemp())
        sortie_entree, sortie_index = dossier / "entree.json", dossier / "index.json"
        self.assertEqual(
            main(
                [
                    "entree",
                    "--site",
                    str(site_publie()),
                    "--run-id",
                    "7",
                    "--sortie",
                    str(sortie_entree),
                ]
            ),
            0,
        )
        self.assertEqual(
            json.loads(sortie_entree.read_text(encoding="utf-8"))["id"], "2026-11-13_7"
        )
        absent = dossier / "absent.json"
        self.assertEqual(
            main(
                [
                    "fusion",
                    "--ancien",
                    str(absent),
                    "--entree",
                    str(sortie_entree),
                    "--sortie",
                    str(sortie_index),
                ]
            ),
            0,
        )
        index = json.loads(sortie_index.read_text(encoding="utf-8"))
        self.assertEqual([c["id"] for c in index["collectes"]], ["2026-11-13_7"])


if __name__ == "__main__":
    unittest.main()
