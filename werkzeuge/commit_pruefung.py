"""Prüfung vor jedem Commit: keine Geheimnisse und keine privaten Daten in Git.

Läuft automatisch über den Git-Hook `.githooks/pre-commit` (einmal einrichten: `git config core.hooksPath .githooks`).
Gleiche Datei in Imagiter (`werkzeuge/`) und imagicoll (`tools/`) – bei Änderungen beide Kopien gleich halten.
Nur Python-Standardbibliothek (läuft trotz Windows „Intelligenter App-Steuerung“).

Geprüft wird nur, was für den Commit vorgemerkt ist (git add):
1. gesperrte Dateien/Ordner (z. B. privat/, Bildschirmfotos der Tests, *.key, *.pw, Schlüsseldateien),
2. neu hinzugefügte Zeilen auf Muster typischer Schlüssel (KI-, GitHub-, Cloud-Schlüssel, private Schlüssel)
   und auf feste Passwörter/Schlüssel im Code (z. B. api_key = "…").

Meldungen zeigen den gefundenen Wert nie vollständig. Ein falscher Alarm in einer Zeile lässt sich mit dem
Vermerk `geheimnis-ok` in derselben Zeile (als Kommentar) freigeben – nur, wenn wirklich kein Geheimnis drinsteht.

Aufrufe:
    python werkzeuge/commit_pruefung.py          vorgemerkte Änderungen prüfen (macht der Hook)
    python werkzeuge/commit_pruefung.py --alle   alle Dateien in Git prüfen (Kontrolle des ganzen Projekts)
"""
from __future__ import annotations

import re
import subprocess
import sys

FREIGABE = "geheimnis-ok"
MAX_GROESSE = 5 * 1024 * 1024   # größere Dateien werden nicht nach Mustern durchsucht (Pfadregeln gelten trotzdem)

# Dateien und Ordner, die nie in Git gehören (Pfade mit / , klein geschrieben verglichen)
GESPERRT = [
    (r"(^|/)privat/", "Ordner privat/ (echte Zeitreisen mit Familiendaten)"),
    (r"(^|/)tests/browser/shots/|(^|/)tools/test/shots/", "Bildschirmfotos der Tests (können private Inhalte zeigen)"),
    (r"\.schluessel\.json$", "gesicherter Datenschlüssel einer Zeitreise"),
    (r"\.(pw|key|secret|pem|p12|pfx|kdbx)$", "Schlüssel- oder Passwortdatei"),
    (r"(^|/)\.env(\.|$)", "Umgebungsdatei mit Zugangsdaten (.env)"),
    (r"(^|/)id_(rsa|ed25519|ecdsa)$", "privater SSH-Schlüssel"),
    (r"-lokal\.php$|(^|/)api/gaeste-config\.php$", "lokale Zugangsdaten (imagicoll)"),
    (r"(^|/)api/daten/|(^|/)upload/", "Server-Daten oder hochgeladene Fotos"),
]

# Muster für Schlüssel in neuen Zeilen
MUSTER = [
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "Anthropic-API-Schlüssel"),
    (r"\bsk-(?!ant-)(proj-)?[A-Za-z0-9_-]{20,}", "OpenAI-API-Schlüssel"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}", "GitHub-Zugangsschlüssel"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS-Zugangsschlüssel"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "Google-API-Schlüssel"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}", "Slack-Schlüssel"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "privater Schlüssel"),
    (r"(?i)\b(api[_-]?key|apikey|secret|client[_-]?secret|passwor[dt]|kennwort|access[_-]?token|auth[_-]?token|bearer)"
     r"\w*[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']", "fest eingetragenes Passwort oder Schlüssel"),
]

_GESPERRT = [(re.compile(m), t) for m, t in GESPERRT]
_MUSTER = [(re.compile(m), t) for m, t in MUSTER]


def pfad_gesperrt(pfad: str) -> str | None:
    """Grund, warum diese Datei nicht in Git darf, sonst None."""
    p = pfad.replace("\\", "/").lower()
    for regel, grund in _GESPERRT:
        if regel.search(p):
            return grund
    return None


def verdeckt(wert: str) -> str:
    """Gefundenen Wert nie ganz zeigen: nur Anfang und Länge."""
    return (wert[:4] + "…" if len(wert) > 6 else "…") + f" ({len(wert)} Zeichen)"


def zeile_pruefen(zeile: str) -> list[str]:
    """Funde in einer Zeile (Beschreibung mit verdecktem Wert). Vermerk „geheimnis-ok“ gibt die Zeile frei."""
    if FREIGABE in zeile:
        return []
    return [f"{grund}: {verdeckt(m.group(0))}" for regel, grund in _MUSTER for m in [regel.search(zeile)] if m]


def _git(*args: str) -> bytes:
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout


def _text(daten: bytes) -> str | None:
    if b"\0" in daten[:8000] or len(daten) > MAX_GROESSE:
        return None   # Bild, Video oder sehr groß: keine Mustersuche
    return daten.decode("utf-8", "replace")


def vorgemerkt_pruefen() -> list[str]:
    """Funde in den für den Commit vorgemerkten Änderungen (nur neu hinzugefügte Zeilen)."""
    funde = []
    namen = [n for n in _git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR").decode("utf-8").split("\0") if n]
    for name in namen:
        grund = pfad_gesperrt(name)
        if grund:
            funde.append(f"{name}: darf nicht in Git – {grund}")
            continue
        diff = _text(_git("diff", "--cached", "-U0", "--no-color", "--", name))
        if diff is None:
            continue
        nr = 0
        for zeile in diff.splitlines():
            kopf = re.match(r"@@ -\S+ \+(\d+)", zeile)
            if kopf:
                nr = int(kopf.group(1))
                continue
            if zeile.startswith("+") and not zeile.startswith("+++"):
                funde += [f"{name}:{nr}: {f}" for f in zeile_pruefen(zeile[1:])]
                nr += 1
    return funde


def alle_pruefen() -> list[str]:
    """Funde in allen Dateien, die in Git sind (ganze Dateien)."""
    funde = []
    for name in [n for n in _git("ls-files", "-z").decode("utf-8").split("\0") if n]:
        grund = pfad_gesperrt(name)
        if grund:
            funde.append(f"{name}: darf nicht in Git – {grund}")
            continue
        try:
            text = _text(_git("show", f":{name}"))
        except subprocess.CalledProcessError:
            continue
        for nr, zeile in enumerate((text or "").splitlines(), 1):
            funde += [f"{name}:{nr}: {f}" for f in zeile_pruefen(zeile)]
    return funde


def main(argv: list[str]) -> int:
    alle = "--alle" in argv
    try:
        funde = alle_pruefen() if alle else vorgemerkt_pruefen()
    except (OSError, subprocess.CalledProcessError) as f:
        print(f"Commit-Prüfung: git ließ sich nicht aufrufen ({f}). Commit abgebrochen.", file=sys.stderr)
        return 1
    if not funde:
        if alle:
            print("Commit-Prüfung: keine Auffälligkeiten.")
        return 0
    print("\nCommit-Prüfung: möglicherweise Geheimnisse oder private Daten gefunden" + ("" if alle else " – Commit abgebrochen") + ":\n",
          file=sys.stderr)
    for f in funde:
        print("  • " + f, file=sys.stderr)
    print("\nWas tun?\n"
          "  – Datei aus dem Commit nehmen:  git restore --staged <Datei>  (und ggf. in .gitignore eintragen)\n"
          "  – Geheimnis aus der Datei entfernen und an einem sicheren Ort ablegen (nicht in Git)\n"
          f"  – Nur bei falschem Alarm: in der Zeile den Kommentar „{FREIGABE}“ ergänzen\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
