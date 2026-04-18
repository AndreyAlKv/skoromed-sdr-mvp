# src/yandex_search.py - Улучшенный парсер Yandex (20+ лидов такси-парков)
import requests
from bs4 import BeautifulSoup
import json
import re
def search_yandex(query="такси парк Москва", limit=25):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    leads = []
    
    for page in range(3):  # 3 страницы = 30+ результатов
        url = f"https://yandex.ru/search/?text={query.replace(' ', '+')}&p={page}"
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Новые селекторы Yandex 2024
        items = soup.find_all('div', class_=re.compile(r'serp-item|organic'))
        for item in items[:10]:  # Топ 10 на страницу
            title_elem = item.find(['h2', 'h3', 'a'], class_=re.compile(r'title|name|organic'))
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Телефоны улучшенный regex
            text = item.get_text()
            phones = re.findall(r'[+78][\s\-\(\)\d]{10,16}', text)
            
            address_elem = item.find(class_=re.compile(r'address|location'))
            address = address_elem.get_text(strip=True)[:50] if address_elem else 'Москва'
            
            if title and ('такси' in title.lower() or 'парк' in title.lower() or 'автопарк' in title.lower()):
                lead = {
                    'name': title[:100],
                    'phones': phones[:2],
                    'address': address,
                    'url': item.find('a')['href'] if item.find('a') else url
                }
                leads.append(lead)
    
    # Уникальные + сортировка
    seen = set()
    unique_leads = []
    for lead in leads:
        key = lead['name'].lower()
        if key not in seen and len(unique_leads) < limit:
            seen.add(key)
            unique_leads.append(lead)
    
    print(f"✅ Yandex: {len(unique_leads)} лидов '{query}'")
    for lead in unique_leads[:5]:
        phone_str = ', '.join(lead['phones']) if lead['phones'] else 'нет'
        print(f"📞 {lead['name'][:50]} | Тел: {phone_str} | {lead['address']}")
    
    filename = f"src/data/yandex_{query.replace(' ', '_').lower()}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(unique_leads, f, ensure_ascii=False, indent=2)
    print(f"💾 Сохранено: {filename} ({len(unique_leads)} лидов)")
    
    return unique_leads
if __name__ == "__main__":
    search_yandex("такси парк Москва", 25)