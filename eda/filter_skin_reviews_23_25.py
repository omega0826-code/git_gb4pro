import pandas as pd
import glob
import os
from datetime import datetime

# 설정
hospital_file = r'd:\git_gb4pro\crawling\gangnam\data\gangnam_hospitals_skin_filter_20260109_231706.csv'
reviews_dir = r'd:\git_gb4pro\crawling\gangnam\data\reviews_year'
target_years = ['2023', '2024', '2025']
output_file = f'd:\\git_gb4pro\\crawling\\gangnam\\data\\gangnam_skin_reviews_2023_2025_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

try:
    print("작업을 시작합니다...")
    
    # 1. 병원 ID 목록 로드
    print(f"병원 목록 로드 중: {hospital_file}")
    try:
        host_df = pd.read_csv(hospital_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        host_df = pd.read_csv(hospital_file, encoding='cp949')
    
    # ID를 문자열로 변환하여 set으로 저장 (검색 속도 향상)
    target_hospital_ids = set(host_df['id'].astype(str))
    print(f"대상 병원 수: {len(target_hospital_ids)}")

    # 2. 리뷰 파일 찾기 및 필터링
    all_filtered_reviews = []
    
    for year in target_years:
        # 해당 연도가 포함된 파일 찾기
        pattern = os.path.join(reviews_dir, f"*_{year}_*.csv")
        files = glob.glob(pattern)
        
        for file_path in files:
            print(f"처리 중: {os.path.basename(file_path)}...")
            try:
                try:
                    review_df = pd.read_csv(file_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    review_df = pd.read_csv(file_path, encoding='cp949')
                
                # hospital_id를 문자열로 변환하여 필터링
                # hospital_id 컬럼이 있는지 확인
                if 'hospital_id' in review_df.columns:
                    review_df['hospital_id'] = review_df['hospital_id'].astype(str)
                    filtered = review_df[review_df['hospital_id'].isin(target_hospital_ids)]
                    
                    if not filtered.empty:
                        all_filtered_reviews.append(filtered)
                        print(f"  -> {len(filtered)} 건 추출됨")
                    else:
                        print("  -> 해당 병원 리뷰 없음")
                else:
                    print("  -> 'hospital_id' 컬럼이 없어 건너뜀")
                    
            except Exception as e:
                print(f"  -> 파일 읽기 오류: {e}")

    # 3. 통합 및 저장
    if all_filtered_reviews:
        final_df = pd.concat(all_filtered_reviews, ignore_index=True)
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n작업 완료!")
        print(f"총 추출된 리뷰 수: {len(final_df)}")
        print(f"저장된 파일: {output_file}")
    else:
        print("\n추출된 리뷰가 없습니다.")

except Exception as e:
    print(f"에러 발생: {e}")
