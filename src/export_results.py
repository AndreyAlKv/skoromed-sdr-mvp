import sqlite3
import pandas as pd
import os
DB_PATH = 'data/sdr.db'
EXPORT_CSV = 'data/results_export.csv'
SUMMARY_TXT = 'data/results_summary.txt'
if not os.path.exists(DB_PATH):
    print("No DB - exit")
    exit()
conn = sqlite3.connect(DB_PATH)
# Export non-test leads (165 rows: inn/name/okved/region/phones/emails)
df_non_test = pd.read_sql("""
    SELECT inn, name, okved, region, moscow, fio, phones, emails, status, timestamp 
    FROM b2b_leads WHERE inn NOT LIKE 'test%'
    ORDER BY inn
""", conn)
df_non_test.to_csv(EXPORT_CSV, index=False, encoding='utf-8')
print(f"Exported {len(df_non_test)} non-test leads to {EXPORT_CSV}")
# Summary stats
total = pd.read_sql("SELECT COUNT(*) FROM b2b_leads", conn).iloc[0,0]
non_test = len(df_non_test)
top_okved = df_non_test['okved'].value_counts().head()
top_region = df_non_test['region'].value_counts().head()
summary = f"""
SDR RESULTS SUMMARY v2.2.7 (DB: data/sdr.db size {os.path.getsize(DB_PATH)/1024:.1f} KB)
================================================================================
TOTAL leads: {total}
Non-test qualified: {non_test} (OKVED 47/56/96/93 Москва)
Top OKVED:
{top_okved.to_string()}
Top region:
{top_region.to_string()}
Preview first 5:
{df_non_test.head().to_string(index=False)}
CSV export: {EXPORT_CSV} ({len(df_non_test)} rows)
Archives: data/archives/*.csv
JSON enrich: data/enriched_companies.json
Logs: logs/full_cycle.log
Daily: python src/db_query.py + python src/export_results.py
Cron: 19.04.2026 9:00 auto
================================================================================
"""
with open(SUMMARY_TXT, 'w', encoding='utf-8') as f:
    f.write(summary)
print(f"Summary saved: {SUMMARY_TXT}")
conn.close()
print("Export OK! Open data/results_export.csv in Excel.")