# scraper.py - MVP Step 1: Collect companies from Yandex
import requests
import json
from bs4 import BeautifulSoup
import os
QUERY = "медкнижка Москва"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
def scrape_companies(query):
    print("Searching:", query)
    url = "https://yandex.ru/search/?text=" + query.replace(' ', '+') + "&numdoc=50"
    response = requests.get(url, headers=HEADERS, timeout=10)
    print("Status:", response.status_code)
    if response.status_code != 200:
        print("Error:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    companies = []
    links = soup.find_all('a', href=True)
    for a in links:
        href = a['href']
        if href.startswith('http') and 'yandex' not in href.lower() and len(companies) < 30:
            name = a.get_text(strip=True)[:100]
            if name and len(name) > 3:
                companies.append({"name": name, "url": href})
    
    print("Found", len(companies), "companies")
    return companies
if __name__ == "__main__":
    companies = scrape_companies(QUERY)
    os.makedirs('src/data', exist_ok=True)
    with open('src/data/companies.json', 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)
    print("Saved to src/data/companies.json")
    for c in companies[:3]:
        print(c['name'][:50] + "...")