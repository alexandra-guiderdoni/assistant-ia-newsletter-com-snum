"""Rendu à partir des blocs HTML qui restent canoniques dans le Markdown V5.16."""

import re
from datetime import date
from html import escape
from urllib.parse import urlparse

RUBRICS = {
    "numerique": ("Numérique", "NUMERIQUE", False),
    "ia": ("Intelligence artificielle", "INTELLIGENCE ARTIFICIELLE (IA)", True),
    "commande": ("Commande publique", "COMMANDE PUBLIQUE", False),
    "rh": ("Ressources humaines", "RESSOURCES HUMAINES", True),
    "bercy": ("Vie de Bercy", "VIE DE BERCY", False),
}
MARKER = re.compile(r"@@[A-Z_]+@@")
FRENCH_MONTHS = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12,
}


def canonical_blocks(markdown):
    blocks = re.findall(r"```html\n(.*?)\n```", markdown, re.DOTALL)

    def one(sentinel):
        matches = [block for block in blocks if sentinel in block]
        if len(matches) != 1:
            raise ValueError(f"bloc canonique introuvable ou ambigu : {sentinel}")
        return matches[0]

    return {
        "page": one("<!doctype html>"),
        "essential": one('id="essentiel"'),
        "rubric": one('id="@@ID_RUBRIQUE@@"'),
        "watch": one('id="surveiller"'),
        "empty": one("<h2>Collecte à compléter</h2>"),
    }


def fill(template, values):
    for name, value in values.items():
        template = template.replace(f"@@{name}@@", value)
    return template


def text(value):
    return escape(str(value), quote=True)


def checked_url(value):
    parsed = urlparse(str(value))
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"URL publique invalide : {value}")
    return text(value)


def publication_date(article, schema_version):
    if schema_version != "SNUM_PAQUET_RENDU_V518":
        return str(article["publication_date"])
    iso_value = str(article["publication_date_iso"])
    long_value = str(article["publication_date_long"])
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso_value):
        raise ValueError("date de publication ISO invalide")
    try:
        iso_date = date.fromisoformat(iso_value)
    except ValueError as error:
        raise ValueError("date de publication ISO invalide") from error
    long_match = re.fullmatch(
        r"([1-9]|[12]\d|3[01]) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) (\d{4})",
        long_value,
    )
    if not long_match:
        raise ValueError("date de publication longue invalide")
    day, month_name, year = long_match.groups()
    try:
        long_date = date(int(year), FRENCH_MONTHS[month_name], int(day))
    except ValueError as error:
        raise ValueError("date de publication longue invalide") from error
    if long_date != iso_date:
        raise ValueError("dates de publication incohérentes")
    return long_value


def article_values(article, rubric_title, schema_version):
    required = {
        "title",
        "source",
        "fact",
        "keywords",
        "takeaway",
        "snum_interest",
        "url",
    }
    if schema_version == "SNUM_PAQUET_RENDU_V518":
        required.update({"publication_date_iso", "publication_date_long"})
    else:
        required.add("publication_date")
    missing = sorted(required - article.keys())
    if missing:
        raise ValueError(f"champs article manquants : {', '.join(missing)}")
    for field, label, limit in (
        ("fact", "fait", 25),
        ("takeaway", "À retenir", 15),
        ("snum_interest", "Intérêt pour le SNUM", 15),
    ):
        if len(str(article[field]).split()) > limit:
            raise ValueError(f"{label} dépasse {limit} mots")
    keywords = article["keywords"]
    if not isinstance(keywords, list) or not 3 <= len(keywords) <= 5:
        raise ValueError("un article doit contenir de 3 à 5 mots-clés")
    return {
        "RUBRIQUE": rubric_title,
        "SOURCE_MAJUSCULES": text(str(article["source"]).upper()),
        "DATE_PUBLICATION_LONGUE_MAJUSCULES": text(
            publication_date(article, schema_version).upper()
        ),
        "TITRE": text(article["title"]),
        "FAIT": text(article["fact"]),
        "MOTS_CLES": " · ".join(text(keyword) for keyword in keywords),
        "A_RETENIR": text(article["takeaway"]),
        "INTERET_SNUM": text(article["snum_interest"]),
        "URL": checked_url(article["url"]),
    }


def render_essentials(template, articles, schema_version):
    card_pattern = re.compile(
        r'    <div class="fr-col-12 fr-col-md-4">.*?</article></div>', re.DOTALL
    )
    card = card_pattern.search(template)
    if not card:
        raise ValueError("carte essentielle canonique introuvable")
    rendered = []
    for article in articles:
        rubric_title = RUBRICS[article["rubric"]][1]
        rendered.append(
            fill(card.group(0), article_values(article, rubric_title, schema_version))
        )
    return card_pattern.sub("\n".join(rendered), template, count=1)


def render_rubric(template, rubric_id, articles, number, schema_version):
    article_pattern = re.compile(
        r'    <article class="fr-col-12">.*?\n    </article>', re.DOTALL
    )
    article_model = article_pattern.search(template)
    if not article_model:
        raise ValueError("article de rubrique canonique introuvable")
    title = RUBRICS[rubric_id][1]
    rendered_articles = [
        fill(article_model.group(0), article_values(article, title, schema_version))
        for article in articles
    ]
    section = article_pattern.sub("\n".join(rendered_articles), template, count=1)
    return fill(
        section,
        {
            "ID_RUBRIQUE": rubric_id,
            "SECTION_MUTED_ATTR": ' class="section-muted"'
            if RUBRICS[rubric_id][2]
            else "",
            "NUMERO": f"{number:02d}",
            "TITRE_RUBRIQUE": title,
        },
    )


def render_watch(template, watch_items, number):
    article_pattern = re.compile(r'<article class="fr-col-12">.*?</article>', re.DOTALL)
    article_model = article_pattern.search(template)
    if not article_model:
        raise ValueError("article À surveiller canonique introuvable")
    rendered = []
    for item in watch_items:
        rendered.append(
            fill(
                article_model.group(0),
                {
                    "TITRE_SUIVI": text(item["title"]),
                    "SUIVI_COURT": text(item["summary"]),
                },
            )
        )
    section = article_pattern.sub("".join(rendered), template, count=1)
    return fill(section, {"NUMERO": f"{number:02d}"})


def build(payload, blocks):
    schema_version = payload.get("schema_version")
    articles = payload.get("articles", [])
    for article in articles:
        if article.get("rubric") not in RUBRICS:
            raise ValueError(f"rubrique inconnue : {article.get('rubric')}")
    grouped = {rubric_id: [] for rubric_id in RUBRICS}
    for article in articles:
        grouped[article["rubric"]].append(article)

    essentials = [article for article in articles if article.get("essential")]
    if len(articles) >= 3 and len(essentials) != 3:
        raise ValueError(
            "exactement trois articles essentiels sont requis à partir de trois articles"
        )
    essential_html = (
        render_essentials(blocks["essential"], essentials, schema_version)
        if len(articles) >= 3
        else ""
    )
    number = 2 if essential_html else 1
    rubric_sections = []
    navigation = (
        ['<a class="fr-link" href="#essentiel">L’essentiel</a>']
        if essential_html
        else []
    )
    for rubric_id, rubric_articles in grouped.items():
        if not rubric_articles:
            continue
        navigation.append(
            f'<a class="fr-link" href="#{rubric_id}">{RUBRICS[rubric_id][0]}</a>'
        )
        rubric_sections.append(
            render_rubric(
                blocks["rubric"],
                rubric_id,
                rubric_articles,
                number,
                schema_version,
            )
        )
        number += 1

    watch_items = payload.get("watch", [])
    watch_html = (
        render_watch(blocks["watch"], watch_items, number) if watch_items else ""
    )
    if watch_html:
        navigation.append('<a class="fr-link" href="#surveiller">À surveiller</a>')
    empty_html = blocks["empty"] if not articles else ""
    page = fill(
        blocks["page"],
        {
            "DATE_EDITION": text(payload["edition_date_long"]),
            "DATE_EDITION_LONGUE": text(payload["edition_date_long"]),
            "DATE_EDITION_LONGUE_MAJUSCULES": text(
                str(payload["edition_date_long"]).upper()
            ),
            "NAVIGATION": "".join(navigation),
            "ESSENTIELS": essential_html,
            "RUBRIQUES": "\n".join(rubric_sections) or empty_html,
            "A_SURVEILLER": watch_html,
        },
    )
    remaining = sorted(set(MARKER.findall(page)))
    if remaining:
        raise ValueError(f"marqueurs non remplacés : {', '.join(remaining)}")
    return page + "\n"
