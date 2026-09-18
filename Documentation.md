# Compendium - Kontext für KI

## Was ist das

Schulprojekt (Ausbildungs-Präsentation) auf Deutsch. Aufgabe: "Entwickle eine Idee für eine App oder Website, die ein soziales oder ökologisches Problem löst, und präsentiere sie überzeugend". Ton: seriös und akademisch. Sprache: Deutsch.

Deadlines: Präsentation am Ende der nächsten Woche. Format: Video oder online über Teams.

## Autor

Autodidaktischer IT-Azubi (Fachinformatiker Systemintegration), Deutsch auf B1-Niveau. Arbeitet solo, ohne Team. Führt das Projekt über Trello in Sprints. Will direktes ehrliches Feedback ohne Komplimente. Antworten auf Russisch, wenn nicht anders gewünscht.

## Problem und Lösung

**Problem.** Klassische und Fachliteratur sind über viele Quellen verstreut. Empfehlungssysteme optimieren auf Popularität statt auf Passung zu den eigenen Interessen. Menschen verlieren das Interesse am Lesen.

**Lösung.** Genrebaum: hierarchische Navigation. Wurzel (Hauptgenre), dann Äste (Untergenres), dann Blätter (konkrete Werke). Der Nutzer geht selbst einen Pfad durch die Struktur, statt endlose Listen zu scrollen.

**Unterschied zu bestehenden Systemen.** Empfehlungen sind manuell kuratiert (Stern), nicht algorithmisch.

## Tech Stack

- HTML5, CSS3 (Custom Properties, CSS Grid), Vanilla JavaScript
- Keine Frameworks, keine Bibliotheken, keine externen Abhängigkeiten
- Alles in einer Datei `index.html`, bewusste Entscheidung für den Prototyp
- Daten: zwei verschachtelte JSON-Objekte (`literatureTree`, `novelTree`)
- Navigation: Drill-Down, `historyStack` für "Zurück", `renderNode` ohne Page-Reload

## Design-System

Dark bzw. "Matrix"-Stil. CSS-Variablen in `:root`:

```
--bg:         #0A0A0A
--card-bg:    #121712
--green:      #33FF66
--green-dim:  #1F8F44
--text-white: #FFFFFF
--text-muted: #9FCDAF
```

Große Schriften für die Lesbarkeit im Video: `h3` 1.25rem, `p` 1rem, `line-height` 1.65.

## Aktueller Stand des Codes

### Zwei Bäume

```js
const trees = {
    literature: literatureTree,   // Belletristik + Fachliteratur
    novels: novelTree             // Manga + Web-Novels
};

const treeLabels = {
    literature: 'Literatur',
    novels: 'Manga & Web-Novels'
};
```

### Struktur eines Knotens

Kategorie:
```js
{ id, title, desc, children: [...] }
```

Buch:
```js
{
    isBook: true,
    id,                    // eindeutig über beide Bäume
    title, author,
    recommended: true,     // optional, zeigt Stern
    desc,                  // 2 Sätze auf Deutsch
    relatedId,             // optional, Cross-Media
    relatedTitle
}
```

### Kernfunktionen

- `renderNode(node)`: rendert die Kinder als Karten im Grid. Bei Büchern prüft die Funktion nach dem Rendern, ob die Beschreibung abgeschnitten ist, und fügt dann den Button "Mehr anzeigen" ein (Klasse `expanded` an `.desc` wird umgeschaltet).
- `findPath(node, targetId)`: rekursive Suche des Pfads von der Wurzel bis zum Knoten
- `navigateTo(targetId)`: Sprung zu einem Knoten, auch in den anderen Baum (Cross-Media)
- `switchTree(key)`: Wechsel zwischen den Bäumen, setzt `historyStack` zurück
- `countWorks(node)`: rekursive Zählung der Bücher unter einer Kategorie
- `updateBreadcrumb()`: Pfad im Stil `Literatur › Belletristik › Science Fiction`

### State

- `currentNode`: der aktuell angezeigte Knoten
- `historyStack`: Array der besuchten Knoten
- `activeTreeKey`: welcher Baum aktiv ist (`'literature'` oder `'novels'`)

### Implementierte Funktionen

- Zwei Bäume mit Umschalter
- Drill-Down-Navigation
- Zurück-Button plus Escape als Shortcut
- Breadcrumb-Navigation
- Zähler "X Werke" auf den Kategorien
- Stern-System (13 Bücher markiert)
- Cross-Media-Sprung: Roman *No Longer Human* ↔ Manga-Adaption
- Karten-Animation (fadeIn mit Stagger 40ms)
- Große Schriften für das Video
- Button "Mehr anzeigen" / "Weniger anzeigen" zum Aufklappen langer Buchbeschreibungen. Der Text wird auf 2 Zeilen begrenzt (line-clamp). Der Button erscheint nur, wenn der Text wirklich abgeschnitten ist (Prüfung scrollHeight gegen clientHeight in renderNode).

### Aktueller Umfang

- 2 Bäume
- 13 Kategorien
- 35 Werke
- 13 davon mit Stern

**Wichtig:** Die Sterne-Bücher sind wirklich vom Autor gelesen. Nicht entfernen und nicht ergänzen ohne seine Bestätigung. Liste: 1984, Die letzte Frage, Auferstehung, Der Meister und Margarita, Der Alchimist, Auf dem Jakobsweg, Die Kunst des Seins, Sapiens, LSD: Mein Sorgenkind, Solo Leveling, The Legendary Moonlight Sculptor, The World After the Fall, The Legendary Mechanic.

## Wichtige Details (nicht in dieselben Fallen treten)

1. **Ein Buch ist ein Blatt.** Es hat kein `children`. Wenn `renderNode` ein Buch bekommt, bricht es. Deshalb springt `navigateTo` zur Elternkategorie des Buchs, nicht zum Buch selbst.
2. **`switchTree` setzt `historyStack` zurück.** Sonst führt "Zurück" in den anderen Baum. Klassischer Bug in der Demo.
3. **`id` ist global eindeutig** über beide Bäume. Nicht nur innerhalb eines Baums.
4. **Daten sind auf Deutsch.** Buchtitel auf Deutsch, wo es eine offizielle Übersetzung gibt. Koreanische und chinesische Web-Novels bleiben auf Englisch.
5. **In renderNode wird der Button "Mehr anzeigen" nach `.desc` eingefügt.** Reihenfolge nicht ändern: der Cross-Link kommt nach dem Toggle, nicht umgekehrt.

## Was schon erledigt ist

- Voll funktionsfähiger Prototyp, live Demo
- README.md auf GitHub
- DOCUMENTATION.md mit Architektur, Daten, Navigation, Changelog (eine Version auf B1-Niveau vorhanden)
- Trello-Board: Backlog / To Do / In Progress / Done
- Zwischen-Fazit Dokument für die Schule (hochgeladen)
- Spickzettel für Obsidian

## Nächste Schritte (Prioritäten)

1. **Flask-Backend**: der nächste technische Schritt. Ziel: `trees` aus dem JS in einen API-Endpunkt `/api/trees` auslagern, damit die Daten dynamisch über `fetch` geladen werden. Die Lehrerin hat dieses Muster im Unterricht gezeigt, der Autor will es ausprobieren.
2. **Zweite Cross-Media-Verknüpfung**: aktuell eine (No Longer Human), eine weitere dazu.
3. **Vorbereitung Abschlusspräsentation**: Folien, Struktur, Demo-Route.
4. **Mögliche Fragen der Lehrerin**: antizipieren und Antworten vorbereiten.

## Links

- Repository: https://github.com/averageuserr42/Compendium
- Live-Demo: https://averageuserr42.github.io/Compendium/
- Trello: privates Board (der Autor schickt bei Bedarf Screenshots)

## Deutsche Schlüsselsätze für die Verteidigung

- "Die Architektur ist datengetrieben: neue Inhalte erfordern keine Code-Änderungen."
- "Cross-Media-Verknüpfungen sind kein Roadmap-Punkt, sie funktionieren bereits."
- "Wir verzichten bewusst auf einen Backend-Stack, weil der Prototyp ohne Server vollständig funktionsfähig ist."
- "Die Empfehlungen sind kuratiert, nicht algorithmisch. Alle Sterne-Werke habe ich selbst gelesen."
- "Zwei Bäume beweisen: die Architektur ist erweiterbar."

## Sätze zur Autorenschaft (häufige Frage der Lehrkräfte)

- "Ich habe alles selbst geschrieben." (Alles selbst geschrieben.)
- "Ich habe keine Frameworks verwendet." (Keine Frameworks benutzt.)
- "KI habe ich zum Debuggen und für die Dokumentation benutzt." (KI nur fürs Debuggen und die Doku.)
- "Die Idee und der Code sind von mir." (Idee und Code sind meine.)

## Regel für russische Antworten

Der Autor übersetzt wörtlich, deshalb zerbrechen komplizierte deutsche Konstrukte den Sinn. Auf Russisch einfache Formulierungen benutzen, keine langen verschachtelten Sätze. Wenn deutscher Text nötig ist: nicht wörtliche Übersetzung, sondern natürliches Deutsch, mit Vermerk "vereinfacht".

## Was nicht tun

- Firebase nicht als "richtige" Wahl für den Prototyp vorschlagen, wurde besprochen und verschoben.
- Keine Funktionen ohne Auftrag ergänzen (Suche, Filter, Routing), das verteilt den Fokus.
- Bestehenden Code nicht "für die Sauberkeit" umschreiben ohne ausdrückliche Bitte.
- Keine übertriebenen Komplimente, der Autor will direktes Feedback.

---

# Changelog

### Version 0.1 - Erster Prototyp
- Ein Literatur-Baum (`genreTree`)
- Drill-Down-Navigation mit `historyStack` und Zurück-Button
- Grundlegende Buch- und Kategorie-Karten

### Version 0.2 - Zweiter Baum und Cross-Media
- Zweiter Baum (`novelTree`) für Manga und Web-Novels
- Baum-Umschalter (`switchTree`) in der Kopfzeile
- Erste Cross-Media-Verknüpfung (*No Longer Human*: Roman ↔ Manga)
- `findPath()` und `navigateTo()` für Sprünge über Baumgrenzen

### Version 0.3 - Inhalte und Kuratierung
- Umfang auf 35 Werke in 13 Kategorien erweitert
- Stern-System: persönlich gelesene Werke werden markiert
- Breadcrumb-Navigation
- Werke-Zähler auf den Kategorie-Karten

### Version 0.4 - Präsentationsoptimierung
- Schriftgrößen für Video- und Online-Präsentation angepasst
- Karten-Einblendanimation (`cardIn` mit Stagger)
- Escape-Taste als Zurück-Shortcut
- Überarbeitete Farbkontraste für bessere Sichtbarkeit in Aufzeichnungen

### Version 0.5 - Mehr anzeigen
- Lange Buchbeschreibungen werden auf 2 Zeilen begrenzt (CSS line-clamp)
- Button "Mehr anzeigen" / "Weniger anzeigen" klappt den Text auf und zu
- Der Button wird nur eingefügt, wenn die Beschreibung wirklich abgeschnitten ist
- Wichtig: Der Button wird NACH `.desc` eingefügt (afterend). Reihenfolge in der Buchkarte: Titel, Autor, Beschreibung, Toggle, Cross-Link