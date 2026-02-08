# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 정밀 데이터 검토 및 종합점수 재산출
작성일: 2026-02-04
버전: Audit V1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 경로 설정
BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
DATA_PATH = BASE_DIR / 'Gangnam_9_Areas'
OUTPUT_DIR = BASE_DIR / 'REPORT' / '07_정밀검토'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("정밀 데이터 검토 및 종합점수 재산출")
print("=" * 80)

# =============================================================================
# 1. 데이터 로딩 및 기간 통일 (2022-2024)
# =============================================================================
print("\n[1/5] 데이터 로딩 중...")

# 모든 데이터셋 로드
df_store = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')
df_sales = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')
df_resident = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(상주인구-상권).csv', encoding='utf-8-sig')
df_worker = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(직장인구-상권).csv', encoding='utf-8-sig')
df_floating = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(길단위인구-상권).csv', encoding='utf-8-sig')
df_facility = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(집객시설-상권).csv', encoding='utf-8-sig')
df_income = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(소득소비-상권).csv', encoding='utf-8-sig')
df_change = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(상권변화지표-상권).csv', encoding='utf-8-sig')
df_area = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(영역-상권).csv', encoding='utf-8-sig')

# 통일 기준: 2024년 4분기 (점포, 매출 데이터 기준)
TARGET_PERIOD = 20244

# =============================================================================
# 2. 차원별 지표 추출
# =============================================================================
print("\n[2/5] 차원별 지표 추출 중...")

# 상권 목록
areas = df_area['상권_코드_명'].unique()
print(f"  - 분석 대상 상권: {len(areas)}개")

# 결과 저장용 DataFrame
results = pd.DataFrame({'상권_명': areas})

# --- 경쟁 환경 (Competition) ---
df_store_latest = df_store[df_store['기준_년분기_코드'] == TARGET_PERIOD]
df_clinic = df_store_latest[df_store_latest['서비스_업종_코드_명'].str.contains('의원|피부', na=False)]
competition = df_clinic.groupby('상권_코드_명')['점포_수'].sum()
results = results.merge(competition.rename('경쟁_점포수'), left_on='상권_명', right_index=True, how='left').fillna(0)

# --- 고객 수요 (Customer) ---
df_sales_latest = df_sales[df_sales['기준_년분기_코드'] == TARGET_PERIOD]
# 타겟: 20-40대 매출
target_sales = df_sales_latest.groupby('상권_코드_명').agg({
    '연령대_20_매출_금액': 'sum',
    '연령대_30_매출_금액': 'sum',
    '연령대_40_매출_금액': 'sum',
    '여성_매출_금액': 'sum'
}).reset_index()
target_sales['타겟_매출'] = target_sales['연령대_20_매출_금액'] + target_sales['연령대_30_매출_금액'] + target_sales['연령대_40_매출_금액']
target_sales['여성_매출'] = target_sales['여성_매출_금액']
results = results.merge(target_sales[['상권_코드_명', '타겟_매출', '여성_매출']], left_on='상권_명', right_on='상권_코드_명', how='left').drop(columns=['상권_코드_명'])

# --- 인구 유동 (Population) ---
# 상주인구 (최신)
res_latest = df_resident[df_resident['기준_년분기_코드'] == df_resident['기준_년분기_코드'].max()]
res_pop = res_latest.groupby('상권_코드_명')['총_상주인구_수'].sum()
results = results.merge(res_pop.rename('상주인구'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 직장인구 (최신)
work_latest = df_worker[df_worker['기준_년분기_코드'] == df_worker['기준_년분기_코드'].max()]
work_pop = work_latest.groupby('상권_코드_명')['총_직장_인구_수'].sum()
results = results.merge(work_pop.rename('직장인구'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 유동인구 (최신) - 가이드라인에서 빠졌던 부분 추가!
float_latest = df_floating[df_floating['기준_년분기_코드'] == df_floating['기준_년분기_코드'].max()]
float_pop = float_latest.groupby('상권_코드_명')['총_유동인구_수'].sum()
float_target = float_latest.groupby('상권_코드_명').apply(
    lambda x: x['연령대_20_유동인구_수'].sum() + x['연령대_30_유동인구_수'].sum() + x['연령대_40_유동인구_수'].sum()
)
results = results.merge(float_pop.rename('유동인구'), left_on='상권_명', right_index=True, how='left').fillna(0)
results = results.merge(float_target.rename('타겟_유동인구'), left_on='상권_명', right_index=True, how='left').fillna(0)

# --- 입지 조건 (Location/Infrastructure) ---
fac_latest = df_facility[df_facility['기준_년분기_코드'] == df_facility['기준_년분기_코드'].max()]
fac_score = fac_latest.groupby('상권_코드_명')['집객시설_수'].sum()
results = results.merge(fac_score.rename('집객시설'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 소득 수준 (최신)
income_latest = df_income[df_income['기준_년분기_코드'] == df_income['기준_년분기_코드'].max()]
income_score = income_latest.groupby('상권_코드_명')['월_평균_소득_금액'].mean()
results = results.merge(income_score.rename('평균소득'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 의료비 지출 (새로운 지표!)
medical_exp = income_latest.groupby('상권_코드_명')['의료비_지출_총금액'].sum()
results = results.merge(medical_exp.rename('의료비지출'), left_on='상권_명', right_index=True, how='left').fillna(0)

# =============================================================================
# 3. 종합 점수 재산출 (Refined Methodology)
# =============================================================================
print("\n[3/5] 종합 점수 재산출 중...")

def normalize(series):
    if series.max() == series.min():
        return pd.Series([1.0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())

# --- 차원별 점수 산출 ---
# 1) 경쟁 환경 (낮을수록 좋음)
results['경쟁_점수'] = 1 - normalize(results['경쟁_점포수'])

# 2) 고객 수요 (높을수록 좋음)
results['타겟_매출_N'] = normalize(results['타겟_매출'])
results['여성_매출_N'] = normalize(results['여성_매출'])
results['고객_점수'] = (results['타겟_매출_N'] * 0.6 + results['여성_매출_N'] * 0.4)

# 3) 인구 유동 (수정: 유동인구 포함)
results['상주_N'] = normalize(results['상주인구'])
results['직장_N'] = normalize(results['직장인구'])
results['유동_N'] = normalize(results['유동인구'])
results['타겟유동_N'] = normalize(results['타겟_유동인구'])
# 가중치: 유동인구(40%) + 타겟유동(30%) + 직장(20%) + 상주(10%)
results['인구_점수'] = (results['유동_N'] * 0.4 + results['타겟유동_N'] * 0.3 + results['직장_N'] * 0.2 + results['상주_N'] * 0.1)

# 4) 입지 조건 (수정: 의료비 지출 포함)
results['시설_N'] = normalize(results['집객시설'])
results['소득_N'] = normalize(results['평균소득'])
results['의료비_N'] = normalize(results['의료비지출'])
# 가중치: 집객시설(40%) + 소득(30%) + 의료비지출(30%)
results['입지_점수'] = (results['시설_N'] * 0.4 + results['소득_N'] * 0.3 + results['의료비_N'] * 0.3)

# --- 최종 종합 점수 (가중치: 경쟁 20%, 고객 40%, 인구 20%, 입지 20%) ---
results['종합점수'] = (
    results['경쟁_점수'] * 0.20 +
    results['고객_점수'] * 0.40 +
    results['인구_점수'] * 0.20 +
    results['입지_점수'] * 0.20
) * 100

# 순위 정렬
results = results.sort_values(by='종합점수', ascending=False).reset_index(drop=True)
results['순위'] = range(1, len(results) + 1)

# =============================================================================
# 4. 시각화 및 리포트 생성
# =============================================================================
print("\n[4/5] 시각화 생성 중...")

# 4-1. 종합 점수 순위
fig, ax = plt.subplots(figsize=(12, 7))
colors = plt.cm.magma(np.linspace(0.2, 0.8, len(results)))
bars = ax.barh(results['상권_명'], results['종합점수'], color=colors)
ax.set_xlabel('종합 점수', fontsize=12)
ax.set_title('강남 9개 상권 - 피부과 입지 종합 점수 (정밀 검토)', fontsize=14, fontweight='bold')
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)
for bar, score in zip(bars, results['종합점수']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{score:.1f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '종합점수_정밀검토.png', dpi=150)
plt.close()

# 4-2. 4차원 레이더 차트 (TOP 3)
from math import pi
categories = ['경쟁', '고객', '인구', '입지']
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
colors_radar = ['#FF6B6B', '#4ECDC4', '#FFE66D']
for i in range(3):
    row = results.iloc[i]
    values = [row['경쟁_점수'], row['고객_점수'], row['인구_점수'], row['입지_점수']]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=row['상권_명'], color=colors_radar[i])
    ax.fill(angles, values, alpha=0.15, color=colors_radar[i])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=11)
ax.set_title('TOP 3 상권 4차원 비교 (정밀 검토)', size=14, y=1.1, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '레이더_정밀검토.png', dpi=150)
plt.close()

# 4-3. 상세 비교 히트맵
fig, ax = plt.subplots(figsize=(14, 8))
heatmap_data = results[['상권_명', '경쟁_점수', '고객_점수', '인구_점수', '입지_점수']].set_index('상권_명')
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax, vmin=0, vmax=1)
ax.set_title('상권별 차원별 점수 히트맵 (정밀 검토)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '히트맵_정밀검토.png', dpi=150)
plt.close()

# =============================================================================
# 5. 결과 저장
# =============================================================================
print("\n[5/5] 결과 저장 중...")

# 전체 결과 CSV
results.to_csv(OUTPUT_DIR / '정밀검토_종합점수.csv', index=False, encoding='utf-8-sig')

# 요약 출력
print("\n" + "=" * 80)
print("정밀 검토 완료 - TOP 3 추천 상권")
print("=" * 80)
for i in range(3):
    row = results.iloc[i]
    print(f"\n{row['순위']}위. {row['상권_명']} (종합점수: {row['종합점수']:.1f}점)")
    print(f"   - 경쟁: {row['경쟁_점수']:.2f} | 고객: {row['고객_점수']:.2f} | 인구: {row['인구_점수']:.2f} | 입지: {row['입지_점수']:.2f}")

print(f"\n결과 저장 경로: {OUTPUT_DIR}")
