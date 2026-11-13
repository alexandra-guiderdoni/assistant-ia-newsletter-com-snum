"""Tests HTTP loopback sans appel extérieur ni jeton réel."""
import json
import threading
import unittest
from unittest import mock
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from veille_snum import web

class WebTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1',0),web.Handler)
        cls.port = cls.server.server_address[1]
        cls.patch = mock.patch.object(web,'PORT',cls.port)
        cls.patch.start()
        cls.thread = threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)
        cls.patch.stop()

    def request(self,path='/',method='GET',data=None,origin=None,host=None,content_type='application/json'):
        headers={'Host':host or f'127.0.0.1:{self.port}'}
        if origin is not None:headers['Origin']=origin
        if data is not None:headers['Content-Type']=content_type
        req=Request(f'http://127.0.0.1:{self.port}{path}',method=method,data=data,headers=headers)
        try:
            with urlopen(req,timeout=5) as response:
                return response.status, response.headers, response.read()
        except HTTPError as exc:
            return exc.code, exc.headers, exc.read()

    def test_html_script_external_et_csp(self):
        code,headers,body=self.request()
        self.assertEqual(code,200)
        self.assertIn(b'<script src="/app.js" defer></script>',body)
        self.assertNotIn(b'<script>',body)
        self.assertIn("script-src 'self'",headers['Content-Security-Policy'])
        self.assertNotIn("script-src 'unsafe-inline'",headers['Content-Security-Policy'])
        code,headers,body=self.request('/app.js')
        self.assertEqual(code,200)
        self.assertIn(b'ALBERT_STORAGE_KEY',body)
        self.assertEqual(headers['Cache-Control'],'no-store')

    def test_http_refus_host_et_origine(self):
        code,_,_=self.request(host='www.example.com')
        self.assertEqual(code,403)
        bad=json.dumps({'edition_date':'2026-11-11'}).encode()
        code,_,_=self.request('/api/collect','POST',bad,origin='https://not-ours.example')
        self.assertEqual(code,403)
        code,_,_=self.request('/api/collect','POST',bad,content_type='text/plain')
        self.assertEqual(code,415)

    def test_localstorage_opt_in_server_policy(self):
        with mock.patch.dict('os.environ', {}, clear=True):
            code, _, body = self.request('/api/info')
            self.assertEqual(code, 200)
            self.assertIs(json.loads(body)['secret_persistence_enabled'], False)
        with mock.patch.dict('os.environ', {'SNUM_ALLOW_LOCALSTORAGE':'1'}):
            code, _, body = self.request('/api/info')
            self.assertEqual(code, 200)
            self.assertIs(json.loads(body)['secret_persistence_enabled'], True)

    def test_dates_invalides_sans_collecte(self):
        bad=json.dumps({'edition_date':'2026-11-11','window_start':'2026-11-10','window_end':'2026-11-01'}).encode()
        code,_,body=self.request('/api/collect','POST',bad)
        self.assertEqual(code,400)
        self.assertIn('Période invalide'.encode(),body)

if __name__=='__main__':
    unittest.main()
