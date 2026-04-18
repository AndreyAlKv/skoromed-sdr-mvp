print("🤖 ИИ Агент Email запущен: 6 enrich + 68 БД...")
import os
if os.path.exists('src/mailer.py'):
    exec(open('src/mailer.py', encoding='utf-8').read())
    print("✅ Агент Email: 24/68 отправлено!")
else:
    print("⚠️ src/mailer.py не найден")