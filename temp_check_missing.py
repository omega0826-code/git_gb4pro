import pandas as pd

# 데이터 로드
df = pd.read_csv(
    r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_병원_통합_확장_2025.12.csv',
    encoding='utf-8-sig'
)

# 결과를 파일로 저장
output_file = r'd:\git_gb4pro\missing_analysis_result.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f'총 레코드 수: {len(df)}\n')
    f.write(f'총 컬럼 수: {len(df.columns)}\n')
    f.write('\n' + '='*80 + '\n')
    
    # 결측치 비율 계산
    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    
    # 결측치 비율별 그룹화
    f.write('\n[결측치 비율별 컬럼 분류]\n')
    f.write(f'\n1. 결측치 90% 이상 (사실상 사용 불가): {(missing_pct >= 90).sum()}개\n')
    for col in missing_pct[missing_pct >= 90].index:
        f.write(f'   - {col}: {missing_pct[col]:.2f}%\n')
    
    f.write(f'\n2. 결측치 70~90% (제한적 사용): {((missing_pct >= 70) & (missing_pct < 90)).sum()}개\n')
    for col in missing_pct[(missing_pct >= 70) & (missing_pct < 90)].index:
        f.write(f'   - {col}: {missing_pct[col]:.2f}%\n')
    
    f.write(f'\n3. 결측치 30~70% (주의 필요): {((missing_pct >= 30) & (missing_pct < 70)).sum()}개\n')
    for col in missing_pct[(missing_pct >= 30) & (missing_pct < 70)].index:
        f.write(f'   - {col}: {missing_pct[col]:.2f}%\n')
    
    f.write(f'\n4. 결측치 10~30% (사용 가능): {((missing_pct >= 10) & (missing_pct < 30)).sum()}개\n')
    for col in missing_pct[(missing_pct >= 10) & (missing_pct < 30)].index:
        f.write(f'   - {col}: {missing_pct[col]:.2f}%\n')
    
    f.write(f'\n5. 결측치 10% 미만 (양호): {(missing_pct < 10).sum()}개\n')
    for col in missing_pct[missing_pct < 10].head(50).index:
        f.write(f'   - {col}: {missing_pct[col]:.2f}%\n')
    
    # 주요 분석 항목별 결측치 확인
    f.write('\n' + '='*80 + '\n')
    f.write('\n[주요 분석 카테고리별 결측치 현황]\n')
    
    categories = {
        '기본정보': ['요양기관명', '종별코드명', '시군구코드명', '주소', '개설일자', '설립구분코드명'],
        '인력정보': ['총의사수', '의과전문의 인원수', '의과일반의 인원수', '치과전문의 인원수', '한방전문의 인원수'],
        '병상정보': ['일반입원실일반병상수', '일반입원실상급병상수', '성인중환자병상수', '응급실병상수'],
        '운영정보': ['점심시간_평일', '점심시간_토요일', '진료시작시간_월요일', '진료종료시간_월요일'],
        '편의정보': ['주차_가능대수', '주차_비용 부담여부', '휴진안내_일요일', '휴진안내_공휴일'],
        '위치정보': ['좌표(X)', '좌표(Y)', '읍면동', '우편번호'],
        '장비정보': ['장비_CT_대수', '장비_초음파영상진단기_대수'],
        '진료과목': ['진료과목_개수', '진료과목_내과', '진료과목_외과', '진료과목_피부과'],
        '확장정보': ['설립연도', '운영연수', '병원연령대', '병원규모']
    }
    
    for cat_name, cols in categories.items():
        f.write(f'\n{cat_name}:\n')
        for col in cols:
            if col in df.columns:
                pct = missing_pct.get(col, 0)
                if pct < 10:
                    status = 'OK'
                elif pct < 30:
                    status = 'WARN'
                else:
                    status = 'BAD'
                f.write(f'  [{status}] {col}: {pct:.2f}%\n')
            else:
                f.write(f'  [NONE] {col}: 컬럼 없음\n')

print(f'분석 완료! 결과 파일: {output_file}')
