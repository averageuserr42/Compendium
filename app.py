"""Flask-Backend für Compendium.

Start:  python app.py
Dann im Browser öffnen:  http://127.0.0.1:5000

Endpunkte:
    GET  /           -> index.html
    GET  /api/trees  -> beide Genre-Bäume als JSON (aus der SQLite-Datenbank)
    POST /api/works  -> neues Werk anlegen. Schreibt zuerst in die Datenbank und
                        danach in data/trees.json (die Quelle der Daten).
    POST /api/covers -> Titelbild hochladen (multipart/form-data, Feld "file").
                        Die Datei landet in data/covers/.
    GET  /data/covers/<datei> -> liefert die Titelbilder aus.
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

import seed

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "compendium.db"
DATA_JSON = BASE_DIR / "data" / "trees.json"
COVERS_DIR = BASE_DIR / "data" / "covers"

ALLOWED_COVER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

app = Flask(__name__)
# Titelbilder sind klein. Alles über 3 MB wird abgelehnt.
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def load_tree_data():
    return json.loads(DATA_JSON.read_text(encoding="utf-8"))


def save_tree_data(payload):
    """Schreibt die Daten zurück in die JSON-Datei. Sie ist die Quelle."""
    DATA_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",  # Zeilenenden bleiben LF, wie in der Datei angelegt
    )


def find_node(node, node_id):
    """Sucht einen Knoten rekursiv im JSON-Baum."""
    if node.get("id") == node_id:
        return node
    for child in node.get("children", []):
        found = find_node(child, node_id)
        if found:
            return found
    return None


def slugify(text):
    """Macht aus einem Titel eine ID: 'Der Alchimist' -> 'der-alchimist'."""
    replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    slug = text.lower()
    for source, target in replacements.items():
        slug = slug.replace(source, target)
    return re.sub(r"[^a-z0-9]+", "-", slug).strip("-") or "werk"


def build_node(connection, row):
    """Baut aus einer Tabellenzeile einen Knoten für das Frontend.

    Kategorien bekommen ihre Kinder aus der Tabelle (parent_id = id dieser Zeile),
    Bücher sind Blätter und haben keine Kinder.
    """
    node = {"id": row["id"], "title": row["title"]}
    if row["description"]:
        node["desc"] = row["description"]

    if row["is_book"]:
        node["isBook"] = True
        if row["author"]:
            node["author"] = row["author"]
        if row["recommended"]:
            node["recommended"] = True
        if row["cover"]:
            node["cover"] = row["cover"]
        if row["wiki"]:
            node["wiki"] = row["wiki"]
        if row["related_id"]:
            node["relatedId"] = row["related_id"]
            node["relatedTitle"] = row["related_title"]
        return node

    children = connection.execute(
        "SELECT * FROM nodes WHERE parent_id = ? ORDER BY rowid", (row["id"],)
    ).fetchall()
    node["children"] = [build_node(connection, child) for child in children]
    return node


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/trees")
def api_trees():
    connection = get_connection()
    try:
        roots = connection.execute(
            "SELECT * FROM nodes WHERE parent_id IS NULL ORDER BY rowid"
        ).fetchall()
        return jsonify({row["tree"]: build_node(connection, row) for row in roots})
    finally:
        connection.close()


@app.route("/api/works", methods=["POST"])
def api_add_work():
    """Legt ein neues Werk an — in der Datenbank und in data/trees.json."""
    data = request.get_json(silent=True) or {}

    missing = [
        field
        for field in ("parent_id", "title", "author")
        if not str(data.get(field) or "").strip()
    ]
    if missing:
        return jsonify({"error": "Fehlende Felder", "fields": missing}), 400

    parent_id = str(data["parent_id"]).strip()
    title = str(data["title"]).strip()
    work_id = str(data.get("id") or slugify(title)).strip()

    # Der neue Knoten hat dieselbe Form wie die Knoten in data/trees.json.
    node = {
        "isBook": True,
        "id": work_id,
        "title": title,
        "author": str(data["author"]).strip(),
    }
    if data.get("recommended"):
        node["recommended"] = True
    if str(data.get("desc") or "").strip():
        node["desc"] = str(data["desc"]).strip()
    if str(data.get("cover") or "").strip():
        node["cover"] = str(data["cover"]).strip()
    if str(data.get("wiki") or "").strip():
        node["wiki"] = str(data["wiki"]).strip()
    if str(data.get("related_id") or "").strip():
        node["relatedId"] = str(data["related_id"]).strip()
        node["relatedTitle"] = str(data.get("related_title") or "").strip()

    connection = get_connection()
    try:
        if connection.execute(
            "SELECT id FROM nodes WHERE id = ?", (work_id,)
        ).fetchone():
            return jsonify({"error": f"Die ID '{work_id}' gibt es schon"}), 409

        parent = connection.execute(
            "SELECT * FROM nodes WHERE id = ?", (parent_id,)
        ).fetchone()
        if parent is None:
            return jsonify({"error": f"Kategorie '{parent_id}' nicht gefunden"}), 404
        if parent["is_book"]:
            return jsonify({"error": f"'{parent_id}' ist ein Buch, keine Kategorie"}), 400

        # 1) in die Datenbank schreiben
        connection.execute(
            """INSERT INTO nodes (id, parent_id, tree, title, description, is_book,
                                  author, recommended, cover, wiki, related_id, related_title)
               VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)""",
            (
                work_id,
                parent_id,
                parent["tree"],
                title,
                node.get("desc"),
                node["author"],
                1 if node.get("recommended") else 0,
                node.get("cover"),
                node.get("wiki"),
                node.get("relatedId"),
                node.get("relatedTitle"),
            ),
        )
        connection.commit()

        # 2) auch in data/trees.json schreiben. Klappt das nicht, wird die
        #    Datenbank zurückgerollt, damit beide Stellen gleich bleiben.
        try:
            payload = load_tree_data()
            category = find_node(payload[parent["tree"]], parent_id)
            if category is None:
                raise LookupError(f"'{parent_id}' fehlt in data/trees.json")
            category.setdefault("children", []).append(node)
            save_tree_data(payload)
        except Exception as error:
            connection.execute("DELETE FROM nodes WHERE id = ?", (work_id,))
            connection.commit()
            return jsonify({"error": f"data/trees.json nicht schreibbar: {error}"}), 500

        return jsonify({"node": node, "parentId": parent_id, "tree": parent["tree"]}), 201
    finally:
        connection.close()


@app.route("/data/covers/<path:filename>")
def api_cover_file(filename):
    """Liefert die Titelbilder aus data/covers/ (unter Flask nötig,
    auf GitHub Pages liegen sie sowieso als statische Dateien)."""
    return send_from_directory(COVERS_DIR, filename)


@app.route("/api/covers", methods=["POST"])
def api_upload_cover():
    """Speichert ein hochgeladenes Titelbild in data/covers/.

    Antwort: 201 mit dem Pfad, der dann in das Feld `cover` gehört.
    """
    file = request.files.get("file")
    if file is None or not file.filename:
        return jsonify({"error": "Keine Datei erhalten"}), 400

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_COVER_EXTENSIONS:
        return jsonify({
            "error": "Nur JPG, JPEG, PNG oder WEBP erlaubt",
            "allowed": sorted(ALLOWED_COVER_EXTENSIONS),
        }), 400

    # Name aus der Werk-ID, sonst aus dem Dateinamen.
    wanted = str(file.filename)
    file_id = str(request.form.get("id") or "").strip()
    name = slugify(file_id) if file_id else slugify(Path(wanted).stem)

    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    target = COVERS_DIR / f"{name}{extension}"
    file.save(target)

    return jsonify({
        "cover": f"data/covers/{target.name}",
        "bytes": target.stat().st_size,
    }), 201


if __name__ == "__main__":
    outdated = seed.missing_columns(DB_PATH)
    if outdated:
        print("Datenbank fehlt oder ist veraltet. Fehlende Spalten: "
              + ", ".join(sorted(outdated)))
        print("Sie wird aus data/trees.json neu erzeugt.")
        seed.build_database()
    app.run(host="127.0.0.1", port=5000, debug=True)
