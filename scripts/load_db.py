import sqlite3
import json
import os

DB_PATH = "../data/db/documents.db"
EXTRACTED_DIR = "../data/extracted_text"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------- CREATE TABLES ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS electricity_bills (
    meter_id TEXT,
    bill_date TEXT,
    billing_period TEXT,
    kwh INTEGER,
    amount_payable REAL,
    zone TEXT,
    tariff_category TEXT,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS constitution_articles (
    article_number TEXT,
    article_title TEXT,
    part TEXT,
    part_title TEXT,
    article_text TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS math_examples (
    unit TEXT,
    section TEXT,
    example_number TEXT,
    example_title TEXT
)
""")

# ---------------- LOAD JSON ----------------

for folder in os.listdir(EXTRACTED_DIR):
    json_path = os.path.join(EXTRACTED_DIR, folder, "output.json")

    if not os.path.exists(json_path):
        continue

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------- Electricity ----------
    if isinstance(data, dict) and data.get("document_type") == "electricity":
        cursor.execute("""
            INSERT INTO electricity_bills VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("meter_id"),
            data.get("bill_date"),
            data.get("billing_period"),
            data.get("kwh"),
            data.get("amount_payable"),
            data.get("zone"),
            data.get("tariff_category"),
            data.get("location")
        ))

    # ---------- Constitution ----------
    elif isinstance(data, list) and data and data[0].get("document_type") == "constitution":
        for row in data:
            cursor.execute("""
                INSERT INTO constitution_articles VALUES (?, ?, ?, ?, ?)
            """, (
                row.get("article_number"),
                row.get("article_title"),
                row.get("part"),
                row.get("part_title"),
                row.get("article_text")
            ))

    # ---------- Math ----------
    elif isinstance(data, list) and data and data[0].get("document_type") == "math":
        for row in data:
            cursor.execute("""
                INSERT INTO math_examples VALUES (?, ?, ?, ?)
            """, (
                row.get("unit"),
                row.get("section"),
                row.get("example_number"),
                row.get("example_title")
            ))

conn.commit()
conn.close()

print("✅ All JSON data loaded into SQLite database")