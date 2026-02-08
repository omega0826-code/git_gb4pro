# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 인구 유동 분석
작성일: 2026-02-04
버전: 5.04 (Robust Date Fix)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

try:
    from korean_font_setup import setup_korean_font
    setup_korean_font()
except:
    plt.rcParams['font.family'] = 'Malgun Gothic'

BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
DATA_PATH = BASE_DIR / 'Gangnam_9_Areas'
OUTPUT_DIR = BASE_DIR / 'REPORT' / '03_인구유동분석'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("인구 유동 분석 시작")

df_resident = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(상주인구-상권).csv', encoding='utf-8-sig')
df_worker = pd.read_csv(DATA_PATH / 'gangnam_서울시 상권분석서비스(직장인구-상권).csv', encoding='utf-8-sig')

# 각각의 최신 데이터 사용
date_col = '기준_년분기_코드'
latest_res_p = df_resident[date_col].max()
latest_work_p = df_worker[date_col].max()

df_res_latest = df_resident[df_resident[date_col] == latest_res_p]
df_work_latest = df_worker[df_worker[date_col] == latest_work_p]

print(f"  - 상주인구 기준: {latest_res_p}, 직장인구 기준: {latest_work_p}")

res_col = [col for col in df_resident.columns if '총_상주' in col][0]
work_col = [col for col in df_worker.columns if '총_직장' in col][0]
area_col = [col for col in df_resident.columns if '상권_코드_명' in col][0]

area_resident = df_res_latest.groupby(area_col)[res_col].sum()
area_worker = df_work_latest.groupby(area_col)[work_col].sum()

comparison = pd.DataFrame({'상주인구': area_resident, '직장인구': area_worker}).fillna(0).sort_values(by='상주인구', ascending=False)

# 시각화
plt.figure(figsize=(12, 6))
comparison.plot(kind='bar', ax=plt.gca(), width=0.8)
plt.title(f'상권별 인구 구조 분석', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '인구유동_분석결과.png', dpi=150)
plt.close()

comparison.to_csv(OUTPUT_DIR / '상권별_인구현황.csv', encoding='utf-8-sig')
print("인구 유동 분석 완료.")
