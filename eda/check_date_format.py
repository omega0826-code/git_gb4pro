import pandas as pd
import numpy as np
from datetime import datetime

# 데이터 로드
df = pd.read_csv(
    r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_병원_통합_확장_2025.12.csv',
    encoding='utf-8-sig'
)

print("="*80)
print("개설일자 컬럼 분석")
print("="*80)

# 개설일자 컬럼 확인
print(f"\n1. 개설일자 컬럼 기본 정보:")
print(f"   - 데이터 타입: {df['개설일자'].dtype}")
print(f"   - 결측치 수: {df['개설일자'].isnull().sum()}")
print(f"   - 결측치 비율: {df['개설일자'].isnull().sum() / len(df) * 100:.2f}%")

# 샘플 데이터 확인
print(f"\n2. 개설일자 샘플 (처음 20개):")
print(df['개설일자'].head(20).to_string())

# 개설일자 형식 분석
print(f"\n3. 개설일자 형식 분석:")
sample_dates = df['개설일자'].dropna().head(100)
for i, date in enumerate(sample_dates):
    if i < 10:
        print(f"   - {date} (타입: {type(date)}, 길이: {len(str(date))})")

# 기존 확장 컬럼 확인
print(f"\n4. 기존 확장 컬럼 상태:")
print(f"   - 개설일자_parsed: {df['개설일자_parsed'].isnull().sum()} / {len(df)} (결측치)")
print(f"   - 설립연도: {df['설립연도'].isnull().sum()} / {len(df)} (결측치)")
print(f"   - 운영연수: {df['운영연수'].isnull().sum()} / {len(df)} (결측치)")

# 개설일자 파싱 테스트
print(f"\n5. 개설일자 파싱 테스트:")

def parse_date(date_str):
    """개설일자를 파싱하여 datetime 객체로 변환"""
    if pd.isnull(date_str):
        return None
    
    date_str = str(date_str).strip()
    
    # 다양한 형식 시도
    formats = [
        '%Y-%m-%d',  # 2019-12-30
        '%Y.%m.%d',  # 2019.12.30
        '%Y/%m/%d',  # 2019/12/30
        '%Y%m%d',    # 20191230
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    
    # pandas의 자동 파싱 시도
    try:
        return pd.to_datetime(date_str)
    except:
        return None

# 테스트 파싱
test_sample = df['개설일자'].dropna().head(100)
parsed_count = 0
failed_count = 0
failed_samples = []

for date in test_sample:
    parsed = parse_date(date)
    if parsed is not None:
        parsed_count += 1
    else:
        failed_count += 1
        if len(failed_samples) < 5:
            failed_samples.append(date)

print(f"   - 성공: {parsed_count} / {len(test_sample)}")
print(f"   - 실패: {failed_count} / {len(test_sample)}")
if failed_samples:
    print(f"   - 실패 샘플: {failed_samples}")

# 현재 날짜
current_date = datetime.now()
print(f"\n6. 현재 날짜: {current_date.strftime('%Y-%m-%d')}")

print("\n" + "="*80)
print("분석 완료!")
