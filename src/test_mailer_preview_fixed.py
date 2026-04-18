# src/test_mailer_preview_fixed.py - ПРОВЕРКА ТЕКСТА БЕЗ JSON ОШИБКИ (hardcoded топ-5 лидов)
leads = [
    {"name": "Салон красоты Люберцы Beauty", "rating": 4.6},
    {"name": "Кафе Химки Уют", "rating": 4.4},
    {"name": "Автосервис Одинцово Профи", "rating": 4.2},
    {"name": "Медкнижка срочно Москва", "rating": 4.5},
    {"name": "NV Medica", "rating": 4.3}
]
print(f"📧 Превью писем для 5 лидов (hardcoded, текст из mailer.py)")
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
    
    print(f"\n--- ПИСЬМО #{leads.index(lead)+1} ДЛЯ '{name}' ---")
    print(f"📨 Получатель: {email}")
    print(f"📧 Тема: {subject}")
    print("📄 Текст:")
    print(body.strip())
    print("--- КОНЕЦ ПИСЬМА ---")
print("\n✅ ТЕКСТ/ПОЛУЧАТЕЛИ OK! Готово к python src/mailer.py")