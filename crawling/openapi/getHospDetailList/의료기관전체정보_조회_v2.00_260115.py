"""
의료기관 전체정보 조회 API 호출 스크립트 v2.00
================================================================================
작성일: 2026-01-15
목적: 건강보험심사평가원 의료기관별상세정보서비스 API를 사용하여 
      11개 모든 정보 카테고리 조회
입력: 병원기본목록 CSV 파일 (암호화된 요양기호 포함)
출력: 병원 전체정보 CSV 파일 (11개 API 응답 통합)
================================================================================
"""

import requests
import json
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import time
import os
from pathlib import Path
from urllib.parse import quote

# ============================================================================
# 설정 (Configuration)
# ============================================================================

# API 기본 정보
API_BASE_URL = "http://apis.data.go.kr/B551182/MadmDtlInfoService2.7"

# 11개 API 엔드포인트 설정
API_ENDPOINTS = {
    'eqp': {
        'operation': 'getEqpInfo2.7',
        'name': '시설정보',
        'description': '의료기관의 시설 현황(병상 수 등)'
    },
    'dtl': {
        'operation': 'getDtlInfo2.7',
        'name': '세부정보',
        'description': '의료기관의 기본 및 상세 현황'
    },
    'dgsbjt': {
        'operation': 'getDgsbjtInfo2.7',
        'name': '진료과목정보',
        'description': '개설된 진료과목 정보'
    },
    'trnsprt': {
        'operation': 'getTrnsprtInfo2.7',
        'name': '교통정보',
        'description': '주변 교통수단 정보'
    },
    'medoft': {
        'operation': 'getMedOftInfo2.7',
        'name': '의료장비정보',
        'description': '보유 의료 장비 현황'
    },
    'foepaddc': {
        'operation': 'getFoepAddcInfo2.7',
        'name': '식대가산정보',
        'description': '입원 환자 식사 제공 가산 정보'
    },
    'nursiggrd': {
        'operation': 'getNursigGrdInfo2.7',
        'name': '간호등급정보',
        'description': '간호 등급 정보'
    },
    'spcldiag': {
        'operation': 'getSpclDiagInfo2.7',
        'name': '특수진료정보',
        'description': '전문 진료 가능 분야'
    },
    'spclhosp': {
        'operation': 'getSpclHospAsgFldList2.7',
        'name': '전문병원지정분야',
        'description': '보건복지부 지정 전문병원 분야'
    },
    'spcsbtj': {
        'operation': 'getSpcSbtjTsdrInfo2.7',
        'name': '전문과목별전문의수',
        'description': '진료 과목별 전문의 인원 수'
    },
    'etchst': {
        'operation': 'getEtcHstInfo2.7',
        'name': '기타인력수정보',
        'description': '약사, 물리치료사 등 의료 인력 현황'
    }
}

# 인증키 설정
SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="# 건강보험심사평가원 의료기관별상세정보서비스 인증키(디코더)
USE_ENCODED_KEY = False

# 재시도 설정
MAX_RETRIES = 3
RETRY_DELAY = 1

# 타임아웃 설정
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 60

# 체크포인트 설정
ENABLE_CHECKPOINT = True
CHECKPOINT_INTERVAL = 5

# 중간 저장 설정 (진행 중인 데이터를 주기적으로 CSV로 저장)
ENABLE_INTERIM_SAVE = True  # 중간 저장 활성화
INTERIM_SAVE_INTERVAL = 10  # 중간 저장 간격 (건수)

# 입력 파일 설정
INPUT_CSV_FILE = r"D:\git_gb4pro\crawling\openapi\getHospDetailList\data\서울_강남구_피부과_20260115_212757.csv" # 서울_강남구_피부과_20260115_212757.csv input 파일 위치
YKIHO_COLUMN = None  # 자동 탐지

# 테스트 모드 설정
TEST_MODE = False  # True로 설정하면 소량 데이터만 처리
MAX_TEST_RECORDS = 3  # 테스트 모드에서 처리할 최대 레코드 수

# ============================================================================
# API 호출 함수
# ============================================================================

def call_single_api(
    service_key: str,
    operation: str,
    ykiho: str,
    use_encoded_key: bool = False,
    max_retries: int = MAX_RETRIES,
    retry_delay: int = RETRY_DELAY
) -> Optional[Dict]:
    """
    단일 API 엔드포인트 호출 (재시도 로직 포함)
    
    Parameters:
    -----------
    service_key : str
        공공데이터포털 인증키
    operation : str
        API operation 이름 (예: getDtlInfo2.7)
    ykiho : str
        암호화된 요양기호
    use_encoded_key : bool
        인증키 인코딩 여부
    max_retries : int
        최대 재시도 횟수
    retry_delay : int
        초기 재시도 대기 시간
    
    Returns:
    --------
    dict or None
        API 응답 데이터 또는 None (실패 시)
    """
    
    # API URL 구성
    api_url = f"{API_BASE_URL}/{operation}"
    
    # 요청 파라미터
    params = {
        'ykiho': ykiho,
        '_type': 'json'
    }
    
    # API 키 처리
    if use_encoded_key:
        encoded_key = quote(service_key, safe='')
        api_url = f"{api_url}?ServiceKey={encoded_key}"
    else:
        params['ServiceKey'] = service_key
    
    # 재시도 로직
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                wait_time = retry_delay * (2 ** (attempt - 1))
                time.sleep(wait_time)
            
            response = requests.get(
                api_url,
                params=params,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
            response.raise_for_status()
            
            data = response.json()
            header = data['response']['header']
            
            if header['resultCode'] != '00':
                # 데이터 없음은 정상 처리 (None 반환)
                if header['resultCode'] == '3':
                    return None
                raise Exception(f"API 오류 [{header['resultCode']}]: {header['resultMsg']}")
            
            return data
            
        except requests.exceptions.Timeout:
            last_exception = Exception(f"API 호출 시간 초과")
            if attempt < max_retries:
                continue
        except requests.exceptions.ConnectionError:
            last_exception = Exception("네트워크 연결 오류")
            if attempt < max_retries:
                continue
        except requests.exceptions.HTTPError as e:
            last_exception = Exception(f"HTTP 오류: {e}")
            break
        except KeyError as e:
            last_exception = Exception(f"응답 데이터 형식 오류: {e}")
            break
        except Exception as e:
            last_exception = Exception(f"예상치 못한 오류: {e}")
            if attempt < max_retries:
                continue
    
    # 모든 재시도 실패
    return None


def flatten_dict_with_prefix(data: Dict, prefix: str, parent_key: str = '') -> Dict:
    """
    중첩된 딕셔너리를 평탄화하고 접두사 추가
    
    Parameters:
    -----------
    data : dict
        평탄화할 딕셔너리
    prefix : str
        추가할 접두사
    parent_key : str
        부모 키 (재귀 호출용)
    
    Returns:
    --------
    dict
        평탄화된 딕셔너리
    """
    items = []
    for k, v in data.items():
        new_key = f"{prefix}_{parent_key}_{k}" if parent_key else f"{prefix}_{k}"
        
        if isinstance(v, dict):
            items.extend(flatten_dict_with_prefix(v, prefix, k).items())
        elif isinstance(v, list):
            # 리스트는 JSON 문자열로 변환
            items.append((new_key, json.dumps(v, ensure_ascii=False)))
        else:
            items.append((new_key, v))
    
    return dict(items)


def get_hospital_all_info(
    service_key: str,
    use_encoded_key: bool,
    ykiho: str,
    hospital_name: str = '',
    hospital_addr: str = ''
) -> Dict:
    """
    단일 병원의 모든 정보 조회 (11개 API 호출)
    
    Parameters:
    -----------
    service_key : str
        공공데이터포털 인증키
    use_encoded_key : bool
        인증키 인코딩 여부
    ykiho : str
        암호화된 요양기호
    hospital_name : str
        병원명 (원본 데이터)
    hospital_addr : str
        병원 주소 (원본 데이터)
    
    Returns:
    --------
    dict
        통합된 병원 정보
    """
    
    # 결과 딕셔너리 초기화
    result = {
        '원본_기관코드': ykiho,
        '원본_병원명': hospital_name,
        '원본_주소': hospital_addr
    }
    
    # API 호출 성공 카운터
    success_count = 0
    
    # 11개 API 순차 호출
    for prefix, endpoint_info in API_ENDPOINTS.items():
        operation = endpoint_info['operation']
        name = endpoint_info['name']
        
        try:
            # API 호출
            data = call_single_api(
                service_key=service_key,
                operation=operation,
                ykiho=ykiho,
                use_encoded_key=use_encoded_key
            )
            
            if data is None:
                print(f"    [{prefix}] {name}: 데이터 없음")
                continue
            
            # 응답 바디 추출
            body = data['response']['body']
            items = body.get('items', {})
            
            if not items or isinstance(items, str):
                print(f"    [{prefix}] {name}: 데이터 없음")
                continue
            
            item_data = items.get('item', {})
            
            if not item_data or isinstance(item_data, str):
                print(f"    [{prefix}] {name}: 데이터 없음")
                continue
            
            # 리스트 형태인 경우 첫 번째 항목만 사용
            if isinstance(item_data, list):
                if len(item_data) > 0:
                    item_data = item_data[0]
                else:
                    print(f"    [{prefix}] {name}: 빈 리스트")
                    continue
            
            # 딕셔너리 평탄화 및 접두사 추가
            flattened = flatten_dict_with_prefix(item_data, prefix)
            result.update(flattened)
            
            success_count += 1
            print(f"    [{prefix}] {name}: 성공 ({len(flattened)}개 필드)")
            
        except Exception as e:
            print(f"    [{prefix}] {name}: 오류 - {e}")
            continue
        
        # API 호출 간격
        time.sleep(0.1)
    
    print(f"    => 총 {success_count}/{len(API_ENDPOINTS)}개 API 성공")
    
    return result


# ============================================================================
# 데이터 처리 함수
# ============================================================================

def load_hospital_list_from_csv(filename: str, ykiho_column: str = None) -> tuple:
    """CSV 파일에서 병원 목록 읽기"""
    print(f"[CSV 읽기] {filename}")
    
    encodings = ['cp949', 'utf-8-sig', 'utf-8', 'euc-kr']
    df = None
    last_error = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print(f"  - 인코딩: {encoding} (성공)")
            break
        except (UnicodeDecodeError, Exception) as e:
            last_error = e
            continue
    
    if df is None:
        raise Exception(f"CSV 파일을 읽을 수 없습니다. 마지막 오류: {last_error}")
    
    print(f"  - 총 {len(df)}건")
    print(f"  - 컬럼: {', '.join(df.columns.tolist()[:5])}...")
    
    # 요양기호 컬럼 자동 탐지
    if ykiho_column is None:
        possible_columns = ['ykiho', '암호화요양기호', '요양기호', 'YKIHO', 'ykiho_enc']
        for col in possible_columns:
            if col in df.columns:
                ykiho_column = col
                print(f"  - 요양기호 컬럼 자동 탐지: {ykiho_column}")
                break
        
        if ykiho_column is None:
            raise Exception(f"요양기호 컬럼을 찾을 수 없습니다. 가능한 컬럼: {df.columns.tolist()}")
    
    if ykiho_column not in df.columns:
        raise Exception(f"컬럼 '{ykiho_column}'을(를) 찾을 수 없습니다.")
    
    return df, ykiho_column


def save_checkpoint(data: Dict, checkpoint_file: str):
    """체크포인트 저장"""
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[체크포인트 저장] {checkpoint_file}")
    except Exception as e:
        print(f"[경고] 체크포인트 저장 실패: {e}")


def load_checkpoint(checkpoint_file: str) -> Optional[Dict]:
    """체크포인트 로드"""
    if not os.path.exists(checkpoint_file):
        return None
    
    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[체크포인트 로드] {checkpoint_file}")
        print(f"  - 이전 진행: {data.get('processed_count', 0)}건 처리 완료")
        return data
    except Exception as e:
        print(f"[경고] 체크포인트 로드 실패: {e}")
        return None


def generate_metadata_markdown(df: pd.DataFrame, csv_filename: str):
    """메타데이터 마크다운 파일 생성"""
    md_filename = csv_filename.replace('.csv', '.md')
    
    with open(md_filename, 'w', encoding='utf-8') as f:
        # 제목
        f.write(f"# 병원 전체정보 데이터 분석 보고서\n\n")
        f.write(f"**생성일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**데이터 파일**: `{Path(csv_filename).name}`\n\n")
        
        # 기본 정보
        f.write("## 📊 데이터 개요\n\n")
        f.write(f"- **총 레코드 수**: {len(df):,}건\n")
        f.write(f"- **총 컬럼 수**: {len(df.columns)}개\n\n")
        
        # API별 컬럼 수 분석
        f.write("## 📋 API별 수집 정보\n\n")
        api_column_counts = {}
        for prefix in API_ENDPOINTS.keys():
            cols = [col for col in df.columns if col.startswith(f"{prefix}_")]
            api_column_counts[prefix] = len(cols)
        
        f.write("| API | 정보 항목 | 컬럼 수 |\n")
        f.write("|-----|----------|--------|\n")
        for prefix, endpoint_info in API_ENDPOINTS.items():
            count = api_column_counts.get(prefix, 0)
            f.write(f"| `{prefix}` | {endpoint_info['name']} | {count}개 |\n")
        f.write("\n")
        
        # 결측치 분석
        f.write("## 🔍 주요 컬럼 결측치 분석\n\n")
        important_cols = ['원본_기관코드', '원본_병원명', '원본_주소']
        important_cols += [col for col in df.columns if col.startswith('dtl_')][:10]
        
        missing_data = df[important_cols].isnull().sum()
        missing_pct = (missing_data / len(df) * 100).round(2)
        missing_df = pd.DataFrame({
            '컬럼명': missing_data.index,
            '결측치 수': missing_data.values,
            '결측치 비율(%)': missing_pct.values
        })
        
        f.write(missing_df.to_markdown(index=False))
        f.write("\n\n")
    
    print(f"[메타데이터 생성] {md_filename}")


def save_to_csv(items: List[Dict], filename: str, generate_metadata: bool = True):
    """CSV 파일로 저장"""
    if not items:
        print("[경고] 저장할 데이터가 없습니다.")
        return
    
    df = pd.DataFrame(items)
    
    # 컬럼 순서 정리
    priority_columns = ['원본_기관코드', '원본_병원명', '원본_주소']
    existing_priority = [col for col in priority_columns if col in df.columns]
    other_columns = [col for col in df.columns if col not in existing_priority]
    final_columns = existing_priority + other_columns
    df = df[final_columns]
    
    # CSV 저장
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"[저장 완료] {filename} ({len(df)}건, {len(df.columns)}개 컬럼)")
    
    # 메타데이터 생성 (선택적)
    if generate_metadata:
        generate_metadata_markdown(df, filename)


# ============================================================================
# 메인 실행 코드
# ============================================================================

def main():
    """메인 실행 함수"""
    
    print("=" * 80)
    print("의료기관 전체정보 조회 프로그램 v2.00")
    print("=" * 80)
    print()
    
    if TEST_MODE:
        print(f"[테스트 모드] 최대 {MAX_TEST_RECORDS}건만 처리합니다.")
        print()
    
    # 인증키 확인
    if SERVICE_KEY == "여기에_발급받은_디코딩_인증키를_입력하세요":
        print("[오류] 인증키를 설정하지 않았습니다.")
        return
    
    # 입력 파일 읽기
    try:
        hospital_df, detected_ykiho_column = load_hospital_list_from_csv(
            INPUT_CSV_FILE,
            ykiho_column=YKIHO_COLUMN
        )
        ykiho_column = detected_ykiho_column
    except Exception as e:
        print(f"[오류] CSV 파일 읽기 실패: {e}")
        return
    
    # 테스트 모드 처리
    if TEST_MODE:
        hospital_df = hospital_df.head(MAX_TEST_RECORDS)
        print(f"[테스트 모드] {len(hospital_df)}건으로 제한")
        print()
    
    # 체크포인트 파일 설정
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_file = f"checkpoint_all_{timestamp}.json"
    
    # 중간 저장 파일 설정
    script_dir = Path(__file__).parent
    output_dir = script_dir / "data"
    output_dir.mkdir(exist_ok=True)
    interim_csv_file = output_dir / f"병원전체정보_진행중_{timestamp}.csv"
    
    # 이전 진행상황 로드
    all_items = []
    processed_indices = set()
    start_index = 0
    
    if ENABLE_CHECKPOINT:
        checkpoint_data = load_checkpoint(checkpoint_file)
        if checkpoint_data:
            all_items = checkpoint_data.get('items', [])
            processed_indices = set(checkpoint_data.get('processed_indices', []))
            start_index = checkpoint_data.get('last_index', 0) + 1
            print(f"[재개] 인덱스 {start_index}부터 계속 진행합니다.")
            print()
    
    total_count = len(hospital_df)
    start_time = time.time()
    
    try:
        for idx in range(start_index, total_count):
            if idx in processed_indices:
                continue
            
            row = hospital_df.iloc[idx]
            ykiho = row[ykiho_column]
            
            # 요양기호 유효성 확인
            if pd.isna(ykiho) or str(ykiho).strip() == '':
                print(f"[경고] 인덱스 {idx}: 요양기호가 비어있습니다.")
                processed_indices.add(idx)
                continue
            
            # 원본 데이터 추출
            hospital_name = row.get('병원명', row.get('yadmNm', ''))
            hospital_addr = row.get('주소', row.get('addr', ''))
            
            # 진행률 계산
            processed_count = len(processed_indices)
            progress_pct = (processed_count / total_count * 100) if total_count > 0 else 0
            elapsed_time = time.time() - start_time
            
            if processed_count > 0 and elapsed_time > 0:
                items_per_sec = processed_count / elapsed_time
                remaining_items = total_count - processed_count
                eta_seconds = remaining_items / items_per_sec if items_per_sec > 0 else 0
                eta_str = f", 예상 남은 시간: {int(eta_seconds)}초"
            else:
                eta_str = ""
            
            print(f"[진행] {processed_count}/{total_count}건 ({progress_pct:.1f}%){eta_str}")
            print(f"  - 인덱스 {idx}: {hospital_name}")
            
            # 11개 API 호출
            hospital_info = get_hospital_all_info(
                service_key=SERVICE_KEY,
                use_encoded_key=USE_ENCODED_KEY,
                ykiho=ykiho,
                hospital_name=hospital_name,
                hospital_addr=hospital_addr
            )
            
            all_items.append(hospital_info)
            processed_indices.add(idx)
            
            # 체크포인트 저장 (JSON)
            if ENABLE_CHECKPOINT and len(processed_indices) % CHECKPOINT_INTERVAL == 0:
                checkpoint_data = {
                    'last_index': idx,
                    'processed_count': len(processed_indices),
                    'processed_indices': list(processed_indices),
                    'total_count': total_count,
                    'timestamp': datetime.now().isoformat(),
                    'items': all_items
                }
                save_checkpoint(checkpoint_data, checkpoint_file)
            
            # 중간 저장 (CSV) - 진행 중인 데이터를 주기적으로 CSV로 저장
            if ENABLE_INTERIM_SAVE and len(processed_indices) % INTERIM_SAVE_INTERVAL == 0:
                print(f"[중간 저장] {len(all_items)}건 저장 중...")
                save_to_csv(all_items, str(interim_csv_file), generate_metadata=False)
            
            print()
        
        print(f"[완료] 총 처리: {len(processed_indices)}건")
        
        # 완료 후 체크포인트 파일 삭제
        if ENABLE_CHECKPOINT and os.path.exists(checkpoint_file):
            try:
                os.remove(checkpoint_file)
                print(f"[체크포인트 삭제] {checkpoint_file}")
            except:
                pass
        
        # 최종 CSV 저장
        if all_items:
            final_csv_file = output_dir / f"병원전체정보_{timestamp}.csv"
            print(f"\n[최종 저장 시작]")
            save_to_csv(all_items, str(final_csv_file), generate_metadata=True)
            
            # 중간 저장 파일 삭제 (최종 파일이 생성되었으므로)
            if ENABLE_INTERIM_SAVE and interim_csv_file.exists():
                try:
                    interim_csv_file.unlink()
                    print(f"[중간 저장 파일 삭제] {interim_csv_file.name}")
                except:
                    pass
        
    except Exception as e:
        print(f"[오류 발생] {e}")
        
        # 오류 발생 시 체크포인트 저장
        if ENABLE_CHECKPOINT:
            checkpoint_data = {
                'last_index': idx if 'idx' in locals() else 0,
                'processed_count': len(processed_indices),
                'processed_indices': list(processed_indices),
                'total_count': total_count,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'items': all_items
            }
            save_checkpoint(checkpoint_data, checkpoint_file)
            print(f"[오류] 진행상황이 저장되었습니다. 다시 실행하면 이어서 진행됩니다.")


if __name__ == "__main__":
    main()
