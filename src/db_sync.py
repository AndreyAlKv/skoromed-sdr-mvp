import sqlite3
import pandas as pd
import logging
import os
import glob
logging.basicConfig(filename='logs/full_cycle.log', level=logging.INFO, format='[%(asctime)s] %(message)s', encoding='utf-8')
DB_PATH = 'data/sdr.db'
def sync_csv_to_db(csv_pattern='data/*.csv'):
    conn = sqlite3.connect(DB_PATH)
    
    # CREATE table IF NOT EXISTS
    create_table = """
    CREATE TABLE IF NOT EXISTS b2b_leads (
        inn TEXT PRIMARY KEY,
        name TEXT,
        okved TEXT,
        region INTEGER,
        moscow INTEGER,
        fio TEXT,
        phones TEXT,
        emails TEXT,
        status TEXT,
        timestamp TEXT
    )
    """
    conn.execute(create_table)
    conn.commit()
    
    # Safe existing_inns (empty table OK)
    try:
        existing_inns = pd.read_sql("SELECT inn FROM b2b_leads WHERE inn NOT LIKE 'test%'", conn)['inn'].astype(str).tolist()
    except:
        existing_inns = []
    
    csv_files = glob.glob(csv_pattern)
    total_new = 0
    os.makedirs('data/archives', exist_ok=True)
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            if 'inn' not in df.columns:
                logging.info(f"Skip {csv_file}: no inn")
                continue
            df['inn'] = df['inn'].astype(str)
            df['region'] = pd.to_numeric(df.get('region', 77), errors='coerce').fillna(77)
            mask = (~df['inn'].isin(existing_inns)) & (df['region'] == 77)
            df_filtered = df[mask]
            if not df_filtered.empty:
                df_filtered.to_sql('b2b_leads', conn, if_exists='append', index=False)
                new_count = len(df_filtered)
                total_new += new_count
                logging.info(f"Added {new_count} unique Moscow from {csv_file}")
            os.rename(csv_file, f"data/archives/{os.path.basename(csv_file)}")
        except Exception as e:
            logging.error(f"Error {csv_file}: {e}")
    
    final_count = pd.read_sql("SELECT COUNT(*) FROM b2b_leads", conn).iloc[0,0]
    conn.close()
    print(f"DB Sync: +{total_new} new → TOTAL {final_count}")
    logging.info(f"Sync END: +{total_new}, total {final_count}")
if __name__ == '__main__':
    sync_csv_to_db()