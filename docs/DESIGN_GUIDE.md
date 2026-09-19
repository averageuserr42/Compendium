# Design-Leitfaden – Compendium

Diese Datei erklärt, wie die Oberfläche aussieht und wie man sie ändert.
Sie ist für die eigene Weiterarbeit gedacht.
Die fachliche Dokumentation für das Bewertungsteam steht in [Documentation.md](../Documentation.md).

Kurzfassung: **Die Farben bleiben, die Form darf sich ändern.**

---

## 1. Zwei Schichten

Die Darstellung hat zwei Schichten:

1. **Farben.** Sie stehen als Variablen in `:root`. Sie sind Teil der Marke und in `Documentation.md`, Abschnitt 7, beschrieben.
2. **Form.** Radien, Schatten, Abstände und Schriften. Diese Werte sind reine Darstellung. Man kann sie ändern, ohne die Farbwelt zu berühren.

Alle Änderungen in diesem Leitfaden betreffen nur den `<style>`-Block in `index.html`. Am JavaScript wird nichts geändert.

---

## 2. Schriften

| Variable | Wert | Verwendung |
|---|---|---|
| `--serif` | `Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Book Antiqua', Times, serif` | Titel COMPENDIUM und Untertitel |
| `--sans` | `system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif` | Fließtext, Karten-Überschriften, Beschreibungen |
| `--mono` | `ui-monospace, 'Cascadia Mono', 'Courier New', monospace` | kleine Etiketten: Werk-Zähler, Autor, Legende |

**Warum diese Aufteilung:** Eine Monospace-Schrift ist auf einem Beamer und in einer Video-Aufzeichnung schwer zu lesen. Für den Fließtext ist eine normale Schrift besser. Der technische Akzent bleibt in den kleinen Etiketten erhalten.

**Der Titel:** Der Titel steht in `--serif`, ist gesperrt (`letter-spacing: 0.16em`) und mittig. Der Untertitel nutzt dieselbe Schrift, aber kursiv. Das ergibt eine Titelseite, wie man sie aus Büchern kennt. Auch hier gilt: nur Systemschriften, es wird nichts nachgeladen.

**Keine externen Schriften.** Beide Stapel nutzen nur Schriften, die auf dem Gerät vorhanden sind. Es wird nichts nachgeladen. Die Aussage „keine externen Abhängigkeiten" bleibt damit richtig.

---

## 3. Karten

Eine Karte ist ein Rechteck mit drei Merkmalen:

- Radius: `--radius-card` (14px)
- Rand: 1px in `--border` (`#232a24`)
- Schatten: `--shadow-card`

Kategorie-Karte und Buch-Karte unterscheiden sich über einen farbigen Balken links:

| Element | Balken | Bedeutung |
|---|---|---|
| Kategorie | `--green` | klickbar |
| Buch | `--green-dim` | nicht klickbar |

**Wichtig:** Der Balken ist kein `border-left`, sondern ein `inset`-Schatten.

```css
box-shadow: inset 3px 0 0 var(--green), var(--shadow-card);
```

Ein `border-left` würde an den runden Ecken abgeschnitten. Der `inset`-Schatten folgt der Rundung. Das ist der Grund für diese Lösung.

---

## 4. Pillen und Chips

`--radius-pill` (999px) macht aus schmalen Elementen Pillen:

- Baum-Umschalter (`.tree-btn`)
- Zurück-Button (`#back-btn`)
- Cross-Media-Link (`.cross-link`)
- Werk-Zähler (`.card .meta`)

Der Werk-Zähler ist ein Chip: grüner Rand, grüner Hintergrund mit 14 Prozent Deckkraft, Monospace-Schrift.

---

## 5. Bewegung

- Beim Rendern kommen die Karten mit `cardIn` herein, 40 Millisekunden Versatz pro Karte.
- Beim Hover hebt sich die Karte um 3px, der Schatten wird größer und der Rand wird grün.
- Der Block `@media (prefers-reduced-motion: reduce)` schaltet Animationen und Übergänge ab, wenn das Betriebssystem das verlangt.

---

## 6. Fokus mit der Tastatur

Buttons zeigen bei Tastatur-Bedienung einen grünen Rahmen (`:focus-visible`).
Betroffen sind: Baum-Umschalter, Zurück-Button, „Mehr anzeigen" und der Cross-Media-Link.
Die Karten sind keine Buttons und bekommen deshalb keinen Fokus-Rahmen.

---

## 7. Was man nicht ändern sollte

1. **Die sechs Farbwerte in `:root`.** Sie stehen in der Dokumentation, Abschnitt 7. Wenn sich ein Wert ändert, muss die Dokumentation mitgeändert werden.
2. **Der Unterschied stark gegen gedämpft.** Kräftiger grüner Balken heißt klickbar, gedämpfter Balken heißt Buch. Ohne diesen Unterschied versteht der Nutzer die Navigation nicht mehr.
3. **Kursiver Buchtitel und Autor in Großbuchstaben.** Das ist die visuelle Hierarchie zwischen Kategorie und Werk.
4. **Kein `display` für `#back-btn` im CSS.** Das JavaScript setzt `display` auf `block` oder `none`. Steht im CSS ein `display`, verschwindet die Schaltfläche nicht mehr.

---

## 8. Rezepte

| Ziel | Änderung |
|---|---|
| Weichere Karten | `--radius-card: 18px;` |
| Weniger Rundung | `--radius-card: 8px;` |
| Ruhigere Oberfläche | kleinere Werte für `--shadow-card` und `--shadow-hover` |
| Ganz ohne Bewegung | den Block `prefers-reduced-motion` dauerhaft greifen lassen, also `animation` der Karte entfernen |
| Zurück zu Monospace | in `body` wieder `font-family: var(--mono);` setzen |
| Neutralere Etiketten | beim Chip `background` und `color` auf `--text-muted` umstellen |

---

## 9. Checkliste vor dem Push

- Seite in 1080p ansehen, so wie sie im Video erscheint.
- Eine Kategorie anklicken, dann ein Buch: funktioniert die Navigation?
- Auf „Mehr anzeigen" klicken: klappt der Text auf und wieder zu?
- Einen Cross-Media-Link anklicken: wechselt die App in den anderen Baum?
- Escape drücken: kommt man eine Ebene zurück?
- Fenster schmal ziehen: brechen die Karten um?
- Prüfen: keine neuen Dateien, keine externen Links, keine Bibliotheken.

Stand: Prototyp, präsentationsbereit.
