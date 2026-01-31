import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("강남구 '내과' 병원명 + 피부과 진료과목 병원 리스트")
print("="*80)

# 1. 데이터 로드
df_hospital = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/1.병원정보서비스(2025.12.).csv',
                          encoding='utf-8-sig')
df_dept = pd.read_csv('d:/git_gb4pro/data/전국 병의원 및 약국 현황 2025.12/CSV/5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
                      encoding='utf-8-sig')

# 2. 강남구 병원 추출
gangnam = df_hospital[df_hospital['시군구코드명']=='강남구'].copy()
print(f"\n[1] 강남구 전체 병원: {len(gangnam):,}개")

# 3. 피부과 진료과목 추출
derma_dept = df_dept[df_dept['진료과목코드명']=='피부과']
print(f"[2] 전국 피부과 레코드: {len(derma_dept):,}개")

# 4. 강남구 피부과 병원
gangnam_derma = gangnam.merge(derma_dept[['암호화요양기호', '진료과목코드명']], 
                               on='암호화요양기호', how='inner')
print(f"[3] 강남구 피부과 병원: {len(gangnam_derma):,}개")

# 5. 병원명에 "내과"가 포함된 병원
gangnam_derma_naegwa = gangnam_derma[gangnam_derma['요양기관명'].str.contains('내과', na=False)]
print(f"[4] 강남구 피부과 병원 중 병원명에 '내과' 포함: {len(gangnam_derma_naegwa):,}개")

# 6. 상세 리스트 생성
print(f"\n{'='*80}")
print(f"강남구 '내과' 병원명 + 피부과 진료 병원 리스트 (총 {len(gangnam_derma_naegwa):,}개)")
print(f"{'='*80}\n")

result_list = []

for idx, (_, row) in enumerate(gangnam_derma_naegwa.iterrows(), 1):
    hosp_id = row['암호화요양기호']
    hosp_name = row['요양기관명']
    hosp_address = row['주소']
    hosp_phone = row['전화번호']
    
    # 해당 병원의 모든 진료과목 조회
    hosp_all_depts = df_dept[df_dept['암호화요양기호']==hosp_id]
    dept_list = hosp_all_depts['진료과목코드명'].tolist()
    
    print(f"[{idx}] {hosp_name}")
    print(f"    주소: {hosp_address}")
    print(f"    전화: {hosp_phone}")
    print(f"    진료과목 ({len(dept_list)}개): {', '.join(dept_list)}")
    print()
    
    result_list.append({
        '순번': idx,
        '병원명': hosp_name,
        '주소': hosp_address,
        '전화번호': hosp_phone,
        '진료과목수': len(dept_list),
        '진료과목': ', '.join(dept_list)
    })

# 7. CSV 저장
result_df = pd.DataFrame(result_list)
output_file = '강남구_내과병원명_피부과진료_리스트.csv'
result_df.to_csv(output_file, encoding='utf-8-sig', index=False)

print(f"{'='*80}")
print(f"리스트가 '{output_file}' 파일로 저장되었습니다.")
print(f"{'='*80}")

# 8. 통계
print(f"\n[통계]")
print(f"  - 총 병원 수: {len(result_list):,}개")
print(f"  - 평균 진료과목 수: {result_df['진료과목수'].mean():.1f}개")
print(f"  - 최대 진료과목 수: {result_df['진료과목수'].max()}개")
print(f"  - 최소 진료과목 수: {result_df['진료과목수'].min()}개")

# 9. 진료과목 수 분포
print(f"\n[진료과목 수 분포]")
dept_count_dist = result_df['진료과목수'].value_counts().sort_index()
for count, freq in dept_count_dist.items():
    print(f"  {count}개 진료과목: {freq}개 병원")
