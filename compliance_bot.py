import telebot
import os
from dotenv import load_dotenv
import pandas as pd
import datetime
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    print("❌ ОШИБКА: TELEGRAM_TOKEN не найден в .env!")
    exit(1)
bot = telebot.TeleBot(TOKEN)
opt_in_users = set()  # Prod: Загрузка из CSV
csv_path = 'data/opt_in_leads.csv'
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Skoromed SDR Bot\n\n/optin — Согласие на рассылку (152-ФЗ OK)\n/leads — Получить шаблоны лидов")
@bot.message_handler(commands=['optin'])
def opt_in(message):
    user_id = str(message.from_user.id)
    if user_id not in opt_in_users:
        opt_in_users.add(user_id)
        os.makedirs('data', exist_ok=True)
        df_new = pd.DataFrame({
            'user_id': [user_id],
            'name': [message.from_user.first_name or 'N/A'],
            'username': [message.from_user.username or 'N/A'],
            'status': ['opt-in'],
            'date': [datetime.datetime.now().isoformat()]
        })
        if os.path.exists(csv_path):
            df_new.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df_new.to_csv(csv_path, index=False)
        bot.reply_to(message, f"✅ Opt-in #{len(opt_in_users)} подтверждено!\n152-ФЗ OK. Теперь /leads.\n📈 Skoromed SDR")
    else:
        bot.reply_to(message, "✅ Вы уже opt-in!")
@bot.message_handler(commands=['leads'])
def leads(message):
    user_id = str(message.from_user.id)
    if user_id in opt_in_users:
        bot.reply_to(message, "🏪 Лид Москва (OKVED 56):\n\nНазвание: Медкнижка\nАдрес: ул. Ленина 10\nТел: +7(495)123-45-67\n\n💬 WA: 'Здравствуйте! Скидка 25% на медкнижки...'\n\n/more для деталей")
    else:
        bot.reply_to(message, "❌ /optin сначала (152-ФЗ)")
print("🤖 @Skoromed_SDR_Bot запущен (Ctrl+C остановить)...")
bot.polling(none_stop=True)