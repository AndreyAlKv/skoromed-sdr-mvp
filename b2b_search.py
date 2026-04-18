import requests
import pandas as pd
import json
import time
KEY = "12c008fe31d9ae6711ad2fbea3d3d94f33626d85"
# ТЕСТ ЛИМИТА ФНС
def test_fns():
    r = requests.get(f"https://api-fns.ru/api/stat?key={KEY}", timeout=10)
    print(f"🔑 Лимит ФНС: {r.status_code}")
    if r.status_code == 200:
        stat = r.json()
        print(f"📊 Used: {stat.get('used', 0)} / Total: {stat.get('total', 0)}")
    else:
        print("❌ Ключ проблема — новый api-fns.ru!")
    return r.status_code == 200
def fetch_egr(inn):
    r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={KEY}", timeout=10)
    if r.status_code != 200:
        return {}
    data = r.json()
    items = data.get('items', [])
    if len(items) == 0:
        return {}
    item = items[0]
    юл = item.get('ЮЛ', {})
    
    okveds = set()
    osn = юл.get('ОснВидДеят', {})
    if osn.get('Код'):
        okveds.add(osn['Код'][:2])
    dop = юл.get('ДопВидДеят', [])
    for v in dop:
        if v.get('Код'):
            okveds.add(v['Код'][:2])
    
    adres = юл.get('Адрес', {})
    kod_reg = adres.get('КодРегион', '')
    poln = adres.get('АдресПолн', '')
    is_moscow = '77' in kod_reg or 'Москва' in poln
    
    fio = юл.get('Руководитель', {}).get('ФИОПолн', 'Клиент')
    phones = юл.get('ЮЛ', {}).get('Контакты', {}).get('Телефон', [])[:2]
    emails = юл.get('ЮЛ', {}).get('Контакты', {}).get('e-mail', [])
    
    status = юл.get('Статус', '')
    
    print(f"  📋 {юл.get('НаимПолнЮЛ', 'N/A')[:50]} | ОКВЭД={list(okveds)} | Москва={is_moscow}")
    
    return {
        'inn': inn, 'name': юл.get('НаимПолнЮЛ'), 'okved': list(okveds),
        'region': kod_reg, 'moscow': is_moscow, 'fio': fio,
        'phones': phones, 'emails': emails, 'status': status
    }
def search_wide():
    params = {
        'q': 'кафе салон магазин фитнес медкнижка Москва',  # Шире — больше!
        'filter': 'region77+active',  # Москва + active
        'key': KEY
    }
    r = requests.get("https://api-fns.ru/api/search", params=params, timeout=15)
    print(f"🔍 Широкий поиск: {r.status_code}")
    if r.status_code != 200:
        return []
    items = r.json().get('items', [])[:100]  # 100 кандидатов!
    print(f"🔍 Нашёл {len(items)} кандидатов...")
    time.sleep(1)  # Пауза лимит
    
    good_okved = {'56', '96', '93', '47', '46'}
    leads = []
    
    for item in items:
        inn = item.get('ИНН', '')
        if inn:
            lead = fetch_egr(inn)
            ok_set = set(lead.get('okved', []))
            if lead.get('moscow') and (ok_set & good_okved) and 'Действующее' in lead.get('status', ''):
                leads.append(lead)
                print(f"✅ НАШЁЛ! {lead['name'][:40]} | {lead['fio']} | Тел: {lead['phones']}")
    
    return leads
# Fallback — тестовые лиды (если ФНС пусто!)
def fallback_leads():
    return pd.DataFrame([
        {'inn': 'test1', 'name': 'Test Cafe Москва', 'okved': ['56'], 'region': '77', 'moscow': True, 'fio': 'Иванов И.И.', 'phones': ['+74951234567'], 'emails': ['test@mail.ru'], 'status': 'Действующее'},
        {'inn': 'test2', 'name': 'Test Salon Москва', 'okved': ['96'], 'region': '77', 'moscow': True, 'fio': 'Петрова А.А.', 'phones': ['+79161234567'], 'emails': ['salon@mail.ru'], 'status': 'Действующее'},
        {'inn': 'test3', 'name': 'Test Fitness Москва', 'okved': ['93'], 'region': '77', 'moscow': True, 'fio': 'Сидоров В.В.', 'phones': ['+79533626602'], 'emails': ['fit@mail.ru'], 'status': 'Действующее'},
        {'inn': 'test4', 'name': 'Test Магазин Москва', 'okved': ['47'], 'region': '77', 'moscow': True, 'fio': 'Козлова Е.Е.', 'phones': ['+74952129031'], 'emails': ['shop@mail.ru'], 'status': 'Действующее'},
        {'inn': 'test5', 'name': 'Test Опт Москва', 'okved': ['46'], 'region': '77', 'moscow': True, 'fio': 'Федоров Д.Д.', 'phones': ['+74957810003'], 'emails': ['opt@mail.ru'], 'status': 'Действующее'},
    ])
# Запуск!
print("🤖 Робот: Тест + поиск + fallback...")
if test_fns():
    leads = search_wide()
else:
    print("🔑 Проблема ключа — fallback...")
    leads_df = fallback_leads()
    leads = leads_df.to_dict('records')
df = pd.DataFrame(leads)
df.to_csv('fns_cafe_moscow.csv', index=False, encoding='utf-8-sig')
print(f"\n🎉 {len(leads)} компаний в fns_cafe_moscow.csv!")
if len(df) > 0:
    print("\nТаблица:")
    print(df[['name', 'fio', 'phones', 'emails', 'okved', 'region']].head())
else:
    df = fallback_leads()
    df.to_csv('fns_cafe_moscow.csv', index=False)
    print("🛡️ Fallback сохранён (5 тестовых)!")