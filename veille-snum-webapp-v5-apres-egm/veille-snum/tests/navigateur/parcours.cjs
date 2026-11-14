// Parcours Chromium de bout en bout de Veille SNUM : deux temps avec des titres réels, cas d'échec,
// mode complet, archives, repêchage, clavier seul, 375 px, zoom 200 %. Le site, api.github.com et
// raw.githubusercontent.com sont simulés ; chaque run exécute le vrai code serveur (produire.py).
const path = require('path');
const fs = require('fs');
const {spawnSync} = require('child_process');
const {creerMonde, verificateur, outils, SITE} = require('./monde.cjs');
const os = require('os');
// Usage : node parcours.cjs [dossier de travail] [dossier des captures]. Par défaut, un dossier temporaire.
const proto = path.join(__dirname, '../..');
const base = fs.mkdtempSync(path.join(os.tmpdir(), 'veille-snum-navigateur-'));
const travail = process.argv[2] || path.join(base, 'travail'), sorties = process.argv[3] || path.join(base, 'captures');
const reel = path.join(__dirname, 'donnees/rapport-titres-reel.json'), reel60 = path.join(__dirname, 'donnees/rapport-titres-60.json');
const JETON = 'github_pat_FAUXJETONPOURLETEST_0123456789abcdef';
const {check, bilan} = verificateur('Parcours');
const SYN = {edition: '2026-11-11', start: '2026-11-01', end: '2026-11-10'};
const REEL = {edition: '2026-11-14', start: '2026-11-09', end: '2026-11-13'};
const tous = [];

async function monde(nom, etat, options = {}) {
 const m = creerMonde({proto, travail: path.join(travail, nom), ...options});
 m.jetons[JETON] = 'ok';
 if (etat) {
  const base = path.join(travail, nom, 'depart'), dates = {edition: '11/11/2026', debut: '01/11/2026', fin: '10/11/2026'};
  fs.mkdirSync(base, {recursive: true});
  const jouer = (mode, inputs, extra = {}) => {
   const sortie = path.join(base, mode);
   fs.writeFileSync(path.join(base, `${mode}.json`), JSON.stringify({mode, jeu: 'synthetique', inputs, sortie, run_id: mode === 'resumes' ? 101 : 100, ...extra}));
   const r = spawnSync('python3', [path.join(__dirname, 'produire.py'), proto, path.join(base, `${mode}.json`)], {encoding: 'utf8'});
   if (r.status !== 0) throw new Error(`état de départ ${mode} : ${r.stdout}${r.stderr}`);
   return sortie;
  };
  if (etat === 'resumes-vide') {
   // Paquet de deux articles et onze candidats écartés : premier temps, puis second temps sur deux titres.
   const titres = jouer('titres', dates);
   const urls = JSON.parse(fs.readFileSync(path.join(titres, 'rapport-collecte.json'), 'utf8')).candidates.slice(0, 2).map(c => ({url: c.url, rubrique: ''}));
   m.enLigne = jouer('resumes', {...dates, selection: JSON.stringify(urls)}, {en_ligne: titres});
  } else m.enLigne = jouer(etat, dates);
 }
 await m.lancer();
 tous.push(m);
 return m;
}
const saisir = async (page, d = SYN) => { await page.fill('#gh-token', JETON); for (const [id, v] of Object.entries(d)) await page.fill(`#${id}`, v); };
// Fin d'un lancement : le bouton utilisé, marqué indisponible dès le clic, redevient disponible.
const fin = o => o.attendre(() => !document.querySelector('#collect[aria-disabled=true], #resumes[aria-disabled=true]'), null, 120000);
const lireEnLigne = (m, nom) => JSON.parse(fs.readFileSync(path.join(m.enLigne, nom), 'utf8'));
const capture = (page, nom, plein = true) => page.screenshot({path: path.join(sorties, nom), fullPage: plein});
// Avance au clavier (Tab) jusqu'à l'élément voulu : prouve qu'il est atteignable sans souris.
async function tabJusqua(page, id, max = 600) {
 for (let i = 0; i < max; i++) {
  await page.keyboard.press('Tab');
  if (await page.evaluate(x => document.activeElement && document.activeElement.id === x, id)) return i + 1;
 }
 return 0;
}
// Indicateur de focus : contour de 2 px sur l'élément, ou sur son pseudo-élément (lien étendu de l'en-tête).
// Le bouton calendrier interne d'un champ date est dessiné par le navigateur : il n'est pas mesurable ici.
const focusVisible = page => page.evaluate(() => { const a = document.activeElement, ok = s => s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2;
 const etiquette = a.id ? document.querySelector(`label[for="${a.id}"]`) : null;   // case à cocher : contour porté par l'étiquette
 return ok(getComputedStyle(a)) || ok(getComputedStyle(a, '::before')) || (etiquette && ok(getComputedStyle(etiquette, '::before'))) || (a.type === 'date' && !a.matches(':focus-visible')); });
// Rapport de contraste du texte de chaque élément visible désigné, fond effectif recherché chez les ancêtres.
const contrastes = (page, selecteur) => page.evaluate(sel => {
 const rgb = c => (c.match(/[\d.]+/g) || []).map(Number);
 const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
 const fond = e => { for (let n = e; n; n = n.parentElement) { const c = rgb(getComputedStyle(n).backgroundColor); if (c.length === 3 || c[3] > 0.99) return c; } return [255, 255, 255]; };
 const opacite = e => { let o = 1; for (let n = e; n; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity); return o; };
 return [...document.querySelectorAll(sel)].filter(e => e.getClientRects().length && e.textContent.trim()).map(e => {
  const bg = fond(e), o = opacite(e), fg = rgb(getComputedStyle(e).color).slice(0, 3).map((v, i) => v * o + bg[i] * (1 - o));
  const a = lum(fg), b = lum(bg);
  return {texte: e.textContent.trim().slice(0, 40), ratio: Math.round(((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)) * 100) / 100};
 });
}, selecteur);
const sansDefilement = page => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);

(async () => {
 fs.mkdirSync(sorties, {recursive: true});

 // ===== A. Deux temps, titres réels, clavier seul pour les gestes clés =====
 {
  const m = await monde('a', 'collecte', {jeu: 'reel', rapportReel: reel});
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  check('A1 départ : paquet précédent affiché, accordéon « Candidats écartés »', (await page.$$('#article-list input[type=checkbox]')).length === 13 && /^Candidats écartés \(\d+\)$/.test(await o.texte('#candidates-button')));
  const doc = await page.getAttribute('#gh-token-doc', 'href');
  check('A2 lien vers la marche à suivre du jeton, nouvelle fenêtre', /docs\/jeton-github\.md$/.test(doc) && await page.getAttribute('#gh-token-doc', 'target') === '_blank', doc);
  // Clavier seul : jeton, dates, lancement.
  const pas = await tabJusqua(page, 'gh-token');
  await page.keyboard.type(JETON);
  check('A3 clavier : champ du jeton atteint par Tab, focus visible', pas > 0 && await focusVisible(page), `${pas} tabulations`);
  // La saisie dans le champ date natif dépend du format régional du navigateur : la valeur est posée une fois le champ atteint par Tab.
  for (const [id, v] of Object.entries(REEL)) { await tabJusqua(page, id); await page.fill(`#${id}`, v); }
  check('A4 clavier : dates saisies', await page.inputValue('#edition') === REEL.edition && await page.inputValue('#start') === REEL.start && await page.inputValue('#end') === REEL.end,
   `${await page.inputValue('#edition')} ${await page.inputValue('#start')} ${await page.inputValue('#end')}`);
  await tabJusqua(page, 'collect');
  check('A5 clavier : bouton de lancement atteint, focus visible', await o.actif() === 'collect' && await focusVisible(page));
  await page.keyboard.press('Enter');
  await o.attendre(() => !document.getElementById('reset-notice').hidden);
  check('A6 page vidée dès l’acceptation, renvoi vers les archives, focus resté sur le bouton', await o.cache('#selection-content') && await page.getAttribute('#reset-notice a', 'href') === 'archives.html'
   && await o.actif() === 'collect' && await page.getAttribute('#collect', 'aria-disabled') === 'true', await o.texte('#reset-status'));
  await capture(page, 'a1-page-videe.png');
  await fin(o);
  const corps = JSON.parse(m.appels.find(c => c.method === 'POST').body);
  check('A7 lancement en mode titres, dates au format attendu', JSON.stringify(corps) === JSON.stringify({ref: 'main', inputs: {edition: '14/11/2026', debut: '09/11/2026', fin: '13/11/2026', mode: 'titres'}}), JSON.stringify(corps));
  const etat = lireEnLigne(m, 'etat-collecte.json');
  const fichiers = fs.readdirSync(m.enLigne).sort().join(',');
  check('A8 site après le premier temps : état et rapport seulement', fichiers === 'etat-collecte.json,rapport-collecte.json' && etat.phase === 'titres' && etat.candidats === 48, fichiers);
  const n = (await page.$$('#titres-list input[type=checkbox]')).length;
  check('A9 48 titres réels affichés, aucun gardé, focus resté sur le bouton', n === 48 && (await o.texte('#titres-count')) === '0 titre gardé sur 48.' && await o.actif() === 'collect'
   && /titres trouvés/.test(await o.texte('#collect-status')), await o.texte('#collect-status'));
  const rapport = lireEnLigne(m, 'rapport-collecte.json');
  const premier = await page.$eval('#titres-list li h4', h => h.textContent);
  check('A10 titres du vrai rapport publié, par source, dates en toutes lettres', rapport.candidates.some(c => c.title === premier) && /novembre 2026/.test(await page.$eval('#titres-list li', l => l.textContent))
   && (await page.$$('#titres-list h3')).length === new Set(rapport.candidates.map(c => c.source)).size, premier);
  check('A11 rapport affiché en phase titres, pas de paquet', (await o.texte('#report-intro')).includes('Titres trouvés, sans résumé') && !(await o.visible('#download')) && await o.visible('#report-stats'));
  check('A12 bouton de rédaction bloqué tant que rien n’est gardé, raison affichée', await page.$eval('#resumes', b => b.disabled) && /Gardez au moins un titre/.test(await o.texte('#resumes-hint')));
  // « Tout garder » pour une source entière, au clavier, puis « Tout retirer ».
  const groupe = await page.$eval('#titres-list section', s => ({n: s.querySelectorAll('input[type=checkbox]').length, bouton: s.querySelector('button').id}));
  await tabJusqua(page, groupe.bouton); await page.keyboard.press('Enter');
  const tous = await page.$eval('#titres-list section', s => [...s.querySelectorAll('input[type=checkbox]')].filter(i => i.checked).length);
  check('A12b « Tout garder » d’une source au clavier : tous cochés, compteur annoncé, focus conservé', tous === groupe.n && (await o.texte(`#${groupe.bouton}`)).startsWith('Tout retirer') && await o.actif() === groupe.bouton
   && new RegExp(`Tous les titres gardés : .*${groupe.n} titres? gardés? sur 48`).test(await o.texte('#titres-count')), await o.texte('#titres-count'));
  await page.keyboard.press('Enter');
  check('A12c « Tout retirer » : plus aucun titre gardé, bouton de rédaction de nouveau bloqué', (await o.texte('#titres-count')).endsWith('0 titre gardé sur 48.') && await page.$eval('#resumes', b => b.disabled) && (await o.texte(`#${groupe.bouton}`)).startsWith('Tout garder'));
  // Clavier seul : cinq titres gardés, une thématique imposée.
  const cles = await page.$$eval('#titres-list input[type=checkbox]', l => l.slice(0, 5).map(i => i.id));
  for (const id of cles) { await tabJusqua(page, id); await page.keyboard.press('Space'); }
  check('A13 clavier : cinq titres gardés, compteur annoncé, focus conservé', (await o.texte('#titres-count')).endsWith('5 titres gardés sur 48.') && await o.actif() === cles[4] && await focusVisible(page), await o.texte('#titres-count'));
  const liste = cles[1].replace('garder', 'thematique');
  await tabJusqua(page, liste); await page.selectOption(`#${liste}`, 'ia');
  const imposee = await page.inputValue(`#${liste}`);
  check('A14 clavier : thématique imposée, focus conservé', imposee === 'ia' && await o.actif() === liste, imposee);
  const garde = await page.$$eval('#titres-list li', (l, ids) => l.filter(li => ids.includes((li.querySelector('input') || {}).id)).map(li => li.querySelector('a').href), cles);
  // Albert : le 3e jugé hors thématique, le 4e en panne ; la page du 5e est protégée contre les robots.
  m.albert = {hors: [garde[2]], pannes: [garde[3]], code: 500};
  m.illisibles = [garde[4]];
  await capture(page, 'a2-titres-gardes.png');
  await tabJusqua(page, 'resumes');
  await page.keyboard.press('Enter');
  await o.attendreTexte('#titres-status', 'Étape en cours');
  check('A15 rédaction suivie : bouton indisponible sans perdre le focus, cases verrouillées, durée annoncée', await page.getAttribute('#resumes', 'aria-disabled') === 'true' && await o.actif() === 'resumes'
   && await page.$eval(`#${cles[0]}`, i => i.disabled) && /5 articles demandés\. Comptez une à deux minutes/.test(await o.texte('#titres-elapsed')), await o.texte('#titres-elapsed'));
  await fin(o);
  const envoi = JSON.parse(m.appels.filter(c => c.method === 'POST').pop().body).inputs;
  const attendu = garde.map((url, i) => ({url, rubrique: i === 1 ? 'ia' : ''}));
  check('A16 sélection envoyée exacte, dates de l’état', envoi.mode === 'resumes' && envoi.selection === JSON.stringify(attendu) && envoi.edition === '14/11/2026' && envoi.debut === '09/11/2026', envoi.selection.slice(0, 160));
  const paquet = lireEnLigne(m, 'paquet-v519.json'), ecartes = lireEnLigne(m, 'candidats-ecartes.json');
  const motifs = Object.fromEntries(ecartes.candidates.map(c => [c.url, c.reason]));
  check('A17 vrai paquet publié : 2 articles, rubrique imposée respectée', paquet.articles.length === 2 && paquet.articles.find(a => a.url === garde[1]).rubric === 'ia', paquet.articles.map(a => a.rubric).join());
  check('A18 motifs publiés : hors thématique, échec Albert, page non relue, non gardés', motifs[garde[2]] === 'HORS_THEMATIQUE' && motifs[garde[3]] === 'ECHEC_ALBERT' && motifs[garde[4]] === 'PAGE_NON_RELUE'
   && ecartes.candidates.filter(c => c.reason === 'NON_SELECTIONNE').length === 43, JSON.stringify([motifs[garde[2]], motifs[garde[3]], motifs[garde[4]]]));
  check('A19 aucun extrait d’article ni jeton dans les fichiers publiés', !fs.readdirSync(m.enLigne).some(f => /"content"|JETON-ALBERT|github_pat/.test(fs.readFileSync(path.join(m.enLigne, f), 'utf8'))));
  check('A20 page : paquet affiché, focus sur le résumé de l’édition, message de fin dans la zone de collecte', (await page.$$('#article-list input[type=checkbox]')).length === 2 && await o.actif() === 'summary-heading'
   && /^Résumés rédigés/.test(await o.texte('#collect-status')) && await o.cache('#titres-section'), await o.texte('#collect-status'));
  check('A21 alerte « Analyse partielle » visible dans les alertes à relire', /Analyse partielle/.test(await o.texte('#watch-list')), (await o.texte('#watch-list')).slice(0, 200));
  await page.click('#candidates-button');
  const textes = await page.$$eval('#candidates-list > li', l => l.map(x => x.textContent));
  check('A22 écartés : 46 candidats, motifs en clair, tous repêchables', textes.length === 46 && textes.some(t => t.includes('non gardé au premier temps')) && textes.some(t => t.includes('jugé hors thématique par Albert'))
   && textes.some(t => t.includes('échec du résumé Albert')) && textes.some(t => t.includes('page non relue au second temps')) && (await page.$$('#candidates-list button')).length === 46);
  await capture(page, 'a3-paquet-apres-resumes.png');
  // Repêchage d'un titre non gardé, au clavier.
  m.albert = {}; m.illisibles = [];
  await page.focus('#repecher-0'); await page.selectOption('#repecher-0', 'commande');
  await page.keyboard.press('Tab'); await page.keyboard.press('Enter');
  await o.attendreTexte('#repechage-status', 'Article repêché et gardé|interrompu', 60000);
  check('A23 repêchage : article ajouté et gardé, focus sur sa case', (await page.$$('#article-list input[type=checkbox]')).length === 3 && /^garder-r1$/.test(await o.actif()) && (await page.$$('#candidates-list > li')).length === 45, await o.texte('#repechage-status'));
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#download')]);
  await dl.saveAs(path.join(sorties, 'a-export.json'));
  const exporte = JSON.parse(fs.readFileSync(path.join(sorties, 'a-export.json'), 'utf8'));
  check('A24 export V519 : 3 articles renumérotés, édition du 14 novembre', exporte.schema_version === 'SNUM_PAQUET_RENDU_V519' && exporte.articles.length === 3 && exporte.articles.every((a, i) => a.id === `U0${i + 1}`)
   && exporte.edition_date === '2026-11-14' && dl.suggestedFilename() === 'paquet-v519-2026-11-14.json');
  await page.click('#copy');
  const copie = JSON.parse(await page.evaluate(() => navigator.clipboard.readText()));
  check('A25 copie du JSON identique au téléchargement', JSON.stringify(copie) === JSON.stringify(exporte) && /copié/.test(await o.texte('#selection-status')));
  // Archives : la collecte résumée y figure, et se rouvre.
  const archives = await p.onglet('archives.html');
  const cartes = await archives.$$eval('#archives-list h2', l => l.map(h => h.textContent));
  check('A26 archives : la collecte résumée est listée', cartes.length === 1 && cartes[0] === 'Édition du 14 novembre 2026' && /1 collecte archivée/.test(await archives.textContent('#archives-status')), cartes.join());
  await capture(archives, 'a4-archives.png');
  await archives.click('#archives-list a.fr-btn');
  await archives.waitForFunction(() => document.querySelectorAll('#article-list input').length > 0);
  check('A27 mode archive : bandeau, lancement retiré, repêchage toujours proposé', /Collecte archivée du 14 novembre 2026/.test(await archives.textContent('#archive-title')) && await archives.$eval('#collect-section', e => e.hidden)
   && (await archives.$$('#article-list input[type=checkbox]')).length === 2 && (await archives.$$('#candidates-list button')).length === 46);
  await capture(archives, 'a5-collecte-archivee.png');
  // Jeton et réseau.
  const dom = await page.evaluate(() => document.documentElement.outerHTML + document.body.innerText);
  check('A28 jeton absent du DOM, des adresses, de la console, du stockage et des fichiers téléchargés', !dom.includes(JETON) && !p.urls.some(u => u.includes(JETON)) && !p.console.some(t => t.includes(JETON))
   && await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0) && !(await p.contexte.cookies()).length && !JSON.stringify(exporte).includes(JETON));
  check('A29 jeton envoyé seulement à api.github.com, jamais à raw ni au site', m.appels.filter(c => c.hote === 'api' && c.method).every(c => !c.headers.authorization || c.headers.authorization === `Bearer ${JETON}`)
   && m.appels.filter(c => c.hote === 'raw').every(c => !c.headers.authorization) && m.appels.some(c => c.hote === 'raw'));
  check('A30 aucune requête hors du site, de api.github.com et de raw.githubusercontent.com', m.fuites.length === 0, m.fuites.join());
  check('A31 aucune erreur ni avertissement dans la console', p.erreurs.length === 0, p.erreurs.join(' | '));
 }

 // ===== B. Soixante titres gardés =====
 {
  const m = await monde('b', 'collecte', {jeu: 'reel', rapportReel: reel60});
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await saisir(page, REEL);
  await page.click('#collect');
  await fin(o);
  await page.$$eval('#titres-list input[type=checkbox]', l => l.forEach(i => i.click()));
  check('B1 soixante titres gardés : bouton actif, limite d’Albert annoncée avant l’envoi', (await o.texte('#resumes')) === 'Rédiger les résumés des 60 articles gardés' && !(await page.$eval('#resumes', b => b.disabled))
   && /Albert s’arrête après six minutes/.test(await o.texte('#resumes-hint')), await o.texte('#resumes-hint'));
  await page.click('#resumes');
  await fin(o);
  const envoi = m.appels.filter(c => c.method === 'POST').pop().body;
  const paquet = lireEnLigne(m, 'paquet-v519.json');
  check('B2 sélection de 60 titres acceptée, loin du plafond GitHub de 65 535 caractères', JSON.parse(JSON.parse(envoi).inputs.selection).length === 60 && envoi.length < 20000, `${envoi.length} caractères`);
  check('B3 paquet de 60 articles publié et affiché', paquet.articles.length === 60 && (await page.$$('#article-list input[type=checkbox]')).length === 60 && /Candidats écartés \(0\)/.test(await o.texte('#candidates-button')));
  await capture(page, 'b-soixante-articles.png');
 }

 // ===== C. Jeton absent, mal formé, expiré, insuffisant, sans accès ; GitHub lent ; réseau coupé =====
 {
  const m = await monde('c', 'titres');
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  check('C1 sans jeton : titres lisibles, rédaction bloquée avec sa raison', (await page.$$('#titres-list input[type=checkbox]')).length === 13 && await page.$eval('#resumes', b => b.disabled)
   && /Un jeton GitHub est nécessaire/.test(await o.texte('#collect-hint')));
  for (const [id, v] of Object.entries(SYN)) await page.fill(`#${id}`, v);
  await page.click('#collect');
  check('C2 lancement sans jeton : champ signalé, focus dessus, rien envoyé', /Saisissez un jeton GitHub/.test(await o.texte('#gh-token-messages')) && await o.actif() === 'gh-token' && await page.getAttribute('#gh-token', 'aria-invalid') === 'true'
   && !m.appels.some(c => c.method === 'POST'), await o.texte('#collect-error'));
  await page.fill('#gh-token', 'pas un jeton !');
  await page.click('#collect');
  check('C3 jeton mal formé : refusé avant tout envoi', /ne ressemble pas à un jeton GitHub/.test(await o.texte('#gh-token-messages')) && !m.appels.some(c => c.hote === 'api' && c.headers && c.headers.authorization));
  const cas = {expire: [/erreur 401/, /expiré ou révoqué/], lecture: [/erreur 403/, /Actions : Read and write/], 'sans-acces': [/erreur 404/, /ne donne pas accès au dépôt/]};
  for (const [droit, [code, conseil]] of Object.entries(cas)) {
   m.jetons[JETON] = droit;
   await page.fill('#gh-token', JETON);
   await page.click('#collect');
   await o.attendre(() => !document.getElementById('collect-error').hidden);
   const erreur = await o.texte('#collect-error');
   check(`C4 jeton ${droit} : message clair, lien vers la marche à suivre cité, titres toujours affichés`, code.test(erreur) && conseil.test(erreur) && /Créer ou renouveler un jeton GitHub/.test(erreur)
    && (await o.texte('#collect-status')) === 'Collecte non lancée.' && (await page.$$('#titres-list input[type=checkbox]')).length === 13 && await o.actif() === 'collect', erreur);
  }
  await capture(page, 'c1-jeton-refuse.png');
  m.jetons[JETON] = 'ok';
  // GitHub lent : longue file d'attente, la page le dit et compte le temps.
  m.attente = 6;
  await page.click('#collect');
  await o.attendreTexte('#collect-status', 'file d’attente');
  await page.waitForTimeout(900);
  check('C5 GitHub lent : file d’attente annoncée, temps écoulé et durée attendue affichés, lien de suivi', /En file d’attente sur GitHub Actions/.test(await o.texte('#collect-status'))
   && /Temps écoulé : \d+ min \d\d s\. La recherche des titres dure trois à quatre minutes\./.test(await o.texte('#collect-elapsed')) && /Suivre l’exécution sur GitHub/.test(await o.texte('#collect-run')), await o.texte('#collect-elapsed'));
  // Réseau coupé pendant le suivi.
  m.panneApi = 50;
  await o.attendre(() => !document.getElementById('collect-error').hidden, null, 60000);
  check('C6 réseau coupé pendant le suivi : la collecte continue, recharger sans relancer', /GitHub est injoignable/.test(await o.texte('#collect-error')) && /la collecte continue peut-être sur GitHub/.test(await o.texte('#collect-error'))
   && (await o.texte('#collect-status')) === 'Collecte : suivi interrompu.', await o.texte('#collect-error'));
  m.panneApi = 0;
 }

 // ===== D. Albert refuse tout ; rien n'est perdu ; ancienne réponse 204 de l'API =====
 {
  const m = await monde('d', 'titres');
  m.albert = {panne: 'tout', code: 503};
  m.reponse204 = true;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await page.fill('#gh-token', JETON);
  for (const i of [1, 2, 3]) await page.click(`label[for=titre-garder-${i}]`);
  await page.selectOption('#titre-thematique-2', 'bercy');
  await page.focus('#resumes'); await page.keyboard.press('Enter');
  await fin(o);
  const erreur = await o.texte('#titres-error');
  check('D1 Albert indisponible : étape en échec nommée, titres gardés toujours cochés, relance possible', /échec à l’étape « Résumés des titres gardés »/.test(erreur) && /Vos titres gardés restent cochés/.test(erreur)
   && (await page.$$eval('#titres-list input[type=checkbox]', l => l.filter(i => i.checked).length)) === 3 && await page.inputValue('#titre-thematique-2') === 'bercy' && await o.actif() === 'resumes'
   && !(await page.$eval('#titre-garder-1', i => i.disabled)), erreur);
  check('D2 rien publié : le site reste en phase titres', lireEnLigne(m, 'etat-collecte.json').phase === 'titres' && !fs.existsSync(path.join(m.enLigne, 'paquet-v519.json')));
  check('D3 réponse 204 sans numéro : exécution retrouvée dans la liste', m.runs.length === 1 && /actions\/runs\/9000/.test(await page.getAttribute('#titres-error a', 'href')));
  await capture(page, 'd-albert-indisponible.png');
  m.albert = {};
  await page.keyboard.press('Enter');
  await fin(o);
  check('D4 relance après retour d’Albert : paquet de 3 articles', (await page.$$('#article-list input[type=checkbox]')).length === 3 && lireEnLigne(m, 'paquet-v519.json').articles.find(a => a.rubric === 'bercy'));
 }

 // ===== E. Cache de GitHub Pages : ancienne version servie durablement, puis état périmé qui trompe la vérification =====
 {
  const m = await monde('e', 'collecte');
  m.delaiCdn = 500;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await saisir(page);
  await page.click('#collect');
  await fin(o);
  const erreur = await o.texte('#collect-error');
  check('E1 ancienne version servie plus de deux minutes : la page le dit, n’affiche pas l’ancien paquet, interdit de relancer', /sert encore l’ancienne version/.test(erreur) && /Ne relancez pas/.test(erreur)
   && (await page.$$('#article-list input[type=checkbox]')).length === 0 && (await page.$$('#titres-list input[type=checkbox]')).length === 0 && !(await o.cache('#reset-notice')), erreur);
  await capture(page, 'e1-ancienne-version.png');
  m.perime = null;
  await page.reload({waitUntil: 'networkidle'});
  check('E2 rechargement une fois le cache expiré : titres affichés', (await page.$$('#titres-list input[type=checkbox]')).length === 13);
  // Deux personnes ; la seconde lit un état périmé : la vérification avant envoi passe, le serveur refuse.
  m.delaiCdn = 0;
  const b = await m.personne(), pb = await b.onglet(), ob = outils(pb);
  await page.fill('#gh-token', JETON); await page.click('label[for=titre-garder-1]');
  await pb.fill('#gh-token', JETON); await pb.click('label[for=titre-garder-2]');
  await page.click('#resumes');
  await fin(o);
  const titresDir = path.join(m.travail, 'depart', 'titres-perime');
  fs.mkdirSync(titresDir, {recursive: true});
  for (const f of ['etat-collecte.json', 'rapport-collecte.json']) fs.copyFileSync(path.join(m.travail, `site-${m.runs[0].id}`, f), path.join(titresDir, f));
  m.perime = {dossier: titresDir, lectures: 1};
  await pb.click('#resumes');
  await fin(ob);
  const messageB = await ob.texte('#collect-error');
  check('E3 état périmé chez la seconde personne : le serveur refuse, aucun appel Albert, le paquet de la première reste', m.runs[2].conclusion === 'failure' && /déjà été résumés/.test(m.runs[2].journal)
   && lireEnLigne(m, 'paquet-v519.json').articles.length === 1 && lireEnLigne(m, 'etat-collecte.json').run_id === m.runs[1].id, m.runs[2].journal);
  check('E4 la seconde personne voit le paquet publié et l’explication', (await pb.$$('#article-list input[type=checkbox]')).length === 1 && /Un paquet a déjà été publié pendant votre tri/.test(messageB)
   && (await ob.texte('#collect-status')) === 'Rédaction des résumés en échec.', messageB);
 }

 // ===== F. Mode complet, puis repêchage depuis un onglet resté sur le paquet pendant la phase titres =====
 {
  const m = await monde('f', 'collecte');
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await saisir(page);
  await page.click('label[for=complete]');
  await page.click('#collect');
  await o.attendreTexte('#collect-status', 'Étape en cours');
  check('F1 collecte complète : durée annoncée d’après les collectes réelles', /de cinq à neuf minutes/.test(await o.texte('#collect-elapsed')) && /Collecte et paquet V519/.test(await o.texte('#collect-status')));
  await fin(o);
  const envoi = JSON.parse(m.appels.find(c => c.method === 'POST').body).inputs;
  check('F2 mode collecte : paquet, rapport et écartés rechargés, archive créée', envoi.mode === 'collecte' && lireEnLigne(m, 'etat-collecte.json').phase === 'collecte' && (await page.$$('#article-list input[type=checkbox]')).length === 13
   && /nouveau paquet/.test(await o.texte('#collect-status')) && Object.keys(m.raw).filter(k => k.startsWith('collectes/')).length === 4);
  // Un second onglet lance les titres ; le premier, resté sur le paquet, repêche encore.
  const autre = await p.onglet();
  await saisir(autre);
  await autre.click('#collect');
  await autre.waitForTimeout(600);
  await autre.click('#collect');     // collecte précédente terminée : pas d'avertissement attendu
  await fin(outils(autre));
  check('F3 second onglet : phase titres publiée', lireEnLigne(m, 'etat-collecte.json').phase === 'titres' && (await autre.$$('#titres-list input[type=checkbox]')).length === 13);
  // Aucun candidat écarté dans ce jeu : le repêchage est vérifié en mode archive, sur le paquet précédent.
  const archive = await p.onglet(`?collecte=${JSON.parse(m.raw['collectes/index.json']).collectes[0].id}`);
  check('F4 pendant la phase titres : la collecte archivée reste consultable et exportable', (await archive.$$('#article-list input[type=checkbox]')).length === 13 && !(await archive.$eval('#download', b => b.disabled))
   && /la collecte en cours n’est pas modifiée/.test(await archive.textContent('#archive-text')));
 }

 // ===== G. Repêchage pendant la phase titres (onglet resté sur le paquet), rien de gardé, page protégée =====
 {
  const m = await monde('g', 'resumes-vide');
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  check('G1 départ : paquet de 2 articles, 11 écartés', (await page.$$('#article-list input[type=checkbox]')).length === 2 && /Candidats écartés \(11\)/.test(await o.texte('#candidates-button')));
  const autre = await p.onglet();
  await saisir(autre);
  await autre.click('#collect');
  await fin(outils(autre));
  check('G2 un autre onglet a lancé les titres : le site est en phase titres', lireEnLigne(m, 'etat-collecte.json').phase === 'titres');
  await page.fill('#gh-token', JETON);
  await page.click('#candidates-button');
  await page.selectOption('#repecher-0', 'rh');
  await page.click('#candidates-list button');
  await o.attendreTexte('#repechage-status', 'Article repêché et gardé|interrompu', 60000);
  check('G3 repêchage pendant la phase titres : article ajouté à la sélection de l’onglet', (await page.$$('#article-list input[type=checkbox]')).length === 3 && /gardé en Ressources humaines/.test(await o.texte('#repechage-status')), await o.texte('#repechage-status'));
  // Page protégée au repêchage : le motif publié est affiché.
  const url = await page.$eval('#candidates-list > li a', a => a.href);
  m.illisibles = [url];
  await page.selectOption('#repecher-0', 'ia');
  await page.click('#candidates-list button');
  await o.attendre(() => !document.getElementById('repechage-error').hidden, null, 60000);
  check('G4 page protégée au repêchage : motif lisible, candidat conservé', /Page illisible : HTTP 403/.test(await o.texte('#repechage-error')) && (await page.$$('#candidates-list > li')).length === 10, await o.texte('#repechage-error'));
  await capture(page, 'g-repechage-refuse.png');
 }

 // ===== H. Clavier, 375 px, zoom 200 %, contrastes, régions annoncées =====
 {
  const m = await monde('h', 'titres');
  for (const [nom, largeur] of [['375 px', 375], ['zoom 200 % (640 px)', 640], ['zoom 400 % (320 px)', 320]]) {
   const p = await m.personne({viewport: {width: largeur, height: 800}}), page = await p.onglet();
   check(`H1 phase titres, ${nom} : pas de défilement horizontal`, await sansDefilement(page), `scrollWidth ${await page.evaluate(() => document.documentElement.scrollWidth)}`);
   await page.fill('#gh-token', JETON);
   await page.click('label[for=titre-garder-1]');
   const boite = await page.$eval('#resumes', b => { const r = b.getBoundingClientRect(); return r.left >= 0 && r.right <= window.innerWidth + 1; });
   check(`H2 phase titres, ${nom} : bouton de rédaction entièrement visible en largeur`, boite);
   if (largeur !== 320) await capture(page, `h-titres-${largeur}.png`, false);
   await p.contexte.close();
  }
  const m2 = await monde('h2', 'resumes-vide');
  for (const [nom, largeur] of [['375 px', 375], ['zoom 200 % (640 px)', 640]]) {
   const p = await m2.personne({viewport: {width: largeur, height: 800}}), page = await p.onglet();
   await page.click('#candidates-button');
   check(`H3 paquet et écartés, ${nom} : pas de défilement horizontal`, await sansDefilement(page));
   await capture(page, `h-paquet-${largeur}.png`, false);
   const arch = await p.onglet('archives.html');
   check(`H4 archives, ${nom} : pas de défilement horizontal`, await sansDefilement(arch));
   await p.contexte.close();
  }
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  // Ordre de tabulation : lien d'évitement, puis tous les contrôles, sans piège.
  await page.keyboard.press('Tab');
  check('H5 premier Tab : lien d’évitement « Contenu »', await page.evaluate(() => document.activeElement.textContent) === 'Contenu');
  const parcourus = [], premiereCase = await page.$eval('#titres-list input[type=checkbox]', i => i.id);
  for (let i = 0; i < 64; i++) { await page.keyboard.press("Tab"); parcourus.push(await o.actif()); if (!(await focusVisible(page))) parcourus.push('SANS-FOCUS-VISIBLE'); }
  check('H6 clavier : jeton, dates, case, bouton, titres atteints dans l’ordre, focus toujours visible', ['gh-token', 'gh-token-forget', 'gh-token-doc', 'edition', 'start', 'end', 'complete', 'collect', premiereCase, premiereCase.replace('garder', 'thematique')]
   .every((id, i, l) => parcourus.includes(id) && (i === 0 || parcourus.indexOf(l[i - 1]) < parcourus.indexOf(id))) && !parcourus.includes('SANS-FOCUS-VISIBLE'), parcourus.slice(0, 40).join(' > '));
  const regions = await page.evaluate(() => ({statuts: [...document.querySelectorAll('[role=status]')].map(e => e.id), alertes: [...document.querySelectorAll('[role=alert]')].map(e => e.id)}));
  check('H7 régions annoncées : états et alertes', ['gh-token-status', 'collect-status', 'reset-status', 'titres-count', 'titres-status', 'report-status', 'selection-status', 'repechage-status', 'export-status'].every(id => regions.statuts.includes(id))
   && ['collect-error', 'load-error', 'titres-error', 'repechage-error'].every(id => regions.alertes.includes(id)), JSON.stringify(regions));
  const etiquettes = await page.$$eval('#titres-list input, #titres-list select', l => l.every(e => { const lab = document.querySelector(`label[for="${e.id}"]`); return lab && /« .+ »/.test(lab.textContent); }));
  check('H8 chaque case et chaque liste porte une étiquette qui nomme son titre', etiquettes);
  await page.fill('#gh-token', JETON); await page.click('label[for=titre-garder-1]');
  const c1 = await contrastes(page, '#titres-section p, #titres-section h3, #titres-section h4, #titres-section label, #titres-section a, #resumes, #collect-section p, #collect, .fr-hint-text, #gh-token-doc');
  const faibles = c1.filter(c => c.ratio < 4.5);
  check('H9 contrastes en phase titres : texte à 4,5 pour 1 au moins', c1.length > 60 && faibles.length === 0, `${c1.length} textes, minimum ${Math.min(...c1.map(c => c.ratio))} ${JSON.stringify(faibles.slice(0, 3))}`);
  const p2 = await m2.personne(), page2 = await p2.onglet();
  await page2.click('label[for=garder-1]'); await page2.click('#candidates-button');
  const c2 = await contrastes(page2, '#article-list p, #article-list h3, #article-list h4, #article-list label, #article-list a, #candidates-list p, #candidates-list a, #candidates-list button, #export-status, #watch-list li, #report-stats p');
  const faibles2 = c2.filter(c => c.ratio < 4.5);
  check('H10 contrastes du paquet, article écarté compris', c2.length > 40 && faibles2.length === 0, `${c2.length} textes, minimum ${Math.min(...c2.map(c => c.ratio))} ${JSON.stringify(faibles2.slice(0, 3))}`);
  fs.writeFileSync(path.join(sorties, 'h-dom-titres.html'), await page.content());
  fs.writeFileSync(path.join(sorties, 'h-dom-paquet.html'), await page2.content());
 }

 // ===== I. Archivage en échec et cache : la publication est quand même reconnue =====
 {
  const m = await monde('i', 'titres');
  m.echecApres.resumes = 'archivage'; m.delaiCdn = 3;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await page.fill('#gh-token', JETON); await page.click('label[for=titre-garder-1]');
  await page.click('#resumes');
  await fin(o);
  const erreur = await o.texte('#titres-error');
  check('I1 archivage en échec : rien n’est publié, étape nommée, titres gardés toujours cochés, relance possible', (await page.$$('#article-list input[type=checkbox]')).length === 0
   && /« Archiver la collecte »/.test(erreur) && /Vos titres gardés restent cochés/.test(erreur) && lireEnLigne(m, 'etat-collecte.json').phase === 'titres', erreur);
  // Paquet sans article : tout est jugé hors thématique ; la page le dit et propose quoi faire.
  m.echecApres = {}; m.delaiCdn = 0;
  const gardee = await page.$eval('#titres-list input:checked', i => i.closest('li').querySelector('a').href);
  m.albert = {hors: [gardee]};
  await page.click('#resumes');
  await fin(o);
  check('I3 paquet sans article : annoncé avec la marche à suivre, candidats repêchables', (await page.$$('#article-list input[type=checkbox]')).length === 0 && /ne contient aucun article : repêchez un candidat écarté/.test(await o.texte('#collect-status'))
   && (await page.$$('#candidates-list button')).length === 13, await o.texte('#collect-status'));
  const arch = await p.onglet('archives.html');
  check('I2 archives : aucune collecte, dit clairement', /Aucune collecte archivée/.test(await arch.textContent('#archives-status')));
  // Indicateur de focus natif du bouton calendrier d'un champ date : capture pour contrôle visuel.
  await page.focus('#edition'); await page.keyboard.press('Tab'); await page.keyboard.press('Tab'); await page.keyboard.press('Tab');
  await page.locator('#edition-group').screenshot({path: path.join(sorties, 'i-focus-calendrier.png')});
 }

 for (const m of tous) {
  check(`Z aucune requête réelle (monde ${path.basename(m.travail)})`, m.fuites.length === 0, m.fuites.slice(0, 3).join());
  await m.fermer();
 }
 console.log(`Captures : ${sorties}`);
 process.exit(bilan() ? 0 : 1);
})().catch(async e => { console.error(e); for (const m of tous) await m.fermer().catch(() => {}); process.exit(2); });
