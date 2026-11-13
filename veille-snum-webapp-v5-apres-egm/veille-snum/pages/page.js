'use strict';
// Page Veille SNUM sur GitHub Pages : chargement des fichiers publiés, connexion
// à GitHub et lancement de la collecte par GitHub Actions, qui joue le rôle du
// serveur local (collecte, Albert, publication).
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
 const S = global.VeilleSelection, G = global.VeilleGithub, R = global.VeilleRapport, E = global.VeilleEcartes;
 const byId = id => document.getElementById(id);
 let collecting = false;

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
 function requireToken() {
  const token = byId('gh-token').value.trim();
  if (!token) setFieldError('gh-token', 'Saisissez un jeton GitHub pour lancer une collecte ou repêcher un article.');
  else if (!G.tokenLooksValid(token)) setFieldError('gh-token', 'Ce jeton ne ressemble pas à un jeton GitHub : vérifiez le copier-coller.');
  else { setFieldError('gh-token', ''); return token; }
  byId('gh-token').focus();
  return null;
 }
 function tokenHints() {
  const has = byId('gh-token').value.trim() !== '';
  byId('collect-hint').textContent = has
   ? 'Jeton GitHub saisi : il reste dans cette page et disparaît à sa fermeture.'
   : 'Un jeton GitHub est nécessaire pour lancer la collecte (section « Connexion à GitHub »).';
  byId('repechage-hint').textContent = has
   ? 'Le repêchage utilise le jeton GitHub saisi plus haut.'
   : 'Un jeton GitHub est nécessaire pour repêcher un article (section « Connexion à GitHub »).';
 }
 byId('gh-token').addEventListener('input', () => { if (byId('gh-token').getAttribute('aria-invalid')) setFieldError('gh-token', ''); tokenHints(); });
 byId('gh-token-forget').addEventListener('click', () => {
  byId('gh-token').value = '';
  setFieldError('gh-token', '');
  tokenHints();
  byId('gh-token-status').textContent = 'Jeton effacé de la page.';
 });

 const status = text => { byId('collect-status').textContent = text; };
 function showError(message, url) {
  const box = byId('collect-error');
  box.hidden = !message;
  box.replaceChildren();
  if (!message) return;
  const p = document.createElement('p'); p.textContent = message; box.append(p);
  if (url) {
   const a = document.createElement('a');
   a.className = 'fr-link'; a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
   a.textContent = 'Consulter le run sur GitHub (nouvelle fenêtre)';
   box.append(a);
  }
 }
 function showRun(url) {
  const p = byId('collect-run');
  p.replaceChildren();
  if (!url) return;
  const a = document.createElement('a');
  a.className = 'fr-link'; a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
  a.textContent = 'Suivre le run sur GitHub (nouvelle fenêtre)';
  p.append(a);
 }

 async function fetchJson(name, bust) {
  const r = await fetch(`./${name}${bust ? `?v=${bust}` : ''}`, {cache: 'no-store'});
  if (r.status === 404) return {missing: true};
  if (!r.ok) throw new Error(`le serveur a répondu ${r.status}`);
  return {data: await r.json()};
 }

 // Charge le paquet, puis le rapport et les candidats ; bust force une lecture fraîche après un lancement.
 async function load(bust) {
  let packet;
  try {
   const got = await fetchJson('paquet-v519.json', bust);
   if (got.missing) throw new Error('le serveur a répondu 404');
   if (!S.isPacket(got.data)) throw new Error('le fichier ne suit pas le schéma SNUM_PAQUET_RENDU_V519');
   packet = got.data;
  } catch (err) {
   S.showLoadError(`Le paquet de la semaine n’a pas pu être chargé (${String(err.message || err)}). Lancez une collecte ou réessayez plus tard.`);
   return false;
  }
  S.mount(packet);
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
  return true;
 }

 const dates = defaultDates(new Date());
 for (const [id] of DATE_FIELDS) {
  byId(id).value = dates[id];
  byId(id).addEventListener('input', () => { if (byId(id).getAttribute('aria-invalid')) setFieldError(id, ''); });
 }

 byId('collect-form').addEventListener('submit', async event => {
  event.preventDefault();
  const button = byId('collect');
  if (collecting) return;
  const values = Object.fromEntries(DATE_FIELDS.map(([id]) => [id, byId(id).value]));
  const errors = dateErrors(values.edition, values.start, values.end);
  for (const [id] of DATE_FIELDS) {
   byId(id).required = true;
   setFieldError(id, errors[id]);
  }
  const first = DATE_FIELDS.map(([id]) => id).find(id => errors[id]);
  if (first) { byId(first).focus(); showError('Corrigez les champs signalés avant de lancer la collecte.'); return; }
  if (E.isBusy()) { showError('Un repêchage est en cours : attendez sa fin avant de lancer une collecte.'); return; }
  const token = requireToken();
  if (!token) { showError('Un jeton GitHub est nécessaire pour lancer la collecte.'); return; }
  collecting = true;
  showError(''); showRun('');
  // Le bouton garde le focus : il est marqué indisponible au lieu d'être désactivé.
  button.setAttribute('aria-disabled', 'true'); button.textContent = 'Collecte en cours…';
  const startedAt = Date.now();
  let runLink = '';
  try {
   status('Envoi de la demande de collecte à GitHub…');
   const run = await G.dispatch('collecte', G.collectInputs(values.edition, values.start, values.end), token);
   runLink = run.htmlUrl; showRun(runLink);
   const end = await G.follow(run.id, token, startedAt, p => {
    if (p.htmlUrl && p.htmlUrl !== runLink) { runLink = p.htmlUrl; showRun(runLink); }
    status(`Collecte : ${p.text}.`);
    byId('collect-elapsed').textContent = `Temps écoulé : ${G.elapsed(p.elapsed)}. Une collecte dure environ huit minutes.`;
   });
   if (end.state !== 'success') throw new Error(`La collecte n’a pas abouti (${end.text}) : le paquet publié précédemment reste en place.`);
   status('Collecte terminée : rechargement du paquet publié…');
   const ok = await load(String(Date.now()));
   status(ok ? 'Collecte terminée : la page affiche le nouveau paquet, le rapport et les candidats écartés.' : 'Collecte terminée, mais le nouveau paquet n’a pas pu être relu.');
  } catch (err) {
   status('Collecte interrompue.');
   showError(String(err.message || err), runLink);
  } finally {
   collecting = false;
   button.removeAttribute('aria-disabled'); button.textContent = 'Lancer la collecte';
  }
 });

 E.configure({requireToken, isCollecting: () => collecting});
 tokenHints();
 load('');
})(typeof window !== 'undefined' ? window : globalThis);
