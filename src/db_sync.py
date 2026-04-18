import glob
import pandas as pd
import sqlite3
from datetime import datetime
conn = sqlite3.connect('db/skoromed_v2.db')
csv_files = glob.glob('data/fns_*.csv') + glob.glob('fns_*.csv') + glob.glob('*leads.csv')
synced = 0
for csv in csv_files:
    try:
        df = pd.read_csv(csv)
        df['timestamp'] = datetime.now().isoformat()
        df.to_sql('b2b_leads', conn, if_exists='append', index=False)
        synced += len(df)
        print(f"Synced {csv}: {len(df)} leads → DB")
    except Exception as e:
        print(f"Skip {csv}: {e}")
count = pd.read_sql("SELECT COUNT(*) cnt FROM b2b_leads", conn)['cnt'].iloc[0]
print(f"✅ TOTAL B2B leads in DB: {count}")
conn.commit()
conn.close()