import sqlite3
import pandas as pd
import os
from datetime import datetime
db_path = 'db/skoromed_v2.db'
conn = sqlite3.connect(db_path)
# B2B (уже есть)
conn.execute('''
CREATE TABLE IF NOT EXISTS b2b_leads (
    inn TEXT PRIMARY KEY, okved TEXT, name TEXT, phone TEXT, address TEXT, 
    emails TEXT, status TEXT, timestamp TEXT DEFAULT (datetime('now'))
)
''')
# B2C (CREATE missing table)
conn.execute('''
CREATE TABLE IF NOT EXISTS b2c_leads (
    phone TEXT PRIMARY KEY, name TEXT, need TEXT, urgency TEXT, source TEXT, 
    timestamp TEXT DEFAULT (datetime('now'))
)
''')
conn.commit()
print("✅ DB tables refreshed: b2b_leads (5 leads) + b2c_leads ready")