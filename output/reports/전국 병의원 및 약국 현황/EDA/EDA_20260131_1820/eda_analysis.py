"""
서울 병원 통합 데이터 EDA 분석
가이드라인: EDA_서울병원통합_분석_가이드라인_V2.00.md
작성일: 2026-01-31
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import sys
warnings.filterwarnings('ignore')

# 스타일 설정
sns.set_style("whitegrid")
sns.set_palette("husl")

# 한글 폰트 설정 (seaborn 스타일 설정 후 재설정 필요)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 출력 폴더 설정
OUTPUT_DIR = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\EDA\EDA_20260131_1820'
LOG_FILE = OUTPUT_DIR + r'\analysis_log.txt'

# 로그 파일 초기화
log = open(LOG_FILE, 'w', encoding='utf-8')

def print_log(msg):
    """콘솔과 파일에 동시 출력"""
    print(msg)
    log.write(msg + '\n')
    log.flush()

print_log("="*80)
print_log("서울 병원 통합 데이터 EDA 분석")
print_log("="*80)

# 데이터 로딩
print_log("\n[Phase 1] 데이터 로딩 중...")
df = pd.read_csv(
    r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_병원_통합_확장_수정_2025.12.csv',
    encoding='utf-8-sig'
)

print_log(f"데이터 로딩 완료")
print_log(f"  - 총 레코드 수: {len(df):,}개")
print_log(f"  - 총 컬럼 수: {len(df.columns)}개")

# 기본 정보 확인
print_log(f"\n[데이터 기본 정보]")
print_log(f"  - 메모리 사용량: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print_log(f"  - 데이터 타입:")
print_log(f"    - object: {(df.dtypes == 'object').sum()}개")
print_log(f"    - int64: {(df.dtypes == 'int64').sum()}개")
print_log(f"    - float64: {(df.dtypes == 'float64').sum()}개")

# 결측치 확인
print_log(f"\n[결측치 현황]")
missing_cols = df.isnull().sum()
missing_cols = missing_cols[missing_cols > 0].sort_values(ascending=False)
if len(missing_cols) > 0:
    print_log(f"  - 결측치 있는 컬럼: {len(missing_cols)}개")
    print_log(f"  - 주요 결측치 (상위 5개):")
    for col, count in missing_cols.head(5).items():
        pct = count / len(df) * 100
        print_log(f"    - {col}: {count:,}개 ({pct:.2f}%)")
else:
    print_log(f"  - 결측치 없음")

print_log(f"\nPhase 1 완료: 환경 설정 및 데이터 로딩")
print_log("="*80)

# 데이터를 전역 변수로 저장 (다음 단계에서 사용)
df.to_pickle(OUTPUT_DIR + r'\df_loaded.pkl')
print_log(f"\n데이터 저장 완료: df_loaded.pkl")

log.close()
print(f"\n로그 파일 저장: {LOG_FILE}")
