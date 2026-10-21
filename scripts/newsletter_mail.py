"""Construit et compare le courriel DSFR ; les données ne pilotent que les valeurs."""

# PDG-LARGE-FILE-JUSTIFICATION: CLI du canal mail, rendu et comparaison du même canon.

import argparse
import json
import re
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path

from newsletter_render import FRENCH_MONTHS, validate_packet

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "_source/30-BLOCS-MAIL-DSFR.md"
MARKER = re.compile(r"@@([A-Z_]+)@@")
LABELS = {
    "numerique": "Numérique",
    "ia": "Intelligence artificielle (IA)",
    "commande": "Commande publique",
    "rh": "Ressources humaines",
    "bercy": "Bercy",
}


def blocks(path=SOURCE):
    return dict(
        re.findall(
            r"^## ([A-Z_]+)\n\n```html\n(.*?)\n```",
            path.read_text(),
            re.MULTILINE | re.DOTALL,
        )
    )


def packet(path):
    value = path.read_text(encoding="utf-8")
    if "SNUM_PAQUET_RENDU_V519_START" in value:
        value = value.split("SNUM_PAQUET_RENDU_V519_START", 1)[1].split(
            "SNUM_PAQUET_RENDU_V519_END", 1
        )[0]
    return json.loads(value)


def fill(template, values):
    return MARKER.sub(lambda match: values[match[1]], template)


def text(value):
    value = escape(str(value), quote=True)
    value = re.sub(r" ([;:!?%])", r"&nbsp;\1", value)
    value = re.sub(r"(\d) (\d{3}\b)", r"\1&nbsp;\2", value)
    return value.replace("@@", "&#64;&#64;")


def long_date(value):
    day = date.fromisoformat(value)
    return f"{day.day} {list(FRENCH_MONTHS)[day.month - 1]} {day.year}"


def build(payload, canon=None):
    validate_packet(payload, allow_outside_window=True)
    canon = blocks() if canon is None else canon
    articles = payload["articles"]
    if len({a["id"] for a in articles}) != len(articles):
        raise ValueError("identifiant d’article dupliqué")
    if len({a["url"] for a in articles}) != len(articles):
        raise ValueError("URL d’article dupliquée")
    if any(a["rubric"] not in LABELS for a in articles):
        raise ValueError("rubrique inconnue")
    groups = {}
    for article in articles:
        groups.setdefault(article["rubric"], []).append(article)
    sections = []
    for number, (rubric, entries) in enumerate(groups.items(), 1):
        rows = []
        for article in entries:
            values = {
                "ID": article["id"],
                "URL": article["url"],
                "TITLE": article["title"],
                "SOURCE": article["source"],
                "DATE_ISO": article["publication_date_iso"],
                "DATE_LONG": article["publication_date_long"],
                "FACT": article["fact"],
                "TAKEAWAY": article["takeaway"],
                "INTEREST": article["snum_interest"],
            }
            values = {name: text(value) for name, value in values.items()}
            values["KEYWORDS"] = " · ".join(text(word) for word in article["keywords"])
            values["ESSENTIAL"] = canon["ESSENTIAL"] if article["essential"] else ""
            rows.append(fill(canon["ARTICLE"], values))
        sections.append(
            fill(
                canon["RUBRIC"],
                {
                    "NUMBER": f"{number:02d}",
                    "LABEL": LABELS[rubric],
                    "ARTICLES": "\n".join(rows),
                },
            )
        )
    count = len(articles)
    essentials = sum(a["essential"] for a in articles)
    intro = "Aucun article sélectionné."
    if count:
        article_label = "article sélectionné" if count == 1 else "articles sélectionnés"
        essential_label = "essentiel" if essentials == 1 else "essentiels"
        intro = (
            f"Veille du {long_date(payload['window_start'])} au {long_date(payload['window_end'])}"
            f" · {count} {article_label}, dont {essentials} {essential_label}."
        )
    return fill(
        canon["PAGE"],
        {
            "EDITION_LONG": text(payload["edition_date_long"]),
            "LOGO": canon["LOGO"],
            "INTRO": text(intro),
            "RUBRICS": "\n".join(sections) if articles else canon["EMPTY"],
            "WATCH": "",
        },
    )


class Shape(HTMLParser):
    """Compare la structure, les textes et attributs sans imposer l’indentation."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.events = []
        self.raw = None
        self.feed(source)
        self.close()

    def trim_block_edge(self):
        if self.events and self.events[-1][0] == "text":
            value = self.events[-1][1].rstrip()
            if value:
                self.events[-1] = ("text", value)
            else:
                self.events.pop()

    def handle_starttag(self, tag, attrs):
        if tag in {
            "html",
            "head",
            "body",
            "div",
            "table",
            "tr",
            "td",
            "p",
            "h1",
            "h2",
            "h3",
        }:
            self.trim_block_edge()
        normalized = []
        for name, value in attrs:
            if name == "style":
                value = re.sub(r"\s*([:;,{}])\s*", r"\1", value.strip())
            normalized.append((name, value))
        self.events.append(("open", tag, sorted(normalized)))
        if tag in {"style", "script"}:
            self.raw = tag

    def handle_endtag(self, tag):
        if tag in {
            "html",
            "head",
            "body",
            "div",
            "table",
            "tr",
            "td",
            "p",
            "h1",
            "h2",
            "h3",
        }:
            self.trim_block_edge()
        self.events.append(("close", tag))
        self.raw = None

    def handle_data(self, value):
        if self.raw:
            value = re.sub(r"\s*([:;,{}])\s*", r"\1", value.strip())
        else:
            value = re.sub(r"\s+", " ", value)
            previous = self.events[-1] if self.events else ()
            inline = {"a", "span", "strong", "time", "em"}
            if not value.strip() and not (previous and previous[1] in inline):
                value = ""
            elif previous and previous[0] == "open" and previous[1] not in inline:
                value = value.lstrip()
        if value:
            self.events.append(("text", value))

    def handle_comment(self, value):
        if value.strip().startswith("[if"):
            self.events.append(("mso", re.sub(r"\s+", " ", value).strip()))

    def handle_decl(self, value):
        self.events.append(("declaration", value.lower()))


def verify(payload, candidate):
    expected = build(payload)
    if not re.search(r"</html>\s*\Z", candidate, re.IGNORECASE):
        return ["HTML_MAIL_INCOMPLET : fermeture absente ou contenu après le document"]
    if Shape(expected).events == Shape(candidate).events:
        return []
    return [
        "MAIL_CANON_MODIFIE : structure, contenu, style, logo ou attributs différents du canon"
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "verify"])
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--html", type=Path)
    args = parser.parse_args()
    payload = packet(args.input)
    if args.command == "build":
        if args.output is None:
            parser.error("--output requis")
        args.output.write_text(build(payload), encoding="utf-8")
    else:
        if args.html is None:
            parser.error("--html requis")
        errors = verify(payload, args.html.read_text(encoding="utf-8"))
        if errors:
            raise ValueError("; ".join(errors))
        print("HTML_MAIL_DSFR_CANONIQUE_OK")


if __name__ == "__main__":
    main()
