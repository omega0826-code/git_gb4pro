"""
출력 파일 검증 스크립트
"""
import pandas as pd
from pathlib import Path
import sys

# UTF-8 출력 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 가장 최근 CSV 파일 찾기
data_dir = Path('data')
csv_files = sorted(data_dir.glob('병원상세정보_*.csv'), reverse=True)

if not csv_files:
    print("CSV 파일을 찾을 수 없습니다.")
    exit(1)

latest_csv = csv_files[0]
print(f"검증 파일: {latest_csv.name}")
print("=" * 80)

# CSV 파일 읽기
df = pd.read_csv(latest_csv, encoding='utf-8-sig')

# 기본 정보
print(f"\n총 레코드 수: {len(df):,}건")
print(f"총 컬럼 수: {len(df.columns)}개")

# 필수 컬럼 확인
required_columns = ['원본_기관코드', '원본_병원명', '원본_주소']
print(f"\n필수 컬럼 확인:")
for col in required_columns:
    exists = col in df.columns
    status = "[O]" if exists else "[X]"
    print(f"  {status} {col}: {exists}")
    if exists:
        non_null_count = df[col].notna().sum()
        null_count = df[col].isna().sum()
        print(f"     - 비어있지 않음: {non_null_count}건")
        print(f"     - 비어있음: {null_count}건")

# 첫 3개 컬럼 출력
print(f"\n처음 5개 컬럼:")
for i, col in enumerate(df.columns[:5], 1):
    print(f"  {i}. {col}")

# 원본 데이터 샘플 출력
if all(col in df.columns for col in required_columns):
    print(f"\n원본 데이터 샘플 (처음 3건):")
    print("-" * 80)
    for idx, row in df[required_columns].head(3).iterrows():
        print(f"\n[{idx+1}]")
        print(f"  원본_기관코드: {str(row['원본_기관코드'])[:50]}...")
        print(f"  원본_병원명: {row['원본_병원명']}")
        print(f"  원본_주소: {row['원본_주소']}")

# 메타데이터 파일 확인
md_file = latest_csv.with_suffix('.md')
if md_file.exists():
    print(f"\n✓ 메타데이터 파일 존재: {md_file.name}")
else:
    print(f"\n✗ 메타데이터 파일 없음")

print("\n" + "=" * 80)
print("검증 완료!")
