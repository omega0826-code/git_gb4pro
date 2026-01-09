import pandas as pd
import os
from datetime import datetime

# 설정
input_file = r'd:\git_gb4pro\crawling\gangnam\data\gangnam_reviews_FINAL_ALL.csv'
output_dir = r'd:\git_gb4pro\crawling\gangnam\data\reviews_year'
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

def parse_date(date_str):
    try:
        # "2024년 1월 1일" 등의 한글 날짜 형식 처리
        date_str = str(date_str).replace('년', '-').replace('월', '-').replace('일', '').replace(' ', '')
        # "2024.1.1" 등의 점 구분자 처리
        date_str = date_str.replace('.', '-')
        # 마지막이 -로 끝나는 경우 제거 (예: 2024-01-01-)
        if date_str.endswith('-'):
            date_str = date_str[:-1]
        
        return pd.to_datetime(date_str)
    except:
        return pd.NaT

try:
    # 1. 데이터 로드
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        print("utf-8-sig failed, trying cp949...")
        df = pd.read_csv(input_file, encoding='cp949')

    print(f"Total records loaded: {len(df)}")

    # 2. 날짜 처리
    print("Processing dates...")
    # 날짜 파싱 적용
    df['parsed_date'] = df['date'].apply(parse_date)
    
    # 날짜 파싱 실패 데이터 확인
    failed_dates = df[df['parsed_date'].isna()]
    if not failed_dates.empty:
        print(f"Warning: {len(failed_dates)} rows could not be parsed for date. Examples:")
        print(failed_dates['date'].head())
    
    # 연도 추출
    df['year'] = df['parsed_date'].dt.year

    # 3. 연도별 저장
    # 유효한 연도가 있는 데이터만 처리
    valid_years_df = df.dropna(subset=['year'])
    years = valid_years_df['year'].unique()
    
    # 정수형으로 변환 (파일명 깔끔하게)
    years = sorted(years.astype(int))
    
    print(f"Found years: {years}")

    for year in years:
        year_df = valid_years_df[valid_years_df['year'] == year].copy()
        
        # 임시 컬럼 제거 후 저장
        save_df = year_df.drop(columns=['parsed_date', 'year'])
        
        file_name = f'gangnam_reviews_{year}_{current_time}.csv'
        file_path = os.path.join(output_dir, file_name)
        
        save_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"Saved {year}: {len(save_df)} rows to {file_path}")

    print("All done.")

except Exception as e:
    print(f"An error occurred: {e}")
