# Dokumentation – Compendium

Diese Dokumentation ist für das Bewertungsteam. Sie erklärt die Architektur, die Entscheidungen und die Navigation des Prototyps. Eine kurze Übersicht steht in [README.md](./README.md).

---

## 1. Problem und Lösung

Klassische und Fachliteratur sind über viele Quellen verteilt. Empfehlungssysteme zeigen oft nur populäre Bücher. Sie zeigen aber nicht, was wirklich zu einem Menschen passt. Wer nicht genau weiß, was er sucht, findet selten ein gutes Buch. Viele verlieren dadurch die Freude am Lesen.

Compendium löst das mit einem **Genre-Baum**. Der Aufbau ist einfach:

- **Wurzel** = Hauptgenre
- **Äste** = Untergenres
- **Blätter** = einzelne Werke

Der Nutzer klickt sich Schritt für Schritt durch den Baum. Er sieht eine klare Struktur statt einer endlosen Liste. Der Start-Inhalt zeigt klassische Werke für ein breites Publikum — nicht nur eine kleine Nische.

**Zielgruppe:** Menschen, die Orientierung suchen — Schüler, Berufseinsteiger, lebenslang Lernende.

---

## 2. Architektur-Entscheidungen

### 2.1 Ein Frontend, eine Datei
Das ganze Frontend liegt weiterhin in einer einzigen `index.html` — HTML, CSS und JavaScript zusammen. Das ist Absicht. Vorteile für den Prototyp:
- Keine Build-Tools, kein Bundler
- Sofortiges Deployment über GitHub Pages
- Schnelle Änderungen möglich
Die **Daten** liegen seit Version 0.7 nicht mehr in dieser Datei, sondern in `data/trees.json` und in der SQLite-Tabelle (siehe 2.5). Eine spätere Aufteilung in Module ist jederzeit möglich. Für die Demo ist sie aber nicht nötig.

### 2.2 Zwei Betriebsarten: statisch oder mit Backend
Compendium läuft in zwei Betriebsarten:

| Betriebsart | Wo | Woher kommen die Daten |
|---|---|---|
| Statisch | GitHub Pages | `data/trees.json` per `fetch` |
| Mit Backend | lokal: `python app.py` | SQLite über `GET /api/trees` |

Das ist Absicht. GitHub Pages liefert nur statische Dateien aus, dort läuft kein Python. Der Prototyp bleibt deshalb auch ohne Server voll funktionsfähig.

**Warum sich diese Entscheidung geändert hat:** Die Versionen 0.1 bis 0.6 speicherten die Bäume direkt im JavaScript. Vorteile waren damals: kein Backend nötig, keine Hosting-Kosten, keine Netzwerkabhängigkeit. Im Unterricht wurde dann gezeigt, wie man Daten mit Flask aus einer SQL-Tabelle lädt. Dieser Weg wurde in Version 0.7 umgesetzt, weil er zwei echte Vorteile bringt:
- Die Daten liegen getrennt vom Code.
- Der Baum kommt aus einer SQL-Abfrage, nicht aus einem Objekt im Speicher.

Firebase bleibt als spätere Option im Backlog.

### 2.3 Zwei Bäume statt einem

Der Prototyp hat zwei Bäume. In `data/trees.json` stehen sie unter den Schlüsseln `literature` und `novels`:

- `literature` — Belletristik und Fachliteratur
- `novels` — Manga und Web-Novels

Beide Bäume nutzen dieselbe Logik und dieselbe Datenstruktur. Das beweist: Die Architektur ist erweiterbar. Ein dritter Baum (z. B. Filme) braucht nur neue Daten und einen neuen Knopf — keine neuen Funktionen.### 2.4 Keine externen Abhängigkeiten (Frontend)
Im Frontend werden nur HTML5, CSS3 und Vanilla JavaScript verwendet. Keine Frameworks, keine Bibliotheken. Das bedeutet: weniger Wartung, weniger Fehlerquellen, keine Einarbeitung in fremde Tools.

### 2.5 Backend: JSON → SQLite → API
Seit Version 0.7 gibt es ein kleines Backend. Es besteht aus drei Teilen:

```text
data/trees.json  →  seed.py  →  data/compendium.db  →  app.py  →  GET /api/trees
```

| Datei | Aufgabe |
|---|---|
| `data/trees.json` | Die Daten. Eine lesbare Textdatei, sie ist die Quelle. |
| `seed.py` | Liest die JSON-Datei und schreibt sie in die SQLite-Tabelle `nodes`. |
| `app.py` | Flask-Server. Liefert `index.html` und `GET /api/trees`. |
| `generate_covers.py` | Erzeugt die Titelbilder und trägt die Wikipedia-Links ein (siehe 2.6). Nur nötig, wenn Werke dazukommen. |
| `data/compendium.db` | Die Datenbank selbst. Sie wird immer neu erzeugt und steht in `.gitignore`. |

Die Datenbankdatei liegt **nicht** im Repository. Sie entsteht mit `python seed.py`. Wenn sie fehlt, legt `app.py` sie beim Start selbst an.

Das Frontend fragt zuerst `GET /api/trees` ab. Nur wenn das nicht geht, lädt es `data/trees.json`. So zeigt die lokale Demo das Backend, und die Live-Demo auf GitHub Pages läuft trotzdem ohne Server.

**Endpunkte**

| Methode | Pfad | Aufgabe |
|---|---|---|
| GET | `/` | liefert `index.html` |
| GET | `/api/trees` | beide Bäume als JSON aus der SQLite-Tabelle |
| POST | `/api/works` | legt ein neues Werk an |
| POST | `/api/covers` | lädt ein Titelbild nach `data/covers/` |
| GET | `/data/covers/<datei>` | liefert die Titelbilder aus |

**Wo neue Werke gespeichert werden**

`POST /api/works` schreibt an **zwei** Stellen: zuerst in die Tabelle `nodes`, danach in `data/trees.json`. Der Grund: Die Datenbank wird aus der JSON-Datei erzeugt (siehe oben). Würde nur die Datenbank geändert, wäre die Ergänzung beim nächsten `python seed.py` wieder weg. Klappt das Schreiben in die Datei nicht, löscht der Server die neue Zeile wieder und antwortet mit Fehler 500. So bleiben Tabelle und Datei gleich.

Pflichtfelder: `parent_id` (muss eine Kategorie sein), `title`, `author`. Optional: `id`, `desc`, `recommended`, `cover`, `wiki`, `related_id`, `related_title`.

| Antwort | Bedeutung |
|---|---|
| 201 | Werk angelegt |
| 400 | Pflichtfeld fehlt, falscher Body, `parent_id` ist ein Buch oder das Bild hat das falsche Format |
| 404 | `parent_id` gibt es nicht |
| 409 | ID ist schon vergeben |
| 413 | Bild ist größer als 3 MB |
| 500 | `data/trees.json` konnte nicht geschrieben werden (Datenbank wird zurückgerollt) |

Titelbilder: erlaubt sind JPG, JPEG, PNG und WEBP bis 3 MB. Der Dateiname wird aus der Werk-ID gebildet (`Prüfwerk Eins` → `pruefwerk-eins.png`).

### 2.6 Titelbilder: selbst erzeugt statt fremd geladen

Alle 44 Werke haben ein Titelbild. Diese Bilder sind **selbst erzeugt**: das Skript `generate_covers.py` schreibt für jedes Werk eine SVG-Datei nach `data/covers/<id>.svg` und trägt den Pfad in das Feld `cover` ein.

```text
data/trees.json  →  generate_covers.py  →  data/covers/*.svg  +  cover/wiki in data/trees.json  →  seed.py  →  Datenbank
```

| Frage | Antwort |
|---|---|
| Warum keine echten Buchcover? | Die deutsche Wikipedia zeigt keine Buchcover (dort sind nicht-freie Dateien nicht erlaubt), die englische nur unter „fair use". Diese Begründung gilt für Wikipedia, **nicht** für dieses Repository und nicht für GitHub Pages. Fremde Bilder herunterzuladen wäre rechtlich nicht sauber, ein eigenes Bild ist es. |
| Was ist ein SVG? | Eine Bilddatei, die nur aus Text besteht: Flächen, Linien, Schrift. Der Browser zeichnet sie wie ein Foto. Etwa 3 KB pro Bild, also sehr klein. |
| Wie sieht ein Titelbild aus? | Oben klein der Baum und die Kategorie, in der Mitte der Titel in einer Serifenschrift, darunter der Autor in einer Monospace-Schrift, unten ein feines Zweigmotiv, oben rechts ★ bei empfohlenen Werken. |
| Warum sieht nicht jedes Bild gleich aus? | Verlauf und Lichtpunkt hängen vom Werk ab, das Zweigmotiv von der Kategorie. Alle Werke einer Kategorie teilen also das Motiv. Das ist eine Designregel, kein Zufall. |
| Kann man das Bild zweimal erzeugen? | Ja. Das Skript ist **deterministisch**: derselbe Titel ergibt Byte für Byte dasselbe Bild (Hashwert aus der Werk-ID). Zweimal ausführen ändert nichts. |
| Wird ein hochgeladenes Bild überschrieben? | Nein. Ein im Browser hochgeladenes Bild bleibt stehen; ersetzt werden nur erzeugte `.svg`-Dateien. Mit `--force` kann man das erzwingen. |

Das Skript nutzt nur die Standardbibliothek von Python, also keine zusätzliche Abhängigkeit. Es ist die einzige Stelle, an der Titelbilder entstehen — im Repository liegt keine fremde Bilddatei.

**Wikipedia-Links:** 41 der 44 Werke haben einen Artikel. Das Skript trägt ihn als Feld `wiki` ein, auf der Karte wird daraus der Knopf „↗ Wikipedia". Drei Werke haben in der deutschen und englischen Wikipedia keinen Artikel und bleiben ohne Link: *Die Kunst des Seins* (der deutsche Artikel „Haben oder Sein" beschreibt ein anderes Buch von Fromm), *The Legendary Moonlight Sculptor* und *The Legendary Mechanic*.

---

## 3. Datenmodell

Jeder Knoten ist entweder eine **Kategorie** oder ein **Buch**.

| Feld | Kategorie | Buch (`isBook: true`) |
|---|---|---|
| `id` | eindeutige ID | eindeutige ID |
| `title` | Name der Kategorie | Buchtitel |
| `desc` | Kurzbeschreibung | Beschreibung (2 Sätze) |
| `children` | Liste weiterer Knoten | – |
| `author` | – | Autor |
| `recommended` | – | optional, zeigt ★ |
| `cover` | – | optional, Pfad zum Titelbild, z. B. `data/covers/1984.svg` |
| `wiki` | – | optional, Link zum Wikipedia-Artikel |
| `relatedId` | – | optional, verknüpftes Werk |
| `relatedTitle` | – | optional, Name der Verknüpfung |

Zwei Bäume werden im Objekt `trees` gespeichert:

- **`literatureTree`** — Belletristik (Science Fiction, Fantasy, Weltliteratur) und Fachliteratur (Informatik, Philosophie, Wissenschaft & Gesellschaft)
- **`novelTree`** — Manga (Shonen, Seinen, Shoujo) und Web-Novels (Light Novels, Isekai, koreanische, chinesische)

Die Anzeigenamen für die Kopfzeile stehen in `treeLabels`. Dadurch kann man einen Baum umbenennen, ohne die Daten zu ändern.

**Aktueller Umfang:** 44 Werke in 17 Unterkategorien, verteilt auf zwei Bäume (26 Werke in der Literatur, 18 in Manga & Web-Novels). 13 Werke tragen ein ★. Alle 44 haben ein Titelbild, 41 davon einen Wikipedia-Link (siehe 2.6).

Dieselben Daten stehen in der SQL-Tabelle `nodes`. Aus dem verschachtelten JSON wird eine flache Tabelle, in der die Nachbarschaft durch `parent_id` entsteht:

| Spalte | Bedeutung |
|---|---|
| `id` | ID des Knotens, weltweit eindeutig |
| `parent_id` | ID der übergeordneten Kategorie; `NULL` = Wurzel |
| `tree` | `literature` oder `novels` |
| `title`, `description` | Titel und Kurzbeschreibung |
| `is_book` | `1` = Buch (Blatt), `0` = Kategorie |
| `author`, `recommended` | Autor und ★ (`1` = empfohlen) |
| `cover`, `wiki` | Pfad zum Titelbild und Link zum Wikipedia-Artikel |

Beide Felder sind optional. Fehlen sie, sieht die Karte aus wie vor Version 0.7 — es gibt also keinen Bruch im Layout.
| `related_id`, `related_title` | Ziel des Cross-Media-Links |

Insgesamt stehen 63 Zeilen in der Tabelle. Der Baum wird beim Auslesen wieder zusammengesetzt (siehe 2.5).

---

## 4. Navigation

### 4.1 Drill-Down mit `historyStack`

Die Navigation funktioniert ohne Page-Reload. Zwei Variablen speichern den Zustand:

- `currentNode` — der aktuelle Knoten
- `historyStack` — Liste der vorherigen Knoten

Ein Klick auf eine Kategorie macht drei Dinge:

1. Der aktuelle Knoten kommt auf den Stack.
2. Der neue Knoten wird aktiv.
3. Der neue Knoten wird gerendert.

Ein Klick auf „Zurück" liest den letzten Knoten aus dem Stack und zeigt ihn wieder.

### 4.2 Wichtige Funktionen

- **`loadTrees()`** — lädt die Baumdaten. Zuerst über `GET /api/trees`, sonst aus `data/trees.json`.
- **`start()`** — ruft `loadTrees()` auf, prüft das Ergebnis und rendert den Startknoten. Wird einmal am Ende des Skripts aufgerufen.
- **`renderNode(node)`** — zeigt die Kinder eines Knotens als Karten. Kategorien sind klickbar, Bücher nicht. Bei Büchern prüft die Funktion nach dem Rendern, ob die Beschreibung abgeschnitten ist. Wenn ja, fügt sie den Button „Mehr anzeigen" ein (siehe 4.5).
- **`findPath(node, targetId)`** — sucht einen Knoten mit einer bestimmten ID. Gibt den ganzen Pfad von der Wurzel zurück.
- **`navigateTo(targetId)`** — springt zu einem Knoten, auch in den anderen Baum. Wird für Cross-Links benutzt. Wenn das Ziel ein Buch ist, springt die App zur übergeordneten Kategorie — so sieht der Nutzer das Buch im Kontext.
- **`switchTree(key)`** — wechselt zwischen den zwei Bäumen. Der `historyStack` wird dabei geleert, damit die Zurück-Taste nicht in den anderen Baum springt.
- **`countWorks(node)`** — zählt rekursiv alle Bücher unter einer Kategorie. Zeigt „X Werke" auf der Karte.

### 4.3 Breadcrumb-Navigation

Unter der Kopfzeile zeigt die App den aktuellen Pfad. Beispiel:

`Literatur › Belletristik › Science Fiction`

Das macht die Struktur sichtbar und hilft bei der Orientierung.

### 4.4 Tastatur und Animation

- Die **Escape-Taste** macht dasselbe wie der Zurück-Button.
- Beim Rendern erscheinen die Karten mit einer kurzen Einblend-Animation (40 ms pro Karte versetzt). Das sieht in Videos und Online-Präsentationen besser aus.

### 4.5 Aufklappbare Beschreibungen („Mehr anzeigen")

Lange Buchbeschreibungen passen nicht immer auf die Karte. Damit die Karten gleich hoch bleiben, ist die Beschreibung auf 2 Zeilen begrenzt (CSS `line-clamp`).

So funktioniert es:

1. Nach dem Rendern vergleicht die App die volle Höhe des Texts mit der sichtbaren Höhe (`scrollHeight` gegen `clientHeight`).
2. Ist der Text wirklich abgeschnitten, erscheint unter der Beschreibung der Button „Mehr anzeigen".
3. Ein Klick darauf klappt den Text auf. Der Button wechselt zu „Weniger anzeigen". Ein weiterer Klick klappt den Text wieder zu.

Wichtig dabei: Der Button erscheint nur, wenn der Text wirklich zu lang ist. Kurze Beschreibungen bekommen keinen Button. Das hält die Karten sauber.

---

## 5. Cross-Media-Verknüpfung

Ein Buch kann optional mit einem Werk im anderen Baum verknüpft werden. Dafür gibt es die Felder `relatedId` und `relatedTitle`. Auf der Buch-Karte erscheint dann ein Button mit dem Symbol `↔`. Ein Klick darauf ruft `navigateTo()` auf und springt zum verknüpften Werk — auch in den anderen Baum.

**Aktuelle Beispiele:** Der Roman *No Longer Human* von Osamu Dazai ↔ die Manga-Adaption von Junji Ito — und die Web-Novel *Solo Leveling* von Chugong ↔ die Manhwa-Adaption von DUBU (Redice Studio). Die Verknüpfung ist in beide Richtungen hinterlegt: jedes Werk kennt sein Gegenstück. Deshalb tragen vier Datensätze ein `relatedId` — das sind **zwei** Verknüpfungen (zwei Paare).

Diese Funktion war ursprünglich nur als Roadmap-Ziel geplant. Sie ist aber schon als Basis umgesetzt. Das zeigt: Die Architektur ist wirklich erweiterbar, nicht nur auf dem Papier. Weitere Verknüpfungen sind im Backlog.

Beide Paare verbinden dieselbe Geschichte über zwei Medien hinweg — einmal Japan (Roman ↔ Manga), einmal Korea (Web-Novel ↔ Manhwa). Damit ist das Prinzip über beide Bäume und zwei Kulturen hinweg gezeigt.

---

## 6. Kuratierung mit ★

Compendium ist eine Alternative zu algorithmischen Empfehlungen. Ein Buch kann mit `recommended: true` markiert werden. Dann erscheint ein ★ vor dem Titel. Eine Legende in der Kopfzeile erklärt:

> ★ Persönlich gelesen und empfohlen

**Die Idee:** Nicht Klickzahlen entscheiden, sondern die echte Leseerfahrung des Kurators. Damit löst das Projekt den zentralen Kritikpunkt an bestehenden Systemen: Popularität ist nicht dasselbe wie Passung.

**Aktueller Stand:** 13 Werke sind mit ★ markiert.

---

## 7. Design-System

Der Prototyp nutzt ein dunkles Farbschema im „Matrix"-Stil. Alle Farben sind als CSS-Variablen zentral definiert.

| Variable | Wert | Verwendung |
|---|---|---|
| `--bg` | `#0A0A0A` | Seitenhintergrund |
| `--card-bg` | `#121712` | Kartenhintergrund |
| `--green` | `#33FF66` | Akzent, Hover, aktive Elemente |
| `--green-dim` | `#1F8F44` | Rahmen, gedämpfter Akzent |
| `--text-white` | `#FFFFFF` | Überschriften |
| `--text-muted` | `#9FCDAF` | Fließtext |

**Visuelle Hierarchie:**

- Kategorie-Karten: kräftige linke Linie in Grün, klickbar.
- Buch-Karten: gedämpfte Linie, kursiver Titel, Autor in Großbuchstaben, nicht klickbar.

**Lesbarkeit:** Der Fließtext nutzt eine Systemschrift (`system-ui`, Segoe UI, Roboto, Arial). Monospace bleibt für kleine Etiketten. Die Schriftgrößen wurden für Video und Online-Präsentationen erhöht (`h3`: 1.2 rem, `p`: 1 rem, `line-height`: 1.72).

**Titel:** Der Titel steht mittig, in einer Systemschrift mit Serifen (Georgia, Palatino, Times), gesperrt mit einer Laufweite von 0.16 em. Der Untertitel ist dieselbe Schrift, kursiv. Das wirkt wie die Titelseite eines Buches. Auch hier werden keine Schriften nachgeladen.

**Karte als Poster (ab Version 0.9):** Bei Kategorien zeigt die Karte Titel, Beschreibung und Werk-Zähler. Bei Werken ist die Karte selbst das Titelbild: Das Bild füllt die Karte oben im Seitenverhältnis 2:3, unten liegt eine dunkle Leiste mit Beschreibung und den Knöpfen „↗ Wikipedia" und Cross-Media-Link. Titel und Autor stehen auf den generierten Bildern schon auf dem Cover, deshalb wiederholt die Karte sie nicht. Bei Kategorien zeigt die Karte Titel, Beschreibung und Werk-Zähler.

Drei Sonderfälle sind abgefangen:

| Fall | Verhalten |
|---|---|
| Werk ohne Bild | dunkle Ersatzfläche mit Titel und Autor |
| Bild aus dem Formular (Foto, ohne Schrift) | Titel und Autor als kleine Zeile unten auf dem Bild, ★ als Ecke |
| Generiertes SVG | nichts zusätzlich — Titel, Autor und ★ stehen schon auf dem Bild (sonst stünde ★ doppelt) |

Werke stehen in engeren Spalten (etwa 185 px) als Kategorien (300 px) — das Raster richtet sich danach, ob in einer Ebene nur Werke liegen. So sieht eine Kategorie wie ein Bücherregal aus.

**Titelbilder:** Die Titelbilder folgen demselben Design-System, aber in einer eigenen Komposition: fester Rahmen in `--green-dim`, Verlauf von `--card-bg` nach `--bg`, oben Baum und Kategorie in Monospace, in der Mitte der Titel in einer Serifenschrift (wie eine Buchseite), darunter der Autor in Monospace, unten ein feines Zweigmotiv. Die sechs Farbwerte sind **dieselben** wie in der Tabelle oben — die Bilder führen keine neuen Farben ein. Die Regeln stehen in [docs/DESIGN_GUIDE.md](./docs/DESIGN_GUIDE.md), Abschnitt 3.1.

**Formular:** Der Knopf „＋ Werk hinzufügen" öffnet ein Formular für neue Werke. Es benutzt dieselben Farbvariablen und Formen wie der Rest der Seite — neue Farben gibt es nicht. Das Formular erscheint nur, wenn das Backend läuft.

**Formsprache:** Karten und Buttons sind gerundet (Karten 14px, Buttons als Pillen). Der farbige Balken links ist ein `inset`-Schatten und kein `border-left`, damit er der Rundung folgt. Der Werk-Zähler ist ein Chip. Alle diese Werte stehen als Variablen in `:root`. Die Farbwerte der Tabelle bleiben unverändert.

---

## 8. Grenzen und Backlog

Aktuelle Grenzen:

- Neue Werke lassen sich nur lokal anlegen (Formular oder `POST /api/works`), nicht auf der Live-Demo.
- Bilder können nur über die API hochgeladen werden; ohne laufendes Backend gar nicht.
- Der Schreib-Endpunkt hat kein Login. Er gehört zum lokalen Prototyp.
- In die Tabelle schreibt `seed.py` (alles) und `app.py` (einzelne neue Werke).
- Keine Build-Pipeline, keine Module.
- Keine automatisierten Tests.
- Zwei Cross-Media-Verknüpfungen (zwei Paare: *No Longer Human*, *Solo Leveling*).
- Keine Suche und keine Filter.
- Drei Werke haben keinen Wikipedia-Link, weil es keinen Artikel gibt (siehe 2.6).
- Die Titelbilder sind typografisch erzeugt, keine Fotografien oder Verlagscover. Das ist eine bewusste Entscheidung (Rechte, Einheitlichkeit, Dateigröße).

Damit die Live-Demo ohne Backend vollständig aussieht, sind die Titelbilder statische Dateien im Repository: sie funktionieren ohne Server und ohne Netz. Nur das **Anlegen** neuer Werke braucht das lokale Backend, weil GitHub Pages keine Python-Programme ausführt.

**Umgesetzt in Version 0.8: Titelbilder und Wikipedia-Links**

- Die Bilder sind selbst erzeugt (SVG) statt fremd geladen — Begründung in 2.6.
- Alle 44 Werke haben ein Bild; 41 haben einen Link zum Artikel, gespeichert als Feld in den Daten.
- Drei Werke bleiben ohne Link, weil es keinen Artikel gibt — die Liste steht in 2.6.
- Der Bild-Bauplan ist eine Designregel und steht in [docs/DESIGN_GUIDE.md](./docs/DESIGN_GUIDE.md), Abschnitt 3.1.

**Umgesetzt in Version 0.7: Flask-Backend**

Im Unterricht wurde ein einfaches Flask-Beispiel gezeigt:

- Das Frontend ruft mit `fetch("/api/begruessung")` einen Endpunkt auf.
- Das Backend antwortet mit JSON.
- Das Frontend zeigt die Daten an.

Dieses Muster ist jetzt in Compendium eingebaut:

- `data/trees.json` enthält die Genre-Bäume als Datei.
- `seed.py` schreibt sie in die SQLite-Tabelle `nodes`.
- `app.py` liefert sie über `GET /api/trees`.
- Das Frontend lädt sie per `fetch` und rendert sie wie vorher.

Vorteile:

- Die Daten sind vom Code getrennt.
- Neue Werke können ohne Code-Änderung hinzugefügt werden.
- Flask ist leichtgewichtig und gut für den Einstieg geeignet.

Die Live-Demo auf GitHub Pages funktioniert unverändert weiter, weil das Frontend als Ausweichlösung die JSON-Datei laden kann.

Firebase bleibt als spätere Option im Backlog.

---

## 9. Änderungen im Überblick

### Version 0.1 — Erster Prototyp
- Ein Literatur-Baum
- Drill-Down mit Zurück-Button
- Einfache Karten für Bücher und Kategorien

### Version 0.2 — Zweiter Baum und Cross-Media
- Zweiter Baum für Manga und Web-Novels
- Umschalter zwischen Bäumen
- Erste Cross-Media-Verknüpfung (*No Longer Human*)
- `findPath()` und `navigateTo()`

### Version 0.3 — Inhalte und Kuratierung
- 35 Werke in 13 Kategorien
- ★-System für persönliche Empfehlungen
- Breadcrumb-Navigation
- Werk-Zähler auf Kategorien

### Version 0.4 — Optimierung für Präsentation
- Größere Schrift für Video und Online
- Einblend-Animation für Karten
- Escape-Taste als Zurück-Shortcut

### Version 0.5 — Mehr anzeigen
- Lange Buchbeschreibungen werden auf 2 Zeilen begrenzt (CSS line-clamp)
- Button „Mehr anzeigen" / „Weniger anzeigen" klappt den Text auf und zu
- Der Button erscheint nur, wenn der Text wirklich abgeschnitten ist
- Reihenfolge in der Buchkarte: Titel, Autor, Beschreibung, Toggle, Cross-Link

### Version 0.6 — Visuelle Auffrischung
- Karten und Buttons sind gerundet (Radius 14px, Buttons als Pillen)
- Weiche Schatten, die Karte hebt sich beim Hover um 3px
- Fließtext in einer Systemschrift, Monospace nur für Etiketten
- Werk-Zähler als Chip
- Fokus-Rahmen für Tastatur-Bedienung
- Sanfter Hintergrundverlauf und Block für reduzierte Bewegung
- Titel als gesperrte Serifenschrift, mittig, wie eine Buchseite
- Keine neuen Dateien, keine externen Abhängigkeiten

### Version 0.7 — Flask-Backend mit SQLite
- Die Daten sind aus `index.html` in die Datei `data/trees.json` gewandert
- `seed.py` erzeugt daraus die SQLite-Tabelle `nodes`
- `app.py` (Flask) liefert beide Bäume über `GET /api/trees`
- Das Frontend lädt per `fetch`: zuerst über die API, sonst aus der JSON-Datei
- Die statische Live-Demo bleibt ohne Backend funktionsfähig
- Fehlermeldung in der Klasse `.status`, wenn keine Daten geladen werden können
- Dokumentation um Abschnitt 2.5 und die SQL-Spalten in Abschnitt 3 ergänzt
- Neue Felder `cover` (Titelbild) und `wiki` (Wikipedia-Link), beide optional
- Karten zeigen links ein Titelbild und darunter den Link „↗ Wikipedia"
- Formular „＋ Werk hinzufügen" im Frontend, sichtbar nur mit laufendem Backend
- `POST /api/covers` lädt Titelbilder nach `data/covers/`, `GET /data/covers/<datei>` liefert sie aus
- Die Datenbank wird automatisch neu erzeugt, wenn das Schema sich ändert

### Version 0.10 — Zweite Cross-Media-Verknüpfung, Fußzeile, Aufräumen
- Zweite Cross-Media-Verknüpfung: Web-Novel *Solo Leveling* (Chugong) ↔ Manhwa-Adaption (DUBU, Redice Studio) — der Manhwa ist als neues Werk im Baum Manga › Seinen
- Jetzt 44 Werke, 44 Titelbilder, 41 Wikipedia-Links
- Fußzeile mit Link zum GitHub-Repository und Kuratierung-Legende
- Knöpfe auf den Postern bleiben auf schmalen Fenstern (Telefon) in einer Zeile
- Recherche-Dokumente zu den Titelbildern (`docs/COVER_KANDIDATEN.*`) entfernt — die Ergebnisse stehen in 2.6 und im Skript

### Version 0.9 — Karte als Poster
- Buchkarten zeigen das Titelbild auf der ganzen Karte (Seitenverhältnis 2:3), darunter Beschreibung und Knöpfe
- Titel und Autor stehen auf den generierten Bildern und werden nicht wiederholt
- Werke liegen in engeren Spalten, wenn eine Ebene nur Werke enthält — Kategorien bleiben breit
- ★ steht bei generierten Bildern im Bild selbst; bei fremden Bildern als Ecke auf dem Cover
- Fallback: Werk ohne Bild zeigt eine dunkle Fläche mit Titel und Autor
- „Mehr anzeigen", Cross-Media-Sprung und Escape funktionieren wie vorher

### Version 0.8 — Titelbilder und Wikipedia-Links
- `generate_covers.py` (neu) erzeugt für alle 43 Werke ein Titelbild als SVG in `data/covers/`
- Die Bilder sind typografisch: Baum, Kategorie, Titel, Autor, Zweigmotiv, ★ — in den Farben des Design-Systems
- Das Skript ist deterministisch und braucht keine zusätzliche Bibliothek
- 40 Werke bekommen das neue Feld `wiki`; auf der Karte erscheint der Knopf „↗ Wikipedia"
- Drei Werke bleiben ohne Link, weil es keinen Artikel gibt
- Karten zeigen links das Titelbild (78 px, 2:3); ohne Bild sieht die Karte aus wie vorher
- Designregeln für Titelbilder in `docs/DESIGN_GUIDE.md` (Abschnitt 3.1)
- Readme erklärt, warum das Formular nur lokal funktioniert

---

*Stand: Prototyp, präsentationsbereit (Version 0.10).*
