// Collecte en deux temps : fonctions pures de pages/titres.js (état publié, choix de
// l'affichage, sélection envoyée au mode « resumes »), chargées par vm sans DOM.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const PAGES = path.join(__dirname, '../pages');
function load() {
 const ctx = {window: {}};
 for (const name of ['selection.js', 'github.js', 'rapport.js', 'ecartes.js', 'titres.js']) vm.runInNewContext(fs.readFileSync(path.join(PAGES, name), 'utf8'), ctx, {filename: name});
 return ctx.window;
}
const W = load();
const T = W.VeilleTitres, G = W.VeilleGithub, R = W.VeilleRapport;
const plain = value => JSON.parse(JSON.stringify(value));
const FAKE = 'github_pat_FAUXJETONDETEST0123456789';
const ETAT = {schema_version: 'SNUM_ETAT_V1', phase: 'titres', edition_date: '2026-11-20', window_start: '2026-11-13',
 window_end: '2026-11-20', run_id: 123, candidats: 45, articles: 0};

test('état de collecte : schéma, phase et dates contrôlés, sinon absent', () => {
 assert.deepEqual(plain(T.parseEtat(ETAT)), {phase: 'titres', edition_date: '2026-11-20', window_start: '2026-11-13',
  window_end: '2026-11-20', run_id: 123, candidats: 45, articles: 0});
 for (const phase of ['resumes', 'collecte']) assert.equal(T.parseEtat({...ETAT, phase}).phase, phase);
 for (const bad of [null, undefined, 'texte', [], {...ETAT, schema_version: 'AUTRE'}, {...ETAT, phase: 'page seule'},
  {...ETAT, phase: undefined}, {...ETAT, edition_date: '20/11/2026'}, {...ETAT, window_start: ''}, {...ETAT, window_end: null}]) {
  assert.equal(T.parseEtat(bad), null, JSON.stringify(bad));
 }
});

test('affichage selon la phase : titres seulement en phase « titres », page actuelle sinon', () => {
 assert.equal(T.view(null), 'paquet');
 assert.equal(T.view(T.parseEtat(ETAT)), 'titres');
 assert.equal(T.view(T.parseEtat({...ETAT, phase: 'resumes'})), 'paquet');
 assert.equal(T.view(T.parseEtat({...ETAT, phase: 'collecte'})), 'paquet');
});

const entry = (n, keep, rubric = '') => ({url: `https://www.numerique.gouv.fr/${n}`, keep, rubric});

test('sélection : titres gardés dans l’ordre, rubrique imposée ou vide pour Albert', () => {
 const got = plain(T.buildSelection([entry('a', true, 'ia'), entry('b', false, 'rh'), entry('c', true), entry('d', true, 'bercy')]));
 assert.deepEqual(got, [{url: 'https://www.numerique.gouv.fr/a', rubrique: 'ia'}, {url: 'https://www.numerique.gouv.fr/c', rubrique: ''},
  {url: 'https://www.numerique.gouv.fr/d', rubrique: 'bercy'}]);
 for (const r of [...W.VeilleSelection.RUBRICS, '']) assert.equal(T.buildSelection([entry('x', true, r)])[0].rubrique, r);
 // L'ancienne thématique ne se choisit plus pour une nouvelle collecte.
 assert.throws(() => T.buildSelection([entry('x', true, 'numerique')]), /RUBRIQUE_INVALIDE/);
});

test('sélection refusée : vide, plus de 60, rubrique inconnue, adresse non https ou en double', () => {
 assert.throws(() => T.buildSelection([]), /SELECTION_VIDE/);
 assert.throws(() => T.buildSelection([entry('a', false)]), /SELECTION_VIDE/);
 const many = Array.from({length: 61}, (_, i) => entry(i, true));
 assert.throws(() => T.buildSelection(many), /SELECTION_TROP_LONGUE/);
 assert.equal(T.buildSelection(many.slice(0, 60)).length, 60);
 assert.throws(() => T.buildSelection([entry('a', true, 'sport')]), /RUBRIQUE_INVALIDE/);
 assert.throws(() => T.buildSelection([{url: 'http://x.fr/a', keep: true, rubric: ''}]), /URL_INVALIDE/);
 assert.throws(() => T.buildSelection([{url: 'https://x.fr/a b', keep: true, rubric: ''}]), /URL_INVALIDE/);
 assert.throws(() => T.buildSelection([entry('a', true), entry('a', true, 'ia')]), /URL_EN_DOUBLE/);
 // Un doublon non gardé ne gêne pas.
 assert.equal(T.buildSelection([entry('a', true), entry('a', false)]).length, 1);
});

test('mode « resumes » : entrées exactes, dates de l’état au format JJ/MM/AAAA, JSON compact', () => {
 const selection = T.buildSelection([entry('a', true, 'ia'), entry('c', true)]);
 const inputs = plain(T.resumesInputs(T.parseEtat(ETAT), selection));
 assert.deepEqual(inputs, {mode: 'resumes', edition: '20/11/2026', debut: '13/11/2026', fin: '20/11/2026',
  selection: '[{"url":"https://www.numerique.gouv.fr/a","rubrique":"ia"},{"url":"https://www.numerique.gouv.fr/c","rubrique":""}]'});
 const req = G.dispatchRequest('collecte', T.resumesInputs(T.parseEtat(ETAT), selection), FAKE);
 assert.equal(req.url, 'https://api.github.com/repos/alexandra-guiderdoni/assistant-ia-newsletter-com-snum/actions/workflows/publier-paquet-snum.yml/dispatches');
 assert.deepEqual(JSON.parse(req.init.body), {ref: 'main', inputs});
 assert.throws(() => T.resumesInputs(null, selection), /ETAT_ABSENT/);
 assert.throws(() => T.resumesInputs(T.parseEtat({...ETAT, phase: 'resumes'}), selection), /PHASE_INVALIDE/);
 assert.throws(() => T.resumesInputs(T.parseEtat(ETAT), []), /SELECTION_VIDE/);
});

test('lancement : « titres » par défaut, « collecte » si la collecte complète est cochée', () => {
 assert.deepEqual(plain(T.launchInputs('2026-11-20', '2026-11-13', '2026-11-20', false)),
  {edition: '20/11/2026', debut: '13/11/2026', fin: '20/11/2026', mode: 'titres'});
 assert.deepEqual(plain(T.launchInputs('2026-11-20', '2026-11-13', '2026-11-20', true)),
  {edition: '20/11/2026', debut: '13/11/2026', fin: '20/11/2026', mode: 'collecte'});
 assert.throws(() => T.launchInputs('20/11/2026', '2026-11-13', '2026-11-20', false), /DATE_INVALIDE/);
});

test('titres groupés par source, plus récents d’abord, doublons retirés', () => {
 const c = (title, source, date, url) => ({title, source, publication_date_iso: date, url});
 const groups = plain(T.groupBySource([
  c('A1', 'DINUM', '2026-11-14', 'https://a/1'), c('B1', 'CNIL', '2026-11-19', 'https://b/1'),
  c('A2', 'DINUM', '2026-11-18', 'https://a/2'), c('A1 bis', 'DINUM', '2026-11-20', 'https://a/1'), c('X', '', '2026-11-15', 'http://x')]));
 assert.deepEqual(groups.map(g => [g.source, g.items.map(i => [i.index, i.candidate.title])]), [
  ['DINUM', [[2, 'A2'], [0, 'A1']]], ['CNIL', [[1, 'B1']]], ['Source inconnue', [[4, 'X']]]]);
 assert.equal(T.isSelectable({url: 'https://a/1'}), true);
 assert.equal(T.isSelectable({url: 'http://x'}), false);
});

test('libellés : bouton, compteur et statut du rapport en phase « titres »', () => {
 assert.equal(T.resumesLabel(0), 'Rédiger les résumés des articles gardés');
 assert.equal(T.resumesLabel(1), 'Rédiger le résumé de l’article gardé');
 assert.equal(T.resumesLabel(3), 'Rédiger les résumés des 3 articles gardés');
 assert.equal(T.countText(0, 36), '0 titre gardé sur 36');
 assert.equal(T.countText(1, 36), '1 titre gardé sur 36');
 assert.equal(T.countText(3, 36), '3 titres gardés sur 36');
 assert.match(R.statusMessage('needs_albert', 'titres'), /^Titres trouvés, sans résumé/);
 assert.equal(R.statusMessage('needs_albert'), 'Candidats recherchés, mais Albert n’est pas configuré : aucun paquet V519 exportable.');
});

test('page : section des titres, case de collecte complète, avis de remise à zéro, régions annoncées', () => {
 const html = fs.readFileSync(path.join(PAGES, 'index.html'), 'utf8');
 assert.match(html, /<script src="ecartes\.js" defer><\/script>\s*<script src="titres\.js" defer><\/script>\s*<script src="archives\.js" defer><\/script>/);
 assert.match(html, /<h2 id="titres-heading">Titres trouvés<\/h2>/);
 assert.match(html, /<input type="checkbox" id="complete"[^>]*>\s*<label class="fr-label" for="complete">Collecte complète en une fois \(plus longue\)/);
 assert.match(html, /id="reset-notice"[\s\S]*?href="archives\.html"/);
 assert.match(html, /id="titres-status" role="status"/);
 assert.match(html, /id="titres-error"[^>]*role="alert"/);
 assert.match(html, /<button class="fr-btn" id="resumes" type="button"[^>]*disabled/);
 for (const name of fs.readdirSync(PAGES).filter(n => n.endsWith('.js'))) {
  const source = fs.readFileSync(path.join(PAGES, name), 'utf8');
  assert.ok(source.split('\n').length < 300, `${name} dépasse 300 lignes`);
  assert.doesNotMatch(source, /innerHTML|outerHTML|insertAdjacentHTML|localStorage|sessionStorage|indexedDB|console\./, name);
  assert.doesNotMatch(source, /\u2014/, name);
 }
 assert.doesNotMatch(html, /\u2014/);
});

test('motifs des écartés propres aux deux temps, affichés en clair', () => {
 const E = W.VeilleEcartes;
 assert.equal(E.REASONS.NON_SELECTIONNE, 'non gardé au premier temps');
 assert.equal(E.REASONS.PAGE_NON_RELUE, 'page non relue au second temps : introuvable, hors période ou protégée');
 for (const k of ['HORS_THEMATIQUE', 'BUDGET_DUREE_ALBERT', 'ECHEC_ALBERT']) assert.ok(E.REASONS[k], k);
});

test('bouton de groupe : « Tout garder » tant qu’un titre ne l’est pas, « Tout retirer » ensuite', () => {
 assert.equal(T.groupAction(0, 4), 'Tout garder');
 assert.equal(T.groupAction(3, 4), 'Tout garder');
 assert.equal(T.groupAction(4, 4), 'Tout retirer');
 assert.equal(T.groupAction(1, 1), 'Tout retirer');
 const html = fs.readFileSync(path.join(PAGES, 'index.html'), 'utf8');
 assert.match(html, /« Tout garder »/);
});
