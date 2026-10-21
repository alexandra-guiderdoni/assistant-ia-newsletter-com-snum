"""Recette déterministe du canal de courriel ; les deux kits historiques restent figés."""

import base64
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
FIXTURE = PROJECT / "tests/fixtures/mail-dsfr/edition-2026-10-14.json"


class MailTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(FIXTURE.read_text())
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def render(self, payload, script="newsletter_mail.py"):
        source = self.folder / "packet.json"
        output = self.folder / "mail.html"
        source.write_text(json.dumps(payload), encoding="utf-8")
        command = [
            sys.executable,
            str(PROJECT / "scripts" / script),
            "build",
            "--input",
            str(source),
            "--output",
            str(output),
        ]
        if script == "newsletter_html.py":
            command += [
                "--template",
                str(PROJECT / "_source/05-BLOCS-HTML-CANONIQUES.md"),
            ]
        result = subprocess.run(
            command, check=False, capture_output=True, text=True, cwd=PROJECT
        )
        return result, output.read_text() if output.exists() else ""

    def test_supplied_edition_and_outside_date_are_preserved(self):
        result, html = self.render(self.payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(html.count("data-article-link="), 5)
        self.assertEqual(html.count('aria-hidden="true"'), 8)
        self.assertIn('datetime="2026-10-15"', html)
        self.assertNotIn("Hors période", html)
        self.assertNotIn("@@", html)
        self.assertNotIn("<script", html)
        self.assertNotIn(
            self.payload["watch"][0]["summary"].replace("'", "&#x27;"), html
        )
        self.assertNotIn("À surveiller", html)
        self.assertEqual(html.count("ESSENTIEL</p>"), 3)

    def test_original_web_renderer_still_rejects_outside_window(self):
        result, _ = self.render(self.payload, "newsletter_html.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hors fenêtre", result.stderr)

    def test_empty_packet_with_and_without_watch(self):
        self.payload["articles"] = []
        for watch in [[], self.payload["watch"]]:
            with self.subTest(watch=bool(watch)):
                self.payload["watch"] = watch
                result, html = self.render(self.payload)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Collecte à compléter", html)
                self.assertEqual(html.count("<h1"), 1)
                self.assertEqual(html.count("data-article-link="), 0)
                self.assertNotIn("À surveiller", html)
                self.assertTrue(html.rstrip().endswith("</html>"))

    def test_variable_article_counts_and_all_five_rubrics(self):
        for count in [1, 2, 3, 18]:
            with self.subTest(count=count):
                articles = []
                for index in range(count):
                    article = copy.deepcopy(self.payload["articles"][0])
                    article.update(
                        id=f"U{index + 1:02d}",
                        url=f"https://example.org/article/{index}",
                        rubric=["bercy", "ia", "commande", "rh", "numerique"][
                            index % 5
                        ],
                        essential=count >= 3 and index < 3,
                    )
                    articles.append(article)
                payload = {**self.payload, "articles": articles, "watch": []}
                result, html = self.render(payload)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(html.count("data-article-link="), count)
                self.assertEqual(html.count("ESSENTIEL</p>"), 3 if count >= 3 else 0)
                self.assertEqual(html.count('<h2 class="text-brand"'), min(count, 5))
                self.assertNotIn("À surveiller", html)
                for article in articles:
                    self.assertEqual(html.count(f'href="{article["url"]}"'), 1)

    def test_untrusted_text_is_escaped_without_rewriting(self):
        self.payload["articles"][0]["title"] = '<script>alert("x")</script> & @@WATCH@@'
        self.payload["articles"][0]["fact"] = "x " * 80
        result, html = self.render(self.payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("<script", html)
        self.assertIn("&lt;script&gt;alert", html)
        self.assertIn("&#64;&#64;WATCH&#64;&#64;", html)
        self.assertIn("x " * 79, html)

    def test_invalid_duplicate_urls_and_ids_are_not_silently_dropped(self):
        for field in ["id", "url"]:
            with self.subTest(field=field):
                payload = copy.deepcopy(self.payload)
                payload["articles"][1][field] = payload["articles"][0][field]
                result, _ = self.render(payload)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("dupliqu", result.stderr)

    def test_generated_shell_reassembles_without_a_byte_change(self):
        source = (PROJECT / "_source/30-BLOCS-MAIL-DSFR.md").read_text()
        page = re.search(r"## PAGE\n\n```html\n(.*?)\n```", source, re.DOTALL)[1]
        pieces = []
        for path in sorted(PROJECT.glob("31-MAIL-DSFR-COQUE-*.md")):
            resource = path.read_text()
            self.assertLessEqual(len(resource), 4500)
            pieces.append(re.search(r"```html\n(.*?)\n```", resource, re.DOTALL)[1])
        self.assertEqual("".join(pieces), page)

    def test_logo_stays_a_complete_png_and_is_not_replaced(self):
        result, html = self.render(self.payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        image = base64.b64decode(
            re.search(r"data:image/png;base64,([^\"]+)", html)[1], validate=True
        )
        self.assertTrue(image.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(len(image), 9024)
        source = (PROJECT / "_source/30-BLOCS-MAIL-DSFR.md").read_text()
        expected = base64.b64decode(
            re.search(r"## LOGO\n\n```html\n(.*?)\n```", source, re.DOTALL)[1]
        )
        self.assertEqual(
            hashlib.sha256(image).hexdigest(), hashlib.sha256(expected).hexdigest()
        )

    def test_logo_resources_reassemble_the_original_binary(self):
        parts = []
        for path in sorted(PROJECT.glob("31-MAIL-DSFR-LOGO-*.md")):
            resource = path.read_text()
            self.assertLessEqual(len(resource), 4500)
            body = re.search(r"```html\n(.*?)\n```", resource, re.DOTALL)[1]
            parts.append(re.sub(r"\s+", "", body))
        encoded = "".join(parts)
        self.assertEqual(len(encoded), 12032)
        self.assertEqual(len(base64.b64decode(encoded, validate=True)), 9024)

    def test_verifier_rejects_changed_logo_style_and_missing_document_type(self):
        result, html = self.render(self.payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        candidate = self.folder / "candidate.html"
        mutations = [
            html.replace("#000091", "#777777", 1),
            html.replace("<!doctype html>", "", 1),
            html.replace("data:image/png;base64,", "data:image/png;base64,AAA", 1),
            html.replace('aria-hidden="true"', 'aria-hidden="false"', 1),
            html.replace("</strong> ", "</strong>", 1),
            html + "<script",
        ]
        for modified in [html, *mutations]:
            with self.subTest(original=modified == html):
                candidate.write_text(modified)
                check = subprocess.run(
                    [
                        sys.executable,
                        str(PROJECT / "scripts/newsletter_mail.py"),
                        "verify",
                        "--input",
                        str(self.folder / "packet.json"),
                        "--html",
                        str(candidate),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                    cwd=PROJECT,
                )
                self.assertEqual(check.returncode == 0, modified == html)


if __name__ == "__main__":
    unittest.main()
