# src/2gis_search.py - 2GIS лиды такси-парков (нуждаются в медкнижках)
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
API_KEY = os.getenv('TWOGIS_API_KEY') or 'c68d2854-3c26-442d-8a78-bf1a20927a1f'  # Демо ключ fallback
def search_2gis(query="такси парк Москва", limit=25):
    url = "https://catalogapi.2gis.com/1.0/search"
    params = {
        'q': query,
        'fields': 'items.id,items.name,items.address_name,items.phones,items.urls,items.rating',
        'limit': limit,
        'key': API_KEY
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            print(f"❌ 2GIS API ошибка {resp.status_code}: {resp.text[:100]}")
            return []
        data = resp.json()
        
        leads = []
        for item in data.get('items', []):
            lead = {
                'name': item['name'],
                'address': item.get('address_name', ''),
                'phones': [p.get('raw_value', '') for p in item.get('phones', [])],
                'url': item.get('urls', [{}])[0].get('url', '') if item.get('urls') else '',
                'rating': item.get('rating', 0)
            }
            leads.append(lead)
        
        print(f"✅ 2GIS: {len(leads)} лидов '{query}'")
        for lead in leads[:5]:
            phone = lead['phones'][0] if lead['phones'] else 'нет'
            print(f"📞 {lead['name']} | {phone} | {lead['address'][:50]} (рейтинг {lead['rating']})")
        
        filename = f"src/data/2gis_{query.replace(' ', '_').lower()}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(leads, f, ensure_ascii=False, indent=2)
        print(f"💾 Сохранено: {filename}")
        
        return leads
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []
if __name__ == "__main__":
    search_2gis("такси парк Москва", 25)