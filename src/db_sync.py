import sqlite3
import pandas as pd
import logging
import os
import glob
# Безопасный logging без PermissionError
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', handlers=[logging.FileHandler('logs/full_cycle.log', mode='a', encoding=None), logging.StreamHandler()])
DB_PATH = 'data/sdr.db'
def sync_csv_to_db(csv_pattern='data/*.csv'):
    conn = sqlite3.connect(DB_PATH)
    
    create_table = """
    CREATE TABLE IF NOT EXISTS b2b_leads (
        inn TEXT PRIMARY KEY, name TEXT, okved TEXT, region INTEGER, moscow INTEGER,
        fio TEXT, phones TEXT, emails TEXT, status TEXT, timestamp TEXT
    )
    """
    conn.execute(create_table)
    conn.commit()
    
    try:
        existing_inns = pd.read_sql("SELECT inn FROM b2b_leads WHERE inn NOT LIKE 'test%'", conn)['inn'].astype(str).tolist()
        print(f"Existing non-test INN: {len(existing_inns)}")
    except:
        existing_inns = []
    
    csv_files = glob.glob(csv_pattern)
    print(f"CSV files found: {len(csv_files)}")
    total_new = 0
    os.makedirs('data/archives', exist_ok=True)
    
    for csv_file in csv_files:
        try:
            # Безопасный parse on_bad_lines='skip'
            df = pd.read_csv(csv_file, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
            print(f"CSV {os.path.basename(csv_file)}: rows={len(df)}, columns={list(df.columns)}")
            if 'inn' not in df.columns:
                print(f"Skip {csv_file}: no 'inn'")
                continue
            df['inn'] = df['inn'].astype(str).str.strip()
            df['region'] = pd.to_numeric(df.get('region', 77), errors='coerce').fillna(77)
            df['okved'] = df['okved'].astype(str).str.strip()
            # Маска: unique non-test + Москва + OKVED retail/beauty/food/fitness
            okved_mask = df['okved'].str.contains(r'47|56|96|93|47\.75', na=False, regex=True, case=False)
            unique_mask = ~df['inn'].isin(existing_inns)
            moscow_mask = df['region'] == 77
            mask = unique_mask & moscow_mask & okved_mask
            print(f"Mask counts: unique={unique_mask.sum()}, moscow={moscow_mask.sum()}, okved={okved_mask.sum()}, total={mask.sum()}")
            df_filtered = df[mask].copy()
            if not df_filtered.empty:
                df_filtered.to_sql('b2b_leads', conn, if_exists='append', index=False)
                new_count = len(df_filtered)
                total_new += new_count
                print(f"Added {new_count} from {os.path.basename(csv_file)}")
            os.rename(csv_file, f"data/archives/{os.path.basename(csv_file)}")
            print(f"Moved: {os.path.basename(csv_file)}")
        except Exception as e:
            print(f"Error {csv_file}: {str(e)[:100]}")
    
    final_count = pd.read_sql("SELECT COUNT(*) FROM b2b_leads", conn).iloc[0,0]
    conn.close()
    print(f"DB Sync END: +{total_new} new → TOTAL {final_count}")
    logging.info(f"Sync END: +{total_new}, total {final_count}")
if __name__ == '__main__':
    sync_csv_to_db()