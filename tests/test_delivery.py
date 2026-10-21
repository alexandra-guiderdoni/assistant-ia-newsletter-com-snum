"""Vérifie les paquets transmis, leurs notices et le fichier DSFR extrait seul."""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
from newsletter_mail import build
from test_mail_tool import cases, invalid_cases

NAMES = [
    "Newsletter SNUM - Collecte",
    "Newsletter SNUM - Rendu HTML",
    "Newsletter SNUM - rendu DSFR",
]


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.output = self.folder / "distribution"
        result = self.command()
        self.assertEqual(result.returncode, 0, result.stderr)

    def command(self, *arguments):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(PROJECT / "scripts/build_delivery.py"),
                "--output-dir",
                str(self.output),
                *arguments,
            ],
            cwd=self.folder,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_archives_include_notices_exact_payloads_and_valid_local_links(self):
        self.assertEqual(self.command("--check").returncode, 0)
        sums = (self.output / "SHA256SUMS.txt").read_text().splitlines()
        self.assertEqual(len(sums), 3)
        for line in sums:
            digest, filename = line.split("  ", 1)
            self.assertEqual(
                digest,
                hashlib.sha256((self.output / filename).read_bytes()).hexdigest(),
            )
        for index, project in enumerate(NAMES):
            with self.subTest(project=project):
                with ZipFile(self.output / f"{project}.zip") as zipped:
                    self.assertIsNone(zipped.testzip())
                    members = zipped.namelist()
                    self.assertEqual(len(members), len(set(members)))
                    self.assertTrue(
                        all(".." not in PurePosixPath(p).parts for p in members)
                    )
                    self.assertTrue(all(p.startswith(project + "/") for p in members))
                    files = [p.removeprefix(project + "/") for p in members]
                    installer = [p for p in files if p.startswith("INSTALLATION-")]
                    self.assertEqual(len(installer), 1)
                    self.assertIn("MODE-OPERATOIRE.md", files)
                    self.assertIn("EXEMPLE-PAQUET-RENDU-V5.19.json", files)
                    numbered = [p for p in files if re.match(r"\d\d-", p)]
                    self.assertEqual(len(numbered), [3, 5, 10][index])
                    for member, relative in zip(members, files, strict=True):
                        self.assertTrue(
                            zipped.read(member) == (PROJECT / relative).read_bytes(),
                            f"Fichier différent : {relative}",
                        )
                    zipped.extractall(self.folder / "extraction")
                root = (self.folder / "extraction" / project).resolve()
                for document in root.rglob("*.md"):
                    for target in re.findall(
                        r"\[[^\]\n]+\]\(([^)]+)\)", document.read_text()
                    ):
                        parsed = urlsplit(target.strip("<>"))
                        if parsed.scheme or not parsed.path:
                            continue
                        path = (document.parent / unquote(parsed.path)).resolve()
                        self.assertTrue(path.is_relative_to(root), target)
                        self.assertTrue(path.exists(), f"Lien absent : {document.name}")
                if index == 2:
                    self.assertTrue((root / "outil-rendu-dsfr.html").is_file())
                    prompt = (root / "30-PROMPT-SYSTEME-RENDU-DSFR-V1.0.md").read_text()
                    self.assertLessEqual(len(prompt), 4000)
                    self.assertNotIn("sinon bloc WATCH avec WATCH_ITEMS", prompt)
                    for resource in root.glob("3[1-4]-*.md"):
                        self.assertLessEqual(len(resource.read_text()), 4500)

    def test_check_rejects_archive_with_missing_installation_notice(self):
        path = self.output / f"{NAMES[0]}.zip"
        with ZipFile(path) as zipped:
            retained = [
                (item, zipped.read(item.filename))
                for item in zipped.infolist()
                if "INSTALLATION-" not in item.filename
            ]
        with ZipFile(path, "w", ZIP_DEFLATED) as zipped:
            for info, data in retained:
                zipped.writestr(info, data)
        result = self.command("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("LIVRAISON_DRIFT", result.stderr)
        with ZipFile(path) as zipped:
            self.assertFalse(any("INSTALLATION-" in p for p in zipped.namelist()))

    def test_dsfr_extracted_alone_matches_reference_without_repository_assets(self):
        with ZipFile(self.output / f"{NAMES[2]}.zip") as zipped:
            bundle = zipped.read(f"{NAMES[2]}/outil-rendu-dsfr.html")
        isolated = self.folder / "poste"
        isolated.mkdir()
        (isolated / "outil-renomme.html").write_bytes(bundle)
        packets = cases()
        run = subprocess.run(
            ["node", "-e", (PROJECT / "tests/mail_tool_runner.js").read_text()],
            input=json.dumps(
                {
                    "bundle": bundle.decode(),
                    "packets": packets,
                    "invalid": invalid_cases(packets[0]),
                }
            ),
            cwd=isolated,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertTrue(result["uiPassed"])
        for packet, rendered in zip(packets, result["rendered"], strict=True):
            self.assertTrue(
                rendered == build(packet), "Mail extrait différent du canon"
            )
        self.assertEqual([p.name for p in isolated.iterdir()], ["outil-renomme.html"])


if __name__ == "__main__":
    unittest.main()
