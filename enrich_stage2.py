import requests
import pandas as pd
import re
import csv
# API КЛЮЧИ (бесплатно: 2gis.ru/developer, fss.ru)
def enrich_fss(inn):
    """Численность из ФСС"""
    try:
        r = requests.get(f"https://api-fss.ru/v1/inn/{inn}/employees", timeout=10)
        return r.json().get("employee_count", 0)
    except:
        return 0
def checks_proverki(inn):
    """Реестр проверок"""
    try:
        r = requests.get(f"https://proverki.gov.ru/api/v1/search?inn={inn}", timeout=10)
        checks = r.json().get("checks", [])
        med_checks = [c for c in checks if "медкнижк" in c.get("desc", "").lower()]
        return med_checks[0].get("result", "") if med_checks else "Нет"
    except:
        return "Ошибка"
def rkn_blacklist(phone):
    """РКН чёрный список (отказы реклама/PD)"""
    try:
        r = requests.get(f"https://eais.rkn.gov.ru/api/v1/phone/{phone.replace('+7','8')}")
        return r.json().get("blacklisted", False)
    except:
        return False
# Загрузка Этапа 1
df = pd.read_csv('parsed_stage1_leads.csv')
print("🤖 Этап 2: Обогащение (численность/проверки/теги/черные)")
for idx, row in df.iterrows():
    inn = row.get('inn', '')
    phone = row.get('phone', '')
    
    # Обогащение
    emp_count = enrich_fss(inn)
    checks = checks_proverki(inn)
    blacklisted = rkn_blacklist(phone)
    tag = "priority_high" if emp_count >=5 else "low"
    ready_tag = "горячий" if re.search(r'ваканси|набираем', row.get('name', '')) else "холодный"
    
    df.at[idx, 'emp_count'] = emp_count
    df.at[idx, 'checks'] = checks
    df.at[idx, 'blacklisted'] = blacklisted
    df.at[idx, 'priority_tag'] = tag
    df.at[idx, 'ready_tag'] = ready_tag
    
    if blacklisted:
        df.at[idx, 'status'] = "❌ Черный список"
    
    print(f"✅ {row['name']}: emp={emp_count}, тег={tag}, проверки={checks[:50]}")
# Фильтр: Убрать черные, сохранить high
df_filtered = df[df['blacklisted'] == False].sort_values('emp_count', ascending=False)
df_filtered.to_csv('enriched_stage2_leads.csv', index=False, encoding='utf-8-sig')
print(f"✅ {len(df_filtered)} обогащённых лидов → enriched_stage2_leads.csv!")