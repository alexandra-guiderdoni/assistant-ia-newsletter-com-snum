// Fonctions pures des modules de la page GitHub (API, rapport, repêchage), chargées par vm sans DOM.
// Aucun appel réseau : seules les requêtes construites et les réponses simulées sont examinées.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
const MODULES = ['selection.js', 'github.js', 'rapport.js', 'ecartes.js', 'lancement.js', 'page.js'];
function load() {
 const ctx = {window: {}};
 for (const name of MODULES) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return ctx.window;
}
const W = load();
const G = W.VeilleGithub, R = W.VeilleRapport, E = W.VeilleEcartes, S = W.VeilleSelection, P = W.VeillePage;
const plain = value => JSON.parse(JSON.stringify(value));
const FAKE = 'github_pat_FAUXJETONDETEST0123456789';
const API = 'https://api.github.com/repos/alexandra-guiderdoni/assistant-ia-newsletter-com-snum';

test('lancement de la collecte : URL, en-têtes et corps attendus par GitHub', () => {
 const req = G.dispatchRequest('collecte', G.collectInputs('2026-11-20', '2026-11-13', '2026-11-20'), FAKE);
 assert.equal(req.url, `${API}/actions/workflows/publier-paquet-snum.yml/dispatches`);
 assert.equal(req.init.method, 'POST');
 assert.deepEqual(plain(req.init.headers), {
  Authorization: `Bearer ${FAKE}`, Accept: 'application/vnd.github+json',
  'X-GitHub-Api-Version': '2026-03-10', 'Content-Type': 'application/json'});
 assert.deepEqual(JSON.parse(req.init.body), {ref: 'main', inputs: {edition: '20/11/2026', debut: '13/11/2026', fin: '20/11/2026'}});
 assert.throws(() => G.collectInputs('20/11/2026', '2026-11-13', '2026-11-20'), /DATE_INVALIDE/);
});

test('repêchage : entrées du workflow, rubrique et adresse contrôlées', () => {
 const inputs = G.repechageInputs('https://www.numerique.gouv.fr/a', 'ia', '2026-11-03', '2026-11-13');
 const req = G.dispatchRequest('repechage', inputs, FAKE);
 assert.equal(req.url, `${API}/actions/workflows/repecher-candidat.yml/dispatches`);
 assert.deepEqual(JSON.parse(req.init.body), {ref: 'main', inputs: {url: 'https://www.numerique.gouv.fr/a', rubrique: 'ia', debut: '2026-11-03', fin: '2026-11-13'}});
 assert.throws(() => G.repechageInputs('https://x.fr/a', 'inconnue', '2026-11-03', '2026-11-13'), /RUBRIQUE_INVALIDE/);
 assert.throws(() => G.repechageInputs('http://x.fr/a', 'ia', '2026-11-03', '2026-11-13'), /URL_INVALIDE/);
});

test('suivi : adresses de run, de tâches, de liste et de résultat public', () => {
 assert.equal(G.runUrl(42), `${API}/actions/runs/42`);
 assert.equal(G.jobsUrl(42), `${API}/actions/runs/42/jobs`);
 assert.equal(G.runsListUrl('collecte'), `${API}/actions/workflows/publier-paquet-snum.yml/runs?event=workflow_dispatch&per_page=5`);
 assert.equal(G.repechageResultUrl(42, 7),
  'https://raw.githubusercontent.com/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/donnees-veille/repechages/42.json?t=7');
 assert.throws(() => G.runUrl('42/../x'), /RUN_INVALIDE/);
 assert.equal(G.tokenLooksValid(FAKE), true);
 assert.equal(G.tokenLooksValid('ghp_court'), false);
 assert.equal(G.tokenLooksValid('ghp_AAAAAAAAAAAAAAAAAAAAAAAA\nX: y'), false);
});

test('réponse 204 : le run retrouvé est le plus récent créé après l’envoi', () => {
 const sent = Date.parse('2026-11-13T10:00:00Z');
 const runs = [
  {id: 3, created_at: '2026-11-13T10:00:04Z'}, {id: 2, created_at: '2026-11-13T10:00:02Z'},
  {id: 1, created_at: '2026-11-13T09:10:00Z'}];
 assert.equal(G.pickRun(runs, sent).id, 3);
 assert.equal(G.pickRun(runs.slice(2), sent), null);
 assert.equal(G.pickRun(undefined, sent), null);
});

test('statuts de run et de tâches traduits en libellés de progression', () => {
 const job = (name, status, steps = []) => ({name, status, steps});
 const step = (name, status) => ({name, status});
 assert.deepEqual(plain(G.progress({status: 'queued'}, null)), {state: 'pending', text: 'En file d’attente sur GitHub Actions'});
 const collecte = job('collecte', 'in_progress', [step('Set up job', 'completed'), step('Collecte et paquet V519', 'in_progress'), step('Résumé du paquet', 'queued')]);
 assert.equal(G.progress({status: 'in_progress'}, {jobs: [collecte]}).text, 'Étape en cours : Collecte et paquet V519');
 const fini = job('collecte', 'completed', [step('Résumé du paquet', 'completed')]);
 assert.equal(G.progress({status: 'in_progress'}, {jobs: [fini, job('deploiement', 'queued')]}).text, 'Déploiement de la page sur GitHub Pages');
 assert.equal(G.progress({status: 'in_progress'}, {jobs: []}).text, 'Exécution en cours');
 assert.deepEqual(plain(G.progress({status: 'completed', conclusion: 'success'}, null)), {state: 'success', text: 'Terminé avec succès'});
 const echec = G.progress({status: 'completed', conclusion: 'failure'}, null);
 assert.equal(echec.state, 'failure');
 assert.match(echec.text, /échec/);
 assert.match(G.progress({status: 'completed', conclusion: 'cancelled'}, null).text, /annulé/);
 assert.equal(G.elapsed(65000), '1 min 05 s');
 assert.equal(G.elapsed(4000), '0 min 04 s');
});

test('erreurs HTTP de GitHub en français, sans jeton', () => {
 for (const status of [401, 403, 404, 422, 500]) {
  const message = G.httpError(status);
  assert.match(message, new RegExp(String(status)));
  assert.doesNotMatch(message, /github_pat|Bearer/);
 }
 assert.match(G.httpError(401), /jeton/i);
 assert.match(G.httpError(403), /pas le droit de lancer une tâche/);
 assert.match(G.httpError(404), /ne donne pas accès au dépôt/);
 assert.match(G.httpError(422), /refusé/);
 // Chaque refus lié au jeton renvoie à la marche à suivre proposée par la page.
 for (const status of [401, 403, 404]) assert.match(G.httpError(status), /Jeton GitHub de l’équipe : marche à suivre/);
 assert.doesNotMatch([401, 403, 404, 422, 429, 500].map(G.httpError).join(' '), /workflow|\brun\b|branche main/);
});

const ARTICLE = {rubric: 'ia', title: 'Titre repêché', source: 'DINUM', publication_date_iso: '2026-11-10',
 publication_date_long: '10 novembre 2026', url: 'https://www.numerique.gouv.fr/r', fact: 'Fait.',
 keywords: ['a', 'b', 'c'], takeaway: 'À retenir.', snum_interest: 'Intérêt.'};
const result = (extra = {}) => ({schema_version: 'SNUM_REPECHAGE_V1', url: ARTICLE.url, status: 'ok', message: '', article: {...ARTICLE}, ...extra});

test('résultat de repêchage : article V519 dans l’ordre du paquet, refus lisibles', () => {
 const ok = E.parseRepechage(result(), ARTICLE.url);
 assert.equal(ok.ok, true);
 assert.deepEqual(Object.keys(ok.article), ['id', 'rubric', 'title', 'source', 'publication_date_iso', 'publication_date_long',
  'url', 'fact', 'keywords', 'takeaway', 'snum_interest', 'essential']);
 assert.deepEqual(plain(E.parseRepechage(result({status: 'erreur', message: 'Date hors période', article: null}), ARTICLE.url)),
  {ok: false, message: 'Date hors période'});
 assert.throws(() => E.parseRepechage({...result(), schema_version: 'AUTRE'}, ARTICLE.url), /illisible/);
 assert.throws(() => E.parseRepechage(result(), 'https://www.numerique.gouv.fr/autre'), /autre adresse/);
 assert.throws(() => E.parseRepechage(result({article: {...ARTICLE, rubric: 'sport'}}), ARTICLE.url), /incomplet/);
 assert.throws(() => E.parseRepechage(result({article: {...ARTICLE, keywords: 'a'}}), ARTICLE.url), /incomplet/);
});

test('fusion d’un article repêché : gardé, retiré des écartés, exporté avec identifiants recalculés', () => {
 const packet = {schema_version: 'SNUM_PAQUET_RENDU_V519', edition_date: '2026-11-13', edition_date_long: '13 novembre 2026',
  window_start: '2026-11-03', window_end: '2026-11-13', watch: [],
  articles: [{id: 'U01', ...ARTICLE, rubric: 'numerique', url: 'https://www.numerique.gouv.fr/p', publication_date_iso: '2026-11-12', essential: false}]};
 const selection = packet.articles.map(a => ({article: a, keep: true, rubric: a.rubric, key: '1'}));
 const candidates = [{url: ARTICLE.url, title: 'Titre repêché'}, {url: 'https://x.fr/b', title: 'Autre'}];
 const article = E.parseRepechage(result(), ARTICLE.url).article;
 const merged = E.merge(selection, candidates, article, 'r1');
 assert.equal(merged.selection.length, 2);
 assert.deepEqual(plain(merged.selection[1]), {article: plain(article), keep: true, rubric: 'ia', key: 'r1'});
 assert.deepEqual(merged.candidates.map(c => c.url), ['https://x.fr/b']);
 assert.equal(selection.length, 1);
 const out = plain(S.rebuild(packet, merged.selection));
 assert.deepEqual(out.articles.map(a => [a.id, a.url]), [['U01', 'https://www.numerique.gouv.fr/p'], ['U02', ARTICLE.url]]);
 for (const a of out.articles) assert.deepEqual(Object.keys(a), Object.keys(packet.articles[0]));
 assert.throws(() => E.merge(merged.selection, candidates, article, 'r2'), /DEJA_SELECTIONNE/);
});

const REPORT = {status: 'partial', edition_date: '2026-11-13', discovery_errors: 2,
 sources: [
  {label: 'DINUM', status: 'checked', opened: 10, attempted: 12, not_visited: 3},
  {label: 'Légifrance', status: 'blocked', opened: 0, attempted: 4, not_visited: 0},
  {label: 'Cour des comptes', status: 'partial', opened: 5, attempted: 5, not_visited: 40}],
 candidates: [{}, {}, {}, {}], excluded: [{}, {}], errors: [{}]};

test('compteurs du rapport identiques à la page locale', () => {
 assert.deepEqual(plain(R.stats(REPORT, {articles: [{}, {}, {}]})), [
  ['1/13', 'sources explorées sans réserve'], ['1', 'sources partielles ou plafonnées'],
  ['15/21', 'pages reçues sur pages tentées'], ['43', 'adresses découvertes non visitées'],
  ['4', 'candidats trouvés'], ['3', 'articles préparés'], ['2', 'exclusions et erreurs'], ['2', 'erreurs de plan de site']]);
 assert.equal(R.stats({...REPORT, discovery_errors: undefined}, null)[7][0], '0');
 assert.match(R.sourceLine({label: 'DINUM', status: 'checked', discovered: 9, notes: ['Note']}), /^DINUM : Découverte effectuée · 9 URL découvertes .* Note$/);
 assert.equal(R.statusMessage('ready'), 'Paquet disponible : relecture des sources obligatoire.');
 assert.ok(R.isReport(REPORT));
 assert.ok(!R.isReport({status: 'ready'}));
});

test('formulaire : mêmes contrôles de dates que la page locale', () => {
 assert.deepEqual(plain(P.dateErrors('2026-11-13', '2026-11-06', '2026-11-13')), {});
 assert.deepEqual(Object.keys(P.dateErrors('', '', '')), ['edition', 'start', 'end']);
 assert.match(P.dateErrors('2026-11-13', '2026-11-14', '2026-11-13').end, /postérieure/);
 assert.match(P.dateErrors('2026-11-13', '2026-09-01', '2026-11-13').end, /61 jours/);
});

test('dates par défaut : prochain mardi ou vendredi, période depuis l’envoi précédent (mêmes cas que publier.py)', () => {
 // [jour de lancement, édition, début] ; mois comptés à partir de 0 dans Date.
 const cas = [
  [[2026, 10, 16], '2026-11-17', '2026-11-13'], [[2026, 10, 17], '2026-11-17', '2026-11-13'],
  [[2026, 10, 18], '2026-11-20', '2026-11-17'], [[2026, 10, 19], '2026-11-20', '2026-11-17'],
  [[2026, 10, 20], '2026-11-20', '2026-11-17'], [[2026, 10, 21], '2026-11-24', '2026-11-20'],
  [[2026, 10, 22], '2026-11-24', '2026-11-20'], [[2026, 11, 30], '2027-01-01', '2026-12-29'],
 ];
 for (const [[y, m, d], edition, start] of cas) {
  // 23 h : un lancement tardif reste sur le jour local, sans glisser au lendemain.
  assert.deepEqual(plain(P.defaultDates(new Date(y, m, d, 23, 30))), {edition, start, end: edition}, `${y}-${m + 1}-${d}`);
 }
});

test('aucune écriture HTML, aucun stockage, aucun tiret cadratin, CSP limitée à GitHub', () => {
 const html = fs.readFileSync(path.join(PAGES, 'index.html'), 'utf8');
 for (const name of MODULES) {
  const source = fs.readFileSync(path.join(PAGES, name), 'utf8');
  assert.doesNotMatch(source, /innerHTML|outerHTML|insertAdjacentHTML|localStorage|sessionStorage|indexedDB|console\./, name);
  assert.doesNotMatch(source, /\u2014/, name);
  assert.match(html, new RegExp(`<script src="${name.replace('.', '\\.')}" defer></script>`), name);
 }
 assert.match(html, /connect-src 'self' https:\/\/api\.github\.com https:\/\/raw\.githubusercontent\.com;/);
 assert.match(html, /id="gh-token"[^>]*type="password"[^>]*autocomplete="off"/);
});
