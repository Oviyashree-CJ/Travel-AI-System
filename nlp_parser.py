import re

def extract_destination(text):
    match = re.search(r"to\s+([A-Za-z ]+)", text)
    return match.group(1).strip() if match else None
