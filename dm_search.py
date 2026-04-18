# dm_search.py - VK/TELEGRAM ПОИСК 10 ЛИДОВ (реальные номера)
import webbrowser
import time
searches = [
    "Медкнижка срочно +79175738991",
    "NV Medica +74951501656",
    "Sitimed медкнижка 87746603104",
    "Medosmotry 365 +74958888202",
    "89037193794@mail.ru медкнижка",
    "office@nv-medica.ru",
    "info@medcentr-sitimed.ru",
    "info@mobil-med.org",
    "info@company24.com медосмотры",
    "info@erisman.ru"
]
print("🤖 DM ПОИСК: VK/Telegram по 10 лидам")
print("🚀 Шаблон: 'Скидка 25% медосмотры! +7(495)212-12-12 https://2121212.ru'")
for search in searches:
    # VK поиск
    vk_query = search.replace(' ', '+').replace('@', '').replace('.', '').replace(',', '')
    webbrowser.open(f"https://vk.com/search?c%5Bq%5D={vk_query}")
    print(f"✅ VK поиск: {search}")
    time.sleep(1)
    
    # Telegram поиск
    webbrowser.open(f"https://t.me/{search.lower().replace(' ', '_').replace('@', '').replace('.', '')}")
    print(f"✅ Telegram: t.me/{search.lower().replace(' ', '_')}")
print("\n🎯 Найди группы/пользователей → DM шаблон → ответы!")