'use strict';
// Sélection éditoriale de la veille SNUM, servie en page statique (GitHub Pages).
// Première partie : fonctions pures, testables sans DOM (tests/test_pages_selection.cjs).
// Seconde partie : interface, montée par page.js si la page est présente.
(function (global) {
 const RUBRICS = ['numerique', 'ia', 'commande', 'rh', 'bercy'];
 const RUBRIC_LABELS = {numerique: 'Numérique', ia: 'Intelligence artificielle', commande: 'Commande publique', rh: 'Ressources humaines', bercy: 'Bercy'};
 const KEPT_PER_RUBRIC = 2;
 const MONTHS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
 const EMPTY_RUBRIC_PREFIX = 'Rubrique sans article : ';
 const LIMITED = 'Collecte limitée';

 // Même rendu que date_long côté Python : « 3 novembre 2026 ».
 function dateLong(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  if (!m || Number(m[2]) < 1 || Number(m[2]) > 12) return String(iso || '');
  return `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
 }

 // Par défaut, seuls les deux premiers articles de chaque thématique (ordre du
 // paquet, donc les plus récents) sont gardés.
 function defaultKept(articles) {
  const seen = {};
  return articles.map(a => {
   seen[a.rubric] = (seen[a.rubric] || 0) + 1;
   return seen[a.rubric] <= KEPT_PER_RUBRIC;
  });
 }

 const compare = (x, y) => (x < y ? -1 : x > y ? 1 : 0);

 // Reconstruit un paquet V519 à partir des articles gardés, en reprenant les
 // règles de packet_for (core.py) : tri, renumérotation, essentiels, alertes.
 // selection : [{article, keep, rubric}] ; les autres champs sont conservés.
 function rebuild(packet, selection) {
  const kept = selection.filter(s => s.keep).map(s => {
   if (!RUBRICS.includes(s.rubric)) throw new Error('RUBRIQUE_INVALIDE');
   return {...s.article, rubric: s.rubric};
  });
  kept.sort((a, b) => compare(b.publication_date_iso, a.publication_date_iso)
   || RUBRICS.indexOf(a.rubric) - RUBRICS.indexOf(b.rubric)
   || compare(a.url, b.url));
  const articles = kept.map((a, i) => ({...a, id: `U${String(i + 1).padStart(2, '0')}`, essential: kept.length >= 3 && i < 3}));
  const present = new Set(articles.map(a => a.rubric));
  const watch = RUBRICS.filter(r => !present.has(r))
   .map(r => ({title: EMPTY_RUBRIC_PREFIX + r, summary: 'Aucun article admissible établi pour cette rubrique.'}));
  if (articles.length < 5) watch.push({title: LIMITED, summary: 'Moins de cinq articles admissibles ont été établis.'});
  for (const w of packet.watch || []) {
   if (w.title === LIMITED || String(w.title).startsWith(EMPTY_RUBRIC_PREFIX)) continue;
   watch.push({...w});
  }
  return {...packet, articles, watch};
 }

 function isPacket(p) {
  return !!p && typeof p === 'object' && p.schema_version === 'SNUM_PAQUET_RENDU_V519'
   && Array.isArray(p.articles) && Array.isArray(p.watch) && typeof p.edition_date === 'string';
 }

 global.VeilleSelection = {RUBRICS, RUBRIC_LABELS, KEPT_PER_RUBRIC, dateLong, defaultKept, rebuild, isPacket};

 if (typeof document === 'undefined' || !document.getElementById('article-list')) return;


 // ---------- Interface ----------
 // Montée par page.js après chargement du paquet publié (mount), complétée par
 // ecartes.js lors d'un repêchage (entries, setEntries).
 const byId = id => document.getElementById(id);
 let packet = null, selection = [];

 function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
 }
 function externalLink(url, text) {
  const a = el('a', 'fr-link', text);
  if (/^https:\/\//.test(String(url))) { a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; }
  return a;
 }
 // Lien vers la publication : son nom porte le titre de l'article, pour le distinguer des liens voisins.
 function publicationLink(url, title) {
  const a = externalLink(url, 'Consulter la publication');
  a.append(el('span', 'fr-sr-only', ` « ${title} »`), document.createTextNode(' (nouvelle fenêtre)'));
  return a;
 }
 // Étiquette visible, complétée du titre de l'article pour les lecteurs d'écran.
 function label(forId, visible, context) {
  const l = el('label', 'fr-label');
  l.htmlFor = forId;
  l.append(document.createTextNode(visible), el('span', 'fr-sr-only', ` « ${context} »`));
  return l;
 }
 // Liste « Thématique » ; sans valeur, une option invite à choisir. Erreur reliée au champ.
 function rubricSelect(id, value, context) {
  const group = el('div', 'fr-select-group');
  const select = el('select', 'fr-select');
  select.id = id;
  const messages = el('div', 'fr-messages-group');
  messages.id = `${id}-messages`;
  messages.setAttribute('aria-live', 'polite');
  select.setAttribute('aria-describedby', messages.id);
  if (!value) {
   const o = el('option', '', 'Sélectionner une thématique');
   o.value = ''; o.selected = true; o.disabled = true;
   select.append(o);
  }
  for (const r of RUBRICS) {
   const o = el('option', '', RUBRIC_LABELS[r]);
   o.value = r; o.selected = r === value;
   select.append(o);
  }
  group.append(label(id, 'Thématique', context), select, messages);
  const setError = message => {
   messages.replaceChildren();
   group.classList.toggle('fr-select-group--error', !!message);
   if (message) { messages.append(el('p', 'fr-message fr-message--error', message)); select.setAttribute('aria-invalid', 'true'); }
   else select.removeAttribute('aria-invalid');
  };
  select.addEventListener('change', () => { if (select.value) setError(''); });
  return {group, select, setError};
 }
 function announce(message) { byId('selection-status').textContent = message; }

 function showLoadError(message) {
  const box = byId('load-error');
  box.hidden = false;
  box.replaceChildren(el('h2', 'fr-alert__title', 'Paquet indisponible'), el('p', '', message));
  byId('selection-content').hidden = true;
 }

 function renderSummary() {
  const kept = selection.filter(s => s.keep).length;
  byId('summary-edition').textContent = packet.edition_date_long || dateLong(packet.edition_date);
  byId('summary-period').textContent = `du ${dateLong(packet.window_start)} au ${dateLong(packet.window_end)}`;
  byId('summary-count').textContent = `${kept} article${kept > 1 ? 's' : ''} gardé${kept > 1 ? 's' : ''} sur ${selection.length}`;
 }

 function renderWatch() {
  const list = byId('watch-list');
  list.replaceChildren();
  const items = packet.watch || [];
  if (!items.length) { list.append(el('li', '', 'Aucune alerte dans le paquet publié.')); return; }
  for (const w of items) {
   const li = el('li');
   li.append(el('strong', '', `${w.title} : `), document.createTextNode(w.summary));
   list.append(li);
  }
 }

 function groupHeading(rubric) {
  const items = selection.filter(s => s.rubric === rubric);
  const kept = items.filter(s => s.keep).length;
  return `${RUBRIC_LABELS[rubric]} (${kept} gardé${kept > 1 ? 's' : ''} sur ${items.length})`;
 }

 function articleItem(s) {
  const a = s.article;
  const li = el('li', 'fr-mb-4w');
  li.classList.toggle('unselected', !s.keep);
  li.dataset.key = s.key;

  const content = el('div', 'article-content');
  content.append(el('p', 'fr-text--sm fr-mb-1v', a.publication_date_long || dateLong(a.publication_date_iso)));
  content.append(el('h4', 'fr-h6 fr-mb-1v', a.title));
  content.append(el('p', 'fr-text--sm fr-mb-1w', `Source : ${a.source}`));
  for (const [name, value] of [['Fait', a.fact], ['À retenir', a.takeaway], ['Intérêt SNUM', a.snum_interest], ['Mots-clés', (a.keywords || []).join(' · ')]]) {
   const p = el('p', 'fr-mb-1w');
   p.append(el('strong', '', `${name} : `), document.createTextNode(value));
   content.append(p);
  }
  const linkP = el('p', 'fr-mb-1w');
  linkP.append(publicationLink(a.url, a.title));
  content.append(linkP);

  const row = el('div', 'fr-grid-row fr-grid-row--gutters fr-grid-row--bottom');
  const keepCol = el('div', 'fr-col-12 fr-col-md-4');
  const keepGroup = el('div', 'fr-checkbox-group');
  const keep = el('input');
  keep.type = 'checkbox'; keep.id = `garder-${s.key}`; keep.checked = s.keep;
  keepGroup.append(keep, label(keep.id, 'Garder', a.title));
  keepCol.append(keepGroup);
  // Mise à jour sur place : la liste n'est pas reconstruite, le focus reste sur la case.
  keep.addEventListener('change', () => {
   s.keep = keep.checked;
   li.classList.toggle('unselected', !s.keep);
   byId(`heading-${s.rubric}`).textContent = groupHeading(s.rubric);
   refresh(`${s.keep ? 'Article gardé' : 'Article écarté'} : ${a.title}`);
  });

  const rubricCol = el('div', 'fr-col-12 fr-col-md-6');
  const field = rubricSelect(`thematique-${s.key}`, s.rubric, a.title);
  const select = field.select;
  rubricCol.append(field.group);
  // L'article change de groupe : la liste est reconstruite, puis le focus revient sur la liste.
  select.addEventListener('change', () => {
   s.rubric = select.value;
   renderArticles();
   const again = byId(select.id);
   if (again) again.focus();
   refresh(`Thématique changée : ${a.title}, désormais en ${RUBRIC_LABELS[s.rubric]}`);
  });

  row.append(keepCol, rubricCol);
  li.append(content, row);
  return li;
 }

 function renderArticles() {
  const box = byId('article-list');
  box.replaceChildren();
  if (!selection.length) { box.append(el('p', '', 'Le paquet publié ne contient aucun article.')); return; }
  for (const rubric of RUBRICS) {
   const items = selection.filter(s => s.rubric === rubric);
   if (!items.length) continue;
   const section = el('section', 'fr-mb-4w');
   const h = el('h3', 'fr-h4', groupHeading(rubric));
   h.id = `heading-${rubric}`;
   section.setAttribute('aria-labelledby', h.id);
   const list = el('ol', 'article-list');
   for (const s of items) list.append(articleItem(s));
   section.append(h, list);
   box.append(section);
  }
 }

 // Après chaque modification : résumé, état des actions et annonce.
 function refresh(message) {
  renderSummary();
  const kept = selection.filter(s => s.keep).length;
  byId('download').disabled = kept === 0;
  byId('copy').disabled = kept === 0;
  byId('export-status').textContent = kept === 0
   ? 'Aucun article gardé : gardez au moins un article pour télécharger ou copier le JSON.'
   : `Le JSON V519 exporté contiendra ${kept} article${kept > 1 ? 's' : ''} ; numérotation, tri, essentiels et alertes sont recalculés.`;
  if (message) announce(message);
 }

 const exported = () => JSON.stringify(rebuild(packet, selection), null, 2) + '\n';

 byId('download').addEventListener('click', () => {
  if (!selection.some(s => s.keep)) return;
  const url = URL.createObjectURL(new Blob([exported()], {type: 'application/json;charset=utf-8'}));
  const a = document.createElement('a');
  a.href = url; a.download = `paquet-v519-${packet.edition_date}.json`;
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
  announce('Téléchargement proposé : vérifiez la présence du fichier.');
 });
 byId('copy').addEventListener('click', async () => {
  if (!selection.some(s => s.keep)) return;
  try {
   if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('indisponible');
   await navigator.clipboard.writeText(exported());
   announce('JSON V519 copié dans le presse-papiers.');
  } catch (_) {
   announce('Copie impossible dans ce navigateur : utilisez « Télécharger le JSON V519 ».');
  }
 });

 // Paquet chargé (ou rechargé après une collecte) : sélection par défaut.
 function mount(data) {
  packet = data;
  const kept = defaultKept(packet.articles);
  selection = packet.articles.map((a, i) => ({article: a, keep: kept[i], rubric: a.rubric, key: String(i + 1)}));
  byId('load-error').hidden = true;
  byId('selection-content').hidden = false;
  renderWatch();
  renderArticles();
  refresh();
 }
 function setEntries(entries, message) {
  selection = entries;
  renderArticles();
  refresh(message);
 }

 Object.assign(global.VeilleSelection, {mount, showLoadError, rubricSelect, publicationLink, setEntries,
  entries: () => selection, packet: () => packet});
})(typeof window !== 'undefined' ? window : globalThis);
