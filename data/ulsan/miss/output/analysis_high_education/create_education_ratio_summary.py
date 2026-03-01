# -*- coding: utf-8 -*-
"""
업종별 연도별 학력 비중 및 집계 테이블 생성
- 행: 업종
- 열: 연도별(2022, 2023, 2024, 3년평균)
- 블록1: 전문대졸+대졸 합산 비중
- 블록2: 전문대졸 비중
- 블록3: 대졸 비중
- 블록4: 학력별 구인인원 집계 (전체, 학력무관, 고졸이하, 전문대졸, 대졸, 대학원졸)
"""

import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INPUT_FILE = os.path.join(BASE_DIR, 'output', 'preprocessed_supply_up.csv')
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
print(f"입력 데이터: {df.shape}")

years = [2022, 2023, 2024]

# ============================================================
# 1. 업종×연도별 전체 구인인원
# ============================================================
total = df.groupby(['통합_산업명', '연도'])['구인인원'].sum().unstack(fill_value=0)
total.columns = [f'전체구인_{y}' for y in total.columns]
total['전체구인_3년합계'] = total.sum(axis=1)

# ============================================================
# 2. 학력그룹별 업종×연도 구인인원
# ============================================================
groups = ['학력무관', '고졸이하', '전문대졸', '대졸', '대학원졸']
group_dfs = {}

for g in groups:
    gdf = df[df['학력_그룹'] == g].groupby(['통합_산업명', '연도'])['구인인원'].sum().unstack(fill_value=0)
    gdf.columns = [f'{g}_{y}' for y in gdf.columns]
    gdf[f'{g}_3년합계'] = gdf.sum(axis=1)
    group_dfs[g] = gdf

# ============================================================
# 3. 비중 계산
# ============================================================
total_arr = df.groupby(['통합_산업명', '연도'])['구인인원'].sum().unstack(fill_value=0)

# 전문대졸 비중
jun = df[df['학력_그룹'] == '전문대졸'].groupby(['통합_산업명', '연도'])['구인인원'].sum().unstack(fill_value=0)
jun = jun.reindex(total_arr.index, fill_value=0)
jun_ratio = (jun / total_arr * 100).round(1).fillna(0)

# 대졸 비중
dae = df[df['학력_그룹'] == '대졸'].groupby(['통합_산업명', '연도'])['구인인원'].sum().unstack(fill_value=0)
dae = dae.reindex(total_arr.index, fill_value=0)
dae_ratio = (dae / total_arr * 100).round(1).fillna(0)

# 전문대졸+대졸 합산 비중
combined = jun + dae
combined_ratio = (combined / total_arr * 100).round(1).fillna(0)

# 3년 평균 비중
combined_ratio['3년평균'] = combined_ratio.mean(axis=1).round(1)
jun_ratio['3년평균'] = jun_ratio.mean(axis=1).round(1)
dae_ratio['3년평균'] = dae_ratio.mean(axis=1).round(1)

# 컬럼명 정리
combined_ratio.columns = [f'전문대+대졸_비중(%)_{c}' if c != '3년평균' else '전문대+대졸_비중(%)_3년평균' for c in combined_ratio.columns]
jun_ratio.columns = [f'전문대졸_비중(%)_{c}' if c != '3년평균' else '전문대졸_비중(%)_3년평균' for c in jun_ratio.columns]
dae_ratio.columns = [f'대졸_비중(%)_{c}' if c != '3년평균' else '대졸_비중(%)_3년평균' for c in dae_ratio.columns]

# ============================================================
# 4. 결합: 비중 블록 + 집계 블록
# ============================================================
result = pd.concat([
    combined_ratio,   # 전문대졸+대졸 비중
    jun_ratio,        # 전문대졸 비중
    dae_ratio,        # 대졸 비중
    total,            # 전체 구인
    group_dfs['학력무관'],
    group_dfs['고졸이하'],
    group_dfs['전문대졸'],
    group_dfs['대졸'],
    group_dfs['대학원졸'],
], axis=1)

result = result.fillna(0)

# 전체구인 3년합계 기준 내림차순 정렬
result = result.sort_values('전체구인_3년합계', ascending=False)
result = result.reset_index()

# ============================================================
# 5. 저장
# ============================================================
path = os.path.join(OUTPUT_DIR, 'education_ratio_summary.csv')
result.to_csv(path, index=False, encoding='utf-8-sig')
print(f"[저장] {path}")

# 콘솔 출력
print(f"\n최종 shape: {result.shape}")
print(f"컬럼 수: {len(result.columns)}")
print(f"\n=== 전문대졸+대졸 비중 (3년평균 TOP10) ===")
cols_show = ['통합_산업명', '전문대+대졸_비중(%)_3년평균', '전문대졸_비중(%)_3년평균', '대졸_비중(%)_3년평균', '전체구인_3년합계']
top = result.sort_values('전문대+대졸_비중(%)_3년평균', ascending=False).head(10)
print(top[cols_show].to_string(index=False))

print(f"\n=== 컬럼 목록 ===")
for i, c in enumerate(result.columns):
    print(f"  {i+1:2d}. {c}")
