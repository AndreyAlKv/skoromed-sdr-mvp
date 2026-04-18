# ... b2b print
print("\nB2B COUNT:", pd.read_sql("SELECT COUNT(*) cnt FROM b2b_leads", conn)['cnt'].iloc[0])
print("B2C COUNT:", pd.read_sql("SELECT COUNT(*) cnt FROM b2c_leads", conn)['cnt'].iloc[0])