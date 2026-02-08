# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 고객 분석
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
REPORT_DIR = BASE_PATH / "REPORT" / "02_고객분석"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("고객 수요 분석 시작")
df_sales = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')

# 최신 데이터 필터링
date_col = '기준_년분기_코드'
latest_period = df_sales[date_col].max()
df_latest = df_sales[df_sales[date_col] == latest_period].copy()
print(f"  - 최신 데이터 기준: {latest_period}")

# 타겟 매출 (20-40대)
target_cols = [col for col in df_sales.columns if '연령대' in col and ('20' in col or '30' in col or '40' in col) and '매출_금액' in col]
df_latest['타겟_매출_금액'] = df_latest[target_cols].sum(axis=1)

area_col = [col for col in df_sales.columns if '상권_코드_명' in col][0]
area_sales = df_latest.groupby(area_col)['타겟_매출_금액'].sum().sort_values(ascending=False)

# 시각화
plt.figure(figsize=(10, 6))
sns.barplot(x=area_sales.values, y=area_sales.index, hue=area_sales.index, palette='magma', legend=False)
plt.title(f'상권별 타겟 고객 매출 현황 ({latest_period})', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(REPORT_DIR / '연령성별_매출분포.png', dpi=150)
plt.close()

area_sales.to_csv(REPORT_DIR / '상권별_매출현황.csv', encoding='utf-8-sig')
print("고객 분석 완료.")
