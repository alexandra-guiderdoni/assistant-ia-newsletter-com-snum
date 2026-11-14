// Articles déjà publiés (#34) : fonctions pures de pages/publies.js, chargées par vm sans DOM.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
function load(fetch) {
 const ctx = {window: {}, URLSearchParams, fetch, AbortSignal, setTimeout};
 for (const name of ['selection.js', 'github.js', 'archives.js', 'publies.js']) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return ctx.window.VeillePublies;
}
const P = load();
const plain = value => JSON.parse(JSON.stringify(value));
const entry = (date, run, articles = 5) => ({id: `${date}_${run}`, run_id: run, edition_date: date, window_start: date, window_end: date,
 status: 'ready', articles, candidats: articles, ecartes: 0, archived_at: `${date}T10:00:00Z`});
const packet = (date, urls) => ({schema_version: 'SNUM_PAQUET_RENDU_V519', edition_date: date, edition_date_long: date, window_start: date,
 window_end: date, articles: urls.map(url => ({url})), watch: []});

test('éditions précédentes : antérieures, avec articles, une par date, quatre au plus', () => {
 const collectes = [entry('2026-11-17', 9), entry('2026-11-13', 8), entry('2026-11-13', 7), entry('2026-11-10', 6, 0),
  entry('2026-11-06', 5), entry('2026-11-03', 4), entry('2026-10-30', 3), entry('2026-10-27', 2)];
 // Index le plus récent en premier : pour une même date, la dernière archive fait foi.
 assert.deepEqual(plain(P.previous(collectes, '2026-11-17')).map(e => e.id),
  ['2026-11-13_8', '2026-11-06_5', '2026-11-03_4', '2026-10-30_3']);
 assert.deepEqual(plain(P.previous(collectes, '2026-10-27')), []);
});

test('adresses déjà publiées : date de la plus récente édition, paquets illisibles ignorés', () => {
 const map = P.published([
  {edition_date: '2026-11-13', packet: packet('2026-11-13', ['https://a.fr/1', 'https://a.fr/2'])},
  {edition_date: '2026-11-10', packet: packet('2026-11-10', ['https://a.fr/2', 'https://a.fr/3'])},
  {edition_date: '2026-11-06', packet: {schema_version: 'AUTRE', articles: [{url: 'https://a.fr/4'}]}},
 ]);
 assert.deepEqual(plain([...map.entries()]), [['https://a.fr/1', '2026-11-13'], ['https://a.fr/2', '2026-11-13'], ['https://a.fr/3', '2026-11-10']]);
});

test('mention et bilan en clair', () => {
 assert.equal(P.note('2026-11-13'), 'Déjà publié dans l’édition du 13 novembre 2026');
 assert.equal(P.summary({found: 0, editions: ['2026-11-13', '2026-11-10']}), 'Aucun article déjà publié dans les 2 éditions précédentes archivées.');
 assert.equal(P.summary({found: 3, editions: ['2026-11-13', '2026-11-10']}),
  '3 articles déjà publiés dans les 2 éditions précédentes archivées : signalés par « Déjà publié », non gardés par défaut.');
 assert.equal(P.summary({found: 1, editions: ['2026-11-13']}),
  '1 article déjà publié dans l’édition précédente archivée : signalé par « Déjà publié », non gardé par défaut.');
 assert.equal(P.summary({found: 0, editions: []}), 'Aucune édition précédente archivée : pas de doublon à signaler.');
 assert.match(P.summary({error: true}), /^Vérification des articles déjà publiés impossible : archives injoignables\. La sélection fonctionne normalement\.$/);
});

test('lecture des archives : index puis paquets, sans jeton, une erreur ne bloque rien', async () => {
 const urls = [];
 const responses = {
  'collectes/index.json': {schema_version: 'SNUM_ARCHIVES_V1', collectes: [entry('2026-11-13', 8), entry('2026-11-10', 6)]},
  'collectes/2026-11-13_8/paquet-v519.json': packet('2026-11-13', ['https://a.fr/1']),
 };
 const fake = async (url, options) => {
  urls.push({url, headers: options && options.headers});
  const key = Object.keys(responses).find(k => url.includes(k));
  return key ? {ok: true, status: 200, json: async () => responses[key]} : {ok: false, status: 404, json: async () => ({})};
 };
 const D = load(fake);
 const result = await D.check('2026-11-17');
 assert.deepEqual(plain(result.editions), ['2026-11-13', '2026-11-10']);
 assert.equal(D.dateOf('https://a.fr/1'), '2026-11-13');
 assert.equal(D.dateOf('https://a.fr/2'), '');
 assert.ok(urls.every(u => u.url.startsWith('https://raw.githubusercontent.com/') && !u.headers), 'lecture publique, sans en-tête d’authentification');
 const broken = load(async () => { throw new Error('réseau coupé'); });
 assert.equal((await broken.check('2026-11-17')).error, true);
 assert.equal(broken.dateOf('https://a.fr/1'), '');
});

test('page : module chargé avant page.js, zone d’état annoncée, aucune écriture HTML ni stockage', () => {
 const html = fs.readFileSync(path.join(PAGES, 'index.html'), 'utf8');
 const order = ['github.js', 'publies.js', 'page.js'].map(name => html.indexOf(`<script src="${name}" defer></script>`));
 assert.ok(order.every(i => i > 0) && order[0] < order[1] && order[1] < order[2], 'github.js, puis publies.js, puis page.js');
 assert.match(html, /<div id="publies-status" class="fr-text--sm fr-mb-2w" role="status"><\/div>/);
 const source = fs.readFileSync(path.join(PAGES, 'publies.js'), 'utf8');
 assert.doesNotMatch(source, /innerHTML|outerHTML|insertAdjacentHTML|localStorage|sessionStorage|indexedDB|console\.|\u2014/);
 for (const name of ['publies.js', 'selection.js', 'titres.js', 'page.js']) assert.ok(fs.readFileSync(path.join(PAGES, name), 'utf8').split('\n').length < 300, name);
});
