import sqlite3
import pandas as pd
import os
conn = sqlite3.connect('db/skoromed_v2.db')
# Schema (columns)
print("DB schema b2b_leads:")
schema = pd.read_sql("PRAGMA table_info(b2b_leads);", conn)
print(schema[['name', 'type']])
print("\nB2B leads ALL columns (LIMIT 5):")
b2b_df = pd.read_sql("SELECT * FROM b2b_leads LIMIT 5;", conn)
print(b2b_df.to_string(index=False))
try:
    b2b_count = pd.read_sql("SELECT COUNT(*) cnt FROM b2b_leads", conn)['cnt'].iloc[0]
    print("B2B COUNT:", int(b2b_count))
except:
    print("B2B COUNT: 0")
try:
    b2c_count = pd.read_sql("SELECT COUNT(*) cnt FROM b2c_leads", conn)['cnt'].iloc[0]
    print("B2C COUNT:", int(b2c_count))
except:
    print("B2C COUNT: 0")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:", list(tables['name']))
db_size = os.path.getsize('db/skoromed_v2.db')
print("DB size:", round(db_size / 1024, 1), "KB")
conn.close()
print("DB query OK!")