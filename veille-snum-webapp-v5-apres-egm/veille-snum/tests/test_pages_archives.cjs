// Fonctions pures de pages/archives.js (index des collectes archivées), chargées par vm sans DOM.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
function load() {
 // URLSearchParams est fourni par le navigateur, pas par le contexte vm.
 const ctx = {window: {}, URLSearchParams};
 for (const name of ['selection.js', 'github.js', 'archives.js']) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return ctx.window.VeilleArchives;
}
const A = load();
const plain = value => JSON.parse(JSON.stringify(value));
const BASE = 'https://raw.githubusercontent.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/donnees-veille/';
const ENTRY = {id: '2026-11-13_43514452853', run_id: 43514452853, edition_date: '2026-11-13', window_start: '2026-11-03',
 window_end: '2026-11-13', status: 'partial', articles: 33, candidats: 55, ecartes: 22, archived_at: '2026-11-13T22:00:45Z'};
const index = (collectes, extra = {}) => ({schema_version: 'SNUM_ARCHIVES_V1', collectes, ...extra});

test('identifiant d’archive : expression stricte, rien d’autre', () => {
 assert.equal(A.isArchiveId('2026-11-13_43514452853'), true);
 for (const bad of ['', '2026-11-13', '2026-11-13_', '2026-11-13_12a', '../2026-11-13_1', '2026-11-13_1/', '2026-1-13_1',
  ' 2026-11-13_1', '2026-11-13_1\n', `2026-11-13_${'9'.repeat(40)}`, null, undefined, 42]) assert.equal(A.isArchiveId(bad), false, String(bad));
});

test('adresses d’archive sur la branche donnees-veille, avec paramètre anti-cache', () => {
 assert.equal(A.indexUrl(7), `${BASE}collectes/index.json?t=7`);
 assert.equal(A.archiveUrl(ENTRY.id, 'paquet-v519.json', 8), `${BASE}collectes/${ENTRY.id}/paquet-v519.json?t=8`);
 assert.equal(A.archiveUrl(ENTRY.id, 'candidats-ecartes.json', 'a b'), `${BASE}collectes/${ENTRY.id}/candidats-ecartes.json?t=a%20b`);
 assert.equal(A.archiveUrl(ENTRY.id, 'rapport-collecte.json', 1), `${BASE}collectes/${ENTRY.id}/rapport-collecte.json?t=1`);
 assert.deepEqual(plain(A.FILES.map(f => f.name)), ['paquet-v519.json', 'candidats-ecartes.json', 'rapport-collecte.json']);
 assert.throws(() => A.archiveUrl('../main', 'paquet-v519.json', 1), /ARCHIVE_INVALIDE/);
 assert.throws(() => A.archiveUrl(ENTRY.id, 'index.html', 1), /FICHIER_INVALIDE/);
 assert.equal(A.selectionHref(ENTRY.id), './?collecte=2026-11-13_43514452853');
 assert.throws(() => A.selectionHref('x'), /ARCHIVE_INVALIDE/);
});

test('paramètre ?collecte= : collecte en cours, archive valide ou identifiant refusé', () => {
 assert.deepEqual(plain(A.requested('')), {mode: 'current'});
 assert.deepEqual(plain(A.requested('?autre=1')), {mode: 'current'});
 assert.deepEqual(plain(A.requested(`?collecte=${ENTRY.id}`)), {mode: 'archive', id: ENTRY.id});
 assert.deepEqual(plain(A.requested('?collecte=..%2Fmain')), {mode: 'invalid', value: '../main'});
 assert.deepEqual(plain(A.requested('?collecte=')), {mode: 'invalid', value: ''});
});

test('index : entrées valides gardées dans l’ordre, entrées illisibles écartées et comptées', () => {
 const older = {...ENTRY, id: '2026-11-06_43000000001', run_id: 43000000001, edition_date: '2026-11-06', window_start: '2026-10-30',
  window_end: '2026-11-06', status: 'ready', articles: 1, candidats: 1, ecartes: 0, archived_at: '2026-11-06T09:05:00Z'};
 const bad = [{...ENTRY, id: '../x'}, {...ENTRY, status: 'done'}, {...ENTRY, articles: -1}, {...ENTRY, candidats: 1.5},
  {...ENTRY, window_start: '03/11/2026'}, {...ENTRY, archived_at: 'hier'}, null, 'texte'];
 const got = A.parseIndex(index([ENTRY, ...bad, older]));
 assert.deepEqual(got.collectes.map(c => c.id), [ENTRY.id, older.id]);
 assert.equal(got.ignored, bad.length);
 assert.deepEqual(plain(A.parseIndex(index([]))), {collectes: [], ignored: 0});
 assert.throws(() => A.parseIndex({schema_version: 'AUTRE', collectes: []}), /INDEX_ILLISIBLE/);
 assert.throws(() => A.parseIndex(index('pas une liste')), /INDEX_ILLISIBLE/);
 assert.throws(() => A.parseIndex(null), /INDEX_ILLISIBLE/);
});

test('description d’une collecte en toutes lettres, heure de Paris', () => {
 const d = plain(A.describe(ENTRY));
 assert.deepEqual(d, {
  title: 'Édition du 13 novembre 2026', period: 'Période du 3 novembre 2026 au 13 novembre 2026',
  status: 'Partielle', statusClass: 'fr-badge--warning',
  counts: ['33 articles', '55 candidats', '22 écartés'],
  archived: 'Archivée le 13 novembre 2026 à 23 h 00 (heure de Paris)'});
 const r = plain(A.describe({...ENTRY, status: 'ready', articles: 1, candidats: 0, ecartes: 1, archived_at: '2026-07-01T21:59:00Z'}));
 assert.equal(r.status, 'Complète');
 assert.equal(r.statusClass, 'fr-badge--success');
 assert.deepEqual(r.counts, ['1 article', '0 candidat', '1 écarté']);
 assert.equal(r.archived, 'Archivée le 1 juillet 2026 à 23 h 59 (heure de Paris)');
});

test('page d’archives : mêmes ressources et même politique que la page de sélection, aucun tableau', () => {
 const html = fs.readFileSync(path.join(PAGES, 'archives.html'), 'utf8');
 const index = fs.readFileSync(path.join(PAGES, 'index.html'), 'utf8');
 const csp = s => /<meta http-equiv="Content-Security-Policy" content="([^"]+)">/.exec(s)[1];
 assert.equal(csp(html), csp(index));
 assert.match(html, /<title>Veille SNUM · Archives des collectes<\/title>/);
 assert.match(html, /<link rel="stylesheet" href="dsfr\/dsfr\.min\.css">/);
 for (const name of ['selection.js', 'github.js', 'archives.js']) assert.match(html, new RegExp(`<script src="${name.replace('.', '\\.')}" defer></script>`), name);
 assert.doesNotMatch(html, /<table/);
 assert.doesNotMatch(html, /(href|src)="\/(?!\/)/);
 assert.doesNotMatch(html, /<(script|link)[^>]+(src|href)="https?:/);
 assert.match(index, /<a class="fr-link" href="archives\.html">Archives des collectes<\/a>/);
 assert.match(index, /<script src="archives\.js" defer><\/script>\s*<script src="page\.js" defer><\/script>/);
 for (const source of [html, fs.readFileSync(path.join(PAGES, 'archives.js'), 'utf8')]) {
  assert.doesNotMatch(source, /innerHTML|outerHTML|insertAdjacentHTML|localStorage|sessionStorage|indexedDB|console\./);
  assert.doesNotMatch(source, /\u2014/);
 }
});
