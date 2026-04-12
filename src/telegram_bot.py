# telegram_bot.py - TG notifications for SDR leads
import json
import requests
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # @BotFather /newbot → token
CHAT_ID = "YOUR_CHAT_ID_HERE"      # Получи: https://api.telegram.org/bot<TOKEN>/getUpdates
def send_tg(msg):
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ Set BOT_TOKEN + CHAT_ID first")
        print(msg)
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    print("✅ TG notification sent!")
if __name__ == "__main__":
    with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
        enriched = json.load(f)
    
    leads = [c for c in enriched if c.get('emails')]
    msg = f"🚀 SDR BOT: {len(leads)} новых лидов с emails!\n\n"
    for lead in leads:
        msg += f"📧 {lead['emails'][0]}\n🏢 {lead['name'][:40]}\n📞 {lead['phones']}\n🔗 {lead['url']}\n\n"
    
    send_tg(msg)
    print("Preview TG message:\n" + msg)