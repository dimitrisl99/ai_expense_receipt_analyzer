import re


def extract_total_amount(text):
    """
    Tries to find 'TOTAL' or 'TOTAL AMOUNT' specifically.
    More reliable than just max().
    """

    cleaned_text = text.replace("S", "$").replace("s", "$")

    # 🔹 ψάχνουμε γραμμές που περιέχουν TOTAL
    lines = cleaned_text.split("\n")

    for line in lines:
        if "total" in line.lower():
            match = re.search(r"(\d+[.,]\d{2})", line)
            if match:
                value = match.group(1).replace(",", ".")
                return float(value)

    # 🔹 fallback
    amounts = re.findall(r"(\d+[.,]\d{2})", cleaned_text)

    if amounts:
        numeric_amounts = [float(a.replace(",", ".")) for a in amounts]
        return max(numeric_amounts)

    return None

#Vendor : Το κατάστημα που έκοψε την απόδειξη
def extract_vendor(text):
    """
    Simple heuristic: first line is usually the vendor.
    """

    lines = text.split("\n")

    for line in lines:
        clean_line = line.strip()
        if len(clean_line) > 3:
            return clean_line

    return None

#Για ημερομηνίες
def extract_date(text): #νέα func που πάλι παίρνει το OCR text
    """
    Extracts and cleans date.
    """

    date_patterns = [ #βάζουμε την λίστα με regex patterns --> ψάξε για ημερομηνία σε αυτά τα πιθανά formats
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b"
    ]
    for pattern in date_patterns: #περνάμε ένα ένα τα patterns
        match = re.search(pattern, text) #ψάχνουμε αν υπάρχει στο OCR text μια ημερομηνία που ταιριάζει
        if match:
            date = match.group()
            # 🔹 fix common OCR errors
            date = date.replace("7", "2", 1) if date.endswith("7019") else date

            return date

    return None