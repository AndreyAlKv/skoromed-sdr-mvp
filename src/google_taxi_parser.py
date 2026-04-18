# src/google_taxi_parser.py - Перехват через Google "медкнижка такси" VK/форумы
import requests
from bs4 import BeautifulSoup
import json
import re
queries = [
    'медкнижка такси москва site:vk.com',
    'медосмотр такси срочно site:drive2.ru',
    'медкнижка яндекс такси москва site:taxi-forum.ru',
    'нужна медкнижка москва такси site:vk.com/club'
]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
leads = []
for query in queries:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=20"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    results = soup.find_all('div', class_='g')[:5]
    for result in results:
        title = result.find('h3').get_text() if result.find('h3') else ''
        snippet = result.get_text()
        phones = re.findall(r'[+78][\s\-\(\)\d]{10,16}', snippet)
        if 'медкнижк' in title.lower() or 'медосмотр' in title.lower():
            leads.append({
                'query': query,
                'title': title[:100],
                'phones': phones[:1],
                'snippet': snippet[:100],
                'url': result.find('a')['href'] if result.find('a') else ''
            })
# Уникальные
unique_leads = []
seen = set()
for lead in leads:
    key = lead['title']
    if key not in seen:
        seen.add(key)
        unique_leads.append(lead)
print(f"✅ {len(unique_leads)} свежих постов 'медкнижка такси?' из Google/VK/форумов")
for lead in unique_leads[:5]:
    phone = lead['phones'][0] if lead['phones'] else 'нет'
    print(f"📞 {phone} | {lead['title'][:50]} | {lead['query']}")
with open('src/data/google_taxi_leads.json', 'w', encoding='utf-8') as f:
    json.dump(unique_leads, f, ensure_ascii=False, indent=2)
print("💾 src/data/google_taxi_leads.json → ОТВЕЧАЙ В ГРУППАХ/ЗВОНИ!")