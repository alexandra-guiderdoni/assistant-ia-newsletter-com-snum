// Constats de l'audit du 14 novembre 2026 : run d'une autre personne suivi par erreur, repêchage
// interrompu mal expliqué, article repêché refusé pour une adresse canonique, appels sans délai maximal.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
function load(fetchImpl) {
 const calls = [];
 const ctx = {window: {}, AbortSignal, setTimeout: fn => { fn(); }, fetch: async (url, init) => { calls.push({url, init}); return fetchImpl(url, init, calls.length); }};
 for (const name of ['selection.js', 'github.js', 'rapport.js', 'ecartes.js']) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return {...ctx.window, calls};
}
const reply = (status, body) => ({ok: status >= 200 && status < 300, status, json: async () => body});
const W = load(async () => reply(404));
const G = W.VeilleGithub, E = W.VeilleEcartes;
const plain = value => JSON.parse(JSON.stringify(value));
const FAKE = 'github_pat_FAUXJETONDETEST0123456789';
const SENT = Date.parse('2026-11-14T10:00:00Z');
const run = (id, created_at) => ({id, created_at, html_url: `https://github.com/o/r/actions/runs/${id}`});

test('réponse 204 : un run qui existait avant l’envoi n’est jamais pris pour le nôtre', () => {
 const autre = run(111, '2026-11-14T09:59:40Z'), notre = run(112, '2026-11-14T10:00:01Z');
 assert.equal(G.pickRun([autre], SENT, ['111']), null);
 assert.equal(G.pickRun([notre, autre], SENT, ['111']).id, 112);
 // Sans relevé préalable, l'ancien comportement reste : le plus récent après l'envoi.
 assert.equal(G.pickRun([notre, autre], SENT).id, 112);
});

test('lancement : les runs existants sont relevés avant l’envoi, puis écartés de la recherche', async () => {
 const autre = run(111, new Date(Date.now() - 20000).toISOString());
 let listes = 0;
 const w = load(async (url, init) => {
  if (init.method === 'POST') return reply(204);
  listes += 1;
  // Première lecture (avant l'envoi) et deuxième : seul le run d'une autre personne ; puis le nôtre apparaît.
  return reply(200, {workflow_runs: listes < 3 ? [autre] : [run(112, new Date(Date.now() + 1000).toISOString()), autre]});
 });
 const got = await w.VeilleGithub.dispatch('collecte', {mode: 'titres'}, FAKE);
 assert.equal(got.id, '112');
 assert.equal(w.calls[0].init.method, undefined, 'la liste est lue avant l’envoi');
 assert.equal(w.calls[1].init.method, 'POST');
});

test('lancement : avec un numéro de run dans la réponse, aucune recherche dans la liste après l’envoi', async () => {
 const w = load(async (url, init) => (init.method === 'POST' ? reply(200, {workflow_run_id: 77, html_url: 'https://github.com/o/r/actions/runs/77'}) : reply(200, {workflow_runs: []})));
 assert.equal((await w.VeilleGithub.dispatch('collecte', {mode: 'titres'}, FAKE)).id, '77');
 assert.equal(w.calls.length, 2);
});

test('chaque appel à GitHub et à raw porte un délai maximal', async () => {
 const w = load(async () => reply(200, {workflow_runs: [], status: 'completed', conclusion: 'success', jobs: []}));
 const g = w.VeilleGithub;
 await g.findActive('collecte', '');
 await g.findActive('collecte', FAKE);
 await g.follow('12', FAKE, Date.now(), () => {});
 await g.dispatch('collecte', {mode: 'titres'}, FAKE).catch(() => {});
 await g.readRepechage('12').catch(() => {});
 assert.ok(w.calls.length >= 6);
 for (const c of w.calls) assert.ok(c.init && c.init.signal instanceof AbortSignal, c.url);
 assert.ok(g.CALL_TIMEOUT_MS >= 10000 && g.CALL_TIMEOUT_MS <= 60000);
});

test('appel abandonné après le délai : traité comme GitHub injoignable, suivi perdu et non bloqué', async () => {
 const w = load(async () => { throw new DOMException('The operation timed out.', 'TimeoutError'); });
 await assert.rejects(w.VeilleGithub.follow('12', FAKE, Date.now(), () => {}), err => err.lost === true && /injoignable/.test(err.message));
});

const ARTICLE = {rubric: 'ia', title: 'Titre repêché', source: 'DINUM', publication_date_iso: '2026-11-10', publication_date_long: '10 novembre 2026',
 url: 'https://numerique.gouv.fr/a', fact: 'Fait.', keywords: ['a'], takeaway: 'À retenir.', snum_interest: 'Intérêt.'};
const result = extra => ({schema_version: 'SNUM_REPECHAGE_V1', url: ARTICLE.url, status: 'ok', message: '', article: {...ARTICLE}, ...extra});

test('repêchage interrompu : le motif publié est affiché, pas « une autre adresse »', () => {
 const repli = {schema_version: 'SNUM_REPECHAGE_V1', url: '', status: 'erreur', message: 'Repêchage interrompu avant son résultat : consulter le journal de la tâche.', article: null};
 assert.deepEqual(plain(E.parseRepechage(repli, ARTICLE.url)), {ok: false, message: repli.message});
 // Un résultat réussi ou en erreur pour une autre adresse reste refusé.
 assert.throws(() => E.parseRepechage(result({url: 'https://numerique.gouv.fr/b'}), ARTICLE.url), /autre adresse/);
 assert.throws(() => E.parseRepechage({...repli, url: 'https://numerique.gouv.fr/b'}, ARTICLE.url), /autre adresse/);
 assert.throws(() => E.parseRepechage(result({url: ''}), ARTICLE.url), /autre adresse/);
});

test('article repêché à l’adresse canonique différente : accepté, sous son adresse canonique', () => {
 const canonique = 'https://www.numerique.gouv.fr/a';
 const got = E.parseRepechage(result({article: {...ARTICLE, url: canonique}}), ARTICLE.url);
 assert.equal(got.ok, true);
 assert.equal(got.article.url, canonique);
 for (const bad of ['http://www.numerique.gouv.fr/a', 'javascript:alert(1)', '', 'https://a b']) {
  assert.throws(() => E.parseRepechage(result({article: {...ARTICLE, url: bad}}), ARTICLE.url), /incomplet/, bad);
 }
});

test('fusion : le candidat demandé quitte les écartés même si l’article porte une autre adresse', () => {
 const candidates = [{url: ARTICLE.url, title: 'A'}, {url: 'https://numerique.gouv.fr/b', title: 'B'}];
 const article = {...ARTICLE, url: 'https://www.numerique.gouv.fr/a'};
 const merged = E.merge([], candidates, article, 'r1', ARTICLE.url);
 assert.deepEqual(plain(merged.candidates), [{url: 'https://numerique.gouv.fr/b', title: 'B'}]);
 assert.equal(merged.selection[0].article.url, article.url);
 assert.throws(() => E.merge(merged.selection, candidates, article, 'r2', ARTICLE.url), /DEJA_SELECTIONNE/);
});
