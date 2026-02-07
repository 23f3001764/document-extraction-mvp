import streamlit as st
import sqlite3
import pandas as pd

if "extraction_mode" not in st.session_state:
    st.session_state.extraction_mode = "Variant C"

DB_PATH = "data/db/documents.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

st.set_page_config(page_title="Document Extraction MVP", layout="wide")

st.title("📄 Document Extraction MVP")
st.caption("Assignment 1 | Electricity • Constitution • Math")
st.markdown("### ⚙️ Extraction Mode")

mode = st.toggle(
    "Switch to Variant B (SLM-based extraction)",
    value=(st.session_state.extraction_mode == "Variant B")
)

st.session_state.extraction_mode = "Variant B" if mode else "Variant C"

st.info(f"Current mode: **{st.session_state.extraction_mode}**")

tab1, tab2, tab3, tab4 = st.tabs([
    "📜 Constitution Search",
    "📘 Math Book Explorer",
    "⚡ Electricity Bills",
    "⬆️ Upload PDF"
])

with tab1:
    st.subheader("Search Constitution Articles")

    article_no = st.text_input("Enter Article Number (e.g. 21)")

    if article_no:
        conn = get_connection()
        query = """
        SELECT article_number, article_title, part, part_title, article_text
        FROM constitution_articles
        WHERE article_number = ?
        """
        df = pd.read_sql_query(query, conn, params=(article_no,))
        conn.close()

        if not df.empty:
            st.success(f"Found Article {article_no}")
            st.write(df)
        else:
            st.warning("Article not found")

with tab2:
    st.subheader("Math Book Examples")

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM math_examples", conn)
    conn.close()

    if df.empty:
        st.warning("No math examples found")
    else:
        unit_filter = st.selectbox(
            "Filter by Unit",
            ["All"] + sorted(df["unit"].dropna().unique().tolist())
        )

        if unit_filter != "All":
            df = df[df["unit"] == unit_filter]

        st.dataframe(df, width="stretch")

with tab3:
    st.subheader("Electricity Bills")

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM electricity_bills", conn)
    conn.close()

    if df.empty:
        st.warning("No electricity bills found")
    else:
        col1, col2 = st.columns(2)

        with col1:
            min_kwh = st.number_input("Minimum kWh", value=0)

        with col2:
            location = st.selectbox(
                "Location",
                ["All"] + sorted(df["location"].dropna().unique().tolist())
            )

        if location != "All":
            df = df[df["location"] == location]

        df = df[df["kwh"] >= min_kwh]

        st.dataframe(df, width="stretch")

with tab4:
    st.subheader("⬆️ Upload Electricity Bill or Math Book PDF")

    st.markdown(
        f"**Current Extraction Mode:** "
        f":blue[{st.session_state.extraction_mode}]"
    )

    with st.form("upload_form"):
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        doc_choice = st.selectbox(
            "Select document type",
            ["Electricity Bill", "Math Book"]
        )

        submitted = st.form_submit_button("🚀 Process PDF")

    # -----------------------------
    # Processing logic (SAFE ZONE)
    if submitted:
        if uploaded_file is None:
            st.error("❌ Please upload a PDF before processing.")
        else:
            import os
            from scripts.extract_pdf import extract_text_from_pdf
            from scripts.extraction_router import extract_data

            # ---------- Progress indicator ----------
            progress = st.progress(0, text="Starting processing...")

            # ---------- Save uploaded file ----------
            UPLOAD_DIR = "data/uploads"
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            progress.progress(20, text="PDF uploaded and saved")

            # ---------- OCR ----------
            output_dir = f"data/extracted_text/{uploaded_file.name.replace('.pdf','')}"
            text_path = extract_text_from_pdf(file_path, output_dir)

            with open(text_path, "r", encoding="utf-8") as f:
                ocr_text = f.read()

            progress.progress(50, text="OCR completed")

            # ---------- Extraction (Variant C / B switch) ----------
            structured_data = extract_data(
                text=ocr_text,
                doc_type=doc_choice,
                mode=st.session_state.extraction_mode
            )

            progress.progress(75, text="Data extraction completed")

            # ---------- Insert into DB ----------
            def insert_into_db(table, data):
                conn = get_connection()
                cur = conn.cursor()

                if table == "electricity_bills":
                    cur.execute("""
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

                elif table == "math_examples":
                    for row in data:
                        cur.execute("""
                            INSERT INTO math_examples VALUES (?, ?, ?, ?)
                        """, (
                            row.get("unit"),
                            row.get("section"),
                            row.get("example_number"),
                            row.get("example_title")
                        ))

                conn.commit()
                conn.close()

            table = "electricity_bills" if doc_choice == "Electricity Bill" else "math_examples"
            insert_into_db(table, structured_data)

            progress.progress(100, text="Done")

            # ---------- Visual Success Feedback ----------
            st.success(
                f"✅ PDF processed successfully using "
                f"**{st.session_state.extraction_mode}**"
            )

            with st.expander("🔍 View Extracted JSON"):
                st.json(structured_data)