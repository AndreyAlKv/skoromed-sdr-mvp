import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import pandas as pd
import datetime
load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')
if not VK_TOKEN:
    print("❌ VK_TOKEN не найден в .env!")
    exit(1)
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
opt_in_users = set()
csv_path = 'data/vk_opt_in_leads.csv'
print("🤖 VK Skoromed SDR Bot запущен (Ctrl+C остановить)...")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        text = event.text.lower()
        
        if text == '/start':
            vk.messages.send(user_id=user_id, message="✅ Skoromed SDR VK Bot\n\n/optin — Согласие на рассылку (152-ФЗ OK)\n/leads — Получить шаблоны лидов", random_id=0)
        
        elif text == '/optin':
            user_id_str = str(user_id)
            if user_id_str not in opt_in_users:
                opt_in_users.add(user_id_str)
                os.makedirs('data', exist_ok=True)
                df_new = pd.DataFrame({
                    'user_id': [user_id_str],
                    'name': ['VK User'],
                    'status': ['opt-in'],
                    'date': [datetime.datetime.now().isoformat()]
                })
                if os.path.exists(csv_path):
                    df_new.to_csv(csv_path, mode='a', header=False, index=False)
                else:
                    df_new.to_csv(csv_path, index=False)
                vk.messages.send(user_id=user_id, message=f"✅ Opt-in #{len(opt_in_users)} подтверждено! 152-ФЗ OK.\nТеперь /leads для лидов.", random_id=0)
            else:
                vk.messages.send(user_id=user_id, message="✅ Вы уже opt-in!", random_id=0)
        
        elif text == '/leads':
            if str(user_id) in opt_in_users:
                vk.messages.send(user_id=user_id, message="🏪 Лид Москва (OKVED 56):\n\nНазвание: Медкнижка\nАдрес: ул. Ленина 10\nТел: +7(495)123-45-67\n\n💬 WA шаблон: 'Здравствуйте! Скидка 25% на SDR услуги...'\n\nБольше: /more", random_id=0)
            else:
                vk.messages.send(user_id=user_id, message="❌ Сначала /optin (152-ФЗ)", random_id=0)