import pandas as pd
import os

# Input file from the previous step
input_file = r'D:\git_gb4pro\crawling\gangnam\data\gangnam_hospitals_final_20260105_065921_update_v1.0.csv'
# Output file
output_file = input_file.replace('_update_v1.0.csv', '_seoul_only.csv')

def extract():
    print(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print("Original shape:", df.shape)
    
    if 'sido' not in df.columns:
        print("Error: 'sido' column not found.")
        return

    # Filter for '서울'
    print("Filtering for sido == '서울'...")
    # There might be variations like '서울특별시', '서울', etc. or whitespace.
    # Let's check unique values first to be sure, but strict filtering as per instruction '서울'
    # The previous script extracted the first word of the address.
    # Usually addresses start with "서울" or "서울특별시".
    
    # Let's inspect unique 'sido' values first
    print("Unique sido values:", df['sido'].unique())
    
    # Filter containing '서울' to be safe, or exact match if the data is clean.
    # The previous script split by space and took index 0.
    # If address was "서울 강남구...", sido is "서울".
    # If address was "서울특별시 강남구...", sido is "서울특별시".
    
    # We will look for '서울' in the string to be inclusive (e.g. 서울, 서울특별시)
    # OR strictly follow the instruction "sido가 '서울'인".
    # Let's try exact match first, if count is low, we might need to adjust.
    
    seoul_df = df[df['sido'].astype(str).str.contains('서울')]
    
    print("Filtered shape:", seoul_df.shape)
    
    print(f"Saving to {output_file}...")
    seoul_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == '__main__':
    extract()
