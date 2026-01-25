import pandas as pd
import os
import time

def main():
    # 경로 설정
    input_path = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260116_212603_geocoded_20260125_164059.csv'
    output_dir = r'd:\git_gb4pro\gis\geocoding\hospital\data\output'
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = f'강남구_피부과_데이터_{timestamp}.csv'
    output_path = os.path.join(output_dir, output_filename)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Reading file: {input_path}")
    # 인코딩 처리 (utf-8-sig 선호, 안되면 cp949)
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception:
        df = pd.read_csv(input_path, encoding='cp949')

    print(f"Total rows: {len(df)}")

    # 강남구 & 피부과 필터링
    # eqp_sgguCdNm == '강남구'
    # dgsbjt_dgsbjtCdNm == '피부과'
    
    filtered_df = df[
        (df['eqp_sgguCdNm'] == '강남구') & 
        (df['dgsbjt_dgsbjtCdNm'] == '피부과')
    ]

    print(f"Filtered rows: {len(filtered_df)}")

    if len(filtered_df) > 0:
        filtered_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Extracted data saved to: {output_path}")
    else:
        print("No data matched the filters.")

if __name__ == "__main__":
    main()
