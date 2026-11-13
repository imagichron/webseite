# Webseite imagichron.de

Die öffentliche Seite, die **Imagichron** vorstellt und den Download anbietet. Hier liegt **nur die Webseite**: kein Programmcode und nichts Privates. Der Programmcode liegt in einem privaten Repo.

Design „E“ (Mischung aus „Nachtlicht“ und „Zeitstrahl“), hell voreingestellt, mit Umschalter hell/dunkel. Hintergrund und Entscheidungen: `docs/WEBSEITE.md` im privaten Imagichron-Repo.

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite |
| `impressum.html`, `datenschutz.html` | Pflichtangaben. **Platzhalter in eckigen Klammern** müssen vor dem Veröffentlichen ersetzt sein. |
| `nutzungsbedingungen.html`, `datenschutz-programm.html` | **Erzeugt**, nicht hier ändern: Quelle in `imagiter/docs/NUTZUNGSBEDINGUNGEN-ENTWURF.md` und `DATENSCHUTZ-PROGRAMM-ENTWURF.md`, neu erzeugen mit `uv run python werkzeuge/rechtstexte.py --webseite ../imagiter-webseite` (im Imagichron-Ordner). Kopf und Fuß kommen aus `datenschutz.html`: nach Menüänderungen dort neu erzeugen. |
| `404.html` | Seite für falsche Adressen |
| `windows-warnung.html` | Anleitung, falls Windows (SmartScreen) beim Setup warnt; von der Download-Karte verlinkt. |
| `beta.html`, `fragebogen.js` | Beta-Test: Anleitung und Fragebogen. Der Fragebogen öffnet das E-Mail-Programm mit den Antworten an kontakt@imagichron.de (kein fremder Dienst, die Seite sendet nichts). **Absichtlich nicht im Menü und mit `noindex`**, solange die Beta geschlossen ist: der Link geht mit der Einladung raus. Für eine offene Beta: Menüpunkt auf allen Seiten ergänzen, `noindex` entfernen und in `sitemap.xml` eintragen. |
| `robots.txt`, `sitemap.xml`, `llms.txt` | Für Suchmaschinen und KI-Suchen. Alle Crawler erlaubt, auch KI-Training (entschieden 11.11.2026). `sitemap.xml` enthält nur Seiten ohne `noindex`; bei Änderungen `lastmod` anpassen. `llms.txt` beschreibt Imagichron in einfachen Worten, bei neuen Funktionen oder Preisen mitpflegen. Strukturierte Daten (JSON-LD: Programm und Fragen) stehen im `<head>` von `index.html`; die Fragen dort müssen zu den sichtbaren „Fragen“ passen. |
| `style.css` | gesamtes Aussehen; Farben für hell und dunkel stehen oben als Variablen |
| `app.js` | Hell/Dunkel, Laufband, Einblenden, Bilder vergrößern, Download-Knopf |
| `bilder/` | Favicon (`favicon.svg`, auch das Logo oben links) und `apple-touch-icon.png` – beide aus `marke/` im Imagichron-Repo (`werkzeuge/icons_bauen.py`), dort ändern und hierher kopieren; Bildschirmfotos (WebP): `trailer`, `jahresseite`, `handy`, `studio`, `quiz` |
| `werkzeuge/commons_suche.py`, `werkzeuge/aufnahmen.ps1` | freie Fotos suchen und Bildschirmfotos aufnehmen (siehe unten) |
| `schriften/` | Josefin Sans für den Logo-Schriftzug (SIL Open Font License, Lizenztext liegt bei) – aus `marke/schrift/` im Imagichron-Repo |
| `CNAME` | eigene Adresse `imagichron.de` für GitHub Pages |
| `_config.yml` | GitHub Pages (Jekyll) kopiert die Dateien unverändert, lässt aber `README.md` und `werkzeuge/` weg (interne Dateien nicht veröffentlichen) |
| `modus.js` | setzt Hell/Dunkel vor dem Zeichnen (eigene Datei, weil die Seiten per Content-Security-Policy nur Skripte aus eigenen Dateien erlauben) |
| `bilder/teilen.jpg` | Vorschaubild beim Teilen des Links (WhatsApp, Facebook; 1200 × 630) |
| `werkzeuge/commit_pruefung.py`, `.githooks/` | Prüfung vor jedem Commit (Kopie aus Imagichron, gleich halten) |

**Menü auf allen Seiten gleich:** Kommt ein neuer Abschnitt oder Menüpunkt dazu, das Hauptmenü in `index.html`, `impressum.html`, `datenschutz.html` und `404.html` anpassen (Unterseiten verlinken mit `index.html#…`, die 404-Seite mit `/index.html#…`).

Grundsätze: einfaches HTML/CSS/JavaScript, **nichts von fremden Servern** (keine Google-Schriften, keine Statistik, keine Cookies).

## Beispielbilder

Die Bildschirmfotos zeigen das **echte Programm** mit der **erfundenen** Beispiel-Zeitreise „40 Jahre Anna & Paul“ (`beispiele/hochzeitstag` im Imagichron-Repo). Die Fotos darin sind **frei lizenzierte Aufnahmen aus Wikimedia Commons**, nur CC0, gemeinfrei oder CC BY (kein CC BY-SA, das würde auch für unsere Bildschirmfotos gelten), und **ohne erkennbare Personen** (Recht am eigenen Bild). Urheber und Lizenz stehen im **Impressum unter „Bildnachweis“**. Wer ein Foto austauscht, muss diesen Nachweis anpassen.

| Jahr | Foto | Lizenz |
|---|---|---|
| 1985 | Kirche St. Peter und Paul, Oberammergau (Jebulon) | CC0 |
| 1985 | Zwei goldene Eheringe (Rgaudin) | CC0 |
| 1986 | Chiemsee bei Chieming (Bananenfalter) | CC0 |
| 1986 | „Alpine Meadow“ (Dana Hutchinson) | CC BY 3.0 |
| 1987 | Hochzeitstorte (Leon Brooks) | gemeinfrei, in keinem Bildschirmfoto sichtbar |
| 1987 | Lampions (Chris Phutully) | CC BY 2.0, in keinem Bildschirmfoto sichtbar |

So entstehen die Bilder neu:
1. `python -I werkzeuge/commons_suche.py <Ordner>` lädt Kandidaten (nur freie Lizenzen, Querformat) und schreibt Urheber und Lizenz in `kandidaten.json`.
2. Eine Kopie der Beispiel-Zeitreise anlegen und die gewählten Fotos als `fotos` der Jahre eintragen.
3. Vorschau (Port 8071) und Studio (Port 8072) dieser Kopie starten sowie einen Dateiserver für den Arbeitsordner (Port 8073). Dann `werkzeuge/aufnahmen.ps1` ausführen. Es nutzt einen **eigenen** unsichtbaren Edge (Port 9351), nicht den gemeinsamen Testbrowser, und braucht `cdp-eigen.ps1` (Kopie von `tests/browser/cdp.ps1` aus Imagichron mit Port 9351 und eigenem Profil).
4. Das Skript speichert die Bilder als WebP (Qualität 0,84, höchstens 1440 bzw. 1600 px breit) nach `bilder/`.

## Ansehen auf dem eigenen Rechner

`index.html` doppelt anklicken. Der Download-Knopf zeigt dort immer „Demnächst“, weil der Browser bei lokal geöffneten Dateien keine `download.json` liest.

## Download freischalten (wenn es eine Installationsdatei gibt)

1. In diesem Repo auf GitHub ein **Release** anlegen (z. B. `v1.0.0`) und die Installationsdatei anhängen.
2. Prüfsumme berechnen (PowerShell): `Get-FileHash .\Imagichron-Setup-1.0.0.exe -Algorithm SHA256`
3. Neben `index.html` eine Datei `download.json` anlegen:

```json
{
  "version": "1.0.0",
  "datum": "1. März 2027",
  "groesse": "85 MB",
  "link": "https://github.com/imagichron/webseite/releases/download/v1.0.0/Imagichron-Setup-1.0.0.exe",
  "sha256": "…"
}
```

4. Committen und hochladen. Nach etwa einer Minute zeigt die Seite den Knopf „Für Windows herunterladen“ mit Version und Prüfsumme. Für jede neue Version nur Release und `download.json` erneuern.

Die Installationsdatei muss **signiert** sein, sonst warnt oder blockiert Windows (siehe `docs/WEBSEITE.md`).

## Veröffentlichen mit GitHub Pages und imagichron.de

1. Repo auf GitHub: **Settings → Pages** → „Deploy from a branch“, Zweig `main`, Ordner `/ (root)`.
2. **Custom domain:** `imagichron.de` (steht schon in `CNAME`).
3. Beim Domain-Anbieter im **DNS** eintragen:
   - `A`-Einträge für `imagichron.de`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA`-Einträge: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `CNAME` für `www`: `imagichron.github.io`
4. Empfohlen: Domain in der Organisation bestätigen (**Organisation → Settings → Pages → Add a domain**, TXT-Eintrag im DNS). So kann niemand sonst imagichron.de auf GitHub verwenden.
5. Sobald GitHub das Zertifikat erstellt hat: **„Enforce HTTPS“** anhaken.

## Commits

Einmal je Kopie: `git config core.hooksPath .githooks`. Nie `--no-verify`.
Dieses Repo ist **öffentlich**: Als Commit-E-Mail ist die anonyme GitHub-Adresse eingestellt (`git config user.email`), damit keine private E-Mail-Adresse sichtbar wird.

Vor einem späteren **Verkauf** zieht die Seite zu Cloudflare Pages um (GitHub Pages ist nicht für Verkaufsseiten gedacht). Dafür ändert man nur die DNS-Einträge, die Dateien bleiben gleich.
