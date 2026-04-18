# src/taxi_groups_parser.py - Перехват вопросов таксистов "медкнижка?"
import requests
from bs4 import BeautifulSoup
import json
import re
vk_groups = [
    'club16682109',   # Яндекс.Такси Москва (100k+)
    'club182273835',  # Такси Москва Работа
    'club189823045',  # Таксисты Москвы
    'public177768833' # Такси СПб
]
leads = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
for group in vk_groups:
    search_url = f"https://vk.com/search?c[q]=медкнижка&c[section]=statuses"
    resp = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    posts = soup.find_all('div', class_='wall_text') or soup.find_all('div', class_='post_content')
    for post in posts[:3]:
        text = post.get_text()
        if 'медкнижк' in text.lower() or 'медосмотр' in text.lower():
            phones = re.findall(r'[+78][\s\-\(\)\d]{10,16}', text)
            leads.append({
                'group': group,
                'phone': phones[0] if phones else 'нет',
                'post': text[:100],
                'url': f"https://vk.com/{group}"
            })
# Форумы (drive2 + taxi-forum)
forum_urls = [
    "https://www.drive2.ru/search?q=медкнижка+москва",
    "https://taxi-forum.ru/search.php?q=медкнижка"
]
for f_url in forum_urls:
    resp = requests.get(f_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    topics = soup.find_all('a', class_='topic-title') or soup.find_all('h3')
    for topic in topics[:3]:
        text = topic.get_text()
        phones = re.findall(r'[+78][\s\-\(\)\d]{10,16}', text)
        if 'медкнижк' in text.lower():
            leads.append({
                'phone': phones[0] if phones else 'нет',
                'post': text[:100],
                'site': 'forum',
                'url': f_url
            })
# Уникальные
unique_leads = {lead['post']: lead for lead in leads}.values()
leads = list(unique_leads)
print(f"✅ {len(leads)} свежих вопросов таксистов 'медкнижка?'")
for lead in leads[:5]:
    print(f"📞 {lead['phone']} | {lead['post'][:50]} | {lead.get('group', lead.get('site', ''))}")
with open('src/data/taxi_questions_today.json', 'w', encoding='utf-8') as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)
print("💾 src/data/taxi_questions_today.json → ОТВЕЧАЙ/ЗВОНИ!")