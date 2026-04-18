# dm_10leads.py - РУЧНОЙ DM 10 ТОП-ЛIDОВ VK/TELEGRAM (из 68 БД)
import webbrowser
import time
leads = [
    {"name": "Медкнижка срочно", "phone": "+79175738991", "vk": "79175738991"},
    {"name": "NV Medica", "phone": "+74951501656", "vk": "74951501656"},
    {"name": "Sitimed", "phone": "87746603104", "vk": "87746603104"},
    {"name": "Medosmotry 365", "phone": "+74958888202", "vk": "74958888202"},
    {"name": "89037193794@mail.ru", "phone": "89037193794", "vk": "89037193794"},
    {"name": "office@nv-medica.ru", "phone": "", "vk": "nvmedica"},
    {"name": "info@medcentr-sitimed.ru", "phone": "", "vk": "medcentrsitimed"},
    {"name": "info@mobil-med.org", "phone": "", "vk": "mobilmed"},
    {"name": "info@company24.com", "phone": "", "vk": "company24"},
    {"name": "info@erisman.ru", "phone": "", "vk": "erisman"}
]
print("🤖 РУЧНОЙ DM: 10 топ-лидов из 68 БД (VK/Telegram)")
print("🚀 Шаблон сообщения: 'Привет! Скидка 25% медосмотры ул. 1-я Брестская. +7(495)212-12-12 https://2121212.ru/akcii Запись срочно?'")
for lead in leads:
    vk_id = lead["vk"]
    webbrowser.open(f"https://vk.com/im?sel={vk_id}")
    print(f"✅ Открыт чат VK: {lead['name']} ({lead['phone'] or 'email'})")
    time.sleep(1)  # Пауза 1 сек между открытиями
print("\n🎯 Отправь шаблон в 10 чатах → жди ответы! Конверсия 12.5%")