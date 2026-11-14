'use strict';
// Page Veille SNUM sur GitHub Pages : chargement des fichiers publiés, connexion
// à GitHub et formulaire de collecte ; GitHub Actions joue le rôle du serveur
// local (collecte, Albert, publication) et lancement.js suit son exécution.
// etat-collecte.json indique la phase publiée : « titres » affiche les titres à
// trier (titres.js), sinon le paquet V519. Avec ?collecte=<id>, la page rouvre
// une collecte archivée (archives.js) au lieu des fichiers du site.
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
 const L = global.VeilleLancement, COLLECT_UI = L.COLLECT_UI, showError = L.showError;
 const byId = id => document.getElementById(id);
 const target = A.requested(global.location.search);
 let shownView = '';

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

 // Collecte en cours : fichiers du site. Archive : branche donnees-veille. cache: 'no-store'
 // écarte le cache du navigateur, pas celui de GitHub (dix minutes pour le site, cinq pour
 // les archives). GitHub Pages répond parfois 503 un court instant : une seconde lecture suit.
 async function fetchJson(name, bust) {
  const url = target.mode === 'archive' ? A.archiveUrl(target.id, name, bust || Date.now()) : `./${name}${bust ? `?v=${bust}` : ''}`;
  for (let attempt = 0; ; attempt++) {
   let r;
   try { r = await fetch(url, G.timed({cache: 'no-store'})); } catch (_) { throw new Error('le site est injoignable'); }
   if (r.status === 404) return {missing: true};
   if (r.ok) return {data: await r.json()};
   if (r.status < 500 || attempt) throw new Error(`le serveur a répondu ${r.status}`);
   await G.sleep(1500);
  }
 }
 function showParts(view) {
  byId('titres-section').hidden = view !== 'titres';
  for (const node of document.querySelectorAll('[data-paquet]')) node.hidden = view !== 'paquet';
  shownView = view;
 }

 // État publié : absent d'un site antérieur, jamais lu en mode archive ; unread : lecture en échec.
 async function readEtat(bust) {
  if (target.mode !== 'current') return {etat: null, unread: false};
  try { const got = await fetchJson('etat-collecte.json', bust); return {etat: got.missing ? null : T.parseEtat(got.data), unread: false}; }
  catch (_) { return {etat: null, unread: true}; }
 }
 // Lit l'état publié, puis la vue qui lui correspond.
 // Renvoie 'titres', 'paquet', ou false si les fichiers n'ont pas pu être chargés.
 async function load(bust) {
  const {etat, unread} = await readEtat(bust);
  byId('reset-notice').hidden = true;
  byId('reset-status').textContent = '';
  return T.view(etat) === 'titres' ? loadTitres(etat, bust) : loadPaquet(bust, unread);
 }

 async function loadTitres(etat, bust) {
  let report = null, why = 'le fichier ne suit pas le format du rapport de collecte';
  try {
   const got = await fetchJson('rapport-collecte.json', bust);
   if (got.missing) why = 'le serveur a répondu 404';
   else if (R.isReport(got.data)) report = got.data;
  } catch (err) { why = String(err.message || err); }
  if (!report) {
   S.showLoadError(`Les titres trouvés n’ont pas pu être chargés (${why}). Rechargez la page dans une minute ; ne lancez une nouvelle collecte que si le problème persiste.`);
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

 // Charge le paquet, puis le rapport et les candidats. unread : l'état publié n'a pas pu être lu,
 // la page ignore donc si des titres attendent d'être triés et ne conseille pas de relancer.
 async function loadPaquet(bust, unread) {
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
    : unread ? `Les fichiers publiés n’ont pas pu être lus (${why}) : GitHub Pages est peut-être indisponible un instant. Rechargez la page dans une minute ; ne lancez une nouvelle collecte que si le problème persiste.`
     : `Le paquet de la semaine n’a pas pu être chargé (${why}). Lancez une collecte ou réessayez plus tard.`);
   if (unread) byId('load-error').firstChild.textContent = 'Page momentanément illisible';
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
  // Annonce propre, que la progression de la collecte ne remplace pas.
  byId('reset-status').textContent = `La page repart de zéro. ${byId('reset-text').textContent}`;
  shownView = '';
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
 // Paquet publié sans article : le dire, avec quoi faire.
 const emptyNote = () => (S.packet() && !S.packet().articles.length ? ' Ce paquet ne contient aucun article : repêchez un candidat écarté, ou lancez une collecte sur une période plus large.' : '');
 const busyReason = () => (L.isRunning() ? 'Une collecte ou une rédaction de résumés est en cours : attendez sa fin.'
  : E.isBusy() ? 'Un repêchage est en cours : attendez sa fin.' : '');

 byId('collect-form').addEventListener('submit', async event => {
  event.preventDefault();
  const button = byId('collect');
  if (target.mode !== 'current' || button.getAttribute('aria-disabled') === 'true') return;
  if (L.isRunning()) { showError(COLLECT_UI, busyReason()); return; }
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
  await L.launch({inputs: T.launchInputs(values.edition, values.start, values.end, complete), token, button, ui: COLLECT_UI,
   busy: 'Collecte en cours…', restore: () => 'Lancer la collecte', name: 'Collecte', subject: 'la collecte', onAccepted: reset,
   duration: complete ? 'Une collecte complète dure de cinq à neuf minutes, selon le nombre d’articles trouvés.' : 'La recherche des titres dure trois à quatre minutes.',
   failed: text => ({reload: true, message: `La collecte n’a pas abouti (${text}) : la page affiche de nouveau ce qui était publié avant ce lancement. Vous pouvez relancer ; si l’échec se répète, réessayez plus tard.`}),
   done: view => (view === 'titres' ? 'Collecte terminée : la page affiche les titres trouvés ; gardez ceux à faire résumer par Albert.'
    : `Collecte terminée : la page affiche le nouveau paquet, le rapport et les candidats écartés.${emptyNote()}`)});
 });

 const fresh = () => String(Date.now());
 L.configure({load, readEtat: async bust => (await readEtat(bust)).etat});
 T.configure({hasToken, requireToken, isBusy: busyReason, readEtat: async () => (await readEtat(fresh())).etat, reload: () => load(fresh()),
  launch: o => L.launch({...o, done: view => (view === 'paquet' ? `Résumés rédigés : la page affiche le nouveau paquet, le rapport et les candidats écartés.${emptyNote()}`
   : 'Rédaction terminée, mais la page publiée affiche encore les titres : rechargez-la dans quelques minutes.')})});
 E.configure({requireToken, isCollecting: L.isRunning});
 tokenHints();
 if (target.mode === 'invalid') {
  byId('archive-title').textContent = 'Collecte archivée introuvable';
  byId('archive-text').textContent = 'Identifiant de collecte invalide.';
  S.showLoadError(`L’identifiant de collecte « ${target.value} » n’est pas valide : rouvrez la collecte depuis la page des archives.`);
 } else load('').then(() => { if (target.mode === 'current') L.announceActive(); });
})(typeof window !== 'undefined' ? window : globalThis);
