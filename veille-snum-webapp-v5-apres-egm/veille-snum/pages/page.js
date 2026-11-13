'use strict';
// Page Veille SNUM sur GitHub Pages : chargement des fichiers publiés, connexion
// à GitHub et lancement de la collecte par GitHub Actions, qui joue le rôle du
// serveur local (collecte, Albert, publication). etat-collecte.json indique la
// phase publiée : « titres » affiche les titres à trier (titres.js), sinon le
// paquet V519. Avec ?collecte=<id>, la page rouvre une collecte archivée
// (archives.js) au lieu des fichiers du site.
(function (global) {
 const DATE_FIELDS = [['edition', 'la date d’édition'], ['start', 'la date de début de période'], ['end', 'la date de fin de période']];
 const pad = n => String(n).padStart(2, '0');
 const localIso = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

 // Mêmes valeurs par défaut que la page locale : aujourd'hui, et sept jours avant.
 function defaultDates(now) {
  const start = new Date(now);
  start.setDate(start.getDate() - 7);
  return {edition: localIso(now), start: localIso(start), end: localIso(now)};
 }
 // Mêmes contrôles que validateDates (veille_snum/app.js) : {champ: message}.
 function dateErrors(edition, start, end) {
  const values = {edition, start, end}, errors = {};
  for (const [id, name] of DATE_FIELDS) if (!values[id]) errors[id] = `Indiquez ${name}.`;
  if (!errors.start && !errors.end) {
   if (start > end) errors.end = 'La fin de période doit être identique ou postérieure au début.';
   else if ((Date.parse(end) - Date.parse(start)) / 86400000 > 60) errors.end = 'La période ne peut pas dépasser 61 jours.';
  }
  return errors;
 }

 global.VeillePage = {defaultDates, dateErrors};

 if (typeof document === 'undefined' || !document.getElementById('collect-form')) return;

 // ---------- Interface ----------
 const S = global.VeilleSelection, G = global.VeilleGithub, R = global.VeilleRapport, E = global.VeilleEcartes, A = global.VeilleArchives, T = global.VeilleTitres;
 const byId = id => document.getElementById(id);
 const target = A.requested(global.location.search);
 const COLLECT_UI = {status: 'collect-status', error: 'collect-error', elapsed: 'collect-elapsed', run: 'collect-run'};
 let collecting = false, shownView = '';

 function setFieldError(id, message) {
  const group = byId(`${id}-group`), box = byId(`${id}-messages`), field = byId(id);
  box.replaceChildren();
  group.classList.toggle('fr-input-group--error', !!message);
  if (message) {
   const p = document.createElement('p');
   p.className = 'fr-message fr-message--error'; p.textContent = message;
   box.append(p);
   field.setAttribute('aria-invalid', 'true');
  } else field.removeAttribute('aria-invalid');
 }

 // Le jeton n'existe que dans le champ de la page : jamais stocké, ni journalisé, ni mis dans l'adresse.
 const hasToken = () => byId('gh-token').value.trim() !== '';
 function requireToken() {
  const token = byId('gh-token').value.trim();
  if (!token) setFieldError('gh-token', 'Saisissez un jeton GitHub pour lancer une collecte ou repêcher un article.');
  else if (!G.tokenLooksValid(token)) setFieldError('gh-token', 'Ce jeton ne ressemble pas à un jeton GitHub : vérifiez le copier-coller.');
  else { setFieldError('gh-token', ''); return token; }
  byId('gh-token').focus();
  return null;
 }
 function tokenHints() {
  byId('collect-hint').textContent = hasToken()
   ? 'Jeton GitHub saisi : il reste dans cette page et disparaît à sa fermeture.'
   : 'Un jeton GitHub est nécessaire pour lancer la collecte (section « Connexion à GitHub »).';
  byId('repechage-hint').textContent = hasToken()
   ? 'Le repêchage utilise le jeton GitHub saisi plus haut.'
   : 'Un jeton GitHub est nécessaire pour repêcher un article (section « Connexion à GitHub »).';
  if (shownView === 'titres') T.refresh();
 }
 byId('gh-token').addEventListener('input', () => { if (byId('gh-token').getAttribute('aria-invalid')) setFieldError('gh-token', ''); tokenHints(); });
 byId('gh-token-forget').addEventListener('click', () => {
  byId('gh-token').value = '';
  setFieldError('gh-token', '');
  tokenHints();
  byId('gh-token-status').textContent = 'Jeton effacé de la page.';
 });

 const say = (ui, text) => { byId(ui.status).textContent = text; };
 function runLink(text, url) {
  const a = document.createElement('a');
  a.className = 'fr-link'; a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = text;
  return a;
 }
 function showError(ui, message, url) {
  const box = byId(ui.error);
  box.hidden = !message;
  box.replaceChildren();
  if (!message) return;
  const p = document.createElement('p'); p.textContent = message; box.append(p);
  if (url) box.append(runLink('Consulter le run sur GitHub (nouvelle fenêtre)', url));
 }
 function showRun(ui, url) {
  byId(ui.run).replaceChildren();
  if (url) byId(ui.run).append(runLink('Suivre le run sur GitHub (nouvelle fenêtre)', url));
 }

 // Collecte en cours : fichiers du site. Archive : branche donnees-veille, toujours relue fraîche.
 async function fetchJson(name, bust) {
  const url = target.mode === 'archive' ? A.archiveUrl(target.id, name, bust || Date.now()) : `./${name}${bust ? `?v=${bust}` : ''}`;
  const r = await fetch(url, {cache: 'no-store'});
  if (r.status === 404) return {missing: true};
  if (!r.ok) throw new Error(`le serveur a répondu ${r.status}`);
  return {data: await r.json()};
 }
 function showParts(view) {
  byId('titres-section').hidden = view !== 'titres';
  for (const node of document.querySelectorAll('[data-paquet]')) node.hidden = view !== 'paquet';
  shownView = view;
 }

 // Lit l'état publié (absent sur un site antérieur, jamais en mode archive), puis la vue qui lui correspond.
 // Renvoie 'titres', 'paquet', ou false si les fichiers n'ont pas pu être chargés.
 async function load(bust) {
  let etat = null;
  if (target.mode === 'current') {
   try { const got = await fetchJson('etat-collecte.json', bust); etat = got.missing ? null : T.parseEtat(got.data); } catch (_) { etat = null; }
  }
  byId('reset-notice').hidden = true;
  return T.view(etat) === 'titres' ? loadTitres(etat, bust) : loadPaquet(bust);
 }

 async function loadTitres(etat, bust) {
  let report = null, why = 'le fichier ne suit pas le format du rapport de collecte';
  try {
   const got = await fetchJson('rapport-collecte.json', bust);
   if (got.missing) why = 'le serveur a répondu 404';
   else if (R.isReport(got.data)) report = got.data;
  } catch (err) { why = String(err.message || err); }
  if (!report) {
   S.showLoadError(`Les titres trouvés n’ont pas pu être chargés (${why}). Réessayez dans quelques minutes.`);
   byId('load-error').firstChild.textContent = 'Titres indisponibles';
   shownView = '';
   return false;
  }
  byId('load-error').hidden = true;
  byId('selection-content').hidden = false;
  showParts('titres');
  T.mount(etat, report);
  R.render(report, null, '', 'titres');
  return 'titres';
 }

 // Charge le paquet, puis le rapport et les candidats ; bust force une lecture fraîche après un lancement.
 async function loadPaquet(bust) {
  let packet;
  try {
   const got = await fetchJson('paquet-v519.json', bust);
   if (got.missing) throw new Error('le serveur a répondu 404');
   if (!S.isPacket(got.data)) throw new Error('le fichier ne suit pas le schéma SNUM_PAQUET_RENDU_V519');
   packet = got.data;
  } catch (err) {
   const why = String(err.message || err);
   S.showLoadError(target.mode === 'archive'
    ? `Le paquet de la collecte archivée ${target.id} n’a pas pu être chargé (${why}). Une archive récente peut mettre quelques minutes à être lisible : réessayez plus tard.`
    : `Le paquet de la semaine n’a pas pu être chargé (${why}). Lancez une collecte ou réessayez plus tard.`);
   if (target.mode === 'archive') byId('archive-text').textContent = 'Collecte archivée indisponible.';
   shownView = '';
   return false;
  }
  showParts('paquet');
  S.mount(packet);
  if (target.mode === 'archive') showArchive(packet);
  try {
   const got = await fetchJson('rapport-collecte.json', bust);
   R.render(got.missing ? null : got.data, packet, got.missing ? 'Le rapport de collecte n’est pas publié pour cette édition (paquet publié avant son ajout).' : '');
  } catch (_) {
   R.render(null, packet, 'Le rapport de collecte n’a pas pu être chargé.');
  }
  try {
   const got = await fetchJson('candidats-ecartes.json', bust);
   E.render(got.missing ? null : got.data, got.missing ? 'Aucune liste de candidats écartés n’est publiée pour cette édition.' : '');
  } catch (_) {
   E.render(null, 'La liste des candidats écartés n’a pas pu être chargée.');
  }
  return 'paquet';
 }

 // Lancement accepté par GitHub : l'ancienne collecte disparaît de la page, elle est dans les archives.
 function reset() {
  byId('reset-text').textContent = shownView === 'titres'
   ? 'Les titres précédents, jamais résumés, ne sont pas archivés ; les collectes précédentes résumées sont consultables dans les archives.'
   : 'La collecte précédente est consultable dans les archives.';
  for (const id of ['article-list', 'candidates-list', 'titres-list', 'found-list']) byId(id).replaceChildren();
  byId('selection-content').hidden = true;
  byId('load-error').hidden = true;
  byId('reset-notice').hidden = false;
  shownView = '';
 }

 // Si le bouton utilisé a disparu avec l'ancienne vue, le focus passe au titre de la nouvelle.
 const visible = node => !!node && node.getClientRects().length > 0;
 function keepFocus(button) {
  if (visible(button)) return;
  const next = ['summary-heading', 'titres-heading', 'load-error'].map(byId).find(visible) || byId('collect');
  if (next.tagName !== 'BUTTON') next.setAttribute('tabindex', '-1');
  next.focus();
 }

 // Lance publier-paquet-snum.yml, suit le run, puis relit les fichiers publiés.
 // o : {inputs, token, button, ui, busy, restore, name, duration, failed, done, onAccepted}.
 async function launch(o) {
  const {ui, button} = o;
  collecting = true;
  showError(ui, ''); showRun(ui, '');
  // Le bouton garde le focus : il est marqué indisponible au lieu d'être désactivé.
  button.setAttribute('aria-disabled', 'true'); button.textContent = o.busy;
  const startedAt = Date.now();
  let link = '', accepted = false;
  try {
   say(ui, 'Envoi de la demande à GitHub…');
   const run = await G.dispatch('collecte', o.inputs, o.token);
   accepted = true; link = run.htmlUrl; showRun(ui, link);
   if (o.onAccepted) { o.onAccepted(); say(ui, `${o.name} acceptée par GitHub : la page repart de zéro, la collecte précédente est dans les archives.`); }
   const end = await G.follow(run.id, o.token, startedAt, p => {
    if (p.htmlUrl && p.htmlUrl !== link) { link = p.htmlUrl; showRun(ui, link); }
    say(ui, `${o.name} : ${p.text}.`);
    byId(ui.elapsed).textContent = `Temps écoulé : ${G.elapsed(p.elapsed)}. ${o.duration}`;
   });
   if (end.state !== 'success') throw new Error(o.failed(end.text));
   say(ui, `${o.name} terminée : rechargement de la page…`);
   const view = await load(String(Date.now()));
   const text = view ? o.done(view) : `${o.name} terminée, mais les fichiers publiés n’ont pas pu être relus.`;
   say(ui, text);
   if (ui !== COLLECT_UI) say(COLLECT_UI, text);
  } catch (err) {
   say(ui, `${o.name} interrompue.`);
   showError(ui, String(err.message || err), link);
   // Page vidée mais rien de nouveau publié : la collecte en ligne est réaffichée.
   if (accepted && o.onAccepted) await load(String(Date.now()));
  } finally {
   collecting = false;
   button.removeAttribute('aria-disabled'); button.textContent = o.restore();
   keepFocus(button);
  }
 }

 // Mode archive : bandeau explicite, lancement de collecte retiré ; le repêchage reste possible.
 function showArchive(packet) {
  const when = packet.edition_date_long || S.dateLong(packet.edition_date);
  byId('archive-title').textContent = `Collecte archivée du ${when}`;
  byId('archive-text').textContent = `Vous consultez la collecte archivée ${target.id}, période du ${S.dateLong(packet.window_start)} au ${S.dateLong(packet.window_end)}. La sélection, l’export et la copie portent sur cette collecte ; la collecte en cours n’est pas modifiée.`;
  document.title = `Veille SNUM · Collecte archivée du ${when}`;
 }
 if (target.mode !== 'current') {
  byId('archive-notice').hidden = false;
  byId('collect-section').hidden = true;
 }

 const dates = defaultDates(new Date());
 for (const [id] of DATE_FIELDS) {
  byId(id).value = dates[id];
  byId(id).addEventListener('input', () => { if (byId(id).getAttribute('aria-invalid')) setFieldError(id, ''); });
 }
 const busyReason = () => (collecting ? 'Une collecte ou une rédaction de résumés est en cours : attendez sa fin.'
  : E.isBusy() ? 'Un repêchage est en cours : attendez sa fin.' : '');

 byId('collect-form').addEventListener('submit', async event => {
  event.preventDefault();
  const button = byId('collect');
  if (target.mode !== 'current' || button.getAttribute('aria-disabled') === 'true') return;
  if (collecting) { showError(COLLECT_UI, busyReason()); return; }
  const values = Object.fromEntries(DATE_FIELDS.map(([id]) => [id, byId(id).value]));
  const errors = dateErrors(values.edition, values.start, values.end);
  for (const [id] of DATE_FIELDS) {
   byId(id).required = true;
   setFieldError(id, errors[id]);
  }
  const first = DATE_FIELDS.map(([id]) => id).find(id => errors[id]);
  if (first) { byId(first).focus(); showError(COLLECT_UI, 'Corrigez les champs signalés avant de lancer la collecte.'); return; }
  if (E.isBusy()) { showError(COLLECT_UI, 'Un repêchage est en cours : attendez sa fin avant de lancer une collecte.'); return; }
  const token = requireToken();
  if (!token) { showError(COLLECT_UI, 'Un jeton GitHub est nécessaire pour lancer la collecte.'); return; }
  const complete = byId('complete').checked;
  await launch({inputs: T.launchInputs(values.edition, values.start, values.end, complete), token, button, ui: COLLECT_UI,
   busy: 'Collecte en cours…', restore: () => 'Lancer la collecte', name: 'Collecte', onAccepted: reset,
   duration: complete ? 'Une collecte complète dure environ huit minutes.' : 'La recherche des titres dure environ trois minutes.',
   failed: text => `La collecte n’a pas abouti (${text}) : la page affiche de nouveau la collecte publiée précédemment.`,
   done: view => (view === 'titres' ? 'Collecte terminée : la page affiche les titres trouvés ; gardez ceux à faire résumer par Albert.'
    : 'Collecte terminée : la page affiche le nouveau paquet, le rapport et les candidats écartés.')});
 });

 T.configure({hasToken, requireToken, isBusy: busyReason,
  launch: o => launch({...o, done: view => (view === 'paquet' ? 'Résumés rédigés : la page affiche le nouveau paquet, le rapport et les candidats écartés.'
   : 'Rédaction terminée, mais la page publiée affiche encore les titres : rechargez-la dans quelques minutes.')})});
 E.configure({requireToken, isCollecting: () => collecting});
 tokenHints();
 if (target.mode === 'invalid') {
  byId('archive-title').textContent = 'Collecte archivée introuvable';
  byId('archive-text').textContent = 'Identifiant de collecte invalide.';
  S.showLoadError(`L’identifiant de collecte « ${target.value} » n’est pas valide : rouvrez la collecte depuis la page des archives.`);
 } else load('');
})(typeof window !== 'undefined' ? window : globalThis);
