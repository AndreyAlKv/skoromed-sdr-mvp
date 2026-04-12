# sheets_sync.py - авто-синк SDR лидов в Google Sheets
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
SHEET_ID = "1BCZ66Dg3qiXmv_THlHJBN8b_7aagGRIZEFDn_JbQKHs"  # Твоя таблица!
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Скачай ниже
def sync_leads():
    with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    leads = [c for c in all_data if c.get('emails')]  # Только лиды с emails!
    
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    
    # Очистка + заголовки
    sheet.clear()
    sheet.append_row(['Дата синка', 'Name', 'URL', 'Emails', 'Phones', 'Статус'])
    
    for lead in leads:
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M'),
            lead.get('name', ''),
            lead.get('url', ''),
            '; '.join(lead.get('emails', [])),
            '; '.join(lead.get('phones', [])),
            'Новый лид'
        ]
        sheet.append_row(row)
    
    print(f"✅ Synced {len(leads)} лидов в Google Sheets! Ссылка: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    print("Примеры:")
    for lead in leads[:3]:
        print(f"📧 {lead.get('emails', [None])[0]} | {lead.get('name', '')}")
if __name__ == "__main__":
    sync_leads()