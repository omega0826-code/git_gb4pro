# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 경쟁 환경 분석
작성일: 2026-02-03
버전: 5.00 (V5.00 가이드라인 반영)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import os

# 폰트 설정
try:
    from korean_font_setup import setup_korean_font
    setup_korean_font()
except:
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

print("=" * 80)
print("경쟁 환경 분석 시작")
print("=" * 80)

# 경로 설정
BASE_PATH = Path(r"d:\git_gb4pro\data\서울시 주요 82장소 영역")
DATA_DIR = BASE_PATH / "Gangnam_9_Areas"
REPORT_DIR = BASE_PATH / "REPORT" / "01_경쟁환경분석"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 데이터 로딩
print("\n[1/5] 데이터 로딩 중...", flush=True)

df_area = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(영역-상권).csv', encoding='utf-8-sig')
df_store = pd.read_csv(DATA_DIR / 'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv', encoding='utf-8-sig')

# 날짜 전처리
df_store['기준_년_코드'] = df_store['기준_년_코드'].astype(str)
df_store['기준_분기_코드'] = df_store['기준_분기_코드'].astype(int)

latest_q = df_store['기준_분기_코드'].max()
latest_y = df_store['기준_년_코드'].max()
print(f"  - 최신 데이터: {latest_y}년 {latest_q}분기")

# [2/5] 피부과 상권 필터링
print("\n[2/5] 피부과 점포 필터링 중...", flush=True)

# 피부과 키워드 (가이드라인에 따라 확장 가능)
target_keywords = ['피부과', '병원', '의원'] # 상권분석 데이터의 서비스_업종_명에 해당
# 실제 데이터에서는 '의원' 또는 특정 키워드가 포함됨. 
# 여기서는 예시로 '의원' 필터링 후 피부과 관련 로직 추가 (필요시)

df_dermatology = df_store[df_store['서비스_업종_명'].str.contains('의원', na=False)].copy()
# 실제로는 전문의 데이터가 필요하나, 제공된 데이터 수준에서 분석 진행

# [3/5] 점포 수 집계
print("\n[3/5] 상권별 점포 수 집계 중...", flush=True)

latest_stores = df_dermatology[(df_dermatology['기준_년_코드'] == latest_y) & (df_dermatology['기준_분기_코드'] == latest_q)]
area_stores = latest_stores.groupby('상권_코드_명')['점포_수'].sum().sort_values(ascending=False)

# [4/5] HHI (시장 집중도) 계산
print("\n[4/5] HHI 계산 중...", flush=True)

total_stores = area_stores.sum()
if total_stores > 0:
    shares = (area_stores / total_stores * 100)
    hhi = (shares ** 2).sum()
    print(f"  - 전체 점포 수: {total_stores}개")
    print(f"  - HHI 지수: {hhi:.1f}")

# [5/5] 시각화 및 저장
print("\n[5/5] 시각화 및 결과 저장 중...", flush=True)

plt.figure(figsize=(12, 8))
sns.barplot(x=area_stores.values, y=area_stores.index, palette='viridis')
plt.title('상권별 피부과 의원 수 (최신 분기)', fontsize=15, fontweight='bold')
plt.xlabel('점포 수')
plt.ylabel('상권명')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(REPORT_DIR / '경쟁밀도_히트맵.png', dpi=150)
plt.close()

# CSV 저장
area_stores.to_csv(REPORT_DIR / '상권별_경쟁분포_현황.csv', encoding='utf-8-sig')

print("\n경쟁 환경 분석 완료.")
