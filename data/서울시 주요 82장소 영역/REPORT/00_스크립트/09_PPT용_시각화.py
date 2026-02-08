# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - PPT용 시각화 및 로데이터 생성
작성일: 2026-02-04
버전: Final Report V1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from math import pi
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300  # PPT용 고해상도

# 경로 설정
BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
DATA_PATH = BASE_DIR / 'Gangnam_9_Areas'
OUTPUT_DIR = BASE_DIR / 'REPORT' / '08_최종보고서'
RAW_DATA_DIR = OUTPUT_DIR / 'raw_data'
CHART_DIR = OUTPUT_DIR / 'charts'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("PPT용 시각화 및 로데이터 생성")
print("=" * 80)

# =============================================================================
# 1. 데이터 로딩 및 처리
# =============================================================================
print("\n[1/6] 데이터 로딩 중...")

TARGET_PERIOD = 20244

df_store = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')
df_sales = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')
df_resident = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(상주인구-상권).csv', encoding='utf-8-sig')
df_worker = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(직장인구-상권).csv', encoding='utf-8-sig')
df_floating = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(길단위인구-상권).csv', encoding='utf-8-sig')
df_facility = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(집객시설-상권).csv', encoding='utf-8-sig')
df_income = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(소득소비-상권).csv', encoding='utf-8-sig')
df_area = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(영역-상권).csv', encoding='utf-8-sig')

areas = df_area['상권_코드_명'].unique()

# =============================================================================
# 2. 지표 추출 및 점수 산출
# =============================================================================
print("\n[2/6] 지표 추출 및 점수 산출 중...")

results = pd.DataFrame({'상권_명': areas})

# 경쟁 환경
df_store_latest = df_store[df_store['기준_년분기_코드'] == TARGET_PERIOD]
df_clinic = df_store_latest[df_store_latest['서비스_업종_코드_명'].str.contains('의원|피부', na=False)]
competition = df_clinic.groupby('상권_코드_명')['점포_수'].sum()
results = results.merge(competition.rename('경쟁_점포수'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 고객 수요
df_sales_latest = df_sales[df_sales['기준_년분기_코드'] == TARGET_PERIOD]
target_sales = df_sales_latest.groupby('상권_코드_명').agg({
    '연령대_20_매출_금액': 'sum', '연령대_30_매출_금액': 'sum', '연령대_40_매출_금액': 'sum',
    '여성_매출_금액': 'sum', '당월_매출_금액': 'sum'
}).reset_index()
target_sales['타겟_매출'] = target_sales['연령대_20_매출_금액'] + target_sales['연령대_30_매출_금액'] + target_sales['연령대_40_매출_금액']
target_sales['여성_매출'] = target_sales['여성_매출_금액']
target_sales['전체_매출'] = target_sales['당월_매출_금액']
results = results.merge(target_sales[['상권_코드_명', '타겟_매출', '여성_매출', '전체_매출']], left_on='상권_명', right_on='상권_코드_명', how='left').drop(columns=['상권_코드_명'])

# 인구 유동
res_latest = df_resident[df_resident['기준_년분기_코드'] == df_resident['기준_년분기_코드'].max()]
res_pop = res_latest.groupby('상권_코드_명')['총_상주인구_수'].sum()
results = results.merge(res_pop.rename('상주인구'), left_on='상권_명', right_index=True, how='left').fillna(0)

work_latest = df_worker[df_worker['기준_년분기_코드'] == df_worker['기준_년분기_코드'].max()]
work_pop = work_latest.groupby('상권_코드_명')['총_직장_인구_수'].sum()
results = results.merge(work_pop.rename('직장인구'), left_on='상권_명', right_index=True, how='left').fillna(0)

float_latest = df_floating[df_floating['기준_년분기_코드'] == df_floating['기준_년분기_코드'].max()]
float_pop = float_latest.groupby('상권_코드_명')['총_유동인구_수'].sum()
float_target = float_latest.groupby('상권_코드_명').apply(
    lambda x: x['연령대_20_유동인구_수'].sum() + x['연령대_30_유동인구_수'].sum() + x['연령대_40_유동인구_수'].sum()
)
results = results.merge(float_pop.rename('유동인구'), left_on='상권_명', right_index=True, how='left').fillna(0)
results = results.merge(float_target.rename('타겟_유동인구'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 입지 조건
fac_latest = df_facility[df_facility['기준_년분기_코드'] == df_facility['기준_년분기_코드'].max()]
fac_score = fac_latest.groupby('상권_코드_명')['집객시설_수'].sum()
results = results.merge(fac_score.rename('집객시설'), left_on='상권_명', right_index=True, how='left').fillna(0)

income_latest = df_income[df_income['기준_년분기_코드'] == df_income['기준_년분기_코드'].max()]
income_score = income_latest.groupby('상권_코드_명')['월_평균_소득_금액'].mean()
medical_exp = income_latest.groupby('상권_코드_명')['의료비_지출_총금액'].sum()
results = results.merge(income_score.rename('평균소득'), left_on='상권_명', right_index=True, how='left').fillna(0)
results = results.merge(medical_exp.rename('의료비지출'), left_on='상권_명', right_index=True, how='left').fillna(0)

# 점수 정규화
def normalize(series):
    if series.max() == series.min():
        return pd.Series([1.0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())

results['경쟁_점수'] = 1 - normalize(results['경쟁_점포수'])
results['타겟매출_N'] = normalize(results['타겟_매출'])
results['여성매출_N'] = normalize(results['여성_매출'])
results['고객_점수'] = (results['타겟매출_N'] * 0.6 + results['여성매출_N'] * 0.4)
results['상주_N'] = normalize(results['상주인구'])
results['직장_N'] = normalize(results['직장인구'])
results['유동_N'] = normalize(results['유동인구'])
results['타겟유동_N'] = normalize(results['타겟_유동인구'])
results['인구_점수'] = (results['유동_N'] * 0.4 + results['타겟유동_N'] * 0.3 + results['직장_N'] * 0.2 + results['상주_N'] * 0.1)
results['시설_N'] = normalize(results['집객시설'])
results['소득_N'] = normalize(results['평균소득'])
results['의료비_N'] = normalize(results['의료비지출'])
results['입지_점수'] = (results['시설_N'] * 0.4 + results['소득_N'] * 0.3 + results['의료비_N'] * 0.3)
results['종합점수'] = (results['경쟁_점수'] * 0.20 + results['고객_점수'] * 0.40 + results['인구_점수'] * 0.20 + results['입지_점수'] * 0.20) * 100
results = results.sort_values(by='종합점수', ascending=False).reset_index(drop=True)
results['순위'] = range(1, len(results) + 1)

# =============================================================================
# 3. PPT용 시각화 생성
# =============================================================================
print("\n[3/6] PPT용 시각화 생성 중...")

# --- 차트 1: 종합 점수 순위 ---
fig, ax = plt.subplots(figsize=(14, 8))
colors = ['#FF6B6B' if i < 3 else '#4ECDC4' if i < 6 else '#95A5A6' for i in range(len(results))]
bars = ax.barh(results['상권_명'], results['종합점수'], color=colors, edgecolor='white', linewidth=0.5)
ax.set_xlabel('종합 점수 (100점 만점)', fontsize=14, fontweight='bold')
ax.set_title('강남 9개 상권 피부과 입지 종합 평가', fontsize=18, fontweight='bold', pad=20)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, score, rank in zip(bars, results['종합점수'], results['순위']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{score:.1f}점', va='center', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / '01_종합점수_순위.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 로데이터 저장
results[['순위', '상권_명', '종합점수', '경쟁_점수', '고객_점수', '인구_점수', '입지_점수']].to_csv(
    RAW_DATA_DIR / '01_종합점수_순위.csv', index=False, encoding='utf-8-sig')

# --- 차트 2: 4차원 레이더 차트 (TOP 3) ---
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
    ax.plot(angles, values, 'o-', linewidth=3, label=f"{row['순위']}위 {row['상권_명']}", color=colors_radar[i], markersize=8)
    ax.fill(angles, values, alpha=0.15, color=colors_radar[i])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=14, fontweight='bold')
ax.set_ylim(0, 1)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=12, frameon=False)
ax.set_title('TOP 3 상권 4차원 비교', size=18, y=1.08, fontweight='bold')
plt.tight_layout()
plt.savefig(CHART_DIR / '02_레이더_TOP3.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 로데이터 저장
results.head(3)[['순위', '상권_명', '경쟁_점수', '고객_점수', '인구_점수', '입지_점수']].to_csv(
    RAW_DATA_DIR / '02_레이더_TOP3.csv', index=False, encoding='utf-8-sig')

# --- 차트 3: 경쟁 vs 고객 수요 버블 차트 ---
fig, ax = plt.subplots(figsize=(12, 8))
bubble_sizes = results['유동인구'] / results['유동인구'].max() * 1000 + 100
scatter = ax.scatter(results['경쟁_점포수'], results['타겟_매출'] / 1e9, s=bubble_sizes, 
                     c=results['종합점수'], cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=1)
for i, row in results.iterrows():
    ax.annotate(row['상권_명'], (row['경쟁_점포수'], row['타겟_매출'] / 1e9), 
                xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
ax.set_xlabel('경쟁 점포 수 (개)', fontsize=14, fontweight='bold')
ax.set_ylabel('타겟 고객 매출 (십억 원)', fontsize=14, fontweight='bold')
ax.set_title('경쟁 강도 vs 고객 수요 (버블 크기: 유동인구)', fontsize=16, fontweight='bold', pad=15)
cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
cbar.set_label('종합 점수', fontsize=12)
ax.grid(alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / '03_경쟁_고객_버블.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 로데이터 저장
results[['상권_명', '경쟁_점포수', '타겟_매출', '유동인구', '종합점수']].to_csv(
    RAW_DATA_DIR / '03_경쟁_고객_버블.csv', index=False, encoding='utf-8-sig')

# --- 차트 4: 차원별 점수 히트맵 ---
fig, ax = plt.subplots(figsize=(12, 8))
heatmap_data = results[['상권_명', '경쟁_점수', '고객_점수', '인구_점수', '입지_점수']].set_index('상권_명')
heatmap_data.columns = ['경쟁\n(낮을수록 좋음)', '고객 수요', '인구 유동', '입지 조건']
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax, 
            vmin=0, vmax=1, linewidths=0.5, annot_kws={'size': 12, 'fontweight': 'bold'})
ax.set_title('상권별 차원별 점수 히트맵', fontsize=16, fontweight='bold', pad=15)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=11)
plt.tight_layout()
plt.savefig(CHART_DIR / '04_차원별_히트맵.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 로데이터 저장
heatmap_data.reset_index().to_csv(RAW_DATA_DIR / '04_차원별_히트맵.csv', index=False, encoding='utf-8-sig')

# --- 차트 5: 인구 구조 비교 (유동/직장/상주) ---
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(results))
width = 0.25
bars1 = ax.bar(x - width, results['유동인구'] / 1e6, width, label='유동인구 (백만)', color='#FF6B6B')
bars2 = ax.bar(x, results['직장인구'] / 1e4, width, label='직장인구 (만)', color='#4ECDC4')
bars3 = ax.bar(x + width, results['상주인구'] / 1e3, width, label='상주인구 (천)', color='#45B7D1')
ax.set_xlabel('상권', fontsize=14, fontweight='bold')
ax.set_ylabel('인구 규모', fontsize=14, fontweight='bold')
ax.set_title('상권별 인구 구조 비교', fontsize=16, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(results['상권_명'], rotation=45, ha='right', fontsize=10)
ax.legend(loc='upper right', fontsize=11, frameon=False)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / '05_인구구조_비교.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 로데이터 저장
results[['상권_명', '유동인구', '직장인구', '상주인구', '타겟_유동인구']].to_csv(
    RAW_DATA_DIR / '05_인구구조_비교.csv', index=False, encoding='utf-8-sig')

# --- 차트 6: TOP 3 상권 프로필 카드 ---
fig, axes = plt.subplots(1, 3, figsize=(18, 8))
colors_profile = ['#FF6B6B', '#4ECDC4', '#FFE66D']
for i, ax in enumerate(axes):
    row = results.iloc[i]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 배경
    rect = plt.Rectangle((0, 0), 10, 10, facecolor=colors_profile[i], alpha=0.1, edgecolor=colors_profile[i], linewidth=3)
    ax.add_patch(rect)
    
    # 내용
    ax.text(5, 9, f'🏆 {row["순위"]}위', fontsize=24, fontweight='bold', ha='center', va='center')
    ax.text(5, 7.5, row['상권_명'], fontsize=20, fontweight='bold', ha='center', va='center')
    ax.text(5, 6, f'종합 점수: {row["종합점수"]:.1f}점', fontsize=18, ha='center', va='center', color=colors_profile[i])
    
    ax.text(1, 4.5, f'경쟁: {row["경쟁_점수"]:.2f}', fontsize=14, ha='left', va='center')
    ax.text(1, 3.5, f'고객: {row["고객_점수"]:.2f}', fontsize=14, ha='left', va='center')
    ax.text(5.5, 4.5, f'인구: {row["인구_점수"]:.2f}', fontsize=14, ha='left', va='center')
    ax.text(5.5, 3.5, f'입지: {row["입지_점수"]:.2f}', fontsize=14, ha='left', va='center')
    
    ax.text(5, 1.5, f'유동인구: {row["유동인구"]/1e6:.1f}백만', fontsize=12, ha='center', va='center', color='gray')
    ax.text(5, 0.8, f'타겟 매출: {row["타겟_매출"]/1e9:.0f}십억', fontsize=12, ha='center', va='center', color='gray')

plt.suptitle('TOP 3 상권 프로필', fontsize=22, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(CHART_DIR / '06_TOP3_프로필.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 로데이터 저장
results.head(3)[['순위', '상권_명', '종합점수', '경쟁_점수', '고객_점수', '인구_점수', '입지_점수', '유동인구', '타겟_매출']].to_csv(
    RAW_DATA_DIR / '06_TOP3_프로필.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 4. 전체 로데이터 저장
# =============================================================================
print("\n[4/6] 전체 로데이터 저장 중...")

# 전체 분석 결과
results.to_csv(RAW_DATA_DIR / '00_전체_분석결과.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 5. 완료
# =============================================================================
print("\n[5/6] 완료!")
print(f"\n시각화 저장 경로: {CHART_DIR}")
print(f"로데이터 저장 경로: {RAW_DATA_DIR}")
print("\n생성된 차트:")
for f in CHART_DIR.glob('*.png'):
    print(f"  - {f.name}")
print("\n생성된 로데이터:")
for f in RAW_DATA_DIR.glob('*.csv'):
    print(f"  - {f.name}")
