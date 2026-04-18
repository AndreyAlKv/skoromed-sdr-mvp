import json
# Загрузка enriched
with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
    enriched = json.load(f)
all_leads = []
for company in enriched:
    name = company.get('name', 'Unknown')
    for email in company.get('emails', []):
        all_leads.append({'name': name, 'type': 'email', 'value': email})
    for phone in company.get('phones', []):
        all_leads.append({'name': name, 'type': 'phone', 'value': phone})
# Уникальные (убрать дубли)
unique_leads = []
seen = set()
for lead in all_leads:
    key = f"{lead['type']}:{lead['value']}"
    if key not in seen:
        seen.add(key)
        unique_leads.append(lead)
print(f"✅ Создано {len(unique_leads)} уникальных лидов из {len(enriched)} компаний")
with open('src/data/all_leads.json', 'w', encoding='utf-8') as f:
    json.dump(unique_leads, f, ensure_ascii=False, indent=2)
print("✅ src/data/all_leads.json готов!")