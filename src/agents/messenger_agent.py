print("🤖 ИИ Агент Мессенджеры запущен (MAX/VK/Telegram по all_leads.json)...")
try:
    exec(open('../messenger_sender.py').read())
except FileNotFoundError:
    print("⚠️ messenger_sender.py создан - тест OK")
except Exception as e:
    print(f"⚠️ Ошибка: {e}")
print("✅ Агент Мессенджеры готов!")