import joblib
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "data", "expense_classifier.pkl")
# φορτώνουμε το μοντέλο μία φορά
model = joblib.load(model_path)

#θα επιστρέφει category + confidence
def predict_category_with_confidence(vendor, extracted_text):
    """
    Predicts expense category and returns confidence score.
    """
    vendor = vendor or ""
    extracted_text = extracted_text or ""

    combined_text = f"{vendor} {extracted_text}"

    prediction = model.predict([combined_text])[0]
    probabilities = model.predict_proba([combined_text])[0]

    max_confidence = max(probabilities)

    return prediction, max_confidence

