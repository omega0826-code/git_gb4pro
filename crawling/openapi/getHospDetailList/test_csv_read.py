"""
CSV 파일 읽기 테스트 스크립트
"""
import pandas as pd

csv_file = r"D:\git_gb4pro\crawling\openapi\getHospBasisList\(CSV)서울_강남구_피부과_20260113_205835.csv"

print("=" * 80)
print("CSV 파일 읽기 테스트")
print("=" * 80)
print()

# cp949 인코딩으로 시도
try:
    print("[시도 1] cp949 인코딩으로 읽기...")
    df = pd.read_csv(csv_file, encoding='cp949', nrows=3)
    print("✓ 성공!")
    print(f"\n총 컬럼 수: {len(df.columns)}")
    print(f"컬럼 목록:\n{df.columns.tolist()}")
    print(f"\n첫 3행 데이터:")
    print(df)
    
    # 요양기호 관련 컬럼 확인
    print("\n" + "=" * 80)
    print("요양기호 관련 컬럼 확인")
    print("=" * 80)
    possible_columns = ['ykiho', '암호화요양기호', '요양기호', 'YKIHO', 'ykiho_enc']
    found_columns = [col for col in possible_columns if col in df.columns]
    
    if found_columns:
        print(f"✓ 발견된 요양기호 컬럼: {found_columns}")
    else:
        print("✗ 요양기호 컬럼을 찾을 수 없습니다.")
        print(f"  현재 CSV 파일의 컬럼: {df.columns.tolist()}")
        
except Exception as e:
    print(f"✗ 실패: {e}")
    print("\n[시도 2] utf-8-sig 인코딩으로 읽기...")
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=3)
        print("✓ 성공!")
        print(f"\n총 컬럼 수: {len(df.columns)}")
        print(f"컬럼 목록:\n{df.columns.tolist()}")
        print(f"\n첫 3행 데이터:")
        print(df)
    except Exception as e2:
        print(f"✗ 실패: {e2}")
