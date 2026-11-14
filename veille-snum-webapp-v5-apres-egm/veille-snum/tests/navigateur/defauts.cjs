// Scénarios qui cassent avant correction : chacun décrit le comportement attendu pour une personne seule
// devant la page. Lancé avant les corrections (rouge), puis après (vert). Vrai code serveur, GitHub simulé.
const path = require('path');
const fs = require('fs');
const {creerMonde, verificateur, outils} = require('./monde.cjs');
const os = require('os');
// Usage : node defauts.cjs [dossier de travail] [dossier des captures]. Par défaut, un dossier temporaire.
const proto = path.join(__dirname, '../..');
const base = fs.mkdtempSync(path.join(os.tmpdir(), 'veille-snum-navigateur-'));
const travail = process.argv[2] || path.join(base, 'travail'), sorties = process.argv[3] || path.join(base, 'captures');
const JETON = 'github_pat_FAUXJETONPOURLETEST_0123456789abcdef';
const {check, bilan} = verificateur('Défauts');
const DATES = {edition: '2026-11-11', start: '2026-11-01', end: '2026-11-10'};

async function monde(nom, etat) {
 const m = creerMonde({proto, travail: path.join(travail, nom)});
 m.jetons[JETON] = 'ok';
 // États de départ produits par le vrai code : collecte complète, ou titres.
 const depart = {id: 100};
 const base = path.join(travail, nom, 'depart');
 const jouer = (mode, extra = {}) => {
  const sortie = path.join(base, mode);
  fs.mkdirSync(base, {recursive: true});
  fs.writeFileSync(path.join(base, `${mode}.json`), JSON.stringify({mode, jeu: 'synthetique', inputs: {edition: '11/11/2026', debut: '01/11/2026', fin: '10/11/2026'}, sortie, run_id: depart.id++, ...extra}));
  const r = require('child_process').spawnSync('python3', [path.join(__dirname, 'produire.py'), proto, path.join(base, `${mode}.json`)], {encoding: 'utf8'});
  if (r.status !== 0) throw new Error(`état de départ ${mode} : ${r.stdout}${r.stderr}`);
  return sortie;
 };
 m.enLigne = jouer(etat);
 await m.lancer();
 return m;
}
async function saisir(page) {
 await page.fill('#gh-token', JETON);
 for (const [id, v] of Object.entries(DATES)) await page.fill(`#${id}`, v);
}

(async () => {
 fs.mkdirSync(sorties, {recursive: true});

 // D1. Après une collecte réussie, GitHub Pages sert encore quelques instants l'ancienne version.
 {
  const m = await monde('d1', 'collecte');
  m.delaiCdn = 3;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await saisir(page);
  await page.click('#collect');
  await o.attendreTexte('#collect-status', 'la page affiche|pas encore visible|interrompu|échec', 90000).catch(() => {});
  const statut = await o.texte('#collect-status');
  const titres = (await page.$$('#titres-list input[type=checkbox]')).length, articles = (await page.$$('#article-list input[type=checkbox]')).length;
  check('D1 cache périmé : la page finit par afficher les titres de CE run, pas l’ancien paquet présenté comme nouveau', titres === 13 && articles === 0 && /titres trouvés/.test(statut),
   `${titres} titres, ${articles} articles de l’ancien paquet ; statut : ${statut}`);
  await page.screenshot({path: path.join(sorties, 'd1-cache-perime.png'), fullPage: true});
  await m.fermer();
 }

 // D2. Le jeton expire pendant le suivi : la collecte, elle, continue sur GitHub.
 {
  const m = await monde('d2', 'collecte');
  m.attente = 50;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await saisir(page);
  await page.click('#collect');
  await o.attendreTexte('#collect-status', 'file d’attente');
  m.jetons[JETON] = 'expire';
  await o.attendre(() => !document.getElementById('collect-error').hidden, null, 60000);
  const erreur = await o.texte('#collect-error'), statut = await o.texte('#collect-status');
  check('D2 jeton expiré pendant le suivi : la page dit que la collecte continue et quoi faire', /continue/.test(erreur + statut) && /rechargez/i.test(erreur + statut) && !/^Collecte interrompue/.test(statut),
   `statut : ${statut} | erreur : ${erreur}`);
  await page.screenshot({path: path.join(sorties, 'd2-suivi-perdu.png'), fullPage: true});
  await m.fermer();
 }

 // D3. Phase titres, état illisible (503 répétés) : ne pas conseiller de relancer une collecte.
 {
  const m = await monde('d3', 'titres');
  m.pannes['etat-collecte.json'] = 6;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  const erreur = (await o.visible('#load-error')) ? await o.texte('#load-error') : '';
  const titres = (await page.$$('#titres-list input[type=checkbox]')).length;
  check('D3 état illisible en phase titres : titres affichés, ou message qui invite à recharger sans relancer', titres === 13 || (/rechargez/i.test(erreur) && !/Lancez une collecte ou/.test(erreur)),
   `${titres} titres ; erreur : ${erreur}`);
  await page.screenshot({path: path.join(sorties, 'd3-etat-illisible.png'), fullPage: true});
  await m.fermer();
 }

 // D4. Deux personnes affichent les mêmes titres ; la seconde demande la rédaction après la première.
 {
  const m = await monde('d4', 'titres');
  const a = await m.personne(), pa = await a.onglet(), b = await m.personne(), pb = await b.onglet();
  for (const page of [pa, pb]) { await page.fill('#gh-token', JETON); await page.click('label[for=titre-garder-1]'); await page.click('label[for=titre-garder-2]'); }
  await pa.click('#resumes');
  await outils(pa).attendreTexte('#collect-status', '^Résumés rédigés', 60000);
  const articlesA = (await pa.$$('#article-list input[type=checkbox]')).length;
  await pb.click('label[for=titre-garder-3]');
  await pb.click('#resumes');
  await outils(pb).attendre(() => !document.getElementById('titres-error').hidden || document.querySelectorAll('#article-list input').length > 0 || !document.getElementById('collect-error').hidden, null, 60000);
  await pb.waitForTimeout(1500);
  const articlesB = (await pb.$$('#article-list input[type=checkbox]')).length;
  const messages = (await pb.textContent('#titres-error')) + ' ' + (await pb.textContent('#collect-error')) + ' ' + (await pb.textContent('#collect-status'));
  const paquetEnLigne = JSON.parse(fs.readFileSync(path.join(m.enLigne, 'paquet-v519.json'), 'utf8')).articles.length;
  check('D4 rédaction demandée deux fois : le paquet de la première reste en ligne', articlesA === 2 && paquetEnLigne === 2, `A voit ${articlesA} articles, en ligne ${paquetEnLigne}`);
  check('D4 la seconde personne voit le paquet publié et comprend pourquoi', articlesB === 2 && /déjà/.test(messages) && !/vous pouvez relancer/.test(messages), `B voit ${articlesB} articles ; messages : ${messages}`);
  await pb.screenshot({path: path.join(sorties, 'd4-seconde-demande.png'), fullPage: true});
  await m.fermer();
 }

 // D5. La publication a eu lieu mais le run finit en échec (archivage) : ne pas dire que rien n'a changé.
 {
  const m = await monde('d5', 'titres');
  m.echecApres.resumes = 'archivage';
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await page.fill('#gh-token', JETON);
  await page.click('label[for=titre-garder-1]');
  await page.click('#resumes');
  await o.attendre(() => !document.querySelector('#resumes[aria-disabled=true]'), null, 90000);
  const articles = (await page.$$('#article-list input[type=checkbox]')).length;
  const messages = (await o.texte('#titres-error')) + ' ' + (await o.texte('#collect-error')) + ' ' + (await o.texte('#collect-status'));
  check('D5 archivage en échec : rien n’est publié, l’étape en échec est nommée, les titres gardés restent cochés', articles === 0 && /« Archiver la collecte »/.test(messages) && /Vos titres gardés restent cochés/.test(messages) && (await page.$$eval('#titres-list input[type=checkbox]', l => l.filter(i => i.checked).length)) === 1 && !fs.existsSync(path.join(m.enLigne, 'paquet-v519.json')), `${articles} article ; messages : ${messages}`);
  await page.screenshot({path: path.join(sorties, 'd5-echec-apres-publication.png'), fullPage: true});
  await m.fermer();
 }

 // D6. Page rechargée (ou second onglet) pendant un run : la personne doit savoir qu'une collecte tourne.
 {
  const m = await monde('d6', 'collecte');
  m.attente = 50;
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  await saisir(page);
  await page.click('#collect');
  await o.attendreTexte('#collect-status', 'file d’attente');
  const autre = await p.onglet();
  await autre.waitForTimeout(1500);
  const statut = await autre.textContent('#collect-status');
  check('D6 second onglet pendant un run : la collecte en cours est signalée, sans jeton', /en cours/.test(statut) && !/^Prêt à lancer/.test(statut), statut);
  // Lancement depuis le second onglet : la personne est prévenue avant tout doublon.
  await saisir(autre);
  await autre.click('#collect');
  await autre.waitForTimeout(2500);
  const lancements = m.appels.filter(c => c.method === 'POST').length;
  const erreur = await autre.textContent('#collect-error');
  check('D6 second lancement : prévenu avant d’envoyer un doublon', lancements === 1 && /déjà en cours/.test(erreur), `${lancements} lancement(s) envoyé(s) ; ${erreur}`);
  await autre.screenshot({path: path.join(sorties, 'd6-run-en-cours.png'), fullPage: true});
  await m.fermer();
 }

 // D7. Libellés et annonces.
 {
  const m = await monde('d7', 'collecte');
  const p = await m.personne(), page = await p.onglet(), o = outils(page);
  const bouton = await o.texte('#candidates-button');
  check('D7 accordéon des écartés : libellé sans « par Albert »', /^Candidats écartés \(\d+\)$/.test(bouton), bouton);
  await saisir(page);
  m.attente = 3;
  await page.click('#collect');
  await o.attendre(() => !document.getElementById('reset-notice').hidden, null, 30000);
  await page.waitForTimeout(1200);
  const regions = await page.$$eval('[role=status]', l => l.filter(e => e.getClientRects().length).map(e => e.textContent));
  check('D7 remise à zéro : toujours annoncée dans une région d’état après le début de la progression', regions.some(t => /repart de zéro|archives/.test(t)) && regions.some(t => /^Collecte : /.test(t)), regions.filter(Boolean).join(' | '));
  await m.fermer();
 }

 console.log(`Captures : ${sorties}`);
 process.exit(bilan() ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
