import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocr import extract_text_from_image
from src.extractor import extract_total_amount, extract_vendor, extract_date
from src.classifier import predict_category_with_confidence

if "history" not in st.session_state:
    st.session_state.history = []

st.title("AI Expense & Receipt Analyzer")
st.write("Upload a receipt image to begin the analysis.")


uploaded_file = st.file_uploader(
    "Choose a receipt image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.image(uploaded_file, caption="Uploaded Receipt", use_container_width=True)

    st.subheader("Extract Text")

    extracted_text = extract_text_from_image(uploaded_file)

    if extracted_text.strip():

        st.text_area("OCR Result", extracted_text, height=300)

        st.subheader("Extracted Information")


        vendor = extract_vendor(extracted_text)
        total = extract_total_amount(extracted_text)
        date = extract_date(extracted_text)

        category, confidence = predict_category_with_confidence(vendor, extracted_text)

        st.write(f"🏪 **Vendor:** {vendor}")
        st.write(f"💰 **Total Amount:** {total}")
        st.write(f"📅 **Date:** {date}")
        st.write(f"🏷️ **Category:** {category}")
        st.write(f"**Confidence:** {confidence:.2%}")

        if confidence < 0.6:
            st.warning("⚠️ Low confidence prediction. Please verify the category.")

        results_df = pd.DataFrame([
            {
                "vendor": vendor,
                "total_amount": total,
                "date": date,
                "category": category,
                "confidence": round(confidence, 4)
            }
        ])

        csv_data = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="receipt_analysis_results.csv",
            mime="text/csv"
        )

        if st.button("➕ Add to History"):
            new_entry = {
                "vendor": vendor,
                "total_amount": total,
                "date": date,
                "category": category,
                "confidence": round(confidence, 4)
            }

            is_duplicate = any(
                entry["vendor"] == new_entry["vendor"] and
                entry["total_amount"] == new_entry["total_amount"] and
                entry["date"] == new_entry["date"]
                for entry in st.session_state.history
            )

            if is_duplicate:
                st.warning("⚠️ This receipt is already in history.")
            else:
                st.session_state.history.append(new_entry)
                st.success("Receipt added to history!")

    else:
        st.warning("No text was extracted from the image.")
else:
    st.info("Please upload a receipt image file.")

if st.session_state.history:

    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader("📂 Receipt History")

    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.history = []

    history_df = pd.DataFrame(st.session_state.history)

    st.subheader("📊 Dashboard Summary")

    total_receipts = len(history_df)
    total_spending = history_df["total_amount"].fillna(0).sum()
    average_spending = history_df["total_amount"].fillna(0).mean()
    top_category = history_df["category"].mode()[0]

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Total Receipts", total_receipts)

    with m2:
        st.metric("Total Spending", f"{total_spending:.2f}")

    with m3:
        st.metric("Average Spending", f"{average_spending:.2f}")

    with m4:
        st.metric("Top Category", top_category)

    st.dataframe(history_df)

    st.subheader("📈 Spending by Category")

    category_spending = history_df.groupby("category")["total_amount"].sum()

    st.bar_chart(category_spending)

    history_csv = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Full History CSV",
        data=history_csv,
        file_name="receipt_history.csv",
        mime="text/csv"
    )

