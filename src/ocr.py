import easyocr #φέρνουμε την βιβλιοθήκη OCR
import numpy as np #ρησιμοποιούμε τη NumPy για να μετατρέψουμε την εικόνα σε μορφή που μπορεί να διαβάσει το OCR
from PIL import Image #η Pillow μάς βοηθά να ανοίξουμε την εικόνα


def extract_text_from_image(uploaded_file):
    """
    Takes an uploaded image file from Streamlit,
    runs OCR on it, and returns the extracted text.
    """

    image = Image.open(uploaded_file) #ανοίγουμε το αρχείο της εικόνας
    image_array = np.array(image) #μετατρέπουμε την εικόνα σε array

    #εδώ δημιουργούμε τον OCR reader
    reader = easyocr.Reader(["en"], gpu=False) #το en σημαίνει οτι ο reader θα διαβάζει αγγλικά
    #και του λέμε να τρέξει σε cpu
    results = reader.readtext(image_array, detail=0) #το EasyOCR κοιτάζει την εικόνα και επιστρέφει τα
    #κομμάτια κειμένου που βρήκε , το detail = 0 --> θέλουμε το κείμενο οχι πολλές τεχνικές λεπτομέριες

    extracted_text = "\n".join(results) #το result είναι λίστα απο μικρά κομμάτια κειμένου
    #εδώ τα ενώνουμε με αλλαγή γραμμής ανάμεσα

    return extracted_text #επιστρέφει η συνάρτηση του τελικό text

