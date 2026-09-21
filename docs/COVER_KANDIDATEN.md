# Kandidaten für Titelbilder (Recherche-Archiv)

> **Erledigt am 2026-09-21.** Die Entscheidung ist gefallen: **eigene Titelbilder**, typografisch, für alle 43 Werke (nicht die freien Commons-Bilder). Umgesetzt in `generate_covers.py`; die geprüfte Linkliste steht dort als `WIKI_LINKS`. Diese Datei ist damit nur noch Archiv — sie darf gelöscht werden, die Ergebnisse sind in `Documentation.md` (Abschnitt 2.6) und im Skript festgehalten.

Diese Liste ist ein **Vorschlag, keine Entscheidung**. Es wurde **nichts heruntergeladen**.

## Kurz gesagt

- 35 Artikel sind automatisch gefunden und in Ordnung.
- 5 Treffer müssen angesehen werden.
- 3 Werke haben keinen Link — die trägst du selbst ein.
- Bilder gibt es nur bei einem Teil der Artikel, und **nur in der englischen Wikipedia** sind Buchcover dabei. Siehe „Rechtlicher Hinweis" unten.

## Wie die Liste entstanden ist

1. Direkte Abfrage des Titels in der Wikipedia (deutsch, dann englisch), mit Weiterleitungen.
2. Für den Rest: Suche nach dem Titel.
3. Verglichen wurde normalisiert (Kleinschreibung, Umlaute, Klammern, führende Artikel).
4. „Sicher" = Artikeltitel passt zum Werktitel. „Bitte prüfen" = der Treffer kann falsch sein.

**Warum nicht automatisch:** Eine Suche ohne Autor lieferte für „1984" ein Foto von Indira Gandhi — der Artikel `1984` handelt vom Jahr. Und „Meditationen" führte zu Descartes statt zu Mark Aurel. Solche Treffer findet man nur beim Hinsehen. Genau das ist unten korrigiert.

## Rechtlicher Hinweis (wichtig für die Bewertung)

Die deutsche Wikipedia zeigt **keine Buchcover**, weil dort keine nicht-freien Dateien erlaubt sind. Geprüft an „Der Herr der Ringe", „Der Alchimist", „Foundation", „Neuromancer" — alle ohne Titelbild.
Cover gibt es fast nur in der **englischen** Wikipedia, und dort unter „fair use". Diese Begründung gilt für Wikipedia, **nicht** für dieses Repository und nicht für GitHub Pages. Ein solches Bild herunterzuladen und zu veröffentlichen ist rechtlich nicht sauber.
Frei nutzbar sind nur alte, gemeinfreie Abbildungen von Wikimedia Commons (zum Beispiel Kafka-Ausgaben).

**Zwei saubere Wege:**
- **Empfehlung:** Titelbilder selbst erzeugen — Titel und Autor in den Farben und Formen des Projekts. Rechtlich einwandfrei, alle 43 Werke sehen einheitlich aus, und es passt zum Design-System.
- Oder nur die wenigen freien Commons-Bilder nehmen und die übrigen Karten ohne Bild lassen (die Karte sieht dann aus wie bisher).

## Passt (35)

| Werk | Artikel | Bild | Datei-Vorschlag |
|---|---|---|---|
| Dune (Frank Herbert) | [Dune](https://de.wikipedia.org/wiki/Dune) (de) | ja | `data/covers/dune.org&utm_campaign=api&utm_content=thumbnail` |
| Foundation (Isaac Asimov) | [Foundation](https://de.wikipedia.org/wiki/Foundation) (de) | nein | `data/covers/foundation.jpg` |
| Fahrenheit 451 (Ray Bradbury) | [Fahrenheit 451](https://de.wikipedia.org/wiki/Fahrenheit_451) (de) | nein | `data/covers/fahrenheit.jpg` |
| Neuromancer (William Gibson) | [Neuromancer](https://de.wikipedia.org/wiki/Neuromancer) (de) | nein | `data/covers/neuromancer.jpg` |
| Der Herr der Ringe (J.R.R. Tolkien) | [Der Herr der Ringe](https://de.wikipedia.org/wiki/Der_Herr_der_Ringe) (de) | nein | `data/covers/lotr.jpg` |
| Der Hobbit (J.R.R. Tolkien) | [Der Hobbit](https://de.wikipedia.org/wiki/Der_Hobbit) (de) | ja | `data/covers/hobbit.org&utm_campaign=api&utm_content=thumbnail` |
| Auferstehung (Leo Tolstoi) | [Auferstehung](https://de.wikipedia.org/wiki/Auferstehung) (de) | nein | `data/covers/auferstehung.jpg` |
| Der Meister und Margarita (Michail Bulgakow) | [Der Meister und Margarita](https://de.wikipedia.org/wiki/Der_Meister_und_Margarita) (de) | ja | `data/covers/meister-margarita.org&utm_campaign=api&utm_content=thumbnail` |
| Der Alchimist (Paulo Coelho) | [Der Alchimist](https://de.wikipedia.org/wiki/Der_Alchimist) (de) | nein | `data/covers/alchimist.jpg` |
| Der Process (Franz Kafka) | [Der Process](https://de.wikipedia.org/wiki/Der_Process) (de) | ja | `data/covers/process.org&utm_campaign=api&utm_content=thumbnail` |
| Die Verwandlung (Franz Kafka) | [Die Verwandlung](https://de.wikipedia.org/wiki/Die_Verwandlung) (de) | ja | `data/covers/verwandlung.org&utm_campaign=api&utm_content=thumbnail` |
| Schuld und Sühne (Fjodor Dostojewski) | [Schuld und Sühne](https://de.wikipedia.org/wiki/Schuld_und_S%C3%BChne) (de) | ja | `data/covers/schuld.org&utm_campaign=api&utm_content=thumbnail` |
| Clean Code (Robert C. Martin) | [Clean Code](https://de.wikipedia.org/wiki/Clean_Code) (de) | nein | `data/covers/clean-code.jpg` |
| The Pragmatic Programmer (Hunt & Thomas) | [The Pragmatic Programmer](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) (en) | nein | `data/covers/pragmatic.jpg` |
| Refactoring (Martin Fowler) | [Refactoring](https://de.wikipedia.org/wiki/Refactoring) (de) | nein | `data/covers/refactoring.jpg` |
| Der Mythos des Sisyphos (Albert Camus) | [Der Mythos des Sisyphos](https://de.wikipedia.org/wiki/Der_Mythos_des_Sisyphos) (de) | ja | `data/covers/sisyphos.org&utm_campaign=api&utm_content=thumbnail` |
| Also sprach Zarathustra (Friedrich Nietzsche) | [Also sprach Zarathustra](https://de.wikipedia.org/wiki/Also_sprach_Zarathustra) (de) | ja | `data/covers/zarathustra.org&utm_campaign=api&utm_content=thumbnail_unscaled` |
| One Piece (Eiichiro Oda) | [One Piece](https://de.wikipedia.org/wiki/One_Piece) (de) | nein | `data/covers/one-piece.jpg` |
| Attack on Titan (Hajime Isayama) | [Attack on Titan](https://de.wikipedia.org/wiki/Attack_on_Titan) (de) | nein | `data/covers/aot.jpg` |
| Fullmetal Alchemist (Hiromu Arakawa) | [Fullmetal Alchemist](https://de.wikipedia.org/wiki/Fullmetal_Alchemist) (de) | ja | `data/covers/fma.org&utm_campaign=api&utm_content=thumbnail_unscaled` |
| Berserk (Kentaro Miura) | [Berserk](https://de.wikipedia.org/wiki/Berserk) (de) | ja | `data/covers/berserk.org&utm_campaign=api&utm_content=thumbnail_unscaled` |
| Monster (Naoki Urasawa) | [Monster](https://de.wikipedia.org/wiki/Monster) (de) | nein | `data/covers/monster.jpg` |
| Fruits Basket (Natsuki Takaya) | [Fruits Basket](https://de.wikipedia.org/wiki/Fruits_Basket) (de) | nein | `data/covers/fruits-basket.jpg` |
| Nana (Ai Yazawa) | [Nana](https://de.wikipedia.org/wiki/Nana) (de) | nein | `data/covers/nana.jpg` |
| Re:Zero (Tappei Nagatsuki) | [Re:Zero](https://en.wikipedia.org/wiki/Re%3AZero) (en) | nein | `data/covers/re-zero.jpg` |
| Overlord (Kugane Maruyama) | [Overlord](https://de.wikipedia.org/wiki/Overlord) (de) | nein | `data/covers/overlord.jpg` |
| Mushoku Tensei (Rifujin na Magonote) | [Mushoku Tensei](https://de.wikipedia.org/wiki/Mushoku_Tensei) (de) | ja | `data/covers/mushoku.org&utm_campaign=api&utm_content=thumbnail` |
| Solo Leveling (Chugong) | [Solo Leveling](https://de.wikipedia.org/wiki/Solo_Leveling) (de) | ja | `data/covers/solo-leveling.org&utm_campaign=api&utm_content=thumbnail` |
| The World After the Fall (Sing-Shong) | [The World After the Fall](https://en.wikipedia.org/wiki/The_World_After_the_Fall) (en) | nein | `data/covers/world-after-fall.jpg` |
| 1984 (George Orwell) | [1984 (Roman)](https://de.wikipedia.org/wiki/1984_%28Roman%29) (de) | ja | `data/covers/1984.org&utm_campaign=api&utm_content=thumbnail` |
| Die letzte Frage (Isaac Asimov) | [The Last Question](https://en.wikipedia.org/wiki/The_Last_Question) (en) | ja | `data/covers/last-question.org&utm_campaign=api&utm_content=thumbnail_unscaled` |
| Auf dem Jakobsweg (Paulo Coelho) | [The Pilgrimage](https://en.wikipedia.org/wiki/The_Pilgrimage) (en) | nein | `data/covers/jakobsweg.jpg` |
| Meditationen (Marcus Aurelius) | [Selbstbetrachtungen](https://de.wikipedia.org/wiki/Selbstbetrachtungen) (de) | ja | `data/covers/meditations.org&utm_campaign=api&utm_content=thumbnail_unscaled` |
| Sapiens: Eine kurze Geschichte der Menschheit (Yuval Noah Harari) | [Eine kurze Geschichte der Menschheit](https://de.wikipedia.org/wiki/Eine_kurze_Geschichte_der_Menschheit) (de) | ja | `data/covers/sapiens.org&utm_campaign=api&utm_content=thumbnail` |
| No Longer Human (Junji Ito (Adaption)) | [Gezeichnet (Dazai Osamu)](https://de.wikipedia.org/wiki/Gezeichnet_%28Dazai_Osamu%29) (de) | nein | `data/covers/nlh-manga.jpg` |

## Bitte prüfen (5)

| Werk | Artikel | Hinweis |
|---|---|---|
| A Song of Ice and Fire | [Das Lied von Eis und Feuer](https://de.wikipedia.org/wiki/Das_Lied_von_Eis_und_Feuer) (de) | Passt: „Das Lied von Eis und Feuer" ist der deutsche Titel. |
| Die Kunst des Seins | [Haben oder Sein](https://de.wikipedia.org/wiki/Haben_oder_Sein) (de) | FALSCH statt richtig: Fromm hat zwei Bücher — „Haben oder Sein" und „Die Kunst des Seins". Bitte den richtigen Artikel eintragen. |
| LSD: Mein Sorgenkind | [LSD, My Problem Child](https://en.wikipedia.org/wiki/LSD%2C_My_Problem_Child) (en) | Passt: „LSD, My Problem Child" ist der englische Titel. |
| Spice and Wolf | [Ōkami to Kōshinryō](https://de.wikipedia.org/wiki/%C5%8Ckami_to_K%C5%8Dshinry%C5%8D) (de) | Passt: „Ōkami to Kōshinryō" ist der japanische Originaltitel. |
| Konosuba | [Kono Subarashii Sekai ni Shukufuku o!](https://de.wikipedia.org/wiki/Kono_Subarashii_Sekai_ni_Shukufuku_o%21) (de) | Passt: „Kono Subarashii Sekai ni Shukufuku o!" ist der volle japanische Titel. |

## Kein Link gefunden (3)

| Werk | Autor | Hinweis |
|---|---|---|
| No Longer Human | Osamu Dazai | in de/en nicht gefunden |
| The Legendary Moonlight Sculptor | Nam Heesung | Abfrage am Limit gescheitert — noch einmal versuchen |
| The Legendary Mechanic | Qi Peijia | Abfrage am Limit gescheitert — noch einmal versuchen |

## Ergebnis der fünf Prüfungen

| Werk | Entscheidung |
|---|---|
| A Song of Ice and Fire | übernommen — „Das Lied von Eis und Feuer" ist der deutsche Titel |
| Die Kunst des Seins | **kein Link** — der Artikel „Haben oder Sein" beschreibt ein anderes Buch von Fromm; „Die Kunst des Seins" selbst gibt es in de und en nicht |
| LSD: Mein Sorgenkind | übernommen — englischer Titel |
| Spice and Wolf | übernommen — japanischer Originaltitel |
| Konosuba | übernommen — voller japanischer Titel |

Zusätzlich geklärt: **No Longer Human** (der Roman) hat doch einen Artikel — in der **englischen** Wikipedia. Der Roman bekommt diesen Link, die Manga-Adaption den deutschen Artikel „Gezeichnet (Dazai Osamu)". Für *The Legendary Moonlight Sculptor* und *The Legendary Mechanic* gibt es in beiden Sprachen keinen Artikel; sie bleiben ohne Link.

Ergebnis: 40 von 43 Werken haben einen Link.

## Nächster Schritt

Keiner mehr — die Umsetzung steht in `generate_covers.py`, die Begründung in `Documentation.md`, Abschnitt 2.6. Rohdaten: `docs/cover-kandidaten.json` (Archiv, kann gelöscht werden).
