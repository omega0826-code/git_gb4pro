# -*- coding: utf-8 -*-
"""
강남구 전체 병원 EDA 분석 스크립트
================================================================================
작성일: 2026-01-27
목적: 강남구 전체 병원 데이터(N=1,153)에 대한 포괄적 EDA 수행
가이드라인: EDA_병원전체정보_강남구_병원현황 가이드라인 v1.00.md
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
OUTPUT_DIR = BASE_DIR / "EDA" / "EDA260127"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("강남구 전체 병원 EDA 분석")
print("=" * 80)
print(f"데이터 파일: {DATA_FILE}")
print(f"출력 경로: {OUTPUT_DIR}")
print()

# ============================================================================
# 1. 데이터 로드 및 품질 확인
# ============================================================================
print("[1] 데이터 로드 및 품질 확인")
df = pd.read_csv(DATA_FILE, encoding='utf-8')
print(f"  - 전체 병원 수: {len(df):,}개")
print(f"  - 전체 컬럼 수: {len(df.columns)}개")
print()

# 결측치 분석
missing_summary = []
for col in df.columns:
    missing_count = df[col].isna().sum()
    missing_pct = (missing_count / len(df)) * 100
    if missing_count > 0:
        missing_summary.append({
            '컬럼명': col,
            '결측수': missing_count,
            '결측비율(%)': round(missing_pct, 1)
        })

missing_df = pd.DataFrame(missing_summary)
if len(missing_df) > 0:
    missing_df = missing_df.sort_values('결측수', ascending=False)
    missing_df.to_csv(OUTPUT_DIR / 'quality_report.csv', index=False, encoding='utf-8-sig')
    print(f"  - 결측치 보고서 저장: quality_report.csv")
print()

# ============================================================================
# 2. 기관 유형 분석
# ============================================================================
print("[2] 기관 유형 분석")

# 2.1 기관 유형별 분포
if 'eqp_orgTyCdNm' in df.columns:
    org_type_counts = df['eqp_orgTyCdNm'].value_counts()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(org_type_counts)), org_type_counts.values, color='steelblue')
    ax.set_xticks(range(len(org_type_counts)))
    ax.set_xticklabels(org_type_counts.index, rotation=45, ha='right')
    ax.set_title(f'기관 유형별 분포 (N={len(df):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('기관 유형', fontsize=12)
    ax.set_ylabel('병원 수', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    # 빈도수 표시
    for i, (bar, count) in enumerate(zip(bars, org_type_counts.values)):
        pct = (count / len(df)) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'org_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 기관 유형별 분포 저장: org_type_distribution.png")

# 2.2 종별 코드 분포
if 'eqp_clCdNm' in df.columns:
    class_counts = df['eqp_clCdNm'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(range(len(class_counts)), class_counts.values, color='coral')
    ax.set_xticks(range(len(class_counts)))
    ax.set_xticklabels(class_counts.index, rotation=45, ha='right')
    ax.set_title(f'종별 코드 분포 (N={len(df):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('종별', fontsize=12)
    ax.set_ylabel('병원 수', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    for i, (bar, count) in enumerate(zip(bars, class_counts.values)):
        pct = (count / len(df)) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'class_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 종별 코드 분포 저장: class_distribution.png")
print()

# ============================================================================
# 3. 진료과목 분석
# ============================================================================
print("[3] 진료과목 분석")

if 'dgsbjt_dgsbjtCdNm' in df.columns:
    # 진료과목 데이터 정제
    dept_data = df['dgsbjt_dgsbjtCdNm'].dropna()
    dept_counts = dept_data.value_counts()
    
    # Top 15 진료과목
    top_15_depts = dept_counts.head(15)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.barh(range(len(top_15_depts)), top_15_depts.values, color='mediumseagreen')
    ax.set_yticks(range(len(top_15_depts)))
    ax.set_yticklabels(top_15_depts.index)
    ax.set_title(f'Top 15 진료과목 분포 (N={len(dept_data):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('병원 수', fontsize=12)
    ax.set_ylabel('진료과목', fontsize=12)
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()
    
    for i, (bar, count) in enumerate(zip(bars, top_15_depts.values)):
        pct = (count / len(dept_data)) * 100
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{count} ({pct:.1f}%)', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'department_top15.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - Top 15 진료과목 분포 저장: department_top15.png")
    
    # 진료과목 전체 리스트 저장
    dept_full = pd.DataFrame({
        '진료과목': dept_counts.index,
        '병원수': dept_counts.values,
        '비율(%)': (dept_counts.values / len(dept_data) * 100).round(1)
    })
    dept_full.to_csv(OUTPUT_DIR / 'department_full_list.csv', index=False, encoding='utf-8-sig')
    print(f"  - 진료과목 전체 리스트 저장: department_full_list.csv")
print()

# ============================================================================
# 4. 인력 분석
# ============================================================================
print("[4] 인력 분석")

if 'dgsbjt_dgsbjtPrSdrCnt' in df.columns:
    staff_data = df['dgsbjt_dgsbjtPrSdrCnt'].dropna()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bins = [0, 1, 2, 3, 5, 10, 20, 50, 100, staff_data.max()+1]
    counts, edges, patches = ax.hist(staff_data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
    
    ax.set_title(f'전문의 수 분포 (N={len(staff_data):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('전문의 수', fontsize=12)
    ax.set_ylabel('병원 수', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    # 빈도수 표시
    for i, (count, edge) in enumerate(zip(counts, edges[:-1])):
        if count > 0:
            pct = (count / len(staff_data)) * 100
            ax.text(edge + (edges[i+1] - edge)/2, count + 5,
                    f'{int(count)}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'staff_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 전문의 수 분포 저장: staff_distribution.png")
    print(f"  - 평균 전문의 수: {staff_data.mean():.2f}명")
    print(f"  - 중앙값: {staff_data.median():.1f}명")
print()

# ============================================================================
# 5. 병상 규모 분석
# ============================================================================
print("[5] 병상 규모 분석")

if 'eqp_stdSickbdCnt' in df.columns:
    bed_data = df['eqp_stdSickbdCnt'].fillna(0)
    bed_categories = pd.cut(bed_data, bins=[-1, 0, 10, 30, 50, 100, bed_data.max()+1],
                            labels=['없음', '1-10개', '11-30개', '31-50개', '51-100개', '100개 이상'])
    bed_counts = bed_categories.value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(bed_counts)), bed_counts.values, color='lightcoral')
    ax.set_xticks(range(len(bed_counts)))
    ax.set_xticklabels(bed_counts.index, rotation=45, ha='right')
    ax.set_title(f'병상 규모 분포 (N={len(df):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('병상 수', fontsize=12)
    ax.set_ylabel('병원 수', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    for i, (bar, count) in enumerate(zip(bars, bed_counts.values)):
        pct = (count / len(df)) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'bed_scale.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 병상 규모 분포 저장: bed_scale.png")
print()

# ============================================================================
# 6. 주말 진료 분석
# ============================================================================
print("[6] 주말 진료 분석")

weekend_summary = []
if 'dtl_rcvSat' in df.columns:
    sat_count = df['dtl_rcvSat'].notna().sum()
    sat_pct = (sat_count / len(df)) * 100
    weekend_summary.append({'구분': '토요일 진료', '병원수': sat_count, '비율(%)': round(sat_pct, 1)})

if 'dtl_trmtSunStart' in df.columns:
    sun_count = df['dtl_trmtSunStart'].notna().sum()
    sun_pct = (sun_count / len(df)) * 100
    weekend_summary.append({'구분': '일요일 진료', '병원수': sun_count, '비율(%)': round(sun_pct, 1)})

if weekend_summary:
    weekend_df = pd.DataFrame(weekend_summary)
    weekend_df.to_csv(OUTPUT_DIR / 'weekend_summary.csv', index=False, encoding='utf-8-sig')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(weekend_df['구분'], weekend_df['병원수'], color=['steelblue', 'coral'])
    ax.set_title(f'주말 진료 현황 (N={len(df):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('병원 수', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    for bar, row in zip(bars, weekend_df.itertuples()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{row.병원수}\n({row._3}%)', ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'weekend_operations.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 주말 진료 현황 저장: weekend_operations.png")
print()

# ============================================================================
# 7. 입지 분석 - 행정동
# ============================================================================
print("[7] 입지 분석 - 행정동")

if 'eqp_emdongNm' in df.columns:
    dong_data = df['eqp_emdongNm'].dropna()
    dong_counts = dong_data.value_counts().head(15)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.barh(range(len(dong_counts)), dong_counts.values, color='mediumpurple')
    ax.set_yticks(range(len(dong_counts)))
    ax.set_yticklabels(dong_counts.index)
    ax.set_title(f'Top 15 행정동별 병원 분포 (N={len(dong_data):,})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('병원 수', fontsize=12)
    ax.set_ylabel('행정동', fontsize=12)
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()
    
    for i, (bar, count) in enumerate(zip(bars, dong_counts.values)):
        pct = (count / len(dong_data)) * 100
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{count} ({pct:.1f}%)', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'location_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  - 행정동별 분포 저장: location_distribution.png")
print()

# ============================================================================
# 8. 좌표 데이터 품질 확인
# ============================================================================
print("[8] 좌표 데이터 품질 확인")

if 'lat' in df.columns and 'lon' in df.columns:
    coord_valid = df[['lat', 'lon']].notna().all(axis=1).sum()
    coord_pct = (coord_valid / len(df)) * 100
    print(f"  - 좌표 데이터 보유: {coord_valid:,}개 ({coord_pct:.1f}%)")
print()

# ============================================================================
# 9. 의료 장비 분석
# ============================================================================
print("[9] 의료 장비 분석")

if 'medoft_oftCdNm' in df.columns:
    equip_data = df['medoft_oftCdNm'].dropna()
    equip_counts = equip_data.value_counts().head(15)
    
    if len(equip_counts) > 0:
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.barh(range(len(equip_counts)), equip_counts.values, color='gold')
        ax.set_yticks(range(len(equip_counts)))
        ax.set_yticklabels(equip_counts.index)
        ax.set_title(f'Top 15 의료장비 보유 현황 (데이터 보유: {len(equip_data):,}개)', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('보유 병원 수', fontsize=12)
        ax.set_ylabel('장비명', fontsize=12)
        ax.grid(axis='x', alpha=0.3)
        ax.invert_yaxis()
        
        for i, (bar, count) in enumerate(zip(bars, equip_counts.values)):
            pct = (count / len(df)) * 100
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                    f'{count} ({pct:.1f}%)', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'equipment_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  - 의료장비 분석 저장: equipment_analysis.png")
        
        # 전체 장비 리스트 저장
        equip_full = pd.DataFrame({
            '장비명': equip_data.value_counts().index,
            '보유병원수': equip_data.value_counts().values
        })
        equip_full.to_csv(OUTPUT_DIR / 'equipment_full_list.csv', index=False, encoding='utf-8-sig')
        print(f"  - 장비 전체 리스트 저장: equipment_full_list.csv")
print()

print("=" * 80)
print("EDA 분석 완료")
print(f"모든 결과물이 {OUTPUT_DIR}에 저장되었습니다.")
print("=" * 80)
