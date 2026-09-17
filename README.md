# Compendium - Prototyp

**Ein neuer Zugang zur Literatur. Ordnung im Meer der Bücher.**

## Über das Projekt
Compendium ist ein Proof-of-Concept für eine strukturierte Literatur-Navigation. Statt auf Bestseller-Listen oder Black-Box-Algorithmen zu setzen, nutzt Compendium einen **Genre-Baum**, um Leser von der Wurzel (Hauptkategorie) über die Äste (Untergenres) bis zu den Blättern (einzelne kuratierte Werke) zu führen.

## Aktueller Stand (Prototyp)
Dieses Repository enthält den interaktiven Frontend-Prototypen, der das Kernkonzept demonstriert:
- Verschachtelte JSON-Datenstruktur für den Genre-Baum.
- Dynamisches DOM-Rendering mittels Vanilla JavaScript.
- Klick-basierte Navigation (Drill-Down) durch die Kategorien.
- **Zwei parallele Bäume:** Literatur (Belletristik / Fachliteratur) und Manga & Web-Novels, umschaltbar über einen Tree-Switcher im Header.
- **Erste Cross-Media-Verknüpfungen** zwischen thematisch verwandten Werken aus beiden Bäumen (z. B. Roman ↔ Manga-Adaption desselben Stoffs) — ursprünglich als späteres Roadmap-Ziel geplant, jetzt als Basis-Implementierung vorhanden.
- Integriertes Design-System (Dark-Theme mit Akzentfarben, "Matrix"-Stil).

Für Details zur Architektur und den Designentscheidungen siehe [Documentation.md](./Documentation.md).

## Tech Stack
- HTML5
- CSS3 (Custom Properties, CSS Grid)
- Vanilla JavaScript (DOM Manipulation, JSON Handling)

## Setup / Demo
Das Projekt besteht aktuell aus einer einzigen `index.html` Datei ohne externe Abhängigkeiten.
👉 **[Hier klicken für die Live-Demo](https://averageuserr42.github.io/Compendium/)**
