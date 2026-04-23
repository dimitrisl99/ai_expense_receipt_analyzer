import re


def extract_total_amount(text):

    #Tries to find 'TOTAL' or 'TOTAL AMOUNT' specifically.
    #More reliable than just max().


    cleaned_text = text.replace("S", "$").replace("s", "$")

    lines = cleaned_text.split("\n")

    for line in lines:
        if "total" in line.lower():
            match = re.search(r"(\d+[.,]\d{2})", line)
            if match:
                value = match.group(1).replace(",", ".")
                return float(value)

    # fallback
    amounts = re.findall(r"(\d+[.,]\d{2})", cleaned_text)

    if amounts:
        numeric_amounts = [float(a.replace(",", ".")) for a in amounts]
        return max(numeric_amounts)

    return None


def extract_vendor(text):

    # Simple heuristic: first line is usually the vendor.

    lines = text.split("\n")

    for line in lines:
        clean_line = line.strip()
        if len(clean_line) > 3:
            return clean_line

    return None

#for dates
def extract_date(text):

    # Extracts and cleans date.

    date_patterns = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date = match.group()
            date = date.replace("7", "2", 1) if date.endswith("7019") else date

            return date

    return None