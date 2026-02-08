# -*- coding: utf-8 -*-
import pandas as pd

# 데이터 로딩
df_store = pd.read_csv('d:/git_gb4pro/data/서울시 주요 82장소 영역/Gangnam_CSV_20260203_094620/gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv', encoding='utf-8')

print("=== 점포 데이터 구조 분석 ===\n")
print(f"총 행 수: {len(df_store):,}")
print(f"총 컬럼 수: {len(df_store.columns)}\n")

print("컬럼 목록:")
for i, col in enumerate(df_store.columns, 1):
    print(f"  {i}. {col} ({df_store[col].dtype})")

print("\n샘플 데이터 (첫 3행):")
print(df_store.head(3))

print("\n업종 코드 샘플:")
if '서비스_업종_코드' in df_store.columns:
    print(df_store['서비스_업종_코드'].head(10).tolist())
