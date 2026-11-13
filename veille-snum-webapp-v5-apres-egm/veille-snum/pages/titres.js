'use strict';
// Collecte en deux temps. Premier temps (mode « titres ») : la collecte publie
// seulement les titres trouvés ; cette page les affiche, la personne coche ceux à
// garder, puis le second temps (mode « resumes ») fait rédiger leurs résumés par Albert.
// Première partie : fonctions pures (tests/test_pages_titres.cjs).
// Seconde partie : interface, montée par page.js en phase « titres ».
(function (global) {
 const S = global.VeilleSelection, G = global.VeilleGithub;
 const ETAT_SCHEMA = 'SNUM_ETAT_V1';
 const PHASES = ['titres', 'resumes', 'collecte'];
 const MAX_SELECTION = 60;
 const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
 const HTTPS_URL = /^https:\/\/[^\s]+$/;

 // etat-collecte.json : renvoie l'état utile, ou null s'il est illisible (traité comme absent).
 function parseEtat(d) {
  if (!d || typeof d !== 'object' || d.schema_version !== ETAT_SCHEMA || !PHASES.includes(d.phase)) return null;
  if (!['edition_date', 'window_start', 'window_end'].every(k => ISO_DATE.test(String(d[k])))) return null;
  const {phase, edition_date, window_start, window_end, run_id, candidats, articles} = d;
  return {phase, edition_date, window_start, window_end, run_id, candidats, articles};
 }
 // Titres à choisir en phase « titres » ; page actuelle (paquet V519) sinon, ou sans état publié.
 const view = etat => (etat && etat.phase === 'titres' ? 'titres' : 'paquet');

 const isSelectable = c => !!c && HTTPS_URL.test(String(c.url || ''));

 // entries : [{url, keep, rubric}] dans l'ordre du rapport ; rubric vide : Albert choisit.
 function buildSelection(entries) {
  const kept = (entries || []).filter(e => e.keep);
  if (!kept.length) throw new Error('SELECTION_VIDE');
  if (kept.length > MAX_SELECTION) throw new Error('SELECTION_TROP_LONGUE');
  const seen = new Set();
  return kept.map(e => {
   if (!HTTPS_URL.test(String(e.url))) throw new Error('URL_INVALIDE');
   if (seen.has(e.url)) throw new Error('URL_EN_DOUBLE');
   seen.add(e.url);
   if (e.rubric !== '' && !S.RUBRICS.includes(e.rubric)) throw new Error('RUBRIQUE_INVALIDE');
   return {url: e.url, rubrique: e.rubric};
  });
 }

 // Entrées du workflow en mode « resumes » : dates de etat-collecte.json, sélection en JSON compact.
 function resumesInputs(etat, selection) {
  if (!etat) throw new Error('ETAT_ABSENT');
  if (etat.phase !== 'titres') throw new Error('PHASE_INVALIDE');
  if (!Array.isArray(selection) || !selection.length) throw new Error('SELECTION_VIDE');
  return {mode: 'resumes', ...G.collectInputs(etat.edition_date, etat.window_start, etat.window_end), selection: JSON.stringify(selection)};
 }
 // « Lancer la collecte » : titres seuls par défaut, collecte complète sur demande.
 const launchInputs = (edition, start, end, complete) => ({...G.collectInputs(edition, start, end), mode: complete ? 'collecte' : 'titres'});

 // Groupes par source, dans l'ordre d'apparition ; titres les plus récents d'abord ; adresse en double ignorée.
 function groupBySource(candidates) {
  const groups = new Map(), urls = new Set();
  (candidates || []).forEach((candidate, index) => {
   if (!candidate || typeof candidate !== 'object' || (candidate.url && urls.has(candidate.url))) return;
   if (candidate.url) urls.add(candidate.url);
   const source = String(candidate.source || '').trim() || 'Source inconnue';
   if (!groups.has(source)) groups.set(source, []);
   groups.get(source).push({candidate, index});
  });
  const date = item => String(item.candidate.publication_date_iso || '');
  return [...groups].map(([source, items]) => ({source,
   items: items.sort((a, b) => (date(a) < date(b) ? 1 : date(a) > date(b) ? -1 : a.index - b.index))}));
 }

 function resumesLabel(n) {
  if (n === 1) return 'Rédiger le résumé de l’article gardé';
  return n > 1 ? `Rédiger les résumés des ${n} articles gardés` : 'Rédiger les résumés des articles gardés';
 }
 const countText = (kept, total) => `${kept} titre${kept > 1 ? 's' : ''} gardé${kept > 1 ? 's' : ''} sur ${total}`;

 global.VeilleTitres = {MAX_SELECTION, parseEtat, view, isSelectable, buildSelection, resumesInputs, launchInputs, groupBySource, resumesLabel, countText};

 if (typeof document === 'undefined' || !document.getElementById('titres-section')) return;

 // ---------- Interface ----------
 const byId = id => document.getElementById(id);
 let etat = null, entries = [];
 let options = {hasToken: () => false, requireToken: () => null, isBusy: () => '', launch: async () => {}};

 function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
 }
 function label(forId, visible, context) {
  const l = el('label', 'fr-label');
  l.htmlFor = forId;
  l.append(document.createTextNode(visible), el('span', 'fr-sr-only', ` « ${context} »`));
  return l;
 }
 const running = () => byId('resumes').getAttribute('aria-disabled') === 'true';
 const keptCount = () => entries.filter(e => e.keep).length;
 function groupHeading(source) {
  const items = entries.filter(e => e.source === source);
  const kept = items.filter(e => e.keep).length;
  return `${source} (${kept} gardé${kept > 1 ? 's' : ''} sur ${items.length})`;
 }

 // Compteur, libellé et état du bouton ; bouton bloqué sans titre gardé, au-delà de 60 ou sans jeton.
 function refresh(message) {
  const kept = keptCount();
  byId('titres-count').textContent = message ? `${message}. ${countText(kept, entries.length)}.` : `${countText(kept, entries.length)}.`;
  if (running()) return;
  const button = byId('resumes');
  button.textContent = resumesLabel(kept);
  const why = !kept ? 'Gardez au moins un titre pour faire rédiger les résumés.'
   : kept > MAX_SELECTION ? `Gardez au plus ${MAX_SELECTION} titres : Albert ne rédige pas davantage de résumés en une fois.`
    : !options.hasToken() ? 'Un jeton GitHub est nécessaire pour faire rédiger les résumés (section « Connexion à GitHub »).' : '';
  button.disabled = !!why;
  byId('resumes-hint').textContent = why || `Albert rédige les résumés des titres gardés, dans la thématique choisie ou celle qu’il juge adaptée ; un titre jugé hors thématique rejoint les candidats écartés. Comptez environ une minute pour dix articles, plus la publication.`;
 }

 function rubricField(e) {
  const group = el('div', 'fr-select-group');
  const select = el('select', 'fr-select');
  select.id = `titre-thematique-${e.key}`;
  const first = el('option', '', 'Albert choisit');
  first.value = ''; first.selected = true;
  select.append(first);
  for (const r of S.RUBRICS) { const o = el('option', '', S.RUBRIC_LABELS[r]); o.value = r; select.append(o); }
  select.addEventListener('change', () => {
   e.rubric = select.value;
   refresh(`Thématique de « ${e.title} » : ${select.value ? S.RUBRIC_LABELS[select.value] : 'Albert choisit'}`);
  });
  group.append(label(select.id, 'Thématique', e.title), select);
  return group;
 }

 function titreItem(e, c) {
  const li = el('li', 'fr-mb-3w');
  li.append(el('h4', 'fr-h6 fr-mb-1v', e.title));
  li.append(el('p', 'fr-text--sm fr-mb-1v', `${c.source || 'Source inconnue'} · ${S.dateLong(c.publication_date_iso)}`));
  if (!e.url) { li.append(el('p', 'fr-text--sm', 'Adresse non publique : ce titre ne peut pas être résumé.')); return li; }
  const linkP = el('p', 'fr-mb-1w'), a = el('a', 'fr-link', 'Consulter la publication (nouvelle fenêtre)');
  a.href = e.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
  linkP.append(a);
  const row = el('div', 'fr-grid-row fr-grid-row--gutters fr-grid-row--bottom');
  const keepCol = el('div', 'fr-col-12 fr-col-md-4'), keepGroup = el('div', 'fr-checkbox-group'), keep = el('input');
  keep.type = 'checkbox'; keep.id = `titre-garder-${e.key}`; keep.checked = false;
  keep.addEventListener('change', () => {
   e.keep = keep.checked;
   byId(`titres-heading-${e.group}`).textContent = groupHeading(e.source);
   refresh(`${e.keep ? 'Titre gardé' : 'Titre retiré'} : ${e.title}`);
  });
  keepGroup.append(keep, label(keep.id, 'Garder', e.title));
  keepCol.append(keepGroup);
  const rubricCol = el('div', 'fr-col-12 fr-col-md-6');
  rubricCol.append(rubricField(e));
  row.append(keepCol, rubricCol);
  li.append(linkP, row);
  return li;
 }

 // Phase « titres » : liste reconstruite à partir du rapport publié, aucun titre gardé.
 function mount(state, report) {
  etat = state;
  const box = byId('titres-list');
  box.replaceChildren();
  entries = [];
  const groups = groupBySource(report.candidates);
  groups.forEach((g, gi) => {
   const section = el('section', 'fr-mb-4w'), list = el('ul', 'article-list');
   const items = g.items.map(({candidate: c, index}) => {
    const e = {key: String(index + 1), group: String(gi + 1), source: g.source, title: String(c.title || 'Titre inconnu'),
     url: isSelectable(c) ? c.url : '', keep: false, rubric: ''};
    if (e.url) entries.push(e);
    return [e, c];
   });
   const h = el('h3', 'fr-h4');
   h.id = `titres-heading-${gi + 1}`;
   section.setAttribute('aria-labelledby', h.id);
   for (const [e, c] of items) list.append(titreItem(e, c));
   section.append(h, list);
   box.append(section);
   h.textContent = groupHeading(g.source);
  });
  entries.sort((a, b) => Number(a.key) - Number(b.key));
  if (!groups.length) box.append(el('p', '', 'Aucun titre trouvé pour cette période.'));
  let intro = `Édition du ${S.dateLong(etat.edition_date)}, période du ${S.dateLong(etat.window_start)} au ${S.dateLong(etat.window_end)} : ${entries.length} titre${entries.length > 1 ? 's' : ''} à trier.`;
  if (report.edition_date && report.edition_date !== etat.edition_date) intro += ` Attention : le rapport publié concerne l’édition du ${S.dateLong(report.edition_date)}.`;
  byId('titres-intro').textContent = intro;
  showError('');
  refresh();
 }

 function showError(message, url) {
  const box = byId('titres-error');
  box.hidden = !message;
  box.replaceChildren();
  if (!message) return;
  box.append(el('p', '', message));
  if (url) { const a = el('a', 'fr-link', 'Consulter le run sur GitHub (nouvelle fenêtre)'); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; box.append(a); }
 }
 function lock(on) {
  for (const field of byId('titres-list').querySelectorAll('input, select')) field.disabled = on;
 }
 const SELECTION_ERRORS = {SELECTION_VIDE: 'Gardez au moins un titre.', SELECTION_TROP_LONGUE: `Gardez au plus ${MAX_SELECTION} titres.`};

 byId('resumes').addEventListener('click', async () => {
  const button = byId('resumes');
  if (running() || button.disabled) return;
  const busy = options.isBusy();
  if (busy) { showError(busy); return; }
  const token = options.requireToken();
  if (!token) { showError('Un jeton GitHub est nécessaire pour faire rédiger les résumés.'); return; }
  let inputs;
  try { inputs = resumesInputs(etat, buildSelection(entries)); }
  catch (err) { showError(SELECTION_ERRORS[err.message] || `Sélection refusée (${err.message}).`); return; }
  const n = keptCount();
  lock(true);
  try {
   await options.launch({inputs, token, button, busy: 'Rédaction des résumés en cours…', restore: () => resumesLabel(keptCount()),
    ui: {status: 'titres-status', error: 'titres-error', elapsed: 'titres-elapsed', run: 'titres-run'},
    name: 'Rédaction des résumés', duration: `Comptez environ une minute pour dix articles (${n} demandé${n > 1 ? 's' : ''}), plus la publication.`,
    failed: text => `La rédaction des résumés n’a pas abouti (${text}) : les titres restent affichés, vous pouvez relancer.`});
  } finally {
   lock(false);
   if (button.isConnected) refresh();
  }
 });

 Object.assign(global.VeilleTitres, {mount, refresh, configure: o => { options = {...options, ...o}; }});
})(typeof window !== 'undefined' ? window : globalThis);
