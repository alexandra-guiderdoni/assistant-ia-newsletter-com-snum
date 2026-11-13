# Mission de contre-revue indépendante EGM : veille SNUM

## Contexte minimal à remettre au Goldfish

Tu es un relecteur technique **sans accès à la conversation ayant produit ce prototype**. Le projet ajoute une webapp de collecte d'articles ciblée sur 14 sources et cinq rubriques, puis prépare un JSON V519 compatible avec le convertisseur existant dans builder-mail-dsfr. La collecte doit rester gratuite côté recherche ; Albert API est utilisé pour la classification et la rédaction, sous réserve d'accès et de quotas. Le prototype actuel est local, non déployé.

Lis uniquement ces pièces, sans reprendre les conclusions du concepteur comme des faits :

1. `docs/designs/veille-snum.md` et `docs/reviews/veille-snum-egm-pre-review.md` ;
2. `veille_snum/core.py`, `veille_snum/web.py`, `veille_snum/index.html`, `veille_snum/sources.json` ;
3. `tests/test_veille_snum.py` ;
4. Dans le dépôt assistant-ia-newsletter-com-snum : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md`, `02-METHODE-COLLECTE-SNUM-V5.23.md`, `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` ;
5. Dans builder-mail-dsfr : `prototype/reference/snum-packet.js`, `app/snum/adapter.js` ;
6. Dans google/elephant-goldfish-model : `agents/zoom_out.md`, `agents/design_critic.md`, `agents/implementation_readiness.md` et rubriques associées de `resources/document_standards/`.

## Tâche

Exécute une revue EGM **à contexte neuf** selon les trois angles :

- **Zoom Out/YAGNI** : simplification possible, pièces inutiles, réutilisation des deux dépôts existants, coût et maintenance.
- **Design Critic** : qualité réelle de la découverte, absence de garantie d'exhaustivité, dates de publication, robots, redirections, droits, sécurité réseau et exposition de la clé Albert, absence de fuite de la source interne.
- **Implementation Readiness** : tests de bout en bout manquants, compatibilité exacte avec le parseur V519 du builder, accès Albert, UI accessible clavier/VoiceOver/NVDA, parcours de lancement macOS.

Pour chaque constat : gravité Bloquant/Majeur/Mineur, emplacement précis du code ou de la spécification, preuve, impact, correction minimale, test de non-régression. Distingue les défauts observés, les hypothèses et les validations impossibles à distance.

N'améliore pas artificiellement le projet en ajoutant une couche de recherche commerciale. Ne suppose pas que RSS, SearXNG ou GDELT sont nécessaires sans mesure empirique. Propose une comparaison sur quatre semaines de publications de référence pour évaluer le rappel de collecte par domaine et rubrique.

Produis un rapport Markdown autonome et une liste courte de corrections prioritaires. Tu peux proposer des changements, mais ne modifie pas `main` ni les rendus historiques. Vérifie que les modifications proposées conservent les 14 sources logiques et le JSON V519.
