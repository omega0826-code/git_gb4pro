import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("설립연도 및 운영연수 추출 작업 시작")
print("="*80)

# 데이터 로드
print("\n1. 데이터 로딩...")
df = pd.read_csv(
    r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_병원_통합_확장_2025.12.csv',
    encoding='utf-8-sig'
)
print(f"   - 총 레코드 수: {len(df):,}개")

# 현재 날짜 (2026-01-31 기준)
current_date = datetime(2026, 1, 31)
print(f"\n2. 기준 날짜: {current_date.strftime('%Y-%m-%d')}")

# 개설일자 파싱
print("\n3. 개설일자 파싱 중...")
df['개설일자_parsed'] = pd.to_datetime(df['개설일자'], format='%Y-%m-%d', errors='coerce')

# 파싱 결과 확인
parsed_count = df['개설일자_parsed'].notna().sum()
print(f"   - 파싱 성공: {parsed_count:,} / {len(df):,} ({parsed_count/len(df)*100:.2f}%)")

# 설립연도 추출
print("\n4. 설립연도 추출 중...")
df['설립연도'] = df['개설일자_parsed'].dt.year
df['설립연도'] = df['설립연도'].astype('Int64')  # nullable integer

# 설립연도 통계
print(f"   - 최소 연도: {df['설립연도'].min()}")
print(f"   - 최대 연도: {df['설립연도'].max()}")
print(f"   - 평균 연도: {df['설립연도'].mean():.0f}")
print(f"   - 결측치: {df['설립연도'].isna().sum()}")

# 운영연수 계산
print("\n5. 운영연수 계산 중...")
df['운영연수'] = (current_date - df['개설일자_parsed']).dt.days / 365.25
df['운영연수'] = df['운영연수'].round(1)

# 운영연수 통계
print(f"   - 최소 운영연수: {df['운영연수'].min():.1f}년")
print(f"   - 최대 운영연수: {df['운영연수'].max():.1f}년")
print(f"   - 평균 운영연수: {df['운영연수'].mean():.1f}년")
print(f"   - 결측치: {df['운영연수'].isna().sum()}")

# 병원연령대 재계산 (기존 로직 유지)
print("\n6. 병원연령대 재계산 중...")
def categorize_age(years):
    if pd.isna(years):
        return '정보없음'
    elif years < 5:
        return '신규 (5년 미만)'
    elif years < 10:
        return '성장기 (5-10년)'
    elif years < 20:
        return '중견 (10-20년)'
    elif years < 30:
        return '성숙 (20-30년)'
    else:
        return '노포 (30년 이상)'

df['병원연령대'] = df['운영연수'].apply(categorize_age)

# 병원연령대 분포
print("\n   병원연령대 분포:")
age_dist = df['병원연령대'].value_counts().sort_index()
for age_cat, count in age_dist.items():
    pct = count / len(df) * 100
    print(f"   - {age_cat}: {count:,}개 ({pct:.1f}%)")

# 샘플 데이터 확인
print("\n7. 샘플 데이터 확인 (처음 10개):")
sample_cols = ['요양기관명', '개설일자', '설립연도', '운영연수', '병원연령대']
print(df[sample_cols].head(10).to_string(index=False))

# 결과 저장
output_path = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_병원_통합_확장_수정_2025.12.csv'
print(f"\n8. 결과 저장 중...")
print(f"   - 저장 경로: {output_path}")

df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"   - 저장 완료!")

# 최종 통계
print("\n" + "="*80)
print("최종 통계")
print("="*80)
print(f"총 레코드 수: {len(df):,}개")
print(f"\n컬럼별 결측치:")
print(f"  - 개설일자_parsed: {df['개설일자_parsed'].isna().sum():,}개 ({df['개설일자_parsed'].isna().sum()/len(df)*100:.2f}%)")
print(f"  - 설립연도: {df['설립연도'].isna().sum():,}개 ({df['설립연도'].isna().sum()/len(df)*100:.2f}%)")
print(f"  - 운영연수: {df['운영연수'].isna().sum():,}개 ({df['운영연수'].isna().sum()/len(df)*100:.2f}%)")
print(f"  - 병원연령대: {(df['병원연령대'] == '정보없음').sum():,}개 ({(df['병원연령대'] == '정보없음').sum()/len(df)*100:.2f}%)")

print("\n" + "="*80)
print("작업 완료!")
print("="*80)
