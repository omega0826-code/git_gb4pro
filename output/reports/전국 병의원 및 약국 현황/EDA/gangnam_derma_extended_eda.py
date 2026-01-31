"""
강남구 피부과 확장 EDA - 1순위 분석 통합 스크립트
작성일: 2026-01-31
분석 항목:
1. 병원 연령 분포 및 신규 진입 트렌드
2. 종별/규모별 경쟁 구도
3. 영업시간 및 접근성 전략
4. 주차 및 교통 접근성
5. 동별 밀집도 및 공백 지역
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 나노 바나나 컬러 팔레트
BG_COLOR = '#0F0F0F'
PRIMARY_COLOR = '#DFFF00'
SECONDARY_COLOR = '#FFFFFF'
ACCENT_COLOR = '#333333'

print("="*80)
print("강남구 피부과 확장 EDA - 1순위 분석")
print("="*80)

# ============================================================================
# 1. 데이터 로드
# ============================================================================
print("\n[1/6] 데이터 로드 중...")

# 병원 기본 정보
df_hospital = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/1.병원정보서비스(2025.12.).csv',
                          encoding='utf-8-sig')

# 진료과목 정보
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
                      encoding='utf-8-sig')

# 통합 데이터 (시설, 세부 정보 포함)
df_integrated = pd.read_csv('d:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/data_260131_0844/서울_병원_통합_2025.12.csv',
                            encoding='utf-8-sig')

print(f"[OK] 병원 정보: {len(df_hospital):,}개")
print(f"[OK] 진료과목 정보: {len(df_dept):,}개 레코드")
print(f"[OK] 통합 데이터: {len(df_integrated):,}개")

# ============================================================================
# 2. 강남구 피부과 병원 추출
# ============================================================================
print("\n[2/6] 강남구 피부과 병원 추출 중...")

# 서울 병원
seoul_hospitals = df_hospital[df_hospital['시도코드명']=='서울'].copy()

# 피부과 진료과목
derma_dept = df_dept[df_dept['진료과목코드명']=='피부과']

# 서울 피부과 병원
seoul_derma = seoul_hospitals.merge(derma_dept[['암호화요양기호', '진료과목코드명']], 
                                     on='암호화요양기호', how='inner')

# 강남구 피부과
gangnam_derma = seoul_derma[seoul_derma['시군구코드명']=='강남구'].copy()

# 통합 데이터와 병합 (시설, 세부 정보 추가)
gangnam_derma_full = gangnam_derma.merge(
    df_integrated[['암호화요양기호', '설립구분코드명', '주차_가능대수', '교통편_개수',
                   '진료시작시간_월요일', '진료종료시간_월요일', '진료시작시간_토요일', 
                   '진료종료시간_토요일', '진료시작시간_일요일', '휴진안내_일요일',
                   '진료과목_개수', '과목별전문의_총수']],
    on='암호화요양기호',
    how='left'
)

print(f"[OK] 강남구 피부과 병원: {len(gangnam_derma_full):,}개")

# ============================================================================
# 3. 분석 1: 병원 연령 분포 및 신규 진입 트렌드
# ============================================================================
print("\n[3/6] 분석 1: 병원 연령 분포...")

# 개설일자 파싱
gangnam_derma_full['개설일자_parsed'] = pd.to_datetime(gangnam_derma_full['개설일자'], format='%Y%m%d', errors='coerce')
gangnam_derma_full['개설연도'] = gangnam_derma_full['개설일자_parsed'].dt.year
gangnam_derma_full['운영연수'] = 2025 - gangnam_derma_full['개설연도']

# 통계
valid_dates = gangnam_derma_full['개설연도'].notna()
print(f"  - 개설일자 정보 있음: {valid_dates.sum():,}개")
print(f"  - 평균 운영연수: {gangnam_derma_full[valid_dates]['운영연수'].mean():.1f}년")
print(f"  - 중앙값 운영연수: {gangnam_derma_full[valid_dates]['운영연수'].median():.0f}년")

# 연령대별 분류
def categorize_age(years):
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

gangnam_derma_full['병원연령대'] = gangnam_derma_full['운영연수'].apply(categorize_age)

age_dist = gangnam_derma_full['병원연령대'].value_counts()
print("\n  병원 연령대 분포:")
for age_group, count in age_dist.items():
    pct = count / len(gangnam_derma_full) * 100
    print(f"    {age_group}: {count}개 ({pct:.1f}%)")

# 최근 5년 신규 개원 트렌드
recent_5years = gangnam_derma_full[gangnam_derma_full['개설연도'] >= 2020]
yearly_new = recent_5years.groupby('개설연도').size()
print(f"\n  최근 5년 신규 개원:")
for year, count in yearly_new.items():
    print(f"    {int(year)}년: {count}개")

# ============================================================================
# 4. 분석 2: 종별/규모별 경쟁 구도
# ============================================================================
print("\n[4/6] 분석 2: 종별/규모별 경쟁 구도...")

# 종별 분포
type_dist = gangnam_derma_full['종별코드명'].value_counts()
print("\n  종별 분포:")
for type_name, count in type_dist.items():
    pct = count / len(gangnam_derma_full) * 100
    print(f"    {type_name}: {count}개 ({pct:.1f}%)")

# 진료과목 수 분포
dept_count_dist = gangnam_derma_full['진료과목_개수'].value_counts().sort_index()
single_dept = (gangnam_derma_full['진료과목_개수'] == 1).sum()
multi_dept = (gangnam_derma_full['진료과목_개수'] > 1).sum()

print(f"\n  진료과목 수:")
print(f"    단일 진료과목: {single_dept}개 ({single_dept/len(gangnam_derma_full)*100:.1f}%)")
print(f"    다과목 (2개 이상): {multi_dept}개 ({multi_dept/len(gangnam_derma_full)*100:.1f}%)")
print(f"    평균 진료과목 수: {gangnam_derma_full['진료과목_개수'].mean():.1f}개")

# 의사 수 분포
doctor_dist = gangnam_derma_full['총의사수'].value_counts().sort_index().head(10)
print(f"\n  의사 수 분포 (상위 10개):")
for doc_count, freq in doctor_dist.items():
    pct = freq / len(gangnam_derma_full) * 100
    print(f"    {int(doc_count)}명: {freq}개 ({pct:.1f}%)")

# ============================================================================
# 5. 분석 3: 영업시간 및 접근성 전략
# ============================================================================
print("\n[5/6] 분석 3: 영업시간 및 접근성 전략...")

# 야간 진료 (20시 이후)
gangnam_derma_full['야간진료_평일'] = gangnam_derma_full['진료종료시간_월요일'] >= 2000
gangnam_derma_full['야간진료_토요일'] = gangnam_derma_full['진료종료시간_토요일'] >= 2000

night_weekday = gangnam_derma_full['야간진료_평일'].sum()
night_saturday = gangnam_derma_full['야간진료_토요일'].sum()

print(f"  야간 진료 (20시 이후):")
print(f"    평일: {night_weekday}개 ({night_weekday/len(gangnam_derma_full)*100:.1f}%)")
print(f"    토요일: {night_saturday}개 ({night_saturday/len(gangnam_derma_full)*100:.1f}%)")

# 주말 진료
sunday_open = (gangnam_derma_full['진료시작시간_일요일'] > 0).sum()
print(f"    일요일: {sunday_open}개 ({sunday_open/len(gangnam_derma_full)*100:.1f}%)")

# 평균 영업시간
avg_start = gangnam_derma_full[gangnam_derma_full['진료시작시간_월요일'] > 0]['진료시작시간_월요일'].mean()
avg_end = gangnam_derma_full[gangnam_derma_full['진료종료시간_월요일'] > 0]['진료종료시간_월요일'].mean()

print(f"\n  평일 평균 영업시간:")
print(f"    시작: {int(avg_start//100):02d}:{int(avg_start%100):02d}")
print(f"    종료: {int(avg_end//100):02d}:{int(avg_end%100):02d}")

# ============================================================================
# 6. 분석 4: 주차 및 교통 접근성
# ============================================================================
print("\n[6/6] 분석 4: 주차 및 교통 접근성...")

# 주차 가능 병원
parking_available = (gangnam_derma_full['주차_가능대수'] > 0).sum()
avg_parking = gangnam_derma_full[gangnam_derma_full['주차_가능대수'] > 0]['주차_가능대수'].mean()

print(f"  주차:")
print(f"    주차 가능 병원: {parking_available}개 ({parking_available/len(gangnam_derma_full)*100:.1f}%)")
print(f"    평균 주차 가능 대수: {avg_parking:.1f}대")

# 교통편
traffic_available = (gangnam_derma_full['교통편_개수'] > 0).sum()
avg_traffic = gangnam_derma_full[gangnam_derma_full['교통편_개수'] > 0]['교통편_개수'].mean()

print(f"  교통편:")
print(f"    교통편 정보 있음: {traffic_available}개 ({traffic_available/len(gangnam_derma_full)*100:.1f}%)")
print(f"    평균 교통편 개수: {avg_traffic:.1f}개")

# ============================================================================
# 7. 분석 5: 동별 밀집도
# ============================================================================
print("\n[추가] 분석 5: 동별 밀집도...")

dong_dist = gangnam_derma_full['읍면동'].value_counts().head(10)
print(f"  동별 피부과 병원 수 (상위 10개):")
for dong, count in dong_dist.items():
    pct = count / len(gangnam_derma_full) * 100
    print(f"    {dong}: {count}개 ({pct:.1f}%)")

# ============================================================================
# 8. 데이터 저장
# ============================================================================
print("\n[저장] 분석 데이터 저장 중...")

output_dir = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/EDA/EDA_강남구_피부과_확장분석_20260131'
import os
os.makedirs(output_dir, exist_ok=True)
os.makedirs(f'{output_dir}/data', exist_ok=True)

# 분석 데이터 저장
gangnam_derma_full.to_csv(f'{output_dir}/data/강남구_피부과_확장분석_데이터.csv', 
                          encoding='utf-8-sig', index=False)

# 요약 통계 저장
summary_stats = {
    '총_병원수': len(gangnam_derma_full),
    '평균_운영연수': gangnam_derma_full[valid_dates]['운영연수'].mean(),
    '신규_3년이내': (gangnam_derma_full['운영연수'] < 3).sum(),
    '노포_20년이상': (gangnam_derma_full['운영연수'] >= 20).sum(),
    '다과목_병원': multi_dept,
    '야간진료_평일': night_weekday,
    '주말진료_일요일': sunday_open,
    '주차가능_병원': parking_available,
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv(f'{output_dir}/data/요약통계.csv', encoding='utf-8-sig', index=False)

print(f"[OK] 데이터 저장 완료: {output_dir}")

print("\n" + "="*80)
print("1순위 분석 완료!")
print("="*80)
print(f"\n다음 단계: 시각화 및 리포트 작성")
