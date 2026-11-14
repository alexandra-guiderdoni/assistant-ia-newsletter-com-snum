'use strict';
// Lancement et suivi des workflows GitHub Actions depuis la page statique.
// Le jeton est fourni à chaque appel par l'appelant : ce module ne le conserve
// pas, ne l'écrit nulle part et ne l'inclut jamais dans un message d'erreur.
(function (global) {
 const REPO = 'alexandra-guiderdoni/assistant-ia-newsletter-com-snum';
 const API = `https://api.github.com/repos/${REPO}`;
 // Branche publique des données produites par GitHub Actions : archives des
 // collectes (collectes/) et résultats de repêchage (repechages/).
 const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/donnees-veille/`;
 const RAW = `${RAW_BASE}repechages/`;
 const WORKFLOWS = {collecte: 'publier-paquet-snum.yml', repechage: 'repecher-candidat.yml'};
 const API_VERSION = '2026-03-10';
 const POLL_MS = 10000;
 // Délai maximal d'un appel : sans lui, une requête restée sans réponse bloquerait le suivi et le bouton.
 const CALL_TIMEOUT_MS = 30000;
 const FOLLOW_LIMIT_MS = 45 * 60000;
 const WAITING = ['queued', 'waiting', 'pending', 'requested'];
 const FAILED = ['failure', 'timed_out', 'cancelled', 'startup_failure'];
 const CONCLUSIONS = {failure: 'échec', cancelled: 'annulé', timed_out: 'délai dépassé', action_required: 'action requise',
  startup_failure: 'échec au démarrage', skipped: 'ignoré', neutral: 'sans conclusion', stale: 'périmé'};

 function isoToFr(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  if (!m) throw new Error('DATE_INVALIDE');
  return `${m[3]}/${m[2]}/${m[1]}`;
 }
 // Jetons GitHub : lettres, chiffres et soulignés. Refuser le reste évite toute
 // injection d'en-tête et signale un copier-coller incomplet.
 const tokenLooksValid = token => /^[A-Za-z0-9_]{20,255}$/.test(String(token || ''));
 const headers = token => ({Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': API_VERSION});
 const runId = id => { if (!/^\d+$/.test(String(id))) throw new Error('RUN_INVALIDE'); return String(id); };

 const collectInputs = (edition, start, end) => ({edition: isoToFr(edition), debut: isoToFr(start), fin: isoToFr(end)});
 function repechageInputs(url, rubric, start, end) {
  if (!global.VeilleSelection.RUBRICS.includes(rubric)) throw new Error('RUBRIQUE_INVALIDE');
  if (!/^https:\/\/[^\s]+$/.test(String(url))) throw new Error('URL_INVALIDE');
  isoToFr(start); isoToFr(end);
  return {url, rubrique: rubric, debut: start, fin: end};
 }
 const dispatchRequest = (workflow, inputs, token) => ({
  url: `${API}/actions/workflows/${WORKFLOWS[workflow]}/dispatches`,
  init: {method: 'POST', headers: {...headers(token), 'Content-Type': 'application/json'}, body: JSON.stringify({ref: 'main', inputs}), cache: 'no-store'},
 });
 const runsListUrl = workflow => `${API}/actions/workflows/${WORKFLOWS[workflow]}/runs?event=workflow_dispatch&per_page=5`;
 // Run le plus récent qui n'est pas terminé, pour prévenir avant un doublon ; null sinon.
 function activeRun(runs) {
  const run = (Array.isArray(runs) ? runs : []).find(r => r && typeof r.status === 'string' && r.status !== 'completed' && /^\d+$/.test(String(r.id)));
  return run ? {id: String(run.id), htmlUrl: githubLink(run.html_url), since: String(run.created_at || '')} : null;
 }
 const runUrl = id => `${API}/actions/runs/${runId(id)}`;
 const jobsUrl = id => `${API}/actions/runs/${runId(id)}/jobs`;
 const repechageResultUrl = (id, bust) => `${RAW}${runId(id)}.json?t=${encodeURIComponent(bust)}`;

 // Réponse 204 sans corps : le run est le plus récent créé après l'envoi, avec une tolérance
 // de 30 secondes pour l'écart entre les horloges. known : numéros des runs qui existaient
 // avant l'envoi (lancement d'une autre personne), jamais pris pour le nôtre.
 function pickRun(runs, sentAt, known) {
  const before = (known || []).map(String);
  const recent = (Array.isArray(runs) ? runs : []).filter(r => r && Date.parse(r.created_at) >= sentAt - 30000 && !before.includes(String(r.id)));
  recent.sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  return recent[0] || null;
 }

 // Première étape en échec d'un run terminé : {job, step}, ou null si GitHub ne la donne pas.
 function failedStep(jobs) {
  const job = (jobs && Array.isArray(jobs.jobs) ? jobs.jobs : []).find(j => j && FAILED.includes(j.conclusion));
  if (!job) return null;
  const step = (job.steps || []).find(s => s && FAILED.includes(s.conclusion));
  return {job: String(job.name || ''), step: String((step || job).name || '')};
 }

 // Libellé de progression à partir du run et de ses tâches.
 function progress(run, jobs) {
  if (!run || typeof run !== 'object') return {state: 'pending', text: 'Lancement demandé, en attente de GitHub Actions'};
  if (run.status === 'completed') {
   if (run.conclusion === 'success') return {state: 'success', text: 'Terminé avec succès'};
   const failed = failedStep(jobs);
   const where = failed && failed.step ? ` à l’étape « ${failed.step} »` : '';
   return {state: 'failure', text: `Terminé sans succès : ${CONCLUSIONS[run.conclusion] || 'issue inconnue'}${where}`, failedJob: failed ? failed.job : ''};
  }
  if (WAITING.includes(run.status)) return {state: 'pending', text: 'En file d’attente sur GitHub Actions'};
  const list = jobs && Array.isArray(jobs.jobs) ? jobs.jobs : [];
  const job = list.find(j => j.status === 'in_progress') || list.find(j => WAITING.includes(j.status));
  if (!job) return {state: 'pending', text: 'Exécution en cours'};
  if (job.name === 'deploiement') return {state: 'pending', text: 'Déploiement de la page sur GitHub Pages'};
  const step = (job.steps || []).find(s => s.status === 'in_progress');
  if (step) return {state: 'pending', text: `Étape en cours : ${step.name}`};
  return {state: 'pending', text: job.status === 'in_progress' ? 'Passage à l’étape suivante' : 'Tâche en attente d’un exécuteur'};
 }

 function elapsed(ms) {
  const s = Math.max(0, Math.floor(ms / 1000));
  return `${Math.floor(s / 60)} min ${String(s % 60).padStart(2, '0')} s`;
 }

 function httpError(status) {
  switch (status) {
  case 401: return 'GitHub a refusé le jeton (erreur 401) : il est incomplet, expiré ou révoqué. Collez-le de nouveau en entier ou créez-en un nouveau, en suivant le lien « Créer ou renouveler un jeton GitHub » de la section « Connexion à GitHub ».';
  case 403: return 'GitHub a refusé la demande (erreur 403) : ce jeton n’a pas le droit de lancer une tâche. Il lui faut la permission « Actions : Read and write » sur le dépôt (lien « Créer ou renouveler un jeton GitHub »). Si le jeton est correct, GitHub limite peut-être les appels : réessayez dans une heure.';
  case 404: return `GitHub ne trouve pas le dépôt avec ce jeton (erreur 404) : le jeton ne donne pas accès au dépôt ${REPO}. Vérifiez le dépôt choisi à la création du jeton (lien « Créer ou renouveler un jeton GitHub »).`;
  case 422: return 'GitHub a refusé la demande (erreur 422) : les dates ou la sélection envoyées ne sont pas acceptées. Rechargez la page puis réessayez ; si l’erreur revient, signalez-la à la personne qui gère le dépôt.';
  case 429: return 'GitHub limite temporairement les appels (erreur 429) : réessayez dans quelques minutes.';
  default: return `GitHub a répondu par une erreur ${status} : réessayez dans quelques minutes.`;
  }
 }

 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
 const lost = message => Object.assign(new Error(message), {lost: true});
 // Chaque appel est abandonné après CALL_TIMEOUT_MS : un abandon vaut « injoignable ».
 // Un navigateur sans AbortSignal.timeout garde l'appel sans délai plutôt que d'échouer.
 const timed = init => (typeof AbortSignal !== 'undefined' && AbortSignal.timeout ? {...init, signal: AbortSignal.timeout(CALL_TIMEOUT_MS)} : init);
 async function call(url, init) {
  try { return await fetch(url, timed(init)); }
  catch (_) { throw new Error('GitHub est injoignable : vérifiez la connexion réseau puis réessayez.'); }
 }
 const read = token => ({headers: headers(token), cache: 'no-store'});
 const githubLink = url => (/^https:\/\/github\.com\//.test(String(url || '')) ? url : '');

 // Envoie le déclenchement et renvoie {id, htmlUrl} du run créé.
 async function dispatch(workflow, inputs, token) {
  // Runs déjà présents, relevés avant l'envoi : sans numéro dans la réponse, ils sont écartés de la recherche.
  let known = [];
  try {
   const b = await call(runsListUrl(workflow), read(token));
   if (b.ok) known = ((((await b.json().catch(() => null)) || {}).workflow_runs) || []).filter(Boolean).map(x => x.id);
  } catch (_) { known = []; }
  const sentAt = Date.now();
  const {url, init} = dispatchRequest(workflow, inputs, token);
  const r = await call(url, init);
  if (r.status === 200) {
   const x = await r.json().catch(() => null);
   if (x && x.workflow_run_id) return {id: runId(x.workflow_run_id), htmlUrl: githubLink(x.html_url)};
  } else if (r.status !== 204) throw new Error(httpError(r.status));
  for (let attempt = 0; attempt < 8; attempt++) {
   await sleep(attempt ? 3000 : 2000);
   const l = await call(runsListUrl(workflow), read(token));
   if (!l.ok) throw lost(httpError(l.status));
   const run = pickRun(((await l.json().catch(() => null)) || {}).workflow_runs, sentAt, known);
   if (run) return {id: runId(run.id), htmlUrl: githubLink(run.html_url)};
  }
  throw lost('La demande est partie, mais GitHub n’a pas indiqué quelle exécution lui correspond.');
 }

 // Lecture facultative du run en cours, avec jeton ou sans (dépôt public) : toute erreur vaut « inconnu ».
 async function findActive(workflow, token) {
  try {
   const r = await fetch(runsListUrl(workflow), timed(token ? read(token) : {headers: {Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': API_VERSION}, cache: 'no-store'}));
   return r.ok ? activeRun(((await r.json()) || {}).workflow_runs) : null;
  } catch (_) { return null; }
 }

 // Interroge le run toutes les 10 secondes jusqu'à sa fin ; onUpdate reçoit
 // {state, text, elapsed, htmlUrl}. Trois échecs d'affilée arrêtent le suivi, pas le run :
 // l'erreur porte alors lost = true, pour que la page ne parle pas d'un échec.
 async function follow(id, token, startedAt, onUpdate) {
  let failures = 0;
  for (;;) {
   try {
    const [r, j] = await Promise.all([call(runUrl(id), read(token)), call(jobsUrl(id), read(token))]);
    if (!r.ok) throw new Error(httpError(r.status));
    const run = await r.json();
    const jobs = j.ok ? await j.json().catch(() => null) : null;
    failures = 0;
    const p = {...progress(run, jobs), elapsed: Date.now() - startedAt, htmlUrl: githubLink(run.html_url)};
    onUpdate(p);
    if (p.state !== 'pending') return p;
   } catch (err) {
    if (++failures >= 3) throw lost(String(err.message || err));
   }
   if (Date.now() - startedAt > FOLLOW_LIMIT_MS) throw lost('Le suivi s’arrête après 45 minutes.');
   await sleep(POLL_MS);
  }
 }

 // Résultat public du repêchage, lu sans jeton ; il peut mettre quelques
 // secondes à apparaître après la fin du run.
 async function readRepechage(id) {
  for (let attempt = 0; attempt < 6; attempt++) {
   if (attempt) await sleep(4000);
   let r;
   try { r = await fetch(repechageResultUrl(id, Date.now()), timed({cache: 'no-store'})); } catch (_) { continue; }
   if (r.ok) return r.json();
   if (r.status !== 404) throw new Error(`Résultat du repêchage illisible (erreur ${r.status}).`);
  }
  throw new Error('Le résultat du repêchage n’est pas encore publié : réessayez dans une minute.');
 }

 global.VeilleGithub = {REPO, RAW_BASE, WORKFLOWS, POLL_MS, CALL_TIMEOUT_MS, timed, isoToFr, tokenLooksValid, collectInputs, repechageInputs, dispatchRequest,
  runsListUrl, runUrl, jobsUrl, repechageResultUrl, pickRun, activeRun, failedStep, progress, elapsed, httpError, sleep, dispatch, findActive, follow, readRepechage};
})(typeof window !== 'undefined' ? window : globalThis);
