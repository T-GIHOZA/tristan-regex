import re
import json
from pathlib import Path

input_path = Path("../input/raw-text.txt")

with open(input_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

alu_official_pattern = r'\b[a-zA-Z0-9._%+-]+@alueducation\.com\b'
alu_alumni_pattern = r'\b[a-zA-Z0-9._%+-]+@alumni\.alueducation\.com\b'
alu_si_pattern = r'\b[a-zA-Z0-9._%+-]+@si\.alueducation\.com\b'

url_pattern = r'https?://[^\s]+'

phone_pattern = r'(\+\d{1,3}\s?)?(\(?\d{2,4}\)?[\s-]?)?\d{3}[\s-]?\d{3,4}'

credit_card_pattern = r'\b(?:\d{4}[- ]?){3}\d{4}\b'

emails = re.findall(email_pattern, raw_text)

alu_official = re.findall(alu_official_pattern, raw_text)
alu_alumni = re.findall(alu_alumni_pattern, raw_text)
alu_si = re.findall(alu_si_pattern, raw_text)

urls = re.findall(url_pattern, raw_text)

phones = [
    ''.join(match).strip()
    for match in re.findall(phone_pattern, raw_text)
]

credit_cards = re.findall(credit_card_pattern, raw_text)

safe_emails = []

for email in emails:
    if "<script>" not in email.lower():
        safe_emails.append(email)

safe_urls = []

for url in urls:
    if not url.lower().startswith("javascript:"):
        safe_urls.append(url)

masked_cards = []

for card in credit_cards:
    clean = re.sub(r'[- ]', '', card)
    masked = "**** **** **** " + clean[-4:]
    masked_cards.append(masked)

results = {
    "emails": safe_emails,
    "alu_official_emails": alu_official,
    "alu_alumni_emails": alu_alumni,
    "alu_si_emails": alu_si,
    "urls": safe_urls,
    "phone_numbers": phones,
    "credit_cards_masked": masked_cards
}

output_path = Path("../output/sample-output.json")

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print(json.dumps(results, indent=4))