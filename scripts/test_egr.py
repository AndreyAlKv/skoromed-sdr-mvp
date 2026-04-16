import requests
import json
KEY = "12c008fe31d9ae6711ad2fbea3d3d94f33626d85"
def test_fns_stat():
    r = requests.get(f"https://api-fns.ru/api/stat?key={KEY}", timeout=10)
    print(f"🔑 Лимит ФНС: {r.status_code}")
    if r.status_code == 200:
        stat = r.json()
        print(f"📊 Used: {stat.get('used', 0)} / Total: {stat.get('total', 0)}")
    return r.status_code == 200
def test_egr(inn="7707083893"):  # Тест ИНН ФНС
    r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={KEY}", timeout=10)
    print(f"🔍 EGR {inn}: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        item = data.get('items', [{}])[0]
        юл = item.get('ЮЛ', {})
        okveds = set()
        osn = юл.get('ОснВидДеят', {})
        if osn.get('Код'):
            okveds.add(osn['Код'][:2])
        print(f"✅ Name: {юл.get('НаимПолнЮЛ', 'N/A')[:50]} | OKVED: {list(okveds)}")
    return r.status_code == 200
# Тест!
print("🤖 Тест FNS EGR Skoromed SDR...")
test_fns_stat()
test_egr()