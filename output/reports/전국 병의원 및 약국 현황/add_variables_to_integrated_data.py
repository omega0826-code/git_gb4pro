"""
서울 병원 통합 데이터 변수 추가 스크립트
작성일: 2026-01-31
목적: 
1. 설립연도 컬럼 추가 (개설일자 기반)
2. 진료과목별 플래그 컬럼 추가 (GIS 활용)
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("서울 병원 통합 데이터 변수 추가")
print("="*80)

# ============================================================================
# 1. 데이터 로드
# ============================================================================
print("\n[1/5] 데이터 로드 중...")

# 통합 데이터
df_integrated = pd.read_csv('d:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/data_260131_0844/서울_병원_통합_2025.12.csv',
                            encoding='utf-8-sig')

# 진료과목 원본 데이터
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
                      encoding='utf-8-sig')

print(f"[OK] 통합 데이터: {len(df_integrated):,}개 병원")
print(f"[OK] 진료과목 데이터: {len(df_dept):,}개 레코드")

# ============================================================================
# 2. 설립연도 컬럼 추가
# ============================================================================
print("\n[2/5] 설립연도 컬럼 추가...")

# 개설일자 파싱
df_integrated['개설일자_parsed'] = pd.to_datetime(df_integrated['개설일자'], format='%Y%m%d', errors='coerce')
df_integrated['설립연도'] = df_integrated['개설일자_parsed'].dt.year
df_integrated['운영연수'] = 2025 - df_integrated['설립연도']

# 연령대 분류
def categorize_hospital_age(years):
    if pd.isna(years):
        return '정보없음'
    elif years < 3:
        return '신규 (0-2년)'
    elif years < 5:
        return '초기 (3-4년)'
    elif years < 10:
        return '성장기 (5-9년)'
    elif years < 20:
        return '성숙기 (10-19년)'
    else:
        return '노포 (20년 이상)'

df_integrated['병원연령대'] = df_integrated['운영연수'].apply(categorize_hospital_age)

valid_dates = df_integrated['설립연도'].notna().sum()
print(f"[OK] 설립연도 정보 있음: {valid_dates:,}개 ({valid_dates/len(df_integrated)*100:.1f}%)")
print(f"     평균 운영연수: {df_integrated['운영연수'].mean():.1f}년")

# ============================================================================
# 3. 진료과목별 플래그 컬럼 추가
# ============================================================================
print("\n[3/5] 진료과목별 플래그 컬럼 추가...")

# 서울 병원의 진료과목 데이터만 추출
seoul_hospital_ids = df_integrated['암호화요양기호'].unique()
df_dept_seoul = df_dept[df_dept['암호화요양기호'].isin(seoul_hospital_ids)]

# 진료과목 목록
dept_list = df_dept_seoul['진료과목코드명'].unique()
print(f"[INFO] 전체 진료과목 종류: {len(dept_list)}개")
print(f"       {', '.join(sorted(dept_list))}")

# 각 진료과목별 플래그 컬럼 생성
for dept in sorted(dept_list):
    # 해당 진료과목을 가진 병원 ID 추출
    dept_hospital_ids = df_dept_seoul[df_dept_seoul['진료과목코드명']==dept]['암호화요양기호'].unique()
    
    # 플래그 컬럼 생성 (1: 있음, 0: 없음)
    col_name = f'진료과목_{dept}'
    df_integrated[col_name] = df_integrated['암호화요양기호'].isin(dept_hospital_ids).astype(int)
    
    count = df_integrated[col_name].sum()
    print(f"  - {col_name}: {count:,}개 병원 ({count/len(df_integrated)*100:.1f}%)")

# ============================================================================
# 4. 추가 파생 변수 생성
# ============================================================================
print("\n[4/5] 추가 파생 변수 생성...")

# 4.1 주요 진료과목 그룹 플래그
df_integrated['진료과목_내과계'] = (
    (df_integrated.get('진료과목_내과', 0) == 1) |
    (df_integrated.get('진료과목_신경과', 0) == 1) |
    (df_integrated.get('진료과목_정신건강의학과', 0) == 1) |
    (df_integrated.get('진료과목_결핵과', 0) == 1)
).astype(int)

df_integrated['진료과목_외과계'] = (
    (df_integrated.get('진료과목_외과', 0) == 1) |
    (df_integrated.get('진료과목_정형외과', 0) == 1) |
    (df_integrated.get('진료과목_신경외과', 0) == 1) |
    (df_integrated.get('진료과목_흉부외과', 0) == 1) |
    (df_integrated.get('진료과목_성형외과', 0) == 1)
).astype(int)

df_integrated['진료과목_미용계'] = (
    (df_integrated.get('진료과목_피부과', 0) == 1) |
    (df_integrated.get('진료과목_성형외과', 0) == 1)
).astype(int)

print(f"  - 내과계: {df_integrated['진료과목_내과계'].sum():,}개")
print(f"  - 외과계: {df_integrated['진료과목_외과계'].sum():,}개")
print(f"  - 미용계: {df_integrated['진료과목_미용계'].sum():,}개")

# 4.2 병원 규모 분류
def categorize_hospital_size(row):
    doctors = row.get('총의사수', 0)
    if pd.isna(doctors) or doctors == 0:
        return '정보없음'
    elif doctors == 1:
        return '소형 (1인)'
    elif doctors <= 3:
        return '중소형 (2-3인)'
    elif doctors <= 10:
        return '중형 (4-10인)'
    else:
        return '대형 (11인 이상)'

df_integrated['병원규모'] = df_integrated.apply(categorize_hospital_size, axis=1)

size_dist = df_integrated['병원규모'].value_counts()
print(f"\n  병원 규모 분류:")
for size, count in size_dist.items():
    print(f"    {size}: {count:,}개 ({count/len(df_integrated)*100:.1f}%)")

# ============================================================================
# 5. 데이터 저장
# ============================================================================
print("\n[5/5] 데이터 저장 중...")

output_path = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/data_260131_0844/서울_병원_통합_확장_2025.12.csv'
df_integrated.to_csv(output_path, encoding='utf-8-sig', index=False)

print(f"[OK] 저장 완료: {output_path}")
print(f"     총 컬럼 수: {len(df_integrated.columns)}개")
print(f"     총 레코드 수: {len(df_integrated):,}개")

# 새로 추가된 컬럼 목록
new_columns = [
    '개설일자_parsed', '설립연도', '운영연수', '병원연령대',
    '병원규모', '진료과목_내과계', '진료과목_외과계', '진료과목_미용계'
] + [f'진료과목_{dept}' for dept in sorted(dept_list)]

print(f"\n[추가된 컬럼] {len(new_columns)}개:")
for i, col in enumerate(new_columns, 1):
    print(f"  {i}. {col}")

print("\n" + "="*80)
print("변수 추가 완료!")
print("="*80)
