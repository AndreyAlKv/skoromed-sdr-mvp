import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import pandas as pd
import time
import ast
sys.stdout.reconfigure(encoding='utf-8')
GMAIL_USER = "gfdnk1971@gmail.com"  # Твой Gmail!
GMAIL_PASS = "jssmipdwevomxxty"  # Новый PASS вставлен!
print(f"GMAIL_USER: {GMAIL_USER}")
print(f"GMAIL_PASS len: {len(GMAIL_PASS)} chars")
# Test login
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.quit()
    print("✅ Gmail LOGIN OK!")
except Exception as e:
    print(f"❌ LOGIN ERROR: {e}")
    exit()
def send_email(to_email, name, phone):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = "Dogovor medknizhka SDR v2.0"
    body = f"Здравствуйте, {name}! SKOROMED medosmotry. Tel: +7(495)123-45-67 /optin {phone}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Send error {to_email}: {str(e)[:80]}")
        return False
conn = sqlite3.connect('db/skoromed_v2.db')
df = pd.read_sql("SELECT fio as name, phones, emails FROM b2b_leads WHERE emails != '[]' LIMIT 3;", conn)
conn.close()
print(f"Loading {len(df)} leads...")
sent = 0
for _, row in df.iterrows():
    try:
        phones = ast.literal_eval(row['phones'])[0] if row['phones'] else 'no_phone'
        emails = ast.literal_eval(row['emails'])[0] if row['emails'] else None
        if emails:
            if send_email(emails, row['name'], phones):
                sent += 1
    except:
        pass
    time.sleep(3)
print(f"Mailer ROI: Sent {sent}/{len(df)} OK")