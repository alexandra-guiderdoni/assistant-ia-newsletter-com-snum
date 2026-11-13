'use strict';
// Rapport de collecte publié (rapport-collecte.json) : mêmes compteurs et mêmes
// listes que la page locale (showResult dans veille_snum/app.js).
(function (global) {
 const STATUS_NAMES = {checked: 'Découverte effectuée', partial: 'Partielle / tronquée', skipped_budget: 'Non traitée (temps)',
  skipped_internal: 'Non traitée (source interne)', blocked: 'Bloquée (robots.txt ou protection anti-robot)',
  error: 'Échec technique', pending: 'En attente'};
 const MESSAGES = {
  ready: 'Paquet disponible : relecture des sources obligatoire.',
  partial: 'Collecte partielle : vérifiez les erreurs et les alertes.',
  needs_albert: 'Candidats recherchés, mais Albert n’est pas configuré : aucun paquet V519 exportable.',
  unavailable: 'Aucune source publique vérifiée : collecte techniquement indisponible.',
 };
 const sum = (sources, key) => sources.reduce((n, s) => n + (s[key] || 0), 0);

 function isReport(r) {
  return !!r && typeof r === 'object' && typeof r.status === 'string' && Array.isArray(r.sources)
   && Array.isArray(r.candidates) && Array.isArray(r.excluded);
 }
 const statusMessage = status => MESSAGES[status] || 'Impossible de produire un paquet complet : consulter les erreurs.';

 // Huit compteurs [valeur, libellé], dans l'ordre de la page locale.
 function stats(report, packet) {
  const s = report.sources;
  return [
   [`${s.filter(x => x.status === 'checked').length}/13`, 'sources explorées sans réserve'],
   [`${s.filter(x => x.status === 'partial').length}`, 'sources partielles ou plafonnées'],
   [`${sum(s, 'opened')}/${sum(s, 'attempted')}`, 'pages reçues sur pages tentées'],
   [`${sum(s, 'not_visited')}`, 'adresses découvertes non visitées'],
   [`${report.candidates.length}`, 'candidats trouvés'],
   [`${packet && Array.isArray(packet.articles) ? packet.articles.length : 0}`, 'articles préparés'],
   [`${report.excluded.length}`, 'exclusions et erreurs'],
   [`${report.discovery_errors || 0}`, 'erreurs de plan de site'],
  ];
 }

 const sourceLine = s => `${s.label} : ${STATUS_NAMES[s.status] || s.status} · ${s.discovered || 0} URL découvertes · ${s.attempted || 0} tentées · ${s.opened || 0} pages reçues · ${s.eligible || 0} candidats · ${s.technical_errors || 0} erreurs d’articles · ${s.discovery_errors || 0} erreurs de découverte · ${s.sitemap_skipped || 0} URL/sitemaps ignorés · ${s.not_visited || 0} non tentées. ${(s.notes || []).join(' ; ')}`;

 global.VeilleRapport = {STATUS_NAMES, isReport, statusMessage, stats, sourceLine};

 if (typeof document === 'undefined' || !document.getElementById('report-section')) return;

 // ---------- Interface ----------
 const byId = id => document.getElementById(id);
 let current = null;

 function line(list, text, url) {
  const li = document.createElement('li');
  if (url && /^https:\/\//.test(String(url))) {
   const a = document.createElement('a');
   a.className = 'fr-link'; a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
   a.textContent = text; a.title = `${text} - nouvelle fenêtre`;
   li.append(a);
  } else li.textContent = text;
  list.append(li);
 }
 function fill(id, items, toLine, empty) {
  const list = byId(id);
  list.replaceChildren();
  if (!items.length) { line(list, empty); return; }
  for (const item of items) { const [text, url] = toLine(item); line(list, text, url); }
 }

 // report null : rapport absent (paquet publié avant) ou illisible, message affiché à la place.
 function render(report, packet, message) {
  current = isReport(report) ? report : null;
  byId('report-content').hidden = !current;
  byId('report-download').disabled = !current;
  const intro = byId('report-intro');
  if (!current) { intro.textContent = message || 'Le rapport de collecte n’est pas publié pour cette édition.'; return; }
  intro.textContent = `Statut de la collecte : ${statusMessage(current.status)}`;
  if (packet && current.edition_date && current.edition_date !== packet.edition_date) {
   intro.textContent += ` Attention : ce rapport concerne l’édition du ${global.VeilleSelection.dateLong(current.edition_date)}.`;
  }
  const box = byId('report-stats');
  box.replaceChildren();
  // Un chiffre mis en valeur, puis son libellé : grille de 2 puis 3 colonnes.
  for (const [value, label] of stats(current, packet)) {
   const li = document.createElement('li');
   li.className = 'fr-col-6 fr-col-md-4';
   const number = document.createElement('p'); number.className = 'fr-h4 fr-mb-0'; number.textContent = value;
   const caption = document.createElement('p'); caption.className = 'fr-text--sm fr-mb-0'; caption.textContent = label;
   li.append(number, caption);
   box.append(li);
  }
  fill('source-list', current.sources, s => [sourceLine(s)], 'Aucune source dans le rapport.');
  fill('found-list', current.candidates, c => [`${c.publication_date_iso} · ${c.title} (${c.source})`, c.url], 'Aucun candidat trouvé.');
  fill('excluded-list', current.excluded, x => [`${x.source} : ${x.reason} (${x.url})`], 'Aucune exclusion.');
  fill('error-list', current.errors || [], x => [`${x.reason} (${x.url})`], 'Aucune erreur d’analyse Albert.');
 }

 byId('report-download').addEventListener('click', () => {
  if (!current) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(current, null, 2) + '\n'], {type: 'application/json;charset=utf-8'}));
  const a = document.createElement('a');
  a.href = url; a.download = `veille-snum-rapport-${current.edition_date}.json`;
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
  byId('report-status').textContent = 'Téléchargement du rapport proposé : vérifiez la présence du fichier.';
 });

 global.VeilleRapport.render = render;
})(typeof window !== 'undefined' ? window : globalThis);
