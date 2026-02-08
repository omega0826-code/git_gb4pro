# -*- coding: utf-8 -*-
"""
서울시 피부과 병의원(의원, 병원, 종합병원, 상급종합) EDA 분석 파이프라인
작성일: 2026-02-05
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# 한글 폰트 직접 설정 (koreanize_matplotlib 대체)
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 환경 설정
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M')
BASE_DIR = Path(r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\EDA')
OUTPUT_DIR = BASE_DIR / f'EDA_Dermatology_{TIMESTAMP}'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RAWDATA_DIR = OUTPUT_DIR / 'rawdata'
RAWDATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / 'analysis_log.txt'
HTML_FILE = OUTPUT_DIR / f'EDA_분석리포트_서울피부과_{TIMESTAMP}.html'

# 로그 함수
def print_log(msg):
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

# 시각화 스타일 설정 (PPT용으로 크게)
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['figure.titlesize'] = 22

# 2. 데이터 로딩 및 필터링
print_log("="*80)
print_log(f"서울시 피부과 병의원 EDA 분석 시작 ({TIMESTAMP})")
print_log("="*80)

DATA_PATH = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_병원_통합_확장_수정_2025.12.csv'
print_log(f"\n[Phase 1] 데이터 로딩 중: {DATA_PATH}")

df_raw = pd.read_csv(DATA_PATH, encoding='utf-8-sig')
print_log(f"전체 데이터 로드 완료: {len(df_raw):,}개 레코드")

# 필터링
target_types = ['의원', '병원', '종합병원', '상급종합']
df = df_raw[
    (df_raw['종별코드명'].isin(target_types)) & 
    (df_raw['진료과목_피부과'] == 1)
].copy()

print_log(f"필터링 완료 (종별: 의원/병원/종합/상급종합, 과목: 피부과)")
print_log(f"분석 대상 기관 수: {len(df):,}개")

# 3. 분석 및 시각화

def save_plot(filename):
    path = OUTPUT_DIR / filename
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print_log(f"  시각화 저장: {filename}")

# 3.0.1 종별 분포
print_log("\n[3.0.1] 종별 분포 분석")
type_dist = df['종별코드명'].value_counts()
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(type_dist.index, type_dist.values, color=sns.color_palette("husl", len(type_dist)))
ax.set_title('서울시 피부과 의료기관 종별 분포', pad=20)
ax.set_ylabel('기관 수')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{int(height):,}개\n({height/len(df)*100:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=12)
save_plot('01_type_distribution.png')

# 3.0.2 자치구별 분포
print_log("\n[3.0.2] 자치구별 분포 분석")
dist_dist = df['시군구코드명'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(x=dist_dist.values, y=dist_dist.index, palette='viridis', ax=ax)
ax.set_title('서울시 피부과 자치구별 분포 (Top 10)', pad=20)
ax.set_xlabel('기관 수')
for i, v in enumerate(dist_dist.values):
    ax.text(v + 3, i, f'{int(v):,} ({v/len(df)*100:.1f}%)', va='center', fontweight='bold')
save_plot('02_district_distribution.png')

# 3.0.3 설립구분 (가로막대 차트로 변경)
print_log("\n[3.0.3] 설립구분 분포 분석")
est_dist = df['설립구분코드명'].value_counts()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=est_dist.values, y=est_dist.index, palette='pastel', ax=ax)
ax.set_title('설립구분별 분포', pad=20)
ax.set_xlabel('기관 수')
for i, v in enumerate(est_dist.values):
    ax.text(v + 3, i, f'{int(v):,} ({v/len(df)*100:.1f}%)', va='center', fontweight='bold')
save_plot('03_establish_distribution.png')

# 3.0.4 개설연도
print_log("\n[3.0.4] 개설연도 분포 분석")
# 설립연도 컬럼이 이미 존재함

fig, ax = plt.subplots(figsize=(14, 7))
sns.histplot(df['설립연도'].dropna(), bins=30, kde=True, color='skyblue', ax=ax)
ax.set_title('연도별 개설 추이', pad=20)
ax.set_xlabel('연도')
ax.set_ylabel('기관 수')
save_plot('04_year_distribution.png')

# 3.1.1 전문의 수
print_log("\n[3.1.1] 전문의 수 분석")
spec_mean = df['의과전문의 인원수'].mean()
fig, ax = plt.subplots(figsize=(12, 7))
sns.boxplot(x='종별코드명', y='의과전문의 인원수', data=df, palette='Set3', ax=ax)
ax.set_title('종별 전문의 인원수 분포', pad=20)
ax.set_ylim(0, df['의과전문의 인원수'].quantile(0.99)) # 상위 1% 제외하고 가시성 확보
save_plot('05_specialist_analysis.png')

# 3.2.1 병상 수
print_log("\n[3.2.1] 병상 수 분석")
bed_cols = ['일반입원실일반병상수', '일반입원실상급병상수']
bed_sum = df[bed_cols].sum()
fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.bar(bed_sum.index, bed_sum.values, color=['#3498db', '#e74c3c'])
ax.set_title('총 병상 수 현황', pad=20)
ax.set_ylabel('병상 수')
ax.set_xticklabels(['일반병상', '상급병상'])
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
save_plot('06_bed_analysis.png')

# 3.2.2 병원당 평균 병상수 분석
print_log("\n[3.2.2] 병원당 평균 병상수 분석")
df['총병상수'] = df['일반입원실일반병상수'].fillna(0) + df['일반입원실상급병상수'].fillna(0)
bed_by_type = df.groupby('종별코드명')['총병상수'].agg(['mean', 'sum', 'count']).reset_index()
bed_by_type.columns = ['종별', '평균병상', '총병상', '기관수']
bed_by_type = bed_by_type[bed_by_type['총병상'] > 0]  # 병상 있는 종별만
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(bed_by_type['종별'], bed_by_type['평균병상'], color=sns.color_palette('Blues_d', len(bed_by_type)))
ax.set_title('종별 병원당 평균 병상수', pad=20)
ax.set_ylabel('평균 병상수')
ax.set_xlabel('기관 종별')
for bar, (_, row) in zip(bars, bed_by_type.iterrows()):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}병상\n(총 {int(row["총병상"]):,}개)',
            ha='center', va='bottom', fontweight='bold', fontsize=11)
save_plot('06b_bed_per_hospital.png')

# 3.5.2 타 진료과목 병행 현황
print_log("\n[3.5.2] 주요 병행 진료과목 TOP 10")
dept_cols = [col for col in df.columns if col.startswith('진료과목_') and col != '진료과목_개수' and col != '진료과목_피부과']
other_depts = df[dept_cols].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(x=other_depts.values, y=[c.replace('진료과목_', '') for c in other_depts.index], palette='magma', ax=ax)
ax.set_title('피부과 병행 주요 진료과목 (Dermatology and ...)', pad=20)
ax.set_xlabel('기관 수')
for i, v in enumerate(other_depts.values):
    ax.text(v + 1, i, f'{int(v):,} ({v/len(df)*100:.1f}%)', va='center', fontweight='bold')
save_plot('07_department_analysis.png')

# 3.6.1 병원 연령대
print_log("\n[3.6.1] 병원 연령대 분석")
current_year = 2026
# 설립연도가 유효한 데이터만 사용 (NaN 및 이상치 제외)
df_age = df[df['설립연도'].notna() & (df['설립연도'] > 1900) & (df['설립연도'] <= current_year)].copy()
df_age['업력'] = current_year - df_age['설립연도']
bins = [0, 5, 10, 20, 30, 200]
labels = ['신규(5년미만)', '성장기(5-10년)', '중견(10-20년)', '성숙(20-30년)', '노포(30년이상)']
df_age['병원연령대'] = pd.cut(df_age['업력'], bins=bins, labels=labels, right=False)

age_dist = df_age['병원연령대'].value_counts().reindex(labels, fill_value=0)
print_log(f"  연령대 분석 대상: {len(df_age):,}개 (설립연도 유효 기준)")
print_log(f"  설립연도 미상: {len(df) - len(df_age):,}개")

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(age_dist.index, age_dist.values, color=sns.color_palette("rocket", len(age_dist)))
ax.set_title(f'피부과 병원 연령대 분포 (N={len(df_age):,})', pad=20)
ax.set_ylabel('기관 수')
for bar in bars:
    height = bar.get_height()
    pct = height / len(df_age) * 100 if len(df_age) > 0 else 0
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{int(height):,}\n({pct:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=12)
save_plot('08_age_size_analysis.png')

# 4. HTML 리포트 생성
print_log("\n[Phase 4] HTML 리포트 생성 중...")

def encode_img(filename):
    with open(OUTPUT_DIR / filename, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

images = [
    ('01_type_distribution.png', '기관 유형 분포'),
    ('02_district_distribution.png', '자치구별 분포 (Top 10)'),
    ('03_establish_distribution.png', '설립구분 분포'),
    ('04_year_distribution.png', '개설연도 추이'),
    ('05_specialist_analysis.png', '전문의 인원수 분석'),
    ('06_bed_analysis.png', '병상 규모 분석'),
    ('06b_bed_per_hospital.png', '병원당 평균 병상수'),
    ('07_department_analysis.png', '주요 병행 진료과목'),
    ('08_age_size_analysis.png', '병원 연령대 분포')
]

html_template = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>서울시 피부과 EDA 분석 리포트</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; margin: 40px; background-color: #f4f7f6; }}
        .container {{ max-width: 1200px; margin: auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 20px; }}
        h2 {{ color: #2980b9; margin-top: 50px; border-left: 5px solid #3498db; padding-left: 15px; }}
        .summary {{ background: #e8f4fd; padding: 25px; border-radius: 10px; margin-bottom: 40px; border-left: 5px solid #3498db; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-card {{ background: #fff; border: 1px solid #ddd; padding: 20px; text-align: center; border-radius: 10px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #e74c3c; }}
        .image-box {{ margin: 40px 0; text-align: center; }}
        img {{ max-width: 100%; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.15); }}
        .caption {{ margin-top: 15px; font-style: italic; color: #7f8c8d; font-size: 16px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>서울시 피부과(의원~상급종합) EDA 분석 리포트</h1>
        <div class="summary">
            <p>본 리포트는 서울시 소재 <strong>피부과</strong> 진료과목을 포함하는 <strong>의원, 병원, 종합병원, 상급종합병원</strong>을 대상으로 분석한 결과입니다.</p>
            <p>데이터 기준일: 2025년 12월 / 리포트 생성일: {TIMESTAMP}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card"><div>총 기관 수</div><div class="stat-value">{len(df):,}개</div></div>
            <div class="stat-card"><div>강남구 집중도</div><div class="stat-value">{(df['시군구코드명']=='강남구').sum()/len(df)*100:.1f}%</div></div>
            <div class="stat-card"><div>의원급 비중</div><div class="stat-value">{(df['종별코드명']=='의원').sum()/len(df)*100:.1f}%</div></div>
            <div class="stat-card"><div>평균 전문의</div><div class="stat-value">{df['의과전문의 인원수'].mean():.2f}명</div></div>
        </div>
"""

for img, capt in images:
    html_template += f"""
        <div class="image-box">
            <h2>{capt}</h2>
            <img src="data:image/png;base64,{encode_img(img)}" alt="{capt}">
            <p class="caption">※ {capt} 시각화 고해상도 자료 (PPT용)</p>
        </div>
    """

html_template += """
    </div>
</body>
</html>
"""

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_template)

# 5. Raw Data 저장
print_log("\n[Phase 5] Raw Data 저장 중...")
df.to_csv(RAWDATA_DIR / f'피부과_분석대상_{TIMESTAMP}.csv', index=False, encoding='utf-8-sig')
print_log(f"  저장됨: 피부과_분석대상_{TIMESTAMP}.csv ({len(df):,}행)")

# 분석별 집계 데이터 저장
type_dist.to_frame('기관수').to_csv(RAWDATA_DIR / '종별분포.csv', encoding='utf-8-sig')
est_dist.to_frame('기관수').to_csv(RAWDATA_DIR / '설립구분분포.csv', encoding='utf-8-sig')
bed_by_type.to_csv(RAWDATA_DIR / '종별_병상현황.csv', index=False, encoding='utf-8-sig')
age_dist.to_frame('기관수').to_csv(RAWDATA_DIR / '병원연령대분포.csv', encoding='utf-8-sig')
print_log(f"  집계 데이터 4개 파일 저장 완료")

print_log(f"\n[성공] 모든 분석이 완료되었습니다.")
print_log(f"결과 폴더: {OUTPUT_DIR}")
print_log(f"Raw Data: {RAWDATA_DIR}")
print_log(f"HTML 리포트: {HTML_FILE}")
print_log("="*80)
