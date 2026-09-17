# Dokumentation – Compendium

Diese Dokumentation richtet sich an das Bewertungsteam und beschreibt die Architektur, die getroffenen Entscheidungen sowie die aktuelle Navigationslogik des Prototyps. Für eine kurze Projektübersicht siehe [README.md](./README.md).

---

## 1. Problemstellung und Lösungsansatz

Klassische und Fachliteratur sind über unzählige Quellen verstreut, und gängige Empfehlungssysteme optimieren auf Popularität statt auf tatsächliche Passung. Wer nicht bereits weiß, wonach er sucht, findet selten Bücher, die wirklich zu ihm passen — und verliert das Interesse am Lesen.

Compendium begegnet dem mit einem **Genre-Baum**: Wurzel (Hauptgenre) → Äste (Untergenres) → Blätter (einzelne kuratierte Werke). Der Nutzer navigiert aktiv durch eine überschaubare Struktur, anstatt sich durch endlose Empfehlungslisten zu scrollen. Der Fokus liegt bewusst auf klassischen, breit zugänglichen Werken statt auf einer engen Nische.

**Zielgruppe:** Leserinnen und Leser, die Orientierung suchen — von Schülern über Berufseinsteiger bis zu lebenslang Lernenden.

---

## 2. Architekturentscheidungen

### 2.1 Single-File-Prototyp

Der gesamte Code (HTML, CSS, JavaScript) liegt aktuell in einer einzigen `index.html`. Das ist eine bewusste Entscheidung für die Prototyp-Phase: keine Build-Pipeline, kein Bundler, sofortiges Deployment über GitHub Pages, minimaler Overhead für schnelle Iteration. Eine spätere Auftrennung in Module ist jederzeit möglich, aber für die Demonstration des Kernkonzepts nicht erforderlich.

### 2.2 JSON statt Datenbank

Die Genre-Bäume sind als hartcodierte JavaScript-Objekte im Code hinterlegt statt in einer externen Datenbank. Auch das ist eine bewusste Prototyp-Entscheidung, kein Zeitmangel: kein Backend, keine Hosting-Kosten, keine Authentifizierung und keine Netzwerkabhängigkeit nötig, um das Kernkonzept zu demonstrieren. Eine Anbindung an eine echte Datenquelle (z. B. Firebase oder ein Flask-Backend, siehe Abschnitt 8) ist im Backlog vorgesehen.

### 2.3 Zwei-Baum-Struktur

Der Prototyp enthält zwei unabhängige Bäume — `literatureTree` (Belletristik, Fachliteratur) und `novelTree` (Manga, Web-Novels) —, die über eine gemeinsame Datenstruktur und identische Navigationslogik funktionieren. Damit wird das Architekturprinzip „ein Muster, mehrere Bäume" praktisch nachgewiesen: ein drittes Baum (z. B. Filme oder Hörbücher) ließe sich allein durch Ergänzung der Daten und einer Kopfzeilen-Schaltfläche hinzufügen, ohne die Navigationslogik zu ändern.

### 2.4 Keine externen Abhängigkeiten

Es werden ausschließlich HTML5, CSS3 (Custom Properties, CSS Grid) und Vanilla JavaScript verwendet. Keine Frameworks, keine Bibliotheken, keine Build-Tools. Das reduziert Angriffsfläche, Wartungsaufwand und Einarbeitungszeit — und stellt sicher, dass der Prototyp langfristig auch ohne Toolchain lauffähig bleibt.

---

## 3. Datenmodell

Jeder Knoten im Baum ist entweder ein **Kategorie-Knoten** oder ein **Buch-Knoten**:

| Feld | Kategorie-Knoten | Buch-Knoten (`isBook: true`) |
|---|---|---|
| `id` | eindeutige ID (global) | eindeutige ID (global) |
| `title` | Anzeigename | Buchtitel |
| `desc` | Kurzbeschreibung | Beschreibung (2 Sätze) |
| `children` | Array weiterer Knoten | – |
| `author` | – | Autor |
| `recommended` | – | optional (Boolean), zeigt ★-Markierung |
| `relatedId` | – | optional, ID des verknüpften Werks im anderen Baum |
| `relatedTitle` | – | optional, Anzeigename der Verknüpfung |

Zwei unabhängige Bäume werden im Objekt `trees` zusammengefasst:

- **`literatureTree`** — Belletristik (Science Fiction, Fantasy, Weltliteratur) und Fachliteratur (Informatik & Code, Philosophie, Wissenschaft & Gesellschaft)
- **`novelTree`** — Manga (Shonen, Seinen, Shoujo) und Web-Novels (Light Novels, Isekai, koreanische und chinesische Web-Novels)

Die menschenlesbaren Anzeigenamen für die Kopfzeile sind in `treeLabels` hinterlegt und vom technischen Schlüssel getrennt — Umbenennungen sind dadurch ohne Datenänderung möglich.

**Aktueller Umfang:** 35 kuratierte Werke in 13 Kategorien.

---

## 4. Navigationslogik

### 4.1 Drill-Down und `historyStack`

Die Navigation erfolgt klickbasiert und ohne Page-Reload. Der Zustand wird in zwei Variablen gehalten:

- `currentNode` — der aktuell gerenderte Knoten.
- `historyStack` — Array der bisher besuchten Elternknoten; ermöglicht Zurück-Navigation durch `pop()`.

Beim Klick auf eine Kategorie wird der aktuelle Knoten auf den Stack gelegt und der neue Knoten gerendert. Beim Klick auf „Zurück" wird der letzte Knoten wieder ausgelesen.

### 4.2 Kernfunktionen

- **`renderNode(node)`** — rendert die Kinder des aktuellen Knotens als Grid aus `.card`-Elementen. Unterscheidet zwischen Kategorie-Karten (klickbar, navigiert eine Ebene tiefer) und Buch-Karten (nicht klickbar, zeigt Titel/Autor/Beschreibung).
- **`findPath(node, targetId)`** — rekursive Tiefensuche, die den vollständigen Pfad von der Wurzel bis zu einem Knoten mit gegebener `id` zurückgibt. Grundlage für baumübergreifende Sprünge.
- **`navigateTo(targetId)`** — durchsucht beide Bäume nach einer Ziel-`id` und aktualisiert `activeTreeKey`, `historyStack` und `currentNode`. Wird für Cross-Links genutzt. Falls das Ziel ein Buch ist, wird zur übergeordneten Kategorie gesprungen, damit der Nutzer das Werk im Kontext sieht.
- **`switchTree(key)`** — wechselt über die Buttons im Header zwischen `literature` und `novels`. Der `historyStack` wird dabei zurückgesetzt, um Fehlnavigation über Baumgrenzen hinweg zu vermeiden.
- **`countWorks(node)`** — zählt rekursiv, wie viele Bücher unter einem Kategorie-Knoten liegen, für die Anzeige „X Werke" auf den Karten.

### 4.3 Breadcrumb-Navigation

Unterhalb der Kopfzeile wird der aktuell navigierte Pfad angezeigt (z. B. `Literatur › Belletristik › Science Fiction`). Diese Anzeige macht die hierarchische Struktur unmittelbar sichtbar und dient gleichzeitig als Orientierungshilfe für den Nutzer.

### 4.4 Tastatursteuerung und Animation

- Die **Escape-Taste** löst dieselbe Aktion aus wie der „Zurück"-Button — ein Detail, das die Bedienung flüssiger macht.
- Beim Rendern eines Knotens werden die Karten mit einer kurzen Einblendanimation (`@keyframes cardIn`, gestaffelt um 40 ms pro Karte) versehen. Das verbessert die visuelle Wahrnehmung insbesondere bei Video- und Online-Präsentationen.

---

## 5. Cross-Media-Verknüpfung

Buch-Knoten können optional `relatedId` und `relatedTitle` besitzen, um sie mit einem thematisch verwandten Werk im jeweils anderen Baum zu verknüpfen. Auf der Buch-Karte erscheint dafür ein `.cross-link`-Button; ein Klick darauf ruft `navigateTo(relatedId)` auf und springt direkt — auch baumübergreifend — zum verknüpften Werk.

**Aktuell umgesetztes Beispiel:** der Roman *No Longer Human* von Osamu Dazai ↔ die gleichnamige Manga-Adaption von Junji Ito.

Diese Verknüpfung war ursprünglich als späteres Roadmap-Ziel vorgesehen und ist im aktuellen Stand bereits als Basis-Implementierung vorhanden. Sie demonstriert, dass die Architektur nicht nur behauptet, sondern tatsächlich erweiterbar ist. Weitere Verknüpfungen sind im Backlog vorgesehen.

---

## 6. Kuratierungssystem (★-Empfehlungen)

Compendium positioniert sich bewusst als Alternative zu algorithmischen Empfehlungssystemen. Buch-Knoten können mit dem Feld `recommended: true` ausgezeichnet werden; in der Oberfläche erscheint dann ein ★-Symbol vor dem Titel. Eine Legende im Kopfbereich erklärt die Bedeutung: *„★ Persönlich gelesen und empfohlen"*.

**Grundidee:** Nicht Beliebtheit oder Klickzahlen bestimmen die Empfehlung, sondern die tatsächliche, persönliche Leseerfahrung des Kurators. Damit wird der zentrale Kritikpunkt an bestehenden Empfehlungssystemen (Optimierung auf Popularität statt auf Passung) unmittelbar adressiert.

**Aktueller Stand:** 13 Werke sind mit ★ ausgezeichnet, verteilt über beide Bäume und mehrere Kategorien.

---

## 7. Design-System

Der Prototyp verwendet ein dunkles Farbschema im „Matrix"-Stil, das sich an das persönliche Portfolio des Autors anlehnt. Alle Farben sind als CSS Custom Properties zentral definiert:

| Variable | Wert | Verwendung |
|---|---|---|
| `--bg` | `#0A0A0A` | Seitenhintergrund |
| `--card-bg` | `#121712` | Kartenhintergrund |
| `--green` | `#33FF66` | Akzent, Hover, aktive Elemente |
| `--green-dim` | `#1F8F44` | Rahmen, gedämpfter Akzent |
| `--text-white` | `#FFFFFF` | Überschriften |
| `--text-muted` | `#9FCDAF` | Fließtext, Beschreibungen |

**Visuelle Hierarchie:** Kategorie-Karten tragen eine kräftige linke Rahmenlinie in `--green` und sind klickbar. Buch-Karten haben eine gedämpfte Rahmenlinie in `--green-dim`, einen kursiven Titel und einen Autor in Großbuchstaben — sie sind bewusst nicht klickbar.

**Lesbarkeit für Präsentationen:** Schriftgrößen wurden gegenüber dem ersten Prototyp erhöht (`h3`: 1.25 rem, `p`: 1 rem, `line-height`: 1.65), um auch bei Video- und Online-Präsentationen (z. B. über Microsoft Teams oder Aufzeichnung in 1080p) gut lesbar zu bleiben.

---

## 8. Bekannte Einschränkungen und Backlog

- Keine Persistenz- oder Datenbank-Anbindung — die Daten sind hartcodiert im JavaScript.
- Keine Build-Pipeline und keine Modultrennung (bewusst, siehe 2.1).
- Kein automatisiertes Testing.
- Aktuell ist eine Cross-Media-Verknüpfung umgesetzt; weitere sind geplant.
- Keine Suchfunktion und keine Filter; die Navigation ist bewusst explorativ.
- **Mögliche nächste Ausbaustufe:** Backend-Anbindung, z. B. nach dem im Unterricht gezeigten Flask-Muster (Frontend ruft einen JSON-Endpunkt per `fetch` ab, statt Daten hart zu codieren) als leichtgewichtige Alternative zu Firebase.

---

## 9. Changelog

### Version 0.1 — Erster Prototyp
- Einzelner Literatur-Baum (`genreTree`)
- Drill-Down-Navigation mit `historyStack` und Zurück-Button
- Grundlegende Buch- und Kategorie-Karten

### Version 0.2 — Zweiter Baum und Cross-Media
- Zweiter Baum (`novelTree`) für Manga und Web-Novels
- Baum-Umschalter (`switchTree`) in der Kopfzeile
- Erste Cross-Media-Verknüpfung (*No Longer Human*: Roman ↔ Manga)
- `findPath()` und `navigateTo()` für baumübergreifende Sprünge

### Version 0.3 — Inhalte und Kuratierung
- Content auf 35 Werke in 13 Kategorien erweitert
- ★-Empfehlungssystem: persönlich gelesene Werke werden markiert
- Breadcrumb-Navigation
- Werk-Zähler auf Kategorie-Karten

### Version 0.4 — Präsentationsoptimierung
- Schriftgrößen für Video- und Online-Präsentation angepasst
- Karten-Einblendanimation (`cardIn` mit Stagger)
- Escape-Taste als Zurück-Shortcut
- Überarbeitete Farbkontraste für bessere Sichtbarkeit in Aufzeichnungen

---

*Stand: Prototyp, präsentationsbereit.*