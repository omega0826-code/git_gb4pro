import pandas as pd
import os

file_path = r'crawling/gangnam/data/gangnam_hospitals_final_20260105_065921.csv'

try:
    df = pd.read_csv(file_path, encoding='cp949')
    print("Read with cp949 successfully.")
    print("Columns:")
    print(df.columns.tolist())
    print("\nFirst 3 rows:")
    print(df.head(3))
except Exception as e:
    print(f"Error reading with cp949: {e}")
