import pandas as pd
import os

file_path = r'crawling/gangnam/data/gangnam_hospitals_final_20260105_065921.csv'

try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except Exception as e:
        print(f"Error reading file: {e}")
        exit()

print("Columns:")
print(df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))
print("\nInfo:")
print(df.info())
