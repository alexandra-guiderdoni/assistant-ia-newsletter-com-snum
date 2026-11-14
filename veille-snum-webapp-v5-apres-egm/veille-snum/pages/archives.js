'use strict';
// Archives des collectes Veille SNUM, publiées par GitHub Actions sur la branche
// publique donnees-veille et lues sans jeton sur raw.githubusercontent.com.
// Première partie : fonctions pures (tests/test_pages_archives.cjs), aussi
// utilisées par page.js pour rouvrir une collecte (?collecte=<id>).
// Seconde partie : interface de archives.html.
(function (global) {
 const S = global.VeilleSelection, G = global.VeilleGithub;
 const INDEX_SCHEMA = 'SNUM_ARCHIVES_V1';
 const FILES = [
  {name: 'paquet-v519.json', label: 'Paquet V519'},
  {name: 'candidats-ecartes.json', label: 'Candidats écartés'},
  {name: 'rapport-collecte.json', label: 'Rapport de collecte'}];
 const STATUS = {ready: ['Complète', 'fr-badge--success'], partial: ['Partielle', 'fr-badge--warning']};
 const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

 // Date d'édition, souligné, numéro de run GitHub : rien d'autre ne peut
 // entrer dans une adresse ou un chemin.
 const isArchiveId = id => typeof id === 'string' && id.length <= 40 && /^\d{4}-\d{2}-\d{2}_\d+$/.test(id);
 const checkId = id => { if (!isArchiveId(id)) throw new Error('ARCHIVE_INVALIDE'); return id; };
 const indexUrl = bust => `${G.RAW_BASE}collectes/index.json?t=${encodeURIComponent(bust)}`;
 function fileUrl(id, name) {
  if (!FILES.some(f => f.name === name)) throw new Error('FICHIER_INVALIDE');
  return `${G.RAW_BASE}collectes/${checkId(id)}/${name}`;
 }
 // raw.githubusercontent.com garde cinq minutes un fichier en cache, et le paramètre t ne
 // contourne pas ce cache (constat du 13 novembre 2026) : avec cache: 'no-store', il écarte
 // seulement celui du navigateur. Une archive peut donc apparaître avec quelques minutes de retard.
 const archiveUrl = (id, name, bust) => `${fileUrl(id, name)}?t=${encodeURIComponent(bust)}`;
 const selectionHref = id => `./?collecte=${encodeURIComponent(checkId(id))}`;

 // Paramètre de la page de sélection : collecte en cours, archive, ou identifiant refusé.
 function requested(search) {
  const value = new URLSearchParams(String(search || '')).get('collecte');
  if (value === null) return {mode: 'current'};
  return isArchiveId(value) ? {mode: 'archive', id: value} : {mode: 'invalid', value};
 }

 const count = n => Number.isInteger(n) && n >= 0;
 function isEntry(c) {
  return !!c && typeof c === 'object' && isArchiveId(c.id) && ['edition_date', 'window_start', 'window_end'].every(k => ISO_DATE.test(String(c[k])))
   && Object.hasOwn(STATUS, c.status) && ['articles', 'candidats', 'ecartes'].every(k => count(c[k]))
   && typeof c.archived_at === 'string' && !Number.isNaN(Date.parse(c.archived_at));
 }
 // Index publié, la collecte la plus récente en premier ; une entrée illisible
 // est écartée et comptée plutôt que de bloquer toute la page.
 function parseIndex(data) {
  if (!data || typeof data !== 'object' || data.schema_version !== INDEX_SCHEMA || !Array.isArray(data.collectes)) throw new Error('INDEX_ILLISIBLE');
  const collectes = data.collectes.filter(isEntry);
  return {collectes, ignored: data.collectes.length - collectes.length};
 }

 const plural = (n, word) => `${n} ${word}${n > 1 ? 's' : ''}`;
 function parisTime(iso) {
  const parts = {};
  const format = new Intl.DateTimeFormat('fr-FR', {timeZone: 'Europe/Paris', year: 'numeric', month: '2-digit', day: '2-digit',
   hour: '2-digit', minute: '2-digit', hourCycle: 'h23'});
  for (const p of format.formatToParts(new Date(iso))) parts[p.type] = p.value;
  return `${S.dateLong(`${parts.year}-${parts.month}-${parts.day}`)} à ${Number(parts.hour)} h ${parts.minute}`;
 }
 function describe(c) {
  const [status, statusClass] = STATUS[c.status];
  return {title: `Édition du ${S.dateLong(c.edition_date)}`,
   period: `Période du ${S.dateLong(c.window_start)} au ${S.dateLong(c.window_end)}`, status, statusClass,
   counts: [plural(c.articles, 'article'), plural(c.candidats, 'candidat'), plural(c.ecartes, 'écarté')],
   archived: `Archivée le ${parisTime(c.archived_at)} (heure de Paris)`};
 }

 global.VeilleArchives = {FILES, isArchiveId, indexUrl, fileUrl, archiveUrl, selectionHref, requested, parseIndex, describe};

 if (typeof document === 'undefined' || !document.getElementById('archives-list')) return;

 // ---------- Interface ----------
 const byId = id => document.getElementById(id);
 function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
 }
 const hidden = text => el('span', 'fr-sr-only', text);
 const announce = text => { byId('archives-status').textContent = text; };
 function showError(message) {
  const box = byId('archives-error');
  box.hidden = false;
  box.replaceChildren(el('h2', 'fr-alert__title', 'Archives indisponibles'), el('p', '', message));
 }

 // Le lien direct reste utilisable sans script ; avec script, le fichier est
 // relu frais puis enregistré sous un nom explicite.
 async function download(event, id, name) {
  event.preventDefault();
  try {
   const r = await fetch(archiveUrl(id, name, Date.now()), G.timed({cache: 'no-store'}));
   if (!r.ok) throw new Error(r.status === 404 ? 'fichier pas encore disponible, réessayez dans quelques minutes' : `erreur ${r.status}`);
   const url = URL.createObjectURL(new Blob([await r.text()], {type: 'application/json;charset=utf-8'}));
   const a = document.createElement('a');
   a.href = url; a.download = `veille-snum-${id}-${name}`;
   document.body.append(a); a.click(); a.remove();
   setTimeout(() => URL.revokeObjectURL(url), 1000);
   byId('download-status').textContent = `Fichier ${name} de la collecte ${id} téléchargé.`;
  } catch (err) {
   byId('download-status').textContent = `Téléchargement impossible (${String(err.message || err)}).`;
  }
 }

 function card(c) {
  const d = describe(c), li = el('li', 'fr-col-12 fr-col-md-6');
  const box = el('div', 'fr-card'), body = el('div', 'fr-card__body'), content = el('div', 'fr-card__content');
  const counts = el('ul');
  for (const text of d.counts) counts.append(el('li', '', text));
  const start = el('div', 'fr-card__start'), badges = el('ul', 'fr-badges-group'), badge = el('p', `fr-badge fr-badge--sm ${d.statusClass}`);
  badge.append(hidden('Statut : '), document.createTextNode(d.status));
  badges.append(el('li')); badges.firstChild.append(badge); start.append(badges);
  const end = el('div', 'fr-card__end');
  end.append(counts, el('p', 'fr-card__detail', d.archived));
  content.append(el('h2', 'fr-card__title', d.title), el('p', 'fr-card__desc', d.period), start, end);
  const footer = el('div', 'fr-card__footer'), links = el('ul', 'fr-links-group');
  for (const f of FILES) {
   const a = el('a', 'fr-link fr-link--download', f.label);
   a.href = fileUrl(c.id, f.name);
   a.addEventListener('click', event => download(event, c.id, f.name));
   a.append(hidden(` de l’${d.title.toLowerCase()}`), el('span', 'fr-link__detail', 'JSON'));
   const item = el('li'); item.append(a); links.append(item);
  }
  const btns = el('ul', 'fr-btns-group fr-btns-group--inline-md fr-mt-2w'), open = el('a', 'fr-btn', 'Ouvrir dans la page de sélection');
  open.href = selectionHref(c.id);
  open.append(hidden(` : ${d.title.toLowerCase()}`));
  btns.append(el('li')); btns.firstChild.append(open);
  footer.append(links, btns);
  body.append(content, footer); box.append(body); li.append(box);
  return li;
 }

 async function load() {
  let r;
  try { r = await fetch(indexUrl(Date.now()), G.timed({cache: 'no-store'})); }
  catch (_) { announce(''); showError('raw.githubusercontent.com est injoignable : vérifiez la connexion réseau puis rechargez la page.'); return; }
  if (r.status === 404) { announce('Aucune collecte archivée pour l’instant.'); return; }
  let got;
  try {
   if (!r.ok) throw new Error(`le serveur a répondu ${r.status}`);
   got = parseIndex(await r.json());
  } catch (err) {
   announce('');
   const why = err.message === 'INDEX_ILLISIBLE' ? 'l’index ne suit pas le schéma SNUM_ARCHIVES_V1' : String(err.message || err);
   showError(`Les archives n’ont pas pu être chargées (${why}). Réessayez dans quelques minutes.`);
   return;
  }
  const n = got.collectes.length;
  let text = n > 1 ? `${n} collectes archivées, de la plus récente à la plus ancienne.`
   : n ? '1 collecte archivée.' : 'Aucune collecte archivée pour l’instant.';
  if (got.ignored) text += got.ignored > 1 ? ` ${got.ignored} entrées illisibles de l’index ont été ignorées.` : ' 1 entrée illisible de l’index a été ignorée.';
  announce(text);
  byId('archives-list').replaceChildren(...got.collectes.map(card));
 }
 load();
})(typeof window !== 'undefined' ? window : globalThis);
