'use strict';
// Rubrique probable d'un titre, d'après des mots-clés écrits à partir des seules définitions des onze rubriques.
// Indicatif : mesuré le 14 novembre 2026 sur 245 titres réels de la revue de presse, un mot-clé est reconnu
// pour 81 % des titres, et la rubrique est alors juste pour 74 % d'entre eux. Albert range l'article après lecture.
// Tests : tests/test_pages_rubriques.cjs.
(function (global) {
 // Départage : la rubrique la plus précise d'abord, comme dans la consigne donnée à Albert.
 const ORDRE = ['ia', 'securite', 'bercy', 'droit', 'commande', 'rh', 'infrastructure', 'applications', 'dsi', 'economie', 'administration'];
 // Mots affichés tels quels ; la recherche se fait sans accents ni majuscules, sur des mots entiers.
 const MOTS = {
  ia: ['IA', 'intelligence artificielle', 'ChatGPT', 'OpenAI', 'Mistral AI', 'Anthropic', 'Gemini', 'Copilot', 'LLM',
   'générative', 'AI Act', 'agent IA', 'agents IA', 'algorithme'],
  securite: ['cyber', 'cyberattaque', 'cybersécurité', 'piratage', 'pirate', 'pirates', 'hacker', 'rançongiciel', 'ransomware',
   'fuite de données', 'fuites de données', 'vulnérabilité', 'faille', 'failles', 'ANSSI', 'phishing', 'hameçonnage',
   'NIS 2', 'malware', 'cybercriminalité', 'cybercriminel'],
  administration: ['administration', 'administrations', 'service public', 'services publics', 'démarche', 'démarches',
   'FranceConnect', 'France Connect', 'identité numérique', 'DINUM', 'collectivité', 'collectivités',
   'dématérialisation', 'données publiques', 'open data', 'État numérique'],
  dsi: ['DSI', 'direction du numérique', 'directeur du numérique', 'gouvernance', 'mutualisation', 'méthode', 'agilité',
   'DevOps', 'chef de projet'],
  economie: ['start-up', 'startup', 'levée de fonds', 'lève', 'valorisation', 'souveraineté', 'DMA', 'DSA', 'concurrence',
   'investissement', 'licorne', 'French Tech', 'plateformes', 'marché du numérique'],
  infrastructure: ['cloud', 'data center', 'data centers', 'datacenter', 'datacenters', 'centre de données', 'centres de données',
   'hébergement', 'réseau', 'réseaux', 'fibre', '5G', 'télécom', 'télécoms', 'satellite', 'serveur', 'serveurs'],
  applications: ['logiciel', 'logiciels', 'application', 'applications', 'appli', 'messagerie', 'Outlook', 'Microsoft 365',
   'Windows', 'Linux', 'navigateur', 'Firefox', 'Chrome', 'Android', 'iOS', 'mise à jour', 'bureautique',
   'open source', 'développeur', 'développeurs'],
  droit: ['CNIL', 'RGPD', 'données personnelles', 'vie privée', 'tribunal', 'juridique', 'Conseil d’État', 'Cour de justice',
   'amende', 'sanction', 'règlement', 'Digital Fairness'],
  commande: ['achat public', 'achats publics', 'commande publique', 'marché public', 'marchés publics', 'appel d’offres',
   'UGAP', 'acheteur', 'acheteurs'],
  rh: ['fonctionnaire', 'fonctionnaires', 'agents publics', 'point d’indice', 'recrutement', 'rémunération', 'fonction publique',
   'DRH', 'ressources humaines', 'nomination', 'nommé', 'nommée', 'télétravail', 'compétences', 'carrière'],
  bercy: ['Bercy', 'Minefi', 'ministère de l’Économie', 'ministères économiques', 'DGFiP', 'douane', 'douanes', 'Insee',
   'DGCCRF', 'Trésor', 'PLF', 'secrétaire générale'],
 };
 // Même mise à plat que la mesure : minuscules, apostrophe droite, sans accents, ponctuation remplacée par des espaces.
 const plat = texte => ` ${String(texte || '').toLowerCase().replace(/’/g, "'").normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9' -]+/g, ' ')} `;
 const echappe = mot => mot.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 const MOTIFS = Object.fromEntries(Object.entries(MOTS).map(([rubrique, mots]) =>
  [rubrique, mots.map(mot => ({mot, motif: new RegExp(`(?<![a-z0-9])${echappe(plat(mot).trim())}(?![a-z0-9])`)}))]));

 // {rubric, keyword} : rubrique qui reconnaît le plus de mots, départagée par ORDRE ; null si aucun mot n'est reconnu.
 function probable(titre) {
  const t = plat(titre);
  let meilleur = null;
  for (const rubrique of ORDRE) {
   const trouves = MOTIFS[rubrique].filter(m => m.motif.test(t));
   if (trouves.length && (!meilleur || trouves.length > meilleur.n)) meilleur = {rubric: rubrique, keyword: trouves[0].mot, n: trouves.length};
  }
  return meilleur && {rubric: meilleur.rubric, keyword: meilleur.keyword};
 }

 global.VeilleRubriquesProbables = {ORDRE, MOTS, plat, probable};
})(typeof window !== 'undefined' ? window : globalThis);
