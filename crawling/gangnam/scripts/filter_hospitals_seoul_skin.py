import pandas as pd
import os

input_file = r'D:\git_gb4pro\crawling\gangnam\data\gangnam_hospitals_final_20260105_065921_update_v1.0.csv'
output_file = input_file.replace('_update_v1.0.csv', '_seoul_skin_filtered.csv')

def filter_data():
    print(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print("Original shape:", df.shape)
    
    # 1. Filter by Sido '서울'
    if 'sido' not in df.columns:
        print("Error: 'sido' column missing.")
        return
        
    sido_mask = df['sido'].astype(str).str.contains('서울', na=False)
    
    # 2. Filter by treatment_tags
    if 'treatment_tags' not in df.columns:
        print("Error: 'treatment_tags' column missing.")
        return
        
    keywords = ['피부', '보톡스', '리프팅', '필러']
    # Create a regex pattern: "피부|보톡스|리프팅|필러"
    pattern = '|'.join(keywords)
    
    tags_mask = df['treatment_tags'].astype(str).str.contains(pattern, na=False)
    
    # Combine masks
    final_mask = sido_mask & tags_mask
    filtered_df = df[final_mask]
    
    print(f"Filtering criteria: sido='서울' AND treatment_tags in {keywords}")
    print("Filtered shape:", filtered_df.shape)
    
    print(f"Saving to {output_file}...")
    filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == '__main__':
    filter_data()
