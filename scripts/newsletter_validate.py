"""Validation bloquante des invariants du gabarit Bacoco."""

import re

from newsletter_render import MARKER, RUBRICS


def matches_template_shell(html, template):
    for name in ("ESSENTIELS", "RUBRIQUES", "A_SURVEILLER"):
        template = re.sub(rf"\s*@@{name}@@\s*", f"@@{name}@@", template)
    html = compact_markup(html)
    fragments = MARKER.split(compact_markup(template))
    if not html.startswith(fragments[0]) or not html.endswith(fragments[-1]):
        return False
    cursor = len(fragments[0])
    for fragment in fragments[1:-1]:
        position = html.find(fragment, cursor)
        if position < 0:
            return False
        cursor = position + len(fragment)
    return cursor <= len(html) - len(fragments[-1])


def compact_markup(value):
    return re.sub(r">\s+<", "><", value.strip())


def validate(html, blocks):
    errors = []

    def require(condition, code, message):
        if not condition:
            errors.append(f"{code}: {message}")

    require(
        matches_template_shell(html, blocks["page"]),
        "PAGE_SHELL",
        "la coque ne correspond pas au GABARIT-COMPLET",
    )
    require(
        '<nav class="fr-container" role="navigation" aria-label="Accès rapide">' in html,
        "SKIPLINKS_ROLE",
        "le rôle navigation des accès rapides manque",
    )
    if "L’essentiel" in html or "top-card" in html:
        require(
            '<section id="essentiel" class="fr-container section-block">' in html,
            "ESSENTIALS_STRUCTURE",
            "la section L’essentiel n’utilise pas le bloc canonique",
        )
        require(
            'class="top-grid fr-grid-row fr-grid-row--gutters"' in html,
            "TOP_GRID",
            "la grille L’essentiel n’utilise pas top-grid",
        )
        require(
            html.count('class="fr-card fr-card--shadow top-card"') == 3,
            "ESSENTIALS_CARD_COUNT",
            "L’essentiel doit contenir exactement trois cartes",
        )
    require(
        '<p class="section-number">00</p>' not in html,
        "SECTION_NUMBER_ZERO",
        "la numérotation doit commencer à 01",
    )
    numbers = [int(value) for value in re.findall(r'class="section-number">(\d{2})<', html)]
    require(
        numbers == list(range(1, len(numbers) + 1)),
        "SECTION_NUMBERS",
        "les numéros de section ne sont pas continus",
    )
    section_ids = set(re.findall(r'<section\b[^>]*\bid="([^"]+)"', html))
    allowed_section_ids = {"essentiel", "surveiller", *RUBRICS}
    unknown_section_ids = sorted(section_ids - allowed_section_ids)
    require(
        not unknown_section_ids,
        "UNKNOWN_RUBRIC_ID",
        "identifiants de rubrique non canoniques : "
        + ", ".join(unknown_section_ids),
    )
    for rubric_id, (_, _, muted) in RUBRICS.items():
        if f'id="{rubric_id}"' not in html:
            continue
        expected = f'<section id="{rubric_id}"' + (' class="section-muted">' if muted else ">")
        require(
            expected in html,
            f"RUBRIC_WRAPPER_{rubric_id.upper()}",
            f"l’enveloppe de la rubrique {rubric_id} n’est pas canonique",
        )
    require('id="fr-theme-modal"' in html, "THEME_MODAL", "le modal de thème manque")
    require(
        '<script type="module" src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.module.min.js"></script>'
        in html,
        "DSFR_MODULE",
        "le script DSFR module manque",
    )
    require(
        '<script nomodule src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.2/dist/dsfr.nomodule.min.js"></script>'
        in html,
        "DSFR_NOMODULE",
        "le script DSFR nomodule manque",
    )
    require(
        '<span class="fr-tag">' not in html,
        "NONINTERACTIVE_TAG",
        "un tag non interactif doit être un p.fr-tag",
    )
    require(not MARKER.search(html), "UNRESOLVED_MARKER", "un marqueur @@...@@ subsiste")
    require(html.count("<h1>") == 1, "H1_COUNT", "la page doit contenir un seul h1")
    return errors
