import requests
import re
import json
import time
import pandas as pd
def extract_emails(html):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\w+', html, re.IGNORECASE)
    return list(set([e.lower() for e in emails if '@' in e and len(e) > 5]))
def extract_phones(html):
    phones = re.findall(r'[\+]?[7|8][\s\-\(\)]?[\d]{3}[\s\-\(\)]?[\d]{3}[\s\-\(\)]?[\d]{2}[\s\-\(\)]?[\d]{2}', html)
    clean_phones = [re.sub(r'[^\d+]', '', p) for p in phones if len(re.sub(r'[^\d+]', '', p)) >= 10]
    return list(set(clean_phones))
def enrich_company(url, name):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            html = resp.text
            emails = extract_emails(html)
            phones = extract_phones(html)
            print(f"SUCCESS {name}: emails={len(emails)} phones={len(phones)}")
            return {'name': name, 'url': url, 'emails': emails, 'phones': phones}
        else:
            print(f"Status {resp.status_code} {name}")
    except Exception as e:
        print(f"Error {url}: {e}")
    return {'name': name, 'url': url, 'emails': [], 'phones': []}
if __name__ == '__main__':
    try:
        df = pd.read_csv('data/fns_okved.csv')
        companies = df[['name', 'url']].drop_duplicates().to_dict('records')
    except:
        print("No data/fns_okved.csv - skip enrich")
        companies = []
    
    enriched = []
    total = len(companies)
    for i, company in enumerate(companies[:10], 1):  # Test 10 first
        name = company.get('name', 'Unknown')[:50]
        url = company.get('url', '')
        print(f"{i}/{min(total,10)} {name}...")
        enriched.append(enrich_company(url, name))
        time.sleep(1.5)
    
    with open('data/enriched_companies.json', 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    
    print("Saved enriched_companies.json")