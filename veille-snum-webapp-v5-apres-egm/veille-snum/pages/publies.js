'use strict';
// Articles déjà publiés (#34) : les périodes se touchent (elles commencent le jour de
// l'envoi précédent), donc un article peut revenir d'une édition à la suivante. Les
// paquets des dernières éditions archivées (branche donnees-veille, lus sans jeton sur
// raw.githubusercontent.com) disent quelles adresses ont déjà été publiées.
// Première partie : fonctions pures (tests/test_pages_publies.cjs).
// Seconde partie : lecture des archives ; selection.js et titres.js affichent la mention.
(function (global) {
 // archives.js est chargé après ce module : il n'est lu qu'au moment de la vérification.
 const S = global.VeilleSelection, G = global.VeilleGithub;
 const MAX_EDITIONS = 4;

 // Index le plus récent en premier : pour une même date d'édition, la dernière archive fait foi.
 function previous(collectes, edition) {
  const seen = new Set(), out = [];
  for (const c of collectes) {
   if (out.length === MAX_EDITIONS) break;
   if (!(c.edition_date < edition) || !c.articles || seen.has(c.edition_date)) continue;
   seen.add(c.edition_date);
   out.push(c);
  }
  return out;
 }
 // [{edition_date, packet}] du plus récent au plus ancien -> Map(adresse -> date de la plus récente édition).
 function published(items) {
  const map = new Map();
  for (const {edition_date: date, packet} of items) {
   if (!S.isPacket(packet)) continue;
   for (const a of packet.articles) if (a && typeof a.url === 'string' && !map.has(a.url)) map.set(a.url, date);
  }
  return map;
 }
 const note = date => `Déjà publié dans l’édition du ${S.dateLong(date)}`;
 function summary(r) {
  if (r.error) return 'Vérification des articles déjà publiés impossible : archives injoignables. La sélection fonctionne normalement.';
  const n = r.editions.length;
  if (!n) return 'Aucune édition précédente archivée : pas de doublon à signaler.';
  const where = n === 1 ? 'l’édition précédente archivée' : `les ${n} éditions précédentes archivées`;
  if (!r.found) return `Aucun article déjà publié dans ${where}.`;
  const one = r.found === 1;
  return `${r.found} article${one ? '' : 's'} déjà publié${one ? '' : 's'} dans ${where} : signalé${one ? '' : 's'} par « Déjà publié », non gardé${one ? '' : 's'} par défaut.`;
 }

 // ---------- Lecture des archives ----------
 let known = new Map();
 const dateOf = url => known.get(url) || '';
 async function readJson(url) {
  const r = await fetch(url, G.timed({cache: 'no-store'}));
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
 }
 // Archives illisibles : {error: true}, et rien n'est signalé. Un paquet illisible est ignoré.
 async function check(edition) {
  try {
   const A = global.VeilleArchives, bust = Date.now();
   const editions = previous(A.parseIndex(await readJson(A.indexUrl(bust))).collectes, edition);
   const packets = await Promise.all(editions.map(c => readJson(A.archiveUrl(c.id, 'paquet-v519.json', bust))
    .then(packet => ({edition_date: c.edition_date, packet}), () => ({edition_date: c.edition_date, packet: null}))));
   known = published(packets);
   return {editions: editions.map(c => c.edition_date)};
  } catch (_) {
   known = new Map();
   return {error: true};
  }
 }

 // Mention ajoutée une fois sous le titre (h4) de node ; renvoie vrai si l'adresse est déjà publiée.
 function decorate(node, url) {
  const date = dateOf(url);
  if (!node || !date) return false;
  if (!node.querySelector('.fr-badge')) {
   const p = document.createElement('p');
   p.className = 'fr-badge fr-badge--sm fr-badge--info fr-mb-1w'; p.textContent = note(date);
   node.querySelector('h4').after(p);
  }
  return true;
 }

 global.VeillePublies = {MAX_EDITIONS, previous, published, note, summary, check, dateOf, decorate};
})(typeof window !== 'undefined' ? window : globalThis);
