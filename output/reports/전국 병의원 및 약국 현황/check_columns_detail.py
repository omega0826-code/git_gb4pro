import pandas as pd

# 데이터 로드
df = pd.read_csv('data_260131_0844/서울_병원_통합_2025.12.csv', encoding='utf-8-sig')

print(f'Total rows: {len(df):,}')
print(f'Total columns: {len(df.columns)}')
print('\nAll column names:')
for i, col in enumerate(df.columns, 1):
    print(f'{i}. {col}')

# 진료과목 관련 컬럼 찾기
print('\n\nColumns containing "진료" or "과목":')
dept_cols = [col for col in df.columns if '진료' in col or '과목' in col]
for col in dept_cols:
    print(f'  - {col}')
    print(f'    Sample values: {df[col].dropna().head(3).tolist()}')
    print(f'    Unique count: {df[col].nunique()}')
    print()

# 강남구 데이터 확인
print('\nGangnam-gu data:')
gangnam = df[df['시군구코드명']=='강남구']
print(f'Total hospitals in Gangnam: {len(gangnam):,}')

# 진료과목 데이터 샘플
if dept_cols:
    print(f'\nSample department data from Gangnam:')
    for col in dept_cols:
        print(f'\n{col}:')
        print(gangnam[col].value_counts().head(10))
