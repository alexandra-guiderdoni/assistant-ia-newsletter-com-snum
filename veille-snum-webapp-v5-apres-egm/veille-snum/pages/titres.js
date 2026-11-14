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
 // GitHub refuse des entrées de plus de 65 535 caractères : marge gardée pour les dates et le mode.
 const MAX_SELECTION_CHARS = 60000;
 // Albert s'arrête après six minutes : au rythme observé, une trentaine d'articles tiennent sans risque.
 const SAFE_SELECTION = 30;
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
  const text = JSON.stringify(selection);
  if (text.length > MAX_SELECTION_CHARS) throw new Error('SELECTION_TROP_VOLUMINEUSE');
  return {mode: 'resumes', ...G.collectInputs(etat.edition_date, etat.window_start, etat.window_end), selection: text};
 }
 // Ce que le site publie a-t-il changé depuis l'affichage des titres ? '' : non, ou état illisible ;
 // 'paquet' : un paquet a été publié depuis ; 'titres' : d'autres titres ont remplacé ceux affichés.
 function moved(shown, online) {
  if (!shown || !online) return '';
  if (online.phase !== 'titres') return 'paquet';
  return ['run_id', 'edition_date', 'window_start', 'window_end'].some(k => String(online[k]) !== String(shown[k])) ? 'titres' : '';
 }
 const MOVED = {
  paquet: 'Un paquet a déjà été publié pendant votre tri (résumés demandés depuis une autre page, ou collecte complète) : la page l’affiche maintenant. Les titres qui n’y figurent pas sont dans les candidats écartés, où ils restent repêchables.',
  titres: 'Une nouvelle collecte a remplacé les titres que vous aviez sous les yeux : la liste a été rechargée, refaites votre sélection.',
 };
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
 // Bouton de groupe : garde tous les titres d'une source, ou les retire tous s'ils sont déjà gardés.
 const groupAction = (kept, total) => (total > 0 && kept === total ? 'Tout retirer' : 'Tout garder');
 const countText = (kept, total) => `${kept} titre${kept > 1 ? 's' : ''} gardé${kept > 1 ? 's' : ''} sur ${total}`;
 // Durée annoncée : estimée d'après quatre collectes publiques du 13 novembre 2026, non mesurée pour ce mode.
 function durationText(kept) {
  const base = 'Comptez une à deux minutes pour dix articles, puis environ deux minutes de publication.';
  return kept > SAFE_SELECTION ? `${base} Albert s’arrête après six minutes de rédaction : au-delà d’une trentaine d’articles, les derniers peuvent ne pas être résumés ; ils rejoignent alors les candidats écartés, où ils restent repêchables.` : base;
 }

 global.VeilleTitres = {MAX_SELECTION, MAX_SELECTION_CHARS, SAFE_SELECTION, MOVED, parseEtat, view, isSelectable, buildSelection, resumesInputs, moved, launchInputs,
  groupBySource, groupAction, resumesLabel, countText, durationText};

 if (typeof document === 'undefined' || !document.getElementById('titres-section')) return;

 // ---------- Interface ----------
 const byId = id => document.getElementById(id);
 let etat = null, entries = [];
 let options = {hasToken: () => false, requireToken: () => null, isBusy: () => '', launch: async () => {}, readEtat: async () => null, reload: async () => false};

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
 // Titre et bouton du groupe après un changement ; le bouton nomme sa source pour les lecteurs d'écran.
 function updateGroup(group, source) {
  const items = entries.filter(e => e.source === source);
  byId(`titres-heading-${group}`).textContent = groupHeading(source);
  const button = byId(`titres-tout-${group}`);
  if (button) button.replaceChildren(document.createTextNode(groupAction(items.filter(e => e.keep).length, items.length)), el('span', 'fr-sr-only', ` : ${source}`));
 }
 function toggleGroup(group, source) {
  const items = entries.filter(e => e.source === source);
  const keep = groupAction(items.filter(e => e.keep).length, items.length) === 'Tout garder';
  for (const e of items) { e.keep = keep; byId(`titre-garder-${e.key}`).checked = keep; }
  updateGroup(group, source);
  refresh(`${keep ? 'Tous les titres gardés' : 'Tous les titres retirés'} : ${source}`);
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
  byId('resumes-hint').textContent = why || `Albert rédige les résumés des titres gardés, dans la thématique choisie ou celle qu’il juge adaptée ; un titre jugé hors thématique rejoint les candidats écartés. ${durationText(kept)}`;
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
  e.li = li;
  li.append(el('p', 'fr-text--sm fr-mb-1v', `${c.source || 'Source inconnue'} · ${S.dateLong(c.publication_date_iso)}`));
  if (!e.url) { li.append(el('p', 'fr-text--sm', 'Adresse non publique : ce titre ne peut pas être résumé.')); return li; }
  const linkP = el('p', 'fr-mb-1w'), a = S.publicationLink(e.url, e.title);
  linkP.append(a);
  const row = el('div', 'fr-grid-row fr-grid-row--gutters fr-grid-row--bottom');
  const keepCol = el('div', 'fr-col-12 fr-col-md-4'), keepGroup = el('div', 'fr-checkbox-group'), keep = el('input');
  keep.type = 'checkbox'; keep.id = `titre-garder-${e.key}`; keep.checked = false;
  keep.addEventListener('change', () => {
   e.keep = keep.checked;
   updateGroup(e.group, e.source);
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

 // Articles déjà publiés (publies.js), lus après l'affichage : mention sur place, sans reconstruire la liste.
 const markPublished = () => entries.filter(e => global.VeillePublies.decorate(e.li, e.url)).length;

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
   const all = el('button', 'fr-btn fr-btn--tertiary fr-btn--sm fr-mb-2w');
   all.type = 'button'; all.id = `titres-tout-${gi + 1}`;
   all.addEventListener('click', () => { if (!all.disabled) toggleGroup(String(gi + 1), g.source); });
   section.append(h, ...(items.some(([e]) => e.url) ? [all] : []), list);
   box.append(section);
   updateGroup(String(gi + 1), g.source);
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
  if (url) { const a = el('a', 'fr-link', 'Voir le détail de l’exécution sur GitHub (nouvelle fenêtre)'); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; box.append(a); }
 }
 function lock(on) {
  for (const field of byId('titres-list').querySelectorAll('input, select, button')) field.disabled = on;
 }
 const SELECTION_ERRORS = {SELECTION_VIDE: 'Gardez au moins un titre.', SELECTION_TROP_LONGUE: `Gardez au plus ${MAX_SELECTION} titres.`,
  SELECTION_TROP_VOLUMINEUSE: 'La sélection dépasse la taille acceptée par GitHub : gardez moins de titres, puis repêchez les autres ensuite.'};
 // Avant l'envoi, puis après un échec : si le site ne publie plus les titres affichés, la page se recharge et l'explique.
 async function reloadIfMoved(online) {
  const change = moved(etat, online);
  if (change) await options.reload();
  return change ? MOVED[change] : '';
 }

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
    name: 'Rédaction des résumés', subject: 'la rédaction des résumés', duration: `${n} article${n > 1 ? 's' : ''} demandé${n > 1 ? 's' : ''}. ${durationText(n)}`,
    before: async () => { const message = await reloadIfMoved(await options.readEtat()); if (message) throw new Error(message); },
    failed: (text, online) => {
     const changed = MOVED[moved(etat, online)] || '';
     return {reload: !!changed, message: changed || `La rédaction des résumés n’a pas abouti (${text}). Vos titres gardés restent cochés : vous pouvez relancer. Si l’échec se répète, Albert est peut-être indisponible : réessayez plus tard.`};
    }});
  } finally {
   lock(false);
   if (button.isConnected) refresh();
  }
 });

 Object.assign(global.VeilleTitres, {mount, markPublished, refresh, configure: o => { options = {...options, ...o}; }});
})(typeof window !== 'undefined' ? window : globalThis);
