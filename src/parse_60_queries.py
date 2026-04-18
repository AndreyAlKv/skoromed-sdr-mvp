import requests
from bs4 import BeautifulSoup
import json
import re
# 60 QUERY ВНУТРИ (если txt проблема)
queries = [
"магазин одежды Москва Химки рейтинг 4 телефон сайт VK telegram",
"салон красоты Люберцы Подмосковье рейтинг 4.5 телефон instagram сайт",
"автосервис Одинцово рейтинг 4 телефон ФИО директора VK telegram",
"кафе Химки рейтинг 4 телефон общепит сайт instagram",
"частный детский сад Реутов рейтинг 4.5 телефон директор VK",
"продукты магазин Красногорск рейтинг 4 телефон сайт telegram",
"электроника розница Балашиха рейтинг 4 телефон instagram",
"парикмахерская Мытищи рейтинг 4 телефон сайт VK",
"ресторан фастфуд Люберцы рейтинг 4 телефон telegram instagram",
"курсы английского частные Одинцово рейтинг 4.5 сайт VK"
]  # Топ 10 для теста (полные 60 в txt)
leads = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
for query in queries:
    url = f"https://yandex.ru/search/?text={query.replace(' ', '+')}&lr=213"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Улучшенный поиск элементов Yandex
    items = soup.find_all('li', class_='serp-item')[:5]
    for item in items:
        text = item.get_text()
        # Название компании
        name_match = re.search(r'([А-ЯЁ][а-яё\s]+?)(?=\s+(рейтинг|отзывы|тел|vk|сайт))', text)
        name = name_match.group(1).strip() if name_match else ''
        # Телефоны
        phones = re.findall(r'8\s*\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}|[\+78]\s*\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', text)
        # Сайты
        websites = re.findall(r'https?://[\w\.-]+\.(ru|com|by|su|net)/?', text)
        # Соцсети
        social = re.findall(r'(vk\.com|t\.me|instagram\.com|ok\.ru|fb\.com)/[\w\.-]+', text)
        # Рейтинг
        rating_match = re.search(r'(\d[.,]\d)\s*(из|баллов)', text)
        rating = float(rating_match.group(1).replace(',', '.')) if rating_match else 0
        
        if rating > 4.0 and (phones or websites or social) and name:
            leads.append({
                'name': name[:50],
                'phones': phones[:2],
                'website': websites[0] if websites else '',
                'social': list(set(social))[:3],
                'rating': rating,
                'query': query
            })
print(f"✅ {len(leads)} лидов с сайтом/соцсетями (из {len(queries)} query)")
for lead in leads[:5]:
    print(f"📱 {lead['name']} | Тел: {lead['phones'] or 'нет'} | Сайт: {lead['website'] or 'нет'} | Соц: {lead['social']}")
with open('src/data/msk_social_leads.json', 'w', encoding='utf-8') as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)
print("💾 src/data/msk_social_leads.json готов! Проверь notepad src/data/msk_social_leads.json")