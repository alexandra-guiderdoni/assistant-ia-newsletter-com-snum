"""Reproductions indépendantes des écarts F01, F02, F03, F04, F09 (réseau simulé)."""
import datetime as dt
import json
import hashlib
from pathlib import Path
import unittest
from unittest import mock
from urllib.error import HTTPError

from veille_snum import core

DATE = dt.date(2026, 11, 6)
START, END = dt.date(2026, 11, 1), dt.date(2026, 11, 10)
SRC = next(s for s in core.sources() if not s['internal'])
URL = f'https://{SRC["domain"]}/article/veille'
P = 'Cette publication officielle décrit les obligations de l’administration et les évolutions du service numérique accessible. '


def page_markup(metadata='', aside='', heading='Un article de veille SNUM', body=None):
    body = body or P * 3
    return f'<html><head><title>{heading}</title>{metadata}</head><body><h1>{heading}</h1><article>{aside}<p>{body}</p><p>{body}</p></article></body></html>'


class FakeNetwork:
    def __init__(self, article, sitemap_failure=False, homepage_links=True):
        self.article = article
        self.sitemap_failure = sitemap_failure
        self.homepage_links = homepage_links
        self.calls = []

    def get(self, url, domain, max_bytes=600_000, timeout=7):
        self.calls.append(url)
        if url.endswith('/robots.txt'):
            return url, 'User-agent: *\nAllow: /\n'
        if url.endswith('/sitemap.xml'):
            if self.sitemap_failure:
                raise TimeoutError('sitemap indisponible')
            return url, '<urlset></urlset>'
        if url.endswith('/article/veille'):
            return url, self.article
        if url.endswith('/'):
            href = '<a href="/article/veille">Actualité</a>' if self.homepage_links else ''
            return url, f'<html><body>{href}</body></html>'
        raise AssertionError(url)


class DateIntegrityTests(unittest.TestCase):
    def test_article_jsonld_identifiants_contradictoires_refuses(self):
        meta = '<script type="application/ld+json">' + json.dumps({
            '@type':'NewsArticle', 'url': f'https://{SRC["domain"]}/autre',
            'mainEntityOfPage':URL, 'datePublished':'2026-11-06'}) + '</script>'
        client = FakeNetwork(page_markup(meta))
        c, ex, _ = core.discover_source(SRC, START, END, client)
        self.assertEqual(c, [])
        self.assertTrue(any('IDENTITE_ARTICLE_CONTRADICTOIRE' in x['reason'] for x in ex))

    def test_date_aside_ne_qualifie_pas(self):
        content = page_markup(aside='<aside><time itemprop="datePublished" datetime="2026-11-06">06/11</time></aside>')
        c, ex, _ = core.discover_source(SRC, START, END, FakeNetwork(content))
        self.assertFalse(c)
        self.assertTrue(any('DATE_PUBLICATION_ABSENTE' in x['reason'] for x in ex))

    def test_date_de_page_principale_et_fragment_retenue(self):
        meta = '<script type="application/ld+json">' + json.dumps({
            '@type':'NewsArticle', 'url':URL, '@id':URL+'#article',
            'mainEntityOfPage':{'@id':URL}, 'datePublished':'2026-11-06'}) + '</script>'
        c, _, _ = core.discover_source(SRC, START, END, FakeNetwork(page_markup(meta)))
        self.assertEqual(len(c),1)
        self.assertEqual(c[0]['publication_date_iso'],'2026-11-06')


class ReadabilityTests(unittest.TestCase):
    def test_page_challenge_court_h1_refusee(self):
        meta = '<meta property="article:published_time" content="2026-11-06">'
        c, ex, _ = core.discover_source(SRC, START, END, FakeNetwork(page_markup(meta, heading='Verify you are human')))
        self.assertFalse(c)
        self.assertTrue(any('PAGE_VERIFICATION_OU_CAPTCHA' in x['reason'] for x in ex))

    def test_article_sur_captcha_ne_devient_pas_challenge(self):
        meta = '<meta property="article:published_time" content="2026-11-06">'
        c, _, _ = core.discover_source(SRC, START, END, FakeNetwork(page_markup(meta, heading='Une analyse des systèmes CAPTCHA')))
        self.assertEqual(len(c),1)

    def test_paywall_jsonld_refuse(self):
        meta = '<script type="application/ld+json">' + json.dumps({
            '@type':'NewsArticle', 'mainEntityOfPage':URL,'datePublished':'2026-11-06',
            'isAccessibleForFree':False}) + '</script>'
        c, ex, _ = core.discover_source(SRC, START, END, FakeNetwork(page_markup(meta)))
        self.assertFalse(c)
        self.assertTrue(any('CONTENU_PAYANT' in x['reason'] for x in ex))


class DiscoveryStatusTests(unittest.TestCase):
    def test_panne_sitemap_et_aucun_lien_produit_reserve(self):
        client=FakeNetwork('', sitemap_failure=True, homepage_links=False)
        c, ex, state = core.discover_source(SRC, START, END, client)
        self.assertEqual(c, [])
        self.assertEqual(state['status'],'partial')
        self.assertEqual(state['discovery_errors'],1)
        self.assertEqual(state['technical_errors'],0)

    def test_pannes_sitemaps_toutes_sources_pas_ready(self):
        client=FakeNetwork('', sitemap_failure=True, homepage_links=False)
        with mock.patch.object(core,'sources',return_value=[{**s, 'homepage': f'https://{s["domain"]}/'} if not s['internal'] else s for s in core.sources()]):
            report=core.collect({'edition_date':'2026-11-11','window_start':'2026-11-01','window_end':'2026-11-10'},client=client,summarize=lambda _: None)
        self.assertEqual(report['status'],'partial')
        self.assertEqual(report['packet']['articles'],[])
        self.assertTrue(any(x['title']=='Sources non couvertes' for x in report['packet']['watch']))

    def test_absence_de_lien_et_sitemap_vide_sans_erreur_reste_vide_valide(self):
        _,_,state=core.discover_source(SRC, START, END, FakeNetwork('',homepage_links=False))
        self.assertEqual(state['status'],'checked')
        self.assertEqual(state['discovery_errors'],0)

    def test_budget_ne_demarre_pas_nouvelle_requete_apres_echeance(self):
        current=[0.0]
        class SlowHttp(FakeNetwork):
            def get(self,*args,**kwargs):
                if current[0]>=180.0:
                    raise AssertionError('Requête lancée après échéance')
                current[0]+=55.0
                return super().get(*args,**kwargs)
        with mock.patch.object(core.time,'monotonic',side_effect=lambda:current[0]):
            report=core.collect({'edition_date':'2026-11-11','window_start':'2026-11-01','window_end':'2026-11-10'},client=SlowHttp('',homepage_links=False),summarize=lambda _: None)
        self.assertEqual(report['status'],'partial')
        self.assertTrue(any(s['status']=='skipped_budget' for s in report['sources']))


class InvariantTests(unittest.TestCase):
    def test_configuration_octets_identiques_a_v3(self):
        payload=Path(core.ROOT/'sources.json').read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(),'292ea241e892829b75e1b0f71af4f9396bd48ddb56a0bb3739579f6eafdd76c9')

    def test_redirections_refusees(self):
        redirect=core.NoAlbertRedirect()
        for code in (301,302,303,307,308):
            with self.subTest(code=code), self.assertRaisesRegex(ValueError,'ALBERT_REDIRECTION_REFUSEE'):
                redirect.redirect_request(None,None,code,'','', 'http://other.example/')


if __name__=='__main__':
    unittest.main()
