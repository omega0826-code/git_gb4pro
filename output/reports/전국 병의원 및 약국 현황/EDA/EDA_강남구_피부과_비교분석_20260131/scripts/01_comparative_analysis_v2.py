"""
강남구 피부과 비교 분석 - 수정된 메인 스크립트
작성일: 2026-01-31
수정: 원본 진료과목 데이터에서 피부과 추출
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
print("강남구 피부과 비교 분석 시작 (수정 버전)")
print("="*60)

# ============================================================================
# 1. 데이터 로드
# ============================================================================
print("\n[1/6] 데이터 로드 중...")

# 병원 기본 정보
df_hospital = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/1.병원정보서비스(2025.12.).csv', 
                          encoding='utf-8-sig')
print(f"[OK] 전국 병원 정보: {len(df_hospital):,}개")

# 진료과목 정보 (1:N 관계)
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
                      encoding='utf-8-sig')
print(f"[OK] 진료과목 정보: {len(df_dept):,}개 레코드")

# ============================================================================
# 2. 서울 + 피부과 필터링
# ============================================================================
print("\n[2/6] 서울 + 피부과 데이터 필터링 중...")

# 서울 병원만 추출
seoul_hospitals = df_hospital[df_hospital['시도코드명']=='서울'].copy()
print(f"[OK] 서울 병원: {len(seoul_hospitals):,}개")

# 피부과 진료과목 추출
derma_dept = df_dept[df_dept['진료과목코드명']=='피부과'].copy()
print(f"[OK] 전국 피부과 레코드: {len(derma_dept):,}개")

# 서울 피부과 병원 (병합)
seoul_derma = seoul_hospitals.merge(
    derma_dept[['암호화요양기호', '진료과목코드명']],
    on='암호화요양기호',
    how='inner'
)
print(f"[OK] 서울 피부과 병원: {len(seoul_derma):,}개")

# ============================================================================
# 3. 구별 통계 계산
# ============================================================================
print("\n[3/6] 구별 통계 계산 중...")

# 비교 대상 구
target_districts = ['강남구', '서초구', '송파구', '중구', '마포구']

# 3.1 구별 전체 병원 수
district_counts = seoul_hospitals[seoul_hospitals['시군구코드명'].isin(target_districts)]['시군구코드명'].value_counts()
district_counts = district_counts.reindex(target_districts)

# 3.2 구별 피부과 병원 수
derma_counts = seoul_derma[seoul_derma['시군구코드명'].isin(target_districts)]['시군구코드명'].value_counts()
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
print("\n구별 통계:")
print(comparison_df)

# ============================================================================
# 4. 시각화
# ============================================================================
print("\n[4/6] 시각화 생성 중...")

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
seoul_total = len(seoul_hospitals)
seoul_derma_total = len(seoul_derma)
seoul_ratio = seoul_derma_total / seoul_total * 100

gangnam_total = int(district_counts['강남구'])
gangnam_derma = int(derma_counts['강남구'])
gangnam_ratio = gangnam_derma / gangnam_total * 100

comparison_data = pd.DataFrame({
    '구분': ['강남구', '서울 평균'],
    '전체 병원': [gangnam_total, seoul_total / 25],  # 25개 구 평균
    '피부과 병원': [gangnam_derma, seoul_derma_total / 25],
    '피부과 비율(%)': [gangnam_ratio, seoul_ratio]
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
print("\n[5/6] 핵심 인사이트 도출 중...")

insights = []

# 인사이트 1: 강남구 피부과 집중도
concentration = gangnam_ratio / seoul_ratio

insights.append(f"1. 강남구 피부과 집중도는 서울 평균 대비 **{concentration:.2f}배** 높음")
insights.append(f"   - 강남구: {gangnam_ratio:.1f}% vs 서울 평균: {seoul_ratio:.1f}%")

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
    insights.append(f"   - 강남구는 {gangnam_ratio:.1f}%로 {highest_ratio_value - gangnam_ratio:.1f}%p 차이")

# 결과 저장
with open('data/핵심_인사이트.txt', 'w', encoding='utf-8') as f:
    f.write("강남구 피부과 비교 분석 - 핵심 인사이트\n")
    f.write("="*60 + "\n\n")
    for insight in insights:
        f.write(insight + "\n")

# ============================================================================
# 6. 강남구 피부과 병원 리스트 저장
# ============================================================================
print("\n[6/6] 강남구 피부과 병원 리스트 저장 중...")

gangnam_derma_list = seoul_derma[seoul_derma['시군구코드명']=='강남구'].copy()
gangnam_derma_list.to_csv('data/강남구_피부과_병원_리스트.csv', encoding='utf-8-sig', index=False)
print(f"[OK] 강남구 피부과 병원 {len(gangnam_derma_list):,}개 저장 완료")

print("\n" + "="*60)
print("분석 완료!")
print("="*60)
print(f"\n생성된 산출물:")
print(f"  - 데이터: data/구별_피부과_통계.csv")
print(f"  - 데이터: data/강남구_피부과_병원_리스트.csv")
print(f"  - 차트: charts/ (3개)")
print(f"  - 인사이트: data/핵심_인사이트.txt")

# 핵심 인사이트 출력
print(f"\n[핵심 인사이트]")
for insight in insights:
    print(insight)
