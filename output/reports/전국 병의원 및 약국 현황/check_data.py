import pandas as pd

# 데이터 로드
df = pd.read_csv('data_260131_0844/서울_병원_통합_2025.12.csv', encoding='utf-8-sig')

print(f'총 행: {len(df):,}')
print(f'총 열: {len(df.columns)}')
print('\n컬럼 목록 (처음 30개):')
for i, col in enumerate(df.columns[:30], 1):
    print(f'{i}. {col}')

print(f'\n강남구 병원: {len(df[df["시군구코드명"]=="강남구"]):,}개')
print(f'서울 전체 병원: {len(df):,}개')

# 진료과목 확인
if '진료과목코드명' in df.columns:
    gangnam_derma = df[(df['시군구코드명']=='강남구') & (df['진료과목코드명']=='피부과')]
    print(f'강남구 피부과: {len(gangnam_derma):,}개')
