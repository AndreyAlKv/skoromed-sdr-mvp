# telegram_bot.py - TG уведомления о лидах SDR (timeout fix)
import json
import requests
import time
BOT_TOKEN = "8762948842:AAEt3G9nYganhs_iTYUAWFRaTvdSX-k4RII"
CHAT_ID = "1435979528"
def send_tg(msg, retries=3):
    if "YOUR" in BOT_TOKEN:
        print("⚠️ SETUP ERROR: BOT_TOKEN/CHAT_ID")
        print(msg[:200])
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for attempt in range(retries):
        try:
            resp = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=30)
            if resp.status_code == 200:
                print("✅ TG отправлено!")
                return
            else:
                print(f"❌ TG error {resp.status_code}: {resp.text}")
        except requests.exceptions.ConnectTimeout:
            print(f"⏳ TG timeout, retry {attempt+1}/{retries}")
            time.sleep(5)
        except Exception as e:
            print(f"❌ TG error: {e}")
    print("❌ TG failed after retries. Check VPN/firewall/internet.")
if __name__ == "__main__":
    try:
        with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
            enriched = json.load(f)
        leads = [c for c in enriched if c.get('emails')]
        msg = f"🚀 SDR BOT: {len(leads)} лидов с emails!\n\n"
        for lead in leads:
            msg += f"📧 {lead['emails'][0]}\n🏢 {lead['name'][:40]}...\n📞 {lead['phones']}\n🔗 {lead['url']}\n\n"
        send_tg(msg)
        print("Preview:", msg[:300])
    except FileNotFoundError:
        print("❌ Нет enriched_companies.json. Запусти python src/enrich.py сначала.")