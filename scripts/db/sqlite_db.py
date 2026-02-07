import sqlite3

DB_PATH = "data/db/documents.db"

def get_sqlite_connection():
    return sqlite3.connect(DB_PATH)
