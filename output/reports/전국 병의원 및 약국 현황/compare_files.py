import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("통합 파일 vs 원본 진료과목 파일 비교")
print("="*60)

# 1. 통합 파일 로드
print("\n[1] 통합 파일 로드 중...")
df_integrated = pd.read_csv('data_260131_0844/서울_병원_통합_2025.12.csv', encoding='utf-8-sig')
print(f"[OK] 통합 파일: {len(df_integrated):,}개 병원")
print(f"컬럼 수: {len(df_integrated.columns)}개")

# 2. 원본 진료과목 파일 로드
print("\n[2] 원본 진료과목 파일 로드 중...")
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv', 
                      encoding='utf-8-sig')
print(f"[OK] 진료과목 파일: {len(df_dept):,}개 레코드")

# 3. 통합 파일의 진료과목 관련 컬럼 확인
print("\n[3] 통합 파일의 진료과목 관련 컬럼:")
dept_cols = [col for col in df_integrated.columns if '진료' in col or '과목' in col]
for col in dept_cols:
    print(f"  - {col}")
    print(f"    샘플 값: {df_integrated[col].dropna().head(3).tolist()}")

# 4. 진료과목코드명 컬럼 존재 여부
print("\n[4] 진료과목 상세 정보 포함 여부:")
if '진료과목코드명' in df_integrated.columns:
    print("  ✓ '진료과목코드명' 컬럼 존재 - 상세 정보 포함됨")
    print(f"  - 고유 진료과목 수: {df_integrated['진료과목코드명'].nunique()}개")
    print(f"  - 피부과 병원 수: {len(df_integrated[df_integrated['진료과목코드명']=='피부과']):,}개")
else:
    print("  ✗ '진료과목코드명' 컬럼 없음 - 상세 정보 미포함")
    print("  → 통합 파일에는 집계된 정보만 있음 (진료과목_개수 등)")

# 5. 병원 정보 파일 로드 및 병합 테스트
print("\n[5] 병원 정보 파일과 진료과목 파일 병합 테스트...")
df_hospital = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/1.병원정보서비스(2025.12.).csv',
                          encoding='utf-8-sig')
print(f"[OK] 병원 정보: {len(df_hospital):,}개")

# 서울 병원만 추출
seoul_hospitals = df_hospital[df_hospital['시도코드명']=='서울'].copy()
print(f"[OK] 서울 병원: {len(seoul_hospitals):,}개")

# 피부과 진료과목 추출
derma_dept = df_dept[df_dept['진료과목코드명']=='피부과'].copy()
print(f"[OK] 전국 피부과 레코드: {len(derma_dept):,}개")

# 병합
seoul_derma = seoul_hospitals.merge(
    derma_dept[['암호화요양기호', '진료과목코드명']],
    on='암호화요양기호',
    how='inner'
)
print(f"[OK] 서울 피부과 병원: {len(seoul_derma):,}개")

# 강남구 피부과
gangnam_derma = seoul_derma[seoul_derma['시군구코드명']=='강남구']
print(f"[OK] 강남구 피부과 병원: {len(gangnam_derma):,}개")

print("\n" + "="*60)
print("결론:")
print("="*60)
print(f"1. 통합 파일에는 진료과목 '상세 정보'가 {'포함' if '진료과목코드명' in df_integrated.columns else '미포함'}되어 있습니다.")
print(f"2. 통합 파일에는 '진료과목_개수' 등 집계된 정보만 있습니다.")
print(f"3. 피부과 분석을 위해서는 원본 진료과목 파일을 사용해야 합니다.")
print(f"4. 원본 파일 기준 강남구 피부과: {len(gangnam_derma):,}개")
