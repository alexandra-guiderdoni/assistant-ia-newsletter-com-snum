// Constats faibles de l'audit du 14 novembre 2026 : données inattendues et messages techniques sur la page.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
function load(fetchImpl) {
 const ctx = {window: {}, AbortSignal, setTimeout: fn => { fn(); }, fetch: async (url, init) => fetchImpl(url, init)};
 for (const name of ['selection.js', 'github.js', 'rapport.js', 'ecartes.js', 'titres.js', 'archives.js', 'lancement.js']) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return ctx.window;
}
const W = load(async () => ({ok: false, status: 404}));
const G = W.VeilleGithub, R = W.VeilleRapport, E = W.VeilleEcartes, L = W.VeilleLancement;
const FAKE = 'github_pat_FAUXJETONDETEST0123456789';

test('progression : tâche ou étape nulle dans la réponse de GitHub, sans plantage', () => {
 assert.equal(G.progress({status: 'in_progress'}, {jobs: [null]}).text, 'Exécution en cours');
 assert.equal(G.progress({status: 'in_progress'}, {jobs: [null, {name: 'collecte', status: 'in_progress', steps: [null, {name: 'Étape A', status: 'in_progress'}]}]}).text, 'Étape en cours : Étape A');
 assert.equal(G.failedStep({jobs: [null, {name: 'collecte', conclusion: 'failure', steps: [null]}]}).step, 'collecte');
});

test('résultat de repêchage qui n’est pas du JSON : message en français', async () => {
 const w = load(async () => ({ok: true, status: 200, json: async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); }}));
 await assert.rejects(w.VeilleGithub.readRepechage('12'), err => /Résultat du repêchage illisible/.test(err.message) && !/Unexpected token/.test(err.message));
});

test('envoi resté sans réponse : la demande a pu partir, la page ne dit pas « non lancée »', async () => {
 const w = load(async (url, init) => { if (init.method === 'POST') throw new TypeError('Failed to fetch'); return {ok: true, status: 200, json: async () => ({workflow_runs: []})}; });
 await assert.rejects(w.VeilleGithub.dispatch('collecte', {mode: 'titres'}, FAKE), err => err.lost === true && /a pu partir/.test(err.message));
 // Un refus explicite de GitHub reste un refus.
 const refus = load(async (url, init) => (init.method === 'POST' ? {ok: false, status: 403} : {ok: true, status: 200, json: async () => ({workflow_runs: []})}));
 await assert.rejects(refus.VeilleGithub.dispatch('collecte', {mode: 'titres'}, FAKE), err => !err.lost && /erreur 403/.test(err.message));
});

test('rapport : éléments inattendus dans les listes ignorés, nom de fichier sans « undefined »', () => {
 assert.deepEqual(JSON.parse(JSON.stringify(R.rows([null, 'texte', {a: 1}, 3, {b: 2}]))), [{a: 1}, {b: 2}]);
 assert.deepEqual(JSON.parse(JSON.stringify(R.rows(null))), []);
 assert.equal(R.fileName({edition_date: '2026-11-14'}), 'veille-snum-rapport-2026-11-14.json');
 for (const bad of [{}, {edition_date: 3}, {edition_date: '../x'}]) assert.equal(R.fileName(bad), 'veille-snum-rapport.json');
});

test('repêchage : un code interne n’est jamais affiché tel quel', () => {
 assert.match(E.readable('DATE_INVALIDE'), /période de la collecte est illisible/);
 assert.match(E.readable('RUBRIQUE_INVALIDE'), /Rechargez la page/);
 assert.equal(E.readable('GitHub est injoignable : vérifiez la connexion réseau puis réessayez.'), 'GitHub est injoignable : vérifiez la connexion réseau puis réessayez.');
});

test('message de collecte déjà en cours : dit ce que GitHub fait vraiment d’une demande en attente', () => {
 const text = L.TEXT.active('');
 assert.match(text, /attendra la fin de celle en cours/);
 assert.match(text, /annule/);
 assert.doesNotMatch(text, /attendra son tour/);
});

test('archives : lectures bornées par le délai maximal', () => {
 const source = fs.readFileSync(path.join(PAGES, 'archives.js'), 'utf8');
 assert.equal((source.match(/fetch\(/g) || []).length, 2);
 assert.equal((source.match(/G\.timed\(\{cache: 'no-store'\}\)/g) || []).length, 2);
});

test('page : chargement initial protégé, lien absent pour une adresse non https', () => {
 const page = fs.readFileSync(path.join(PAGES, 'page.js'), 'utf8');
 assert.match(page, /load\(''\)\.then\([^\n]*\)\.catch\(/);
 const ecartes = fs.readFileSync(path.join(PAGES, 'ecartes.js'), 'utf8');
 assert.doesNotMatch(ecartes, /if \(c\.url\) \{\s*const p = el\('p', 'fr-mb-1w'\);/);
});

test('progression : les étapes techniques de GitHub ne sont pas montrées telles quelles', () => {
 const run = {status: 'in_progress'};
 const job = name => ({jobs: [{name: 'collecte', status: 'in_progress', steps: [{name, status: 'in_progress'}]}]});
 for (const name of ['Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1', 'Set up job', 'Post Run actions/checkout@3d3c', 'Complete job']) {
  assert.equal(G.progress(run, job(name)).text, 'Préparation de la tâche', name);
 }
 assert.equal(G.progress(run, job('Collecte et paquet V519')).text, 'Étape en cours : Collecte et paquet V519');
 assert.equal(G.progress(run, {jobs: [{name: 'archivage', status: 'in_progress', steps: [{name: 'Archiver la collecte', status: 'in_progress'}]}]}).text, 'Étape en cours : Archiver la collecte');
});
