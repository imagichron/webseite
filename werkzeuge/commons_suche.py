"""Sucht freie Fotos (nur gemeinfrei / CC0) bei Wikimedia Commons und lädt Vorschaubilder.

Aufruf: python -I commons_suche.py <zielordner>
Schreibt je Motiv bis zu 6 Kandidaten als JPG (1200 px breit) und eine kandidaten.json mit Herkunft.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ziel = Path(sys.argv[1])
ziel.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (compatible; bildsuche-skript/1.0)"
API = "https://commons.wikimedia.org/w/api.php"

MOTIVE = {
    "kirche": "Bavarian church onion dome village",
    "torte": "wedding cake",
    "ringe": "wedding rings",
    "see": "Chiemsee sunset",
    "berge": "alpine meadow Bavaria mountains flowers",
    "auto": "Volkswagen Golf I",
    "garten": "garden party lanterns",
}
FREI = re.compile(r"^(cc0|public domain|pd\b|pd-|cc[ -]by[ -]\d(\.\d)?( de)?$)", re.I)   # CC BY ja, CC BY-SA nein


def holen(url, binaer=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read() if binaer else json.loads(r.read().decode("utf-8"))


if len(sys.argv) > 2:
    MOTIVE = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
alt = ziel / "kandidaten.json"
ergebnis = json.loads(alt.read_text(encoding="utf-8")) if alt.exists() else {}
for motiv, suche in MOTIVE.items():
    q = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": "6",
        "gsrsearch": suche + " filetype:bitmap", "gsrlimit": "40",
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": "1200",
    }
    daten = holen(API + "?" + urllib.parse.urlencode(q))
    seiten = sorted((daten.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 0))
    liste = []
    for p in seiten:
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lizenz = meta.get("LicenseShortName", {}).get("value", "")
        if not FREI.search(lizenz.strip()):
            continue
        if ii.get("mime") not in ("image/jpeg", "image/png") or ii.get("width", 0) < 1200 or ii.get("width", 0) < ii.get("height", 1):
            continue   # nur Querformat, groß genug
        name = f"{motiv}-{len(liste) + 1}.jpg"
        if any(k["titel"] == p["title"] for k in liste):
            continue
        try:
            (ziel / name).write_bytes(holen(ii["thumburl"], binaer=True))
        except Exception as f:
            print("  Fehler beim Laden:", f)
            continue
        urheber = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
        liste.append({"datei": name, "titel": p["title"], "lizenz": lizenz, "urheber": urheber,
                      "seite": ii.get("descriptionurl"), "groesse": f'{ii.get("width")}x{ii.get("height")}'})
        time.sleep(1.5)
        if len(liste) >= 6:
            break
    ergebnis[motiv] = liste
    print(f"{motiv}: {len(liste)} freie Kandidaten")
    (ziel / "kandidaten.json").write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(4)

(ziel / "kandidaten.json").write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
