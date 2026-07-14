"""Database access layer for Spendly.

No ORM — plain sqlite3, parameterized queries only.
"""

import sqlite3
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"


def get_db():
    """Open a new connection to expense_tracker.db.

    Rows are dict-like (sqlite3.Row); foreign key enforcement is on.
    Caller is responsible for closing the connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't exist. Safe to call repeatedly."""
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert one demo user + 8 sample expenses. No-op if users already exist."""
    conn = get_db()
    try:
        row = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()
        if row["n"] > 0:
            return

        password_hash = generate_password_hash("demo123")
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cur.lastrowid

        today = date.today()
        offsets = [2, 5, 8, 11, 14, 17, 21, 25]
        d = [date(today.year, today.month, o).isoformat() for o in offsets]

        sample_expenses = [
            (user_id, 12.50, "Food",         d[0], "Groceries at the supermarket"),
            (user_id, 45.00, "Transport",     d[1], "Monthly metro pass"),
            (user_id, 89.99, "Bills",         d[2], "Electricity bill"),
            (user_id, 25.00, "Health",        d[3], "Pharmacy purchase"),
            (user_id, 15.00, "Entertainment", d[4], "Movie tickets"),
            (user_id, 60.75, "Shopping",      d[5], "New shoes"),
            (user_id,  9.99, "Other",         d[6], "Miscellaneous purchase"),
            (user_id, 32.40, "Food",          d[7], "Dinner with friends"),
        ]
        conn.executemany(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            sample_expenses,
        )
        conn.commit()
    finally:
        conn.close()
