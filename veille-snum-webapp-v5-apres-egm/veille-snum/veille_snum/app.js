'use strict';
const byId = id => document.getElementById(id);
// V5 utilise une nouvelle clé : une ancienne page V4, sans verrou, ne peut
// pas modifier les secrets enregistrés par cette version.
const ALBERT_STORAGE_KEY = 'veille-snum:albert:v2';
const OLD_ALBERT_STORAGE_KEY = 'veille-snum:albert:v1';
const ALBERT_LOCK_KEY = 'veille-snum:albert:lock:v2';
let storageSnapshot = null, storageEpoch = 0;
let persistenceAllowed = false;
const memoryStatus = message => { byId('albert-storage-status').textContent = message; };
const canLockStorage = () => typeof navigator !== 'undefined' &&
  navigator.locks && typeof navigator.locks.request === 'function';
function disablePersistence(message, clearFields=false) {
 byId('remember-albert').checked = false;
 storageSnapshot = null;
 storageEpoch++;
 if (clearFields) { byId('albert-key').value = ''; byId('albert-model').value = ''; }
 memoryStatus(message);
}
// Toute lecture-comparaison-écriture et suppression de secrets V5 doit
// s'exécuter dans la MÊME section critique inter-onglets (Web Locks API).
// L'absence de Web Locks désactive la persistance ; aucun repli non atomique.
function lockedStorage(action) {
 if (!canLockStorage()) {
  disablePersistence('La mémorisation est désactivée : coordination inter-onglets indisponible. Utilisez la saisie temporaire.');
  return Promise.resolve(false);
 }
 return navigator.locks.request(ALBERT_LOCK_KEY, {mode:'exclusive'}, action)
   .catch(() => {
     disablePersistence('Stockage impossible : une ancienne valeur peut subsister. Videz les données du site si nécessaire.');
     return false;
   });
}
function rememberAlbert() {
 if (!persistenceAllowed) {
  disablePersistence('Mémorisation désactivée sur ce serveur : utilisation temporaire uniquement.');
  return Promise.resolve(false);
 }
 if (!byId('remember-albert').checked) return Promise.resolve(false);
 const epoch = ++storageEpoch;
 const apiKey = byId('albert-key').value.trim();
 const model = byId('albert-model').value.trim();
 if (!apiKey) {
  disablePersistence('Saisissez une clé avant de demander sa mémorisation.');
  return Promise.resolve(false);
 }
 return lockedStorage(() => {
  if (epoch !== storageEpoch || !byId('remember-albert').checked) return false;
  try {
   const current = localStorage.getItem(ALBERT_STORAGE_KEY);
   if (storageSnapshot !== current) {
    disablePersistence('La clé enregistrée a changé dans un autre onglet. Mémorisation désactivée ; vérifiez les champs.',true);
    return false;
   }
   const value = JSON.stringify({apiKey,model});
   localStorage.setItem(ALBERT_STORAGE_KEY,value);
   storageSnapshot = value;
   memoryStatus('Clé et modèle conservés dans ce navigateur ; aucun chiffrement applicatif.');
   return true;
  } catch (_) {
   disablePersistence('Échec de stockage : une ancienne clé pourrait encore être enregistrée. Vérifiez les paramètres.');
   return false;
  }
 });
}
function forgetAlbert(clearFields=true,explicit=true) {
 const epoch=++storageEpoch, expected=storageSnapshot;
 byId('remember-albert').checked=false;
 // Vider les champs même si l'effacement persistant est interdit.
 if(clearFields){byId('albert-key').value='';byId('albert-model').value='';}
 return lockedStorage(() => {
  if(epoch!==storageEpoch) return false;
  try {
   const current=localStorage.getItem(ALBERT_STORAGE_KEY);
   if(!explicit && current!==expected){
    disablePersistence('Conflit inter-onglets : la nouvelle clé est préservée. Rechargez cette page.',true);
    return false;
   }
   localStorage.removeItem(ALBERT_STORAGE_KEY);
   localStorage.removeItem(OLD_ALBERT_STORAGE_KEY);
   storageSnapshot=null;
   memoryStatus('Entrée V5 supprimée sur cette origine. Une clé côté Python et une révocation Albert ne sont pas concernées.');
   return true;
  } catch (_) {
   storageSnapshot=null;
   memoryStatus('Suppression impossible : une clé peut subsister dans le stockage. Champs de cette page vidés.');
   return false;
  }
 });
}
function restoreAlbert() {
 if (!canLockStorage()) {
  memoryStatus('Mémorisation désactivée sur ce navigateur : Web Locks indisponible. Saisie temporaire possible.');
  return;
 }
 try {
  const raw=localStorage.getItem(ALBERT_STORAGE_KEY);
  if(raw){
   const saved=JSON.parse(raw);
   if(!saved || typeof saved.apiKey!=='string' || !saved.apiKey || typeof saved.model!=='string') {
    storageSnapshot=raw; void forgetAlbert(true,true);
    return;
   }
   byId('albert-key').value=saved.apiKey;
   byId('albert-model').value=saved.model;
   byId('remember-albert').checked=true;
   storageSnapshot=raw;
   memoryStatus('Clé V5 restaurée de cette origine ; stockage non chiffré.');
  }
  // Nettoyage à sens unique de l'ancien format V4 non coordonné.
  // Une page V4 encore ouverte peut recréer sa propre entrée : fermer V4.
  if(localStorage.getItem(OLD_ALBERT_STORAGE_KEY)!==null){
   void lockedStorage(() => {
    try {localStorage.removeItem(OLD_ALBERT_STORAGE_KEY); return true;}
    catch (_){ memoryStatus('Ancienne clé V4 non supprimée : effacez les données du site.');return false; }
   });
  }
 }catch(_){
  // Une entrée corrompue ne doit pas être restaurée. Sa suppression passe
  // par le même verrou ; si le navigateur refuse, ne pas annoncer de succès.
  try { storageSnapshot = localStorage.getItem(ALBERT_STORAGE_KEY); }
  catch (_) { storageSnapshot = null; }
  void forgetAlbert(true,true);
 }
}
byId('remember-albert').addEventListener('change', () => {
 if(byId('remember-albert').checked && !persistenceAllowed){
  disablePersistence('Mémorisation non autorisée sur cette exécution : utilisez la clé temporairement.');
  return;
 }
 if(byId('remember-albert').checked){
  if(storageSnapshot===null){
   try {if(localStorage.getItem(ALBERT_STORAGE_KEY)!==null){
    disablePersistence('Une clé existe déjà dans un autre onglet. Rechargez avant de la modifier.');return;
   }}catch(_){disablePersistence('Lecture du stockage impossible.');return;}
  }
  void rememberAlbert();
 }else void forgetAlbert(false,false);
});
for(const id of ['albert-key','albert-model']) {
 byId(id).addEventListener('change',()=>{
  if(byId('remember-albert').checked) {
   if(byId('albert-key').value.trim()) void rememberAlbert();
   else void forgetAlbert(false,false);
  }
 });
}
byId('forget-albert').addEventListener('click',()=>{void forgetAlbert(true,true);});
window.addEventListener('storage',event=>{
 if(event.key!==ALBERT_STORAGE_KEY && event.key!==null) return;
 if(event.newValue===storageSnapshot) return;
 disablePersistence('La clé a changé dans un autre onglet : anciens champs invalidés.',true);
});
byId('remember-albert').disabled = true;
let currentPacket = null, currentReport = null;
const pad = n => String(n).padStart(2, '0');
function localIso(d) { return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`; }
const today = new Date(), start = new Date(today); start.setDate(start.getDate()-7);
byId('edition').value = localIso(today); byId('end').value = localIso(today); byId('start').value = localIso(start);
const RUBRIC_LABELS = {numerique:'Numérique',ia:'Intelligence artificielle',commande:'Commande publique',rh:'Ressources humaines',bercy:'Bercy'};
const statusNames = {checked:'Découverte effectuée',partial:'Partielle / tronquée',skipped_budget:'Non traitée (temps)',skipped_internal:'Non traitée (source interne)',blocked:'Bloquée (robots.txt ou protection anti-robot)',error:'Échec technique',pending:'En attente'};
function line(list, label, url) {
 const li=document.createElement('li');
 if (url && /^https:\/\//.test(url)) { const a=document.createElement('a'); a.href=url; a.target='_blank'; a.rel='noopener noreferrer'; a.textContent=label; a.title=`${label} - nouvelle fenêtre`; li.append(a); }
 else li.textContent=label;
 list.append(li);
}
function clear(id) {byId(id).replaceChildren();}
function notice(message, error=false) {
 const box=byId('notice'), p=document.createElement('p');p.textContent=message;box.replaceChildren(p);
 box.classList.toggle('fr-alert--error',error);box.classList.toggle('fr-alert--info',!error);
}
// Validation différée (DSFR) : contraintes posées au premier envoi, erreur reliée au champ.
const DATE_FIELDS=[['edition',"la date d'édition"],['start','la date de début de période'],['end','la date de fin de période']];
function setFieldError(id,message){
 const group=byId(id+'-group'), box=byId(id+'-messages'), field=byId(id);
 box.replaceChildren();group.classList.toggle('fr-input-group--error',!!message);
 if(message){const p=document.createElement('p');p.className='fr-message fr-message--error';p.id=id+'-message-error';p.textContent=message;box.append(p);field.setAttribute('aria-invalid','true');}
 else field.removeAttribute('aria-invalid');
}
function validateDates(){
 const errors={};
 for(const [id,label] of DATE_FIELDS){const field=byId(id);field.required=true;field.setAttribute('aria-required','true');if(!field.value)errors[id]=`Indiquez ${label}.`;}
 const start=byId('start').value, end=byId('end').value;
 if(!errors.start&&!errors.end){
  if(start>end)errors.end='La fin de période doit être identique ou postérieure au début.';
  else if((Date.parse(end)-Date.parse(start))/86400000>60)errors.end='La période ne peut pas dépasser 61 jours.';
 }
 for(const [id] of DATE_FIELDS)setFieldError(id,errors[id]);
 const first=DATE_FIELDS.map(([id])=>id).find(id=>errors[id]);
 if(first){byId(first).focus();return false;}
 return true;
}
for(const [id] of DATE_FIELDS)byId(id).addEventListener('input',()=>{if(byId(id).getAttribute('aria-invalid'))setFieldError(id,'');});
async function info() {
 try {const r=await fetch('/api/info');if(!r.ok)throw Error('Service indisponible');const x=await r.json();
  persistenceAllowed=x.secret_persistence_enabled===true;
  byId('remember-albert').disabled=!persistenceAllowed;
  if(persistenceAllowed)restoreAlbert();
  else {
   // L'interdiction serveur retire les données des versions antérieures
   // plutôt que laisser un jeton dormant dans le profil du navigateur.
   memoryStatus('Mémorisation interdite dans cette exécution. Nettoyage des anciennes entrées en cours.');
   void forgetAlbert(true,true);
  }
  byId('configuration').textContent=`${x.sources.length} sources configurées · Albert ${x.albert_configured?'configuré sur ce poste':'à renseigner dans les options pour obtenir le JSON'}`;}
 catch(e) {byId('configuration').textContent='Configuration inaccessible';}
}
info();
byId('form').addEventListener('submit',async e=>{
 e.preventDefault();
 const payload={edition_date:byId('edition').value,window_start:byId('start').value,window_end:byId('end').value,albert_api_key:byId('albert-key').value,albert_model:byId('albert-model').value};
 if(!validateDates()){
  currentPacket=null;currentReport=null;byId('download').disabled=true;byId('report-download').disabled=true;byId('results').hidden=true;
  notice('Corrigez les champs signalés avant de lancer la collecte. L’export précédent est invalidé.',true);return;
 }
 if(byId('remember-albert').checked && !await rememberAlbert()) {
  notice('Clé enregistrée non synchronisée : collecte non lancée. Recontrôlez la clé.',true);
  return;
 }
 // Le verrou peut constater une modification dans un autre onglet et effacer
 // les champs pendant l'attente : utiliser les valeurs APRÈS vérification.
 payload.albert_api_key=byId('albert-key').value;
 payload.albert_model=byId('albert-model').value;
 try{sessionStorage.removeItem(RESULT_KEY);}catch(_){}
 byId('collect').disabled=true;byId('download').disabled=true;byId('report-download').disabled=true;currentPacket=null;currentReport=null;byId('results').hidden=true;
 notice('Collecte en cours. La consultation des sites peut prendre du temps.');
 const poll=setInterval(showProgress,1500);
 try {
  const response=await fetch('/api/collect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const result=await response.json();if(!response.ok)throw Error(result.error||'Échec HTTP');
  showResult(result);
  notice(result.status==='ready'?'Paquet disponible : relecture des sources obligatoire.':result.status==='partial'?'Collecte partielle : vérifiez les erreurs et les alertes.':result.status==='needs_albert'?'Candidats recherchés, mais Albert n’est pas configuré : aucun paquet V519 exportable.':result.status==='unavailable'?'Aucune source publique vérifiée : collecte techniquement indisponible.':'Impossible de produire un paquet complet : consulter les erreurs.',result.status==='incomplete'||result.status==='unavailable');
 } catch(err) {notice('Erreur de collecte : '+String(err.message||err),true);}finally{clearInterval(poll);byId('collect').disabled=false;if(!byId('remember-albert').checked)byId('albert-key').value='';}
});
// Avancement lu sur le serveur local : étape, nombre traité, source courante.
let lastProgress='';
async function showProgress(){
 try {
  const r=await fetch('/api/progress',{cache:'no-store'});if(!r.ok)return;
  const p=await r.json();
  const where=p.current?` (${p.current})`:'';
  const text=p.phase==='sites'&&p.total?`Recherche sur les sites : ${p.done}/${p.total}${where}…`
   :p.phase==='albert'&&p.total?`Résumés Albert : ${p.done}/${p.total} articles${where}…`
   :p.phase==='done'?'Préparation du résultat…':'';
  if(text&&text!==lastProgress&&byId('collect').disabled){lastProgress=text;notice(text);}
 } catch(_) {}
}
function showResult(result){
 byId('results').hidden=false;currentReport=result;currentPacket=result.packet||null;byId('download').disabled=!currentPacket;byId('report-download').disabled=false;
 byId('export-notice').textContent=currentPacket?'Après relecture, exporter le JSON.':'Export indisponible : vérifier le statut Albert.';
 const checked=result.sources.filter(x=>x.status==='checked').length;
 const partial=result.sources.filter(x=>x.status==='partial').length;
 const opened=result.sources.reduce((n,x)=>n+(x.opened||0),0);
 const attempted=result.sources.reduce((n,x)=>n+(x.attempted||0),0);
 const notVisited=result.sources.reduce((n,x)=>n+(x.not_visited||0),0);
 const stat=byId('summary');stat.hidden=false;stat.replaceChildren();
 // Un chiffre mis en valeur, puis son libellé : lecture rapide, grille de 2 puis 3 colonnes.
 const stats=[[`${checked}/13`,'sources explorées sans réserve'],[`${partial}`,'sources partielles ou plafonnées'],
  [`${opened}/${attempted}`,'pages reçues sur pages tentées'],[`${notVisited}`,'adresses découvertes non visitées'],
  [`${result.candidates.length}`,'candidats trouvés'],[`${currentPacket?currentPacket.articles.length:0}`,'articles préparés'],
  [`${result.excluded.length}`,'exclusions et erreurs'],[`${result.discovery_errors||0}`,'erreurs de plan de site']];
 for(const [value,label] of stats){
  const li=document.createElement('li');li.className='fr-col-6 fr-col-md-4';
  const number=document.createElement('p');number.className='fr-h4 fr-mb-0';number.textContent=value;
  const caption=document.createElement('p');caption.className='fr-text--sm fr-mb-0';caption.textContent=label;
  li.append(number,caption);stat.append(li);
 }
 for(const id of ['article-list','watch-list','source-list','candidate-list','excluded-list','error-list','rejected-list'])clear(id);
 selection=(currentPacket?.articles||[]).map(a=>({...a,keep:true}));
 // Repêchables : jugés hors thématique, non résumés faute de temps ou en échec Albert.
 const reasons={HORS_THEMATIQUE:'hors thématique',BUDGET_DUREE_ALBERT:'non résumé faute de temps'};
 const find=url=>result.candidates.find(c=>c.url===url);
 const seen=new Set();
 rejected=[...result.excluded.filter(x=>reasons[x.reason]).map(x=>({...find(x.url),motif:reasons[x.reason]})),
  ...(result.errors||[]).map(x=>({...find(x.url),motif:'échec Albert'}))]
  .filter(c=>c.url&&c.title&&!seen.has(c.url)&&seen.add(c.url));
 renderSelection();renderRejected();
 byId('selection-notice').textContent='';byId('update-packet').disabled=true;
 saveResult();
 for(const w of currentPacket?.watch||[])line(byId('watch-list'),`${w.title} : ${w.summary}`);
 if(!(currentPacket?.watch?.length))line(byId('watch-list'),'Pas de paquet ou pas d’alerte à présenter.');
 for(const s of result.sources)line(byId('source-list'),`${s.label} : ${statusNames[s.status]||s.status} · ${s.discovered||0} URL découvertes · ${s.attempted||0} tentées · ${s.opened||0} pages reçues · ${s.eligible||0} candidats · ${s.technical_errors||0} erreurs d’articles · ${s.discovery_errors||0} erreurs de découverte · ${s.sitemap_skipped||0} URL/sitemaps ignorés · ${s.not_visited||0} non tentées. ${(s.notes||[]).join(' ; ')}`);
 for(const c of result.candidates)line(byId('candidate-list'),`${c.publication_date_iso} · ${c.title} (${c.source})`,c.url);
 for(const x of result.excluded)line(byId('excluded-list'),`${x.source} : ${x.reason} (${x.url})`);
 for(const x of result.errors)line(byId('error-list'),`${x.reason} (${x.url})`);
}
// Sélection éditoriale : garder, écarter, reclasser ou repêcher, puis revalider côté serveur.
let selection=[], rejected=[];
// RGAA 11.1 : étiquette visible liée par for/id ; le titre de l'article, réservé aux lecteurs
// d'écran, rend chaque étiquette distincte tout en contenant le texte visible.
function visibleLabel(forId,visible,context){
 const label=document.createElement('label');label.className='fr-label';label.htmlFor=forId;
 const sr=document.createElement('span');sr.className='fr-sr-only';sr.textContent=` « ${context} »`;
 label.append(document.createTextNode(visible),sr);return label;
}
function rubricSelect(value,context,id){
 const group=document.createElement('div');group.className='fr-select-group';
 const select=document.createElement('select');select.className='fr-select';select.id=id;
 const messages=document.createElement('div');messages.className='fr-messages-group';messages.id=id+'-messages';messages.setAttribute('aria-live','polite');
 select.setAttribute('aria-describedby',messages.id);
 if(!value){const o=document.createElement('option');o.value='';o.textContent='Sélectionner une thématique';o.selected=true;o.disabled=true;select.append(o);}
 for(const [rid,name] of Object.entries(RUBRIC_LABELS)){const o=document.createElement('option');o.value=rid;o.textContent=name;o.selected=rid===value;select.append(o);}
 group.append(visibleLabel(id,'Thématique',context),select,messages);
 const setError=message=>{
  messages.replaceChildren();group.classList.toggle('fr-select-group--error',!!message);
  if(message){const p=document.createElement('p');p.className='fr-message fr-message--error';p.textContent=message;messages.append(p);select.setAttribute('aria-invalid','true');}
  else select.removeAttribute('aria-invalid');
 };
 select.addEventListener('change',()=>{if(select.value)setError('');});
 return {group,select,setError};
}
function keepCheckbox(checked,context,id){
 const group=document.createElement('div');group.className='fr-checkbox-group fr-checkbox-group--sm';
 const input=document.createElement('input');input.type='checkbox';input.id=id;input.checked=checked;
 group.append(input,visibleLabel(id,'Garder',context));
 return {group,input};
}
function selectionChanged(message){
 currentPacket=null;byId('download').disabled=true;byId('update-packet').disabled=false;
 byId('export-notice').textContent='Sélection modifiée : mettez à jour le paquet avant de le télécharger.';
 byId('selection-notice').textContent=message||'';
 saveResult();
}
// Résultat conservé dans l'onglet (effacé à sa fermeture) ; aucun secret n'y figure.
const RESULT_KEY='veille-snum:resultat:v1';
function saveResult(){
 if(!currentReport)return;
 const sources=currentReport.sources.map(({not_visited_urls,sitemap_skipped_urls,...rest})=>rest);
 try{sessionStorage.setItem(RESULT_KEY,JSON.stringify({report:{...currentReport,sources},packet:currentPacket,selection,rejected}));}catch(_){}
}
function restoreResult(){
 let saved=null;
 try{saved=JSON.parse(sessionStorage.getItem(RESULT_KEY)||'null');}catch(_){saved=null;}
 if(!saved?.report)return;
 showResult(saved.report);
 selection=saved.selection||[];rejected=saved.rejected||[];currentPacket=saved.packet||null;
 renderSelection();renderRejected();
 byId('download').disabled=!currentPacket;byId('update-packet').disabled=!!currentPacket;
 byId('export-notice').textContent=currentPacket?'Après relecture, exporter le JSON.':'Sélection modifiée : mettez à jour le paquet avant de le télécharger.';
 notice('Résultat de la dernière collecte restauré dans cet onglet.');
 saveResult();
}
function renderSelection(){
 const box=byId('article-list');box.replaceChildren();
 const kept=selection.filter(a=>a.keep).length;
 byId('article-count').textContent=selection.length?`${kept} article(s) gardé(s) sur ${selection.length}, soumis à relecture.`:'Aucun article éditorial prêt.';
 for(const [rubric,label] of Object.entries(RUBRIC_LABELS)){
  const items=selection.filter(a=>a.rubric===rubric);if(!items.length)continue;
  const title=document.createElement('h4');title.textContent=`${label} (${items.filter(a=>a.keep).length})`;
  const list=document.createElement('ol');box.append(title,list);
  for(const a of items){
   const li=document.createElement('li');li.className='fr-mb-3w';li.classList.toggle('unselected',!a.keep);
   const pick=document.createElement('div');pick.className='fr-grid-row fr-grid-row--gutters fr-grid-row--bottom fr-mt-1w';
   const index=selection.indexOf(a);
   const keepField=keepCheckbox(a.keep,a.title,`garder-${index}`), keep=keepField.input;
   // Après le nouveau rendu, le focus revient sur le champ modifié (identifiant stable).
   keep.addEventListener('change',()=>{a.keep=keep.checked;renderSelection();byId(keep.id)?.focus();selectionChanged(`${a.keep?'Article gardé':'Article écarté'} : ${a.title}`);});
   const rubricField=rubricSelect(a.rubric,a.title,`thematique-${index}`), select=rubricField.select;
   select.addEventListener('change',()=>{a.rubric=select.value;renderSelection();byId(select.id)?.focus();selectionChanged(`Thématique changée : ${a.title} → ${RUBRIC_LABELS[a.rubric]}`);});
   const keepCol=document.createElement('div');keepCol.className='fr-col-12 fr-col-md-4';keepCol.append(keepField.group);
   const rubricCol=document.createElement('div');rubricCol.className='fr-col-12 fr-col-md-6';rubricCol.append(rubricField.group);
   pick.append(keepCol,rubricCol);
   const details=document.createElement('details'), heading=document.createElement('summary');
   heading.textContent=`${a.publication_date_long||a.publication_date_iso} · ${a.title} (${a.source})`;
   const link=document.createElement('a');link.href=a.url;link.rel='noopener noreferrer';link.target='_blank';link.textContent='Consulter la publication (nouvelle fenêtre)';
   details.append(heading,link);
   for(const [label2,value] of [['Fait',a.fact],['À retenir',a.takeaway],['Intérêt SNUM',a.snum_interest],['Mots-clés',a.keywords.join(' · ')]]) {const p=document.createElement('p');const strong=document.createElement('strong');strong.textContent=label2+' : ';p.append(strong,document.createTextNode(value));details.append(p);}
   li.append(details,pick);list.append(li);
  }
 }
}
function renderRejected(){
 const list=byId('rejected-list');list.replaceChildren();
 if(!rejected.length){line(list,'Aucun article écarté comme hors thématique.');return;}
 for(const c of rejected){
  const li=document.createElement('li'), pick=document.createElement('div');li.className='fr-mb-3w';
  const link=document.createElement('a');link.href=c.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=`${c.publication_date_iso} · ${c.title} (${c.source}), ${c.motif||'écarté'}`;link.title=`${link.textContent} - nouvelle fenêtre`;
  const rubricField=rubricSelect('',c.title,`repecher-${rejected.indexOf(c)}`), select=rubricField.select;
  const add=document.createElement('button');add.type='button';add.className='fr-btn fr-btn--secondary fr-btn--sm';
  const addLabel=()=>{const sr=document.createElement('span');sr.className='fr-sr-only';sr.textContent=` « ${c.title} »`;add.replaceChildren(document.createTextNode('Ajouter'),sr);};
  addLabel();
  add.addEventListener('click',async()=>{
   if(!select.value){rubricField.setError('Choisissez la thématique de cet article avant de l’ajouter.');select.focus();return;}
   add.disabled=true;add.textContent='Résumé Albert en cours…';
   try{
    const r=await fetch('/api/summarize',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:c.url,rubric:select.value,albert_api_key:byId('albert-key').value,albert_model:byId('albert-model').value})});
    const x=await r.json();if(!r.ok)throw Error(x.error||'Échec');
    selection.push({...x.article,keep:true});rejected=rejected.filter(z=>z!==c);
    renderSelection();renderRejected();selectionChanged(`Article ajouté en ${RUBRIC_LABELS[x.article.rubric]} : ${x.article.title}`);
   }catch(err){add.disabled=false;addLabel();byId('selection-notice').textContent='Ajout impossible : '+String(err.message||err);}
  });
  const title=document.createElement('p');title.className='fr-mb-1w';title.append(link);
  const row=document.createElement('div');row.className='fr-grid-row fr-grid-row--gutters fr-grid-row--bottom';
  const selectCol=document.createElement('div');selectCol.className='fr-col-12 fr-col-md-6';selectCol.append(rubricField.group);
  const buttonCol=document.createElement('div');buttonCol.className='fr-col-12 fr-col-md-4';buttonCol.append(add);
  row.append(selectCol,buttonCol);pick.append(title,row);li.append(pick);list.append(li);
 }
}
byId('update-packet').addEventListener('click',async()=>{
 if(!currentReport)return;
 const button=byId('update-packet');button.disabled=true;byId('selection-notice').textContent='Mise à jour du paquet…';
 const fields=['title','source','publication_date_iso','url','rubric','fact','keywords','takeaway','snum_interest'];
 const payload={edition_date:currentReport.edition_date,window_start:currentReport.window_start,window_end:currentReport.window_end,
  articles:selection.filter(a=>a.keep).map(a=>Object.fromEntries(fields.map(f=>[f,a[f]]))),
  sources:currentReport.sources.map(s=>({label:s.label,status:s.status,opened:s.opened||0,not_visited:s.not_visited||0}))};
 try{
  const r=await fetch('/api/packet',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const x=await r.json();if(!r.ok)throw Error(x.error||'Échec');
  currentPacket=x.packet;byId('download').disabled=false;saveResult();
  byId('export-notice').textContent='Paquet mis à jour et revalidé : relecture puis téléchargement.';
  byId('selection-notice').textContent=`${currentPacket.articles.length} article(s) dans le paquet V519.`;
 }catch(err){button.disabled=false;byId('selection-notice').textContent='Paquet refusé : '+String(err.message||err);}
});
byId('report-download').addEventListener('click',()=>{
 if(!currentReport)return;
 downloadJson(currentReport,`veille-snum-rapport-${currentReport.edition_date}.json`);
});
function downloadJson(value, filename) {
 const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)+'\n'],{type:'application/json;charset=utf-8'}));
 const anchor=document.createElement('a');anchor.href=url;anchor.download=filename;anchor.click();
 setTimeout(()=>URL.revokeObjectURL(url),2000);
}
byId('download').addEventListener('click',()=>{
 if(!currentPacket)return;
 downloadJson(currentPacket,`veille-snum-${currentPacket.edition_date}.json`);
 byId('export-notice').textContent='Téléchargement proposé : vérifier la présence du fichier.';
});
// Après toutes les déclarations : restaure le dernier résultat de cet onglet.
restoreResult();
