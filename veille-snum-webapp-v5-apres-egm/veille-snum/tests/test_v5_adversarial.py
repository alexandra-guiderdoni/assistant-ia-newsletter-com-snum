"""Tests adverses EGM V4 : exclusivement fixtures locales, aucun réseau externe."""
import datetime as dt
import hashlib
import io
import json
from email.message import Message
from pathlib import Path
from unittest import TestCase, mock
from urllib.request import HTTPSHandler, ProxyHandler, build_opener
from urllib.response import addinfourl

from veille_snum import core

START = dt.date(2026, 11, 1)
END = dt.date(2026, 11, 10)
SRC = next(s for s in core.sources() if not s['internal'])
URL = f'https://{SRC["domain"]}/article/veille'
TEXT = ('Cette publication présente une évolution du service numérique et détaille les nouvelles démarches pour les agents publics. ' * 2)


def fixture(meta='', body=TEXT, inside=''):
    return f'<html><head><title>Une information institutionnelle pour la veille SNUM</title>{meta}</head><body><h1>Une information institutionnelle pour la veille SNUM</h1>{inside}<article><p>{body}</p><p>{body}</p></article></body></html>'


def ldjson(obj):
    return '<script type="application/ld+json">' + json.dumps(obj) + '</script>'


class Network:
    def __init__(self, page='', robots='User-agent: *\nAllow: /\n', sitemap='<urlset></urlset>'):
        self.page, self.robots, self.sitemap = page, robots, sitemap
        self.calls = []

    def get(self, url, domain, max_bytes=600_000, timeout=7):
        self.calls.append(url)
        if url.endswith('/robots.txt'):
            return url, self.robots
        if url.endswith('/sitemap.xml'):
            return url, self.sitemap
        if url.endswith('/article/veille'):
            return url, self.page
        if url.endswith('/'):
            return url, '<html><a href="/article/veille">actualité</a></html>'
        raise AssertionError(url)


class PublicationTests(TestCase):
    def test_F02_nested_identifiers_all_inspected(self):
        for identity in (
            {'mainEntityOfPage': {'@id': URL, 'url': f'https://{SRC["domain"]}/other'}},
            {'url': [URL, f'https://{SRC["domain"]}/other'], '@id': URL},
        ):
            with self.subTest(identity=identity):
                page = fixture(ldjson({'@type':'NewsArticle','datePublished':'2026-11-06',**identity}))
                candidates, exclusions, _ = core.discover_source(SRC, START, END, Network(page))
                self.assertEqual(candidates, [])
                self.assertTrue(any('IDENTITE_ARTICLE_CONTRADICTOIRE' in x['reason'] for x in exclusions))

    def test_F02_consistent_identity_fragment_still_allowed(self):
        page=fixture(ldjson({'@type':'NewsArticle','datePublished':'2026-11-06','url':URL,'@id':URL+'#article','mainEntityOfPage':{'@id':URL}}))
        candidates,_,_=core.discover_source(SRC,START,END,Network(page))
        self.assertEqual(len(candidates),1)

    def test_F03_visible_challenge_alert_refused(self):
        page=fixture('<meta property="article:published_time" content="2026-11-06">',inside='<div role="alert">Verify you are human to access this article</div>')
        candidates,exclusions,_=core.discover_source(SRC,START,END,Network(page))
        self.assertEqual(candidates,[])
        self.assertTrue(any('PAGE_VERIFICATION' in x['reason'] for x in exclusions))

    def test_F03_article_quoting_challenge_is_not_blocked(self):
        body='Cet article examine le message « verify you are human » et ses conséquences pour les utilisateurs de lecteurs écran. '*3
        page=fixture('<meta property="article:published_time" content="2026-11-06">',body=body)
        candidates,_,_=core.discover_source(SRC,START,END,Network(page))
        self.assertEqual(len(candidates),1)

    def test_F03_identified_webpage_paywall_blocks(self):
        for restricted in (
            {'@type':'WebPage','@id':URL,'isAccessibleForFree':False},
            {'@type':'WebPage','url':URL,'isAccessibleForFree':'false'},
        ):
            with self.subTest(restricted=restricted):
                meta=ldjson([restricted,{'@type':'NewsArticle','mainEntityOfPage':URL,'datePublished':'2026-11-06'}])
                candidates,exclusions,_=core.discover_source(SRC,START,END,Network(fixture(meta)))
                self.assertEqual(candidates,[])
                self.assertTrue(any('CONTENU_PAYANT' in x['reason'] for x in exclusions))

    def test_F03_secondary_paywall_does_not_block_free_page(self):
        meta=ldjson([{'@type':'WebPage','@id':f'https://{SRC["domain"]}/secondary','isAccessibleForFree':False},
                     {'@type':'NewsArticle','mainEntityOfPage':URL,'datePublished':'2026-11-06'}])
        candidates,_,_=core.discover_source(SRC,START,END,Network(fixture(meta)))
        self.assertEqual(len(candidates),1)


class DiscoveryTests(TestCase):
    def test_F04_robots_denied_sitemap_is_partial(self):
        network=Network(robots='User-agent: *\nDisallow: /sitemap.xml\nAllow: /\n')
        network.get=lambda url,domain,**kw: ((url,network.robots) if url.endswith('robots.txt') else
                         (url,'<html></html>') if url.endswith('/') else (_ for _ in ()).throw(AssertionError(url)))
        _,_,state=core.discover_source(SRC,START,END,network)
        self.assertEqual(state['status'],'partial')
        self.assertEqual(state['robots_denied'],1)
        self.assertEqual(state['sitemap_skipped'],1)
        self.assertIn('/sitemap.xml',state['sitemap_skipped_urls'][0])

    def test_F05_first_child_error_does_not_hide_second(self):
        children=[f'https://{SRC["domain"]}/sitemap-{n}.xml' for n in range(core.MAX_SITEMAP_CHILDREN+2)]
        class ChildNetwork(Network):
            def get(self,url,domain,**kw):
                self.calls.append(url)
                if url.endswith('/robots.txt'):return url,self.robots
                if url.endswith('/sitemap.xml'):return url,'<sitemapindex>'+''.join(f'<sitemap><loc>{u}</loc></sitemap>' for u in children)+'</sitemapindex>'
                if url.endswith('/sitemap-0.xml'):raise TimeoutError('child unavailable')
                if url.endswith('/sitemap-1.xml'):return url,f'<urlset><url><loc>{URL}</loc></url></urlset>'
                if '/sitemap-' in url:return url,'<urlset></urlset>'
                if url==URL:return url,self.page
                if url.endswith('/'):return url,'<html></html>'
                raise AssertionError(url)
        network=ChildNetwork(fixture('<meta property="article:published_time" content="2026-11-06">'))
        candidates,_,state=core.discover_source(SRC,START,END,network)
        cap=core.MAX_SITEMAP_CHILDREN
        self.assertIn(children[1],network.calls)
        self.assertNotIn(children[cap],network.calls)
        self.assertEqual(len(candidates),1)
        self.assertEqual(state['discovery_errors'],1)
        self.assertIn(children[cap],state['sitemap_skipped_urls'])
        self.assertIn(children[cap+1],state['sitemap_skipped_urls'])

    def test_F09_budget_exception_propagates_through_robots(self):
        class BudgetNetwork(Network):
            def get(self,*args,**kwargs):raise core.BudgetExceeded('expired')
        with self.assertRaises(core.BudgetExceeded):
            core.robots_allowed(BudgetNetwork(), SRC['homepage'],SRC['domain'],SRC['homepage'])
        _,_,state=core.discover_source(SRC,START,END,BudgetNetwork())
        self.assertEqual(state['status'],'skipped_budget')

    def test_F09_redirect_cannot_dispatch_after_deadline(self):
        clock=[179.0]
        class Transport(HTTPSHandler):
            def __init__(self):super().__init__();self.calls=[]
            def https_open(self,req):
                self.calls.append((req.full_url,clock[0],req.timeout))
                headers=Message();headers['Content-Type']='text/html; charset=utf-8'
                if len(self.calls)==1:
                    clock[0]=181.0
                    headers['Location']=f'https://{SRC["domain"]}/other'
                    response=addinfourl(io.BytesIO(b''),headers,req.full_url,302)
                else:
                    response=addinfourl(io.BytesIO(b'<html></html>'),headers,req.full_url,200)
                response.msg='OK';return response
        transport=Transport()
        def factory(*handlers):return build_opener(ProxyHandler({}),*handlers,transport)
        with mock.patch.object(core,'build_opener',side_effect=factory), mock.patch.object(core.time,'monotonic',side_effect=lambda:clock[0]):
            with self.assertRaises(core.BudgetExceeded):
                core.DeadlineClient(core.HttpClient(),180.0).get(URL,SRC['domain'])
        self.assertEqual(len(transport.calls),1)

    def test_R01_report_has_window_and_version_without_albert(self):
        network=Network()
        with mock.patch.object(core,'sources',return_value=[SRC]):
            result=core.collect({'edition_date':'2026-11-11','window_start':'2026-11-01','window_end':'2026-11-10'},client=network)
        for field in ('edition_date','window_start','window_end','started_at_utc','collector_version','collector_sha256'):
            self.assertIn(field,result)
        self.assertEqual(result['window_end'],'2026-11-10')
        self.assertEqual(result['collector_sha256'],hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest())
        self.assertIsNone(result['packet'])
