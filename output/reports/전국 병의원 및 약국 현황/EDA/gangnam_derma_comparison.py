# -*- coding: utf-8 -*-
"""
강남구 피부과 특징 비교 분석 리포트
- 비교 대상: 강남구 vs 서초구 vs 송파구 vs 서울평균
작성일: 2026-02-05
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 16

# 환경 설정
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M')
BASE_DIR = Path(r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\EDA')
OUTPUT_DIR = BASE_DIR / f'EDA_Dermatology_Comparison_{TIMESTAMP}'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RAWDATA_DIR = OUTPUT_DIR / 'rawdata'
RAWDATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / 'analysis_log.txt'
HTML_FILE = OUTPUT_DIR / f'EDA_비교분석리포트_강남구피부과_{TIMESTAMP}.html'

def print_log(msg):
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def save_plot(filename):
    path = OUTPUT_DIR / filename
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print_log(f"  시각화 저장: {filename}")

# 데이터 로드
print_log("="*80)
print_log(f"강남구 피부과 비교 분석 시작 ({TIMESTAMP})")
print_log("="*80)

DATA_PATH = BASE_DIR / 'EDA_Dermatology_20260205_0424' / 'rawdata' / '피부과_분석대상_20260205_0424.csv'
print_log(f"\n[Phase 1] 데이터 로딩 중: {DATA_PATH}")
df = pd.read_csv(DATA_PATH, encoding='utf-8-sig', low_memory=False)
print_log(f"전체 데이터 로드: {len(df):,}개")

# 강남언니 입점 데이터 병합
UNNI_PATH = Path(r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\merged\HIRA_강남언니_결합_최종.csv')
print_log(f"강남언니 데이터 로딩 및 병합 중: {UNNI_PATH}")
df_unni = pd.read_csv(UNNI_PATH, usecols=['암호화요양기호', '강남언니_등록'], low_memory=False)
df = pd.merge(df, df_unni, on='암호화요양기호', how='left')
df['강남언니_등록'] = df['강남언니_등록'].fillna(False)
print_log(f"병합 후 강남언니 등록 태그 확인: {df['강남언니_등록'].value_counts().to_dict()}")

# 비교 대상 정의
TARGETS = ['강남구', '서초구', '송파구']
COLORS = {'강남구': '#e74c3c', '서초구': '#3498db', '송파구': '#2ecc71', '서울평균': '#95a5a6'}

# 데이터 분리
df_gangnam = df[df['시군구코드명'] == '강남구'].copy()
df_seocho = df[df['시군구코드명'] == '서초구'].copy()
df_songpa = df[df['시군구코드명'] == '송파구'].copy()

print_log(f"강남구: {len(df_gangnam):,}개, 서초구: {len(df_seocho):,}개, 송파구: {len(df_songpa):,}개")

# ========== 분석 레이어 1: 기관 규모 ==========
print_log("\n[Layer 1] 기관 규모 비교")

scale_data = {
    '지역': TARGETS + ['서울평균'],
    '기관수': [len(df_gangnam), len(df_seocho), len(df_songpa), len(df) / 25],
    '서울비중(%)': [len(df_gangnam)/len(df)*100, len(df_seocho)/len(df)*100, 
                   len(df_songpa)/len(df)*100, 4.0]
}
df_scale = pd.DataFrame(scale_data)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(df_scale['지역'], df_scale['기관수'], 
              color=[COLORS[t] for t in df_scale['지역']])
ax.set_title('피부과 기관 수 비교', pad=20)
ax.set_ylabel('기관 수')
for bar, pct in zip(bars, df_scale['서울비중(%)']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 10,
            f'{int(height):,}\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold')
save_plot('01_institution_scale.png')

# 종별 구성비
print_log("\n[Layer 1-2] 종별 구성비 비교")
type_comp = pd.DataFrame({
    '강남구': df_gangnam['종별코드명'].value_counts(normalize=True) * 100,
    '서초구': df_seocho['종별코드명'].value_counts(normalize=True) * 100,
    '송파구': df_songpa['종별코드명'].value_counts(normalize=True) * 100,
    '서울평균': df['종별코드명'].value_counts(normalize=True) * 100
}).fillna(0).T

fig, ax = plt.subplots(figsize=(14, 7))
type_comp.plot(kind='bar', ax=ax, color=sns.color_palette('Set2', len(type_comp.columns)))
ax.set_title('종별 구성비 비교 (%)', pad=20)
ax.set_ylabel('비율 (%)')
ax.set_xlabel('')
ax.legend(title='종별', bbox_to_anchor=(1.02, 1))
plt.xticks(rotation=0)
save_plot('02_type_composition.png')

# ========== 분석 레이어 2: 인력 현황 ==========
print_log("\n[Layer 2] 전문의 인력 비교")

specialist_stats = pd.DataFrame({
    '지역': TARGETS + ['서울평균'],
    '평균전문의': [df_gangnam['의과전문의 인원수'].mean(), df_seocho['의과전문의 인원수'].mean(),
                  df_songpa['의과전문의 인원수'].mean(), df['의과전문의 인원수'].mean()],
    '중앙값': [df_gangnam['의과전문의 인원수'].median(), df_seocho['의과전문의 인원수'].median(),
              df_songpa['의과전문의 인원수'].median(), df['의과전문의 인원수'].median()],
    '총전문의': [df_gangnam['의과전문의 인원수'].sum(), df_seocho['의과전문의 인원수'].sum(),
               df_songpa['의과전문의 인원수'].sum(), df['의과전문의 인원수'].sum() / 25]
})

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 평균 전문의 수
bars = axes[0].bar(specialist_stats['지역'], specialist_stats['평균전문의'],
                   color=[COLORS[t] for t in specialist_stats['지역']])
axes[0].set_title('기관당 평균 전문의 수', pad=20)
axes[0].set_ylabel('전문의 수 (명)')
for bar in bars:
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                 f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

# 총 전문의 수
bars = axes[1].bar(specialist_stats['지역'], specialist_stats['총전문의'],
                   color=[COLORS[t] for t in specialist_stats['지역']])
axes[1].set_title('지역 총 전문의 수', pad=20)
axes[1].set_ylabel('전문의 수 (명)')
for bar in bars:
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
save_plot('03_specialist_comparison.png')

# ========== 분석 레이어 3: 시설 현황 ==========
print_log("\n[Layer 3] 병상 시설 비교")

def calc_bed_stats(data):
    data = data.copy()
    data['총병상수'] = data['일반입원실일반병상수'].fillna(0) + data['일반입원실상급병상수'].fillna(0)
    has_bed = (data['총병상수'] > 0).sum()
    return {
        '병상보유기관': has_bed,
        '병상보유율(%)': has_bed / len(data) * 100 if len(data) > 0 else 0,
        '평균병상수': data[data['총병상수'] > 0]['총병상수'].mean() if has_bed > 0 else 0,
        '총병상수': data['총병상수'].sum()
    }

bed_stats = pd.DataFrame({
    '강남구': calc_bed_stats(df_gangnam),
    '서초구': calc_bed_stats(df_seocho),
    '송파구': calc_bed_stats(df_songpa),
    '서울평균': {k: v/25 if k in ['병상보유기관', '총병상수'] else v 
                for k, v in calc_bed_stats(df).items()}
}).T

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 병상 보유율
bars = axes[0].bar(bed_stats.index, bed_stats['병상보유율(%)'],
                   color=[COLORS[t] for t in bed_stats.index])
axes[0].set_title('병상 보유 기관 비율 (%)', pad=20)
axes[0].set_ylabel('비율 (%)')
for bar in bars:
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# 병상 보유기관 평균 병상수
bars = axes[1].bar(bed_stats.index, bed_stats['평균병상수'],
                   color=[COLORS[t] for t in bed_stats.index])
axes[1].set_title('병상보유 기관의 평균 병상수', pad=20)
axes[1].set_ylabel('병상 수')
for bar in bars:
    height = bar.get_height()
    if height > 0:
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                     f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
save_plot('04_bed_comparison.png')

# ========== 분석 레이어 4: 설립 구조 ==========
print_log("\n[Layer 4] 설립연도 및 신규개원 비교")

current_year = 2026
df['업력'] = current_year - df['설립연도']
df_gangnam['업력'] = current_year - df_gangnam['설립연도']
df_seocho['업력'] = current_year - df_seocho['설립연도']
df_songpa['업력'] = current_year - df_songpa['설립연도']

# 연도별 분포 히스토그램
fig, ax = plt.subplots(figsize=(14, 7))
for region, data, color in [('강남구', df_gangnam, COLORS['강남구']), 
                             ('서초구', df_seocho, COLORS['서초구']),
                             ('송파구', df_songpa, COLORS['송파구'])]:
    valid_years = data['설립연도'].dropna()
    valid_years = valid_years[(valid_years > 1980) & (valid_years <= 2025)]
    ax.hist(valid_years, bins=20, alpha=0.5, label=region, color=color)
ax.set_title('설립연도 분포 비교', pad=20)
ax.set_xlabel('설립연도')
ax.set_ylabel('기관 수')
ax.legend()
save_plot('05_establishment_trend.png')

# 신규개원 비율 (5년 이내)
def calc_new_ratio(data):
    valid = data[data['업력'].notna() & (data['업력'] >= 0)]
    new_count = (valid['업력'] < 5).sum()
    return new_count / len(valid) * 100 if len(valid) > 0 else 0

new_ratios = {
    '강남구': calc_new_ratio(df_gangnam),
    '서초구': calc_new_ratio(df_seocho),
    '송파구': calc_new_ratio(df_songpa),
    '서울평균': calc_new_ratio(df)
}

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(new_ratios.keys(), new_ratios.values(),
              color=[COLORS[t] for t in new_ratios.keys()])
ax.set_title('신규 개원 비율 (최근 5년 이내)', pad=20)
ax.set_ylabel('비율 (%)')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
save_plot('06_new_clinic_ratio.png')

# ========== 분석 레이어 5: 진료과목 히트맵 ==========
print_log("\n[Layer 5] 병행 진료과목 비교")

dept_cols = [c for c in df.columns if c.startswith('진료과목_') and c != '진료과목_개수' and c != '진료과목_피부과']

def get_top_depts(data, n=5):
    return data[dept_cols].sum().sort_values(ascending=False).head(n)

top_depts_all = get_top_depts(df, 10)
selected_depts = top_depts_all.index.tolist()

dept_compare = pd.DataFrame({
    '강남구': (df_gangnam[selected_depts].sum() / len(df_gangnam) * 100),
    '서초구': (df_seocho[selected_depts].sum() / len(df_seocho) * 100),
    '송파구': (df_songpa[selected_depts].sum() / len(df_songpa) * 100),
    '서울평균': (df[selected_depts].sum() / len(df) * 100)
})
dept_compare.index = [c.replace('진료과목_', '') for c in dept_compare.index]

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(dept_compare, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax,
            cbar_kws={'label': '보유 비율 (%)'})
ax.set_title('주요 병행 진료과목 보유 비율 (%)', pad=20)
ax.set_xlabel('')
ax.set_ylabel('')
save_plot('07_department_heatmap.png')

# ========== 분석 레이어 8: 강남언니 플랫폼 분석 (개수 및 비율) ==========
print_log("\n[Layer 8] 강남언니 플랫폼 입점 분석 비교")

def get_unni_stats(data):
    count = int((data['강남언니_등록'] == True).sum())
    ratio = count / len(data) * 100 if len(data) > 0 else 0
    return count, ratio

# 데이터 분리 재확인 (병합된 컬럼 반영)
df_gangnam = df[df['시군구코드명'] == '강남구'].copy()
df_seocho = df[df['시군구코드명'] == '서초구'].copy()
df_songpa = df[df['시군구코드명'] == '송파구'].copy()

unni_stats = {
    '강남구': get_unni_stats(df_gangnam),
    '서초구': get_unni_stats(df_seocho),
    '송파구': get_unni_stats(df_songpa),
    '서울평균': (int((df['강남언니_등록'] == True).sum() / 25), get_unni_stats(df)[1]) # 서울평균은 1개구 기준 산술평균
}

fig, ax = plt.subplots(figsize=(12, 7))
labels = list(unni_stats.keys())
counts = [s[0] for s in unni_stats.values()]
ratios = [s[1] for s in unni_stats.values()]

bars = ax.bar(labels, ratios, color=[COLORS[t] for t in labels])
ax.set_title('강남언니 플랫폼 입점 현황 (비율 및 개수)', pad=30)
ax.set_ylabel('입점 비율 (%)')

# 막대 상단에 개수와 비율 병기
for bar, count, ratio in zip(bars, counts, ratios):
    height = bar.get_height()
    label_text = f'{count:,}개\n({ratio:.1f}%)'
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            label_text, ha='center', va='bottom', fontweight='bold', 
            fontsize=14, color='#2c3e50')

# Y축 여유 공간 확보
ax.set_ylim(0, max(ratios) * 1.25)
save_plot('08_gangnam_unni_rate.png')

# ========== Raw Data 저장 ==========
print_log("\n[Phase 5] Raw Data 저장 중...")

df_scale.to_csv(RAWDATA_DIR / '지역별_기관수.csv', index=False, encoding='utf-8-sig')
specialist_stats.to_csv(RAWDATA_DIR / '지역별_전문의통계.csv', encoding='utf-8-sig')
bed_stats.to_csv(RAWDATA_DIR / '지역별_병상통계.csv', encoding='utf-8-sig')
pd.DataFrame({'지역': list(new_ratios.keys()), '신규개원비율(%)': list(new_ratios.values())}).to_csv(
    RAWDATA_DIR / '지역별_신규개원비율.csv', index=False, encoding='utf-8-sig')
dept_compare.to_csv(RAWDATA_DIR / '지역별_진료과목비교.csv', encoding='utf-8-sig')
pd.DataFrame({
    '지역': list(unni_stats.keys()), 
    '입점개수': [s[0] for s in unni_stats.values()],
    '입점비율(%)': [s[1] for s in unni_stats.values()]
}).to_csv(RAWDATA_DIR / '지역별_강남언니입점비율.csv', index=False, encoding='utf-8-sig')
print_log("  6개 CSV 저장 완료")

# ========== HTML 리포트 생성 ==========
print_log("\n[Phase 6] HTML 리포트 생성 중...")

def encode_img(filename):
    with open(OUTPUT_DIR / filename, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

images = [
    ('01_institution_scale.png', '기관 규모 비교'),
    ('02_type_composition.png', '종별 구성비 비교'),
    ('03_specialist_comparison.png', '전문의 인력 비교'),
    ('04_bed_comparison.png', '병상 시설 비교'),
    ('05_establishment_trend.png', '설립연도 분포'),
    ('06_new_clinic_ratio.png', '신규개원 비율'),
    ('07_department_heatmap.png', '병행 진료과목 비교'),
    ('08_gangnam_unni_rate.png', '강남언니 플랫폼 입점 현황 (개수 및 비율)')
]

html_template = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>강남구 피부과 비교 분석 리포트</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 4px solid #e74c3c; padding-bottom: 20px; }}
        h2 {{ color: #e74c3c; margin-top: 50px; border-left: 6px solid #e74c3c; padding-left: 15px; }}
        .summary {{ background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%); padding: 25px; border-radius: 15px; margin-bottom: 40px; border-left: 6px solid #e74c3c; }}
        .comparison-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 30px 0; }}
        .stat-card {{ background: #fff; border: 2px solid #ddd; padding: 20px; text-align: center; border-radius: 12px; transition: transform 0.3s; }}
        .stat-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .stat-card.gangnam {{ border-color: #e74c3c; background: #fff5f5; }}
        .stat-value {{ font-size: 28px; font-weight: bold; color: #e74c3c; }}
        .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
        .image-box {{ margin: 40px 0; text-align: center; }}
        img {{ max-width: 100%; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }}
        .insight {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #3498db; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 강남구 피부과 비교 분석 리포트</h1>
        <div class="summary">
            <p><strong>분석 목적:</strong> 강남구 피부과의 특징을 서울 평균 및 Top 2 자치구(서초구, 송파구)와 비교 분석하여 경쟁력과 차별점을 도출</p>
            <p><strong>데이터 기준:</strong> 2025년 12월 / 리포트 생성: {TIMESTAMP}</p>
        </div>
        
        <div class="comparison-grid">
            <div class="stat-card gangnam"><div class="stat-label">강남구</div><div class="stat-value">{len(df_gangnam):,}개</div><div class="stat-label">서울의 {len(df_gangnam)/len(df)*100:.1f}%</div></div>
            <div class="stat-card"><div class="stat-label">서초구</div><div class="stat-value">{len(df_seocho):,}개</div><div class="stat-label">서울의 {len(df_seocho)/len(df)*100:.1f}%</div></div>
            <div class="stat-card"><div class="stat-label">송파구</div><div class="stat-value">{len(df_songpa):,}개</div><div class="stat-label">서울의 {len(df_songpa)/len(df)*100:.1f}%</div></div>
            <div class="stat-card"><div class="stat-label">서울 총</div><div class="stat-value">{len(df):,}개</div><div class="stat-label">25개 자치구</div></div>
        </div>
"""

for img, title in images:
    html_template += f"""
        <div class="image-box">
            <h2>{title}</h2>
            <img src="data:image/png;base64,{encode_img(img)}" alt="{title}">
        </div>
    """

html_template += """
    </div>
</body>
</html>
"""

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_template)

print_log(f"\n[성공] 비교 분석이 완료되었습니다.")
print_log(f"결과 폴더: {OUTPUT_DIR}")
print_log(f"HTML 리포트: {HTML_FILE}")
print_log("="*80)
