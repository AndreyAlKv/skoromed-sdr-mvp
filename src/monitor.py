import sqlite3
import pandas as pd
DB_PATH = 'data/sdr.db'
conn = sqlite3.connect(DB_PATH)
count = pd.read_sql("SELECT COUNT(*) FROM b2b_leads WHERE inn NOT LIKE 'test%'", conn).iloc[0,0]
print(f"DB non-test COUNT: {count}")
new = pd.read_sql("SELECT * FROM b2b_leads WHERE inn NOT LIKE 'test%' LIMIT 5", conn)
print(new)
conn.close()
print("Monitor OK")