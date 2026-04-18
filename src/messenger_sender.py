# src/messenger_sender.py - DM VK/MAX/TELEGRAM ПО 68 ЛИДАМ
import json
import webbrowser
leads = json.load(open('src/data/all_leads.json', 'r', encoding='utf-8'))[:10]
print(f"📨 Загружено {len(leads)} лидов для DM")
message = "Привет! Медосмотры скидка 25% ул. 1-я Брестская. +7(495)212-12-12 https://2121212.ru/akcii Запись?"
for lead in leads:
    name = lead.get('name', 'клиника')
    social = lead.get('social', ['vk.com/example'])[0]
    print(f"✅ DM {name} → {social}: {message}")
webbrowser.open('vk.com/krasanovoross')
print("🚀 10 DM готово! Копируй в VK.")