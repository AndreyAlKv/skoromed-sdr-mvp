# src/all_leads_merger.py - ЕДИНАЯ БД (все парсеры) + ФИКС JSON ERROR
import json
import os
files = [
    'src/data/msk_social_leads.json', 
    'src/data/moscow_max_leads.json', 
    'src/data/competitors_intercept.json',
    'src/data/enriched_companies.json', 
    'src/data/companies.json'
]
all_leads = []
for file in files:
    if os.path.exists(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                leads = data if isinstance(data, list) else data.get('items', [])
                all_leads.extend(leads)
                print(f"✅ Загружено {len(leads)} из {file}")
        except Exception as e:
            print(f"⚠️ Пропуск {file}: {e}")
json.dump(all_leads, open('src/data/all_leads.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"🚀 Единая БД: {len(all_leads)} лидов в src/data/all_leads.json")