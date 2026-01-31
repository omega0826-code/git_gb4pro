"""
강남구 피부과 확장 EDA - 시각화 스크립트
작성일: 2026-01-31
스타일: 기본 matplotlib/seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 스타일 설정
sns.set_style("whitegrid")
sns.set_palette("husl")

print("="*80)
print("강남구 피부과 확장 EDA - 시각화")
print("="*80)

# 데이터 로드
data_path = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/EDA/EDA_강남구_피부과_확장분석_20260131/data/강남구_피부과_확장분석_데이터.csv'
df = pd.read_csv(data_path, encoding='utf-8-sig')

print(f"\n데이터 로드 완료: {len(df):,}개 병원")

# 출력 디렉토리
output_dir = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/EDA/EDA_강남구_피부과_확장분석_20260131/charts'
import os
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# 차트 1: 종별 분포 + 다과목 비율
# ============================================================================
print("\n[1/5] 차트 1: 종별 분포 및 다과목 전략...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 종별 분포
type_dist = df['종별코드명'].value_counts()
colors1 = sns.color_palette("Set2", len(type_dist))
bars1 = ax1.bar(range(len(type_dist)), type_dist.values, color=colors1)
ax1.set_xticks(range(len(type_dist)))
ax1.set_xticklabels(type_dist.index, rotation=45, ha='right')
ax1.set_ylabel('병원 수', fontsize=12)
ax1.set_title(f'종별 분포 (N={len(df):,})', fontsize=14, fontweight='bold')

for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}\n({height/len(df)*100:.1f}%)',
             ha='center', va='bottom', fontsize=10)

# 다과목 비율
single_dept = (df['진료과목_개수'] == 1).sum()
multi_dept = (df['진료과목_개수'] > 1).sum()
dept_data = pd.Series({'단일 진료과목': single_dept, '다과목 (2개 이상)': multi_dept})
colors2 = ['#FF6B6B', '#4ECDC4']
wedges, texts, autotexts = ax2.pie(dept_data.values, labels=dept_data.index, autopct='%1.1f%%',
                                     colors=colors2, startangle=90, textprops={'fontsize': 11})
plt.setp(autotexts, size=12, weight="bold")
ax2.set_title('진료과목 수 전략', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/01_종별_다과목_분포.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 1 저장 완료")

# ============================================================================
# 차트 2: 의사 수 분포
# ============================================================================
print("[2/5] 차트 2: 의사 수 분포...")

fig, ax = plt.subplots(figsize=(14, 6))

doctor_dist = df['총의사수'].value_counts().sort_index().head(15)
bars = ax.bar(doctor_dist.index, doctor_dist.values, color='#3498DB', edgecolor='black', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xlabel('의사 수 (명)', fontsize=12)
ax.set_ylabel('병원 수', fontsize=12)
ax.set_title(f'의사 수 분포 (N={len(df):,})', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/02_의사수_분포.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 2 저장 완료")

# ============================================================================
# 차트 3: 영업시간 분석 (야간/주말 진료)
# ============================================================================
print("[3/5] 차트 3: 영업시간 분석...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 야간 진료
night_weekday = (df['진료종료시간_월요일'] >= 2000).sum()
night_saturday = (df['진료종료시간_토요일'] >= 2000).sum()
regular_weekday = len(df) - night_weekday
regular_saturday = len(df) - night_saturday

night_data = pd.DataFrame({
    '구분': ['평일', '평일', '토요일', '토요일'],
    '유형': ['일반 (20시 이전)', '야간 (20시 이후)', '일반 (20시 이전)', '야간 (20시 이후)'],
    '병원수': [regular_weekday, night_weekday, regular_saturday, night_saturday]
})

colors_night = ['#95A5A6', '#E74C3C', '#95A5A6', '#E74C3C']
x_pos = [0, 0.4, 1.2, 1.6]
bars1 = ax1.bar(x_pos, night_data['병원수'], color=colors_night, width=0.35)

for i, bar in enumerate(bars1):
    height = bar.get_height()
    pct = height / len(df) * 100
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax1.set_xticks([0.2, 1.4])
ax1.set_xticklabels(['평일', '토요일'])
ax1.set_ylabel('병원 수', fontsize=12)
ax1.set_title('야간 진료 (20시 이후) 운영 현황', fontsize=14, fontweight='bold')
ax1.legend(['일반', '야간'], loc='upper right')

# 주말 진료
sunday_open = (df['진료시작시간_일요일'] > 0).sum()
sunday_closed = len(df) - sunday_open

weekend_data = pd.Series({'일요일 휴진': sunday_closed, '일요일 진료': sunday_open})
colors_weekend = ['#BDC3C7', '#27AE60']
wedges, texts, autotexts = ax2.pie(weekend_data.values, labels=weekend_data.index, autopct='%1.1f%%',
                                     colors=colors_weekend, startangle=90, textprops={'fontsize': 11})
plt.setp(autotexts, size=12, weight="bold")
ax2.set_title('일요일 진료 현황', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/03_영업시간_분석.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 3 저장 완료")

# ============================================================================
# 차트 4: 주차 및 교통 접근성
# ============================================================================
print("[4/5] 차트 4: 주차 및 교통 접근성...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 주차 가능 여부
parking_yes = (df['주차_가능대수'] > 0).sum()
parking_no = len(df) - parking_yes

parking_data = pd.Series({'주차 불가': parking_no, '주차 가능': parking_yes})
colors_parking = ['#E74C3C', '#2ECC71']
wedges, texts, autotexts = ax1.pie(parking_data.values, labels=parking_data.index, autopct='%1.1f%%',
                                     colors=colors_parking, startangle=90, textprops={'fontsize': 11})
plt.setp(autotexts, size=12, weight="bold")
ax1.set_title(f'주차 가능 여부 (N={len(df):,})', fontsize=14, fontweight='bold')

# 교통편 정보
traffic_yes = (df['교통편_개수'] > 0).sum()
traffic_no = len(df) - traffic_yes

traffic_data = pd.Series({'교통편 정보 없음': traffic_no, '교통편 정보 있음': traffic_yes})
colors_traffic = ['#E74C3C', '#3498DB']
wedges, texts, autotexts = ax2.pie(traffic_data.values, labels=traffic_data.index, autopct='%1.1f%%',
                                     colors=colors_traffic, startangle=90, textprops={'fontsize': 11})
plt.setp(autotexts, size=12, weight="bold")
ax2.set_title(f'대중교통 정보 제공 여부 (N={len(df):,})', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/04_주차_교통_접근성.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 4 저장 완료")

# ============================================================================
# 차트 5: 동별 밀집도
# ============================================================================
print("[5/5] 차트 5: 동별 밀집도...")

fig, ax = plt.subplots(figsize=(14, 8))

dong_dist = df['읍면동'].value_counts().head(15)
colors_dong = sns.color_palette("viridis", len(dong_dist))
bars = ax.barh(range(len(dong_dist)), dong_dist.values, color=colors_dong)

ax.set_yticks(range(len(dong_dist)))
ax.set_yticklabels(dong_dist.index, fontsize=11)
ax.set_xlabel('병원 수', fontsize=12)
ax.set_title(f'동별 피부과 병원 밀집도 (상위 15개, N={len(df):,})', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for i, bar in enumerate(bars):
    width = bar.get_width()
    pct = width / len(df) * 100
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f' {int(width)}개 ({pct:.1f}%)',
            ha='left', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/05_동별_밀집도.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 차트 5 저장 완료")

print("\n" + "="*80)
print("시각화 완료!")
print("="*80)
print(f"저장 위치: {output_dir}")
print("\n생성된 차트:")
print("  1. 01_종별_다과목_분포.png")
print("  2. 02_의사수_분포.png")
print("  3. 03_영업시간_분석.png")
print("  4. 04_주차_교통_접근성.png")
print("  5. 05_동별_밀집도.png")
