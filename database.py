import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "linkkiwi2026"

def get_db():
    """Database connection"""
    conn = sqlite3.connect('myproject.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """create table"""
    conn = get_db()  # <-- 4 space indent
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll INTEGER NOT NULL UNIQUE,
            marks INTEGER NOT NULL,
            subject TEXT NOT NULL,
            ATTENDANCE INTEGER DEFAULT 0
        )
    ''')  # <-- Sab indent
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)