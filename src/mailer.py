# src/mailer.py - SMTP LOGIN ASCII FIX (Python 3.14)
import smtplib
import json
from email.message import EmailMessage
GMAIL_USER = "gfdnk1971@gmail.com"  # ASCII Gmail! ЗАМЕНИ НА СВОЙ (без кириллицы)
GMAIL_PASS = "diwg wjwv ffvg oawv"  # App Password ASCII OK
leads = json.load(open('src/data/all_leads.json', 'r', encoding='utf-8'))
print("Mailer: Загружено лидов из CSV - OK")
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(GMAIL_USER, GMAIL_PASS)  # str ASCII OK
sent = 0
for lead in leads[:24]:
    name = lead.get('name', 'клиника')
    email = lead.get('email') or f"info@{name.lower().replace(' ', '').replace('/', '').replace('.', '').replace('-', '')}.ru"
    
    msg = EmailMessage()
    msg['Subject'] = f"Медосмотры для {name}: скидка 25%!"
    msg['From'] = GMAIL_USER
    msg['To'] = email
    msg.set_content(f"Привет, {name}! Скидка 25% медосмотры. +7(495)212-12-12 https://2121212.ru/akcii")
    
    try:
        server.send_message(msg)
        print(f"✅ {name} → {email}")
        sent += 1
    except Exception as e:
        print(f"❌ {e}")
server.quit()
print(f"🚀 {sent}/24 отправлено! Gmail 'Отправленные'.")