import pandas as pd
import os
from datetime import datetime

# Input paths
hospital_file = r'D:\git_gb4pro\crawling\gangnam\data\gangnam_hospitals_final_20260105_065921_seoul_skin_filtered.csv'
review_files = [
    r'D:\git_gb4pro\crawling\gangnam\data\reviews_year\gangnam_reviews_2023_20260109_232353.csv',
    r'D:\git_gb4pro\crawling\gangnam\data\reviews_year\gangnam_reviews_2024_20260109_232353.csv',
    r'D:\git_gb4pro\crawling\gangnam\data\reviews_year\gangnam_reviews_2025_20260109_232353.csv'
]

# Output paths
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_data_file = f'D:\\git_gb4pro\\crawling\\gangnam\\data\\seoul_skin_reviews_2023_2025_{timestamp}.csv'
output_report_file = f'D:\\git_gb4pro\\crawling\\gangnam\\data\\report_review_extraction_23_25_{timestamp}.md'

def process():
    print("Loading filtered hospital list...")
    try:
        hospitals = pd.read_csv(hospital_file, encoding='utf-8-sig')
    except Exception as e:
        print(f"Error reading hospital file: {e}")
        return
        
    if 'id' not in hospitals.columns:
        print("Error: 'id' column missing in hospital file")
        return

    valid_ids = set(hospitals['id'].unique())
    print(f"Number of valid hospital IDs: {len(valid_ids)}")

    all_filtered_reviews = []
    summary = []

    for f in review_files:
        if not os.path.exists(f):
            print(f"Warning: File not found {f}")
            continue
            
        print(f"Processing {os.path.basename(f)}...")
        try:
            # Low_memory=False to handle mixed types if any, though usually cleaner to specify dtypes
            rdf = pd.read_csv(f, encoding='utf-8-sig', low_memory=False)
            
            # Check hospital_id column
            h_col = 'hospital_id' if 'hospital_id' in rdf.columns else 'id'
            
            original_count = len(rdf)
            filtered_rdf = rdf[rdf[h_col].isin(valid_ids)]
            filtered_count = len(filtered_rdf)
            
            all_filtered_reviews.append(filtered_rdf)
            
            summary.append({
                'file': os.path.basename(f),
                'original': original_count,
                'filtered': filtered_count
            })
            print(f"  {original_count} -> {filtered_count}")
            
        except Exception as e:
            print(f"Error processing {f}: {e}")

    if all_filtered_reviews:
        final_df = pd.concat(all_filtered_reviews, ignore_index=True)
        print(f"Total reviews extracted: {len(final_df)}")
        
        print(f"Saving combined reviews to {output_data_file}...")
        final_df.to_csv(output_data_file, index=False, encoding='utf-8-sig')
        
        # Generate Report
        print(f"Generating report to {output_report_file}...")
        report_content = f"""# 리뷰 데이터 추출 결과 리포트 (2023~2025)

**1. 작업 개요**
*   **작업 일시:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
*   **목적:** 필터링된 서울 지역 피부/미용 병원(645개소)에 해당하는 2023~2025년 리뷰 데이터 추출

**2. 기준 정보**
*   **병원 마스터:** `gangnam_hospitals_final_20260105_065921_seoul_skin_filtered.csv`
*   **대상 리뷰 연도:** 2023, 2024, 2025

**3. 추출 통계**

| 소스 파일 | 전체 리뷰 수 | 추출 리뷰 수 | 비고 |
| :--- | :---: | :---: | :--- |
"""
        for s in summary:
            report_content += f"| {s['file']} | {s['original']:,} | {s['filtered']:,} | | \n"
            
        report_content += f"""
**4. 최종 결과**
*   **총 추출 리뷰 수:** {len(final_df):,} 건
*   **저장 데이터 파일:** `{os.path.basename(output_data_file)}`
*   **저장 경로:** `D:\\git_gb4pro\\crawling\\gangnam\\data\\`
"""
        with open(output_report_file, 'w', encoding='utf-8') as f_out:
            f_out.write(report_content)
            
        print("Done.")
    else:
        print("No data extracted.")

if __name__ == '__main__':
    process()
