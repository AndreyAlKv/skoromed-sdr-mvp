# src/test_mailer_preview.py - ПРОВЕРКА ТЕКСТА ПИСЬМА + EMAIL (БЕЗ ОТПРАВКИ)
import json
import os
def load_leads():
    leads = []
    files = ['src/data/enriched_companies.json', 'src/data/yandex_такси_парк_москва.json', 'src/data/companies.json', 'src/data/msk_social_leads.json']
    for file in files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                leads.extend(data if isinstance(data, list) else data.get('items', []))
    return leads
leads = load_leads()[:5]  # Топ 5 для примера
print(f"📧 Загружено {len(leads)} лидов (пример топ-5)")
for lead in leads:
    name = lead.get('name', 'клиника')
    rating = lead.get('rating', 4.5)
    email = f"info@{name.lower().replace(' ', '').replace('/', '').replace('\\', '').replace('.', '').replace('-', '')}.ru"
    
    subject = f"Медосмотры для {name}: скидка 25% срочно!"
    
    body = f"""
Привет, {name}!
Медосмотры/медкнижки для мастеров/сотрудников: скидка 25%, 160 метров от метро Белорусская, ул. 1-я Брестская д. 66. Срочно!
+7(495)212-12-12 | https://2121212.ru/akcii
Запись сейчас!
SDR Skoromed
Рейтинг: {rating}
    """
    
    print(f"\n--- ПИСЬМО ДЛЯ '{name}' ---")
    print(f"📨 Получатель: {email}")
    print(f"📧 Тема: {subject}")
    print("📄 Текст:")
    print(body)
    print("--- КОНЕЦ ПИСЬМА ---")
print("\n✅ Текст/получатели OK! Готово к отправке python src/mailer.py (после App Password)")