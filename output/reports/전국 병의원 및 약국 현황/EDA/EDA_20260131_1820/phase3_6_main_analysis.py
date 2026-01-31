"""
Phase 3-6: 주요 섹션 통합 분석
- 인력 분석 (섹션 3.1)
- 병상 규모 분석 (섹션 3.2)
- 진료과목 분석 (섹션 3.5)
- 병원 규모 및 연령대 분석 (섹션 3.6)
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

# ============================================================================
# Phase 3: 인력 분석 (섹션 3.1)
# ============================================================================
print_log("\n" + "="*80)
print_log("[Phase 3] 인력 분석 (섹션 3.1)")
print_log("="*80)

print_log("\n[3.1.1] 의과전문의 수 분석")
specialist_stats = df['의과전문의 인원수'].describe()
print_log(f"  평균: {specialist_stats['mean']:.2f}명")
print_log(f"  중앙값: {specialist_stats['50%']:.2f}명")
print_log(f"  최대: {specialist_stats['max']:.0f}명")

# 1인 vs 다인 의원
one_person = (df['의과전문의 인원수'] == 1).sum()
multi_person = (df['의과전문의 인원수'] > 1).sum()
zero_person = (df['의과전문의 인원수'] == 0).sum()

print_log(f"\n  의과전문의 보유 현황:")
print_log(f"  - 0명: {zero_person:,}개 ({zero_person/len(df)*100:.1f}%)")
print_log(f"  - 1명 (1인 의원): {one_person:,}개 ({one_person/len(df)*100:.1f}%)")
print_log(f"  - 2명 이상: {multi_person:,}개 ({multi_person/len(df)*100:.1f}%)")

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 히스토그램
ax1.hist(df[df['의과전문의 인원수'] <= 20]['의과전문의 인원수'], bins=20, color='#3498db', edgecolor='black')
ax1.set_xlabel('의과전문의 수', fontsize=12)
ax1.set_ylabel('병원 수', fontsize=12)
ax1.set_title(f'의과전문의 수 분포 (20명 이하, N={len(df):,})', fontsize=13, fontweight='bold')

# 파이 차트
labels = ['0명', '1명', '2명 이상']
sizes = [zero_person, one_person, multi_person]
colors = ['#95a5a6', '#3498db', '#e74c3c']
ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax2.set_title(f'의과전문의 보유 현황 (N={len(df):,})', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\05_specialist_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 05_specialist_analysis.png")

# ============================================================================
# Phase 4: 병상 규모 분석 (섹션 3.2)
# ============================================================================
print_log("\n" + "="*80)
print_log("[Phase 4] 병상 규모 분석 (섹션 3.2)")
print_log("="*80)

print_log("\n[3.2.1] 일반병상 분석")
general_bed_has = (df['일반입원실일반병상수'] > 0).sum()
general_bed_none = (df['일반입원실일반병상수'] == 0).sum()
print_log(f"  - 보유: {general_bed_has:,}개 ({general_bed_has/len(df)*100:.1f}%)")
print_log(f"  - 미보유: {general_bed_none:,}개 ({general_bed_none/len(df)*100:.1f}%)")
print_log(f"  - 평균 병상수: {df[df['일반입원실일반병상수']>0]['일반입원실일반병상수'].mean():.1f}개")

print_log("\n[3.2.2] 상급병상 분석")
premium_bed_has = (df['일반입원실상급병상수'] > 0).sum()
premium_bed_none = (df['일반입원실상급병상수'] == 0).sum()
print_log(f"  - 보유: {premium_bed_has:,}개 ({premium_bed_has/len(df)*100:.1f}%)")
print_log(f"  - 미보유: {premium_bed_none:,}개 ({premium_bed_none/len(df)*100:.1f}%)")
print_log(f"  - 평균 병상수: {df[df['일반입원실상급병상수']>0]['일반입원실상급병상수'].mean():.1f}개")

# 시각화
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))

# 일반병상 파이 차트
ax1.pie([general_bed_none, general_bed_has], labels=['미보유', '보유'], 
        autopct='%1.1f%%', colors=['#95a5a6', '#3498db'], startangle=90)
ax1.set_title(f'일반병상 보유 현황 (N={len(df):,})', fontsize=12, fontweight='bold')

# 상급병상 파이 차트
ax2.pie([premium_bed_none, premium_bed_has], labels=['미보유', '보유'], 
        autopct='%1.1f%%', colors=['#95a5a6', '#e74c3c'], startangle=90)
ax2.set_title(f'상급병상 보유 현황 (N={len(df):,})', fontsize=12, fontweight='bold')

# 일반병상 분포
ax3.hist(df[df['일반입원실일반병상수'] <= 100]['일반입원실일반병상수'], 
         bins=20, color='#3498db', edgecolor='black')
ax3.set_xlabel('일반병상 수', fontsize=11)
ax3.set_ylabel('병원 수', fontsize=11)
ax3.set_title(f'일반병상 수 분포 (100개 이하)', fontsize=12, fontweight='bold')

# 상급병상 분포
ax4.hist(df[df['일반입원실상급병상수'] <= 50]['일반입원실상급병상수'], 
         bins=20, color='#e74c3c', edgecolor='black')
ax4.set_xlabel('상급병상 수', fontsize=11)
ax4.set_ylabel('병원 수', fontsize=11)
ax4.set_title(f'상급병상 수 분포 (50개 이하)', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\06_bed_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 06_bed_analysis.png")

# ============================================================================
# Phase 5: 진료과목 분석 (섹션 3.5)
# ============================================================================
print_log("\n" + "="*80)
print_log("[Phase 5] 진료과목 분석 (섹션 3.5)")
print_log("="*80)

print_log("\n[3.5.1] 진료과목 개수 분석")
dept_count_dist = df['진료과목_개수'].value_counts().sort_index()
print_log(f"  평균 진료과목 수: {df['진료과목_개수'].mean():.2f}개")
print_log(f"  중앙값: {df['진료과목_개수'].median():.0f}개")
print_log(f"  최대: {df['진료과목_개수'].max():.0f}개")

single_dept = (df['진료과목_개수'] == 1).sum()
multi_dept = (df['진료과목_개수'] > 1).sum()
print_log(f"\n  - 단일 과목: {single_dept:,}개 ({single_dept/len(df)*100:.1f}%)")
print_log(f"  - 다과목 운영: {multi_dept:,}개 ({multi_dept/len(df)*100:.1f}%)")

# 주요 진료과목 TOP 10
print_log("\n[3.5.2] 주요 진료과목 TOP 10")
dept_cols = [col for col in df.columns if col.startswith('진료과목_') and col != '진료과목_개수']
dept_counts = {}
for col in dept_cols:
    dept_name = col.replace('진료과목_', '')
    count = df[col].sum()
    if count > 0:
        dept_counts[dept_name] = count

top10_depts = sorted(dept_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (dept, count) in enumerate(top10_depts, 1):
    pct = count / len(df) * 100
    print_log(f"  {i}. {dept}: {count:,}개 ({pct:.1f}%)")

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 진료과목 개수 분포
ax1.hist(df['진료과목_개수'], bins=range(0, int(df['진료과목_개수'].max())+2), 
         color='#2ecc71', edgecolor='black')
ax1.set_xlabel('진료과목 수', fontsize=12)
ax1.set_ylabel('병원 수', fontsize=12)
ax1.set_title(f'진료과목 개수 분포 (N={len(df):,})', fontsize=13, fontweight='bold')

# TOP 10 진료과목
depts = [d[0] for d in top10_depts]
counts = [d[1] for d in top10_depts]
bars = ax2.barh(range(len(depts)), counts, color='#2ecc71')
ax2.set_yticks(range(len(depts)))
ax2.set_yticklabels(depts)
ax2.set_xlabel('병원 수', fontsize=12)
ax2.set_title(f'주요 진료과목 TOP 10 (N={len(df):,})', fontsize=13, fontweight='bold')
ax2.invert_yaxis()

for i, (bar, count) in enumerate(zip(bars, counts)):
    pct = count / len(df) * 100
    ax2.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2, 
            f'{count:,} ({pct:.1f}%)', ha='left', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\07_department_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 07_department_analysis.png")

# ============================================================================
# Phase 6: 병원 규모 및 연령대 분석 (섹션 3.6)
# ============================================================================
print_log("\n" + "="*80)
print_log("[Phase 6] 병원 규모 및 연령대 분석 (섹션 3.6)")
print_log("="*80)

print_log("\n[3.6.1] 병원연령대 분석")
age_dist = df['병원연령대'].value_counts()
age_order = ['신규 (5년 미만)', '성장기 (5-10년)', '중견 (10-20년)', '성숙 (20-30년)', '노포 (30년 이상)']
age_dist = age_dist.reindex(age_order, fill_value=0)

for age_cat, count in age_dist.items():
    pct = count / len(df) * 100
    print_log(f"  - {age_cat}: {count:,}개 ({pct:.1f}%)")

print_log("\n[3.6.2] 병원규모 분석")
size_dist = df['병원규모'].value_counts()
size_order = ['소형', '중소형', '중형', '대형']
size_dist = size_dist.reindex(size_order, fill_value=0)

for size_cat, count in size_dist.items():
    pct = count / len(df) * 100
    print_log(f"  - {size_cat}: {count:,}개 ({pct:.1f}%)")

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 병원연령대
bars1 = ax1.bar(range(len(age_dist)), age_dist.values, color='#9b59b6')
ax1.set_xticks(range(len(age_dist)))
ax1.set_xticklabels([a.split(' ')[0] for a in age_dist.index], rotation=45, ha='right')
ax1.set_ylabel('병원 수', fontsize=12)
ax1.set_title(f'병원연령대 분포 (N={len(df):,})', fontsize=13, fontweight='bold')

for i, (bar, count) in enumerate(zip(bars1, age_dist.values)):
    pct = count / len(df) * 100
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
            f'{count:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

# 병원규모
bars2 = ax2.bar(range(len(size_dist)), size_dist.values, color='#f39c12')
ax2.set_xticks(range(len(size_dist)))
ax2.set_xticklabels(size_dist.index)
ax2.set_ylabel('병원 수', fontsize=12)
ax2.set_title(f'병원규모 분포 (N={len(df):,})', fontsize=13, fontweight='bold')

for i, (bar, count) in enumerate(zip(bars2, size_dist.values)):
    pct = count / len(df) * 100
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
            f'{count:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR + r'\08_age_size_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print_log("  시각화 저장: 08_age_size_analysis.png")

print_log("\nPhase 3-6 완료: 주요 섹션 통합 분석")
print_log("="*80)

log.close()
print(f"\n로그 파일 업데이트 완료")
