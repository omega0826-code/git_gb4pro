# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 입지 조건 분석
작성일: 2026-02-04
버전: 5.02 (Robust Date Fix)
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
REPORT_DIR = BASE_PATH / "REPORT" / "04_입지조건분석"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("입지 조건 분석 시작")
df_fac = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(집객시설-상권).csv', encoding='utf-8-sig')

date_col = '기준_년분기_코드'
latest_period = df_fac[date_col].max()
df_latest = df_fac[df_fac[date_col] == latest_period]
print(f"  - 최신 데이터 기준: {latest_period}")

area_col = [col for col in df_fac.columns if '상권_코드_명' in col][0]
area_fac = df_latest.groupby(area_col)['집객시설_수'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=area_fac.values, y=area_fac.index, hue=area_fac.index, palette='coolwarm', legend=False)
plt.title(f'상권별 집객시설 수 ({latest_period})', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(REPORT_DIR / '집객시설_분포.png', dpi=150)
plt.close()

area_fac.to_csv(REPORT_DIR / '상권별_입지조건.csv', encoding='utf-8-sig')
print("입지 조건 분석 완료.")
