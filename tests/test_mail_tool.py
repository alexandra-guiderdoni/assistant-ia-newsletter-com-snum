"""Compare l'outil distribué au moteur de référence et exerce son parcours métier."""

import base64
import copy
import hashlib
import json
import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
from newsletter_mail import blocks, build


def cases():
    sample = json.loads(
        (PROJECT / "tests/fixtures/mail-dsfr/edition-2026-10-14.json").read_text()
    )
    result = [sample]
    for count in [0, 1, 2, 3, 18, 60]:
        packet = copy.deepcopy(sample)
        packet["articles"] = []
        packet["watch"] = []
        for index in range(count):
            article = copy.deepcopy(sample["articles"][index % 5])
            article["id"] = f"A{index}"
            article["url"] = f"https://example.gouv.fr/article/{index}?a=1&b=2"
            article["rubric"] = ["numerique", "ia", "commande", "rh", "bercy"][
                index % 5
            ]
            article["essential"] = index % 2 == 0
            packet["articles"].append(article)
        result.append(packet)
    watched = copy.deepcopy(result[1])
    watched["watch"] = sample["watch"]
    result.append(watched)
    escaped = copy.deepcopy(sample)
    escaped["articles"][0]["title"] = (
        '<img src=x onerror="alert(1)"> @@TITLE@@ & « État »'
    )
    escaped["articles"][0]["title"] += (
        " SNUM_PAQUET_RENDU_V519_START SNUM_PAQUET_RENDU_V519_END"
    )
    escaped["articles"][0]["fact"] = "Très long texte conservé : " * 150
    escaped["articles"][0]["snum_interest"] = "SansEspace" * 100
    escaped["watch"][0]["summary"] = "</script><script>alert('exemple')</script>"
    result.append(escaped)
    weekday = copy.deepcopy(sample)
    weekday["edition_date_long"] = "mercredi 14 octobre 2026"
    result.append(weekday)
    return result


def invalid_cases(sample):
    result = [
        None,
        [],
        {**sample, "extra": True},
        {**sample, "schema_version": "autre"},
    ]
    for field, value in [
        ("edition_date", "2026-02-30"),
        ("edition_date", "0000-01-01"),
        ("edition_date_long", "13 octobre 2026"),
        ("window_start", "2026-10-20"),
        ("articles", {}),
    ]:
        result.append({**sample, field: value})
    for field, value in [
        ("url", "javascript:alert(1)"),
        ("url", "http://example.gouv.fr"),
        ("url", "https://example.gouv.fr/\narticle"),
        ("rubric", "__proto__"),
        ("keywords", ["un"]),
        ("essential", "true"),
        ("publication_date_long", "1 octobre 2026"),
        ("title", ""),
    ]:
        packet = copy.deepcopy(sample)
        packet["articles"][0][field] = value
        result.append(packet)
    duplicate = copy.deepcopy(sample)
    duplicate["articles"].append(copy.deepcopy(duplicate["articles"][0]))
    result.append(duplicate)
    missing = copy.deepcopy(sample)
    del missing["articles"][0]["source"]
    result.append(missing)
    result.append({**sample, "watch": [{"title": "x"}]})
    return result


class Markup(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.tags = []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class MailToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = (PROJECT / "outil-rendu-dsfr.html").read_text()
        cls.packets = cases()
        cls.invalid = invalid_cases(cls.packets[0])
        run = subprocess.run(
            ["node", str(PROJECT / "tests/mail_tool_runner.js")],
            input=json.dumps(
                {"bundle": cls.bundle, "packets": cls.packets, "invalid": cls.invalid}
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        if run.returncode:
            raise AssertionError(run.stderr)
        cls.result = json.loads(run.stdout)

    def test_actual_bundle_matches_canon_for_ten_variants(self):
        self.assertEqual(len(self.packets), 10)
        for index, (packet, actual) in enumerate(
            zip(self.packets, self.result["rendered"], strict=True)
        ):
            with self.subTest(case=index):
                self.assertTrue(actual == build(packet), "HTML différent du canon")
                image = re.search(r'data:image/png;base64,([^"\s]+)', actual)[1]
                self.assertEqual(image, blocks()["LOGO"])
                self.assertEqual(len(base64.b64decode(image, validate=True)), 9024)

    def test_ui_preview_download_and_invalidation(self):
        self.assertTrue(self.result["uiPassed"])
        self.assertEqual(self.result["invalidRejected"], len(self.invalid) + 3)

    def test_collection_notes_are_absent_from_exported_mail(self):
        for packet, html in zip(self.packets, self.result["rendered"], strict=True):
            self.assertFalse("À surveiller" in html, "Alertes présentes dans le mail")
            for item in packet["watch"]:
                self.assertFalse(
                    item["summary"] in html, "Commentaire présent dans le mail"
                )

    def test_bundle_is_offline_and_preview_is_sandboxed(self):
        markup = Markup(self.bundle)
        html = next(attrs for tag, attrs in markup.tags if tag == "html")
        self.assertEqual(html["lang"], "fr")
        iframe = next(attrs for tag, attrs in markup.tags if tag == "iframe")
        self.assertEqual(iframe["sandbox"], "")
        self.assertTrue(iframe["title"])
        for tag, attrs in markup.tags:
            self.assertFalse(tag in {"script", "img", "iframe"} and "src" in attrs)
            self.assertFalse(tag == "link" and "href" in attrs)
        csp = next(
            attrs["content"]
            for tag, attrs in markup.tags
            if attrs.get("http-equiv") == "Content-Security-Policy"
        )
        self.assertIn("connect-src 'none'", csp)
        scripts = re.findall(r"<script>(.*?)</script>", self.bundle, re.DOTALL)
        for code in scripts:
            sha = base64.b64encode(hashlib.sha256(code.encode()).digest()).decode()
            self.assertIn(f"'sha256-{sha}'", csp)
        self.assertNotIn("localStorage", "\n".join(scripts))
        self.assertNotIn("fetch(", "\n".join(scripts))


if __name__ == "__main__":
    unittest.main()
