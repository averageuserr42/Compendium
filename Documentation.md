# Dokumentation – Compendium

Diese Dokumentation ist für das Bewertungsteam. Sie erklärt die Architektur, die Entscheidungen und die Navigation des Prototyps. Eine kurze Übersicht steht in [README.md](./README.md).

---

## 1. Problem und Lösung

Klassische und Fachliteratur sind über viele Quellen verteilt. Empfehlungssysteme zeigen oft nur populäre Bücher. Sie zeigen aber nicht, was wirklich zu einem Menschen passt. Wer nicht genau weiß, was er sucht, findet selten ein gutes Buch. Viele verlieren daмdurch die Freude am Lesen.

Compendium löst das mit einem **Genre-Baum**. Der Aufbau ist einfach:

- **Wurzel** = Hauptgenre
- **Äste** = Untergenres
- **Blätter** = einzelne Werke

Der Nutzer klickt sich Schritt für Schritt durch den Baum. Er sieht eine klare Struktur statt einer endlosen Liste. Der Start-Inhalt zeigt klassische Werke für ein breites Publikum — nicht nur eine kleine Nische.

**Zielgruppe:** Menschen, die Orientierung suchen — Schüler, Berufseinsteiger, lebenslang Lernende.

---

## 2. Architektur-Entscheidungen

### 2.1 Alles in einer Datei

Der ganze Code liegt in einer einzigen `index.html` — HTML, CSS und JavaScript zusammen. Das ist Absicht. Vorteile für den Prototyp:

- Keine Build-Tools, kein Bundler
- Sofortiges Deployment über GitHub Pages
- Schnelle Änderungen möglich

Eine spätere Aufteilung in Module ist jederzeit möglich. Für die Demo ist sie aber nicht nötig.

### 2.2 JSON statt Datenbank

Die Genre-Bäume sind direkt im JavaScript-Code als Objekt gespeichert. Auch das ist Absicht. Vorteile:

- Kein Backend nötig
- Keine Hosting-Kosten
- Keine Anmeldung, keine Sicherheitsregeln
- Keine Netzwerkabhängigkeit

Eine echte Datenbank (z. B. Firebase oder Flask-Backend, siehe Abschnitt 8) ist im Backlog geplant.

### 2.3 Zwei Bäume statt einem

Der Prototyp hat zwei Bäume:

- `literatureTree` — Belletristik und Fachliteratur
- `novelTree` — Manga und Web-Novels

Beide Bäume nutzen dieselbe Logik und dieselbe Datenstruktur. Das beweist: Die Architektur ist erweiterbar. Ein drittes Baum (z. B. Filme) braucht nur neue Daten und einen neuen Button — keine neuen Funktionen.

### 2.4 Keine externen Abhängigkeiten

Es werden nur HTML5, CSS3 und Vanilla JavaScript verwendet. Keine Frameworks, keine Bibliotheken. Das bedeutet: weniger Wartung, weniger Fehlerquellen, keine Einarbeitung in fremde Tools.

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
| `relatedId` | – | optional, verknüpftes Werk |
| `relatedTitle` | – | optional, Name der Verknüpfung |

Zwei Bäume werden im Objekt `trees` gespeichert:

- **`literatureTree`** — Belletristik (Science Fiction, Fantasy, Weltliteratur) und Fachliteratur (Informatik, Philosophie, Wissenschaft & Gesellschaft)
- **`novelTree`** — Manga (Shonen, Seinen, Shoujo) und Web-Novels (Light Novels, Isekai, koreanische, chinesische)

Die Anzeigenamen für die Kopfzeile stehen in `treeLabels`. Dadurch kann man einen Baum umbenennen, ohne die Daten zu ändern.

**Aktueller Umfang:** 35 Werke in 13 Kategorien.

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

- **`renderNode(node)`** — zeigt die Kinder eines Knotens als Karten. Kategorien sind klickbar, Bücher nicht.
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

---

## 5. Cross-Media-Verknüpfung

Ein Buch kann optional mit einem Werk im anderen Baum verknüpft werden. Dafür gibt es die Felder `relatedId` und `relatedTitle`. Auf der Buch-Karte erscheint dann ein Button mit dem Symbol `↔`. Ein Klick darauf ruft `navigateTo()` auf und springt zum verknüpften Werk — auch in den anderen Baum.

**Aktuelles Beispiel:** Der Roman *No Longer Human* von Osamu Dazai ↔ die Manga-Adaption von Junji Ito.

Diese Funktion war ursprünglich nur als Roadmap-Ziel geplant. Sie ist aber schon als Basis umgesetzt. Das zeigt: Die Architektur ist wirklich erweiterbar, nicht nur auf dem Papier. Weitere Verknüpfungen sind im Backlog.

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

**Lesbarkeit:** Die Schriftgrößen wurden für Video und Online-Präsentationen erhöht (`h3`: 1.25 rem, `p`: 1 rem, `line-height`: 1.65).

---

## 8. Grenzen und Backlog

Aktuelle Grenzen:

- Keine Datenbank — die Daten sind hartcodiert.
- Keine Build-Pipeline, keine Module.
- Keine automatisierten Tests.
- Nur eine Cross-Media-Verknüpfung.
- Keine Suche und keine Filter.

**Nächster Schritt: Flask-Backend**

Im Unterricht wurde ein einfaches Flask-Beispiel gezeigt:

- Das Frontend ruft mit `fetch("/api/begruessung")` einen Endpunkt auf.
- Das Backend antwortet mit JSON.
- Das Frontend zeigt die Daten an.

Dieses Muster ist ein guter nächster Schritt für Compendium. Statt die Genre-Bäume direkt im JavaScript zu speichern, könnten sie über einen Flask-Endpunkt geladen werden. Vorteile:

- Die Daten sind vom Code getrennt.
- Neue Werke können ohne Code-Änderung hinzugefügt werden.
- Flask ist leichtgewichtig und gut für den Einstieg geeignet.

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

---

*Stand: Prototyp, präsentationsbereit.*