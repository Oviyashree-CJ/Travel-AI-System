import re

def extract_destination(text):
    text = text.strip()

    patterns = [
        r"trip to\s+([A-Za-z ]+)",
        r"travel to\s+([A-Za-z ]+)",
        r"go to\s+([A-Za-z ]+)",
        r"visit\s+([A-Za-z ]+)",
        r"to\s+([A-Za-z ]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return text
