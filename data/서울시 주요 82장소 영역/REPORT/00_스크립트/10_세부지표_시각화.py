# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 세부 지표 완전 시각화
작성일: 2026-02-04
버전: Complete V1.0
목적: 모든 세부 지표에 대한 개별 시각화 및 로데이터 생성
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
plt.rcParams['figure.dpi'] = 300

# 경로 설정
BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
DATA_PATH = BASE_DIR / 'Gangnam_9_Areas'
OUTPUT_DIR = BASE_DIR / 'REPORT' / '09_완전보고서'
RAW_DATA_DIR = OUTPUT_DIR / 'raw_data'
CHART_DIR = OUTPUT_DIR / 'charts'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("세부 지표 완전 시각화 생성")
print("=" * 80)

# =============================================================================
# 1. 데이터 로딩
# =============================================================================
print("\n[1/8] 데이터 로딩 중...")

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
# 2. 차원 1: 경쟁 환경 분석
# =============================================================================
print("\n[2/8] 경쟁 환경 분석 중...")

df_store_latest = df_store[df_store['기준_년분기_코드'] == TARGET_PERIOD]
df_clinic = df_store_latest[df_store_latest['서비스_업종_코드_명'].str.contains('의원|피부', na=False)]
competition_detail = df_clinic.groupby(['상권_코드_명', '서비스_업종_코드_명'])['점포_수'].sum().reset_index()
competition_total = df_clinic.groupby('상권_코드_명')['점포_수'].sum().reset_index()
competition_total.columns = ['상권_명', '경쟁_점포수']

# 차트 A1: 경쟁 점포 수 (수평 막대)
fig, ax = plt.subplots(figsize=(14, 8))
comp_sorted = competition_total.sort_values('경쟁_점포수', ascending=True)
colors = ['#FF6B6B' if v > 200 else '#FFE66D' if v > 50 else '#4ECDC4' for v in comp_sorted['경쟁_점포수']]
bars = ax.barh(comp_sorted['상권_명'], comp_sorted['경쟁_점포수'], color=colors, edgecolor='white')
ax.set_xlabel('피부과/의원 점포 수 (개)', fontsize=14, fontweight='bold')
ax.set_title('A1. 상권별 경쟁 강도 (의원/피부과 점포 수)', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, comp_sorted['경쟁_점포수']):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, f'{int(v)}개', va='center', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'A1_경쟁_점포수.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
competition_total.to_csv(RAW_DATA_DIR / 'A1_경쟁_점포수.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 3. 차원 2: 고객 수요 분석
# =============================================================================
print("\n[3/8] 고객 수요 분석 중...")

df_sales_latest = df_sales[df_sales['기준_년분기_코드'] == TARGET_PERIOD]
customer_data = df_sales_latest.groupby('상권_코드_명').agg({
    '연령대_20_매출_금액': 'sum', '연령대_30_매출_금액': 'sum', '연령대_40_매출_금액': 'sum',
    '연령대_50_매출_금액': 'sum', '연령대_60_이상_매출_금액': 'sum',
    '여성_매출_금액': 'sum', '남성_매출_금액': 'sum', '당월_매출_금액': 'sum'
}).reset_index()
customer_data['타겟_매출'] = customer_data['연령대_20_매출_금액'] + customer_data['연령대_30_매출_금액'] + customer_data['연령대_40_매출_금액']
customer_data.columns = ['상권_명', '20대_매출', '30대_매출', '40대_매출', '50대_매출', '60대이상_매출', '여성_매출', '남성_매출', '전체_매출', '타겟_매출']

# 차트 B1: 타겟 매출 (20-40대)
fig, ax = plt.subplots(figsize=(14, 8))
cust_sorted = customer_data.sort_values('타겟_매출', ascending=True)
bars = ax.barh(cust_sorted['상권_명'], cust_sorted['타겟_매출'] / 1e9, color='#FF6B6B', edgecolor='white')
ax.set_xlabel('타겟 고객 매출 (십억 원)', fontsize=14, fontweight='bold')
ax.set_title('B1. 상권별 타겟 고객(20-40대) 매출', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, cust_sorted['타겟_매출']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{v/1e9:.0f}십억', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'B1_타겟_매출.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 B2: 여성 vs 남성 매출 비교
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(customer_data))
width = 0.35
cust_sorted2 = customer_data.sort_values('여성_매출', ascending=False)
bars1 = ax.bar(x - width/2, cust_sorted2['여성_매출'] / 1e9, width, label='여성 매출', color='#FF6B6B')
bars2 = ax.bar(x + width/2, cust_sorted2['남성_매출'] / 1e9, width, label='남성 매출', color='#4ECDC4')
ax.set_ylabel('매출 (십억 원)', fontsize=14, fontweight='bold')
ax.set_title('B2. 상권별 성별 매출 비교', fontsize=16, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(cust_sorted2['상권_명'], rotation=45, ha='right', fontsize=10)
ax.legend(fontsize=12, frameon=False)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'B2_성별_매출.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 B3: 연령대별 매출 스택 바
fig, ax = plt.subplots(figsize=(14, 8))
cust_sorted3 = customer_data.sort_values('전체_매출', ascending=False)
bottom = np.zeros(len(cust_sorted3))
age_cols = ['20대_매출', '30대_매출', '40대_매출', '50대_매출', '60대이상_매출']
colors_age = ['#FF6B6B', '#FFE66D', '#4ECDC4', '#45B7D1', '#95A5A6']
for col, color in zip(age_cols, colors_age):
    values = cust_sorted3[col].values / 1e9
    ax.bar(cust_sorted3['상권_명'], values, bottom=bottom, label=col.replace('_매출', ''), color=color)
    bottom += values
ax.set_ylabel('매출 (십억 원)', fontsize=14, fontweight='bold')
ax.set_title('B3. 상권별 연령대별 매출 분포', fontsize=16, fontweight='bold', pad=15)
ax.set_xticklabels(cust_sorted3['상권_명'], rotation=45, ha='right', fontsize=10)
ax.legend(loc='upper right', fontsize=10, frameon=False)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'B3_연령대별_매출.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

customer_data.to_csv(RAW_DATA_DIR / 'B_고객수요_상세.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 4. 차원 3: 인구 유동 분석
# =============================================================================
print("\n[4/8] 인구 유동 분석 중...")

# 상주인구
res_latest = df_resident[df_resident['기준_년분기_코드'] == df_resident['기준_년분기_코드'].max()]
res_data = res_latest.groupby('상권_코드_명').agg({
    '총_상주인구_수': 'sum', '남성_상주인구_수': 'sum', '여성_상주인구_수': 'sum',
    '연령대_20_상주인구_수': 'sum', '연령대_30_상주인구_수': 'sum', '연령대_40_상주인구_수': 'sum'
}).reset_index()
res_data['타겟_상주인구'] = res_data['연령대_20_상주인구_수'] + res_data['연령대_30_상주인구_수'] + res_data['연령대_40_상주인구_수']
res_data.columns = ['상권_명', '총_상주인구', '남성_상주', '여성_상주', '20대_상주', '30대_상주', '40대_상주', '타겟_상주인구']

# 직장인구
work_latest = df_worker[df_worker['기준_년분기_코드'] == df_worker['기준_년분기_코드'].max()]
work_data = work_latest.groupby('상권_코드_명').agg({
    '총_직장_인구_수': 'sum',
    '연령대_20_직장_인구_수': 'sum', '연령대_30_직장_인구_수': 'sum', '연령대_40_직장_인구_수': 'sum'
}).reset_index()
work_data['타겟_직장인구'] = work_data['연령대_20_직장_인구_수'] + work_data['연령대_30_직장_인구_수'] + work_data['연령대_40_직장_인구_수']
work_data.columns = ['상권_명', '총_직장인구', '20대_직장', '30대_직장', '40대_직장', '타겟_직장인구']

# 유동인구
float_latest = df_floating[df_floating['기준_년분기_코드'] == df_floating['기준_년분기_코드'].max()]
float_data = float_latest.groupby('상권_코드_명').agg({
    '총_유동인구_수': 'sum', '남성_유동인구_수': 'sum', '여성_유동인구_수': 'sum',
    '연령대_20_유동인구_수': 'sum', '연령대_30_유동인구_수': 'sum', '연령대_40_유동인구_수': 'sum'
}).reset_index()
float_data['타겟_유동인구'] = float_data['연령대_20_유동인구_수'] + float_data['연령대_30_유동인구_수'] + float_data['연령대_40_유동인구_수']
float_data.columns = ['상권_명', '총_유동인구', '남성_유동', '여성_유동', '20대_유동', '30대_유동', '40대_유동', '타겟_유동인구']

# 통합
pop_data = res_data.merge(work_data, on='상권_명', how='left').merge(float_data, on='상권_명', how='left').fillna(0)

# 차트 C1: 유동인구 총량
fig, ax = plt.subplots(figsize=(14, 8))
pop_sorted = pop_data.sort_values('총_유동인구', ascending=True)
bars = ax.barh(pop_sorted['상권_명'], pop_sorted['총_유동인구'] / 1e6, color='#4ECDC4', edgecolor='white')
ax.set_xlabel('유동인구 (백만 명)', fontsize=14, fontweight='bold')
ax.set_title('C1. 상권별 유동인구 규모', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, pop_sorted['총_유동인구']):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{v/1e6:.1f}백만', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'C1_유동인구.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 C2: 타겟 유동인구 (20-40대)
fig, ax = plt.subplots(figsize=(14, 8))
pop_sorted2 = pop_data.sort_values('타겟_유동인구', ascending=True)
bars = ax.barh(pop_sorted2['상권_명'], pop_sorted2['타겟_유동인구'] / 1e6, color='#FF6B6B', edgecolor='white')
ax.set_xlabel('타겟 유동인구 (백만 명)', fontsize=14, fontweight='bold')
ax.set_title('C2. 상권별 타겟 유동인구 (20-40대)', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, pop_sorted2['타겟_유동인구']):
    ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2, f'{v/1e6:.1f}백만', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'C2_타겟_유동인구.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 C3: 직장인구
fig, ax = plt.subplots(figsize=(14, 8))
pop_sorted3 = pop_data.sort_values('총_직장인구', ascending=True)
bars = ax.barh(pop_sorted3['상권_명'], pop_sorted3['총_직장인구'] / 1e4, color='#45B7D1', edgecolor='white')
ax.set_xlabel('직장인구 (만 명)', fontsize=14, fontweight='bold')
ax.set_title('C3. 상권별 직장인구 규모', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, pop_sorted3['총_직장인구']):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{v/1e4:.1f}만', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'C3_직장인구.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 C4: 상주인구
fig, ax = plt.subplots(figsize=(14, 8))
pop_sorted4 = pop_data.sort_values('총_상주인구', ascending=True)
bars = ax.barh(pop_sorted4['상권_명'], pop_sorted4['총_상주인구'] / 1e3, color='#96CEB4', edgecolor='white')
ax.set_xlabel('상주인구 (천 명)', fontsize=14, fontweight='bold')
ax.set_title('C4. 상권별 상주인구 규모', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, pop_sorted4['총_상주인구']):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{v/1e3:.1f}천', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'C4_상주인구.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

pop_data.to_csv(RAW_DATA_DIR / 'C_인구유동_상세.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 5. 차원 4: 입지 조건 분석
# =============================================================================
print("\n[5/8] 입지 조건 분석 중...")

# 집객시설
fac_latest = df_facility[df_facility['기준_년분기_코드'] == df_facility['기준_년분기_코드'].max()]
fac_data = fac_latest.groupby('상권_코드_명').agg({
    '집객시설_수': 'sum', '지하철_역_수': 'sum', '버스_정거장_수': 'sum',
    '은행_수': 'sum', '일반_병원_수': 'sum', '약국_수': 'sum'
}).reset_index()
fac_data.columns = ['상권_명', '집객시설_총합', '지하철역', '버스정거장', '은행', '병원', '약국']

# 소득/소비
income_latest = df_income[df_income['기준_년분기_코드'] == df_income['기준_년분기_코드'].max()]
income_data = income_latest.groupby('상권_코드_명').agg({
    '월_평균_소득_금액': 'mean', '의료비_지출_총금액': 'sum', '지출_총금액': 'sum'
}).reset_index()
income_data.columns = ['상권_명', '평균소득', '의료비지출', '총지출']

# 통합
loc_data = fac_data.merge(income_data, on='상권_명', how='left').fillna(0)

# 차트 D1: 집객시설 수
fig, ax = plt.subplots(figsize=(14, 8))
loc_sorted = loc_data.sort_values('집객시설_총합', ascending=True)
bars = ax.barh(loc_sorted['상권_명'], loc_sorted['집객시설_총합'], color='#FFE66D', edgecolor='white')
ax.set_xlabel('집객시설 수 (개)', fontsize=14, fontweight='bold')
ax.set_title('D1. 상권별 집객시설 현황', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, loc_sorted['집객시설_총합']):
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{int(v)}개', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'D1_집객시설.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 D2: 평균 소득
fig, ax = plt.subplots(figsize=(14, 8))
loc_sorted2 = loc_data.sort_values('평균소득', ascending=True)
bars = ax.barh(loc_sorted2['상권_명'], loc_sorted2['평균소득'] / 1e4, color='#4ECDC4', edgecolor='white')
ax.set_xlabel('월 평균 소득 (만 원)', fontsize=14, fontweight='bold')
ax.set_title('D2. 상권별 평균 소득 수준', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, loc_sorted2['평균소득']):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, f'{v/1e4:.0f}만원', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'D2_평균소득.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 D3: 의료비 지출
fig, ax = plt.subplots(figsize=(14, 8))
loc_sorted3 = loc_data.sort_values('의료비지출', ascending=True)
bars = ax.barh(loc_sorted3['상권_명'], loc_sorted3['의료비지출'] / 1e8, color='#FF6B6B', edgecolor='white')
ax.set_xlabel('의료비 지출 (억 원)', fontsize=14, fontweight='bold')
ax.set_title('D3. 상권별 의료비 지출 현황', fontsize=16, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, v in zip(bars, loc_sorted3['의료비지출']):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{v/1e8:.1f}억', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'D3_의료비지출.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

loc_data.to_csv(RAW_DATA_DIR / 'D_입지조건_상세.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 6. 종합 평가
# =============================================================================
print("\n[6/8] 종합 평가 산출 중...")

# 통합 결과
results = competition_total.copy()
results = results.merge(customer_data[['상권_명', '타겟_매출', '여성_매출', '전체_매출']], on='상권_명', how='left')
results = results.merge(pop_data[['상권_명', '총_유동인구', '타겟_유동인구', '총_직장인구', '총_상주인구']], on='상권_명', how='left')
results = results.merge(loc_data[['상권_명', '집객시설_총합', '평균소득', '의료비지출']], on='상권_명', how='left')

# 정규화 및 점수 산출
def normalize(series):
    if series.max() == series.min():
        return pd.Series([1.0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())

results['경쟁_점수'] = 1 - normalize(results['경쟁_점포수'])
results['타겟매출_N'] = normalize(results['타겟_매출'])
results['여성매출_N'] = normalize(results['여성_매출'])
results['고객_점수'] = (results['타겟매출_N'] * 0.6 + results['여성매출_N'] * 0.4)
results['유동_N'] = normalize(results['총_유동인구'])
results['타겟유동_N'] = normalize(results['타겟_유동인구'])
results['직장_N'] = normalize(results['총_직장인구'])
results['상주_N'] = normalize(results['총_상주인구'])
results['인구_점수'] = (results['유동_N'] * 0.4 + results['타겟유동_N'] * 0.3 + results['직장_N'] * 0.2 + results['상주_N'] * 0.1)
results['시설_N'] = normalize(results['집객시설_총합'])
results['소득_N'] = normalize(results['평균소득'])
results['의료비_N'] = normalize(results['의료비지출'])
results['입지_점수'] = (results['시설_N'] * 0.4 + results['소득_N'] * 0.3 + results['의료비_N'] * 0.3)
results['종합점수'] = (results['경쟁_점수'] * 0.20 + results['고객_점수'] * 0.40 + results['인구_점수'] * 0.20 + results['입지_점수'] * 0.20) * 100
results = results.sort_values('종합점수', ascending=False).reset_index(drop=True)
results['순위'] = range(1, len(results) + 1)

# 차트 E1: 종합 점수 순위
fig, ax = plt.subplots(figsize=(14, 8))
res_sorted = results.sort_values('종합점수', ascending=True)
colors = ['#FF6B6B' if r <= 3 else '#4ECDC4' if r <= 6 else '#95A5A6' for r in res_sorted['순위']]
bars = ax.barh(res_sorted['상권_명'], res_sorted['종합점수'], color=colors, edgecolor='white')
ax.set_xlabel('종합 점수 (100점 만점)', fontsize=14, fontweight='bold')
ax.set_title('E1. 강남 9개 상권 종합 평가 순위', fontsize=18, fontweight='bold', pad=20)
ax.set_xlim(0, 100)
ax.grid(axis='x', alpha=0.3, linestyle='--')
for bar, score, rank in zip(bars, res_sorted['종합점수'], res_sorted['순위']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{score:.1f}점 ({int(10-rank+1)}위)', va='center', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(CHART_DIR / 'E1_종합점수_순위.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 E2: TOP 3 레이더
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
ax.set_title('E2. TOP 3 상권 4차원 프로파일', size=18, y=1.08, fontweight='bold')
plt.tight_layout()
plt.savefig(CHART_DIR / 'E2_레이더_TOP3.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 차트 E3: 차원별 히트맵
fig, ax = plt.subplots(figsize=(14, 10))
heatmap_cols = ['경쟁_점수', '타겟매출_N', '여성매출_N', '유동_N', '타겟유동_N', '직장_N', '상주_N', '시설_N', '소득_N', '의료비_N']
heatmap_labels = ['경쟁(역산)', '타겟매출', '여성매출', '유동인구', '타겟유동', '직장인구', '상주인구', '집객시설', '평균소득', '의료비지출']
heatmap_data = results[['상권_명'] + heatmap_cols].set_index('상권_명')
heatmap_data.columns = heatmap_labels
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax, vmin=0, vmax=1,
            linewidths=0.5, annot_kws={'size': 10, 'fontweight': 'bold'})
ax.set_title('E3. 상권별 세부 지표 히트맵', fontsize=16, fontweight='bold', pad=15)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
plt.tight_layout()
plt.savefig(CHART_DIR / 'E3_세부지표_히트맵.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 전체 결과 저장
results.to_csv(RAW_DATA_DIR / 'E_종합평가_전체.csv', index=False, encoding='utf-8-sig')

# =============================================================================
# 7. 요약 출력
# =============================================================================
print("\n[7/8] 요약...")
print("\n" + "=" * 80)
print("세부 지표 완전 시각화 완료")
print("=" * 80)
print(f"\n생성된 차트: {len(list(CHART_DIR.glob('*.png')))}개")
print(f"생성된 로데이터: {len(list(RAW_DATA_DIR.glob('*.csv')))}개")
print(f"\n저장 경로: {OUTPUT_DIR}")

# =============================================================================
# 8. 목차 생성
# =============================================================================
print("\n[8/8] 목차 생성 중...")

toc = """
# 분석 보고서 목차

## A. 경쟁 환경 분석 (가중치 20%)
- A1. 상권별 경쟁 강도 (의원/피부과 점포 수)

## B. 고객 수요 분석 (가중치 40%)
- B1. 상권별 타겟 고객(20-40대) 매출
- B2. 상권별 성별 매출 비교 (여성 vs 남성)
- B3. 상권별 연령대별 매출 분포

## C. 인구 유동 분석 (가중치 20%)
- C1. 상권별 유동인구 규모
- C2. 상권별 타겟 유동인구 (20-40대)
- C3. 상권별 직장인구 규모
- C4. 상권별 상주인구 규모

## D. 입지 조건 분석 (가중치 20%)
- D1. 상권별 집객시설 현황
- D2. 상권별 평균 소득 수준
- D3. 상권별 의료비 지출 현황

## E. 종합 평가
- E1. 강남 9개 상권 종합 평가 순위
- E2. TOP 3 상권 4차원 프로파일
- E3. 상권별 세부 지표 히트맵
"""

with open(OUTPUT_DIR / '00_목차.txt', 'w', encoding='utf-8') as f:
    f.write(toc)

print("\n완료!")
