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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            html = resp.text
            emails = extract_emails(html)
            phones = extract_phones(html)
            print(f"SUCCESS emails: {emails} phones: {phones}")
            return {'name': name, 'url': url, 'emails': emails, 'phones': phones}
    except:
        pass
    return {'name': name, 'url': url, 'emails': [], 'phones': []}
if __name__ == '__main__':
    try:
        df = pd.read_csv('data/fns_okved.csv')
        companies = df[['name', 'url']].drop_duplicates().to_dict('records')
    except:
        companies = []
    enriched = [enrich_company(c['url'], c['name']) for c in companies[:10]]  # Test 10
    with open('data/enriched_companies.json', 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False)
    print("Saved enriched_companies.json")