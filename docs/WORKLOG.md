# Arbeitsprotokoll – Compendium

Dieses Protokoll hält fest, was wann geändert wurde und warum.
Es ergänzt die Trello-Karte: Trello zeigt den Plan, dieses Protokoll zeigt die Umsetzung.

Tageszusammenfassungen im Schulformat werden außerhalb des Repositoriums geführt und in der Akademie hochgeladen (zuletzt: 2026-09-21).

Regeln für dieses Protokoll:

- Ein Eintrag pro Arbeitseinheit, nicht pro Klick.
- Kurze Sätze, einfache Formulierungen.
- Immer: Was, Warum, Dateien, Ergebnis, Offen.
- Datum nach dem Muster JJJJ-MM-TT.

Hinweis: Die Einträge vor dem 19.09.2026 sind aus der Git-Historie rekonstruiert.

---

## Format

```text
### JJJJ-MM-TT – Titel
- Was:
- Warum:
- Dateien:
- Ergebnis:
- Offen:
```

---

## Einträge

### 2026-09-23 – Zweite Cross-Media-Verknüpfung, Fußzeile, Aufräumen (Version 0.10)

- **Was:** Neue Verknüpfung: Web-Novel *Solo Leveling* (Chugong) ↔ Manhwa-Adaption (DUBU, Redice Studio). Der Manhwa steht als neues Werk in Manga › Seinen, beide Richtungen sind in den Daten hinterlegt. Dazu: Fußzeile mit GitHub-Link und Kuratierung-Legende, und die Knöpfe auf den Postern bleiben auf schmalen Fenstern (bis 480 px) in einer Zeile. Entfernt: `docs/COVER_KANDIDATEN.md` und `docs/cover-kandidaten.json` (Recherche abgeschlossen, Ergebnisse stehen in Dokumentation 2.6 und im Skript) sowie die Tagesdokumentation vom 21.09. (sie ist in der Akademie hochgeladen, nicht fürs Repository).
- **Warum:** Der offene Punkt „nur eine Cross-Media-Verknüpfung" aus der Dokumentation ist damit geschlossen — zwei Paare zeigen das Prinzip über beide Bäume (Japan: Roman ↔ Manga, Korea: Web-Novel ↔ Manhwa). Der Fußzeilen-Punkt war offen geblieben, weil die ★-Legende nur im Kopfbereich stand. Der offene Punkt aus 0.9 (Knöpfe auf dem Telefon) ist damit ebenfalls geprüft und geschlossen.
- **Dateien:** `data/trees.json` (neues Werk + zwei relatedId-Felder, Generator hat cover/wiki ergänzt), `generate_covers.py` (ein Eintrag in `WIKI_LINKS`), `index.html` (Fußzeile, Media-Query für schmale Fenster), `Documentation.md` (Abschnitt 5, Zahlen 44/41/63, Changelog 0.10), `README.md` (Zahlen), `docs/CODE_TOUR.md` (Zahlen, Stand-Zeile), gelöscht: `docs/COVER_KANDIDATEN.md`, `docs/cover-kandidaten.json`, `docs/TAGESDOKUMENTATION_2026-09-21.txt`.
- **Ergebnis (geprüft):** Diff gegen die gesicherte Vorgängerdatei zeigt nur den neuen Manhwa-Knoten und die zwei `relatedId`-Felder. 44 Werke, 13 ★, 44 Titelbilder, 41 Wikipedia-Links, alle IDs eindeutig. Im Browser (Flask-Modus): Cross-Media-Sprung in beide Richtungen führt zur richtigen Kategorie, das Manhwa-Bild lädt. Bei 375 px Fensterbreite stehen beide Knöpfe in einer Zeile (Höhe 35 px). Fußzeile sichtbar, Link mit `target="_blank" rel="noopener"`. Im statischen Modus separat geprüft.
- **Offen:** Nichts. Code eingefroren zur Präsentationsvorbereitung.

### 2026-09-21 – Buchkarte als Poster (Version 0.9)

- **Was:** Die Buchkarte ist jetzt ein vertikales Poster: das Titelbild füllt die Karte oben im Verhältnis 2:3, unten liegt eine dunkle Leiste mit Beschreibung und den Knöpfen. Titel und Autor stehen auf den generierten SVG-Bildern und werden auf der Karte nicht wiederholt. Ebenen, in denen nur Werke liegen, nutzen enge Spalten (etwa 185 px) — die Kategorie-Ebenen bleiben bei 300 px. Werk ohne Bild bekommt eine dunkle Ersatzfläche mit Titel und Autor; ein hochgeladenes Foto (ohne eigene Schrift) bekommt Titel und Autor als kleine Zeile auf dem Bild und ★ als Ecke.
- **Warum:** Die Karte sah bisher wie ein Dokument mit kleinem Bild daneben aus. Als Poster wirkt die Kategorie wie ein Bücherregal, und die Bilder — die ohnehin Titel und Autor tragen — werden zum Hauptträger der Information. Die enge Spaltenbreite passt zu den hochkanten Bildern.
- **Dateien:** nur `index.html` (CSS und die Buch-Zweige in `renderNode`), `Documentation.md` (Abschnitt 7, Changelog 0.9), `docs/DESIGN_GUIDE.md` (Abschnitt 3.2, Anmerkung zum Balken in 3), `docs/CODE_TOUR.md` (Block „Карточка-постер", zwei Fragen in der Tabelle), `docs/WORKLOG.md`.
- **Ergebnis (im Browser geprüft, beide Betriebsarten):** Generierte Bilder füllen die Karte; keine doppelte Überschrift, kein doppelter ★ (der erste Entwurf hatte „★★" — das Badge wird jetzt nur bei Nicht-SVG-Bildern gesetzt). „Mehr anzeigen" klappt Beschreibung auf (41 → 124 px) und zu. Cross-Media-Sprung aus „No Longer Human" (Roman) in den Manga-Baum funktioniert. Im statischen Modus (ohne Backend): Bilder da, Formular versteckt, Hinweis sichtbar, keine Fehler in der Konsole.
- **Offen:** Noch nicht committet. Auf sehr schmalen Fenstern rücken die Knöpfe in zwei Zeilen — bei 185 px Spaltenbreite akzeptabel, auf dem Telefon noch einmal ansehen.

### 2026-09-21 – Titelbilder, Wikipedia-Links und ein Generator (Version 0.8)

- **Was:** Alle 43 Werke haben jetzt ein Titelbild, 40 davon einen Link zum Wikipedia-Artikel. Die Bilder sind nicht heruntergeladen, sondern **selbst erzeugt**: das neue Skript `generate_covers.py` schreibt für jedes Werk eine SVG-Datei nach `data/covers/<id>.svg` und trägt den Pfad in das Feld `cover` ein; dasselbe Skript setzt das Feld `wiki`. Bauplan der Bilder: oben klein Baum und Kategorie, in der Mitte der Titel in einer Serifenschrift, darunter der Autor in Monospace, unten ein feines Zweigmotiv, oben rechts ★. Verlauf und Lichtpunkt hängen vom Werk (Hashwert der ID), das Zweigmotiv von der Kategorie — so wirken alle Werke einer Kategorie wie eine Serie.
- **Warum:** Der offene Punkt aus dem vorigen Eintrag („Titelbilder fehlen noch") ist damit geschlossen. Fremde Buchcover kamen nicht in Frage: Die deutsche Wikipedia zeigt keine (dort sind nicht-freie Dateien nicht erlaubt), die englische nur unter „fair use" — diese Begründung gilt für Wikipedia, **nicht** für dieses Repository. Eigene Bilder sind rechtlich sauber, einheitlich und mit etwa 3 KB pro Datei sehr klein. Außerdem soll die Recherche nicht verloren gehen: die geprüfte Liste steht jetzt als `WIKI_LINKS` im Skript.
- **Dateien:** `generate_covers.py` (neu), `data/covers/` (43 SVG-Dateien, neu), `data/trees.json` (nur die Felder `cover` und `wiki` ergänzt), `Documentation.md` (neuer Abschnitt 2.6, Abschnitte 3, 7, 8, Changelog 0.8 — und ein fehlender Zeilenumbruch in 2.1 repariert), `README.md` (Abschnitte „Formular nur lokal" und „Titelbilder erzeugen"), `docs/DESIGN_GUIDE.md` (neuer Abschnitt 3.1, Checkliste), `docs/CODE_TOUR.md` (neuer Abschnitt 7), `docs/COVER_KANDIDATEN.md` (Entscheidung festgehalten).
- **Ergebnis (geprüft, nicht behauptet):** `data/trees.json` wurde vorher gesichert und danach feldweise verglichen — geändert haben sich **nur** `cover` (43 Werke) und `wiki` (40 Werke); Kategorien, Beschreibungen, ★ (13) und die Cross-Media-Verknüpfung sind unverändert. Zweimal ausführen ergibt denselben SHA-256 (also deterministisch). Alle 43 SVG-Dateien sind gültiges XML. Im Browser geprüft: Bilder laden (78 px, 2:3), „↗ Wikipedia" zeigt auf den passenden Artikel, „Mehr anzeigen" klappt auf, der Cross-Media-Sprung führt weiterhin in den Manga-Baum. Auch im Modus **ohne Server** geprüft (statischer Server): Bilder und Links sind da, Formular versteckt, Hinweis sichtbar. Ein Fehler kam dabei ans Licht und wurde behoben: zuerst stand in der zweiten Zeile der Bilder der Werktitel statt der Kategorie („DUNE" statt „SCIENCE FICTION") — Ursache war ein Schritt zu viel im rekursiven Pfad.
- **Offen:** Noch nicht committet. `docs/COVER_KANDIDATEN.md` und `docs/cover-kandidaten.json` sind jetzt reine Recherche-Dokumente und können gelöscht werden, wenn die Liste nicht mehr gebraucht wird. Drei Werke bleiben ohne Wikipedia-Link, weil es keinen Artikel gibt.

### 2026-09-21 – Flask-Backend mit SQLite (Version 0.7)

- **Was:** Die Genre-Bäume sind aus `index.html` in die Datei `data/trees.json` gezogen. `seed.py` schreibt diese Daten in die SQLite-Tabelle `nodes`, `app.py` (Flask) liefert sie über `GET /api/trees`. Das Frontend lädt sie jetzt per `fetch`: zuerst über die API, sonst aus der JSON-Datei. Dazu neu: `.gitignore` (für `__pycache__` und `data/compendium.db`) und `docs/CODE_TOUR.md` — ein Durchlauf durch den Code mit den wichtigsten Fragen und Antworten.
- **Warum:** Im Unterricht wurde gezeigt, wie man Daten mit Flask aus einer SQL-Tabelle lädt. Das war der nächste technische Schritt aus den Notizen.
- **Dateien:** `index.html` (Daten entfernt, `loadTrees()`/`start()` neu), `data/trees.json` (neu), `seed.py` (neu), `app.py` (neu), `.gitignore` (neu), `docs/CODE_TOUR.md` (neu), `README.md`, `Documentation.md` (2.1, 2.2, 2.5, 3, 4.2, 5, 7, 8, 9), `docs/WORKLOG.md`.
- **Ergebnis:** Die Daten wurden nicht per Hand übertragen, sondern per Skript aus dem HTML gezogen. Danach geprüft: `GET /api/trees` liefert exakt dieselben Daten wie `data/trees.json` (62 Knoten, 43 Werke). Im Browser getestet: Drill-Down, Breadcrumb, ★, „Mehr anzeigen", Zurück, Cross-Media-Sprung in den anderen Baum, Baum-Umschalter — keine Fehler. Zusätzlich der Modus **ohne Server** getestet (statischer Server): `/api/trees` gibt 404, die App lädt `data/trees.json` und rendert normal.
- **Offen:** Noch nicht committet. Zwei Zahlen in der Dokumentation waren falsch und wurden korrigiert: dort standen 35 Werke in 13 Kategorien, tatsächlich sind es 43 Werke in 17 Unterkategorien. Neue Abhängigkeit: Flask — nur für das lokale Backend, die Live-Demo braucht es nicht.

- **Gleicher Tag, danach — Titelbilder, Wikipedia-Links und ein Formular:** Neue optionale Felder `cover` (Pfad zum Bild) und `wiki` (Link zum Artikel). Buchkarten zeigen jetzt links das Bild (78 px, 2:3) und darunter die Knöpfe „↗ Wikipedia" und den Cross-Media-Link. Dazu ein Formular „＋ Werk hinzufügen": Kategorie aus einer Liste (17 Unterkategorien mit Pfad), Titel, Autor, Beschreibung, Wikipedia-Link, Bild-Upload, ★. Gespeichert wird über `POST /api/works`, Bilder gehen über `POST /api/covers` nach `data/covers/` und werden über `GET /data/covers/<datei>` ausgeliefert. Das Formular erscheint **nur** mit laufendem Backend; auf GitHub Pages steht dort ein Hinweis. Die Datenbank wird jetzt automatisch neu erzeugt, wenn das Schema sich ändert.
- **Warum:** Der Prototyp soll sich pflegen lassen, ohne `data/trees.json` von Hand zu bearbeiten. Außerdem fehlte zu jedem Werk ein Weg zu mehr Information.
- **Dateien:** `index.html`, `app.py`, `seed.py`, `Documentation.md`, `README.md`, `docs/CODE_TOUR.md`, neu: `docs/COVER_KANDIDATEN.md`, `docs/cover-kandidaten.json`, `data/covers/`.
- **Ergebnis (alles geprüft, nicht nur geschrieben):** Bilder-Upload: PNG → 201, `.exe` → 400, 4 MB → 413, ohne Datei → 400. Werk anlegen: 201; doppelte ID → 409; fehlendes Feld → 400; unbekannte Kategorie → 404; Kategorie ist ein Buch → 400. Round-Trip JSON → Datenbank → API identisch. Schema-Wechsel: Datenbank ohne die neuen Spalten wird beim Start automatisch ersetzt. Alte Karten ohne Bild sehen unverändert aus; „Mehr anzeigen" und der Cross-Media-Sprung funktionieren weiter. Im Modus ohne Server: Formular versteckt, Hinweis sichtbar, Bilder und Links da, keine Fehler außer dem erwarteten 404 auf `/api/trees`. Testwerk und Testbild danach entfernt, `data/trees.json` wieder byte-identisch (SHA-256 geprüft).
- **Offen:** Titelbilder fehlen noch. Befund aus der Recherche: Die deutsche Wikipedia zeigt **keine** Buchcover (nicht-freie Dateien sind dort nicht erlaubt), die englische nur unter „fair use" — das ist für dieses Repository und GitHub Pages rechtlich nicht sauber. Entscheidung nötig: eigene Titelbilder erzeugen oder nur freie Commons-Bilder nehmen. Siehe `docs/COVER_KANDIDATEN.md`. Weiterhin: noch nicht committet. → **Entschieden und umgesetzt** im nächsten Eintrag (Version 0.8): eigene Titelbilder.

### 2026-09-19 – Visuelle Auffrischung der Oberfläche

- **Was:** Nur der `<style>`-Block in `index.html`. Karten sind jetzt gerundet (Radius 14px) und haben weiche Schatten. Beim Hover hebt sich die Karte um 3px. Fließtext nutzt eine Systemschrift, Monospace bleibt für kleine Etiketten. Buttons und der Werk-Zähler sind Pillen, der Werk-Zähler ist ein grüner Chip. Der Titel steht jetzt mittig in einer gesperrten Serifenschrift, der Untertitel kursiv, wie die Titelseite eines Buches. Dazu ein sanfter Hintergrundverlauf, ein Fokus-Rahmen für die Tastatur und ein Block für reduzierte Bewegung.
- **Warum:** Lesbarkeit auf Beamer und in der Video-Aufzeichnung, und eine ruhigere, weichere Oberfläche. Als Vorbild diente die Formensprache von ranobehub.org: runde Karten, Pillen, klare Schrift. Der Aufbau der Seite wurde **nicht** übernommen, nur die Optik.
- **Dateien:** `index.html` (nur CSS), `docs/DESIGN_GUIDE.md` (neu), `docs/WORKLOG.md` (neu), `Documentation.md` (Abschnitt 7 und Changelog 0.6).
- **Ergebnis:** In der lokalen Vorschau geprüft: Kategorie-Karten, Buch-Karten, ★-Markierung, Cross-Media-Link, „Mehr anzeigen", Baum-Umschalter, Escape zurück. Keine Fehler in der Konsole. Farben, Daten und Logik unverändert.
- **Offen:** Noch nicht committet. Vor dem Commit die Checkliste in `docs/DESIGN_GUIDE.md` durchgehen.

### 2026-09-18 – Dokumentation Version 0.5 („Mehr anzeigen")

- **Was:** Abschnitt 4.5 „Aufklappbare Beschreibungen" ergänzt, Hinweis in `renderNode` in Abschnitt 4.2, neue Version 0.5 im Changelog.
- **Warum:** Die Dokumentation endete bei Version 0.4, obwohl die Funktion längst im Code war.
- **Dateien:** `Documentation.md`
- **Ergebnis:** Commit `a78d8f6`, auf `main` gepusht.
- **Offen:** nichts.

### 2026-09-18 – Funktion „Mehr anzeigen"

- **Was:** Lange Buchbeschreibungen werden auf zwei Zeilen begrenzt (`line-clamp`). Ein Button klappt sie auf und zu. Der Button erscheint nur, wenn der Text wirklich abgeschnitten ist.
- **Warum:** Die Beschreibungen sind zwei Sätze lang. Ungeschnitten werden die Karten im Grid unterschiedlich hoch.
- **Dateien:** `index.html`
- **Ergebnis:** im Code vorhanden, Commit `88e4db4`. Der Commit `c0d217e` hat danach nur einen Daten-Eintrag (`world-after-fall`) auf eine Zeile umformatiert.
- **Offen:** nichts. Der Button ist ein echtes `button`-Element und damit mit Tab und Enter erreichbar. Die Escape-Taste bleibt für „Zurück" reserviert.

---

## Nächste Schritte (Stand der Trello-Karte, 2026-09-19)

**In Arbeit**

- Berichtsheft und Tagesdokumentation für die Akademie
- Pitch-Präsentation (.pptx) finalisieren

**Diese Woche (To Do)**

- Zweiten Cross-Media-Link hinzufügen
- Cross-Media-Link testen
- Lesbarkeitstest in 1080p
- Mobile Voreinstellung prüfen
- Breadcrumb bei tiefer Navigation testen
- Demo-Script entwerfen (Text, kein Video)
- Präsentationsfolien strukturieren

**Backlog**

- Echte Datenbank anbinden (MongoDB oder Firebase)
- Layering-System für komplexe Suchfilter entwerfen
- Dritter Baum (Filme und Hörbücher)
- localStorage für Favoriten

**Gelöst am 2026-09-21:** Der Widerspruch ist aufgelöst — beides ist jetzt umgesetzt. `/api/trees` liefert die Daten aus, und dahinter steht eine echte SQLite-Datenbank, die aus `data/trees.json` erzeugt wird. Die Karte `Echte Datenbank anbinden` kann auf „Done". Der Zusatz „MongoDB/Firebase" ist damit erledigt: es ist SQLite geworden, weil es keinen Server braucht.

---

## Regeln für die Arbeit

- Nach jeder fertigen Änderung: ansehen, prüfen, committen. Dann ist die letzte funktionierende Version immer bekannt.
- In den letzten zwei Tagen vor der Abgabe wird nichts Neues gebaut. Diese Tage sind für Übung, Demo-Ablauf und Video.
- Große Schritte kamen nicht in dasselbe Paket wie kleine Korrekturen.
- Keine neuen Funktionen ohne Auftrag. Keine neuen Abhängigkeiten.

Stand: Prototyp, präsentationsbereit.
