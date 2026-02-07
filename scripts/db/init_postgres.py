from scripts.db.postgres_db import get_pg_connection

def init_tables():
    conn = get_pg_connection()
    cur = conn.cursor()

    # ---------------------------
    # Constitution Articles
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS constitution_articles (
        id SERIAL PRIMARY KEY,
        article_number TEXT,
        article_title TEXT,
        part TEXT,
        part_title TEXT,
        article_text TEXT
    );
    """)

    # ---------------------------
    # Math Book Examples
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS math_examples (
        id SERIAL PRIMARY KEY,
        unit TEXT,
        section TEXT,
        example_number TEXT,
        example_title TEXT
    );
    """)

    # ---------------------------
    # Electricity Bills
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS electricity_bills (
        id SERIAL PRIMARY KEY,
        meter_id TEXT,
        bill_date TEXT,
        kwh FLOAT,
        amount_payable FLOAT,
        location TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Postgres tables created successfully")


if __name__ == "__main__":
    init_tables()
