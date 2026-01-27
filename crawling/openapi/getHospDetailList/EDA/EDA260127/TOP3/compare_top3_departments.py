# -*- coding: utf-8 -*-
"""
TOP3 진료과목 비교 분석 스크립트
================================================================================
작성일: 2026-01-27
목적: 피부과 중심의 TOP3 진료과목(성형외과, 피부과, 내과) 비교 분석
분석 대상: 성형외과(412), 피부과(333), 내과(300) = 총 1,045개
================================================================================
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

# ============================================================================
# 경로 설정
# ============================================================================
BASE_DIR = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList")
DATA_FILE = BASE_DIR / "data" / "병원전체정보_20260116_212603_geocoded_20260125_164059.csv"
OUTPUT_DIR = BASE_DIR / "EDA" / "EDA260127" / "TOP3"
VIZ_DIR = OUTPUT_DIR / "visualizations"
DATA_DIR = OUTPUT_DIR / "data"

# 디렉토리 생성
VIZ_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 색상 정의 (피부과 강조)
COLORS = {
    '피부과': '#2E86DE',      # 파란색 (메인)
    '성형외과': '#FF6B6B',    # 주황/빨강
    '내과': '#95A5A6'         # 회색
}

print("=" * 80)
print("TOP3 진료과목 비교 분석 (피부과 중심)")
print("=" * 80)
print(f"데이터 파일: {DATA_FILE}")
print(f"출력 경로: {OUTPUT_DIR}")
print()

# ============================================================================
# 데이터 로드 및 필터링
# ============================================================================
print("[1] 데이터 로드 및 TOP3 필터링")
df = pd.read_csv(DATA_FILE, encoding='utf-8')
print(f"  - 전체 병원 수: {len(df):,}개")

# TOP3 진료과목 필터링
top3_df = df[df['dgsbjt_dgsbjtCdNm'].isin(['성형외과', '피부과', '내과'])].copy()
print(f"  - TOP3 병원 수: {len(top3_df):,}개")

# 과목별 개수
dept_counts = top3_df['dgsbjt_dgsbjtCdNm'].value_counts()
for dept, count in dept_counts.items():
    pct = (count / len(top3_df)) * 100
    print(f"    - {dept}: {count}개 ({pct:.1f}%)")
print()

# ============================================================================
# 2. 인력 구조 비교
# ============================================================================
print("[2] 인력 구조 비교")

# 2.1 전문의 수 분포 비교
if 'dgsbjt_dgsbjtPrSdrCnt' in top3_df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 히스토그램 오버레이
    ax1 = axes[0]
    for dept in ['피부과', '성형외과', '내과']:
        data = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]['dgsbjt_dgsbjtPrSdrCnt'].dropna()
        ax1.hist(data, bins=range(0, 11), alpha=0.6, label=f'{dept} (N={len(data)})', 
                 color=COLORS[dept], edgecolor='black')
    
    ax1.set_title('전문의 수 분포 비교', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('전문의 수', fontsize=12)
    ax1.set_ylabel('병원 수', fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # 1인 의원 비율
    ax2 = axes[1]
    solo_ratios = []
    for dept in ['피부과', '성형외과', '내과']:
        data = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]['dgsbjt_dgsbjtPrSdrCnt'].dropna()
        solo_ratio = (data <= 1).sum() / len(data) * 100
        solo_ratios.append(solo_ratio)
    
    bars = ax2.bar(['피부과', '성형외과', '내과'], solo_ratios, 
                    color=[COLORS['피부과'], COLORS['성형외과'], COLORS['내과']])
    ax2.set_title('1인 의원 비율 비교', fontsize=16, fontweight='bold', pad=20)
    ax2.set_ylabel('비율 (%)', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, ratio in zip(bars, solo_ratios):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{ratio:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'staff_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 인력 구조 비교 저장: staff_comparison.png")

# ============================================================================
# 3. 병상 보유율 비교
# ============================================================================
print("[3] 병상 보유율 비교")

if 'eqp_stdSickbdCnt' in top3_df.columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 병상 보유율
    ax1 = axes[0]
    bed_ratios = []
    for dept in ['피부과', '성형외과', '내과']:
        dept_data = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]
        has_bed = (dept_data['eqp_stdSickbdCnt'].fillna(0) > 0).sum()
        ratio = (has_bed / len(dept_data)) * 100
        bed_ratios.append(ratio)
    
    bars = ax1.bar(['피부과', '성형외과', '내과'], bed_ratios,
                    color=[COLORS['피부과'], COLORS['성형외과'], COLORS['내과']])
    ax1.set_title('병상 보유율 비교', fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('보유율 (%)', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, ratio in zip(bars, bed_ratios):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{ratio:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 병상 수 분포 (박스플롯)
    ax2 = axes[1]
    bed_data = []
    labels = []
    for dept in ['피부과', '성형외과', '내과']:
        data = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]['eqp_stdSickbdCnt'].fillna(0)
        data = data[data > 0]  # 병상 있는 경우만
        if len(data) > 0:
            bed_data.append(data)
            labels.append(f'{dept}\n(N={len(data)})')
    
    if bed_data:
        bp = ax2.boxplot(bed_data, labels=labels, patch_artist=True)
        for patch, dept in zip(bp['boxes'], ['피부과', '성형외과', '내과']):
            patch.set_facecolor(COLORS[dept])
            patch.set_alpha(0.7)
        
        ax2.set_title('병상 수 분포 (보유 병원만)', fontsize=16, fontweight='bold', pad=20)
        ax2.set_ylabel('병상 수', fontsize=12)
        ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'bed_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 병상 비교 저장: bed_comparison.png")

# ============================================================================
# 4. 지역 분포 비교
# ============================================================================
print("[4] 지역 분포 비교")

if 'eqp_emdongNm' in top3_df.columns:
    # 상위 10개 행정동
    top_dongs = top3_df['eqp_emdongNm'].value_counts().head(10).index
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    
    # 행정동별 분포
    ax1 = axes[0]
    dong_data = []
    for dong in top_dongs:
        dong_counts = []
        for dept in ['피부과', '성형외과', '내과']:
            count = len(top3_df[(top3_df['eqp_emdongNm'] == dong) & 
                                (top3_df['dgsbjt_dgsbjtCdNm'] == dept)])
            dong_counts.append(count)
        dong_data.append(dong_counts)
    
    x = np.arange(len(top_dongs))
    width = 0.25
    
    ax1.bar(x - width, [d[0] for d in dong_data], width, label='피부과', color=COLORS['피부과'])
    ax1.bar(x, [d[1] for d in dong_data], width, label='성형외과', color=COLORS['성형외과'])
    ax1.bar(x + width, [d[2] for d in dong_data], width, label='내과', color=COLORS['내과'])
    
    ax1.set_title('Top 10 행정동별 진료과목 분포', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('행정동', fontsize=12)
    ax1.set_ylabel('병원 수', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(top_dongs, rotation=45, ha='right')
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # 상권 유형별 분포 (핵심 상권 vs 기타)
    ax2 = axes[1]
    core_areas = ['역삼동', '신사동', '청담동', '논현동', '대치동']
    
    area_data = []
    for dept in ['피부과', '성형외과', '내과']:
        dept_df = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]
        core_count = len(dept_df[dept_df['eqp_emdongNm'].isin(core_areas)])
        other_count = len(dept_df[~dept_df['eqp_emdongNm'].isin(core_areas)])
        area_data.append([core_count, other_count])
    
    x = np.arange(3)
    width = 0.35
    
    ax2.bar(x, [d[0] for d in area_data], width, label='핵심 상권', 
            color=[COLORS['피부과'], COLORS['성형외과'], COLORS['내과']], alpha=0.8)
    ax2.bar(x, [d[1] for d in area_data], width, bottom=[d[0] for d in area_data],
            label='기타 지역', color=[COLORS['피부과'], COLORS['성형외과'], COLORS['내과']], alpha=0.4)
    
    ax2.set_title('상권 유형별 분포', fontsize=16, fontweight='bold', pad=20)
    ax2.set_ylabel('병원 수', fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(['피부과', '성형외과', '내과'])
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    # 비율 표시
    for i, data in enumerate(area_data):
        total = sum(data)
        core_pct = (data[0] / total) * 100
        ax2.text(i, total + 5, f'{core_pct:.1f}%\n핵심상권', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'location_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 지역 분포 비교 저장: location_comparison.png")

# ============================================================================
# 5. 주말 진료 비교
# ============================================================================
print("[5] 주말 진료 비교")

fig, ax = plt.subplots(figsize=(12, 6))

weekend_data = []
for dept in ['피부과', '성형외과', '내과']:
    dept_df = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]
    sat_ratio = (dept_df['dtl_rcvSat'].notna().sum() / len(dept_df)) * 100
    sun_ratio = (dept_df['dtl_trmtSunStart'].notna().sum() / len(dept_df)) * 100
    weekend_data.append([sat_ratio, sun_ratio])

x = np.arange(3)
width = 0.35

bars1 = ax.bar(x - width/2, [d[0] for d in weekend_data], width, label='토요일 진료',
               color=[COLORS['피부과'], COLORS['성형외과'], COLORS['내과']], alpha=0.8)
bars2 = ax.bar(x + width/2, [d[1] for d in weekend_data], width, label='일요일 진료',
               color=[COLORS['피부과'], COLORS['성형외과'], COLORS['내과']], alpha=0.5)

ax.set_title('주말 진료율 비교', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('진료율 (%)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(['피부과', '성형외과', '내과'])
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# 비율 표시
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    ax.text(bar1.get_x() + bar1.get_width()/2, bar1.get_height() + 0.3,
            f'{weekend_data[i][0]:.1f}%', ha='center', va='bottom', fontsize=10)
    ax.text(bar2.get_x() + bar2.get_width()/2, bar2.get_height() + 0.3,
            f'{weekend_data[i][1]:.1f}%', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(VIZ_DIR / 'weekend_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  - 주말 진료 비교 저장: weekend_comparison.png")

# ============================================================================
# 6. 요약 통계 생성
# ============================================================================
print("[6] 요약 통계 생성")

summary_data = []
for dept in ['피부과', '성형외과', '내과']:
    dept_df = top3_df[top3_df['dgsbjt_dgsbjtCdNm'] == dept]
    
    # 기본 통계
    total = len(dept_df)
    
    # 전문의 수
    avg_staff = dept_df['dgsbjt_dgsbjtPrSdrCnt'].mean()
    solo_ratio = (dept_df['dgsbjt_dgsbjtPrSdrCnt'].fillna(0) <= 1).sum() / total * 100
    
    # 병상
    bed_ratio = (dept_df['eqp_stdSickbdCnt'].fillna(0) > 0).sum() / total * 100
    
    # 주말 진료
    sat_ratio = dept_df['dtl_rcvSat'].notna().sum() / total * 100
    sun_ratio = dept_df['dtl_trmtSunStart'].notna().sum() / total * 100
    
    # 핵심 상권
    core_areas = ['역삼동', '신사동', '청담동', '논현동', '대치동']
    core_ratio = dept_df['eqp_emdongNm'].isin(core_areas).sum() / total * 100
    
    summary_data.append({
        '진료과목': dept,
        '병원수': total,
        '평균전문의수': round(avg_staff, 2),
        '1인의원비율(%)': round(solo_ratio, 1),
        '병상보유율(%)': round(bed_ratio, 1),
        '토요일진료율(%)': round(sat_ratio, 1),
        '일요일진료율(%)': round(sun_ratio, 1),
        '핵심상권비율(%)': round(core_ratio, 1)
    })

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(DATA_DIR / 'top3_summary.csv', index=False, encoding='utf-8-sig')
print(f"  - 요약 통계 저장: top3_summary.csv")
print()

print("=" * 80)
print("TOP3 비교 분석 완료!")
print(f"시각화 파일: {VIZ_DIR}")
print(f"데이터 파일: {DATA_DIR}")
print("=" * 80)
