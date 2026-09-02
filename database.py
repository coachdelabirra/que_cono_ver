"""
🍿 Que coño ver!!! #YConCervezaEsMejor
-----------------------------------------
Capa de acceso a datos. Todo en SQLite local, sin servicios externos.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quecono.db")
COVERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "covers")
os.makedirs(COVERS_DIR, exist_ok=True)

# Escala de calificación: 0 = 1 café (peor) ... 6 = 6 birras (LA MAJOE, mejor)
RATING_LEVELS = {
    0: "☕ 1 Café",
    1: "🍺 1 Birra",
    2: "🍺🍺 2 Birras",
    3: "🍺🍺🍺 3 Birras",
    4: "🍺🍺🍺🍺 4 Birras",
    5: "🍺🍺🍺🍺🍺 5 Birras",
    6: "🍺🍺🍺🍺🍺🍺 LA MAJOE",
}


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            avatar_emoji TEXT DEFAULT '🎮',
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('pelicula','serie')),
            rating INTEGER NOT NULL CHECK(rating BETWEEN 0 AND 6),
            cover_path TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(user_id, friend_id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(friend_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


# ---------- USUARIOS ----------

def create_user(username, avatar_emoji="🎮"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, avatar_emoji, created_at) VALUES (?, ?, ?)",
            (username.strip(), avatar_emoji, datetime.now().isoformat()),
        )
        conn.commit()
        return True, "Usuario creado."
    except sqlite3.IntegrityError:
        return False, "Ese nombre de jugador ya existe."
    finally:
        conn.close()


def get_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY username").fetchall()
    conn.close()
    return rows


def get_user_by_name(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


# ---------- ITEMS (peliculas / series) ----------

def add_item(user_id, title, category, rating, cover_path=None, notes=""):
    conn = get_connection()
    conn.execute(
        """INSERT INTO items (user_id, title, category, rating, cover_path, notes, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, title.strip(), category, rating, cover_path, notes, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def update_item(item_id, title, rating, notes, cover_path=None):
    conn = get_connection()
    if cover_path is not None:
        conn.execute(
            "UPDATE items SET title=?, rating=?, notes=?, cover_path=? WHERE id=?",
            (title.strip(), rating, notes, cover_path, item_id),
        )
    else:
        conn.execute(
            "UPDATE items SET title=?, rating=?, notes=? WHERE id=?",
            (title.strip(), rating, notes, item_id),
        )
    conn.commit()
    conn.close()


def delete_item(item_id):
    conn = get_connection()
    conn.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()


def get_items(user_id, category=None):
    conn = get_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM items WHERE user_id=? AND category=? ORDER BY rating DESC, created_at DESC",
            (user_id, category),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM items WHERE user_id=? ORDER BY rating DESC, created_at DESC",
            (user_id,),
        ).fetchall()
    conn.close()
    return rows


def get_item(item_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    conn.close()
    return row


# ---------- AMIGOS ----------

def add_friend(user_id, friend_id):
    if user_id == friend_id:
        return False, "No puedes seguirte a ti mismo, crack."
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO friends (user_id, friend_id, created_at) VALUES (?, ?, ?)",
            (user_id, friend_id, datetime.now().isoformat()),
        )
        conn.commit()
        return True, "¡Amigo añadido!"
    except sqlite3.IntegrityError:
        return False, "Ya sigues a este jugador."
    finally:
        conn.close()


def remove_friend(user_id, friend_id):
    conn = get_connection()
    conn.execute("DELETE FROM friends WHERE user_id=? AND friend_id=?", (user_id, friend_id))
    conn.commit()
    conn.close()


def get_friends(user_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT u.* FROM users u
           INNER JOIN friends f ON u.id = f.friend_id
           WHERE f.user_id = ? ORDER BY u.username""",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def compute_compatibility(user_id, friend_id):
    """Compara titulos en comun y la cercania de las calificaciones (0-100%)."""
    conn = get_connection()
    mine = conn.execute("SELECT title, rating FROM items WHERE user_id=?", (user_id,)).fetchall()
    theirs = conn.execute("SELECT title, rating FROM items WHERE user_id=?", (friend_id,)).fetchall()
    conn.close()

    mine_map = {r["title"].strip().lower(): r["rating"] for r in mine}
    theirs_map = {r["title"].strip().lower(): r["rating"] for r in theirs}
    common = set(mine_map.keys()) & set(theirs_map.keys())

    if not common:
        return 0, 0

    diffs = [abs(mine_map[t] - theirs_map[t]) for t in common]
    avg_diff = sum(diffs) / len(diffs)
    # 0 de diferencia = 100% compatible, 6 de diferencia = 0%
    score = max(0, round(100 - (avg_diff / 6) * 100))
    return score, len(common)
