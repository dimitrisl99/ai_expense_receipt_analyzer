import joblib


def test_classifier():
    model = joblib.load("data/expense_classifier.pkl") #φορτώνει το αποθηκευμένο μοντέλο απο το αρχείο .pkl

    test_vendors = [ #Λίστα με παραδείγματα που θέλουμε να δοκιμαστούν
        "Starbucks",
        "Shell",
        "Zara",
        "Vodafone",
        "Pharmacy",
        "Uber",
        "IKEA",
        "McDonalds",
        "Cosmote",
        "Hospital",
        "Kiosk",
        "Amazon"
    ]

    print("Expense Category Predictions:\n")

    for vendor in test_vendors:
        prediction = model.predict([vendor])[0] #για αυτό το vendor πες μου κατηγορία
        print(f"{vendor} --> {prediction}")


if __name__ == "__main__":
    test_classifier()