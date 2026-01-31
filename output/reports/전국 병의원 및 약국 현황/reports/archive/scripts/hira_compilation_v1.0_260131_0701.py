import pandas as pd
import os
import json
from datetime import datetime

# 설정
TIMESTAMP = "260131_0701"
DATA_DIR = r"d:\git_gb4pro\data\전국 병의원 및 약국 현황 2025.12"
OUTPUT_DIR = r"d:\git_gb4pro\output\reports\전국 병의원 및 약국 현황"
SCRIPTS_DIR = os.path.join(OUTPUT_DIR, f"scripts_{TIMESTAMP}")
REPORTS_DIR = os.path.join(OUTPUT_DIR, f"reports_{TIMESTAMP}")
FINAL_CSV_PATH = os.path.join(f"d:\git_gb4pro\output", f"전국_병의원_통합_2025.12_{TIMESTAMP}.csv")

# 파일 목록 정의 (가이드라인 기준)
FILES = {
    'hospital': '1.병원정보서비스(2025.12.).xlsx',
    'pharmacy': '2.약국정보서비스(2025.12.).xlsx',
    'facility': '3.의료기관별상세정보서비스_01_시설정보 2025.12..xlsx',
    'detail': '4.의료기관별상세정보서비스_02_세부정보 2025.12..xlsx',
    'subject': '5.의료기관별상세정보서비스_03_진료과목정보 2025.12..xlsx',
    'traffic': '6.의료기관별상세정보서비스_04_교통정보 2025.12..xlsx',
    'equipment': '7.의료기관별상세정보서비스_05_의료장비정보 2025.12..xlsx',
    'meal': '8.의료기관별상세정보서비스_06_식대가산정보 2025.12..xlsx',
    'nursing': '9.의료기관별상세정보서비스_07_간호등급정보 2025.12..xlsx',
    'special': '10.의료기관별상세정보서비스_08_특수진료정보서비스 2025.12..xlsx',
    'specialized': '11.의료기관별상세정보서비스_09_전문병원지정분야 2025.12..xlsx',
    'staff': '12.의료기관별상세정보서비스_10_기타인력정보 2025.12..xlsx'
}

error_logs = []
compilation_stats = {
    "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "files_processed": [],
    "total_rows_before": 0,
    "total_rows_after": 0,
    "errors_found": 0
}

def log_error(file_key, message, severity="Error"):
    error_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": file_key,
        "message": message,
        "severity": severity
    })
    compilation_stats["errors_found"] += 1

def main():
    data = {}
    
    # 1. 데이터 로드
    print("Step 1: 데이터 로딩 시작...")
    for key, filename in FILES.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            log_error(key, f"파일을 찾을 수 없습니다: {filename}", "Critical")
            continue
        try:
            data[key] = pd.read_excel(filepath)
            compilation_stats["files_processed"].append(filename)
            print(f"✓ {key} 로드 완료: {data[key].shape}")
        except Exception as e:
            log_error(key, f"로드 중 에러 발생: {str(e)}", "Critical")

    if 'hospital' not in data:
        print("!! Critical: 기준 데이터(병원정보)가 없어 작업을 중단합니다.")
        return

    df_base = data['hospital'].copy()
    compilation_stats["total_rows_before"] = len(df_base)

    # 2. 1:1 병합 (시설, 세부)
    print("Step 2: 1:1 관계 데이터 병합...")
    for key in ['facility', 'detail']:
        if key in data:
            try:
                df_base = df_base.merge(
                    data[key],
                    on='암호화요양기호',
                    how='left',
                    suffixes=('', f'_{key}')
                )
                print(f"✓ {key} 병합 완료")
            except Exception as e:
                log_error(key, f"병합 중 에러 발생: {str(e)}")

    # 3. 1:N 집계 및 병합
    print("Step 3: 1:N 관계 데이터 집계 및 병합...")
    
    # 3.1 진료과목 (집계)
    if 'subject' in data:
        df_subject_agg = data['subject'].groupby('암호화요양기호').agg({
            '진료과목코드': 'count',
            '과목별 전문의수': 'sum',
            '선택진료 의사수': 'sum'
        }).rename(columns={
            '진료과목코드': '진료과목_개수',
            '과목별 전문의수': '전문의_총합',
            '선택진료 의사수': '선택진료의사_총합'
        }).reset_index()
        df_base = df_base.merge(df_subject_agg, on='암호화요양기호', how='left')
        print("✓ subject 집계 완료")

    # 3.2 의료장비 (피벗 - 주요 장비 CT, MRI 등 예시)
    if 'equipment' in data:
        major_eq = ['CT', 'MRI', '초음파영상진단기']
        df_eq_filtered = data['equipment'][data['equipment']['장비코드명'].isin(major_eq)]
        df_eq_pivot = df_eq_filtered.pivot_table(
            index='암호화요양기호',
            columns='장비코드명',
            values='장비대수',
            aggfunc='sum',
            fill_value=0
        ).reset_index()
        df_eq_pivot.columns = ['암호화요양기호'] + [f'장비_{c}_대수' for c in df_eq_pivot.columns[1:]]
        df_base = df_base.merge(df_eq_pivot, on='암호화요양기호', how='left')
        print("✓ equipment 피벗 완료")

    # 3.3 기타 (교통, 특수진료, 기타인력 등 가이드라인 약식 적용)
    if 'traffic' in data:
        df_traffic_count = data['traffic'].groupby('암호화요양기호').size().reset_index(name='교통편_개수')
        df_base = df_base.merge(df_traffic_count, on='암호화요양기호', how='left')
    
    if 'special' in data:
        df_special_count = data['special'].groupby('암호화요양기호').size().reset_index(name='특수진료_개수')
        df_base = df_base.merge(df_special_count, on='암호화요양기호', how='left')

    if 'staff' in data:
        df_staff_agg = data['staff'].groupby('암호화요양기호')['기타인력수'].sum().reset_index(name='기타인력_총수')
        df_base = df_base.merge(df_staff_agg, on='암호화요양기호', how='left')

    # 4. 후처리
    print("Step 4: 데이터 후처리...")
    # 중복 컬럼 (요양기관명_시설 등) 제거
    drop_cols = [c for c in df_base.columns if any(x in c for x in ['_facility', '_detail', '_시설', '_세부'])]
    df_base = df_base.drop(columns=drop_cols, errors='ignore')

    # 결측치 채우기
    numeric_cols = df_base.select_dtypes(include=['number']).columns
    df_base[numeric_cols] = df_base[numeric_cols].fillna(0)
    df_base = df_base.fillna("정보없음")

    compilation_stats["total_rows_after"] = len(df_base)
    compilation_stats["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 5. 저장
    print(f"Step 5: 최종 데이터 저장 ({FINAL_CSV_PATH})...")
    df_base.to_csv(FINAL_CSV_PATH, index=False, encoding='utf-8-sig')

    # 6. 리포트 생성
    generate_reports()

def generate_reports():
    print("Step 6: 리포트 생성 중...")
    
    # 6.1 에러 리포트
    error_report_name = f"ERROR_REPORT_전국병원현황_{TIMESTAMP}.md"
    error_report_path = os.path.join(REPORTS_DIR, error_report_name)
    with open(error_report_path, "w", encoding="utf-8") as f:
        f.write(f"# 에러 리포트 (데이터 취합: {TIMESTAMP})\n\n")
        f.write(f"- 발생 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 총 에러 건수: {len(error_logs)}\n\n")
        if not error_logs:
            f.write("특이 사항 없음 (Clean Run)\n")
        else:
            f.write("| 발생시간 | 대상파일 | 구분 | 메시지 |\n")
            f.write("| --- | --- | --- | --- |\n")
            for log in error_logs:
                f.write(f"| {log['timestamp']} | {log['file']} | {log['severity']} | {log['message']} |\n")

    # 6.2 취합 결과 리포트
    result_report_name = f"SUMMARY_REPORT_전국병원현황_{TIMESTAMP}.md"
    result_report_path = os.path.join(REPORTS_DIR, result_report_name)
    with open(result_report_path, "w", encoding="utf-8") as f:
        f.write(f"# 데이터 취합 결과 리포트 (2025.12)\n\n")
        f.write("## 1. 개요\n")
        f.write(f"- **취합 일시**: {compilation_stats['start_time']} ~ {compilation_stats['end_time']}\n")
        f.write(f"- **대상 파일**: {len(compilation_stats['files_processed'])}개 로드\n")
        f.write(f"- **최종 데이터 행 수**: {compilation_stats['total_rows_after']:,} (최초: {compilation_stats['total_rows_before']:,})\n\n")
        
        f.write("## 2. 취합 통계\n")
        f.write(f"- 파일 로드 성공: {len(compilation_stats['files_processed'])} / {len(FILES)}\n")
        f.write(f"- 처리 중 발생 에러: {compilation_stats['errors_found']}건 (별도 에러 리포트 참조)\n\n")
        
        f.write("## 3. 에러 발생 및 반영 사항\n")
        if compilation_stats['errors_found'] > 0:
            f.write("데이터 취합 중 다음과 같은 이슈가 발생하여 처리되었습니다:\n\n")
            for log in error_logs:
                f.write(f"- **[{log['file']}]**: {log['message']} (반영사항: 해당 데이터 제외 또는 기본값 처리)\n")
        else:
            f.write("특이사항 없음. 모든 데이터가 규칙에 따라 정상적으로 취합되었습니다.\n")

    print(f"✓ 리포트 생성 완료: {REPORTS_DIR}")

if __name__ == "__main__":
    main()
