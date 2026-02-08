# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 입지 조건 분석
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
print("입지 조건 분석 시작")
print("=" * 80)

# 경로 설정
BASE_PATH = Path(r"d:\git_gb4pro\data\서울시 주요 82장소 영역")
DATA_DIR = BASE_PATH / "Gangnam_9_Areas"
REPORT_DIR = BASE_PATH / "REPORT" / "04_입지조건분석"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 데이터 로딩
print("\n[1/4] 데이터 로딩 중...", flush=True)
df_facility = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(집객시설-상권).csv', encoding='utf-8-sig')

# [2/4] 집객시설 분석
print("\n[2/4] 집객시설 분석 중...", flush=True)
latest_y = df_facility['기준_년_코드'].max()
latest_q = df_facility['기준_분기_코드'].max()
latest_fac = df_facility[(df_facility['기준_년_코드'] == latest_y) & (df_facility['기준_분기_코드'] == latest_q)]

area_fac = latest_fac.groupby('상권_코드_명')['집객시설_수'].sum().sort_values(ascending=False)

# [3/4] 시각화
print("\n[3/4] 시각화 생성 중...", flush=True)

plt.figure(figsize=(12, 8))
area_fac.plot(kind='bar', color='skyblue')
plt.title('상권별 집객시설 수', fontsize=14, fontweight='bold')
plt.ylabel('시설 수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORT_DIR / '집객시설_분포.png', dpi=150)
plt.close()

# CSV 저장
area_fac.to_csv(REPORT_DIR / '상권별_입지조건.csv', encoding='utf-8-sig')

print("\n입지 조건 분석 완료.")
