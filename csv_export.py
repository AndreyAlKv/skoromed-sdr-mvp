import json
import csv
with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)
with open('leads_moskva.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'URL', 'Emails', 'Phones'])
    for lead in leads:
        emails_str = '; '.join(lead.get('emails', []))
        if emails_str:  # Только лиды с emails
            writer.writerow([
                lead.get('name', ''),
                lead.get('url', ''),
                emails_str,
                '; '.join(lead.get('phones', []))
            ])
print(f"✅ CSV готов: {len([l for l in leads if l.get('emails')])} лидов! Открой в Excel.")