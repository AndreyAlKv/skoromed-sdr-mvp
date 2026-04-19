import sqlite3
import pandas as pd
import os
import json
import re

DB_PATH = ‘data/sdr.db’
EXPORT_CSV = ‘data/results_export.csv’
SUMMARY_TXT = ‘data/results_summary.txt’

if not os.path.exists(DB_PATH):
print(“No DB - exit”)
exit()

conn = sqlite3.connect(DB_PATH)

df_non_test = pd.read_sql(“””
SELECT inn, name, okved, region, moscow, fio, phones, emails, status, timestamp
FROM b