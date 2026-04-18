import json
import csv
with open('src/data/all_leads.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)
print(f"✅ {len(leads)} лидов загружено")
with open('leads.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Компания', 'Тип', 'Контакт', 'Действие'])
    for lead in leads:
        writer.writerow([
            lead['name'],
            lead['type'],
            lead['value'],
            f'Скидка 25% ул. 1-я Брестская, 66 +7(495)212-12-12'
        ])
print("✅ leads.csv готов! Открой Excel")