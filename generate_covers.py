"""Erzeugt typografische Titelbilder (SVG) und trägt Wikipedia-Links ein.

Aufruf:  python generate_covers.py [--force]

Was das Skript macht:
  1. liest data/trees.json (die Quelle der Daten),
  2. schreibt für jedes Werk data/covers/<id>.svg,
  3. setzt die Felder `cover` (Pfad zur SVG) und `wiki` (Link zum Artikel),
  4. schreibt data/trees.json zurück und erzeugt die SQLite-Datenbank neu.

Warum eigene Bilder: Die deutsche Wikipedia zeigt keine Buchcover (dort sind
nicht-freie Dateien nicht erlaubt), die englische nur unter „fair use". Fremde
Cover herunterzuladen wäre für dieses Repository rechtlich nicht sauber.
Eigene SVG-Dateien sind dagegen: kleine Textdateien (etwa 2 KB), rechtlich
einwandfrei und im Design des Projekts.

Das Skript ist deterministisch: derselbe Titel ergibt Byte für Byte dasselbe
Bild. Es braucht keine externen Bibliotheken, nur die Standardbibliothek.

Zwei Design-Regeln (siehe docs/DESIGN_GUIDE.md):
  * Die Farbpalette ist fest — dieselben Werte wie :root in index.html.
  * Die Komposition variiert: Verlauf, Lichtpunkt und Zweigmotiv hängen vom
    Werk und von der Kategorie ab. Alle Werke einer Kategorie teilen also das
    Motiv, unterscheiden sich aber im Hintergrund und im Titelbild-Aufbau.
"""
from __future__ import annotations

import hashlib
import html
import json
import math
import sys
from pathlib import Path

import seed

BASE_DIR = Path(__file__).resolve().parent
DATA_JSON = BASE_DIR / "data" / "trees.json"
COVERS_DIR = BASE_DIR / "data" / "covers"

# --- Farben: identisch mit :root in index.html -------------------------------
BG = "#0A0A0A"
CARD_BG = "#121712"
BG_LIGHT = "#0E1410"
GREEN = "#33FF66"
GREEN_DIM = "#1F8F44"
TEXT = "#FFFFFF"
MUTED = "#9FCDAF"

WIDTH = 400
HEIGHT = 600

TREE_LABELS = {"literature": "Literatur", "novels": "Manga & Web-Novels"}

# --- Wikipedia-Links ---------------------------------------------------------
# Ermittelt in docs/COVER_KANDIDATEN.md (Stand: siehe Dateidatum) und dort
# einzeln geprüft. Drei Werke haben keinen Artikel und bleiben leer:
#   kunst-seins        -> „Haben oder Sein" ist ein anderes Buch von Fromm
#   lms                -> kein Artikel in de/en
#   legendary-mechanic -> kein Artikel in de/en
WIKI_LINKS = {
    "1984": "https://de.wikipedia.org/wiki/1984_%28Roman%29",
    "last-question": "https://en.wikipedia.org/wiki/The_Last_Question",
    "dune": "https://de.wikipedia.org/wiki/Dune",
    "foundation": "https://de.wikipedia.org/wiki/Foundation",
    "fahrenheit": "https://de.wikipedia.org/wiki/Fahrenheit_451",
    "neuromancer": "https://de.wikipedia.org/wiki/Neuromancer",
    "lotr": "https://de.wikipedia.org/wiki/Der_Herr_der_Ringe",
    "hobbit": "https://de.wikipedia.org/wiki/Der_Hobbit",
    "asoiaf": "https://de.wikipedia.org/wiki/Das_Lied_von_Eis_und_Feuer",
    "auferstehung": "https://de.wikipedia.org/wiki/Auferstehung",
    "meister-margarita": "https://de.wikipedia.org/wiki/Der_Meister_und_Margarita",
    "alchimist": "https://de.wikipedia.org/wiki/Der_Alchimist",
    "jakobsweg": "https://en.wikipedia.org/wiki/The_Pilgrimage",
    "nlh-novel": "https://en.wikipedia.org/wiki/No_Longer_Human",
    "process": "https://de.wikipedia.org/wiki/Der_Process",
    "verwandlung": "https://de.wikipedia.org/wiki/Die_Verwandlung",
    "schuld": "https://de.wikipedia.org/wiki/Schuld_und_S%C3%BChne",
    "clean-code": "https://de.wikipedia.org/wiki/Clean_Code",
    "pragmatic": "https://en.wikipedia.org/wiki/The_Pragmatic_Programmer",
    "refactoring": "https://de.wikipedia.org/wiki/Refactoring",
    "meditations": "https://de.wikipedia.org/wiki/Selbstbetrachtungen",
    "sisyphos": "https://de.wikipedia.org/wiki/Der_Mythos_des_Sisyphos",
    "zarathustra": "https://de.wikipedia.org/wiki/Also_sprach_Zarathustra",
    "sapiens": "https://de.wikipedia.org/wiki/Eine_kurze_Geschichte_der_Menschheit",
    "lsd": "https://en.wikipedia.org/wiki/LSD%2C_My_Problem_Child",
    "one-piece": "https://de.wikipedia.org/wiki/One_Piece",
    "aot": "https://de.wikipedia.org/wiki/Attack_on_Titan",
    "fma": "https://de.wikipedia.org/wiki/Fullmetal_Alchemist",
    "nlh-manga": "https://de.wikipedia.org/wiki/Gezeichnet_%28Dazai_Osamu%29",
    "berserk": "https://de.wikipedia.org/wiki/Berserk",
    "monster": "https://de.wikipedia.org/wiki/Monster",
    "fruits-basket": "https://de.wikipedia.org/wiki/Fruits_Basket",
    "nana": "https://de.wikipedia.org/wiki/Nana",
    "spice-wolf": "https://de.wikipedia.org/wiki/%C5%8Ckami_to_K%C5%8Dshinry%C5%8D",
    "re-zero": "https://en.wikipedia.org/wiki/Re%3AZero",
    "overlord": "https://de.wikipedia.org/wiki/Overlord",
    "mushoku": "https://de.wikipedia.org/wiki/Mushoku_Tensei",
    "konosuba": "https://de.wikipedia.org/wiki/Kono_Subarashii_Sekai_ni_Shukufuku_o%21",
    "solo-leveling": "https://de.wikipedia.org/wiki/Solo_Leveling",
    "world-after-fall": "https://en.wikipedia.org/wiki/The_World_After_the_Fall",
}

# Vier Verläufe und vier Lichtpunkte. Der Hash des Werks wählt aus.
GRADIENTS = (
    ("0%", "0%", "100%", "100%"),
    ("100%", "0%", "0%", "100%"),
    ("0%", "100%", "100%", "0%"),
    ("50%", "0%", "50%", "100%"),
)
LIGHTS = ((92, 512), (318, 96), (86, 128), (306, 498), (200, 560))


def esc(text) -> str:
    """Text für SVG/XML sicher machen (&, <, >)."""
    return html.escape(str(text), quote=False)


def digest_of(value: str) -> bytes:
    """Stabiler Hashwert — daraus entsteht die „Zufälligkeit" des Motivs."""
    return hashlib.sha256(value.encode("utf-8")).digest()


def wrap(text: str, size: float, max_width: float, factor: float = 0.52) -> list:
    """Bricht einen Titel in Zeilen. Die Breite wird geschätzt (Antiqua ≈ 0.52 em)."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) * size * factor > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def title_layout(title: str) -> tuple:
    """Größte Schriftgröße, bei der der Titel sauber in den Block passt."""
    for size in (46, 42, 38, 34, 30, 26, 23, 20):
        lines = wrap(title, size, 314)
        widest = max(len(line) for line in lines) * size * 0.52
        if widest <= 314 and len(lines) <= 4 and len(lines) * size * 1.22 <= 250:
            return size, lines
    return 20, wrap(title, 20, 314)


def small_caps_layout(text: str, max_width: float) -> tuple:
    """Größe für die obere Zeile. Bei sehr langen Namen wird die Schrift kleiner."""
    for size in (12, 11, 10, 9, 8):
        if len(text) * (size * 0.62 + 1.4) <= max_width:
            return size
    return 8  # längste Kategorie: „Wissenschaft & Gesellschaft" — passt auch so


def star_points(cx: float, cy: float, outer: float, inner: float) -> str:
    """Fünfzackiger Stern als Polygon — als Zeichen gezeichnet, nicht als Text,
    damit er auf jedem System gleich aussieht."""
    points = []
    for index in range(10):
        radius = outer if index % 2 == 0 else inner
        angle = math.radians(-90 + index * 36)
        points.append(f"{cx + radius * math.cos(angle):.1f},{cy + radius * math.sin(angle):.1f}")
    return " ".join(points)


def branch(x: float, y: float, angle: float, length: float, levels: int,
           width: float, spread: float, out: list) -> None:
    """Zeichnet einen dünnen Zweig und ruft sich für die Verästelung selbst auf."""
    if levels <= 0 or length < 5:
        return
    radians = math.radians(angle)
    x2 = x + length * math.sin(radians)
    y2 = y - length * math.cos(radians)
    out.append(
        f'<path d="M{x:.1f} {y:.1f} L{x2:.1f} {y2:.1f}" stroke="{GREEN_DIM}" '
        f'stroke-width="{width:.2f}" stroke-linecap="round" opacity="0.55"/>'
    )
    if levels == 1:
        out.append(
            f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2.4" fill="{GREEN}" opacity="0.20"/>'
        )
        return
    branch(x2, y2, angle - spread, length * 0.62, levels - 1, width * 0.68, spread, out)
    branch(x2, y2, angle + spread * 0.92, length * 0.58, levels - 1, width * 0.68, spread, out)


def cover_svg(book: dict, category: str, tree: str) -> str:
    """Baut die komplette SVG-Datei für ein Werk."""
    layout = digest_of(book["id"])
    motif = digest_of(f"{tree}:{category}")

    # Hintergrund: Verlauf + weicher Lichtpunkt
    x1, y1, x2, y2 = GRADIENTS[layout[0] % len(GRADIENTS)]
    light_x, light_y = LIGHTS[layout[1] % len(LIGHTS)]
    glow = 0.10 + (layout[2] / 255) * 0.06

    # Zweigmotiv: gleiche Kategorie -> gleiche Form, andere Ausprägung
    spread = 24 + (motif[3] / 255) * 12
    trunk = 40 + (motif[4] / 255) * 12
    lean = ((motif[5] / 255) - 0.5) * 10
    branches: list = []
    branch(WIDTH / 2, 566, lean, trunk, 3, 1.5, spread, branches)

    # Titel und obere Zeile
    title_size, title_lines = title_layout(book["title"])
    line_height = title_size * 1.22
    block = len(title_lines) * line_height
    top = 286 - block / 2 + title_size * 0.82
    title_svg = []
    for index, line in enumerate(title_lines):
        y = top + index * line_height
        title_svg.append(
            f'<text x="{WIDTH / 2}" y="{y:.1f}" text-anchor="middle" '
            f'font-family="Georgia, \'Times New Roman\', serif" font-size="{title_size}" '
            f'fill="{TEXT}" letter-spacing="0.5">{esc(line)}</text>'
        )

    # Zeile unter dem Titel + Autor
    divider_y = top + (len(title_lines) - 1) * line_height + title_size * 0.95
    author_y = divider_y + 34

    category_text = category.upper()
    path_size = small_caps_layout(category_text, 320)

    star = ""
    if book.get("recommended"):
        star = (
            f'<polygon points="{star_points(348, 48, 13, 5.4)}" fill="{GREEN}" opacity="0.14"/>'
            f'<polygon points="{star_points(348, 48, 9.5, 4.0)}" fill="{GREEN}" opacity="0.85"/>'
        )

    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="Titelbild: {esc(book["title"])} – {esc(book.get("author", ""))}">',
        f"  <title>{esc(book['title'])} – {esc(book.get('author', ''))}</title>",
        "  <defs>",
        f'    <linearGradient id="bg" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">',
        f'      <stop offset="0%" stop-color="{CARD_BG}"/>',
        f'      <stop offset="55%" stop-color="{BG}"/>',
        f'      <stop offset="100%" stop-color="{BG_LIGHT}"/>',
        "    </linearGradient>",
        '    <radialGradient id="glow">',
        f'      <stop offset="0%" stop-color="{GREEN_DIM}" stop-opacity="{glow:.2f}"/>',
        f'      <stop offset="100%" stop-color="{GREEN_DIM}" stop-opacity="0"/>',
        "    </radialGradient>",
        "  </defs>",
        f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        f'  <circle cx="{light_x}" cy="{light_y}" r="230" fill="url(#glow)"/>',
        f'  <rect x="18" y="18" width="{WIDTH - 36}" height="{HEIGHT - 36}" fill="none" '
        f'stroke="{GREEN_DIM}" stroke-width="1" opacity="0.35"/>',
        star,
        f'  <text x="{WIDTH / 2}" y="60" text-anchor="middle" font-family="Consolas, '
        f'\'Courier New\', monospace" font-size="11" fill="{MUTED}" letter-spacing="3.4" '
        f'opacity="0.85">{esc(TREE_LABELS.get(tree, tree).upper())}</text>',
        f'  <text x="{WIDTH / 2}" y="82" text-anchor="middle" font-family="Consolas, '
        f'\'Courier New\', monospace" font-size="{path_size}" fill="{GREEN_DIM}" '
        f'letter-spacing="1.6">{esc(category_text)}</text>',
        f'  <path d="M{WIDTH / 2 - 32} 102 L{WIDTH / 2 + 32} 102" stroke="{GREEN}" '
        f'stroke-width="1" opacity="0.45"/>',
        *[f"  {line}" for line in title_svg],
        f'  <path d="M{WIDTH / 2 - 24} {author_y - 34:.1f} L{WIDTH / 2 + 24} {author_y - 34:.1f}" '
        f'stroke="{GREEN}" stroke-width="1" opacity="0.35"/>',
        f'  <text x="{WIDTH / 2}" y="{author_y:.1f}" text-anchor="middle" font-family="Consolas, '
        f'\'Courier New\', monospace" font-size="12.5" fill="{MUTED}" letter-spacing="2.2">'
        f'{esc(book.get("author", "").upper())}</text>',
        *[f"  {line}" for line in branches],
        "</svg>",
        "",
    ])


def walk_books(node, tree, found):
    """Sammelt alle Werke. `node` ist dabei immer eine Kategorie,
    die Werke stehen direkt darunter — also ist node["title"] die Kategorie.

    (Wichtig: den Pfad nicht an das Werk selbst hängen, sonst steht später
    der Werktitel dort, wo die Kategorie stehen soll.)
    """
    for child in node.get("children", []):
        if child.get("isBook"):
            found.append({
                "id": child["id"],
                "title": child["title"],
                "author": child.get("author"),
                "recommended": bool(child.get("recommended")),
                "category": node["title"],
                "tree": tree,
                "node": child,
            })
        else:
            walk_books(child, tree, found)


def is_generated(cover) -> bool:
    """Wurde das Bild von diesem Skript erzeugt?"""
    return bool(cover) and cover.startswith("data/covers/") and cover.endswith(".svg")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    force = "--force" in argv

    payload = json.loads(DATA_JSON.read_text(encoding="utf-8"))

    books = []
    for tree, root in payload.items():
        walk_books(root, tree, books)

    COVERS_DIR.mkdir(parents=True, exist_ok=True)

    written = links = skipped = 0
    for book in books:
        node = book["node"]

        # Ein im Browser hochgeladenes Bild wird nicht überschrieben (ohne --force).
        current = node.get("cover")
        uploaded = bool(current) and not is_generated(current) and (BASE_DIR / current).exists()
        if uploaded and not force:
            skipped += 1
        else:
            node["cover"] = _write_cover(book)
            written += 1

        url = WIKI_LINKS.get(book["id"])
        if url:
            node["wiki"] = url
            links += 1

    DATA_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",  # Zeilenenden bleiben LF, wie in der Datei angelegt
    )

    path = seed.build_database()

    print(f"Titelbilder geschrieben: {written}")
    if skipped:
        print(f"Übersprungen (eigenes Bild vorhanden): {skipped} — mit --force überschreiben")
    print(f"Wikipedia-Links gesetzt: {links}")
    print(f"Werke insgesamt: {len(books)}")
    print(f"Datenbank: {path.name}")
    print(f"data/trees.json: {DATA_JSON.stat().st_size} Bytes")
    return 0


def _write_cover(book) -> str:
    """Schreibt die SVG-Datei und gibt den Pfad für das Feld `cover` zurück."""
    svg = cover_svg(book, book["category"], book["tree"])
    target = COVERS_DIR / f"{book['id']}.svg"
    target.write_text(svg, encoding="utf-8", newline="\n")
    return f"data/covers/{target.name}"


if __name__ == "__main__":
    raise SystemExit(main())
