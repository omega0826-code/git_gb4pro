import pandas as pd
import sys

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("진료과목 정보 파일 검증")
print("="*60)

try:
    # 파일 로드
    file_path = 'd:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv'
    
    print(f"\n[1] 파일 로드 중...")
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    print(f"[OK] 파일 로드 성공")
    print(f"총 레코드 수: {len(df):,}개")
    print(f"총 컬럼 수: {len(df.columns)}개")
    
    # 컬럼 확인
    print(f"\n[2] 컬럼 목록:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # 진료과목코드명 확인
    if '진료과목코드명' in df.columns:
        print(f"\n[3] 진료과목코드명 분석:")
        print(f"  - 고유 진료과목 수: {df['진료과목코드명'].nunique()}개")
        print(f"\n  - 상위 20개 진료과목:")
        dept_counts = df['진료과목코드명'].value_counts().head(20)
        for dept, count in dept_counts.items():
            print(f"    {dept}: {count:,}개")
        
        # 피부과 확인
        print(f"\n[4] 피부과 데이터 확인:")
        derma_data = df[df['진료과목코드명']=='피부과']
        print(f"  - 피부과 레코드 수: {len(derma_data):,}개")
        
        if len(derma_data) > 0:
            print(f"\n  - 피부과 샘플 데이터 (처음 5개):")
            print(derma_data.head())
            
            # 서울 피부과 확인
            if '시도코드명' in df.columns:
                seoul_derma = derma_data[derma_data['시도코드명']=='서울']
                print(f"\n  - 서울 피부과 레코드 수: {len(seoul_derma):,}개")
        else:
            print("  [경고] 피부과 데이터가 없습니다!")
            print("\n  - 진료과목명에 '피부' 포함된 항목 검색:")
            skin_related = df[df['진료과목코드명'].str.contains('피부', na=False)]
            print(f"    발견된 레코드 수: {len(skin_related):,}개")
            if len(skin_related) > 0:
                print(f"    진료과목명: {skin_related['진료과목코드명'].unique()}")
    else:
        print("\n[오류] '진료과목코드명' 컬럼이 없습니다!")
    
    # 데이터 샘플 저장
    print(f"\n[5] 샘플 데이터 저장 중...")
    df.head(100).to_csv('dept_sample.csv', encoding='utf-8-sig', index=False)
    print(f"[OK] dept_sample.csv 저장 완료")
    
except Exception as e:
    print(f"\n[오류 발생]")
    print(f"오류 내용: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("검증 완료")
print("="*60)
