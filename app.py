import streamlit as st
import sqlite3
import pandas as pd

import streamlit as st
from scripts.db.db_router import get_connection_by_variant

if "extraction_mode" not in st.session_state:
    st.session_state.extraction_mode = "Variant C"

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
        conn, db_type = get_connection_by_variant(st.session_state.extraction_mode)

        if db_type == "sqlite":
            query = """
            SELECT article_number, article_title, part, part_title, article_text
            FROM constitution_articles
            WHERE article_number = ?
            """
            params = (article_no,)
        else:
            query = """
            SELECT article_number, article_title, part, part_title, article_text
            FROM constitution_articles
            WHERE article_number = %s
            """
            params = (article_no,)

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        if df.empty:
            if st.session_state.extraction_mode == "Variant B":
                st.warning(
                    "No articles extracted yet using SLM-based Variant B. "
                    "This demonstrates the probabilistic limitation of small language models "
                    "on long legal documents."
                )
        else:
            st.success(f"Found Article {article_no}")
            st.dataframe(df, width="stretch")

with tab2:
    st.subheader("Math Book Examples")

    conn, _ = get_connection_by_variant(st.session_state.extraction_mode)
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

    conn, _ = get_connection_by_variant(st.session_state.extraction_mode)
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

    # -----------------------------
    # Upload form
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
            from scripts.db.db_router import get_connection_by_variant

            # 🔐 Always initialize
            table = None

            # ---------- Progress ----------
            progress = st.progress(0, text="Starting processing...")

            # ---------- Save file ----------
            UPLOAD_DIR = "data/uploads"
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            progress.progress(20, text="📁 PDF saved")

            # ---------- OCR ----------
            output_dir = f"data/extracted_text/{uploaded_file.name.replace('.pdf','')}"
            text_path = extract_text_from_pdf(file_path, output_dir)

            with open(text_path, "r", encoding="utf-8") as f:
                ocr_text = f.read()

            progress.progress(50, text="🔍 OCR completed")

            # ---------- Extraction ----------
            structured_data = extract_data(
                text=ocr_text,
                doc_type=doc_choice,
                mode=st.session_state.extraction_mode
            )

            progress.progress(75, text="🧠 Data extraction completed")

            # ---------- Decide table ----------
            if doc_choice == "Electricity Bill":
                table = "electricity_bills"
            elif doc_choice == "Math Book":
                table = "math_examples"

            if not structured_data or table is None:
                st.warning("⚠️ No structured data extracted. Nothing to save.")
            else:
                # ---------- DB Insert ----------
                conn, db_type = get_connection_by_variant(
                    st.session_state.extraction_mode
                )
                cur = conn.cursor()

                if table == "electricity_bills":
                    if db_type == "sqlite":
                        cur.execute("""
                            INSERT INTO electricity_bills
                            (meter_id, bill_date, kwh, amount_payable, location)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            structured_data.get("meter_id"),
                            structured_data.get("bill_date"),
                            structured_data.get("kwh"),
                            structured_data.get("amount_payable"),
                            structured_data.get("location")
                        ))
                    else:  # postgres
                        cur.execute("""
                            INSERT INTO electricity_bills
                            (meter_id, bill_date, kwh, amount_payable, location)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            structured_data.get("meter_id"),
                            structured_data.get("bill_date"),
                            structured_data.get("kwh"),
                            structured_data.get("amount_payable"),
                            structured_data.get("location")
                        ))

                elif table == "math_examples":
                    for row in structured_data:
                        if db_type == "sqlite":
                            cur.execute("""
                                INSERT INTO math_examples
                                (unit, section, example_number, example_title)
                                VALUES (?, ?, ?, ?)
                            """, (
                                row.get("unit"),
                                row.get("section"),
                                row.get("example_number"),
                                row.get("example_title")
                            ))
                        else:  # postgres
                            cur.execute("""
                                INSERT INTO math_examples
                                (unit, section, example_number, example_title)
                                VALUES (%s, %s, %s, %s)
                            """, (
                                row.get("unit"),
                                row.get("section"),
                                row.get("example_number"),
                                row.get("example_title")
                            ))

                conn.commit()
                conn.close()

                progress.progress(100, text="✅ Done")

                # ---------- Success ----------
                st.success(
                    f"✅ PDF processed successfully using "
                    f"**{st.session_state.extraction_mode}**"
                )

                with st.expander("🔍 View Extracted JSON"):
                    st.json(structured_data)