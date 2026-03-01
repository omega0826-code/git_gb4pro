# -*- coding: utf-8 -*-
"""
울산 산업별 연간 학력별 구인인원 비중 분석
- 행: 업종별 × 학력 수준(학력_그룹: 학력무관, 고졸이하, 전문대졸, 대졸, 대학원졸)
- 열: 연도별 데이터 (2022, 2023, 2024)
- 핵심: 전문대졸 이상 구인비중
"""

import pandas as pd
import os
from datetime import datetime

# ============================================================
# 경로 설정
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INPUT_FILE = os.path.join(BASE_DIR, 'output', 'preprocessed_supply_up.csv')
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"[시작] 고학력 구인비중 분석: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================
# 데이터 로드
# ============================================================
df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
print(f"입력 데이터: {df.shape}")

# ============================================================
# 1. 업종별 × 학력그룹별 × 연도별 구인인원 집계
# ============================================================
pivot = df.groupby(['통합_산업명', '학력_그룹', '연도'])['구인인원'].sum().reset_index()

# ============================================================
# 2. 업종별 × 연도별 전체 구인인원 (비중 계산용 분모)
# ============================================================
total_by_year = df.groupby(['통합_산업명', '연도'])['구인인원'].sum().reset_index()
total_by_year.rename(columns={'구인인원': '연간_전체'}, inplace=True)

# merge
pivot = pivot.merge(total_by_year, on=['통합_산업명', '연도'], how='left')
pivot['비중(%)'] = (pivot['구인인원'] / pivot['연간_전체'] * 100).round(1)
pivot['비중(%)'] = pivot['비중(%)'].fillna(0)

# ============================================================
# 3. 산출물 1: 업종별 × 학력그룹별 × 연도별 구인인원 (피벗 테이블)
# ============================================================
# 구인인원 피벗
tbl_count = pivot.pivot_table(
    index=['통합_산업명', '학력_그룹'],
    columns='연도',
    values='구인인원',
    fill_value=0,
    aggfunc='sum'
)
tbl_count.columns = [f'{y}년_구인인원' for y in tbl_count.columns]

# 비중 피벗
tbl_ratio = pivot.pivot_table(
    index=['통합_산업명', '학력_그룹'],
    columns='연도',
    values='비중(%)',
    fill_value=0,
    aggfunc='sum'
)
tbl_ratio.columns = [f'{y}년_비중(%)' for y in tbl_ratio.columns]

# 결합
tbl_combined = pd.concat([tbl_count, tbl_ratio], axis=1)

# 연도별로 정렬 (구인인원, 비중)
col_order = []
for y in [2022, 2023, 2024]:
    col_order.append(f'{y}년_구인인원')
    col_order.append(f'{y}년_비중(%)')
tbl_combined = tbl_combined[col_order]
tbl_combined = tbl_combined.reset_index()

# 정렬: 산업명순 → 학력그룹순
edu_order = {'학력무관': 0, '고졸이하': 1, '전문대졸': 2, '대졸': 3, '대학원졸': 4, '기타': 5}
tbl_combined['_sort'] = tbl_combined['학력_그룹'].map(edu_order)
tbl_combined = tbl_combined.sort_values(['통합_산업명', '_sort']).drop(columns='_sort')

# 저장
path1 = os.path.join(OUTPUT_DIR, 'industry_education_yearly.csv')
tbl_combined.to_csv(path1, index=False, encoding='utf-8-sig')
print(f"[저장] {path1}")

# ============================================================
# 4. 산출물 2: 고학력 구인비중 요약 (업종별 × 연도별)
# ============================================================
high_edu = pivot[pivot['학력_그룹'].isin(['전문대졸', '대졸', '대학원졸'])].copy()
high_edu = high_edu.groupby(['통합_산업명', '연도']).agg(
    구인인원=('구인인원', 'sum'),
    연간_전체=('연간_전체', 'first')
).reset_index()
high_edu['비중(%)'] = (high_edu['구인인원'] / high_edu['연간_전체'] * 100).round(1)

tbl_high = high_edu.pivot_table(
    index='통합_산업명',
    columns='연도',
    values=['구인인원', '비중(%)'],
    fill_value=0,
    aggfunc='sum'
)

# 컬럼 정리
result = pd.DataFrame()
result['통합_산업명'] = high_edu['통합_산업명'].unique()
result = result.set_index('통합_산업명')

for y in [2022, 2023, 2024]:
    yr_data = high_edu[high_edu['연도'] == y].set_index('통합_산업명')
    result[f'{y}년_고학력_구인'] = yr_data['구인인원']
    result[f'{y}년_고학력_비중(%)'] = yr_data['비중(%)']

result = result.fillna(0)

# 3개년 평균 비중 추가
result['3개년_평균비중(%)'] = result[[c for c in result.columns if '비중' in c]].mean(axis=1).round(1)

# 3개년 평균비중 내림차순 정렬
result = result.sort_values('3개년_평균비중(%)', ascending=False)
result = result.reset_index()

path2 = os.path.join(OUTPUT_DIR, 'high_education_ratio_by_industry.csv')
result.to_csv(path2, index=False, encoding='utf-8-sig')
print(f"[저장] {path2}")

# ============================================================
# 5. 산출물 3: 전체 요약 통계
# ============================================================
print("\n" + "=" * 60)
print("전문대졸 이상(전문대졸+대졸+대학원졸) 구인비중 TOP 10 (3개년 평균)")
print("=" * 60)
for _, row in result.head(10).iterrows():
    print(f"  {row['통합_산업명']:<45} {row['3개년_평균비중(%)']:>5.1f}%")

print(f"\n전체 평균 전문대졸 이상 비중:")
for y in [2022, 2023, 2024]:
    total_all = df[df['연도'] == y]['구인인원'].sum()
    total_high = df[(df['연도'] == y) & (df['학력_그룹'].isin(['전문대졸', '대졸', '대학원졸']))]['구인인원'].sum()
    ratio = total_high / total_all * 100 if total_all > 0 else 0
    print(f"  {y}년: {total_high:,}명 / {total_all:,}명 = {ratio:.1f}%")

print(f"\n학력그룹별 연도별 구인인원:")
for y in [2022, 2023, 2024]:
    print(f"  [{y}년]")
    grp = df[df['연도'] == y].groupby('학력_그룹')['구인인원'].sum().sort_values(ascending=False)
    for g, v in grp.items():
        print(f"    {g:<10} {v:>8,}명")

print(f"\n[완료] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
