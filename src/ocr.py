import easyocr
import numpy as np
from PIL import Image


def extract_text_from_image(uploaded_file):
    """
    Takes an uploaded image file from Streamlit,
    runs OCR on it, and returns the extracted text.
    """

    image = Image.open(uploaded_file)
    image_array = np.array(image)

    reader = easyocr.Reader(["en"], gpu=False)
    results = reader.readtext(image_array, detail=0)

    extracted_text = "\n".join(results)

    return extracted_text

