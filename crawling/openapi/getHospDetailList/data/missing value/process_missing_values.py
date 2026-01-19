"""
병원 데이터 결측치 처리 스크립트
처리 기준: missing_value_analysis_20260118_232100.md
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

def process_missing_values(input_file, output_file):
    """
    결측치 처리 함수
    
    Parameters:
    -----------
    input_file : str
        입력 파일 경로
    output_file : str
        출력 파일 경로
    
    Returns:
    --------
    dict : 처리 결과 통계
    """
    
    print("=" * 80)
    print("병원 데이터 결측치 처리 시작")
    print("=" * 80)
    
    # 1. 데이터 로드
    print("\n[1/6] 데이터 로드 중...")
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    print(f"  - 원본 데이터: {len(df):,}건, {len(df.columns)}개 컬럼")
    
    # 처리 전 통계
    before_stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'total_missing': int(df.isnull().sum().sum())
    }
    
    df_processed = df.copy()
    
    # 2. 필수 정보 결측 시 제외
    print("\n[2/6] 필수 정보 결측 데이터 제외 중...")
    essential_cols = ['원본_기관코드', '원본_병원명', '원본_주소']
    rows_before = len(df_processed)
    df_processed = df_processed.dropna(subset=essential_cols)
    rows_removed = rows_before - len(df_processed)
    print(f"  - 제외된 데이터: {rows_removed}건")
    
    # 3. 수치형 컬럼 0으로 대체
    print("\n[3/6] 수치형 컬럼 결측치 처리 중...")
    numeric_fill_zero = [
        # 시설 정보
        'eqp_stdSickbdCnt', 'eqp_emymCnt', 'eqp_aduChldSprmCnt',
        'eqp_anvirTrrmSbdCnt', 'eqp_chldSprmCnt', 'eqp_hghrSickbdCnt',
        'eqp_isnrSbdCnt', 'eqp_nbySprmCnt', 'eqp_partumCnt',
        'eqp_permSbdCnt', 'eqp_psydeptClsGnlSbdCnt', 'eqp_psydeptClsHigSbdCnt',
        'eqp_psydeptOpenGnlSbdCnt', 'eqp_psydeptOpenHigSbdCnt', 'eqp_ptrmCnt',
        'eqp_soprmCnt',
        # 진료과목 정보
        'dgsbjt_cdiagDrCnt', 'dgsbjt_dgsbjtPrSdrCnt',
        # 의료장비 정보
        'medoft_oftCnt',
        # 식대가산 정보
        'foepaddc_calcNopCnt',
        # 기타인력 정보
        'etchst_gnlNopCnt', 'etchst_gnlNopDtlCd',
        # 세부정보 - 주차
        'dtl_parkQty'
    ]
    
    zero_filled_count = 0
    for col in numeric_fill_zero:
        if col in df_processed.columns:
            missing_count = df_processed[col].isnull().sum()
            if missing_count > 0:
                df_processed[col] = df_processed[col].fillna(0)
                zero_filled_count += missing_count
                print(f"  - {col}: {missing_count}건 → 0으로 대체")
    
    print(f"  - 총 {zero_filled_count:,}개 결측치를 0으로 대체")
    
    # 4. Y/N 컬럼 'N'으로 대체
    print("\n[4/6] Y/N 컬럼 결측치 처리 중...")
    yn_cols = ['foepaddc_gnmAddcYn', 'dtl_emyDayYn', 'dtl_emyNgtYn', 'dtl_parkXpnsYn']
    yn_filled_count = 0
    for col in yn_cols:
        if col in df_processed.columns:
            missing_count = df_processed[col].isnull().sum()
            if missing_count > 0:
                df_processed[col] = df_processed[col].fillna('N')
                yn_filled_count += missing_count
                print(f"  - {col}: {missing_count}건 → 'N'으로 대체")
    
    print(f"  - 총 {yn_filled_count:,}개 결측치를 'N'으로 대체")
    
    # 5. 전화번호 '정보없음'으로 대체
    print("\n[5/6] 전화번호 결측치 처리 중...")
    if 'eqp_telno' in df_processed.columns:
        missing_count = df_processed['eqp_telno'].isnull().sum()
        if missing_count > 0:
            df_processed['eqp_telno'] = df_processed['eqp_telno'].fillna('정보없음')
            print(f"  - eqp_telno: {missing_count}건 → '정보없음'으로 대체")
    
    # 6. 나머지는 결측 유지 (NULL)
    print("\n[6/6] 나머지 컬럼은 결측 유지 (NULL)...")
    remaining_missing = df_processed.isnull().sum().sum()
    print(f"  - 남은 결측치: {remaining_missing:,}개 (정보 미제공 또는 해당 없음)")
    
    # 처리 후 통계
    after_stats = {
        'total_rows': len(df_processed),
        'total_columns': len(df_processed.columns),
        'total_missing': int(df_processed.isnull().sum().sum())
    }
    
    # 7. 결과 저장
    print("\n" + "=" * 80)
    print("처리 결과 저장 중...")
    print("=" * 80)
    
    df_processed.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"[OK] 처리된 데이터 저장 완료: {output_file}")
    
    # 8. 처리 로그 생성
    processing_log = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input_file': input_file,
        'output_file': output_file,
        'before': before_stats,
        'after': after_stats,
        'changes': {
            'rows_removed': int(before_stats['total_rows'] - after_stats['total_rows']),
            'missing_reduced': int(before_stats['total_missing'] - after_stats['total_missing']),
            'zero_filled': int(zero_filled_count),
            'yn_filled': int(yn_filled_count)
        },
        'processing_rules': {
            'essential_columns_check': essential_cols,
            'numeric_zero_fill': len(numeric_fill_zero),
            'yn_columns_fill': len(yn_cols),
            'phone_fill': 1
        }
    }
    
    log_file = output_file.replace('.csv', '_processing_log.json')
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(processing_log, f, ensure_ascii=False, indent=2)
    print(f"[OK] 처리 로그 저장 완료: {log_file}")
    
    # 9. 처리 전후 비교 출력
    print("\n" + "=" * 80)
    print("처리 전후 비교")
    print("=" * 80)
    print(f"\n[데이터 건수]")
    print(f"  - 처리 전: {before_stats['total_rows']:,}건")
    print(f"  - 처리 후: {after_stats['total_rows']:,}건")
    print(f"  - 제외됨: {processing_log['changes']['rows_removed']:,}건")
    
    print(f"\n[결측치 수]")
    print(f"  - 처리 전: {before_stats['total_missing']:,}개")
    print(f"  - 처리 후: {after_stats['total_missing']:,}개")
    print(f"  - 감소량: {processing_log['changes']['missing_reduced']:,}개")
    print(f"  - 감소율: {(processing_log['changes']['missing_reduced'] / before_stats['total_missing'] * 100):.2f}%")
    
    print(f"\n[처리 내역]")
    print(f"  - 0으로 대체: {zero_filled_count:,}개")
    print(f"  - 'N'으로 대체: {yn_filled_count:,}개")
    print(f"  - '정보없음'으로 대체: {missing_count if 'eqp_telno' in df_processed.columns else 0:,}개")
    print(f"  - 결측 유지: {after_stats['total_missing']:,}개")
    
    print("\n" + "=" * 80)
    print("[완료] 결측치 처리 완료!")
    print("=" * 80)
    
    return processing_log


if __name__ == '__main__':
    # 파일 경로 설정
    input_file = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260116_212603.csv'
    
    # 출력 파일명에 처리 일시 포함
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = rf'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_결측치처리완료_{timestamp}.csv'
    
    # 처리 실행
    try:
        log = process_missing_values(input_file, output_file)
        print(f"\n[생성된 파일]")
        print(f"  1. {output_file}")
        print(f"  2. {output_file.replace('.csv', '_processing_log.json')}")
        
    except Exception as e:
        print(f"\n[오류] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
