'use strict';
// Lancement et suivi des workflows GitHub Actions depuis la page statique.
// Le jeton est fourni à chaque appel par l'appelant : ce module ne le conserve
// pas, ne l'écrit nulle part et ne l'inclut jamais dans un message d'erreur.
(function (global) {
 const REPO = 'alexandra-guiderdoni/assistant-ia-newsletter-com-snum';
 const API = `https://api.github.com/repos/${REPO}`;
 const RAW = `https://raw.githubusercontent.com/${REPO}/donnees-repechage/repechages/`;
 const WORKFLOWS = {collecte: 'publier-paquet-snum.yml', repechage: 'repecher-candidat.yml'};
 const API_VERSION = '2026-03-10';
 const POLL_MS = 10000;
 const FOLLOW_LIMIT_MS = 45 * 60000;
 const WAITING = ['queued', 'waiting', 'pending', 'requested'];
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
 const runUrl = id => `${API}/actions/runs/${runId(id)}`;
 const jobsUrl = id => `${API}/actions/runs/${runId(id)}/jobs`;
 const repechageResultUrl = (id, bust) => `${RAW}${runId(id)}.json?t=${encodeURIComponent(bust)}`;

 // Réponse 204 sans corps : le run est le plus récent créé après l'envoi,
 // avec une tolérance de 30 secondes pour l'écart entre les horloges.
 function pickRun(runs, sentAt) {
  const recent = (Array.isArray(runs) ? runs : []).filter(r => r && Date.parse(r.created_at) >= sentAt - 30000);
  recent.sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  return recent[0] || null;
 }

 // Libellé de progression à partir du run et de ses tâches.
 function progress(run, jobs) {
  if (!run || typeof run !== 'object') return {state: 'pending', text: 'Lancement demandé, en attente de GitHub Actions'};
  if (run.status === 'completed') {
   if (run.conclusion === 'success') return {state: 'success', text: 'Terminé avec succès'};
   return {state: 'failure', text: `Terminé sans succès : ${CONCLUSIONS[run.conclusion] || 'issue inconnue'}`};
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
  case 401: return 'GitHub a refusé le jeton (erreur 401) : vérifiez qu’il est complet et qu’il n’a pas expiré.';
  case 403: return 'GitHub a refusé l’accès (erreur 403) : le jeton doit avoir la permission « Actions : Read and write » sur le dépôt, ou la limite d’appels de l’API est atteinte.';
  case 404: return 'Dépôt ou workflow introuvable (erreur 404) : le jeton ne donne pas accès au dépôt, ou le workflow n’existe pas sur la branche main.';
  case 422: return 'GitHub a refusé le lancement (erreur 422) : entrées invalides ou déclenchement manuel absent sur la branche main.';
  default: return `GitHub a répondu par une erreur ${status}. Réessayez dans quelques minutes.`;
  }
 }

 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
 async function call(url, init) {
  try { return await fetch(url, init); }
  catch (_) { throw new Error('GitHub est injoignable : vérifiez la connexion réseau puis réessayez.'); }
 }
 const read = token => ({headers: headers(token), cache: 'no-store'});
 const githubLink = url => (/^https:\/\/github\.com\//.test(String(url || '')) ? url : '');

 // Envoie le déclenchement et renvoie {id, htmlUrl} du run créé.
 async function dispatch(workflow, inputs, token) {
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
   if (!l.ok) throw new Error(httpError(l.status));
   const run = pickRun(((await l.json().catch(() => null)) || {}).workflow_runs, sentAt);
   if (run) return {id: runId(run.id), htmlUrl: githubLink(run.html_url)};
  }
  throw new Error('Lancement envoyé, mais le run n’a pas été retrouvé : consultez l’onglet Actions du dépôt.');
 }

 // Interroge le run toutes les 10 secondes jusqu'à sa fin ; onUpdate reçoit
 // {state, text, elapsed, htmlUrl}. Trois échecs réseau d'affilée arrêtent le suivi.
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
    if (++failures >= 3) throw err;
   }
   if (Date.now() - startedAt > FOLLOW_LIMIT_MS) throw new Error('Suivi interrompu après 45 minutes : consultez le run sur GitHub.');
   await sleep(POLL_MS);
  }
 }

 // Résultat public du repêchage, lu sans jeton ; il peut mettre quelques
 // secondes à apparaître après la fin du run.
 async function readRepechage(id) {
  for (let attempt = 0; attempt < 6; attempt++) {
   if (attempt) await sleep(4000);
   let r;
   try { r = await fetch(repechageResultUrl(id, Date.now()), {cache: 'no-store'}); } catch (_) { continue; }
   if (r.ok) return r.json();
   if (r.status !== 404) throw new Error(`Résultat du repêchage illisible (erreur ${r.status}).`);
  }
  throw new Error('Le résultat du repêchage n’est pas encore publié : réessayez dans une minute.');
 }

 global.VeilleGithub = {REPO, WORKFLOWS, POLL_MS, isoToFr, tokenLooksValid, collectInputs, repechageInputs, dispatchRequest,
  runsListUrl, runUrl, jobsUrl, repechageResultUrl, pickRun, progress, elapsed, httpError, dispatch, follow, readRepechage};
})(typeof window !== 'undefined' ? window : globalThis);
