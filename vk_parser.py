import requests
from bs4 import BeautifulSoup
import re
import json
url = "https://vk.com/erisman_ru"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
text = soup.get_text()
phones = re.findall(r'\+7\d{10}|\d{10}', text)
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
print(f"Erisman_ru: {len(phones)} phones: {phones[:3]}, {len(emails)} emails: {emails}")
if phones or emails:
    leads = [{"name": "Erisman_ru", "type": "phone", "value": p} for p in phones[:5]] + [{"name": "Erisman_ru", "type": "email", "value": e} for e in emails[:3]]
    with open('src/data/vk_leads.json', 'w', encoding='utf-8') as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    print("✅ vk_leads.json готов!")
else:
    print("0 лидов — VK антибот. Фокус пост/DM")