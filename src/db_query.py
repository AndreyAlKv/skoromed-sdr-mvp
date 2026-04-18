import sqlite3
import pandas as pd
import os
DB_PATH = 'data/sdr.db'
if not os.path.exists(DB_PATH):
    print("No DB file - create empty")
    exit()
conn = sqlite3.connect(DB_PATH)
print("DB schema b2b_leads:")
schema = pd.read_sql("PRAGMA table_info(b2b_leads)", conn)
print(schema)
print("\nB2B leads ALL columns (LIMIT 5):")
all_preview = pd.read_sql("SELECT * FROM b2b_leads LIMIT 5", conn)
print(all_preview)
all_count = pd.read_sql("SELECT COUNT(*) FROM b2b_leads", conn).iloc[0,0]
print(f"B2B COUNT all: {all_count}")
non_test_count = pd.read_sql("SELECT COUNT(*) FROM b2b_leads WHERE inn NOT LIKE 'test%'", conn).iloc[0,0]
print(f"B2B non-test COUNT: {non_test_count}")
print("\nNon-test preview (LIMIT 5):")
non_test_preview = pd.read_sql("SELECT * FROM b2b_leads WHERE inn NOT LIKE 'test%' LIMIT 5", conn)
print(non_test_preview)
try:
    b2c_count = pd.read_sql("SELECT COUNT(*) FROM b2c_leads", conn).iloc[0,0]
except:
    b2c_count = 0
print(f"B2C COUNT: {b2c_count}")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()
print(f"Tables: {tables}")
db_size = os.path.getsize(DB_PATH) / 1024
print(f"DB size: {db_size:.1f} KB")
conn.close()
print("DB query OK!")