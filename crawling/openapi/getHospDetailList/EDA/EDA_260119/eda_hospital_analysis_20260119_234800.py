"""
병원 데이터 탐색적 데이터 분석 (EDA)
분석 대상: 병원전체정보_결측치처리완료_20260119_233319.csv
작성 일시: 2026-01-19 23:48
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 타임스탬프
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
print("=" * 80)
print("병원 데이터 탐색적 데이터 분석 (EDA)")
print("=" * 80)

# ============================================================================
# Phase 1: 데이터 로드 및 기본 정보 확인
# ============================================================================
print("\n[Phase 1] 데이터 로드 중...")
data_path = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_결측치처리완료_20260119_233319.csv'
df = pd.read_csv(data_path, encoding='utf-8-sig')

print(f"  - 데이터 건수: {len(df):,}건")
print(f"  - 컬럼 수: {len(df.columns)}개")
print(f"  - 결측치 총합: {df.isnull().sum().sum():,}개")
print(f"  - 메모리 사용량: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ============================================================================
# Phase 2: 파생 변수 생성 (프로젝트 규칙 적용)
# ============================================================================
print("\n[Phase 2] 파생 변수 생성 중...")

# 1. 전문의 구분
df['의사유형'] = df['dgsbjt_dgsbjtPrSdrCnt'].apply(
    lambda x: '전문의' if x > 0 else '일반의'
)
print(f"  - 의사유형 생성 완료")

# 2. 병원 규모 분류
df['총의사수'] = df['dgsbjt_cdiagDrCnt'] + df['dgsbjt_dgsbjtPrSdrCnt']
df['병원규모'] = df['총의사수'].apply(
    lambda x: 'Type A (대형)' if x >= 5 
    else ('Type B (중형)' if x >= 2 else 'Type C (1인)')
)
print(f"  - 병원규모 생성 완료")

# 3. 야간 진료 여부 (간단한 버전)
# 진료 시간 데이터가 복잡하므로 일단 기본 분류만
df['수술가능'] = df['eqp_soprmCnt'].apply(
    lambda x: '수술가능' if x >= 1 else '시술중심'
)
print(f"  - 수술가능 여부 생성 완료")

# ============================================================================
# Phase 3: 기본 통계 분석
# ============================================================================
print("\n[Phase 3] 기본 통계 분석 중...")

# 1. 전체 데이터 개요
overview = {
    '총 병원 수': int(len(df)),
    '행정동 수': int(df['eqp_emdongNm'].nunique()),
    '진료과목 수': int(df['dgsbjt_dgsbjtCdNm'].nunique()),
    '평균 병상 수': float(df['eqp_stdSickbdCnt'].mean()),
    '평균 직원 수': float(df['eqp_emymCnt'].mean()),
    '평균 의사 수': float(df['총의사수'].mean())
}

print("\n  [전체 데이터 개요]")
for key, value in overview.items():
    if isinstance(value, float):
        print(f"    - {key}: {value:.2f}")
    else:
        print(f"    - {key}: {value:,}")

# 2. 병원 유형별 분포
type_dist = df['의사유형'].value_counts()
scale_dist = df['병원규모'].value_counts()
surgery_dist = df['수술가능'].value_counts()

print("\n  [병원 유형별 분포]")
print(f"    전문의: {type_dist.get('전문의', 0)}건 ({type_dist.get('전문의', 0)/len(df)*100:.1f}%)")
print(f"    일반의: {type_dist.get('일반의', 0)}건 ({type_dist.get('일반의', 0)/len(df)*100:.1f}%)")

print("\n  [병원 규모별 분포]")
for scale, count in scale_dist.items():
    print(f"    {scale}: {count}건 ({count/len(df)*100:.1f}%)")

# 3. 행정동별 분포
district_dist = df.groupby('eqp_emdongNm').size().sort_values(ascending=False)
print(f"\n  [행정동별 분포] (상위 10개)")
for i, (dong, count) in enumerate(district_dist.head(10).items(), 1):
    print(f"    {i}. {dong}: {count}건")

# 4. 행정동별 평균 지표
district_stats = df.groupby('eqp_emdongNm').agg({
    'eqp_stdSickbdCnt': 'mean',
    'eqp_emymCnt': 'mean',
    '총의사수': 'mean'
}).round(2)

# ============================================================================
# Phase 4: 시각화
# ============================================================================
print("\n[Phase 4] 시각화 생성 중...")
output_dir = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_260119'

# 1. 병원 유형 분포
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1-1. 전문의 vs 일반의
type_dist.plot(kind='bar', ax=axes[0], color=['#2E86AB', '#A23B72'])
axes[0].set_title('전문의 vs 일반의 분포', fontsize=14, fontweight='bold')
axes[0].set_xlabel('의사 유형', fontsize=12)
axes[0].set_ylabel('병원 수', fontsize=12)
axes[0].tick_params(axis='x', rotation=0)
for i, v in enumerate(type_dist):
    axes[0].text(i, v + 5, str(v), ha='center', fontsize=11, fontweight='bold')

# 1-2. 병원 규모
scale_dist.plot(kind='bar', ax=axes[1], color=['#F18F01', '#C73E1D', '#6A994E'])
axes[1].set_title('병원 규모 분포', fontsize=14, fontweight='bold')
axes[1].set_xlabel('병원 규모', fontsize=12)
axes[1].set_ylabel('병원 수', fontsize=12)
axes[1].tick_params(axis='x', rotation=15)
for i, v in enumerate(scale_dist):
    axes[1].text(i, v + 5, str(v), ha='center', fontsize=11, fontweight='bold')

# 1-3. 수술 가능 여부
surgery_dist.plot(kind='bar', ax=axes[2], color=['#06A77D', '#D4A373'])
axes[2].set_title('수술 인프라 보유 현황', fontsize=14, fontweight='bold')
axes[2].set_xlabel('수술 가능 여부', fontsize=12)
axes[2].set_ylabel('병원 수', fontsize=12)
axes[2].tick_params(axis='x', rotation=0)
for i, v in enumerate(surgery_dist):
    axes[2].text(i, v + 5, str(v), ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/barplot_hospital_type_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: barplot_hospital_type_{timestamp}.png")
plt.close()

# 2. 행정동별 분포
fig, ax = plt.subplots(figsize=(14, 10))
district_dist.plot(kind='barh', ax=ax, color='#4A90E2')
ax.set_title('강남구 행정동별 병원 분포', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('병원 수', fontsize=13)
ax.set_ylabel('행정동', fontsize=13)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# 값 표시
for i, v in enumerate(district_dist):
    ax.text(v + 1, i, str(v), va='center', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/barplot_district_dist_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: barplot_district_dist_{timestamp}.png")
plt.close()

# 3. 행정동별 평균 지표 (상위 15개 동)
top_districts = district_dist.head(15).index
district_stats_top = district_stats.loc[top_districts]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 3-1. 평균 병상 수
district_stats_top['eqp_stdSickbdCnt'].plot(kind='barh', ax=axes[0], color='#E63946')
axes[0].set_title('행정동별 평균 병상 수 (상위 15개)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('평균 병상 수', fontsize=11)
axes[0].grid(axis='x', alpha=0.3)

# 3-2. 평균 직원 수
district_stats_top['eqp_emymCnt'].plot(kind='barh', ax=axes[1], color='#457B9D')
axes[1].set_title('행정동별 평균 직원 수 (상위 15개)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('평균 직원 수', fontsize=11)
axes[1].grid(axis='x', alpha=0.3)

# 3-3. 평균 의사 수
district_stats_top['총의사수'].plot(kind='barh', ax=axes[2], color='#2A9D8F')
axes[2].set_title('행정동별 평균 의사 수 (상위 15개)', fontsize=12, fontweight='bold')
axes[2].set_xlabel('평균 의사 수', fontsize=11)
axes[2].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/barplot_district_stats_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: barplot_district_stats_{timestamp}.png")
plt.close()

# 4. 병상 수 분포
fig, ax = plt.subplots(figsize=(12, 6))
df['eqp_stdSickbdCnt'].hist(bins=50, ax=ax, color='#F4A261', edgecolor='black', alpha=0.7)
ax.set_title('병상 수 분포', fontsize=14, fontweight='bold')
ax.set_xlabel('병상 수', fontsize=12)
ax.set_ylabel('병원 수', fontsize=12)
ax.axvline(df['eqp_stdSickbdCnt'].mean(), color='red', linestyle='--', linewidth=2, label=f'평균: {df["eqp_stdSickbdCnt"].mean():.1f}')
ax.axvline(df['eqp_stdSickbdCnt'].median(), color='blue', linestyle='--', linewidth=2, label=f'중앙값: {df["eqp_stdSickbdCnt"].median():.1f}')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}/histogram_bed_count_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: histogram_bed_count_{timestamp}.png")
plt.close()

# 5. 상관관계 히트맵
numeric_cols = ['eqp_stdSickbdCnt', 'eqp_emymCnt', 'dgsbjt_cdiagDrCnt', 
                'dgsbjt_dgsbjtPrSdrCnt', 'eqp_soprmCnt', '총의사수']
fig, ax = plt.subplots(figsize=(10, 8))
correlation = df[numeric_cols].corr()
sns.heatmap(correlation, annot=True, fmt='.2f', cmap='RdYlBu_r', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('주요 변수 상관관계', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(f'{output_dir}/heatmap_correlation_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: heatmap_correlation_{timestamp}.png")
plt.close()

# ============================================================================
# Phase 5: 데이터 및 통계 저장
# ============================================================================
print("\n[Phase 5] 결과 저장 중...")

# 1. 파생 변수 추가된 데이터 저장
output_csv = f'{output_dir}/processed_hospital_with_features_{timestamp}.csv'
df.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"  - 저장: processed_hospital_with_features_{timestamp}.csv")

# 2. 통계 요약 저장
statistics = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'overview': overview,
    'type_distribution': {
        '전문의': int(type_dist.get('전문의', 0)),
        '일반의': int(type_dist.get('일반의', 0))
    },
    'scale_distribution': {k: int(v) for k, v in scale_dist.items()},
    'surgery_distribution': {k: int(v) for k, v in surgery_dist.items()},
    'top_10_districts': {k: int(v) for k, v in district_dist.head(10).items()},
    'district_stats': {
        k: {
            '평균_병상수': float(v['eqp_stdSickbdCnt']),
            '평균_직원수': float(v['eqp_emymCnt']),
            '평균_의사수': float(v['총의사수'])
        } for k, v in district_stats.head(15).iterrows()
    }
}

output_json = f'{output_dir}/statistics_summary_{timestamp}.json'
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(statistics, f, ensure_ascii=False, indent=2)
print(f"  - 저장: statistics_summary_{timestamp}.json")

# ============================================================================
# 완료
# ============================================================================
print("\n" + "=" * 80)
print("[완료] EDA 분석 완료!")
print("=" * 80)
print(f"\n생성된 파일:")
print(f"  1. barplot_hospital_type_{timestamp}.png")
print(f"  2. barplot_district_dist_{timestamp}.png")
print(f"  3. barplot_district_stats_{timestamp}.png")
print(f"  4. histogram_bed_count_{timestamp}.png")
print(f"  5. heatmap_correlation_{timestamp}.png")
print(f"  6. processed_hospital_with_features_{timestamp}.csv")
print(f"  7. statistics_summary_{timestamp}.json")
print(f"\n저장 위치: {output_dir}")
