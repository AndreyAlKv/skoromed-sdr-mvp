import requests
from bs4 import BeautifulSoup
import re
import json
import time
import os
# Загрузка компаний
with open('src/data/companies.json', 'r', encoding='utf-8') as f:
    companies = json.load(f)
enriched = []
print(f"Loaded {len(companies)} companies")
for i, company in enumerate(companies, 1):
    name = company.get('name', 'Unknown')
    url = company.get('url', '')
    
    print(f"{i}/{len(companies)} {name}...")
    print(f"URL: {url}")
    
    try:
        # ФИКС: HEADERS + TIMEOUT
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Emails regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, soup.get_text())
            emails = list(set(emails))  # Уникальные
            
            # Phones regex (RU номера)
            phone_pattern = r'(\+?7|8)?[\s\-\(\)]*(\(?[0-9]{3}\)?[\s\-\)]*[0-9]{3}[\s\-\)]*[0-9]{2}[\s\-\)]*[0-9]{2})'
            phones_text = re.findall(phone_pattern, soup.get_text())
            phones = []
            for match in phones_text:
                phone = re.sub(r'[^\d+]', '', ''.join(match))
                if len(phone) in [10, 11, 12] and phone.startswith(('7', '8', '+7')):
                    phones.append(phone)
            phones = list(set(phones))  # Уникальные
            
            if emails or phones:
                print(f"SUCCESS emails: {emails} phones: {phones}")
                enriched.append({
                    'name': name,
                    'url': url,
                    'emails': emails,
                    'phones': phones
                })
            else:
                print(f"SUCCESS emails: [] phones: []")
                enriched.append({
                    'name': name,
                    'url': url,
                    'emails': [],
                    'phones': []
                })
        else:
            print(f"FAIL {response.status_code}")
            enriched.append({'name': name, 'url': url, 'emails': [], 'phones': []})
            
    except Exception as e:
        print(f"ERROR: {str(e)[:100]}")
        enriched.append({'name': name, 'url': url, 'emails': [], 'phones': []})
    
    # ФИКС: ЗАДЕРЖКА 2 сек (антибот)
    time.sleep(2)
# Сохранение
with open('src/data/enriched_companies.json', 'w', encoding='utf-8') as f:
    json.dump(enriched, f, ensure_ascii=False, indent=2)
print("✅ Saved enriched_companies.json")
# Вывод топ лидов
for e in enriched[:5]:
    print(f"- {e['name']} emails: {e['emails']} phones: {e['phones']}")