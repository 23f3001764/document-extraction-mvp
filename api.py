from fastapi import FastAPI
from scripts.db.postgres_db import get_pg_connection

app = FastAPI()

@app.get("/constitution/{article_no}")
def get_article(article_no: str):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT article_title, part FROM constitution_articles WHERE article_number=%s",
        (article_no,)
    )
    result = cur.fetchone()
    conn.close()
    return result