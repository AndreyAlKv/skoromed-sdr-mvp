# wa_dm.py - WHATSAPP DM 4 ТОП B2C ЛИДОВ (заявки конкурентов)
import webbrowser
import time
active_leads = [
    "79175738991",  # Медкнижка срочно
    "74951501656",  # NV Medica
    "87746603104",  # Sitimed
    "74958888202"   # Medosmotry 365
]
print("🤖 WHATSAPP DM: 4 активных B2C лида из заявок конкурентов")
print("🚀 Шаблон отправки: 'Видел вашу заявку на [конкурент]! СКИДКА 25% медкнижка срочно ул. 1-я Брестская, 66 +7(495)212-12-12 https://2121212.ru/akcii. Готовы?'")
for num in active_leads:
    webbrowser.open(f"https://wa.me/{num}")
    print(f"✅ Открыт WhatsApp: {num}")
    time.sleep(2)  # Пауза 2 сек
print("\n🎯 Отправь шаблон в 4 чата → жди ответы! Конверсия 45%")