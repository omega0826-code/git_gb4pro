# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 인구 유동 분석
작성일: 2026-02-03
버전: 5.01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# 한글 폰트 설정
from korean_font_setup import setup_korean_font
setup_korean_font()

# 경로 설정
BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
DATA_PATH = BASE_DIR / 'Gangnam_9_Areas'
OUTPUT_DIR = BASE_DIR / 'REPORT' / '03_인구유동분석'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("인구 유동 분석 시작")
print("=" * 80)

# 데이터 로딩
print("\n[1/4] 데이터 로딩 중...", flush=True)

df_resident = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(상주인구-상권).csv', encoding='utf-8-sig')
df_worker = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(직장인구-상권).csv', encoding='utf-8-sig')
df_floating = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(길단위인구-상권).csv', encoding='utf-8-sig')

# 최신 데이터 추출
latest_period = df_resident['기준_년_분기_코드'].max()
latest_resident = df_resident[df_resident['기준_년_분기_코드'] == latest_period]
latest_worker = df_worker[df_worker['기준_년_분기_코드'] == latest_period]
latest_floating = df_floating[df_floating['기준_년_분기_코드'] == latest_period]

# [2/4] 상권별 인구 분석
print("\n[2/4] 상권별 인구 분석 중...", flush=True)

# 인구 컬럼명 확인 (상주인구: 총_상주_인구_수, 직장인구: 총_직장_인구_수)
res_col = '총_상주_인구_수'
work_col = '총_직장_인구_수'

area_resident = latest_resident.groupby('상권_코드_명')[res_col].sum().sort_values(ascending=False)
area_worker = latest_worker.groupby('상권_코드_명')[work_col].sum().sort_values(ascending=False)

# [3/4] 시각화 생성
print("\n[3/4] 시각화 생성 중...", flush=True)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
plt.rcParams['font.family'] = 'Malgun Gothic'

# 1. 상권별 상주인구
area_resident.plot(kind='barh', ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('상권별 상주인구', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3)

# 2. 상권별 직장인구
area_worker.plot(kind='barh', ax=axes[0, 1], color='lightgreen')
axes[0, 1].set_title('상권별 직장인구', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='x', alpha=0.3)

# 3. 상주 vs 직장 비교
comparison = pd.DataFrame({'상주인구': area_resident, '직장인구': area_worker}).fillna(0)
comparison.plot(kind='bar', ax=axes[1, 0])
axes[1, 0].set_title('상권별 인구 구조 비교', fontsize=12, fontweight='bold')
plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')

# 4. 요약 텍스트
axes[1, 1].axis('off')
summary_text = f"인구 분석 요약 ({latest_period})\n\n"
summary_text += f"- 최대 상주인구: {area_resident.idxmax()} ({area_resident.max():,.0f}명)\n"
summary_text += f"- 최대 직장인구: {area_worker.idxmax()} ({area_worker.max():,.0f}명)\n"
axes[1, 1].text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center')

plt.tight_layout()
fig.savefig(OUTPUT_DIR / '인구유동_분석결과.png', dpi=150)

# 결과 저장
comparison.to_csv(OUTPUT_DIR / '상권별_인구현황.csv', encoding='utf-8-sig')

print("\n[4/4] 인구 유동 분석 완료")
print("=" * 80)
