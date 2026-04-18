import pandas as pd
import os
import re
# ПРИОРИТЕТ CSV (leads.csv OK)
csv_files = ['enriched_stage2_leads.csv', 'fio_stage1_leads.csv', 'leads.csv']
csv_file = None
for file in csv_files:
    if os.path.exists(file):
        csv_file = file
        break
if csv_file:
    df = pd.read_csv(csv_file)
    print(f"✅ Загружен {csv_file}: {len(df)} лидов")
else:
    # ТЕСТ DF
    df = pd.DataFrame({
        'name': ['Erisman', 'Медкнижка', 'NV Medica', 'Sitimed', 'Mobil-Med'],
        'fio': ['Иванов И.И.', 'Петрова А.А.', 'Сидоров С.С.', 'Козлова К.К.', 'Михайлов М.М.'],
        'phone': ['84959532010', '79175738991', '74951501656', '74952129031', '74957810003'],
        'okved': ['56.10', '96.02', '47.29', '93', '95']
    })
    print("✅ Тест DF: 5 лидов")
# Фильтр
if 'status' in df.columns:
    df = df[df['status'].str.contains('✅', na=False)]
print("\n🤖 Этап 3: ЛЕГИТИМНАЯ РАССЫЛКА (ТОП 13)")
print("📋 РУЧНОЙ ЗАПУСК:\n1. Открой WA.me/[номер] или TG/VK.\n2. Ctrl+V шаблон + Enter.\n3. Жди 'Да' → шаблон 2.\n\n")
for idx, row in df.head(13).iterrows():
    fio = str(row.get('fio', 'Уважаемый клиент')).title()
    okved = str(row.get('okved', 'вашей отрасли'))
    phone = str(row.get('phone', ''))
    name = str(row.get('name', 'Клиент'))
    
    # ЧИСТЫЙ PHONE ДЛЯ WA.ME
    clean_phone = re.sub(r'[^\d]', '', phone)
    if clean_phone.startswith('8'):
        clean_phone = '7' + clean_phone[1:]
    wa_link = f"https://wa.me/{clean_phone}"
    
    # ШАБЛОН 1: СОГЛАСИЕ
    consent_template = f"""Уважаемый {fio} ({name})!
Источник: открытые данные ФНС/2GIS (38-ФЗ). Отказ: ответьте СТОП.
Соглашаетесь на инфо по медкнижкам для {okved}? 
Да (скидка 25% ул. 1-я Брестская, 66 +7(495)212-12-12) / Нет.
МЦ Скоромед https://2121212.ru/akcii"""
    
    print(f"✅ {idx+1}/13: {name}")
    print(f"   Phone: {phone} | WA: {wa_link}")
    print(f"   ФИО: {fio} | ОКВЭД: {okved}")
    print(f"   ШАБЛОН 1 (копипаст):")
    print(f"   ─────")
    print(consent_template)
    print(f"   ─────\n")
print("🎯 ОТПРАВЬ 13 КАСКАДОВ! После 'Да' — шаблон 2 ниже.")
print("\nШАБЛОН 2 (для 'Да'-ответов):")
print("Уважаемый {fio}! Для {okved}: скидка 25% медкнижка 15 мин ул. 1-я Брестская, 66 +7(495)212-12-12 https://2121212.ru/akcii. Источник: ФНС. СТОП.")
print("\nЛоги: notepad results.txt 'Да: X/13'")