"""Baut die SQLite-Datenbank aus data/trees.json.

Aufruf:  python seed.py

Die Datenbank ist eine reine Ausgabedatei: sie wird bei jedem Aufruf
neu aus der JSON-Datei erzeugt. Quelle der Daten bleibt data/trees.json.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_JSON = BASE_DIR / "data" / "trees.json"
DB_PATH = BASE_DIR / "data" / "compendium.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes (
    id            TEXT PRIMARY KEY,
    parent_id     TEXT REFERENCES nodes(id),
    tree          TEXT NOT NULL,
    title         TEXT NOT NULL,
    description   TEXT,
    is_book       INTEGER NOT NULL DEFAULT 0,
    author        TEXT,
    recommended   INTEGER NOT NULL DEFAULT 0,
    cover         TEXT,
    wiki          TEXT,
    related_id    TEXT,
    related_title TEXT
);
"""

REQUIRED_COLUMNS = (
    "id",
    "parent_id",
    "tree",
    "title",
    "description",
    "is_book",
    "author",
    "recommended",
    "cover",
    "wiki",
    "related_id",
    "related_title",
)


def missing_columns(db_path=DB_PATH):
    """Spalten, die in der vorhandenen Tabelle fehlen.

    Wird das Schema erweitert, erkennt die App das und erzeugt die Tabelle
    neu, statt mit einer kryptischen Fehlermeldung abzubrechen.
    """
    db_path = Path(db_path)
    if not db_path.exists():
        return set(REQUIRED_COLUMNS)

    connection = sqlite3.connect(db_path)
    try:
        present = {row[1] for row in connection.execute("PRAGMA table_info(nodes)")}
    finally:
        connection.close()

    return set(REQUIRED_COLUMNS) - present


def insert_node(cursor, tree_key, node, parent_id):
    """Schreibt einen Knoten in die Tabelle und ruft sich für die Kinder selbst auf."""
    cursor.execute(
        """INSERT INTO nodes (id, parent_id, tree, title, description, is_book,
                              author, recommended, cover, wiki, related_id, related_title)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            node["id"],
            parent_id,
            tree_key,
            node["title"],
            node.get("desc"),
            1 if node.get("isBook") else 0,
            node.get("author"),
            1 if node.get("recommended") else 0,
            node.get("cover"),
            node.get("wiki"),
            node.get("relatedId"),
            node.get("relatedTitle"),
        ),
    )

    for child in node.get("children", []):
        insert_node(cursor, tree_key, child, node["id"])


def build_database(json_path=DATA_JSON, db_path=DB_PATH):
    """Erzeugt die Datenbank neu. Gibt den Pfad der Datenbank zurück."""
    payload = json.loads(Path(json_path).read_text(encoding="utf-8"))

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    connection = sqlite3.connect(db_path)
    try:
        with connection:
            connection.executescript(SCHEMA)
            cursor = connection.cursor()
            for tree_key, root in payload.items():
                insert_node(cursor, tree_key, root, None)
    finally:
        connection.close()

    return db_path


if __name__ == "__main__":
    path = build_database()
    count = sqlite3.connect(path).execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    print(f"Datenbank erstellt: {path} ({count} Knoten)")
