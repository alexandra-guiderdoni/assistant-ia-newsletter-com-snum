// Relevé d'accessibilité du 14 novembre 2026 : points corrigés, vérifiés sur les sources des pages.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const PAGES = path.join(__dirname, '../pages');
const lire = nom => fs.readFileSync(path.join(PAGES, nom), 'utf8');

test('passages en anglais de l’aide du jeton marqués lang="en"', () => {
 const html = lire('index.html');
 for (const passage of ['fine-grained', 'Actions : Read and write', 'Contents : Read']) assert.match(html, new RegExp(`<span lang="en">${passage}</span>`), passage);
});

test('région d’état vide : un div, pas un paragraphe vide', () => {
 const html = lire('index.html');
 assert.match(html, /<div id="reset-status" class="fr-sr-only" role="status"><\/div>/);
 assert.doesNotMatch(html, /<p id="reset-status"/);
});

test('liens « Consulter la publication » : le titre de l’article fait partie du nom du lien', () => {
 assert.match(lire('selection.js'), /function publicationLink\(url, title\)/);
 for (const nom of ['selection.js', 'titres.js', 'ecartes.js']) {
  const source = lire(nom);
  assert.match(source, /publicationLink\(/, nom);
  assert.doesNotMatch(source, /'Consulter la publication \(nouvelle fenêtre\)'/, nom);
 }
});

test('pied de page : mention d’accessibilité exacte, liée au relevé présent dans le dépôt', () => {
 for (const nom of ['index.html', 'archives.html']) {
  const html = lire(nom);
  assert.doesNotMatch(html, /audit non réalisé/, nom);
  const lien = /<a class="fr-footer__bottom-link" href="https:\/\/github\.com\/alexandra-guiderdoni\/assistant-ia-newsletter-com-snum\/blob\/main\/([^"]+)" target="_blank" rel="noopener noreferrer">Accessibilité : non conforme \(nouvelle fenêtre\)<\/a>/.exec(html);
  assert.ok(lien, nom);
  assert.ok(fs.existsSync(path.join(__dirname, '../../..', lien[1])), lien[1]);
 }
});

test('rapport : « plans de site » plutôt que le mot anglais', () => {
 assert.doesNotMatch(lire('rapport.js'), /URL\/sitemaps/);
});
