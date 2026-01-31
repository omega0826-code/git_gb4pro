import pandas as pd
import os

# 강남구 데이터 파일 경로
gangnam_file = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_강남구_병원_2025.12.csv'

# 데이터 로드
df = pd.read_csv(gangnam_file, encoding='utf-8-sig')

# 기본 정보
print("=" * 80)
print("강남구 병원 데이터 요약")
print("=" * 80)
print(f"총 병원 수: {len(df):,}개")
print(f"컬럼 수: {len(df.columns)}개")
file_size = os.path.getsize(gangnam_file) / 1024 / 1024
print(f"파일 크기: {file_size:.1f} MB")

# 주요 통계
print("\n" + "=" * 80)
print("주요 통계")
print("=" * 80)

if '진료과목_개수' in df.columns:
    avg_subjects = df['진료과목_개수'].mean()
    print(f"평균 진료과목 수: {avg_subjects:.1f}개")

if '총의사수' in df.columns:
    total_doctors = df['총의사수'].sum()
    print(f"총 의사 수: {total_doctors:,.0f}명")

if '과목별전문의_총수' in df.columns:
    total_specialists = df['과목별전문의_총수'].sum()
    print(f"총 전문의 수: {total_specialists:,.0f}명")

# 종별 분포
print("\n" + "=" * 80)
print("종별 분포")
print("=" * 80)
if '종별코드명' in df.columns:
    type_dist = df['종별코드명'].value_counts()
    for type_name, count in type_dist.items():
        print(f"{type_name}: {count:,}개 ({count/len(df)*100:.1f}%)")

# 읍면동 분포 (상위 10개)
print("\n" + "=" * 80)
print("읍면동 분포 (상위 10개)")
print("=" * 80)
if '읍면동' in df.columns:
    dong_dist = df['읍면동'].value_counts().head(10)
    for dong, count in dong_dist.items():
        print(f"{dong}: {count:,}개")

print("\n" + "=" * 80)
print(f"파일 저장 위치: {gangnam_file}")
print("=" * 80)
