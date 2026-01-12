import pandas as pd
import os
import sys

input_file = r'D:\git_gb4pro\crawling\gangnam\data\gangnam_hospitals_final_20260105_065921.csv'
output_file = input_file.replace('.csv', '_update_v1.0.csv')

def process():
    print(f"Reading {input_file}...")
    # Try reading with utf-8 first, then cp949 if it fails
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 failed, trying CP949...")
        try:
            df = pd.read_csv(input_file, encoding='cp949')
        except Exception as e:
            print(f"Failed to read file: {e}")
            return

    print("Columns:", df.columns)
    if 'address' not in df.columns:
        print("Error: 'address' column not found.")
        return

    print("Processing addresses...")
    
    def extract_sido(addr):
        if pd.isna(addr): return ""
        parts = str(addr).split()
        if len(parts) > 0:
            return parts[0]
        return ""

    def extract_sigungu(addr):
        if pd.isna(addr): return ""
        parts = str(addr).split()
        if len(parts) > 1:
            return parts[1]
        return ""

    df['sido'] = df['address'].apply(extract_sido)
    df['sigungu'] = df['address'].apply(extract_sigungu)
    
    # Check the result
    print("Sample result:")
    print(df[['address', 'sido', 'sigungu']].head())

    print(f"Saving to {output_file}...")
    df.to_csv(output_file, index=False, encoding='utf-8-sig') 
    print("Done.")

if __name__ == '__main__':
    process()
