from scripts.extract_pdf import extract_text_from_pdf
from scripts.extractors.slm_extractor import extract_with_slm
from scripts.db.postgres_db import get_pg_connection
from scripts.utils.chunking import chunk_text

# -----------------------------
# Paths
# -----------------------------
pdf_path = "data/raw_pdfs/Constitution of India-1-50.pdf"
output_dir = "data/extracted_text/constitution"

# -----------------------------
# OCR / Text extraction
# -----------------------------
text_path = extract_text_from_pdf(pdf_path, output_dir)

with open(text_path, "r", encoding="utf-8") as f:
    text = f.read()

# -----------------------------
# Chunking (VERY IMPORTANT)
# -----------------------------
chunks = chunk_text(text, max_chars=1200)

MAX_CHUNKS = 3   # MVP limit for Variant B
all_articles = []

print(f"📄 Total chunks: {len(chunks)}")
print(f"⚙️ Processing first {MAX_CHUNKS} chunks (Variant B MVP)")

for i, chunk in enumerate(chunks[:MAX_CHUNKS], start=1):
    print(f"🔹 Processing chunk {i}/{MAX_CHUNKS}")
    articles = extract_with_slm(chunk, "Constitution")

    if isinstance(articles, list):
        all_articles.extend(articles)

# -----------------------------
# Insert into Postgres
# -----------------------------
if not all_articles:
    print("⚠️ No articles extracted by SLM. Nothing to insert.")
else:
    conn = get_pg_connection()
    cur = conn.cursor()

    for art in all_articles:
        cur.execute("""
            INSERT INTO constitution_articles
            (article_number, article_title, part, part_title, article_text)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            art.get("article_number"),
            art.get("article_title"),
            art.get("part"),
            art.get("part_title"),
            art.get("article_text")
        ))

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Inserted {len(all_articles)} constitution articles into Postgres (Variant B)")