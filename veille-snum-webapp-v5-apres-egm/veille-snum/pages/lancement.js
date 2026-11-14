'use strict';
// Lancement d'une collecte ou d'une rédaction de résumés par GitHub Actions, suivi de
// l'exécution, puis vérification de ce que le site publie réellement : etat-collecte.json
// porte le numéro du run qui l'a produit. GitHub Pages garde ses fichiers dix minutes en
// cache et un paramètre d'adresse ne contourne pas ce cache (constat du 13 novembre 2026) :
// la page attend donc la nouvelle version au lieu de présenter l'ancienne comme le résultat.
// Première partie : fonctions pures (tests/test_pages_lancement.cjs). Seconde : interface.
(function (global) {
 const G = global.VeilleGithub;
 const FRESH_TRIES = 24, FRESH_WAIT_MS = 5000;

 const publishedBy = (etat, id) => !!etat && etat.run_id !== undefined && etat.run_id !== null && String(etat.run_id) === String(id);
 // Issue d'un run terminé, selon sa conclusion et l'état publié : 'publie', 'attente'
 // (succès pas encore visible sur le site), 'publie-en-echec' ou 'echec'.
 function outcome(state, etat, id) {
  const published = publishedBy(etat, id);
  if (state === 'success') return published ? 'publie' : 'attente';
  return published ? 'publie-en-echec' : 'echec';
 }
 // « depuis 14 h 32 » (heure de Paris), précédé d'une espace ; vide si la date est illisible.
 function sinceText(iso) {
  const date = new Date(String(iso || ''));
  if (Number.isNaN(date.getTime())) return '';
  const parts = {};
  for (const p of new Intl.DateTimeFormat('fr-FR', {timeZone: 'Europe/Paris', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'}).formatToParts(date)) parts[p.type] = p.value;
  return ` depuis ${Number(parts.hour)} h ${parts.minute}`;
 }
 const TEXT = {
  active: since => `Une collecte ou une rédaction de résumés est déjà en cours sur GitHub${since} : elle a été lancée depuis une autre page, ou avant un rechargement de celle-ci. Attendez sa fin, puis rechargez cette page : son résultat s’y affichera. Pour lancer quand même, activez de nouveau le bouton : votre demande attendra la fin de celle en cours, puis remplacera son résultat ; GitHub annule alors toute autre demande déjà en attente.`,
  notice: since => `Une collecte ou une rédaction de résumés est en cours sur GitHub${since}. Son résultat s’affichera ici après rechargement de la page : inutile de la relancer.`,
  lost: (subject, why) => `${why} Le suivi s’arrête ici, mais ${subject} continue peut-être sur GitHub : rechargez cette page dans quelques minutes pour voir le résultat, sans relancer.`,
  stale: name => `${name} terminée sur GitHub, mais le site sert encore l’ancienne version (cache de GitHub Pages, dix minutes au plus). Rechargez cette page dans quelques minutes : le résultat s’y affichera. Ne relancez pas.`,
  publishedFailed: text => `Les fichiers ont été publiés et la page les affiche, mais l’exécution s’est ensuite terminée en échec (${text}). Rien n’est à relancer : le détail de l’exécution dit ce qui a manqué.`,
 };

 // Le paquet lu est-il celui que décrit l'état publié ? Sans état (site antérieur), rien à comparer.
 const sameEdition = (etat, packet) => !etat || ['edition_date', 'window_start', 'window_end'].every(k => String(etat[k]) === String(packet[k]));

 global.VeilleLancement = {FRESH_TRIES, FRESH_WAIT_MS, publishedBy, outcome, sameEdition, sinceText, TEXT};

 if (typeof document === 'undefined' || !document.getElementById('collect-form')) return;

 // ---------- Interface ----------
 const byId = id => document.getElementById(id);
 const COLLECT_UI = {status: 'collect-status', error: 'collect-error', elapsed: 'collect-elapsed', run: 'collect-run'};
 let running = false, acknowledged = '';
 let hooks = {load: async () => false, readEtat: async () => null};

 const visible = node => !!node && node.getClientRects().length > 0;
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
  if (url) box.append(runLink('Voir le détail de l’exécution sur GitHub (nouvelle fenêtre)', url));
 }
 function showRun(ui, url) {
  byId(ui.run).replaceChildren();
  if (url) byId(ui.run).append(runLink('Suivre l’exécution sur GitHub (nouvelle fenêtre)', url));
 }
 // Fin d'un lancement : message dans la zone du bouton utilisé, repris dans la zone de
 // la collecte ; l'erreur y est reprise aussi quand la première zone a disparu avec sa vue.
 function conclude(ui, status, error, link) {
  say(ui, status); showError(ui, error, link);
  if (ui === COLLECT_UI) return;
  say(COLLECT_UI, status);
  showError(COLLECT_UI, visible(byId(ui.status)) ? '' : error, link);
 }
 // Si le bouton utilisé a disparu avec l'ancienne vue, le focus passe au titre de la nouvelle.
 function keepFocus(button) {
  if (visible(button)) return;
  const next = ['summary-heading', 'titres-heading', 'load-error'].map(byId).find(visible) || byId('collect');
  if (next.tagName !== 'BUTTON') next.setAttribute('tabindex', '-1');
  next.focus();
 }

 // Lance publier-paquet-snum.yml, suit l'exécution, puis relit ce que le site publie.
 // o : {inputs, token, button, ui, busy, restore, name, subject, duration, before, onAccepted, failed, done}.
 // failed(texte, étatEnLigne) renvoie {message, reload} ; done(vue) renvoie le message de fin.
 async function launch(o) {
  const {ui, button} = o, fresh = () => String(Date.now());
  // Une erreur d'affichage des fichiers relus ne doit pas passer pour une interruption du lancement.
  const reload = () => hooks.load(fresh()).catch(() => false);
  running = true;
  showError(ui, ''); showRun(ui, ''); showError(COLLECT_UI, '');
  // Le bouton garde le focus : il est marqué indisponible au lieu d'être désactivé.
  button.setAttribute('aria-disabled', 'true'); button.textContent = o.busy;
  const startedAt = Date.now();
  let link = '', sent = false;
  try {
   say(ui, 'Vérification auprès de GitHub…');
   const other = await G.findActive('collecte', o.token);
   if (other && other.id !== acknowledged) {
    acknowledged = other.id;
    throw Object.assign(new Error(TEXT.active(sinceText(other.since))), {link: other.htmlUrl});
   }
   if (o.before) await o.before();
   say(ui, 'Envoi de la demande à GitHub…');
   const run = await G.dispatch('collecte', o.inputs, o.token);
   sent = true; acknowledged = ''; link = run.htmlUrl; showRun(ui, link);
   if (o.onAccepted) o.onAccepted();
   say(ui, `${o.name} acceptée par GitHub.`);
   const end = await G.follow(run.id, o.token, startedAt, p => {
    if (p.htmlUrl && p.htmlUrl !== link) { link = p.htmlUrl; showRun(ui, link); }
    say(ui, `${o.name} : ${p.text}.`);
    byId(ui.elapsed).textContent = `Temps écoulé : ${G.elapsed(p.elapsed)}. ${o.duration}`;
   });
   say(ui, `${o.name} terminée sur GitHub : lecture des fichiers publiés…`);
   let etat = await hooks.readEtat(fresh());
   // L'archivage précède la publication : après un échec, rien de neuf n'est attendu sur le site.
   const expected = end.state === 'success';
   for (let i = 0; expected && !publishedBy(etat, run.id) && i < FRESH_TRIES; i++) {
    say(ui, `${o.name} terminée sur GitHub : la page publiée se met à jour, nouvelle lecture dans quelques secondes…`);
    await G.sleep(FRESH_WAIT_MS);
    etat = await hooks.readEtat(fresh());
   }
   const result = outcome(end.state, etat, run.id);
   if (result === 'attente') { conclude(ui, `${o.name} terminée, résultat pas encore visible.`, TEXT.stale(o.name), link); return; }
   if (result === 'echec') {
    const failure = o.failed(end.text, etat);
    if (failure.reload) await reload();
    conclude(ui, `${o.name} en échec.`, failure.message, link);
    return;
   }
   const view = await reload();
   if (result === 'publie-en-echec') conclude(ui, `${o.name} publiée, mais exécution en échec.`, TEXT.publishedFailed(end.text), link);
   else conclude(ui, view ? o.done(view) : `${o.name} terminée, mais les fichiers publiés n’ont pas pu être relus : rechargez la page.`, '');
  } catch (err) {
   const why = String(err.message || err);
   if (err.lost) {
    // Page vidée au lancement : ce qui est publié pour l'instant est réaffiché.
    if (sent && o.onAccepted) await reload();
    conclude(ui, `${o.name} : suivi interrompu.`, TEXT.lost(o.subject, why), link);
   } else conclude(ui, sent ? `${o.name} interrompue.` : `${o.name} non lancée.`, why, err.link || link);
  } finally {
   running = false;
   button.removeAttribute('aria-disabled'); button.textContent = o.restore();
   keepFocus(button);
  }
 }

 // À l'ouverture de la page, sans jeton : prévient si une collecte tourne déjà (autre
 // personne, autre onglet, page rechargée en cours de route). Sans réponse, rien n'est dit.
 async function announceActive() {
  const run = await G.findActive('collecte', '');
  if (!run || running) return;
  say(COLLECT_UI, TEXT.notice(sinceText(run.since)));
  showRun(COLLECT_UI, run.htmlUrl);
 }

 Object.assign(global.VeilleLancement, {COLLECT_UI, say, showError, launch, announceActive, isRunning: () => running,
  configure: o => { hooks = {...hooks, ...o}; }});
})(typeof window !== 'undefined' ? window : globalThis);
