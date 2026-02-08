# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 고객 분석
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
print("고객 분석 시작")
print("=" * 80)

# 경로 설정
BASE_PATH = Path(r"d:\git_gb4pro\data\서울시 주요 82장소 영역")
DATA_DIR = BASE_PATH / "Gangnam_9_Areas"
REPORT_DIR = BASE_PATH / "REPORT" / "02_고객분석"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 데이터 로딩
print("\n[1/5] 데이터 로딩 중...", flush=True)
df_sales = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')

# 날짜 전처리
df_sales['기준_년_코드'] = df_sales['기준_년_코드'].astype(str)
df_sales['기준_분기_코드'] = df_sales['기준_분기_코드'].astype(int)

# [2/5] 타겟 고객 매출 분석 (20-40대 여성)
print("\n[2/5] 타겟 고객 매출 분석 중...", flush=True)

# 피부과(의원) 관련 매출 필터링 - 실제 데이터는 서비스_업종_코드_명 확인 필요
# 여기서는 전체 매출 중 타겟 연령대 비율 분석 예시
target_cols = ['여성_연령대_20_매출_금액', '여성_연령대_30_매출_금액', '여성_연령대_40_매출_금액']
df_sales['타겟_매출_금액'] = df_sales[target_cols].sum(axis=1)

latest_y = df_sales['기준_년_코드'].max()
latest_q = df_sales['기준_분기_코드'].max()
latest_sales = df_sales[(df_sales['기준_년_코드'] == latest_y) & (df_sales['기준_분기_코드'] == latest_q)]

area_target_sales = latest_sales.groupby('상권_코드_명')['타겟_매출_금액'].sum().sort_values(ascending=False)

# [3/5] 시각화 - 연령/성별 매출 분포
print("\n[3/5] 시각화 생성 중...", flush=True)

plt.figure(figsize=(12, 8))
area_target_sales.head(10).plot(kind='bar', color='pink')
plt.title('상권별 타겟 고객(20-40대 여성) 매출 현황 (최신 분기)', fontsize=14, fontweight='bold')
plt.ylabel('매출 금액')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORT_DIR / '연령성별_매출분포.png', dpi=150)
plt.close()

# CSV 저장
area_target_sales.to_csv(REPORT_DIR / '상권별_매출현황.csv', encoding='utf-8-sig')

print("\n고객 분석 완료.")
