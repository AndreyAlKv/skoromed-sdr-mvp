# src/test_smtp.py - SMTP LOGIN TEST (534 FIX)
import smtplib
GMAIL_USER = "gfdnk1971@gmail.com"
GMAIL_PASS = "diwg wjwv ffvg oawv"  # НОВЫЙ App Password!
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
try:
    server.login(GMAIL_USER, GMAIL_PASS)
    print("✅ SMTP LOGIN OK! App Password работает!")
except Exception as e:
    print(f"❌ Ошибка: {e}")
server.quit()






diwg wjwv ffvg oawv