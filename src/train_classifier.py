import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_expense_classifier():
    # 1. Διαβάζουμε το dataset
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "expense_categories.csv")

    df = pd.read_csv(csv_path)

    # 2. Features και labels
    df["combined_text"] = df["vendor"].fillna("") + " " + df["text"].fillna("")

    X = df["combined_text"]
    y = df["category"] #tager = category

    # 3. Χωρίζουμε train/test
    X_train, X_test, y_train, y_test = train_test_split( #τα χωρίζουμε σε 2 μέρη, training set για να μάθε το μοντέλο
        #test set για να δούμε πόσο καλά τα πάει σε νέα δεδομένα
        X, y, test_size=0.2, random_state=42,stratify=y
    )
    #To stratify=y το χρησημοποιούμε γιατί ουσιαστικά λέει στο split "μοίρασε τα δεδομένα έτσι ώστε κάθε κατηγορία
    #να εκπροσωπείται αναλογικά και στο train και στο test

    # 4. Φτιάχνουμε pipeline
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)), #μια λέξη την φορά και 2 λέξεις μαζί
        ("classifier", LogisticRegression(max_iter=1000)) #περνά τους αριθμούς στο Logistic Regression classifier
    ])

    # 5. Εκπαίδευση
    model.fit(X_train, y_train) #εδώ είναι που μαθαίνει το μοντέλο

    # 6. Predictions
    y_pred = model.predict(X_test) #εδώ κάνει προβλέψεις στο test set

    # 7. Metrics
    accuracy = accuracy_score(y_test, y_pred) #Θα μετρήσουμε πόσες προβλέψεις βγήκαν σωστές
    print("Accuracy:", accuracy)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred, zero_division=0)) #αν μια κατηγορία δεν έχει prediction
    #μην πετάς warning απλά βάλε 0 --> για πιο καθαρό output

    # 8. Save model
    model_path = os.path.join(base_dir, "data", "expense_classifier.pkl")
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")


if __name__ == "__main__":
    train_expense_classifier()