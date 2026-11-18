"""Comparaison ponctuelle des deux consignes sur des extraits identiques."""
import datetime
import json
import runpy
import sys
from pathlib import Path
from unittest.mock import patch

from veille_snum import core, repecher

urls = json.loads(Path("recette-urls.json").read_text())
items = {}
for url in urls:
    source, address = repecher.source_publique(url)
    try:
        item = repecher.lire_candidat(address, source, datetime.date(2026, 11, 13),
                                     datetime.date(2026, 11, 17), core.HttpClient())
    except repecher.Refus as error:
        print("Lecture refusée", url, str(error), flush=True)
        continue
    items.setdefault(source["id"], []).append(item)

def replay(source, *args, **kwargs):
    found = items.get(source["id"], [])
    return found, [], {"id": source["id"], "label": source["label"],
                       "status": "checked" if found else "skipped_internal"}

params = {"edition_date": "2026-11-17", "window_start": "2026-11-13", "window_end": "2026-11-17"}
previous = Path("consigne-temoin.txt").read_text()
with patch.object(core, "discover_source", replay):
    with patch.object(core, "ALBERT_PROMPT", previous):
        report = core.collect(params)
        print("TÉMOIN", json.dumps({k: report[k] for k in ("errors","excluded")}), flush=True)
        print("TÉMOIN RETENUS", [(a["url"],a["rubric"]) for a in (report["packet"] or {}).get("articles", [])], flush=True)
    runpy.run_module("veille_snum.publier", run_name="__main__")
