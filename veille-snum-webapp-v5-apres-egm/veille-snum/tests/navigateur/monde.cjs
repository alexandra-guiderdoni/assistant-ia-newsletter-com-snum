// Monde simulé pour les parcours Chromium de Veille SNUM : le site public, api.github.com et
// raw.githubusercontent.com sont interceptés (aucune requête réelle ne sort), et chaque run lancé par
// la page exécute le VRAI code serveur (produire.py) contre l'état en ligne du moment.
// Playwright n'est pas une dépendance du dépôt : PLAYWRIGHT désigne son dossier, sinon le module « playwright » du poste.
const {chromium} = require(process.env.PLAYWRIGHT || 'playwright');
const fs = require('fs');
const path = require('path');
const {spawnSync} = require('child_process');

const REPO = 'alexandra-guiderdoni/assistant-ia-newsletter-com-snum';
const SITE = `https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/`;
const API = `https://api.github.com/repos/${REPO}`;
const RAW = `https://raw.githubusercontent.com/${REPO}/donnees-veille/`;
const DATA = ['etat-collecte.json', 'rapport-collecte.json', 'paquet-v519.json', 'candidats-ecartes.json'];
const TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css', '.json': 'application/json',
 '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json'};
const WORKFLOWS = {'publier-paquet-snum.yml': {inputs: ['edition', 'debut', 'fin', 'mode', 'selection'], modes: ['titres', 'resumes', 'collecte', 'page seule']},
 'repecher-candidat.yml': {inputs: ['url', 'rubrique', 'debut', 'fin'], required: ['url', 'rubrique', 'debut', 'fin'], rubriques: ['ia', 'administration', 'dsi', 'economie', 'infrastructure', 'securite', 'applications', 'droit', 'commande', 'rh', 'bercy']}};
const ETAPES = {titres: 'Collecte des titres, sans Albert', resumes: 'Résumés des titres gardés', collecte: 'Collecte et paquet V519', repechage: 'Repêchage par Albert'};

function creerMonde(o) {
 const proto = o.proto, travail = o.travail;
 fs.mkdirSync(travail, {recursive: true});
 const m = {
  SITE, API, RAW, proto, travail,
  enLigne: o.enLigne || null,     // dossier des fichiers de données publiés
  perime: null,                   // {dossier, lectures} : le CDN sert encore l'ancien dossier pendant n lectures de l'état
  delaiCdn: 0,                    // nombre de lectures périmées après chaque déploiement
  absent: 404,                    // code servi pour un fichier absent (GitHub Pages répond parfois 503)
  pannes: {},                     // nom de fichier -> nombre de réponses 503 à servir d'abord
  jetons: {},                     // jeton -> 'ok' | 'expire' | 'lecture' | 'sans-acces'
  attente: 1,                     // nombre de lectures « en file d'attente » avant le démarrage d'un run
  reponse204: false,              // ancien comportement de l'API : 204 sans corps au lancement
  albert: {}, illisibles: [], jeu: o.jeu || 'synthetique', rapportReel: o.rapportReel || '',
  echecApres: {},                 // mode -> nom de la tâche qui échoue après la publication (ex. archivage)
  runs: [], raw: {}, appels: [], fuites: [], prochain: 9000,
 };
 m.html = id => `https://github.com/${REPO}/actions/runs/${id}`;
 const lire = (dossier, nom) => { try { return fs.readFileSync(path.join(dossier, nom)); } catch (_) { return null; } };

 // ---------- Site public ----------
 m.site = async route => {
  const url = new URL(route.request().url());
  let rel = decodeURIComponent(url.pathname).replace('/assistant-ia-newsletter-com-snum/', '');
  if (rel === '') rel = 'index.html';
  if (DATA.includes(rel)) {
   m.appels.push({hote: 'site', url: url.href});
   if (m.pannes[rel] > 0) { m.pannes[rel] -= 1; return route.fulfill({status: 503, contentType: 'text/html', body: 'indisponible'}); }
   let dossier = m.enLigne;
   if (m.perime) { dossier = m.perime.dossier; if (rel === 'etat-collecte.json' && --m.perime.lectures <= 0) m.perime = null; }
   const corps = dossier ? lire(dossier, rel) : null;
   if (!corps) return route.fulfill({status: m.absent, contentType: 'text/html', body: 'Page not found'});
   return route.fulfill({status: 200, contentType: 'application/json; charset=utf-8', headers: {'cache-control': 'max-age=600'}, body: corps});
  }
  const fichier = rel.startsWith('dsfr/') ? path.join(proto, 'veille_snum', rel) : path.join(proto, 'pages', rel);
  const corps = lire(path.dirname(fichier), path.basename(fichier));
  if (!corps) return route.fulfill({status: 404, contentType: 'text/html', body: 'Page not found'});
  return route.fulfill({status: 200, contentType: TYPES[path.extname(fichier)] || 'application/octet-stream', body: corps});
 };

 // ---------- Runs ----------
 const actif = r => r.status !== 'completed';
 function produire(run, consigne) {
  const fichier = path.join(travail, `consigne-${run.id}.json`);
  fs.writeFileSync(fichier, JSON.stringify({jeu: m.jeu, rapport_reel: m.rapportReel, albert: m.albert, illisibles: m.illisibles, run_id: run.id, ...consigne}));
  const r = spawnSync('python3', [path.join(__dirname, 'produire.py'), proto, fichier], {encoding: 'utf8'});
  run.journal = (r.stdout || '') + (r.stderr || '');
  return r.status;
 }
 function demarrer(run) {
  run.status = 'in_progress';
  if (run.workflow === 'repecher-candidat.yml') {
   run.etape = ETAPES.repechage;
   const sortie = path.join(travail, `repechage-${run.id}.json`);
   produire(run, {mode: 'repechage', inputs: run.inputs, sortie, en_ligne: m.enLigne});
   run.fin = () => { const corps = lire(travail, `repechage-${run.id}.json`); if (corps) m.raw[`repechages/${run.id}.json`] = corps.toString(); };
   run.code = 0;   // un refus n'arrête pas la tâche : son motif est publié
   return;
  }
  const mode = run.inputs.mode === undefined || run.inputs.mode === '' ? 'titres' : run.inputs.mode;
  run.mode = mode; run.etape = ETAPES[mode];
  const sortie = path.join(travail, `site-${run.id}`);
  run.code = produire(run, {mode, inputs: run.inputs, sortie, en_ligne: m.enLigne});
  run.fin = () => {
   if (run.code !== 0 || m.echecApres[mode] === 'archivage') return;
   if (m.delaiCdn > 0 && m.enLigne) m.perime = {dossier: m.enLigne, lectures: m.delaiCdn};
   m.enLigne = sortie;
   const vide = (mode === 'resumes' || mode === 'collecte') && JSON.parse(fs.readFileSync(path.join(sortie, 'paquet-v519.json'), 'utf8')).articles.length === 0;
   if ((mode === 'resumes' || mode === 'collecte') && !vide) {
    const archive = path.join(travail, `archive-${run.id}`);
    fs.mkdirSync(archive, {recursive: true});
    const ancien = path.join(travail, 'index-ancien.json');
    if (m.raw['collectes/index.json']) fs.writeFileSync(ancien, m.raw['collectes/index.json']); else fs.rmSync(ancien, {force: true});
    produire({id: run.id}, {mode: 'archive', site: sortie, ancien, sortie: archive});
    const entree = JSON.parse(fs.readFileSync(path.join(archive, 'entree.json'), 'utf8'));
    m.raw['collectes/index.json'] = fs.readFileSync(path.join(archive, 'index.json'), 'utf8');
    for (const nom of DATA.slice(1)) m.raw[`collectes/${entree.id}/${nom}`] = fs.readFileSync(path.join(sortie, nom), 'utf8');
   }
  };
 }
 // Une lecture du run le fait avancer d'un cran : file d'attente, étape, déploiement, fin.
 function avancer(run) {
  if (run.status === 'completed' || run.fige) return;
  if (run.status === 'queued' || run.status === 'pending') {
   const devant = m.runs.some(r => r !== run && r.workflow === run.workflow && run.workflow === 'publier-paquet-snum.yml' && actif(r) && r.id < run.id);
   if (devant) { run.status = 'pending'; return; }
   if (run.patience-- > 0) { run.status = 'queued'; return; }
   demarrer(run); run.cran = 0; return;
  }
  run.cran += 1;
  if (run.cran >= (run.duree || 2)) {
   const apres = run.code === 0 ? m.echecApres[run.mode] : null;
   if (run.fin) run.fin();
   run.status = 'completed';
   run.conclusion = run.code === 0 && !apres ? 'success' : 'failure';
   run.echec = run.code !== 0 ? ['collecte', run.etape] : apres ? [apres, apres === 'archivage' ? 'Archiver la collecte' : 'Déploiement'] : null;
  } else if (run.cran === (run.duree || 2) - 1 && run.code === 0 && run.workflow === 'publier-paquet-snum.yml') run.deploiement = true;
 }
 function jobs(run) {
  if (run.status === 'queued' || run.status === 'pending') return [];
  const etape = (nom, statut, conclusion) => ({name: nom, status: statut, conclusion: conclusion || null});
  const nom = run.workflow === 'repecher-candidat.yml' ? 'repechage' : 'collecte';
  if (run.status === 'completed') {
   const liste = [{name: nom, status: 'completed', conclusion: run.echec && run.echec[0] === nom ? 'failure' : 'success',
    steps: [etape('Set up job', 'completed', 'success'), etape(run.etape, 'completed', run.echec && run.echec[0] === nom ? 'failure' : 'success')]}];
   if (run.echec && run.echec[0] !== nom) liste.push({name: run.echec[0], status: 'completed', conclusion: 'failure', steps: [etape(run.echec[1], 'completed', 'failure')]});
   return liste;
  }
  if (run.deploiement) return [{name: nom, status: 'completed', conclusion: 'success', steps: []}, {name: 'deploiement', status: 'in_progress', steps: []}];
  return [{name: nom, status: 'in_progress', steps: [etape('Set up job', 'completed', 'success'), etape(run.etape, 'in_progress')]}];
 }
 const vue = run => ({id: run.id, name: run.workflow, status: run.status, conclusion: run.conclusion || null, html_url: m.html(run.id),
  created_at: run.created_at, event: 'workflow_dispatch', path: `.github/workflows/${run.workflow}`});

 // ---------- api.github.com ----------
 m.github = async route => {
  const req = route.request(), url = new URL(req.url());
  const cors = {'access-control-allow-origin': new URL(SITE).origin, 'access-control-allow-headers': 'authorization, accept, x-github-api-version, content-type',
   'access-control-allow-methods': 'GET, POST', 'content-type': 'application/json'};
  if (req.method() === 'OPTIONS') return route.fulfill({status: 204, headers: cors});
  const entetes = await req.allHeaders();
  m.appels.push({hote: 'api', method: req.method(), url: req.url(), headers: entetes, body: req.postData()});
  const json = (status, body) => route.fulfill({status, headers: cors, body: body === undefined ? '' : JSON.stringify(body)});
  const jeton = (entetes.authorization || '').replace(/^Bearer /, '');
  const droit = jeton ? m.jetons[jeton] || 'inconnu' : 'anonyme';
  if (droit === 'expire' || droit === 'inconnu') return json(401, {message: 'Bad credentials'});
  if (droit === 'sans-acces') return json(404, {message: 'Not Found'});
  if (m.panneApi > 0) { m.panneApi -= 1; return route.abort('failed'); }
  const d = /\/actions\/workflows\/([^/]+)\/dispatches$/.exec(url.pathname);
  if (req.method() === 'POST' && d) {
   if (droit === 'anonyme') return json(401, {message: 'Requires authentication'});
   if (droit === 'lecture') return json(403, {message: 'Resource not accessible by personal access token'});
   const regles = WORKFLOWS[d[1]];
   let corps; try { corps = JSON.parse(req.postData()); } catch (_) { return json(400, {message: 'Problems parsing JSON'}); }
   const inputs = corps.inputs || {};
   const refuse = !regles || corps.ref !== 'main' || Object.keys(inputs).some(k => !regles.inputs.includes(k)) || Object.keys(inputs).length > 25
    || Object.values(inputs).some(v => typeof v !== 'string') || JSON.stringify(inputs).length > 65535
    || (regles.required || []).some(k => !inputs[k]) || (regles.modes && inputs.mode !== undefined && !regles.modes.includes(inputs.mode))
    || (regles.rubriques && !regles.rubriques.includes(inputs.rubrique));
   if (refuse) return json(422, {message: 'Unexpected inputs provided'});
   const run = {id: m.prochain++, workflow: d[1], inputs, status: 'queued', patience: m.attente, created_at: new Date().toISOString(), duree: m.duree || 2};
   // Groupe de concurrence « pages » : un seul run en attente, le précédent en attente est annulé.
   if (d[1] === 'publier-paquet-snum.yml') {
    for (const r of m.runs) if (r.workflow === d[1] && r.status === 'pending') { r.status = 'completed'; r.conclusion = 'cancelled'; }
    if (m.runs.some(r => r.workflow === d[1] && actif(r))) run.status = 'pending';
   }
   m.runs.push(run);
   if (m.reponse204) return route.fulfill({status: 204, headers: cors, body: ''});
   return json(200, {workflow_run_id: run.id, run_url: `${API}/actions/runs/${run.id}`, html_url: m.html(run.id)});
  }
  const liste = /\/actions\/workflows\/([^/]+)\/runs$/.exec(url.pathname);
  if (liste) {
   if (droit === 'anonyme' && m.anonymeRefuse) return json(403, {message: 'API rate limit exceeded'});
   const runs = m.runs.filter(r => r.workflow === liste[1]).sort((a, b) => b.id - a.id).slice(0, Number(url.searchParams.get('per_page') || 30));
   return json(200, {total_count: runs.length, workflow_runs: runs.map(vue)});
  }
  const r = /\/actions\/runs\/(\d+)(\/jobs)?$/.exec(url.pathname);
  const run = r && m.runs.find(x => String(x.id) === r[1]);
  if (!run) return json(404, {message: 'Not Found'});
  if (r[2]) { const j = jobs(run); return json(200, {total_count: j.length, jobs: j}); }
  avancer(run);
  return json(200, vue(run));
 };

 // ---------- raw.githubusercontent.com ----------
 m.rawRoute = async route => {
  const url = new URL(route.request().url());
  m.appels.push({hote: 'raw', url: url.href, headers: await route.request().allHeaders()});
  const corps = m.raw[url.href.split('?')[0].replace(RAW, '')];
  const entetes = {'access-control-allow-origin': '*', 'cache-control': 'max-age=300'};
  if (corps === undefined) return route.fulfill({status: 404, headers: entetes, contentType: 'text/plain', body: '404: Not Found'});
  return route.fulfill({status: 200, headers: entetes, contentType: 'text/plain; charset=utf-8', body: corps});
 };

 // ---------- Navigateur ----------
 m.lancer = async () => { m.navigateur = await chromium.launch(); return m; };
 m.fermer = async () => { if (m.navigateur) await m.navigateur.close(); };
 // Nouvelle personne : contexte isolé, routes du monde, temps accéléré (les attentes de plus d'une seconde sont divisées).
 m.personne = async (options = {}) => {
  const contexte = await m.navigateur.newContext({acceptDownloads: true, viewport: options.viewport || {width: 1280, height: 900}, locale: 'fr-FR',
   timezoneId: 'Europe/Paris', permissions: ['clipboard-read', 'clipboard-write'], ...(options.contexte || {})});
  const acc = options.accelere === undefined ? 25 : options.accelere;
  if (acc > 1) await contexte.addInitScript(k => { const st = window.setTimeout; window.setTimeout = (f, ms, ...a) => st(f, ms >= 1000 ? ms / k : ms, ...a); }, acc);
  await contexte.route(u => true, route => { m.fuites.push(route.request().url()); return route.abort('blockedbyclient'); });
  await contexte.route(u => u.href.startsWith(SITE), m.site);
  await contexte.route(u => u.hostname === 'api.github.com', m.github);
  await contexte.route(u => u.hostname === 'raw.githubusercontent.com', m.rawRoute);
  const p = {contexte, console: [], erreurs: [], reseau: [], urls: []};
  p.onglet = async (chemin = '') => {
   const page = await contexte.newPage();
   page.on('console', c => {
    p.console.push(c.text());
    if (c.type() === 'error' && c.text().startsWith('Failed to load resource')) p.reseau.push(`${(c.text().match(/status of (\d+)/) || [])[1] || c.text()} ${c.location().url}`);
    else if (c.type() === 'error' || c.type() === 'warning') p.erreurs.push(`${c.type()}: ${c.text()}`);
   });
   page.on('pageerror', e => p.erreurs.push('pageerror: ' + e.message));
   page.on('request', r => p.urls.push(r.url()));
   await page.goto(SITE + chemin, {waitUntil: 'networkidle'});
   return page;
  };
  return p;
 };
 return m;
}

// ---------- Vérifications ----------
function verificateur(titre) {
 const resultats = [];
 const check = (nom, ok, detail = '') => { resultats.push(!!ok); console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}${detail ? ' : ' + String(detail).replace(/\s+/g, ' ').slice(0, 420) : ''}`); return !!ok; };
 const bilan = () => { const n = resultats.filter(Boolean).length; console.log(`${titre} : ${n}/${resultats.length} vérifications`); return n === resultats.length; };
 return {check, bilan};
}
const outils = page => ({
 texte: sel => page.textContent(sel),
 cache: sel => page.$eval(sel, e => e.hidden),
 visible: sel => page.isVisible(sel),
 actif: () => page.evaluate(() => { const a = document.activeElement; return a ? (a.id || a.tagName) : ''; }),
 attendreTexte: (sel, motif, delai = 30000) => page.waitForFunction(([s, r]) => new RegExp(r).test(document.querySelector(s).textContent), [sel, motif], {timeout: delai}),
 attendre: (fn, arg, delai = 30000) => page.waitForFunction(fn, arg, {timeout: delai}),
});

module.exports = {creerMonde, verificateur, outils, SITE, API, RAW, DATA};
