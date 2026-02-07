# 📄 Document Extraction MVP (Utilities Domain)

> **Assignment 1 – Document Extraction MVP**  
> Domain: **Electricity Utilities**  
> Variants Implemented: **Variant C (Rule-based + SQLite)** and **Variant B (SLM + Postgres)**

---

## 📌 Overview

This project builds a **working MVP** that reads long, complex PDFs (both digital and scanned), extracts structured information using OCR and language models, stores the data in a database, and provides a **simple web UI** for search and filtering.

The system supports **three document types**:

1. **Indian Constitution PDFs**
2. **Engineering Mathematics Textbooks**
3. **Electricity Utility Bills**

The application supports **two variants**, switchable at runtime via the UI:

- **Variant C** – Rule-based extraction + SQLite (fast, lightweight)
- **Variant B** – Small Language Model (SLM) extraction + Postgres (more intelligent)

---

## 🏗 Architecture

PDF → OCR → Chunking → Extraction → Database → Streamlit UI

---

## 🧠 Variants Explained

### 🔹 Variant C (Default – Fast MVP)
- OCR: Tesseract
- Extraction: Regex / rules
- Database: SQLite
- UI: Streamlit

### 🔹 Variant B (Advanced)
- OCR: Tesseract
- Extraction: Small Language Model (Qwen 0.5B)
- Database: PostgreSQL
- UI: Streamlit (runtime switch)

---

## 📂 Supported Schemas

### Constitution
- article_number
- article_title
- part
- part_title
- article_text

### Math Book
- unit
- section
- example_number
- example_title

### Electricity Bill
- meter_id
- bill_date
- kwh
- amount_payable
- location

---

## 🖥 Web Interface

Tabs:
1. Constitution Search  
2. Math Book Browser  
3. Electricity Bills  
4. Upload PDF (with Variant switch)

---

## ⚙️ Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🐳 Docker Deployment

```bash
docker compose up -d --build
```

Open: http://localhost:8501

---

## 🚧 Limitations
- CPU-only SLM is slow
- OCR quality depends on scan
- Constitution SLM limited to few chunks (MVP)

---
## Cloud Deployment

The application is designed to be deployed on a cloud VM (e.g., AWS EC2) using Docker Compose.

Deployment steps:
1. Provision an Ubuntu VM
2. Install Docker and Docker Compose
3. Clone the repository
4. Run `docker compose up -d --build`

The deployment runs three containers:
- PostgreSQL database
- One-time data loader (for initial PDF processing)
- Streamlit web application

This ensures the application is immediately usable after startup.

---

## 🚀 Future Improvements
- Vector search
- Fine-tuned SLM
- Async pipelines
- Better table extraction

---

## 👤 Author
**Sahil Raj**  
BS in Data Science & Applications