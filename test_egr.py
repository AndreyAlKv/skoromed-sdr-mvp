import requests
import json
KEY = "12c008fe31d9ae6711ad2fbea3d3d94f33626d85"
INN_TEST = "1032502271548"  # Docs пример (ДАЛЬЧЕРМЕТ)
r = requests.get(f"https://api-fns.ru/api/egr?req={INN_TEST}&key={KEY}")
print(f"✅ EGR: {r.status_code} | JSON keys: {list(r.json().keys())}")
data = r.json()
items = data.get('items', [])
print(f"Items len: {len(items)}")
if len(items) > 0:
    item = items[0]
    print(f"✅ Компания: {item.get('ЮЛ', {}).get('НаимПолнЮЛ', 'N/A')}")
    
    # PARSE OKVED
    okveds = set()
    osn = item.get('ЮЛ', {}).get('ОснВидДеят', {})
    if osn.get('Код'):
        okveds.add(osn['Код'][:2])
    dop = item.get('ЮЛ', {}).get('ДопВидДеят', [])
    for v in dop:
        if v.get('Код'):
            okveds.add(v['Код'][:2])
    print(f"OKVED группы: {okveds}")
    
    # REGION МОСКВА
    adres = item.get('ЮЛ', {}).get('Адрес', {})
    kod_reg = adres.get('КодРегион', '')
    poln = adres.get('АдресПолн', '')
    is_moscow = '77' in kod_reg or 'Москва' in poln
    print(f"Регион: {kod_reg} | Адрес: {poln[:50]}... | Москва: {is_moscow}")
    
    # КОНТАКТЫ + FИО
    fio = item.get('ЮЛ', {}).get('Руководитель', {}).get('ФИОПолн', 'N/A')
    phones = item.get('ЮЛ', {}).get('Контакты', {}).get('Телефон', [])
    emails = item.get('ЮЛ', {}).get('Контакты', {}).get('e-mail', [])
    print(f"FИО: {fio} | Phones: {phones[:2]} | Emails: {emails}")
    
    # ELIGIBLE ЛМК
    moscow_okved = {'56', '96', '93', '94', '95', '47', '46'}
    eligible = is_moscow and bool(okveds & moscow_okved)
    print(f"✅ ELIGIBLE ЛМК Москва: {eligible} (OKVED ∩ {moscow_okved})")
    
    # SAVE LEAD
    lead = {'inn': INN_TEST, 'name': item.get('ЮЛ', {}).get('НаимПолнЮЛ'), 'okved': list(okveds), 'region': kod_reg, 'fio': fio, 'phones': phones, 'emails': emails}
    print(f"Lead JSON: {json.dumps(lead, ensure_ascii=False, indent=2)}")
else:
    print("❌ Нет items для ИНН. Попробуй другой: 2540096950")