'use strict';
// Candidats écartés (candidats-ecartes.json) : jugés hors thématique par Albert, non
// résumés faute de temps ou après un échec, non gardés au premier temps, ou page non
// relue. Repêchage d'un candidat par le workflow repecher-candidat.yml, comme
// « Ajouter » en local.
(function (global) {
 const REASONS = {
  HORS_THEMATIQUE: 'jugé hors thématique par Albert',
  BUDGET_DUREE_ALBERT: 'non résumé faute de temps',
  ECHEC_ALBERT: 'échec du résumé Albert',
  NON_SELECTIONNE: 'non gardé au premier temps',
  PAGE_NON_RELUE: 'page non relue au second temps : introuvable, hors période ou protégée',
 };
 // Ordre des champs d'un article V519 ; id et essential sont recalculés à l'export.
 const TEXT_FIELDS = ['title', 'source', 'publication_date_iso', 'publication_date_long', 'url', 'fact', 'takeaway', 'snum_interest'];
 const filled = v => typeof v === 'string' && v.trim() !== '';

 // Résultat SNUM_REPECHAGE_V1 : {ok: true, article} ou {ok: false, message}.
 function parseRepechage(result, expectedUrl) {
  if (!result || typeof result !== 'object' || result.schema_version !== 'SNUM_REPECHAGE_V1') throw new Error('Résultat du repêchage illisible.');
  const refused = result.status === 'erreur';
  // Repêchage interrompu avant son résultat : la tâche publie un refus sans adresse, dont le motif doit s'afficher.
  if (result.url !== expectedUrl && !(refused && result.url === '')) throw new Error('Le résultat publié concerne une autre adresse que le candidat choisi.');
  if (refused) return {ok: false, message: filled(result.message) ? result.message : 'Repêchage refusé sans motif précisé.'};
  const a = result.article;
  const valid = result.status === 'ok' && a && typeof a === 'object'
   && global.VeilleSelection.RUBRICS.includes(a.rubric) && TEXT_FIELDS.every(f => filled(a[f]))
   // L'article porte son adresse canonique (www, paramètres retirés) : elle peut différer de celle du candidat.
   && /^https:\/\/[^\s]+$/.test(a.url) && /^\d{4}-\d{2}-\d{2}$/.test(a.publication_date_iso)
   && Array.isArray(a.keywords) && a.keywords.length > 0 && a.keywords.every(filled);
  if (!valid) throw new Error('Article repêché incomplet : il n’a pas été ajouté.');
  return {ok: true, article: {id: '', rubric: a.rubric, title: a.title, source: a.source, publication_date_iso: a.publication_date_iso,
   publication_date_long: a.publication_date_long, url: a.url, fact: a.fact, keywords: [...a.keywords], takeaway: a.takeaway,
   snum_interest: a.snum_interest, essential: false}};
 }

 // Ajoute l'article gardé à la sélection et retire le candidat demandé (candidateUrl, ou l'adresse
 // de l'article à défaut) des candidats, sans modifier les listes reçues.
 function merge(selection, candidates, article, key, candidateUrl) {
  if (selection.some(s => s.article.url === article.url)) throw new Error('DEJA_SELECTIONNE');
  return {selection: [...selection, {article, keep: true, rubric: article.rubric, key}],
   candidates: candidates.filter(c => c.url !== article.url && c.url !== candidateUrl)};
 }

 global.VeilleEcartes = {REASONS, parseRepechage, merge};

 if (typeof document === 'undefined' || !document.getElementById('candidates-list')) return;

 // ---------- Interface ----------
 const S = global.VeilleSelection, G = global.VeilleGithub;
 const byId = id => document.getElementById(id);
 let data = null, candidates = [], busy = false, added = 0;
 let options = {requireToken: () => null, isCollecting: () => false};

 function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
 }
 const status = text => { byId('repechage-status').textContent = text; };
 function showError(message, url) {
  const box = byId('repechage-error');
  box.hidden = !message;
  box.replaceChildren();
  if (!message) return;
  box.append(el('p', '', message));
  if (url) { const a = el('a', 'fr-link', 'Voir le détail de l’exécution sur GitHub (nouvelle fenêtre)'); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; box.append(a); }
 }
 function buttonLabel(button, text, title) {
  button.replaceChildren(document.createTextNode(text), el('span', 'fr-sr-only', ` « ${title} »`));
 }

 async function repecher(c, select, field, button) {
  if (busy) { showError('Un repêchage est déjà en cours : attendez sa fin.'); return; }
  if (options.isCollecting()) { showError('Une collecte est en cours : attendez sa fin avant de repêcher un article.'); return; }
  if (!select.value) { field.setError('Choisissez la thématique de cet article avant de le repêcher.'); select.focus(); return; }
  const token = options.requireToken();
  if (!token) return;
  busy = true; showError('');
  // Le bouton garde le focus : il est marqué indisponible au lieu d'être désactivé.
  button.setAttribute('aria-disabled', 'true'); buttonLabel(button, 'Repêchage en cours…', c.title);
  const startedAt = Date.now();
  let runLink = '';
  try {
   status(`Repêchage demandé pour « ${c.title} ». Comptez une à deux minutes.`);
   const inputs = G.repechageInputs(c.url, select.value, data.window_start, data.window_end);
   const run = await G.dispatch('repechage', inputs, token);
   runLink = run.htmlUrl;
   const end = await G.follow(run.id, token, startedAt, p => {
    runLink = p.htmlUrl || runLink;
    status(`Repêchage de « ${c.title} » : ${p.text}.`);
    byId('repechage-elapsed').textContent = `Temps écoulé : ${G.elapsed(p.elapsed)}.`;
   });
   if (end.state !== 'success') throw new Error(`Le repêchage n’a pas abouti (${end.text}).`);
   status(`Lecture du résultat du repêchage de « ${c.title} »…`);
   const parsed = parseRepechage(await G.readRepechage(run.id), c.url);
   if (!parsed.ok) throw new Error(`Albert n’a pas pu repêcher « ${c.title} » : ${parsed.message}`);
   const key = `r${++added}`;
   let merged;
   try { merged = merge(S.entries(), candidates, parsed.article, key, c.url); }
   catch (_) { throw new Error(`« ${c.title} » figure déjà dans la sélection.`); }
   candidates = merged.candidates;
   const label = S.RUBRIC_LABELS[parsed.article.rubric];
   S.setEntries(merged.selection, `Article repêché et gardé en ${label} : ${parsed.article.title}`);
   renderList();
   // Le bouton disparaît avec le candidat : le focus passe sur la case « Garder » du nouvel article.
   const target = byId(`garder-${key}`);
   if (target) target.focus();
   status(`Article repêché et gardé en ${label} : ${parsed.article.title}. Il figure dans l’export.`);
   byId('repechage-elapsed').textContent = '';
  } catch (err) {
   const why = String(err.message || err);
   // Suivi perdu : le repêchage, lui, continue peut-être ; son résultat ne pourra plus être repris ici.
   status(err.lost ? 'Repêchage : suivi interrompu.' : 'Repêchage interrompu.');
   showError(err.lost ? `${why} Le suivi s’arrête ici, mais le repêchage continue peut-être sur GitHub. Attendez deux minutes avant de repêcher de nouveau cet article.` : why, runLink);
  } finally {
   busy = false;
   if (button.isConnected) { button.removeAttribute('aria-disabled'); buttonLabel(button, 'Repêcher avec Albert', c.title); }
  }
 }

 function candidateItem(c, index) {
  const li = el('li', 'fr-mb-4w');
  const title = el('p', 'fr-mb-1v');
  title.append(el('strong', '', c.title || 'Titre inconnu'),
   document.createTextNode(` (${c.source || 'source inconnue'}, ${c.publication_date_long || S.dateLong(c.publication_date_iso)})`));
  const reason = el('p', 'fr-text--sm fr-mb-1v', `Motif : ${REASONS[c.reason] || c.reason || 'non précisé'}.`);
  li.append(title, reason);
  if (c.url) {
   const p = el('p', 'fr-mb-1w');
   const a = el('a', 'fr-link', 'Consulter la publication (nouvelle fenêtre)');
   if (/^https:\/\//.test(String(c.url))) { a.href = c.url; a.target = '_blank'; a.rel = 'noopener noreferrer'; }
   p.append(a);
   li.append(p);
  }
  if (!/^https:\/\//.test(String(c.url || ''))) return li;
  const field = S.rubricSelect(`repecher-${index}`, '', c.title || '');
  const button = el('button', 'fr-btn fr-btn--secondary fr-btn--sm');
  button.type = 'button';
  button.setAttribute('aria-describedby', 'repechage-hint');
  buttonLabel(button, 'Repêcher avec Albert', c.title || '');
  button.addEventListener('click', () => {
   if (button.getAttribute('aria-disabled') !== 'true') repecher(c, field.select, field, button);
  });
  const row = el('div', 'fr-grid-row fr-grid-row--gutters fr-grid-row--bottom');
  const selectCol = el('div', 'fr-col-12 fr-col-md-6'); selectCol.append(field.group);
  const buttonCol = el('div', 'fr-col-12 fr-col-md-6'); buttonCol.append(button);
  row.append(selectCol, buttonCol);
  li.append(row);
  return li;
 }

 function renderList() {
  const intro = byId('candidates-intro'), list = byId('candidates-list');
  list.replaceChildren();
  byId('candidates-button').textContent = `Candidats écartés (${candidates.length})`;
  intro.textContent = candidates.length
   ? 'Ces publications ont été trouvées pendant la collecte mais ne figurent pas dans le paquet ; le motif est indiqué pour chacune. Choisissez une thématique puis « Repêcher avec Albert » : Albert rédige alors le résumé de l’article dans cette thématique et l’article est ajouté à la sélection.'
   : 'Aucun candidat écarté pour cette édition.';
  const packet = S.packet();
  if (data && data.edition_date && packet && data.edition_date !== packet.edition_date) {
   intro.textContent += ` Attention : cette liste concerne l’édition du ${S.dateLong(data.edition_date)}.`;
  }
  candidates.forEach((c, i) => list.append(candidateItem(c, i)));
 }

 // json null : liste absente ou illisible, message affiché à la place.
 function render(json, message) {
  data = json && Array.isArray(json.candidates) ? json : null;
  candidates = data ? data.candidates.slice() : [];
  showError('');
  if (!data) {
   byId('candidates-list').replaceChildren();
   byId('candidates-button').textContent = 'Candidats écartés';
   byId('candidates-intro').textContent = message || 'La liste des candidats écartés n’a pas pu être chargée.';
   return;
  }
  renderList();
 }

 Object.assign(global.VeilleEcartes, {render, configure: o => { options = {...options, ...o}; }, isBusy: () => busy});
})(typeof window !== 'undefined' ? window : globalThis);
