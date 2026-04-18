import sqlite3
import os
db_path = 'db/skoromed_v2.db'
conn = sqlite3.connect(db_path)
conn.execute('''
CREATE TABLE IF NOT EXISTS b2b_leads (
    inn TEXT PRIMARY KEY, okved TEXT, name TEXT, phone TEXT, address TEXT, emails TEXT, status TEXT, timestamp TEXT DEFAULT (datetime('now'))
)
''')
conn.execute('''
CREATE TABLE IF NOT EXISTS b2c_leads (
    phone TEXT PRIMARY KEY, name TEXT, need TEXT, urgency TEXT, source TEXT, timestamp TEXT DEFAULT (datetime('now'))
)
''')
conn.commit()
print("DB tables created OK: b2b_leads + b2c_leads")
print("File size:", os.path.getsize(db_path), "bytes")