import streamlit as st # Εισάγει την βιβλιοθήκη streamlit μέσα στο αρχείο
import sys
import os
import pandas as pd #για την  δημιουργία ενός table με τα αποτελέσματα

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocr import extract_text_from_image
from src.extractor import extract_total_amount, extract_vendor, extract_date
from src.classifier import predict_category_with_confidence

if "history" not in st.session_state: #αν δεν υπάρχει ιστορικό το δημιουργούμε
    st.session_state.history = [] #μια λίστα είναι

st.title("AI Expense & Receipt Analyzer") #εμφανίζει τον βασικό τίτλο της εφαρμογής
st.write("Upload a receipt image to begin the analysis.") #εμφανίζει ένα απλό κείμενο κάτω απο τον τίτλο
#με το st.write() είναι γενική εντολή για να εμφανίζεις κείμενο, μεταβλητές και άλλα

uploaded_file = st.file_uploader( #είναι το στοιχείο που δημιουργεί το upload box στο app
    "Choose a receipt image", #το κείμενο που θα βλέπει ο χρήστης
    type=["png", "jpg", "jpeg"] #λέει στο app δέξου μόνο εικόνες αυτών των τύπων
)

if uploaded_file is not None: #ελέγχει αν όντως έχει ανέβει το αρχείο , αν υπάρχει --> μπες σε αυτό το block
    st.success("File uploaded successfully!") #εμφάνισε πράσινο μήνυμα επιτυχίας
    st.image(uploaded_file, caption="Uploaded Receipt", use_container_width=True) #ποιά εικόνα να δείξει
    #μικρό κείμενο κάτω απο την εικόνα. να προσαρμοστεί στο πλάτος της σελίδας

    st.subheader("Extract Text") #βάζει ένα μικρό τίτλο πριν το αποτέλεσμα του OCR

    extracted_text = extract_text_from_image(uploaded_file) #παίρνει το uploaded file και το στέλνει στην συναρτηση OCR

    if extracted_text.strip(): #Ελέγχει αν το text που επιστράφηκε δεν είναι άδειο (το strip αφαιρεί κενά
        #απο την αρχή και το τέλος του string)
        st.text_area("OCR Result", extracted_text, height=300) #εμφανίζει το string σε ένα μεγάλο πλαίσιο

        st.subheader("Extracted Information") #Εμφανίζει έναν τίτλο στο app, ουσιαστικά για να χωρίσουμε
        #το UI σε OCR text και structure data

        vendor = extract_vendor(extracted_text) #Πάιρνει το κέιμενο απο OCR το στέλνει στην συνάρτηση extract vendor
        #Επιστρέφει το αποτέλεσμα και το αποθηκεύει στη μεταβλητή vendor
        total = extract_total_amount(extracted_text) #παίρνει το ιδιο OCR text και ψάχνει για ποσά και επιστρέφει νούμερο στην μεταβλητη τοταλ
        date = extract_date(extracted_text) #το ίδιο αλλα για την ημερομηνία

        category, confidence = predict_category_with_confidence(vendor, extracted_text)

        st.write(f"🏪 **Vendor:** {vendor}") #Ποιό είναι το μαγαζί που έκοψε την απόδειξη
        st.write(f"💰 **Total Amount:** {total}") #ποιό είναι το τελικό ποσο
        st.write(f"📅 **Date:** {date}") #ποιά είναι η ημερομηνία
        st.write(f"🏷️ **Category:** {category}") #για να επιστρέφει την κατηγορία του καταστήματος
        st.write(f"**Confidence:** {confidence:.2%}") #πόσο σίγουρο είναι το μοντέλο για την κατηγορία

        if confidence < 0.6: #αν το confidence είναι κάτω απο 60% βγάλε warning
            st.warning("⚠️ Low confidence prediction. Please verify the category.")

        results_df = pd.DataFrame([ #φτιάχνουμε εναν πίνακα και βάζουμε μέσα ενα dictionary με τα αποτελέσματα
            {
                "vendor": vendor,
                "total_amount": total,
                "date": date,
                "category": category,
                "confidence": round(confidence, 4)
            }
        ])

        csv_data = results_df.to_csv(index=False).encode("utf-8") #Μετατρέπει τον πίνακα σε csv text
        #με το index=False για να μην έχω εξτρα αρίθμηση και το encode("utf-8") μετατρέπει το text
        #σε bytes, ώστε να μπορεί να το κατεβάσει το Streamlit σαν αρχείο

        st.download_button( #το κουμπι "download"
            label="Download Results as CSV", #Το κείμενο που θα βλέπει ο χρήστης
            data=csv_data, #το περιεχόμενο του αρχείου
            file_name="receipt_analysis_results.csv", #Το όνομα που θα έχει το αρχείο όταν κατέβει
            mime="text/csv" #πρόκειται για csv αρχείο
        )

        if st.button("➕ Add to History"): #εκτελείτε όταν πατάει κάποιος το κουμπί
            new_entry = {
                "vendor": vendor,
                "total_amount": total,
                "date": date,
                "category": category,
                "confidence": round(confidence, 4)
            }

            is_duplicate = any( #το any  επιστρέφει true/false αν βρει εγγραφη που ταιριάζει ή οχι
                entry["vendor"] == new_entry["vendor"] and #αν ισχύουν και τα 3 --> duplicate
                entry["total_amount"] == new_entry["total_amount"] and
                entry["date"] == new_entry["date"]
                for entry in st.session_state.history
            )

            if is_duplicate: #αν την απόδειξη την έχουμε ήδη δεν την ξαναβάζουμε
                st.warning("⚠️ This receipt is already in history.") #απλώς βγάζουμε warning
            else:
                st.session_state.history.append(new_entry)
                st.success("Receipt added to history!")

    else:
        st.warning("No text was extracted from the image.") #αν το OCR δεν βρεί τίποτα warning
else:
    st.info("Please upload a receipt image file.")

if st.session_state.history: #αν η λίστα δεν είναι άδεια (δηλαδή αν υπάρχει ιστορικό

    col1, col2 = st.columns([4, 1]) #δημιουργεί 2 στήλες col1: μεγάλη (τίτλος) , col2: μικρή (κουμπί)

    with col1:
        st.subheader("📂 Receipt History")

    with col2:
        if st.button("🗑️ Clear"): #όταν το πατήσεις καθαρίζει η στήλη
            st.session_state.history = []

    history_df = pd.DataFrame(st.session_state.history) #δημιουργείται ο πίνακας

    st.subheader("📊 Dashboard Summary") #τίτλος πάνω απο τα metrics

    total_receipts = len(history_df) #πόσες γραμμές έχει ο πίνακας
    total_spending = history_df["total_amount"].fillna(0).sum() #αρθοίζει τα πάντα απο το "total amount"
    average_spending = history_df["total_amount"].fillna(0).mean() #βρίσκει τον μ.ο. των ποσών
    top_category = history_df["category"].mode()[0] #βρίσκει την πιο συχνή "τιμή" απο τις κατηγορίες

    m1, m2, m3, m4 = st.columns(4) #φτιάχνει 4 στήλες δίπλα διπλα

    #st.metric : είναι ειδικό widget του streamlit για dashboard metrics
    with m1:
        st.metric("Total Receipts", total_receipts)

    with m2:
        st.metric("Total Spending", f"{total_spending:.2f}")

    with m3:
        st.metric("Average Spending", f"{average_spending:.2f}")

    with m4:
        st.metric("Top Category", top_category)

    st.dataframe(history_df) #δείχνει τον πίνακα στο app

    st.subheader("📈 Spending by Category") #βάζει τίτλο για το chart

    category_spending = history_df.groupby("category")["total_amount"].sum() #ομαδοποιεί τις γραμμές ανά
    #category και αθροίζει τα αντίστοιχα ποσά

    st.bar_chart(category_spending) #δημιουργεί αυτόματα bar chart σε αυτά τα aggregated data

    history_csv = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Full History CSV",
        data=history_csv,
        file_name="receipt_history.csv",
        mime="text/csv"
    )

