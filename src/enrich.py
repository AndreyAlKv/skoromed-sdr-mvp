# enrich.py - MVP Step 3: Extract emails/phones from company websites
import json
import requests
import re
from bs4 import BeautifulSoup
import os
import time
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def find_contacts(html_text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html_text)
    phones = re.findall(r'(?:\+7|8|7)[\s\-\(\)]?\d{3}[\s\-\(\)]?\d{3}[\s\-\(\)]?\d{2}[\s\-\(\)]?\d{2}', html_text)
    emails = list(set([e.lower() for e in emails if len(e) > 5]))[:3]
    phones = list(set([re.sub(r'[^\d+]', '', p) for p in phones if len(re.sub(r'[^\d]', '', p)) == 11]))[:3]
    return emails, phones
if __name__ == "__main__":
    with open('src/data/companies.json', 'r', encoding='utf-8') as f:
        companies = json.load(f)
    print(f"Loaded {len(companies)} companies")
    
    enriched = []
    for i, company in enumerate(companies, 1):
        print(f"\n{i}/{len(companies)} {company['name'][:50]}...")
        print(f"URL: {company['url']}")
        try:
            resp = requests.get(company['url'], headers=HEADERS, timeout=15)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                emails, phones = find_contacts(text)
                company['emails'] = emails
                company['phones'] = phones
                print(f"SUCCESS emails: {emails} phones: {phones}")
            else:
                company['emails'] = []
                company['phones'] = []
                print(f"FAIL {resp.status_code}")
        except Exception as e:
            print(f"ERROR: {str(e)[:80]}")
            company['emails'] = []
            company['phones'] = []
        enriched.append(company)
        time.sleep(2)
    
    with open('src/data/enriched_companies.json', 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print("\n✅ Saved enriched_companies.json")
    for c in enriched[:2]:
        print(f"- {c['name'][:30]} emails: {c.get('emails',[])} phones: {c.get('phones',[])}")