import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("강남구 병원 다과목 의원 분포 분석")
print("="*80)

# 1. 데이터 로드
df_hospital = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/1.병원정보서비스(2025.12.).csv',
                          encoding='utf-8-sig')
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
                      encoding='utf-8-sig')

# 2. 강남구 병원 추출
gangnam = df_hospital[df_hospital['시군구코드명']=='강남구'].copy()
print(f"\n[1] 강남구 전체 병원: {len(gangnam):,}개")

# 3. 각 병원의 진료과목 수 계산
dept_count = df_dept.groupby('암호화요양기호').size().reset_index(name='진료과목수')
print(f"[2] 진료과목 정보가 있는 병원: {len(dept_count):,}개")

# 4. 강남구 병원과 병합
gangnam_with_dept = gangnam.merge(dept_count, on='암호화요양기호', how='left')
gangnam_with_dept['진료과목수'] = gangnam_with_dept['진료과목수'].fillna(0).astype(int)

print(f"[3] 강남구 병원 중 진료과목 정보 있음: {(gangnam_with_dept['진료과목수']>0).sum():,}개")
print(f"[4] 강남구 병원 중 진료과목 정보 없음: {(gangnam_with_dept['진료과목수']==0).sum():,}개")

# 5. 기본 통계
print(f"\n{'='*80}")
print(f"진료과목 수 기본 통계")
print(f"{'='*80}")
print(f"  - 평균: {gangnam_with_dept['진료과목수'].mean():.2f}개")
print(f"  - 중앙값: {gangnam_with_dept['진료과목수'].median():.0f}개")
print(f"  - 최빈값: {gangnam_with_dept['진료과목수'].mode()[0]:.0f}개")
print(f"  - 최소: {gangnam_with_dept['진료과목수'].min():.0f}개")
print(f"  - 최대: {gangnam_with_dept['진료과목수'].max():.0f}개")
print(f"  - 표준편차: {gangnam_with_dept['진료과목수'].std():.2f}개")

# 6. 다과목 의원 분류
gangnam_with_dept['병원유형'] = gangnam_with_dept['진료과목수'].apply(
    lambda x: '진료과목 정보 없음' if x == 0 
    else '단일 진료과목' if x == 1 
    else '2-3개 진료과목' if x <= 3 
    else '4-5개 진료과목' if x <= 5 
    else '6-10개 진료과목' if x <= 10 
    else '11개 이상 진료과목'
)

# 7. 병원 유형별 분포
print(f"\n{'='*80}")
print(f"병원 유형별 분포")
print(f"{'='*80}")
type_dist = gangnam_with_dept['병원유형'].value_counts()
for type_name, count in type_dist.items():
    pct = count / len(gangnam_with_dept) * 100
    print(f"  {type_name}: {count:,}개 ({pct:.1f}%)")

# 8. 진료과목 수별 상세 분포
print(f"\n{'='*80}")
print(f"진료과목 수별 상세 분포 (상위 20개)")
print(f"{'='*80}")
dept_count_dist = gangnam_with_dept['진료과목수'].value_counts().sort_index().head(20)
for count, freq in dept_count_dist.items():
    pct = freq / len(gangnam_with_dept) * 100
    print(f"  {count:2d}개 진료과목: {freq:4d}개 병원 ({pct:5.1f}%)")

# 9. 다과목 의원 (2개 이상) 분석
multi_dept = gangnam_with_dept[gangnam_with_dept['진료과목수'] >= 2]
print(f"\n{'='*80}")
print(f"다과목 의원 (2개 이상 진료과목) 분석")
print(f"{'='*80}")
print(f"  - 총 개수: {len(multi_dept):,}개")
print(f"  - 비율: {len(multi_dept)/len(gangnam_with_dept)*100:.1f}%")
print(f"  - 평균 진료과목 수: {multi_dept['진료과목수'].mean():.2f}개")

# 10. 종별코드별 진료과목 수
print(f"\n{'='*80}")
print(f"종별코드별 평균 진료과목 수")
print(f"{'='*80}")
type_dept_avg = gangnam_with_dept.groupby('종별코드명')['진료과목수'].agg(['count', 'mean', 'max'])
type_dept_avg = type_dept_avg.sort_values('mean', ascending=False)
for idx, row in type_dept_avg.iterrows():
    print(f"  {idx}: 평균 {row['mean']:.1f}개 (최대 {row['max']:.0f}개, {row['count']:.0f}개 병원)")

# 11. 시각화
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 11.1 병원 유형별 분포 (파이 차트)
ax1 = axes[0, 0]
type_order = ['진료과목 정보 없음', '단일 진료과목', '2-3개 진료과목', '4-5개 진료과목', '6-10개 진료과목', '11개 이상 진료과목']
type_dist_ordered = type_dist.reindex(type_order, fill_value=0)
colors = ['#CCCCCC', '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
ax1.pie(type_dist_ordered.values, labels=type_dist_ordered.index, autopct='%1.1f%%', 
        colors=colors, startangle=90)
ax1.set_title(f'강남구 병원 유형별 분포 (N={len(gangnam_with_dept):,})', fontsize=14, fontweight='bold')

# 11.2 진료과목 수 분포 (히스토그램)
ax2 = axes[0, 1]
dept_with_info = gangnam_with_dept[gangnam_with_dept['진료과목수'] > 0]
ax2.hist(dept_with_info['진료과목수'], bins=range(0, 31), color='#3498DB', edgecolor='black', alpha=0.7)
ax2.axvline(dept_with_info['진료과목수'].mean(), color='red', linestyle='--', 
            linewidth=2, label=f'평균: {dept_with_info["진료과목수"].mean():.1f}개')
ax2.axvline(dept_with_info['진료과목수'].median(), color='green', linestyle='--', 
            linewidth=2, label=f'중앙값: {dept_with_info["진료과목수"].median():.0f}개')
ax2.set_xlabel('진료과목 수', fontsize=12)
ax2.set_ylabel('병원 수', fontsize=12)
ax2.set_title(f'진료과목 수 분포 (진료과목 정보 있는 병원, N={len(dept_with_info):,})', 
              fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 11.3 진료과목 수별 병원 수 (막대 그래프)
ax3 = axes[1, 0]
top_15 = gangnam_with_dept['진료과목수'].value_counts().sort_index().head(15)
bars = ax3.bar(top_15.index, top_15.values, color='#2ECC71', edgecolor='black')
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=9)
ax3.set_xlabel('진료과목 수', fontsize=12)
ax3.set_ylabel('병원 수', fontsize=12)
ax3.set_title('진료과목 수별 병원 수 (상위 15개)', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

# 11.4 종별코드별 평균 진료과목 수
ax4 = axes[1, 1]
top_types = type_dept_avg.head(10)
bars = ax4.barh(range(len(top_types)), top_types['mean'], color='#F39C12', edgecolor='black')
ax4.set_yticks(range(len(top_types)))
ax4.set_yticklabels(top_types.index, fontsize=10)
for i, (idx, row) in enumerate(top_types.iterrows()):
    ax4.text(row['mean'], i, f" {row['mean']:.1f}개", 
             va='center', fontsize=9, fontweight='bold')
ax4.set_xlabel('평균 진료과목 수', fontsize=12)
ax4.set_title('종별코드별 평균 진료과목 수 (상위 10개)', fontsize=14, fontweight='bold')
ax4.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('강남구_다과목의원_분포분석.png', dpi=300, bbox_inches='tight')
print(f"\n[시각화] 차트가 '강남구_다과목의원_분포분석.png'로 저장되었습니다.")

# 12. 상세 데이터 저장
gangnam_with_dept.to_csv('강남구_병원_진료과목수_분석.csv', encoding='utf-8-sig', index=False)
print(f"[데이터] 상세 데이터가 '강남구_병원_진료과목수_분석.csv'로 저장되었습니다.")

print(f"\n{'='*80}")
print(f"분석 완료!")
print(f"{'='*80}")
