# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 종합 평가
작성일: 2026-02-03
버전: 5.00 (V5.00 가이드라인 반영)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# 폰트 설정
try:
    from korean_font_setup import setup_korean_font
    setup_korean_font()
except:
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

print("=" * 80)
print("종합 평가 시작")
print("=" * 80)

# 경로 설정
BASE_PATH = Path(r"d:\git_gb4pro\data\서울시 주요 82장소 영역")
REPORT_BASE = BASE_PATH / "REPORT"
REPORT_DIR = REPORT_BASE / "05_종합평가"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# [1/4] 데이터 로딩 (이전 단계 산출물)
print("\n[1/4] 이전 단계 결과 로딩 중...", flush=True)

try:
    df_comp = pd.read_csv(REPORT_BASE / "01_경쟁환경분석" / "상권별_경쟁분포_현황.csv")
    df_cust = pd.read_csv(REPORT_BASE / "02_고객분석" / "상권별_매출현황.csv")
    df_pop = pd.read_csv(REPORT_BASE / "03_인구유동분석" / "상권별_인구현황.csv")
    df_loc = pd.read_csv(REPORT_BASE / "04_입지조건분석" / "상권별_입지조건.csv")
except Exception as e:
    print(f"데이터 로딩 실패: {e}")
    sys.exit(1)

# 컬럼명 통일
df_comp.columns = ['상권_명', '경쟁지표']
df_cust.columns = ['상권_명', '고객지표']
df_pop.columns = ['상권_명', '인구지표']
df_loc.columns = ['상권_명', '입지지표']

# 데이터 병합
df_merge = df_comp.merge(df_cust, on='상권_명').merge(df_pop, on='상권_명').merge(df_loc, on='상권_명')

# [2/4] 점수 정규화 및 종합 점수 산출
print("\n[2/4] 점수 정규화 및 종합 점수 산출 중...", flush=True)

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df_merge['경쟁_N'] = 1 - normalize(df_merge['경쟁지표']) # 경쟁은 낮을수록 좋음
df_merge['고객_N'] = normalize(df_merge['고객지표'])
df_merge['인구_N'] = normalize(df_merge['인구지표'])
df_merge['입지_N'] = normalize(df_merge['입지지표'])

# 가중치 적용 (경쟁 20%, 고객 40%, 인구 20%, 입지 20%)
df_merge['종합점수'] = (df_merge['경쟁_N'] * 0.2 + 
                    df_merge['고객_N'] * 0.4 + 
                    df_merge['인구_N'] * 0.2 + 
                    df_merge['입지_N'] * 0.2) * 100

df_merge = df_merge.sort_values(by='종합점수', ascending=False)

# [3/4] 시각화
print("\n[3/4] 시각화 생성 중...", flush=True)

plt.figure(figsize=(12, 8))
sns.barplot(x='종합점수', y='상권_명', data=df_merge, palette='magma')
plt.title('상권별 의원급 피부과 입지 종합 평가 점수', fontsize=15, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(REPORT_DIR / '종합점수_순위.png', dpi=150)
plt.close()

# 레이더 차트 (상위 3개)
from math import pi

def create_radar_chart(df, output_path):
    categories = ['경쟁', '고객', '인구', '입지']
    N = len(categories)
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    for i, row in df.head(3).iterrows():
        values = [row['경쟁_N'], row['고객_N'], row['인구_N'], row['입지_N']]
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['상권_명'])
        ax.fill(angles, values, alpha=0.1)
        
    plt.xticks(angles[:-1], categories)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('상위 3개 상권 4차원 비교', size=15, y=1.1)
    plt.savefig(output_path, dpi=150)
    plt.close()

create_radar_chart(df_merge, REPORT_DIR / '4차원_레이더.png')

# [4/4] 결과 저장
df_merge.to_csv(REPORT_DIR / '전체_상권_종합점수.csv', index=False, encoding='utf-8-sig')

print("\n종합 평가 완료.")
