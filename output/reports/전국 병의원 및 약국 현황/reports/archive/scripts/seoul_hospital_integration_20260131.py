"""
서울 병의원 및 약국 데이터 통합 스크립트
- 12개 CSV 파일에서 서울 데이터만 추출
- 가이드라인에 따라 1:1, 1:N 관계 처리
- 검증 및 리포트 생성
"""

import pandas as pd
import os
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 설정
# ============================================================================

# 경로 설정
DATA_DIR = r'd:\git_gb4pro\data\전국 병의원 및 약국 현황 2025.12\CSV'
OUTPUT_DIR = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844'
REPORT_DIR = r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\reports_260131_0844'

# 출력 디렉토리 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# 파일 목록
FILES = {
    'hospital': '1.병원정보서비스(2025.12.).csv',
    'pharmacy': '2.약국정보서비스(2025.12.).csv',
    'facility': '3.의료기관별상세정보서비스_01_시설정보 2025.12..csv',
    'detail': '4.의료기관별상세정보서비스_02_세부정보 2025.12..csv',
    'subject': '5.의료기관별상세정보서비스_03_진료과목정보 2025.12..csv',
    'traffic': '6.의료기관별상세정보서비스_04_교통정보 2025.12..csv',
    'equipment': '7.의료기관별상세정보서비스_05_의료장비정보 2025.12..csv',
    'meal': '8.의료기관별상세정보서비스_06_식대가산정보 2025.12..csv',
    'nursing': '9.의료기관별상세정보서비스_07_간호등급정보 2025.12..csv',
    'special': '10.의료기관별상세정보서비스_08_특수진료정보서비스 2025.12..csv',
    'specialized': '11.의료기관별상세정보서비스_09_전문병원지정분야 2025.12..csv',
    'staff': '12.의료기관별상세정보서비스_10_기타인력정보 2025.12..csv'
}

# 로그 저장
logs = []

def log(message, level='INFO'):
    """로그 메시지 출력 및 저장"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    logs.append(log_msg)

# ============================================================================
# 1단계: 데이터 로드 및 서울 필터링
# ============================================================================

def load_and_filter_seoul():
    """CSV 파일 로드 및 서울 데이터 필터링"""
    log("=" * 80)
    log("1단계: 데이터 로드 및 서울 필터링 시작")
    log("=" * 80)
    
    data = {}
    seoul_data = {}
    
    for key, filename in FILES.items():
        filepath = os.path.join(DATA_DIR, filename)
        
        try:
            # CSV 로드
            df = pd.read_csv(filepath, encoding='utf-8-sig')
            data[key] = df
            log(f"로드 완료: {key} - {len(df):,}행 × {len(df.columns)}열")
            
            # 서울 필터링 (시도코드명 컬럼이 있는 경우)
            if '시도코드명' in df.columns:
                df_seoul = df[df['시도코드명'].str.contains('서울', na=False)].copy()
                seoul_data[key] = df_seoul
                log(f"  -> 서울 필터링: {len(df_seoul):,}행")
            else:
                # 시도코드명이 없는 경우 (1:N 관계 파일)
                # 나중에 병합 키로 필터링
                seoul_data[key] = df
                log(f"  -> 시도코드명 없음 (나중에 필터링)")
                
        except Exception as e:
            log(f"에러 발생: {key} - {str(e)}", 'ERROR')
            raise
    
    log("")
    return data, seoul_data

# ============================================================================
# 2단계: 1:1 관계 병합
# ============================================================================

def merge_one_to_one(seoul_data):
    """1:1 관계 파일 병합"""
    log("=" * 80)
    log("2단계: 1:1 관계 병합 시작")
    log("=" * 80)
    
    # 병원정보를 기준으로 시작
    df_base = seoul_data['hospital'].copy()
    log(f"기준 데이터: 병원정보 - {len(df_base):,}행")
    
    # 시설정보 병합
    if len(seoul_data['facility']) > 0:
        before = len(df_base)
        df_base = df_base.merge(
            seoul_data['facility'],
            on='암호화요양기호',
            how='left',
            suffixes=('', '_시설')
        )
        log(f"시설정보 병합: {before:,}행 -> {len(df_base):,}행")
    
    # 세부정보 병합
    if len(seoul_data['detail']) > 0:
        before = len(df_base)
        df_base = df_base.merge(
            seoul_data['detail'],
            on='암호화요양기호',
            how='left',
            suffixes=('', '_세부')
        )
        log(f"세부정보 병합: {before:,}행 -> {len(df_base):,}행")
    
    log(f"1:1 병합 완료: 총 {len(df_base):,}행 × {len(df_base.columns)}열")
    log("")
    return df_base

# ============================================================================
# 3단계: 1:N 관계 처리
# ============================================================================

def process_one_to_many(df_base, seoul_data):
    """1:N 관계 파일 처리 (집계/피벗)"""
    log("=" * 80)
    log("3단계: 1:N 관계 처리 시작")
    log("=" * 80)
    
    # 서울 병원의 암호화요양기호 목록
    seoul_codes = set(df_base['암호화요양기호'].unique())
    
    # 진료과목정보 - 집계
    df_subject = seoul_data['subject']
    df_subject_seoul = df_subject[df_subject['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_subject_seoul) > 0:
        df_subject_agg = df_subject_seoul.groupby('암호화요양기호').agg({
            '진료과목코드': 'count',
            '과목별 전문의수': 'sum',
            '선택진료 의사수': 'sum'
        }).rename(columns={
            '진료과목코드': '진료과목_개수',
            '과목별 전문의수': '과목별전문의_총수',
            '선택진료 의사수': '선택진료의사_총수'
        }).reset_index()
        
        df_base = df_base.merge(df_subject_agg, on='암호화요양기호', how='left')
        log(f"진료과목정보 집계 완료: {len(df_subject_seoul):,}행 -> {len(df_subject_agg):,}개 병원")
    
    # 의료장비정보 - 주요 장비만 피벗
    df_equipment = seoul_data['equipment']
    df_equipment_seoul = df_equipment[df_equipment['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_equipment_seoul) > 0:
        # 주요 장비 목록
        major_equipment = ['CT', 'MRI(자기공명영상촬영장치)', '초음파영상진단기', 'X선촬영장치']
        df_eq_major = df_equipment_seoul[df_equipment_seoul['장비코드명'].isin(major_equipment)]
        
        if len(df_eq_major) > 0:
            df_eq_pivot = df_eq_major.pivot_table(
                index='암호화요양기호',
                columns='장비코드명',
                values='장비대수',
                aggfunc='sum',
                fill_value=0
            ).reset_index()
            
            # 컬럼명 정리
            df_eq_pivot.columns = ['암호화요양기호'] + \
                [f'장비_{col}_대수' for col in df_eq_pivot.columns[1:]]
            
            df_base = df_base.merge(df_eq_pivot, on='암호화요양기호', how='left')
            log(f"의료장비정보 피벗 완료: {len(df_equipment_seoul):,}행 -> 주요 장비 {len(df_eq_pivot.columns)-1}개")
    
    # 교통정보 - 개수 집계
    df_traffic = seoul_data['traffic']
    df_traffic_seoul = df_traffic[df_traffic['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_traffic_seoul) > 0:
        df_traffic_count = df_traffic_seoul.groupby('암호화요양기호').size().reset_index(name='교통편_개수')
        df_base = df_base.merge(df_traffic_count, on='암호화요양기호', how='left')
        log(f"교통정보 집계 완료: {len(df_traffic_seoul):,}행 -> {len(df_traffic_count):,}개 병원")
    
    # 특수진료정보 - 개수 집계
    df_special = seoul_data['special']
    df_special_seoul = df_special[df_special['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_special_seoul) > 0:
        df_special_count = df_special_seoul.groupby('암호화요양기호').size().reset_index(name='특수진료_개수')
        df_base = df_base.merge(df_special_count, on='암호화요양기호', how='left')
        log(f"특수진료정보 집계 완료: {len(df_special_seoul):,}행 -> {len(df_special_count):,}개 병원")
    
    # 기타인력정보 - 총수 집계
    df_staff = seoul_data['staff']
    df_staff_seoul = df_staff[df_staff['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_staff_seoul) > 0:
        df_staff_sum = df_staff_seoul.groupby('암호화요양기호')['기타인력수'].sum().reset_index(name='기타인력_총수')
        df_base = df_base.merge(df_staff_sum, on='암호화요양기호', how='left')
        log(f"기타인력정보 집계 완료: {len(df_staff_seoul):,}행 -> {len(df_staff_sum):,}개 병원")
    
    # 식대가산정보 - 건수 집계
    df_meal = seoul_data['meal']
    df_meal_seoul = df_meal[df_meal['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_meal_seoul) > 0:
        df_meal_count = df_meal_seoul.groupby('암호화요양기호').size().reset_index(name='식대가산_건수')
        df_base = df_base.merge(df_meal_count, on='암호화요양기호', how='left')
        log(f"식대가산정보 집계 완료: {len(df_meal_seoul):,}행 -> {len(df_meal_count):,}개 병원")
    
    # 간호등급정보 - 피벗
    df_nursing = seoul_data['nursing']
    df_nursing_seoul = df_nursing[df_nursing['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_nursing_seoul) > 0:
        df_nursing_pivot = df_nursing_seoul.pivot_table(
            index='암호화요양기호',
            columns='유형코드명',
            values='간호등급',
            aggfunc='first'
        ).reset_index()
        
        # 컬럼명 정리
        df_nursing_pivot.columns = ['암호화요양기호'] + \
            [f'간호등급_{col}' for col in df_nursing_pivot.columns[1:]]
        
        df_base = df_base.merge(df_nursing_pivot, on='암호화요양기호', how='left')
        log(f"간호등급정보 피벗 완료: {len(df_nursing_seoul):,}행 -> {len(df_nursing_pivot.columns)-1}개 유형")
    
    # 전문병원지정분야 - 리스트
    df_specialized = seoul_data['specialized']
    df_specialized_seoul = df_specialized[df_specialized['암호화요양기호'].isin(seoul_codes)]
    
    if len(df_specialized_seoul) > 0:
        df_spec_list = df_specialized_seoul.groupby('암호화요양기호')['검색코드명'].apply(
            lambda x: ', '.join(x.astype(str))
        ).reset_index(name='전문병원지정분야')
        df_base = df_base.merge(df_spec_list, on='암호화요양기호', how='left')
        log(f"전문병원지정분야 처리 완료: {len(df_specialized_seoul):,}행 -> {len(df_spec_list):,}개 병원")
    
    log(f"1:N 처리 완료: 총 {len(df_base):,}행 × {len(df_base.columns)}열")
    log("")
    return df_base

# ============================================================================
# 4단계: 데이터 후처리
# ============================================================================

def postprocess_data(df):
    """데이터 후처리 (중복 컬럼 제거, 결측치 처리)"""
    log("=" * 80)
    log("4단계: 데이터 후처리 시작")
    log("=" * 80)
    
    # 중복 컬럼 제거
    cols_to_drop = [col for col in df.columns if col.endswith('_시설') or col.endswith('_세부')]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        log(f"중복 컬럼 제거: {len(cols_to_drop)}개")
    
    # 결측치 처리
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    log(f"수치형 결측치 0으로 채우기: {len(numeric_cols)}개 컬럼")
    
    log(f"후처리 완료: {len(df):,}행 × {len(df.columns)}열")
    log("")
    return df

# ============================================================================
# 5단계: 검증
# ============================================================================

def validate_data(df, original_hospital_count):
    """데이터 검증"""
    log("=" * 80)
    log("5단계: 데이터 검증 시작")
    log("=" * 80)
    
    errors = []
    
    # 1. 행 수 검증
    if len(df) != original_hospital_count:
        errors.append(f"행 수 불일치: 예상 {original_hospital_count}, 실제 {len(df)}")
    else:
        log(f"[OK] 행 수 검증: {len(df):,}행")
    
    # 2. 중복 행 확인
    duplicates = df['암호화요양기호'].duplicated().sum()
    if duplicates > 0:
        errors.append(f"중복 행 발견: {duplicates}개")
    else:
        log(f"[OK] 중복 행 없음")
    
    # 3. 필수 컬럼 존재 확인
    required_cols = ['암호화요양기호', '요양기관명', '시도코드명', '좌표(X)', '좌표(Y)']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"필수 컬럼 누락: {missing_cols}")
    else:
        log(f"[OK] 필수 컬럼 존재")
    
    # 4. 좌표 범위 검증
    if '좌표(X)' in df.columns and '좌표(Y)' in df.columns:
        invalid_x = (~df['좌표(X)'].between(124, 132)).sum()
        invalid_y = (~df['좌표(Y)'].between(33, 43)).sum()
        if invalid_x > 0 or invalid_y > 0:
            errors.append(f"좌표 범위 이상: X={invalid_x}개, Y={invalid_y}개")
        else:
            log(f"[OK] 좌표 범위 정상")
    
    # 5. 결측치 비율 확인
    missing_rate = df.isnull().sum() / len(df) * 100
    high_missing = missing_rate[missing_rate > 50]
    if len(high_missing) > 0:
        log(f"[WARN] 결측치 50% 이상 컬럼: {len(high_missing)}개", 'WARN')
        for col, rate in high_missing.items():
            log(f"  - {col}: {rate:.1f}%", 'WARN')
    else:
        log(f"[OK] 결측치 비율 양호")
    
    log("")
    if errors:
        log("검증 실패:", 'ERROR')
        for error in errors:
            log(f"  - {error}", 'ERROR')
        return False, errors
    else:
        log("검증 성공!")
        return True, []

# ============================================================================
# 6단계: 저장
# ============================================================================

def save_data(df, seoul_pharmacy):
    """데이터 저장"""
    log("=" * 80)
    log("6단계: 데이터 저장 시작")
    log("=" * 80)
    
    # 병원 통합 데이터 저장
    hospital_path = os.path.join(OUTPUT_DIR, '서울_병원_통합_2025.12.csv')
    df.to_csv(hospital_path, index=False, encoding='utf-8-sig')
    log(f"병원 데이터 저장: {hospital_path}")
    log(f"  - {len(df):,}행 × {len(df.columns)}열")
    
    # 약국 데이터 저장
    pharmacy_path = os.path.join(OUTPUT_DIR, '서울_약국_정보_2025.12.csv')
    seoul_pharmacy.to_csv(pharmacy_path, index=False, encoding='utf-8-sig')
    log(f"약국 데이터 저장: {pharmacy_path}")
    log(f"  - {len(seoul_pharmacy):,}행 × {len(seoul_pharmacy.columns)}열")
    
    log("")
    return hospital_path, pharmacy_path

# ============================================================================
# 7단계: 리포트 작성
# ============================================================================

def create_report(df, seoul_pharmacy, validation_result, total_time):
    """취합 결과 리포트 작성"""
    log("=" * 80)
    log("7단계: 리포트 작성 시작")
    log("=" * 80)
    
    report_path = os.path.join(REPORT_DIR, '취합_결과_리포트_260131_0844.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 서울 병의원 및 약국 데이터 취합 결과 리포트\n\n")
        f.write(f"**작업 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**총 소요 시간**: {total_time:.1f}초\n\n")
        
        f.write("---\n\n")
        f.write("## 취합 통계\n\n")
        f.write(f"- **병원 데이터**: {len(df):,}행 × {len(df.columns)}열\n")
        f.write(f"- **약국 데이터**: {len(seoul_pharmacy):,}행 × {len(seoul_pharmacy.columns)}열\n")
        f.write(f"- **검증 결과**: {'성공' if validation_result[0] else '실패'}\n\n")
        
        f.write("---\n\n")
        f.write("## 주요 지표\n\n")
        f.write(f"- 총 병원 수: {len(df):,}개\n")
        f.write(f"- 총 약국 수: {len(seoul_pharmacy):,}개\n")
        
        if '진료과목_개수' in df.columns:
            f.write(f"- 평균 진료과목 수: {df['진료과목_개수'].mean():.1f}개\n")
        
        if '총의사수' in df.columns:
            f.write(f"- 총 의사 수: {df['총의사수'].sum():,.0f}명\n")
        
        f.write("\n---\n\n")
        f.write("## 처리 로그\n\n")
        f.write("```\n")
        for log_msg in logs:
            f.write(log_msg + "\n")
        f.write("```\n")
    
    log(f"리포트 저장: {report_path}")
    log("")
    return report_path

# ============================================================================
# 메인 실행
# ============================================================================

def main():
    """메인 실행 함수"""
    start_time = time.time()
    
    try:
        # 1. 데이터 로드 및 서울 필터링
        data, seoul_data = load_and_filter_seoul()
        original_hospital_count = len(seoul_data['hospital'])
        
        # 2. 1:1 관계 병합
        df_merged = merge_one_to_one(seoul_data)
        
        # 3. 1:N 관계 처리
        df_merged = process_one_to_many(df_merged, seoul_data)
        
        # 4. 데이터 후처리
        df_merged = postprocess_data(df_merged)
        
        # 5. 검증
        validation_result = validate_data(df_merged, original_hospital_count)
        
        # 6. 저장
        hospital_path, pharmacy_path = save_data(df_merged, seoul_data['pharmacy'])
        
        # 7. 리포트 작성
        total_time = time.time() - start_time
        report_path = create_report(df_merged, seoul_data['pharmacy'], validation_result, total_time)
        
        log("=" * 80)
        log("작업 완료!")
        log("=" * 80)
        log(f"총 소요 시간: {total_time:.1f}초")
        log(f"병원 데이터: {hospital_path}")
        log(f"약국 데이터: {pharmacy_path}")
        log(f"리포트: {report_path}")
        
        return df_merged, seoul_data['pharmacy']
        
    except Exception as e:
        log(f"에러 발생: {str(e)}", 'ERROR')
        import traceback
        log(traceback.format_exc(), 'ERROR')
        raise

if __name__ == '__main__':
    df_hospital, df_pharmacy = main()
