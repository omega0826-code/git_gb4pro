import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("진료과목 데이터 구조 상세 분석")
print("="*80)

# 1. 진료과목 파일 로드
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
                      encoding='utf-8-sig')

print(f"\n[1] 기본 정보:")
print(f"  - 총 레코드 수: {len(df_dept):,}개")
print(f"  - 고유 병원 수: {df_dept['암호화요양기호'].nunique():,}개")
print(f"  - 평균 진료과목 수: {len(df_dept) / df_dept['암호화요양기호'].nunique():.2f}개/병원")

# 2. 컬럼 확인
print(f"\n[2] 컬럼 목록:")
for i, col in enumerate(df_dept.columns, 1):
    print(f"  {i}. {col}")

# 3. 샘플 데이터 - 한 병원의 여러 진료과목
print(f"\n[3] 샘플: 한 병원의 여러 진료과목 (처음 발견된 병원)")
sample_hospital = df_dept['암호화요양기호'].iloc[0]
sample_data = df_dept[df_dept['암호화요양기호']==sample_hospital]
print(f"  - 병원명: {sample_data['요양기관명'].iloc[0]}")
print(f"  - 진료과목 수: {len(sample_data)}개")
print(f"  - 진료과목 목록:")
for idx, row in sample_data.iterrows():
    print(f"    {row['진료과목코드명']}")

# 4. 피부과 데이터 확인
print(f"\n[4] 피부과 데이터 분석:")
derma_data = df_dept[df_dept['진료과목코드명']=='피부과']
print(f"  - 피부과 레코드 수: {len(derma_data):,}개")
print(f"  - 피부과를 운영하는 고유 병원 수: {derma_data['암호화요양기호'].nunique():,}개")

# 5. 피부과 + 다른 과목 운영하는 병원 샘플
print(f"\n[5] 피부과 + 다른 진료과목을 함께 운영하는 병원 샘플:")
derma_hospitals = derma_data['암호화요양기호'].unique()[:5]
for i, hosp_id in enumerate(derma_hospitals, 1):
    hosp_data = df_dept[df_dept['암호화요양기호']==hosp_id]
    print(f"\n  [{i}] {hosp_data['요양기관명'].iloc[0]}")
    print(f"      진료과목: {', '.join(hosp_data['진료과목코드명'].tolist())}")

# 6. 병원명에 "내과"가 있지만 피부과 진료과목이 있는 경우
print(f"\n[6] 병원명에 '내과'가 있지만 피부과 진료과목도 있는 병원:")
derma_with_naegwa_name = derma_data[derma_data['요양기관명'].str.contains('내과', na=False)]
print(f"  - 해당 병원 수: {derma_with_naegwa_name['암호화요양기호'].nunique():,}개")
if len(derma_with_naegwa_name) > 0:
    print(f"\n  샘플 (처음 5개):")
    for idx, (_, row) in enumerate(derma_with_naegwa_name.head(5).iterrows(), 1):
        hosp_id = row['암호화요양기호']
        hosp_all_depts = df_dept[df_dept['암호화요양기호']==hosp_id]
        print(f"  [{idx}] {row['요양기관명']}")
        print(f"      전체 진료과목: {', '.join(hosp_all_depts['진료과목코드명'].tolist())}")

# 7. 병원 정보와 병합 테스트
print(f"\n[7] 병원 정보와 병합 방식 비교:")
df_hospital = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/1.병원정보서비스(2025.12.).csv',
                          encoding='utf-8-sig')
seoul_hospitals = df_hospital[df_hospital['시도코드명']=='서울'].copy()

# 방법 1: inner join (제가 사용한 방법) - 문제 있음!
derma_dept_only = df_dept[df_dept['진료과목코드명']=='피부과']
method1 = seoul_hospitals.merge(derma_dept_only[['암호화요양기호', '진료과목코드명']], 
                                 on='암호화요양기호', how='inner')
print(f"\n  방법 1 (inner join - 피부과 레코드만):")
print(f"    - 결과: {len(method1):,}개 병원")
print(f"    - 문제: 피부과를 운영하는 병원만 추출 (정확함)")

# 방법 2: 피부과가 있는 병원 ID만 추출 후 필터링
derma_hospital_ids = derma_dept_only['암호화요양기호'].unique()
method2 = seoul_hospitals[seoul_hospitals['암호화요양기호'].isin(derma_hospital_ids)]
print(f"\n  방법 2 (피부과 운영 병원 ID 기준 필터링):")
print(f"    - 결과: {len(method2):,}개 병원")
print(f"    - 고유 병원 수: {method2['암호화요양기호'].nunique():,}개")

print(f"\n  → 두 방법 모두 동일한 결과: {len(method1) == len(method2)}")

# 8. 강남구 피부과 상세 확인
gangnam_derma = method2[method2['시군구코드명']=='강남구']
print(f"\n[8] 강남구 피부과 병원 상세:")
print(f"  - 총 {len(gangnam_derma):,}개")
print(f"\n  샘플 (처음 10개):")
for idx, (_, row) in enumerate(gangnam_derma.head(10).iterrows(), 1):
    hosp_id = row['암호화요양기호']
    hosp_depts = df_dept[df_dept['암호화요양기호']==hosp_id]
    dept_list = hosp_depts['진료과목코드명'].tolist()
    print(f"  [{idx}] {row['요양기관명']}")
    print(f"      진료과목 ({len(dept_list)}개): {', '.join(dept_list[:5])}{' ...' if len(dept_list) > 5 else ''}")

print("\n" + "="*80)
print("결론:")
print("="*80)
print("1. 진료과목 파일은 1:N 관계로, 한 병원이 여러 행에 나타납니다.")
print("2. 피부과 레코드(17,769개)는 피부과를 운영하는 병원 수가 아닙니다.")
print(f"3. 실제 피부과를 운영하는 고유 병원 수: {derma_data['암호화요양기호'].nunique():,}개")
print(f"4. 서울 피부과 병원: {len(method2):,}개")
print(f"5. 강남구 피부과 병원: {len(gangnam_derma):,}개")
print("6. 병원명에 '내과'가 있어도 피부과 진료과목을 함께 운영할 수 있습니다.")
print("   → 이는 정상적인 데이터입니다 (종합병원, 다과목 의원 등)")
