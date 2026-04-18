# src/test_smtp_login.py - ТЕСТ ЛОГИНА GMAIL (без писем)
import smtplib
GMAIL_USER = "gfdnk1971@gmail.com"  # ИЗ mailer.py
GMAIL_PASS = "uetf rgeg qedv khlq"  # ИЗ mailer.py
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    print("✅ SMTP ЛОГИН OK! Готово к mailer.py")
    server.quit()
except Exception as e:
    print(f"❌ SMTP ОШИБКА: {e}. Фикс GMAIL_USER/PASS!")