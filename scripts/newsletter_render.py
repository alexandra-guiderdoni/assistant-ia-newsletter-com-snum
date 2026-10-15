"""Rendu à partir des blocs HTML canoniques du kit V5.19."""

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
MARKER = re.compile(r"@@[^@\r\n]+@@")
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
SCHEMA_VERSION = "SNUM_PAQUET_RENDU_V519"
PACKET_FIELDS = {
    "schema_version",
    "edition_date",
    "edition_date_long",
    "window_start",
    "window_end",
    "articles",
    "watch",
}
ARTICLE_FIELDS = {
    "id",
    "rubric",
    "title",
    "source",
    "publication_date_iso",
    "publication_date_long",
    "url",
    "fact",
    "keywords",
    "takeaway",
    "snum_interest",
    "essential",
}
WEEKDAYS = "lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche"


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
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"URL HTTPS requise : {value}")
    return text(value)


def iso_date(value, label):
    value = str(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label} ISO invalide")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{label} ISO invalide") from error


def long_date(value, label, allow_weekday=False):
    prefix = rf"(?:(?:{WEEKDAYS}) )?" if allow_weekday else ""
    match = re.fullmatch(
        prefix
        + r"([1-9]|[12]\d|3[01]) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) (\d{4})",
        str(value),
    )
    if not match:
        raise ValueError(f"{label} longue invalide")
    day, month_name, year = match.groups()
    try:
        return date(int(year), FRENCH_MONTHS[month_name], int(day))
    except ValueError as error:
        raise ValueError(f"{label} longue invalide") from error


def publication_date(article, schema_version):
    iso_value = str(article["publication_date_iso"])
    long_value = str(article["publication_date_long"])
    parsed_iso = iso_date(iso_value, "date de publication")
    parsed_long = long_date(long_value, "date de publication")
    if parsed_long != parsed_iso:
        raise ValueError("dates de publication incohérentes")
    return long_value


def validate_packet(payload):
    if not isinstance(payload, dict):
        raise TypeError("objet JSON requis")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("schéma V5.19 requis")
    missing = sorted(PACKET_FIELDS - payload.keys())
    if missing:
        raise ValueError(f"champs paquet manquants : {', '.join(missing)}")
    unexpected = sorted(payload.keys() - PACKET_FIELDS)
    if unexpected:
        raise ValueError(f"champs paquet inattendus : {', '.join(unexpected)}")
    if not isinstance(payload["articles"], list) or not isinstance(
        payload["watch"], list
    ):
        raise TypeError("articles et watch doivent être des listes")

    edition = iso_date(payload["edition_date"], "date d’édition")
    edition_long = long_date(
        payload["edition_date_long"], "date d’édition", allow_weekday=True
    )
    if edition != edition_long:
        raise ValueError("dates d’édition incohérentes")
    window_start = iso_date(payload["window_start"], "borne basse")
    window_end = iso_date(payload["window_end"], "borne haute")
    if window_start > window_end:
        raise ValueError("fenêtre de collecte inversée")

    for article in payload["articles"]:
        if not isinstance(article, dict):
            raise TypeError("objet article requis")
        missing = sorted(ARTICLE_FIELDS - article.keys())
        if missing:
            raise ValueError(f"champs article manquants : {', '.join(missing)}")
        unexpected = sorted(article.keys() - ARTICLE_FIELDS)
        if unexpected:
            raise ValueError(f"champs article inattendus : {', '.join(unexpected)}")
        if not isinstance(article["id"], str) or not article["id"].strip():
            raise ValueError("id d’article textuel requis")
        for field in (
            "rubric",
            "title",
            "source",
            "publication_date_iso",
            "publication_date_long",
            "url",
            "fact",
            "takeaway",
            "snum_interest",
        ):
            if not isinstance(article[field], str) or not article[field].strip():
                raise ValueError(f"champ article textuel requis : {field}")
        if not isinstance(article["essential"], bool):
            raise TypeError("champ essential booléen requis")
        publication_date(article, SCHEMA_VERSION)
        published = iso_date(article["publication_date_iso"], "date de publication")
        if not window_start <= published <= window_end:
            raise ValueError("date de publication hors fenêtre")
        checked_url(article["url"])
        keywords = article["keywords"]
        if not isinstance(keywords, list) or not 3 <= len(keywords) <= 5:
            raise ValueError("un article doit contenir de 3 à 5 mots-clés")
        if any(
            not isinstance(keyword, str) or not keyword.strip() for keyword in keywords
        ):
            raise ValueError("mot-clé textuel requis")

    for item in payload["watch"]:
        if not isinstance(item, dict) or set(item) != {"title", "summary"}:
            raise ValueError("objet watch invalide")
        if any(
            not isinstance(item[field], str) or not item[field].strip()
            for field in item
        ):
            raise ValueError("champ watch textuel requis")


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
    required.update({"publication_date_iso", "publication_date_long"})
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
    validate_packet(payload)
    schema_version = payload.get("schema_version")
    articles = payload.get("articles", [])
    seen_ids = set()
    seen_urls = set()
    for article in articles:
        article_id = article.get("id")
        if article_id in seen_ids:
            raise ValueError(f"id d’article dupliqué : {article_id}")
        seen_ids.add(article_id)
        if article.get("rubric") not in RUBRICS:
            raise ValueError(f"rubrique inconnue : {article.get('rubric')}")
        article_url = article.get("url")
        if article_url in seen_urls:
            raise ValueError(f"URL d’article dupliquée : {article_url}")
        seen_urls.add(article_url)
    grouped = {rubric_id: [] for rubric_id in RUBRICS}
    for article in articles:
        grouped[article["rubric"]].append(article)

    essentials = [article for article in articles if article.get("essential")]
    if len(articles) >= 3 and len(essentials) != 3:
        raise ValueError(
            "exactement trois articles essentiels sont requis à partir de trois articles"
        )
    if len(articles) < 3 and essentials:
        raise ValueError("aucun article essentiel sous trois articles")
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
