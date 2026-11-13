// Fonctions pures de pages/selection.js, chargées par vm sans DOM.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '../pages/selection.js'), 'utf8');
function load() {
 const ctx = {window: {}};
 vm.runInNewContext(script, ctx, {filename: 'selection.js'});
 return ctx.window.VeilleSelection;
}
const S = load();
// Les objets créés dans le contexte vm ont un autre prototype : comparaison par JSON.
const plain = value => JSON.parse(JSON.stringify(value));
const rebuild = (p, s) => plain(S.rebuild(p, s));

function article(id, rubric, date, url, extra = {}) {
 return {id, rubric, title: `Titre ${id}`, source: 'DINUM', publication_date_iso: date,
  publication_date_long: S.dateLong(date), url: `https://example.gouv.fr/${url}`,
  fact: 'Fait.', keywords: ['a', 'b'], takeaway: 'À retenir.', snum_interest: 'Intérêt.', essential: false, ...extra};
}
function packet(articles, watch = []) {
 return {schema_version: 'SNUM_PAQUET_RENDU_V519', edition_date: '2026-11-13', edition_date_long: '13 novembre 2026',
  window_start: '2026-11-03', window_end: '2026-11-13', articles, watch};
}
const OTHER_WATCH = [
 {title: 'Sources protégées contre les robots', summary: 'Accès refusé : Légifrance.'},
 {title: 'Découverte bornée', summary: '12 URL découvertes non analysées.'},
];
const sel = (p, keep = () => true) => p.articles.map((a, i) => ({article: a, keep: keep(a, i), rubric: a.rubric}));

test('dates en toutes lettres comme date_long Python', () => {
 assert.equal(S.dateLong('2026-11-03'), '3 novembre 2026');
 assert.equal(S.dateLong('2026-08-01'), '1 août 2026');
});

test('deux premiers articles de chaque thématique cochés par défaut', () => {
 const p = packet([
  article('U01', 'numerique', '2026-11-13', 'a'), article('U02', 'numerique', '2026-11-13', 'b'),
  article('U03', 'ia', '2026-11-13', 'c'), article('U04', 'numerique', '2026-11-12', 'd'),
  article('U05', 'rh', '2026-11-12', 'e'), article('U06', 'ia', '2026-11-11', 'f'), article('U07', 'ia', '2026-11-10', 'g'),
 ]);
 assert.deepEqual(plain(S.defaultKept(p.articles)), [true, true, true, false, true, true, false]);
});

test('tri date décroissante, puis rubrique, puis URL ; renumérotation et essentiels', () => {
 const p = packet([
  article('U01', 'rh', '2026-11-05', 'z'), article('U02', 'numerique', '2026-11-05', 'b'),
  article('U03', 'numerique', '2026-11-05', 'a'), article('U04', 'bercy', '2026-11-13', 'y'),
  article('U05', 'commande', '2026-11-10', 'w'), article('U06', 'ia', '2026-11-10', 'x'),
 ], OTHER_WATCH);
 const out = rebuild(p, sel(p));
 assert.deepEqual(out.articles.map(a => [a.id, a.url.slice(-1)]),
  [['U01', 'y'], ['U02', 'x'], ['U03', 'w'], ['U04', 'a'], ['U05', 'b'], ['U06', 'z']]);
 assert.deepEqual(out.articles.map(a => a.essential), [true, true, true, false, false, false]);
 // Toutes les rubriques présentes et au moins cinq articles : seules les alertes publiées restent.
 assert.deepEqual(plain(out.watch), OTHER_WATCH);
 // Frontière : quatre articles déclenchent « Collecte limitée », cinq non.
 assert.ok(rebuild(p, sel(p, (a, i) => i < 4)).watch.some(w => w.title === 'Collecte limitée'));
 assert.ok(!rebuild(p, sel(p, (a, i) => i < 5)).watch.some(w => w.title === 'Collecte limitée'));
});

test('alertes recalculées : rubriques absentes, collecte limitée, puis alertes publiées', () => {
 const p = packet([
  article('U01', 'numerique', '2026-11-13', 'a'), article('U02', 'ia', '2026-11-12', 'b'), article('U03', 'rh', '2026-11-11', 'c'),
 ], [{title: 'Rubrique sans article : commande', summary: 'Aucun article admissible établi pour cette rubrique.'},
  {title: 'Rubrique sans article : bercy', summary: 'Aucun article admissible établi pour cette rubrique.'},
  {title: 'Collecte limitée', summary: 'Moins de cinq articles admissibles ont été établis.'}, ...OTHER_WATCH]);
 const out = rebuild(p, sel(p, a => a.rubric !== 'ia'));
 assert.deepEqual(out.watch.map(w => w.title), [
  'Rubrique sans article : ia', 'Rubrique sans article : commande', 'Rubrique sans article : bercy',
  'Collecte limitée', 'Sources protégées contre les robots', 'Découverte bornée']);
 assert.equal(out.watch[0].summary, 'Aucun article admissible établi pour cette rubrique.');
 assert.equal(out.watch[3].summary, 'Moins de cinq articles admissibles ont été établis.');
 // Moins de trois articles : aucun essentiel.
 assert.deepEqual(out.articles.map(a => [a.id, a.essential]), [['U01', false], ['U02', false]]);
});

test('changement de thématique : rubrique exportée, ordre et alertes mis à jour', () => {
 const p = packet([
  article('U01', 'numerique', '2026-11-13', 'b'), article('U02', 'numerique', '2026-11-13', 'a'),
  article('U03', 'ia', '2026-11-12', 'c'), article('U04', 'commande', '2026-11-12', 'd'),
  article('U05', 'rh', '2026-11-11', 'e'), article('U06', 'bercy', '2026-11-10', 'f'),
 ], OTHER_WATCH);
 const s = sel(p);
 s[0].rubric = 'ia';
 const out = rebuild(p, s);
 assert.deepEqual(out.articles.slice(0, 2).map(a => [a.id, a.rubric, a.url.slice(-1)]), [['U01', 'numerique', 'a'], ['U02', 'ia', 'b']]);
 s[1].rubric = 'ia';
 const out2 = rebuild(p, s);
 assert.equal(out2.watch[0].title, 'Rubrique sans article : numerique');
 // Le paquet d'origine n'est pas modifié.
 assert.equal(p.articles[0].rubric, 'numerique');
 assert.equal(p.articles[0].id, 'U01');
 assert.throws(() => S.rebuild(p, [{article: p.articles[0], keep: true, rubric: 'inconnue'}]), /RUBRIQUE_INVALIDE/);
});

test('paquet V519 : mêmes champs, aucun champ ajouté, autres champs conservés', () => {
 const p = packet([article('U01', 'numerique', '2026-11-13', 'a', {essential: true}), article('U02', 'ia', '2026-11-12', 'b')]);
 const out = rebuild(p, sel(p));
 assert.deepEqual(Object.keys(out), Object.keys(p));
 for (const [i, a] of out.articles.entries()) assert.deepEqual(Object.keys(a), Object.keys(p.articles[i]));
 for (const w of out.watch) assert.deepEqual(Object.keys(w).sort(), ['summary', 'title']);
 assert.equal(out.edition_date_long, '13 novembre 2026');
 assert.equal(out.articles[0].fact, 'Fait.');
 assert.ok(S.isPacket(out));
});

test('sélection vide : aucun article, toutes les rubriques et la collecte limitée en alerte', () => {
 const p = packet([article('U01', 'numerique', '2026-11-13', 'a')], OTHER_WATCH);
 const out = rebuild(p, sel(p, () => false));
 assert.equal(out.articles.length, 0);
 assert.deepEqual(out.watch.map(w => w.title), [
  'Rubrique sans article : numerique', 'Rubrique sans article : ia', 'Rubrique sans article : commande',
  'Rubrique sans article : rh', 'Rubrique sans article : bercy', 'Collecte limitée',
  'Sources protégées contre les robots', 'Découverte bornée']);
});

test('aucune écriture HTML ni stockage navigateur ni tiret cadratin dans la page', () => {
 const html = fs.readFileSync(path.join(__dirname, '../pages/index.html'), 'utf8');
 for (const source of [script, html]) {
  assert.doesNotMatch(source, /innerHTML|outerHTML|insertAdjacentHTML|localStorage|sessionStorage|indexedDB/);
  assert.doesNotMatch(source, /\u2014/);
 }
 // Ressources locales en chemins relatifs uniquement.
 assert.doesNotMatch(html, /(href|src)="\/(?!\/)/);
 assert.doesNotMatch(html, /<(script|link)[^>]+(src|href)="https?:/);
});
