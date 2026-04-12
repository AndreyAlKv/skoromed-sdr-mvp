# mailer.py - SDR MVP: Send emails to enriched leads
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
SMTP_CONFIG = {
    "host": "smtp.gmail.com",  # или smtp.yandex.ru:587
    "port": 587,
    "user": "your@gmail.com",  # ЗАМЕНИ на свой email
    "pass": "your_app_pass"    # App password (Gmail: настройки > безопасность)
}
def send_email(to_email, subject, body, from_email="info@skoromed.ai"):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port'])
        server.starttls()
        server.login(SMTP_CONFIG['user'], SMTP_CONFIG['pass'])
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ SENT to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Send error: {e}")
        return False
if __name__ == "__main__":
    with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
        enriched = json.load(f)
    
    leads = [c for c in enriched if c.get('emails')]
    print(f"Loaded {len(leads)} leads")
    
    REAL_SEND = False  # True для реальной отправки
    
    for lead in leads:
        email = lead['emails'][0]
        subject = "AI SDR для лидов медкнижек Москва +30%"
        body = f"""Добрый день!
Вижу, вы предлагаете медкнижки срочно ({lead['name']}, {lead['url']}).
Skoromed AI SDR автоматизирует:
- Scrape лидов Yandex
- Enrich emails/phones
- Массовые emails + звонки
+30% клиентов. Демо?
+7(999)123-45-67 | info@skoromed.ai
С уважением,
Команда Skoromed"""
        
        print(f"\n📧 TO: {email} ({lead['name'][:40]})")
        print(f"Subject: {subject}")
        print(f"Body preview:\n{body}\n")
        
        if REAL_SEND:
            send_email(email, subject, body)
        else:
            print("--- SIMULATE SEND (set REAL_SEND=True) ---\n")
    
    print("🚀 Mailer ready!")