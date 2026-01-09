import pandas as pd
from datetime import datetime

# 파일 경로 설정
input_file = r'd:\git_gb4pro\crawling\gangnam\data\gangnam_hospitals_final_20260105_065921.csv'
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'd:\\git_gb4pro\\crawling\\gangnam\\data\\gangnam_hospitals_skin_filter_{current_time}.csv'

try:
    # CSV 로드 (encoding은 보통 utf-8-sig 또는 cp949)
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding='cp949')

    # 'treatment_tags' 컬럼에서 '피부'가 포함된 행 추출
    # 결측치(NaN) 처리 포함
    filtered_df = df[df['treatment_tags'].str.contains('피부', na=False)]

    # 결과 저장
    filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Filtered file saved to: {output_file}")
    print(f"Total rows filtered: {len(filtered_df)}")

except Exception as e:
    print(f"Error occurred: {e}")
