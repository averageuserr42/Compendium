# Compendium - Prototyp

**Ein neuer Zugang zur Literatur. Ordnung im Meer der Bücher.**

## Über das Projekt
Compendium ist ein Proof-of-Concept für eine strukturierte Literatur-Navigation. Statt auf Bestseller-Listen oder Black-Box-Algorithmen zu setzen, nutzt Compendium einen **Genre-Baum**, um Leser von der Wurzel (Hauptkategorie) über die Äste (Untergenres) bis zu den Blättern (einzelne kuratierte Werke) zu führen.

## Aktueller Stand (Prototyp)
Dieses Repository enthält den interaktiven Frontend-Prototypen, der das Kernkonzept demonstriert:
- Verschachtelte JSON-Datenstruktur für den Genre-Baum – seit Version 0.7 in `data/trees.json`, nicht mehr im HTML.
- Dynamisches DOM-Rendering mittels Vanilla JavaScript.
- Klick-basierte Navigation (Drill-Down) durch die Kategorien.
- **Zwei parallele Bäume:** Literatur (Belletristik / Fachliteratur) und Manga & Web-Novels, umschaltbar über einen Tree-Switcher im Header.
- **Zwei Cross-Media-Verknüpfungen** zwischen thematisch verwandten Werken aus beiden Bäumen (Roman ↔ Manga-Adaption von Osamu Dazai, Web-Novel ↔ Manhwa-Adaption von Solo Leveling) – ursprünglich als späteres Roadmap-Ziel geplant, jetzt als Basis-Implementierung vorhanden.
- Integriertes Design-System (Dark-Theme mit Akzentfarben, "Matrix"-Stil).
- **Titelbilder und Wikipedia-Links:** Alle 44 Werke haben ein Titelbild, 41 davon einen Link zum Wikipedia-Artikel. Beide Felder sind optional – fehlen sie, sieht die Karte aus wie vorher. Die Titelbilder sind **selbst erzeugt** (SVG, typografisch): im Repository liegt keine fremde Bilddatei.
- **Neue Werke über den Browser:** Mit laufendem Backend öffnet der Knopf „＋ Werk hinzufügen" ein Formular (Kategorie, Titel, Autor, Beschreibung, Wikipedia-Link, Bild, ★). Gespeichert wird über `POST /api/works`, Bilder gehen über `POST /api/covers` nach `data/covers/`. Auf der Live-Demo ist das Formular nicht sichtbar, weil dort kein Backend läuft – die Begründung steht unten unter „Formular nur lokal".

Für Details zur Architektur und den Designentscheidungen siehe [Documentation.md](./Documentation.md).

## Tech Stack
- HTML5
- CSS3 (Custom Properties, CSS Grid)
- Vanilla JavaScript (DOM Manipulation, JSON Handling)
- Python 3 mit Flask und SQLite – nur für das optionale lokale Backend

## Setup / Demo
**Nur ansehen (ohne Installation)**
Die Live-Demo läuft ohne Server: das Frontend lädt `data/trees.json` selbst. Flask und SQLite werden dafür nicht gebraucht.
👉 **[Hier klicken für die Live-Demo](https://averageuserr42.github.io/Compendium/)**

**Mit Backend starten (Flask + SQLite) – Windows: Doppelklick auf `start.bat`**

Das Skript erzeugt die Datenbank und startet den Server in einem Schritt:

```bash
start.bat
```

Oder manuell:

```bash
python -m pip install flask
python seed.py      # data/trees.json -> data/compendium.db
python app.py       # Server auf http://127.0.0.1:5000
python generate_covers.py   # optional: Titelbilder (SVG) erzeugen und Wikipedia-Links setzen
```

Danach im Browser öffnen: `http://127.0.0.1:5000`. Das Frontend holt die Daten dann über `GET /api/trees` und zeigt zusätzlich das Formular für neue Werke.

**API im Überblick**

| Methode | Pfad | Aufgabe |
|---|---|---|
| GET | `/api/trees` | beide Bäume als JSON |
| POST | `/api/works` | neues Werk anlegen |
| POST | `/api/covers` | Titelbild hochladen |
| GET | `/data/covers/<datei>` | Titelbild ausliefern |

Die Datenbankdatei liegt nicht im Repository. Sie entsteht mit `python seed.py` oder automatisch beim Start von `app.py`.

## Formular nur lokal

Die Live-Demo liegt auf **GitHub Pages**. Das ist reines statisches Hosting: es liefert Dateien aus, kann aber keine Programme starten. Das Backend (`app.py`) läuft deshalb nur auf dem eigenen Rechner. Daraus folgt:

| Funktion | Live-Demo (GitHub Pages) | Lokal (`python app.py`) |
|---|---|---|
| Baum ansehen und navigieren | ja | ja |
| Titelbilder und Wikipedia-Links | ja (statische Dateien) | ja |
| Neues Werk anlegen | nein (kein Backend) | ja |
| Titelbild hochladen | nein | ja |

Auf der Live-Demo steht an der Stelle des Formulars ein kurzer Hinweis. Das ist kein Fehler, sondern die Grenze des statischen Hostings. Wer neue Werke anlegen will, startet den Server wie oben.

## Titelbilder erzeugen

```bash
python generate_covers.py            # schreibt data/covers/<id>.svg, setzt cover und wiki
python generate_covers.py --force    # ersetzt auch im Browser hochgeladene Bilder
```

Das Skript ist deterministisch (derselbe Titel ergibt dasselbe Bild), braucht nur die Standardbibliothek von Python und erklärt sich im Kopf der Datei selbst. Warum keine fremden Buchcover verwendet werden, steht in [Documentation.md](./Documentation.md), Abschnitt 2.6; die Gestaltungsregeln stehen in [docs/DESIGN_GUIDE.md](./docs/DESIGN_GUIDE.md), Abschnitt 3.1.

Ein Durchlauf durch den Code steht in [docs/CODE_TOUR.md](./docs/CODE_TOUR.md).
