"""Interface sur les composants officiels DSFR 1.15.4, servis localement (hors ligne, CSP stricte)."""

import hashlib
import json
import re
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from veille_snum import web

ROOT = Path(web.__file__).parent
PAGE = (ROOT / "index.html").read_text(encoding="utf-8")
SCRIPT = (ROOT / "app.js").read_text(encoding="utf-8")


class PageDsfrTests(unittest.TestCase):
    def test_feuille_et_scripts_dsfr_locaux(self):
        self.assertIn('<link rel="stylesheet" href="/dsfr/dsfr.min.css">', PAGE)
        self.assertIn(
            '<script type="module" src="/dsfr/dsfr.module.min.js"></script>', PAGE
        )
        self.assertNotRegex(PAGE, r'(href|src)="https?://[^"]*(cdn|jsdelivr|unpkg)')

    def test_enveloppe_de_page_dsfr(self):
        for expected in (
            'class="fr-skiplinks"',
            '<header role="banner" class="fr-header">',
            '<main id="contenu"',
            'class="fr-footer" role="contentinfo" id="footer"',
            'class="fr-header__service-title"',
            'class="fr-container"',
        ):
            self.assertIn(expected, PAGE)
        self.assertNotIn(
            "fr-header__logo", PAGE
        )  # mode neutre : pas de bloc marque sans droit d'usage
        self.assertNotIn('href="#"', PAGE)
        self.assertEqual(len(re.findall(r"<h1\b", PAGE)), 1)
        self.assertIn('<html lang="fr" dir="ltr"', PAGE)

    def test_composants_officiels_dans_le_formulaire(self):
        for field in ("edition", "start", "end", "albert-key", "albert-model"):
            self.assertRegex(
                PAGE,
                rf'<div class="fr-input-group"[^>]*>\s*<label class="fr-label" for="{field}">',
            )
            self.assertRegex(PAGE, rf'<input class="fr-input"[^>]*id="{field}"')
        self.assertRegex(PAGE, r'class="fr-checkbox-group[ "]')
        self.assertIn('class="fr-fieldset"', PAGE)
        self.assertIn('class="fr-accordion"', PAGE)
        self.assertRegex(PAGE, r'<button class="fr-btn" id="collect" type="submit">')
        self.assertRegex(
            PAGE,
            r'id="notice" class="fr-alert fr-alert--info fr-alert--sm" role="status"',
        )

    def test_pas_de_feuille_de_style_maison(self):
        styles = re.findall(r"<style>(.*?)</style>", PAGE, re.DOTALL)
        self.assertLessEqual(sum(len(s) for s in styles), 200)
        self.assertNotIn("--background", "".join(styles))

    def test_elements_dynamiques_en_composants_dsfr(self):
        for expected in (
            "fr-checkbox-group",
            "fr-select-group",
            "fr-select",
            "fr-btn fr-btn--secondary fr-btn--sm",
            "fr-alert--error",
            "fr-alert--info",
        ):
            self.assertIn(expected, SCRIPT)


class AssetsDsfrTests(unittest.TestCase):
    def test_version_et_empreintes_des_fichiers_embarques(self):
        manifest = json.loads(
            (ROOT / "dsfr" / "MANIFEST.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["package"], "@gouvfr/dsfr")
        self.assertEqual(manifest["version"], "1.15.4")
        for rel, digest in manifest["files"].items():
            with self.subTest(rel=rel):
                self.assertEqual(
                    hashlib.sha256((ROOT / "dsfr" / rel).read_bytes()).hexdigest(),
                    digest,
                )
        css = (ROOT / "dsfr" / "dsfr.min.css").read_text(encoding="utf-8")
        for url in set(re.findall(r"url\(([^)]+)\)", css)):
            url = url.strip("'\"")
            if not url.startswith("data:"):
                self.assertTrue((ROOT / "dsfr" / url).resolve().is_file(), url)


class ServiceDsfrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
        cls.port = cls.server.server_address[1]
        cls.patch = mock.patch.object(web, "PORT", cls.port)
        cls.patch.start()
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.patch.stop()

    def get(self, path):
        req = Request(
            f"http://127.0.0.1:{self.port}{path}",
            headers={"Host": f"127.0.0.1:{self.port}"},
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, response.headers, response.read()
        except HTTPError as exc:
            return exc.code, exc.headers, b""

    def test_fichiers_dsfr_servis_avec_le_bon_type(self):
        for path, kind in (
            ("/dsfr/dsfr.min.css", "text/css"),
            ("/dsfr/dsfr.module.min.js", "text/javascript"),
            ("/dsfr/fonts/Marianne-Regular.woff2", "font/woff2"),
            ("/dsfr/favicon/favicon.svg", "image/svg+xml"),
        ):
            with self.subTest(path=path):
                code, headers, body = self.get(path)
                self.assertEqual(code, 200)
                self.assertTrue(headers["Content-Type"].startswith(kind))
                self.assertGreater(len(body), 100)

    def test_aucune_sortie_du_dossier_dsfr(self):
        for path in (
            "/dsfr/../web.py",
            "/dsfr/%2e%2e/web.py",
            "/dsfr/MANIFEST.json.bak",
            "/dsfr/",
            "/dsfr/dsfr.min.css.map",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.get(path)[0], 404)

    def test_politique_de_securite_autorise_polices_et_icones_locales(self):
        _, headers, _ = self.get("/")
        csp = headers["Content-Security-Policy"]
        self.assertIn("font-src 'self'", csp)
        self.assertIn("img-src 'self' data:", csp)
        self.assertIn("style-src 'self'", csp)
        self.assertIn("script-src 'self'", csp)
        self.assertNotIn("unsafe-eval", csp)


if __name__ == "__main__":
    unittest.main()


class EtiquettesVisiblesTests(unittest.TestCase):
    """RGAA 11.1 : chaque champ créé par le script a une étiquette visible liée par for/id."""

    def test_aucun_champ_nomme_seulement_par_aria_label(self):
        self.assertNotIn("setAttribute('aria-label'", SCRIPT)
        self.assertNotIn('setAttribute("aria-label"', SCRIPT)

    def test_etiquettes_visibles_liees_et_distinctes(self):
        for expected in ("fr-label", "htmlFor", "fr-sr-only", "'Thématique'", "'Garder'"):
            self.assertIn(expected, SCRIPT)


class MetaDescriptionTests(unittest.TestCase):
    def test_description_de_page_presente_et_informative(self):
        match = re.search(r'<meta name="description" content="([^"]+)">', PAGE)
        self.assertIsNotNone(match)
        self.assertGreaterEqual(len(match.group(1)), 50)
        self.assertLessEqual(len(match.group(1)), 160)


class ValiditeAriaTests(unittest.TestCase):
    """HTML valide (RGAA 8.2) : aria-label interdit sur div ou span sans rôle explicite."""

    def test_aria_label_seulement_sur_un_element_qui_le_permet(self):
        for tag, attrs in re.findall(r"<(div|span|p)\b([^>]*)>", PAGE):
            if "aria-label=" in attrs:
                with self.subTest(tag=tag, attrs=attrs.strip()[:60]):
                    self.assertRegex(attrs, r'role="(group|region|navigation|search|list|img)"')


class GrilleEtFormulaireTests(unittest.TestCase):
    CSS = (ROOT / "dsfr" / "dsfr.min.css").read_text(encoding="utf-8")

    def test_classes_utilisees_existent_dans_le_dsfr_embarque(self):
        used = set(re.findall(r'class="([^"]+)"', PAGE))
        used |= set(re.findall(r"className='([^']+)'", SCRIPT))
        names = {c for group in used for c in group.split() if c.startswith("fr-")}
        dead = sorted(c for c in names if not re.search(r"\." + re.escape(c) + r"(?![\w-])", self.CSS))
        self.assertEqual(dead, [])

    def test_grille_de_lecture_et_champs_en_colonnes(self):
        self.assertIn('class="fr-grid-row fr-grid-row--center"', PAGE)
        self.assertIn('class="fr-col-12 fr-col-lg-10"', PAGE)
        self.assertEqual(PAGE.count('class="fr-col-12 fr-col-md-4"'), 3)
        self.assertEqual(PAGE.count('class="fr-col-12 fr-col-md-6"'), 2)
        self.assertIn('<ul id="summary" class="fr-grid-row fr-grid-row--gutters fr-mb-3w"', PAGE)

    def test_mentions_obligatoire_et_facultatif(self):
        self.assertIn("Sauf mention contraire, tous les champs sont obligatoires.", PAGE)
        self.assertEqual(PAGE.count("(facultatif)"), 2)

    def test_validation_differee_avec_messages_relies(self):
        self.assertNotRegex(PAGE, r"<input[^>]*\brequired\b")
        self.assertNotIn("aria-invalid", PAGE)
        for field in ("edition", "start", "end"):
            self.assertIn(f'aria-describedby="{field}-messages"', PAGE)
            self.assertIn(f'<div class="fr-messages-group" id="{field}-messages" aria-live="polite"></div>', PAGE)
        for expected in ("fr-input-group--error", "fr-message fr-message--error", "aria-invalid", "aria-required",
                         "function validateDates", ".focus()"):
            self.assertIn(expected, SCRIPT)

    def test_invite_de_selection_pour_le_repechage(self):
        self.assertIn("Sélectionner une thématique", SCRIPT)
        self.assertIn("fr-select-group--error", SCRIPT)


class TitreDeLienTests(unittest.TestCase):
    """RGAA 6.1 : un title de lien reprend l'intitulé visible, puis le complète."""

    def test_title_reprend_l_intitule_visible(self):
        for attrs, text in re.findall(r"<a ([^>]*)>\s*(.*?)\s*</a>", PAGE, re.S):
            title = re.search(r'title="([^"]*)"', attrs)
            if title:
                with self.subTest(lien=text):
                    visible = " ".join(re.sub(r"<[^>]+>", " ", text).split())
                    self.assertIn(visible, title.group(1))

    def test_liens_nouvelle_fenetre_du_script_signales(self):
        self.assertIn("nouvelle fenêtre", SCRIPT[SCRIPT.index("function line("):SCRIPT.index("function clear(")])



class EspacementsTests(unittest.TestCase):
    def test_statistiques_chiffre_puis_libelle(self):
        block = SCRIPT[SCRIPT.index("const stat=byId('summary')"):SCRIPT.index("for(const id of ['article-list'")]
        self.assertIn("fr-col-6 fr-col-md-4", block)
        self.assertIn("fr-h4 fr-mb-0", block)

    def test_articles_espaces_et_commandes_alignees(self):
        block = SCRIPT[SCRIPT.index("function renderSelection"):SCRIPT.index("function renderRejected")]
        self.assertIn("li.className='fr-mb-3w'", block)
        self.assertIn("fr-grid-row--bottom", block)
