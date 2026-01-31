import pandas as pd
import sys

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# 데이터 로드
df = pd.read_csv('data_260131_0844/서울_병원_통합_2025.12.csv', encoding='utf-8-sig')

print(f'Total rows: {len(df):,}')
print(f'Total columns: {len(df.columns)}')

# 컬럼 리스트를 파일로 저장
with open('column_list.txt', 'w', encoding='utf-8') as f:
    f.write('All Columns:\n')
    f.write('='*60 + '\n')
    for i, col in enumerate(df.columns, 1):
        f.write(f'{i}. {col}\n')
    
    # 진료과목 관련 컬럼
    f.write('\n\nDepartment-related columns:\n')
    f.write('='*60 + '\n')
    dept_cols = [col for col in df.columns if '진료' in col or '과목' in col or '피부' in col]
    for col in dept_cols:
        f.write(f'  - {col}\n')
        f.write(f'    Type: {df[col].dtype}\n')
        f.write(f'    Non-null: {df[col].notna().sum():,}\n')
        f.write(f'    Unique: {df[col].nunique()}\n')
        if df[col].dtype == 'object':
            f.write(f'    Sample: {df[col].dropna().head(5).tolist()}\n')
        f.write('\n')

print('Column list saved to column_list.txt')

# 강남구 데이터 확인
gangnam = df[df['시군구코드명']=='강남구']
print(f'\nGangnam hospitals: {len(gangnam):,}')

# 데이터 샘플 저장
gangnam.head(10).to_csv('gangnam_sample.csv', encoding='utf-8-sig', index=False)
print('Gangnam sample saved to gangnam_sample.csv')
