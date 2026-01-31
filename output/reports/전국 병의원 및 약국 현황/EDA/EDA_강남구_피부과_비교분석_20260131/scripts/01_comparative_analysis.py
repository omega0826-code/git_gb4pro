"""
강남구 피부과 비교 분석 - 메인 스크립트
작성일: 2026-01-31
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 색상 팔레트
COLORS = {
    '강남구': '#E74C3C',
    '서초구': '#3498DB',
    '송파구': '#2ECC71',
    '중구': '#F39C12',
    '마포구': '#9B59B6',
    '서울평균': '#95A5A6'
}

print("="*60)
print("강남구 피부과 비교 분석 시작")
print("="*60)

# ============================================================================
# 1. 데이터 로드
# ============================================================================
print("\n[1/5] 데이터 로드 중...")

df = pd.read_csv('d:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/data_260131_0844/서울_병원_통합_2025.12.csv', encoding='utf-8-sig')
print(f"[OK] 서울 전체 병원: {len(df):,}개")
print(f"[OK] 컬럼 수: {len(df.columns)}개")

# ============================================================================
# 2. 데이터 전처리
# ============================================================================
print("\n[2/5] 데이터 전처리 중...")

# 비교 대상 구
target_districts = ['강남구', '서초구', '송파구', '중구', '마포구']

# 진료과목 컬럼 확인
dept_cols = [col for col in df.columns if '진료과목' in col]
print(f"[OK] 진료과목 관련 컬럼: {dept_cols}")

# 진료과목 데이터 확인 (여러 컬럼 확인)
has_derma = pd.Series([False] * len(df))
for col in dept_cols:
    if df[col].dtype == 'object':
        has_derma |= df[col].fillna('').str.contains('피부과', na=False)

df['피부과_여부'] = has_derma

# 통계
gangnam_total = len(df[df['시군구코드명']=='강남구'])
gangnam_derma = len(df[(df['시군구코드명']=='강남구') & (df['피부과_여부']==True)])

print(f"[OK] 강남구 전체 병원: {gangnam_total:,}개")
print(f"[OK] 강남구 피부과: {gangnam_derma:,}개 ({gangnam_derma/gangnam_total*100:.1f}%)")

# ============================================================================
# 3. 기본 현황 비교
# ============================================================================
print("\n[3/5] 기본 현황 비교 분석 중...")

# 3.1 구별 전체 병원 수
district_counts = df[df['시군구코드명'].isin(target_districts)]['시군구코드명'].value_counts()
district_counts = district_counts.reindex(target_districts)

# 3.2 구별 피부과 병원 수
derma_counts = df[(df['시군구코드명'].isin(target_districts)) & 
                   (df['피부과_여부']==True)]['시군구코드명'].value_counts()
derma_counts = derma_counts.reindex(target_districts, fill_value=0)

# 3.3 피부과 비율
derma_ratio = (derma_counts / district_counts * 100).round(1)

# 결과 저장
comparison_df = pd.DataFrame({
    '전체_병원수': district_counts,
    '피부과_병원수': derma_counts,
    '피부과_비율(%)': derma_ratio
})

comparison_df.to_csv('data/구별_피부과_통계.csv', encoding='utf-8-sig')
print(f"[OK] 구별 통계 저장 완료")

# ============================================================================
# 4. 시각화
# ============================================================================
print("\n[4/5] 시각화 생성 중...")

# 4.1 구별 전체 병원 수 비교
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(district_counts.index, district_counts.values,
               color=[COLORS.get(x, '#95A5A6') for x in district_counts.index])

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title(f'구별 전체 병원 수 비교 (N={district_counts.sum():,})', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_ylabel('병원 수', fontsize=12)
ax.set_xlabel('구', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/01_구별_병원수_비교.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 1/3 생성 완료")

# 4.2 구별 피부과 병원 수 및 비율
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 피부과 병원 수
bars1 = ax1.bar(derma_counts.index, derma_counts.values,
                color=[COLORS.get(x, '#95A5A6') for x in derma_counts.index])

for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_title(f'구별 피부과 병원 수 (N={derma_counts.sum():,})', 
              fontsize=14, fontweight='bold')
ax1.set_ylabel('피부과 병원 수', fontsize=12)
ax1.set_xlabel('구', fontsize=12)

# 피부과 비율
bars2 = ax2.bar(derma_ratio.index, derma_ratio.values,
                color=[COLORS.get(x, '#95A5A6') for x in derma_ratio.index])

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_title('구별 피부과 비율 (전체 병원 대비)', fontsize=14, fontweight='bold')
ax2.set_ylabel('피부과 비율 (%)', fontsize=12)
ax2.set_xlabel('구', fontsize=12)
ax2.axhline(y=derma_ratio.mean(), color='red', linestyle='--', 
            label=f'평균: {derma_ratio.mean():.1f}%', linewidth=2)
ax2.legend()

plt.tight_layout()
plt.savefig('charts/02_구별_피부과_비교.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 2/3 생성 완료")

# 4.3 강남구 vs 서울 평균 비교
seoul_total = len(df)
seoul_derma = len(df[df['피부과_여부']==True])
seoul_ratio = seoul_derma / seoul_total * 100

comparison_data = pd.DataFrame({
    '구분': ['강남구', '서울 평균'],
    '전체 병원': [gangnam_total, seoul_total / 25],  # 25개 구 평균
    '피부과 병원': [gangnam_derma, seoul_derma / 25],
    '피부과 비율(%)': [gangnam_derma/gangnam_total*100, seoul_ratio]
})

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, col in enumerate(['전체 병원', '피부과 병원', '피부과 비율(%)']):
    ax = axes[idx]
    bars = ax.bar(comparison_data['구분'], comparison_data[col],
                   color=['#E74C3C', '#95A5A6'])
    
    for bar in bars:
        height = bar.get_height()
        if col == '피부과 비율(%)':
            label = f'{height:.1f}%'
        else:
            label = f'{int(height):,}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_title(col, fontsize=13, fontweight='bold')
    ax.set_ylabel(col.split('(')[0], fontsize=11)

plt.suptitle('강남구 vs 서울 평균 비교', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('charts/03_강남구_vs_서울평균.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 3/3 생성 완료")

# ============================================================================
# 5. 핵심 인사이트 도출
# ============================================================================
print("\n[5/5] 핵심 인사이트 도출 중...")

insights = []

# 인사이트 1: 강남구 피부과 집중도
gangnam_ratio_value = gangnam_derma / gangnam_total * 100
seoul_avg_ratio = seoul_ratio
concentration = gangnam_ratio_value / seoul_avg_ratio

insights.append(f"1. 강남구 피부과 집중도는 서울 평균 대비 **{concentration:.1f}배** 높음")
insights.append(f"   - 강남구: {gangnam_ratio_value:.1f}% vs 서울 평균: {seoul_avg_ratio:.1f}%")

# 인사이트 2: 구별 순위
derma_rank = derma_counts.rank(ascending=False)
gangnam_rank = int(derma_rank['강남구'])

insights.append(f"\n2. 강남구는 비교 대상 5개 구 중 피부과 병원 수 **{gangnam_rank}위**")
insights.append(f"   - 강남구: {gangnam_derma:,}개")

# 인사이트 3: 비율 비교
highest_ratio_district = derma_ratio.idxmax()
highest_ratio_value = derma_ratio.max()

if highest_ratio_district == '강남구':
    insights.append(f"\n3. 강남구는 피부과 비율이 **가장 높은 구** ({highest_ratio_value:.1f}%)")
else:
    insights.append(f"\n3. 피부과 비율은 {highest_ratio_district}가 가장 높음 ({highest_ratio_value:.1f}%)")
    insights.append(f"   - 강남구는 {gangnam_ratio_value:.1f}%로 {highest_ratio_value - gangnam_ratio_value:.1f}%p 차이")

# 결과 저장
with open('data/핵심_인사이트.txt', 'w', encoding='utf-8') as f:
    f.write("강남구 피부과 비교 분석 - 핵심 인사이트\n")
    f.write("="*60 + "\n\n")
    for insight in insights:
        f.write(insight + "\n")

print("\n" + "="*60)
print("분석 완료!")
print("="*60)
print(f"\n생성된 산출물:")
print(f"  - 데이터: data/구별_피부과_통계.csv")
print(f"  - 차트: charts/ (3개)")
print(f"  - 인사이트: data/핵심_인사이트.txt")

# 핵심 인사이트 출력
print(f"\n[핵심 인사이트]")
for insight in insights:
    print(insight)
