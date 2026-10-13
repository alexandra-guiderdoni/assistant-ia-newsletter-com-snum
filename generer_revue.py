"""Valide la sortie éditoriale DINUM et génère les livrables SNUM."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

# PDG-LARGE-FILE-JUSTIFICATION: point d’entrée autonome sans dépendance, qui garde ensemble contrat, validation et rendu du seul format SNUM.

VERSION = "snum-v5.6"
TEMPLATE_SHA256 = "749d682af63910fbf618328e693714e056e4726c758dd770cd9096390ee9a431"
ROOT_KEYS = {
    "version",
    "date_edition",
    "date_debut_collecte",
    "date_fin_collecte",
    "etat_assistant",
    "evenements",
    "essentiels",
    "a_surveiller",
    "collecte",
    "limites",
}
EVENT_KEYS = {
    "id",
    "rubrique",
    "titre",
    "fait",
    "mots_cles",
    "a_retenir",
    "interet_snum",
    "titre_original",
    "source",
    "date_publication",
    "url",
    "lecture",
    "preuve_lecture",
}
COLLECT_KEYS = {"domaines_consultes", "requetes", "exclusions"}
EXCLUSION_KEYS = {"url", "raison"}
RUBRICS = {
    "NUMERIQUE": ("numerique", "NUMERIQUE"),
    "INTELLIGENCE_ARTIFICIELLE_IA": ("ia", "INTELLIGENCE ARTIFICIELLE (IA)"),
    "COMMANDE_PUBLIQUE": ("commande", "COMMANDE PUBLIQUE"),
    "RESSOURCES_HUMAINES": ("rh", "RESSOURCES HUMAINES"),
    "VIE_DE_BERCY": ("bercy", "VIE DE BERCY"),
}
READING_VALUES = {"INTEGRAL_LU", "INTEGRAL_FOURNI"}
WEEKDAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MONTHS = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]
EMOJI = re.compile("[\U0001f000-\U0001faff\U00002600-\U000027bf]")


class ValidationError(Exception):
    """Erreur de contrat destinée à être lue par l’utilisatrice."""


def fail(message: str) -> None:
    raise ValidationError(message)


def extract_json(raw: str) -> dict:
    stripped = raw.strip()
    fenced = re.fullmatch(
        r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.DOTALL | re.IGNORECASE
    )
    payload = fenced.group(1) if fenced else stripped
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"JSON invalide à la ligne {exc.lineno}, colonne {exc.colno} : {exc.msg}")
    if not isinstance(data, dict):
        fail("La racine JSON doit être un objet.")
    return data


def exact_keys(value: dict, expected: set[str], location: str) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing or extra:
        fail(f"{location} : clés manquantes {missing} ; clés interdites {extra}.")


def parse_date(value: object, location: str) -> date:
    if not isinstance(value, str):
        fail(f"{location} doit être une date AAAA-MM-JJ.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        fail(f"{location} doit être une date réelle au format AAAA-MM-JJ.")


def text(value: object, location: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        fail(f"{location} doit être une chaîne non vide.")
    if "<" in value or ">" in value or EMOJI.search(value):
        fail(f"{location} contient du HTML ou un pictogramme interdit.")
    return value.strip()


def string_list(value: object, location: str) -> list[str]:
    if not isinstance(value, list):
        fail(f"{location} doit être une liste.")
    return [text(item, f"{location}[{index}]") for index, item in enumerate(value)]


def word_count(value: str) -> int:
    return len(value.split())


def validate_url(value: object, location: str, *, allow_empty: bool = False) -> str:
    url = text(value, location, allow_empty=allow_empty)
    if not url and allow_empty:
        return url
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{location} doit être une URL publique HTTPS exacte.")
    return url


def validate(data: dict) -> dict:
    exact_keys(data, ROOT_KEYS, "racine")
    if data["version"] != VERSION:
        fail(f"version doit valoir {VERSION}.")
    if data["etat_assistant"] != "A_COMPLETER":
        fail("etat_assistant doit rester A_COMPLETER.")

    edition = parse_date(data["date_edition"], "date_edition")
    start = parse_date(data["date_debut_collecte"], "date_debut_collecte")
    end = parse_date(data["date_fin_collecte"], "date_fin_collecte")
    if not start <= end <= edition:
        fail("La fenêtre doit respecter début <= fin <= date d’édition.")

    events = data["evenements"]
    if not isinstance(events, list):
        fail("evenements doit être une liste.")
    ids: set[str] = set()
    urls: set[str] = set()
    for index, event in enumerate(events):
        location = f"evenements[{index}]"
        if not isinstance(event, dict):
            fail(f"{location} doit être un objet.")
        exact_keys(event, EVENT_KEYS, location)
        event_id = text(event["id"], f"{location}.id")
        if not re.fullmatch(r"E\d{2,}", event_id) or event_id in ids:
            fail(f"{location}.id doit être unique et suivre E01, E02, etc.")
        ids.add(event_id)
        if event["rubrique"] not in RUBRICS:
            fail(f"{location}.rubrique est interdite.")
        for field in ("titre", "titre_original", "source", "preuve_lecture"):
            text(event[field], f"{location}.{field}")
        for field, maximum in (("fait", 25), ("a_retenir", 15), ("interet_snum", 15)):
            value = text(event[field], f"{location}.{field}")
            count = word_count(value)
            if count > maximum:
                fail(f"{location}.{field} contient {count} mots, maximum {maximum}.")
        keywords = string_list(event["mots_cles"], f"{location}.mots_cles")
        if not 3 <= len(keywords) <= 5 or len(set(map(str.casefold, keywords))) != len(
            keywords
        ):
            fail(f"{location}.mots_cles doit contenir 3 à 5 valeurs distinctes.")
        published = parse_date(
            event["date_publication"], f"{location}.date_publication"
        )
        if not start <= published <= end:
            fail(f"{location}.date_publication est hors fenêtre.")
        url = validate_url(event["url"], f"{location}.url")
        if url in urls:
            fail(f"{location}.url duplique un autre événement.")
        urls.add(url)
        if event["lecture"] not in READING_VALUES:
            fail(f"{location}.lecture doit valoir INTEGRAL_LU ou INTEGRAL_FOURNI.")

    essentials = data["essentiels"]
    if not isinstance(essentials, list) or not all(
        isinstance(item, str) for item in essentials
    ):
        fail("essentiels doit être une liste d’identifiants.")
    expected = 3 if len(events) >= 3 else 0
    if len(essentials) != expected or len(set(essentials)) != len(essentials):
        fail(
            f"essentiels doit contenir exactement {expected} identifiant(s) distinct(s)."
        )
    if not set(essentials) <= ids:
        fail("essentiels référence un événement absent.")

    data["a_surveiller"] = string_list(data["a_surveiller"], "a_surveiller")
    for index, item in enumerate(data["a_surveiller"]):
        if word_count(item) > 25:
            fail(f"a_surveiller[{index}] dépasse 25 mots.")
    data["limites"] = string_list(data["limites"], "limites")

    collect = data["collecte"]
    if not isinstance(collect, dict):
        fail("collecte doit être un objet.")
    exact_keys(collect, COLLECT_KEYS, "collecte")
    for key in ("domaines_consultes", "requetes"):
        collect[key] = string_list(collect[key], f"collecte.{key}")
    exclusions = collect["exclusions"]
    if not isinstance(exclusions, list):
        fail("collecte.exclusions doit être une liste.")
    for index, exclusion in enumerate(exclusions):
        location = f"collecte.exclusions[{index}]"
        if not isinstance(exclusion, dict):
            fail(f"{location} doit être un objet.")
        exact_keys(exclusion, EXCLUSION_KEYS, location)
        validate_url(exclusion["url"], f"{location}.url", allow_empty=True)
        text(exclusion["raison"], f"{location}.raison")
    if not events and (
        not collect["domaines_consultes"] or not collect["requetes"] or not exclusions
    ):
        fail("Une collecte vide doit documenter domaines, requêtes et exclusions.")
    return data


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def long_date(value: str, *, weekday: bool = False) -> str:
    parsed = date.fromisoformat(value)
    core = f"{parsed.day} {MONTHS[parsed.month - 1]} {parsed.year}"
    return f"{WEEKDAYS[parsed.weekday()]} {core}" if weekday else core


def event_card(event: dict) -> str:
    _, rubric_title = RUBRICS[event["rubrique"]]
    keywords = " · ".join(map(escape, event["mots_cles"]))
    return f'''<div class="fr-col-12 fr-col-md-4"><article class="fr-card fr-card--shadow top-card"><div class="fr-card__body"><div class="fr-card__content"><div class="fr-card__start"><ul class="fr-tags-group"><li><p class="fr-tag">{escape(rubric_title)}</p></li></ul></div><p class="meta">{escape(event["source"].upper())} · {escape(long_date(event["date_publication"]).upper())}</p><h3 class="fr-card__title">{escape(event["titre"])}</h3><p class="fr-card__desc"><span class="summary-text">{escape(event["fait"])}</span><br><strong>Mots-clés :</strong> <span class="keywords">{keywords}</span></p><p class="takeaway"><strong>À retenir :</strong> {escape(event["a_retenir"])}</p><p class="impact"><strong>Intérêt pour le SNUM :</strong> {escape(event["interet_snum"])}</p><div class="fr-card__end"><a class="fr-link fr-link--icon-right fr-icon-external-link-line" href="{escape(event["url"])}" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : {escape(event["titre"])} - nouvelle fenêtre</span></a></div></div></div></article></div>'''


def article(event: dict) -> str:
    keywords = " · ".join(map(escape, event["mots_cles"]))
    return f'''<article class="fr-col-12"><div class="article-body"><p class="meta">{escape(event["source"].upper())} · {escape(long_date(event["date_publication"]).upper())}</p><h3>{escape(event["titre"])}</h3><p class="summary"><span class="summary-text">{escape(event["fait"])}</span><br><strong>Mots-clés :</strong> <span class="keywords">{keywords}</span></p><p class="takeaway"><strong>À retenir :</strong> {escape(event["a_retenir"])}</p><p class="snum"><strong>Intérêt pour le SNUM :</strong> {escape(event["interet_snum"])}</p></div><a class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-external-link-line source-btn" href="{escape(event["url"])}" target="_blank" rel="noopener noreferrer">Lire la source<span class="fr-sr-only"> : {escape(event["titre"])} - nouvelle fenêtre</span></a></article>'''


def render_html(data: dict, template: str) -> str:
    events_by_id = {event["id"]: event for event in data["evenements"]}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for event in data["evenements"]:
        grouped[event["rubrique"]].append(event)

    navigation: list[str] = []
    if data["essentiels"]:
        navigation.append('<a class="fr-link" href="#essentiel">L’essentiel</a>')
    for rubric, (rubric_id, rubric_title) in RUBRICS.items():
        if grouped[rubric]:
            navigation.append(
                f'<a class="fr-link" href="#{rubric_id}">{escape(rubric_title.title())}</a>'
            )
    if data["a_surveiller"]:
        navigation.append('<a class="fr-link" href="#surveiller">À surveiller</a>')

    essential = ""
    section_number = 1
    if data["essentiels"]:
        cards = "".join(
            event_card(events_by_id[event_id]) for event_id in data["essentiels"]
        )
        essential = f'<section id="essentiel" class="fr-container section-block"><div class="section-title"><p class="section-number">01</p><div><h2>L’essentiel</h2></div></div><div class="top-grid fr-grid-row fr-grid-row--gutters">{cards}</div></section>'
        section_number = 2

    rubric_sections: list[str] = []
    visible_index = 0
    for rubric, (rubric_id, rubric_title) in RUBRICS.items():
        if not grouped[rubric]:
            continue
        background = ' class="section-muted"' if visible_index % 2 else ""
        items = "".join(article(event) for event in grouped[rubric])
        rubric_sections.append(
            f'<section id="{rubric_id}"{background}><div class="fr-container section-block"><div class="section-title"><p class="section-number">{section_number:02d}</p><div><h2>{escape(rubric_title)}</h2></div></div><div class="article-list fr-grid-row">{items}</div></div></section>'
        )
        section_number += 1
        visible_index += 1

    watch = ""
    if data["a_surveiller"]:
        items = "".join(f"<li>{escape(item)}</li>" for item in data["a_surveiller"])
        watch = f'<section id="surveiller" class="section-muted"><div class="fr-container section-block"><div class="watch"><h2>À surveiller</h2><ul>{items}</ul></div></div></section>'

    replacements = {
        "{{DATE_EDITION}}": long_date(data["date_edition"]),
        "{{DATE_EDITION_LONGUE}}": long_date(data["date_edition"], weekday=True),
        "{{DATE_EDITION_LONGUE_MAJUSCULES}}": long_date(
            data["date_edition"], weekday=True
        ).upper(),
        "{{DATE_DEBUT_COLLECTE}}": long_date(data["date_debut_collecte"]),
        "{{DATE_FIN_COLLECTE}}": long_date(data["date_fin_collecte"]),
        "@@NAVIGATION@@": "\n          ".join(navigation),
        "@@ESSENTIEL@@": essential,
        "@@RUBRIQUES@@": "\n    ".join(rubric_sections),
        "@@A_SURVEILLER@@": watch,
    }
    result = template
    for marker, value in replacements.items():
        result = result.replace(marker, value)
    forbidden = ("{{", "}}", "@@", "example.invalid", "EMPLACEMENT_")
    if any(marker in result for marker in forbidden):
        fail("Le gabarit rendu contient encore un marqueur technique.")
    if result.count("<h1") != 1 or result.count('class="fr-skiplinks"') != 1:
        fail("Le contrôle structurel du h1 ou des accès rapides a échoué.")
    for required in (
        'href="#main"',
        'href="#navigation"',
        'href="#footer"',
        'id="footer"',
        "Accessibilité : non conforme",
        "Mentions légales",
        "Données personnelles",
        "Gestion des cookies",
        "Plan du site",
        "Archives",
        'type="module"',
        "nomodule",
        'id="fr-theme-modal"',
    ):
        if required not in result:
            fail(f"Le gabarit rendu a perdu l’élément obligatoire : {required}")
    if "span.fr-tag" in result:
        fail("Le gabarit contient un tag DSFR invalide.")
    return result


def render_markdown(data: dict) -> str:
    by_id = {event["id"]: event for event in data["evenements"]}
    lines = [
        f"# Revue de presse du SNUM - {long_date(data['date_edition'])}",
        "",
        f"Période de collecte : {long_date(data['date_debut_collecte'])} - {long_date(data['date_fin_collecte'])}.",
        "",
    ]
    if data["essentiels"]:
        lines.extend(["## L’essentiel", ""])
        for event_id in data["essentiels"]:
            lines.extend(render_event_markdown(by_id[event_id], level=3))
    for rubric, (_, rubric_title) in RUBRICS.items():
        events = [event for event in data["evenements"] if event["rubrique"] == rubric]
        if not events:
            continue
        lines.extend([f"## {rubric_title}", ""])
        for event in events:
            lines.extend(render_event_markdown(event, level=3))
    if data["a_surveiller"]:
        lines.extend(
            ["## À surveiller", ""]
            + [f"- {item}" for item in data["a_surveiller"]]
            + [""]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_event_markdown(event: dict, *, level: int) -> list[str]:
    prefix = "#" * level
    return [
        f"{prefix} {event['titre']}",
        "",
        event["fait"],
        "",
        f"**Mots-clés :** {' · '.join(event['mots_cles'])}",
        "",
        f"**À retenir :** {event['a_retenir']}",
        "",
        f"**Intérêt pour le SNUM :** {event['interet_snum']}",
        "",
        f"**Source :** [{event['source']} - {event['titre_original']}]({event['url']}), {long_date(event['date_publication'])}.",
        "",
    ]


def render_private_report(data: dict) -> str:
    lines = [
        f"# Dossier privé - {data['date_edition']}",
        "",
        "État : `A_COMPLETER`.",
        "",
        f"Fenêtre : {data['date_debut_collecte']} au {data['date_fin_collecte']}.",
        f"Événements validés par le générateur : {len(data['evenements'])}.",
        "",
        "## Preuves déclarées par l’Assistant DINUM",
        "",
    ]
    for event in data["evenements"]:
        lines.append(
            f"- {event['id']} - {event['source']}, {event['date_publication']}, `{event['lecture']}` : {event['preuve_lecture']}"
        )
    lines.extend(["", "## Collecte", ""])
    lines.extend(
        f"- Domaine : {item}" for item in data["collecte"]["domaines_consultes"]
    )
    lines.extend(f"- Requête : {item}" for item in data["collecte"]["requetes"])
    lines.extend(["", "## Exclusions", ""])
    lines.extend(
        f"- {item['url'] or 'URL non obtenue'} : {item['raison']}"
        for item in data["collecte"]["exclusions"]
    )
    lines.extend(["", "## Limites", ""])
    lines.extend(f"- {item}" for item in data["limites"])
    lines.extend(
        [
            "",
            "## Contrôles déterministes",
            "",
            "- Schéma JSON, dates, rubriques, identifiants, URLs et preuves renseignées : validés.",
            "- Limites de mots, nombre de mots-clés et trois essentiels : validés.",
            "- Structure HTML, accès rapides, footer, dialogue et scripts DSFR : validés.",
            "- Accès public réel, lecture intégrale et exactitude des faits : non vérifiés par le générateur.",
            "- Audit RGAA complet et contrôle visuel à 200 % : non exécutés.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Génère la revue SNUM depuis la sortie JSON de DINUM."
    )
    parser.add_argument(
        "entree",
        type=Path,
        help="Fichier JSON ou réponse DINUM copiée dans un fichier texte.",
    )
    parser.add_argument(
        "--sortie", type=Path, default=Path.cwd(), help="Dossier parent des livrables."
    )
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    template_path = script_dir / "gabarit-loic.html"
    try:
        raw = args.entree.read_text(encoding="utf-8")
        data = validate(extract_json(raw))
        template = template_path.read_text(encoding="utf-8")
        actual_hash = hashlib.sha256(template.encode()).hexdigest()
        if actual_hash != TEMPLATE_SHA256:
            fail(
                "Le gabarit Loïc a été modifié sans mise à jour contrôlée du générateur."
            )
        output_dir = args.sortie / f"livrable-{data['date_edition']}"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"revue-snum-{data['date_edition']}.md").write_text(
            render_markdown(data), encoding="utf-8"
        )
        (output_dir / f"dossier-prive-{data['date_edition']}.md").write_text(
            render_private_report(data), encoding="utf-8"
        )
        if data["evenements"]:
            rendered = render_html(data, template)
            (output_dir / f"revue-snum-{data['date_edition']}.html").write_text(
                rendered, encoding="utf-8"
            )
        (output_dir / "source-dinum.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except (OSError, ValidationError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 1
    print(f"Livrables créés dans : {output_dir}")
    if not data["evenements"]:
        print("Aucun HTML créé : la collecte ne contient aucun événement admissible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
