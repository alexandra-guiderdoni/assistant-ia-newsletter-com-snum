// Rubrique probable d'un titre (pages/rubriques-probables.js), chargée par vm sans DOM.
// Titres inventés : aucun titre de la revue de presse interne dans ce dépôt public.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const ctx = {window: {}};
for (const name of ['selection.js', 'rubriques-probables.js']) {
 vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../pages', name), 'utf8'), ctx, {filename: name});
}
const P = ctx.window.VeilleRubriquesProbables, S = ctx.window.VeilleSelection;

test('les onze rubriques de la revue ont leurs mots-clés, et seulement elles', () => {
 assert.deepEqual([...P.ORDRE].sort(), [...S.RUBRICS].sort());
 assert.deepEqual(Object.keys(P.MOTS).sort(), [...S.RUBRICS].sort());
});

test('un mot-clé reconnu donne sa rubrique et le mot tel qu’il est affiché', () => {
 const cas = [
  ['Une cyberattaque paralyse une collectivité imaginaire', 'securite', 'cyberattaque'],
  ['La CNIL publie un avis fictif sur les caméras', 'droit', 'CNIL'],
  ['Un nouveau data center annoncé dans une région inventée', 'infrastructure', 'data center'],
  ['Bercy présente un plan fictif de simplification', 'bercy', 'Bercy'],
  ['L’UGAP lance un appel d’offres imaginaire', 'commande', 'appel d’offres'],
 ];
 for (const [titre, rubric, keyword] of cas) assert.deepEqual({...P.probable(titre)}, {rubric, keyword}, titre);
});

test('sans accents, majuscules ni apostrophe typographique, le mot est reconnu', () => {
 assert.equal(P.probable('LA CYBERSECURITE DES HOPITAUX FICTIFS').rubric, 'securite');
 assert.equal(P.probable("Le Conseil d'Etat rend une decision imaginaire").rubric, 'droit');
});

test('mots entiers seulement : « IA » ne se trouve pas dans « médias » ni « Asie »', () => {
 assert.equal(P.probable('Les médias en Asie, une enquête inventée'), null);
});

test('égalité départagée par la rubrique la plus précise, plus de mots l’emporte', () => {
 // Un mot pour l'IA, un pour la sécurité : l'IA passe d'abord dans l'ordre de départage.
 assert.equal(P.probable('Une IA détecte une faille imaginaire').rubric, 'ia');
 // Deux mots pour la sécurité contre un pour l'IA.
 assert.equal(P.probable('Une IA face à une cyberattaque et une faille inventées').rubric, 'securite');
});

test('aucun mot reconnu : null, pour le groupe « Rubrique non reconnue »', () => {
 assert.equal(P.probable('Un titre sans aucun indice de rubrique'), null);
 assert.equal(P.probable(''), null);
 assert.equal(P.probable(undefined), null);
});
