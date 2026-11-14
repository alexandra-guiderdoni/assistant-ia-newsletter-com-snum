// Lancement, suivi et vérification de ce que le site publie : fonctions pures de pages/lancement.js,
// compléments de pages/github.js et de pages/titres.js. Aucun appel réseau : fetch est une doublure.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
// replies : file de réponses de la doublure de fetch ; les attentes (setTimeout) sont immédiates.
function load(replies = []) {
 const calls = [];
 const ctx = {window: {}, setTimeout: fn => { fn(); }, fetch: async (url, init) => {
  calls.push({url, init});
  const next = replies.length > 1 ? replies.shift() : replies[0];
  if (!next || next.fail) throw new TypeError('Failed to fetch');
  return {ok: next.status >= 200 && next.status < 300, status: next.status, json: async () => next.body};
 }};
 for (const name of ['selection.js', 'github.js', 'rapport.js', 'ecartes.js', 'titres.js', 'lancement.js']) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return {...ctx.window, calls};
}
const W = load();
const G = W.VeilleGithub, L = W.VeilleLancement, T = W.VeilleTitres;
const plain = value => JSON.parse(JSON.stringify(value));
const FAKE = 'github_pat_FAUXJETONDETEST0123456789';
const ETAT = {schema_version: 'SNUM_ETAT_V1', phase: 'titres', edition_date: '2026-11-20', window_start: '2026-11-13',
 window_end: '2026-11-20', run_id: 43527276440, candidats: 45, articles: 0};

test('le site publie le résultat de ce run : numéro du run comparé à celui de l’état', () => {
 assert.equal(L.publishedBy(ETAT, '43527276440'), true);
 assert.equal(L.publishedBy(ETAT, 43527276440), true);
 assert.equal(L.publishedBy(ETAT, '43527276441'), false);
 for (const etat of [null, undefined, {}, {run_id: null}, {run_id: undefined}]) assert.equal(L.publishedBy(etat, '1'), false);
});

test('issue d’un run : publié, pas encore visible, publié malgré un échec, échec', () => {
 assert.equal(L.outcome('success', ETAT, ETAT.run_id), 'publie');
 // Cache de GitHub Pages : le run a réussi mais le site sert encore l'état d'un autre run.
 assert.equal(L.outcome('success', {...ETAT, run_id: 1}, ETAT.run_id), 'attente');
 assert.equal(L.outcome('success', null, ETAT.run_id), 'attente');
 // Échec survenu après la publication : les fichiers sont bien ceux de ce run.
 assert.equal(L.outcome('failure', ETAT, ETAT.run_id), 'publie-en-echec');
 assert.equal(L.outcome('failure', {...ETAT, run_id: 1}, ETAT.run_id), 'echec');
 assert.equal(L.outcome('failure', null, ETAT.run_id), 'echec');
});

test('heure de début d’un run en cours, à l’heure de Paris', () => {
 assert.equal(L.sinceText('2026-11-13T23:36:50Z'), ' depuis 0 h 36');
 assert.equal(L.sinceText('2026-07-01T12:05:00Z'), ' depuis 14 h 05');
 for (const bad of ['', null, undefined, 'hier']) assert.equal(L.sinceText(bad), '');
});

test('messages : le suivi perdu ne parle pas d’échec, le cache périmé interdit de relancer', () => {
 const lost = L.TEXT.lost('la collecte', 'GitHub est injoignable.');
 assert.match(lost, /la collecte continue peut-être sur GitHub/);
 assert.match(lost, /rechargez cette page/);
 assert.doesNotMatch(lost, /échec|échoué/);
 assert.match(L.TEXT.stale('Collecte'), /sert encore l’ancienne version/);
 assert.match(L.TEXT.stale('Collecte'), /Ne relancez pas/);
 assert.match(L.TEXT.active(' depuis 14 h 05'), /déjà en cours sur GitHub depuis 14 h 05/);
 assert.match(L.TEXT.active(''), /activez de nouveau le bouton/);
 assert.match(L.TEXT.notice(''), /inutile de la relancer/);
 assert.match(L.TEXT.publishedFailed('échec'), /Rien n’est à relancer/);
 assert.doesNotMatch(Object.values(L.TEXT).map(f => f('x', 'y')).join(' '), /\u2014|workflow|\brun\b/);
});

test('étape en échec nommée dans le libellé de fin', () => {
 const jobs = {jobs: [{name: 'collecte', conclusion: 'failure', steps: [{name: 'Set up job', conclusion: 'success'}, {name: 'Résumés des titres gardés', conclusion: 'failure'}]}]};
 assert.deepEqual(plain(G.failedStep(jobs)), {job: 'collecte', step: 'Résumés des titres gardés'});
 assert.deepEqual(plain(G.progress({status: 'completed', conclusion: 'failure'}, jobs)),
  {state: 'failure', text: 'Terminé sans succès : échec à l’étape « Résumés des titres gardés »', failedJob: 'collecte'});
 // Tâche en échec sans étape détaillée : son nom suffit ; sans tâche, le libellé reste celui d'avant.
 assert.deepEqual(plain(G.failedStep({jobs: [{name: 'collecte', conclusion: 'success'}, {name: 'archivage', conclusion: 'failure', steps: []}]})), {job: 'archivage', step: 'archivage'});
 assert.equal(G.failedStep({jobs: []}), null);
 assert.equal(G.failedStep(null), null);
 assert.deepEqual(plain(G.progress({status: 'completed', conclusion: 'failure'}, null)), {state: 'failure', text: 'Terminé sans succès : échec', failedJob: ''});
 assert.deepEqual(plain(G.progress({status: 'completed', conclusion: 'cancelled'}, {jobs: []})), {state: 'failure', text: 'Terminé sans succès : annulé', failedJob: ''});
});

test('run en cours : le plus récent non terminé, lien limité à github.com', () => {
 const runs = [{id: 9, status: 'completed', conclusion: 'success'}, {id: 8, status: 'in_progress', html_url: 'https://github.com/o/r/actions/runs/8', created_at: '2026-11-13T23:00:00Z'},
  {id: 7, status: 'queued'}];
 assert.deepEqual(plain(G.activeRun(runs)), {id: '8', htmlUrl: 'https://github.com/o/r/actions/runs/8', since: '2026-11-13T23:00:00Z'});
 assert.equal(G.activeRun([{id: 9, status: 'completed'}]), null);
 for (const bad of [null, undefined, {}, 'x', [null, {status: 'queued'}, {id: 'abc', status: 'queued'}]]) assert.equal(G.activeRun(bad), null);
 assert.equal(G.activeRun([{id: 5, status: 'pending', html_url: 'https://evil.example/x'}]).htmlUrl, '');
});

test('recherche d’un run en cours : avec jeton, sans jeton, et silencieuse en cas d’erreur', async () => {
 const body = {workflow_runs: [{id: 8, status: 'queued', html_url: 'https://github.com/o/r/actions/runs/8', created_at: '2026-11-13T23:00:00Z'}]};
 const avec = load([{status: 200, body}]);
 assert.equal((await avec.VeilleGithub.findActive('collecte', FAKE)).id, '8');
 assert.equal(avec.calls[0].url, G.runsListUrl('collecte'));
 assert.equal(avec.calls[0].init.headers.Authorization, `Bearer ${FAKE}`);
 const sans = load([{status: 200, body}]);
 assert.equal((await sans.VeilleGithub.findActive('collecte', '')).id, '8');
 assert.equal(Object.keys(sans.calls[0].init.headers).includes('Authorization'), false);
 for (const reply of [{status: 403}, {status: 401}, {status: 404}, {status: 500}, {fail: true}, {status: 200, body: null}, {status: 200, body: {workflow_runs: 'x'}}]) {
  assert.equal(await load([reply]).VeilleGithub.findActive('collecte', ''), null, JSON.stringify(reply));
 }
});

test('suivi perdu (jeton expiré, réseau coupé) : erreur marquée, distincte d’un échec du run', async () => {
 for (const reply of [{status: 401}, {fail: true}]) {
  const w = load([reply]);
  await assert.rejects(w.VeilleGithub.follow('12', FAKE, Date.now(), () => {}), err => err.lost === true && !err.message.includes(FAKE));
  assert.equal(w.calls.length, 6);   // trois lectures du run et de ses tâches
 }
 // Run terminé en échec : pas une perte de suivi, l'issue est renvoyée.
 const w = load([{status: 200, body: {status: 'completed', conclusion: 'failure', jobs: []}}]);
 const end = await w.VeilleGithub.follow('12', FAKE, Date.now(), () => {});
 assert.equal(end.state, 'failure');
});

test('lancement accepté sans numéro de run (réponse 204) puis liste illisible : suivi perdu, pas un refus', async () => {
 // Liste relevée avant l'envoi, envoi accepté sans numéro, puis liste illisible.
 const w = load([{status: 200, body: {workflow_runs: []}}, {status: 204}, {status: 500}]);
 await assert.rejects(w.VeilleGithub.dispatch('collecte', {mode: 'titres'}, FAKE), err => err.lost === true);
 const refuse = load([{status: 401}]);
 await assert.rejects(refuse.VeilleGithub.dispatch('collecte', {mode: 'titres'}, FAKE), err => !err.lost && /erreur 401/.test(err.message));
});

test('titres affichés et site en ligne : inchangé, paquet publié depuis, ou autres titres', () => {
 const shown = T.parseEtat(ETAT);
 assert.equal(T.moved(shown, T.parseEtat(ETAT)), '');
 assert.equal(T.moved(shown, null), '');
 assert.equal(T.moved(null, shown), '');
 assert.equal(T.moved(shown, T.parseEtat({...ETAT, phase: 'resumes', run_id: 2})), 'paquet');
 assert.equal(T.moved(shown, T.parseEtat({...ETAT, phase: 'collecte', run_id: 3})), 'paquet');
 assert.equal(T.moved(shown, T.parseEtat({...ETAT, run_id: 4})), 'titres');
 assert.equal(T.moved(shown, T.parseEtat({...ETAT, window_start: '2026-11-12'})), 'titres');
 assert.match(T.MOVED.paquet, /repêchables/);
 assert.match(T.MOVED.titres, /refaites votre sélection/);
});

test('sélection trop volumineuse pour GitHub refusée avant l’envoi', () => {
 const url = n => `https://www.numerique.gouv.fr/${'a'.repeat(1000)}${n}`;
 const big = Array.from({length: 60}, (_, i) => ({url: url(i), rubrique: ''}));
 assert.throws(() => T.resumesInputs(T.parseEtat(ETAT), big), /SELECTION_TROP_VOLUMINEUSE/);
 // Soixante adresses de la longueur maximale observée (201 caractères) passent largement.
 const real = Array.from({length: 60}, (_, i) => ({url: `https://acteurspublics.fr/articles/${'b'.repeat(165)}${String(i).padStart(2, '0')}`, rubrique: 'numerique'}));
 const inputs = T.resumesInputs(T.parseEtat(ETAT), real);
 assert.ok(JSON.stringify(inputs).length < 65535 / 3, String(JSON.stringify(inputs).length));
 assert.ok(T.MAX_SELECTION_CHARS + 200 < 65535);
});

test('durée annoncée : prudente, et limite d’Albert signalée au-delà d’une trentaine d’articles', () => {
 assert.equal(T.durationText(10), 'Comptez une à deux minutes pour dix articles, puis environ deux minutes de publication.');
 assert.equal(T.durationText(30), T.durationText(1));
 assert.match(T.durationText(31), /Albert s’arrête après six minutes/);
 assert.match(T.durationText(60), /restent repêchables/);
});

test('page : marche à suivre du jeton liée et présente dans le dépôt, annonce de remise à zéro, libellé des écartés', () => {
 const html = fs.readFileSync(path.join(PAGES, 'index.html'), 'utf8');
 const doc = /id="gh-token-doc" href="https:\/\/github\.com\/alexandra-guiderdoni\/assistant-ia-newsletter-com-snum\/blob\/main\/([^"]+)" target="_blank" rel="noopener noreferrer">([^<]+)</.exec(html);
 assert.ok(doc, 'lien vers la marche à suivre du jeton');
 assert.match(doc[2], /nouvelle fenêtre/);
 assert.ok(fs.existsSync(path.join(__dirname, '../../..', doc[1])), doc[1]);
 assert.match(html, /<div id="reset-status" class="fr-sr-only" role="status"><\/div>/);
 assert.match(html, />Candidats écartés<\/button>/);
 assert.doesNotMatch(html + fs.readFileSync(path.join(PAGES, 'ecartes.js'), 'utf8'), /écartés par Albert \(|écartés par Albert<|écartés par Albert'/);
 assert.match(html, /<script src="archives\.js" defer><\/script>\s*<script src="lancement\.js" defer><\/script>\s*<script src="page\.js" defer><\/script>/);
 // Les durées annoncées par la page sont celles du code.
 assert.match(html, /trois à quatre minutes/);
 assert.match(html, /de cinq à neuf minutes/);
 assert.doesNotMatch(html + fs.readFileSync(path.join(PAGES, 'page.js'), 'utf8'), /environ huit minutes|environ trois minutes/);
});
