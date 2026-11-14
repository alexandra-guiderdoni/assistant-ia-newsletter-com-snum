const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname,'../veille_snum/index.html'),'utf8');
const script = fs.readFileSync(path.join(__dirname,'../veille_snum/app.js'),'utf8');
const key = 'veille-snum:albert:v2';
// Élément créé par le script : assez de DOM pour rendre la sélection éditoriale.
const domElement = () => ({
  textContent:'', className:'', children:[], classList:{toggle(){}},
  append(...items){this.children.push(...items);}, replaceChildren(){this.children=[];},
  setAttribute(){}, removeAttribute(){}, addEventListener(){}, click(){},
});
async function load(storage = new Map(), failing = false, opts = {}) {
  const fails = failing === true ? {read:true,write:true,remove:true} : (failing || {});
  const nodes = new Map();
  const element = id => {
    if (!nodes.has(id)) nodes.set(id, {
      id, value:'', checked:false, disabled:false, textContent:'', hidden:false,
      events:{},
      classList:{toggle(){}},
      addEventListener(type, cb) {this.events[type] = cb;},
      children:[], replaceChildren(){this.children=[];}, append(...items){this.children.push(...items);},
    });
    return nodes.get(id);
  };
  const ls = {
    getItem(k) {if(fails.read) throw Error('disabled');return storage.get(k) ?? null;},
    setItem(k,v) {if(fails.write) throw Error('disabled');storage.set(k,v);},
    removeItem(k) {if(fails.remove) throw Error('disabled');storage.delete(k);},
  };
  const ctx = {
    document:{getElementById:element,createElement:domElement,createTextNode:s=>s},
    localStorage:ls, Date, String, URL, Blob, setTimeout(){},
    navigator:{locks: opts.locks === false ? undefined : (opts.locks || {request(_key,_opts,cb){return Promise.resolve(cb());}})},
    window:{addEventListener(type, cb) {this.events[type]=cb;},events:{}},
    fetch:async()=>({ok:true,json:async()=>({sources:Array(14),albert_configured:false,secret_persistence_enabled:opts.persistence !== false,...(opts.info || {})})}),
  };
  vm.runInNewContext(script,ctx,{filename:'index.html'});
  await new Promise(resolve=>setImmediate(resolve));
  return {node:element,store:storage,ctx};
}

test('stockage désactivé par défaut, même après saisie',async()=>{
  const a=await load();
  assert.equal(a.store.size,0);
  a.node('albert-key').value='jeton-factice';
  a.node('albert-key').events.change();
  assert.equal(a.store.size,0);
});

test('opt-in persiste clé et modèle; rechargement restaure; effacement supprime',async()=>{
  const a=await load();
  a.node('albert-key').value='jeton-factice';
  a.node('albert-model').value='modele-test';
  a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();
  assert.deepEqual(JSON.parse(a.store.get(key)),{apiKey:'jeton-factice',model:'modele-test'});
  const b=await load(a.store);
  assert.equal(b.node('albert-key').value,'jeton-factice');
  assert.equal(b.node('albert-model').value,'modele-test');
  assert.equal(b.node('remember-albert').checked,true);
  b.node('forget-albert').events.click();
  assert.equal(b.store.has(key),false);
  assert.equal(b.node('albert-key').value,'');
  assert.equal(b.node('albert-model').value,'');
});

test('décocher supprime le stockage mais préserve les champs de la collecte courante',async()=>{
  const a=await load();
  a.node('albert-key').value='jeton-factice';
  a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();
  assert.ok(a.store.has(key));
  a.node('remember-albert').checked=false;
  a.node('remember-albert').events.change();
  assert.equal(a.store.has(key),false);
  assert.equal(a.node('albert-key').value,'jeton-factice');
});

test('stockage indisponible ne bloque pas la saisie',async()=>{
  const a=await load(new Map(),true);
  a.node('albert-key').value='jeton-factice';
  a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();
  assert.equal(a.node('remember-albert').checked,false);
  assert.match(a.node('albert-storage-status').textContent,/impossible|indisponible/);
});

test('enregistrement refusé sans jeton et données stockées invalides supprimées',async()=>{
  const a=await load();
  a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();
  assert.equal(a.node('remember-albert').checked,false);
  assert.equal(a.store.size,0);
  const storage=new Map([[key,'{']]);
  const b=await load(storage);
  assert.equal(b.store.has(key),false);
  assert.equal(b.node('albert-key').value,'');
});


test('S03 : un second onglet ne réenregistre pas une clé supprimée sans notification',async()=>{
  const shared = new Map();
  const a = await load(shared);
  a.node('albert-key').value='SECRET-FAKE';
  a.node('albert-model').value='M1';
  a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();
  const b = await load(shared);
  a.node('forget-albert').events.click();
  assert.equal(shared.has(key),false);
  b.node('albert-model').value='M2';
  b.node('albert-model').events.change();
  assert.equal(shared.has(key),false);
  assert.equal(b.node('remember-albert').checked,false);
  assert.equal(b.node('albert-key').value,'');
});

test('S03 : suppression dans un onglet invalide immédiatement la copie reçue',async()=>{
  const shared = new Map();
  const a = await load(shared);
  a.node('albert-key').value='FAKE';
  a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();
  const b = await load(shared);
  a.node('forget-albert').events.click();
  b.ctx.window.events.storage({key,newValue:null});
  assert.equal(b.node('remember-albert').checked,false);
  assert.equal(b.node('albert-key').value,'');
});


test('S01 : erreur en écriture ne prétend pas avoir supprimé une ancienne clé',async()=>{
  const old = JSON.stringify({apiKey:'OLD_FAKE',model:'M0'});
  const store = new Map([[key,old]]);
  const a = await load(store,{write:true});
  a.node('albert-key').value='NEW_FAKE';
  a.node('remember-albert').checked=true;
  a.node('albert-model').value='M1';
  a.node('albert-model').events.change();
  assert.equal(store.get(key),old);
  assert.match(a.node('albert-storage-status').textContent,/ancienne clé|échec|Rechargez/i);
});

test('S01 : effacement refusé ne peut pas être annoncé comme réussi',async()=>{
  const old = JSON.stringify({apiKey:'OLD_FAKE',model:'M0'});
  const store = new Map([[key,old]]);
  const a = await load(store,{remove:true});
  a.node('forget-albert').events.click();
  assert.equal(store.get(key),old);
  assert.match(a.node('albert-storage-status').textContent,/impossible/i);
});

const tick = () => new Promise(resolve => setImmediate(resolve));
function serialLocks() {
  const chains = new Map();
  return {request(name,_options,action) {
    const predecessor = chains.get(name) || Promise.resolve();
    const task = predecessor.catch(()=>{}).then(action);
    chains.set(name,task.catch(()=>{}));
    return task;
  }};
}

test('S03 V5 : deux onglets concurrents, effacement ne ressuscite pas la clé',async()=>{
  const shared=new Map(),locks=serialLocks();
  const a=await load(shared,false,{locks});
  a.node('albert-key').value='FAKE-ONLY-A';a.node('albert-model').value='M1';
  a.node('remember-albert').checked=true;a.node('remember-albert').events.change();await tick();
  const b=await load(shared,false,{locks});
  a.node('forget-albert').events.click();
  b.node('albert-model').value='M2';b.node('albert-model').events.change();
  await tick();
  assert.equal(shared.has(key),false);
  assert.equal(b.node('remember-albert').checked,false);
  assert.equal(b.node('albert-key').value,'');
});

test('S03 V5 : rotation simultanée protégée sous verrou partagé',async()=>{
  const shared=new Map(),locks=serialLocks();
  const a=await load(shared,false,{locks});
  a.node('albert-key').value='FAKE-OLD';a.node('remember-albert').checked=true;a.node('remember-albert').events.change();await tick();
  const b=await load(shared,false,{locks});
  a.node('albert-key').value='FAKE-NEW';a.node('albert-key').events.change();
  b.node('albert-model').value='M2';b.node('albert-model').events.change();
  await tick();
  assert.equal(JSON.parse(shared.get(key)).apiKey,'FAKE-NEW');
  assert.equal(b.node('remember-albert').checked,false);
});

test('S03 V5 : effacement implicite périmé ne supprime pas la nouvelle clé',async()=>{
  const shared=new Map(),locks=serialLocks();
  const a=await load(shared,false,{locks});
  a.node('albert-key').value='FAKE-OLD';a.node('remember-albert').checked=true;a.node('remember-albert').events.change();await tick();
  const b=await load(shared,false,{locks});
  a.node('albert-key').value='FAKE-NEW';a.node('albert-key').events.change();
  b.node('albert-key').value='';b.node('albert-key').events.change();
  await tick();
  assert.equal(JSON.parse(shared.get(key)).apiKey,'FAKE-NEW');
  assert.match(b.node('albert-storage-status').textContent,/conflit|modifi/i);
});

test('V5 : mémoire désactivée par défaut sur le serveur, même avec Web Locks',async()=>{
  const shared=new Map(),a=await load(shared,false,{persistence:false});
  assert.equal(a.node('remember-albert').disabled,true);
  a.node('albert-key').value='FAKE';a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();await tick();
  assert.equal(shared.has(key),false);
  assert.equal(a.node('remember-albert').checked,false);
});

test('V5 : sans Web Locks, aucune mémorisation même si serveur la permet',async()=>{
  const shared=new Map(),a=await load(shared,false,{locks:false});
  a.node('albert-key').value='FAKE';a.node('remember-albert').checked=true;
  a.node('remember-albert').events.change();await tick();
  assert.equal(shared.has(key),false);
  assert.equal(a.node('remember-albert').checked,false);
  assert.match(a.node('albert-storage-status').textContent,/désactivée/i);
});

test('V5 : échec suppression vide les champs, conserve avertissement exact',async()=>{
  const shared=new Map([[key,JSON.stringify({apiKey:'FAKE',model:'M'})]]);
  const a=await load(shared,{remove:true});
  a.node('forget-albert').events.click();await tick();
  assert.equal(a.node('albert-key').value,'');
  assert.equal(a.node('albert-model').value,'');
  assert.equal(shared.has(key),true);
  assert.match(a.node('albert-storage-status').textContent,/Suppression impossible/);
});


test('V5 : désactivation serveur efface un secret antérieurement persisté',async()=>{
 const shared=new Map([[key,JSON.stringify({apiKey:'FAKE',model:'OLD'})]]);
 const a=await load(shared,false,{persistence:false});await tick();
 assert.equal(shared.has(key),false);
 assert.equal(a.node('albert-key').value,'');
 assert.equal(a.node('remember-albert').disabled,true);
});

test('modèle prérempli par le serveur, sans écraser un modèle mémorisé',async()=>{
 const a=await load(new Map(),false,{persistence:false,info:{albert_model:'openweight-large'}});await tick();
 assert.equal(a.node('albert-model').value,'openweight-large');
 const shared=new Map([[key,JSON.stringify({apiKey:'FAKE',model:'modele-test'})]]);
 const b=await load(shared,false,{info:{albert_model:'openweight-large'}});await tick();
 assert.equal(b.node('albert-model').value,'modele-test');
});

function packetArticle(i,rubric){
 return {id:`U${String(i).padStart(2,'0')}`,rubric,title:`Article ${i}`,source:'Next',publication_date_iso:'2026-11-06',
  publication_date_long:'6 novembre 2026',url:`https://next.ink/article/${i}`,fact:'Fait.',keywords:['numérique'],
  takeaway:'À retenir.',snum_interest:'Intérêt.',essential:false};
}
const collectResult=rubrics=>({status:'ready',sources:[],candidates:[],excluded:[],errors:[],discovery_errors:0,
 packet:{articles:rubrics.map((r,i)=>packetArticle(i+1,r)),watch:[]}});
function keepBoxes(node,found={}){
 if(node&&node.type==='checkbox'&&String(node.id).startsWith('garder-'))found[node.id]=node.checked;
 for(const child of node?.children||[])keepBoxes(child,found);
 return found;
}

test('par défaut, seuls les deux premiers articles de chaque thématique sont gardés',async()=>{
 const a=await load();
 a.ctx.showResult(collectResult(['numerique','numerique','numerique','ia','bercy','bercy','bercy']));
 assert.equal(a.node('article-count').textContent,'5 article(s) gardé(s) sur 7, soumis à relecture.');
 assert.deepEqual(keepBoxes(a.node('article-list')),
  {'garder-0':true,'garder-1':true,'garder-2':false,'garder-3':true,'garder-4':true,'garder-5':true,'garder-6':false});
 // La sélection par défaut diffère du paquet du serveur : export bloqué jusqu'à revalidation.
 assert.equal(a.node('download').disabled,true);
 assert.equal(a.node('update-packet').disabled,false);
 assert.match(a.node('selection-notice').textContent,/2 premiers articles de chaque thématique/);
});

test('thématiques de deux articles au plus : tout reste gardé et le paquet reste téléchargeable',async()=>{
 const a=await load();
 a.ctx.showResult(collectResult(['numerique','numerique','ia']));
 assert.equal(a.node('article-count').textContent,'3 article(s) gardé(s) sur 3, soumis à relecture.');
 assert.equal(a.node('download').disabled,false);
 assert.equal(a.node('update-packet').disabled,true);
});
