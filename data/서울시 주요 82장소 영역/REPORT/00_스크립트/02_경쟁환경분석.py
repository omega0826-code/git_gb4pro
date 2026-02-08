# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 경쟁 환경 분석
작성일: 2026-02-04
버전: 5.03 (Robust Date Fix)
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

BASE_PATH = Path(r"d:\git_gb4pro\data\서울시 주요 82장소 영역")
DATA_DIR = BASE_PATH / "Gangnam_9_Areas"
REPORT_DIR = BASE_PATH / "REPORT" / "01_경쟁환경분석"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("경쟁 환경 분석 시작")
df_store = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')

# 최신 데이터 필터링 (combined code 사용)
date_col = '기준_년분기_코드'
latest_period = df_store[date_col].max()
df_latest = df_store[df_store[date_col] == latest_period].copy()
print(f"  - 최신 데이터 기준: {latest_period}")

# 피부과 점포 필터링
df_dermatology = df_latest[df_latest['서비스_업종_코드_명'].str.contains('의원|피부', na=False)].copy()

# 상권별 집계
area_col = [col for col in df_store.columns if '상권_코드_명' in col][0]
area_stores = df_dermatology.groupby(area_col)['점포_수'].sum().sort_values(ascending=False)

# 시각화
plt.figure(figsize=(10, 6))
sns.barplot(x=area_stores.values, y=area_stores.index, hue=area_stores.index, palette='viridis', legend=False)
plt.title(f'상권별 의원 수 ({latest_period})', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(REPORT_DIR / '경쟁밀도_히트맵.png', dpi=150)
plt.close()

area_stores.to_csv(REPORT_DIR / '상권별_경쟁분포_현황.csv', encoding='utf-8-sig')
print("경쟁 환경 분석 완료.")
