"""
Phase 2: 기본 현황 분석 (섹션 3.0)
- 종별 분포
- 시군구별 분포
- 설립구분 분포
- 개설연도 분포
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 스타일 설정
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 경로 설정
OUTPUT_DIR = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\EDA\EDA_20260131_1820'
LOG_FILE = OUTPUT_DIR + r'\analysis_log.txt'

# 로그 파일 열기
log = open(LOG_FILE, 'a', encoding='utf-8')

def print_log(msg):
    print(msg)
    log.write(msg + '\n')
    log.flush()

# 데이터 로딩
df = pd.read_pickle(OUTPUT_DIR + r'\df_loaded.pkl')

print_log("\n" + "="*80)
print_log("[Phase 2] 기본 현황 분석 (섹션 3.0)")
print_log("="*80)

# 3.0.1 종별 분포
print_log("\n[3.0.1] 종별 분포 분석")
type_dist = df['종별코드명'].value_counts()
print_log(f"  총 {len(df):,}개 병의원")
for type_name, count in type_dist.items():
    pct = count / len(df) * 100
    print_log(f"  - {type_name}: {count:,}개 ({pct:.1f}%)")

# 시각화
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(range(len(type_dist)), type_dist.values, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
ax.set_xticks(range(len(type_dist)))
ax.set_xticklabels(type_dist.index, rotation=0)
ax.set_ylabel('병원 수', fontsize=12)
ax.set_title(f'종별 분포 (N={len(df):,})', fontsize=14, fontweight='bold')

# 빈도수 표시
for i, (bar, count) in enumerate(zip(bars, type_dist.values)):
    pct = count / len(df) * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
            f'{count:,}\n({pct:.1f}%)', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\01_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 01_type_distribution.png")

# 3.0.2 시군구별 분포
print_log("\n[3.0.2] 시군구별 분포 분석")
district_dist = df['시군구코드명'].value_counts().head(10)
print_log(f"  상위 10개 자치구:")
for district, count in district_dist.items():
    pct = count / len(df) * 100
    print_log(f"  - {district}: {count:,}개 ({pct:.1f}%)")

# 시각화
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(range(len(district_dist)), district_dist.values, color='#3498db')
ax.set_yticks(range(len(district_dist)))
ax.set_yticklabels(district_dist.index)
ax.set_xlabel('병원 수', fontsize=12)
ax.set_title(f'시군구별 병원 수 (상위 10개, N={len(df):,})', fontsize=14, fontweight='bold')
ax.invert_yaxis()

# 빈도수 표시
for i, (bar, count) in enumerate(zip(bars, district_dist.values)):
    pct = count / len(df) * 100
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
            f'{count:,} ({pct:.1f}%)', 
            ha='left', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\02_district_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 02_district_distribution.png")

# 3.0.3 설립구분 분포
print_log("\n[3.0.3] 설립구분 분포 분석")
establish_dist = df['설립구분코드명'].value_counts()
print_log(f"  설립구분별 분포:")
for est_type, count in establish_dist.items():
    pct = count / len(df) * 100
    print_log(f"  - {est_type}: {count:,}개 ({pct:.1f}%)")

# 시각화
fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'][:len(establish_dist)]
wedges, texts, autotexts = ax.pie(establish_dist.values, labels=establish_dist.index, 
                                    autopct='%1.1f%%', colors=colors, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)
ax.set_title(f'설립구분 분포 (N={len(df):,})', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\03_establish_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 03_establish_distribution.png")

# 3.0.4 개설연도 분포
print_log("\n[3.0.4] 개설연도 분포 분석")
year_dist = df['설립연도'].value_counts().sort_index()
print_log(f"  개설연도 범위: {df['설립연도'].min():.0f}년 ~ {df['설립연도'].max():.0f}년")
print_log(f"  평균 개설연도: {df['설립연도'].mean():.0f}년")
print_log(f"  중앙값: {df['설립연도'].median():.0f}년")

# 연대별 집계
decade_bins = [1900, 1980, 1990, 2000, 2010, 2020, 2030]
decade_labels = ['~1979', '1980s', '1990s', '2000s', '2010s', '2020s']
df['연대'] = pd.cut(df['설립연도'], bins=decade_bins, labels=decade_labels, right=False)
decade_dist = df['연대'].value_counts().sort_index()

print_log(f"\n  연대별 분포:")
for decade, count in decade_dist.items():
    pct = count / len(df) * 100
    print_log(f"  - {decade}: {count:,}개 ({pct:.1f}%)")

# 시각화
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(df['설립연도'].dropna(), bins=50, color='#3498db', edgecolor='black', alpha=0.7)
ax.set_xlabel('개설연도', fontsize=12)
ax.set_ylabel('병원 수', fontsize=12)
ax.set_title(f'개설연도 분포 (N={len(df):,})', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\04_year_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 04_year_distribution.png")

print_log("\nPhase 2 완료: 기본 현황 분석")
print_log("="*80)

log.close()
print(f"\n로그 파일 업데이트 완료")
