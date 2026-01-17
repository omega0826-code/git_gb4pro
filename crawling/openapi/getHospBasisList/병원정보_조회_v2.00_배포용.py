"""
병원정보 조회 API 호출 스크립트 v2.00 (배포용)
================================================================================
버전: 2.00
작성일: 2026-01-17
목적: 건강보험심사평가원 병원정보서비스 API를 사용하여 병원 기본정보 조회
================================================================================

이 스크립트는 다음과 같은 기능을 제공합니다:
- 지역별, 진료과목별, 종별 등 다양한 조건으로 병원 검색
- 자동 페이징 처리로 전체 데이터 수집
- 체크포인트 기능으로 중단 후 재개 가능
- 진행률 실시간 표시
- CSV 파일로 결과 저장 (암호화된 요양기호 포함)
"""

import requests
import json
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import time
import os
from pathlib import Path


# ============================================================================
# ⚙️ 사용자 설정 영역 - 아래 항목들을 수정하세요
# ============================================================================

# 1. 인증키 설정 (필수) ⭐
# 공공데이터포털(https://www.data.go.kr)에서 발급받은 디코딩 인증키를 입력하세요
SERVICE_KEY = "여기에_발급받은_디코딩_인증키를_입력하세요"

# 2. API 키 타입 설정
# True: 인코딩 키 사용 (URL에 직접 포함)
# False: 디코딩 키 사용 (권장)
USE_ENCODED_KEY = False

# 3. 검색 조건 설정
# 아래 예시를 참고하여 원하는 검색 조건을 설정하세요

# 예시 1: 서울 강남구 피부과 검색
SEARCH_SIDO = '서울'           # 시도명 (예: '서울', '부산', '경기' 등)
SEARCH_SGGU = '강남구'         # 시군구명 (예: '강남구', '서초구' 등)
SEARCH_DGSBJ = '피부과'        # 진료과목 (예: '피부과', '내과', '정형외과' 등)
SEARCH_CL = None              # 종별 (예: '의원', '병원', '종합병원' 등, None이면 전체)
SEARCH_YADM_NM = None         # 병원명 (예: '서울의료원', None이면 전체)
SEARCH_EMDONG_NM = None       # 읍면동명 (예: '삼성동', None이면 전체)

# 예시 2: 특정 병원명으로 검색 (사용하려면 위 예시 1을 주석 처리하고 아래 주석 해제)
# SEARCH_SIDO = None
# SEARCH_SGGU = None
# SEARCH_DGSBJ = None
# SEARCH_CL = None
# SEARCH_YADM_NM = '서울의료원'
# SEARCH_EMDONG_NM = None

# 4. 재시도 설정
MAX_RETRIES = 3          # 최대 재시도 횟수
RETRY_DELAY = 1          # 초기 재시도 대기 시간 (초)

# 5. 타임아웃 설정
CONNECT_TIMEOUT = 10     # 연결 타임아웃 (초)
READ_TIMEOUT = 60        # 읽기 타임아웃 (초)

# 6. 체크포인트 설정
ENABLE_CHECKPOINT = True # 진행상황 저장 활성화 (중단 후 재개 가능)
CHECKPOINT_INTERVAL = 5  # 체크포인트 저장 간격 (페이지 단위)

# 7. 출력 파일 설정
OUTPUT_INCLUDE_YKIHO = True  # 암호화된 요양기호 포함 여부 (상세정보 조회 시 필요)

# ============================================================================
# 🔧 시스템 설정 영역 - 일반적으로 수정할 필요 없음
# ============================================================================

# API 기본 정보
API_BASE_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

# 지역 코드 (시도/시군구)
SIDO_CODES = {
    '서울': '110000',
    '부산': '260000',
    '대구': '270000',
    '인천': '280000',
    '광주': '290000',
    '대전': '300000',
    '울산': '310000',
    '세종': '360000',
    '경기': '410000',
    '강원': '430000',
    '충북': '440000',
    '충남': '450000',
    '전북': '460000',
    '전남': '470000',
    '경북': '480000',
    '경남': '490000',
    '제주': '500000'
}

# 서울 시군구 코드 (API v2 기준)
SEOUL_SGGU_CODES = {
    '강남구': '110001',
    '강동구': '110002',
    '강북구': '110003',
    '강서구': '110004',
    '관악구': '110005',
    '광진구': '110006',
    '구로구': '110007',
    '금천구': '110008',
    '노원구': '110009',
    '도봉구': '110010',
    '동대문구': '110011',
    '동작구': '110012',
    '마포구': '110013',
    '서대문구': '110014',
    '서초구': '110015',
    '성동구': '110016',
    '성북구': '110017',
    '송파구': '110018',
    '양천구': '110019',
    '영등포구': '110020',
    '용산구': '110021',
    '은평구': '110022',
    '종로구': '110023',
    '중구': '110024',
    '중랑구': '110025'
}

# 진료과목 코드
DGSBJ_CODES = {
    '일반의': '00',
    '내과': '01',
    '신경과': '02',
    '정신건강의학과': '03',
    '외과': '04',
    '정형외과': '05',
    '신경외과': '06',
    '흉부외과': '07',
    '성형외과': '08',
    '마취통증의학과': '09',
    '산부인과': '10',
    '소아청소년과': '11',
    '안과': '12',
    '이비인후과': '13',
    '피부과': '14',
    '비뇨의학과': '15',
    '가정의학과': '23',
    '응급의학과': '24'
}

# 종별 코드
CL_CODES = {
    '상급종합병원': '01',
    '종합병원': '11',
    '병원': '21',
    '요양병원': '28',
    '정신병원': '29',
    '의원': '31',
    '치과병원': '41',
    '치과의원': '51',
    '조산원': '61',
    '보건소': '71',
    '보건지소': '72',
    '보건진료소': '73',
    '보건의료원': '75',
    '한방병원': '92',
    '한의원': '93'
}


# ============================================================================
# API 호출 함수
# ============================================================================

def get_hospital_list(
    service_key: str,
    use_encoded_key: bool = False,
    sido_cd: Optional[str] = None,
    sggu_cd: Optional[str] = None,
    emdong_nm: Optional[str] = None,
    yadm_nm: Optional[str] = None,
    cl_cd: Optional[str] = None,
    dgsbj_cd: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
    max_retries: int = MAX_RETRIES,
    retry_delay: int = RETRY_DELAY
) -> Dict:
    """
    병원정보 API 호출 함수 (재시도 로직 포함)
    
    Parameters:
    -----------
    service_key : str
        공공데이터포털에서 발급받은 인증키 (인코딩 또는 디코딩)
    use_encoded_key : bool
        True: 인코딩 키 사용 (URL에 직접 포함)
        False: 디코딩 키 사용 (params로 전달)
    sido_cd : str, optional
        시도코드 (예: '110000' - 서울)
    sggu_cd : str, optional
        시군구코드 (예: '110001' - 강남구)
    emdong_nm : str, optional
        읍면동명 (예: '삼성동')
    yadm_nm : str, optional
        병원명 (예: '서울의료원')
    cl_cd : str, optional
        종별코드 (예: '31' - 의원)
    dgsbj_cd : str, optional
        진료과목코드 (예: '14' - 피부과)
    page_no : int
        페이지 번호 (기본값: 1)
    num_of_rows : int
        한 페이지 결과 수 (기본값: 100)
    max_retries : int
        최대 재시도 횟수 (기본값: 3)
    retry_delay : int
        초기 재시도 대기 시간 (기본값: 1초)
    
    Returns:
    --------
    dict
        API 응답 데이터 (JSON 형식)
    
    Raises:
    -------
    Exception
        API 호출 실패 시 예외 발생
    """
    
    # 요청 파라미터 구성
    params = {
        'pageNo': page_no,
        'numOfRows': num_of_rows,
        '_type': 'json'  # JSON 형식으로 응답 받기
    }
    
    # API 키 처리 방식 결정
    if use_encoded_key:
        # 인코딩 키: URL에 직접 포함
        api_url = f"{API_BASE_URL}?ServiceKey={service_key}"
    else:
        # 디코딩 키: params로 전달 (requests가 자동 인코딩)
        api_url = API_BASE_URL
        params['ServiceKey'] = service_key
    
    # 선택적 파라미터 추가 (값이 있을 때만)
    if sido_cd:
        params['sidoCd'] = sido_cd
    if sggu_cd:
        params['sgguCd'] = sggu_cd
    if emdong_nm:
        params['emdongNm'] = emdong_nm
    if yadm_nm:
        params['yadmNm'] = yadm_nm
    if cl_cd:
        params['clCd'] = cl_cd
    if dgsbj_cd:
        params['dgsbjtCd'] = dgsbj_cd
    
    # 재시도 로직
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                wait_time = retry_delay * (2 ** (attempt - 1))  # 지수 백오프
                print(f"[재시도 {attempt}/{max_retries}] {wait_time}초 대기 중...")
                time.sleep(wait_time)
            
            # API 호출
            if attempt == 0:
                print(f"[API 호출] 페이지: {page_no}, 결과 수: {num_of_rows}")
            
            response = requests.get(
                api_url, 
                params=params, 
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
            
            # HTTP 상태 코드 확인
            response.raise_for_status()
            
            # JSON 파싱
            data = response.json()
            
            # API 응답 헤더 확인
            header = data['response']['header']
            if header['resultCode'] != '00':
                raise Exception(f"API 오류 [{header['resultCode']}]: {header['resultMsg']}")
            
            return data
            
        except requests.exceptions.Timeout as e:
            last_exception = Exception(f"API 호출 시간 초과 (연결: {CONNECT_TIMEOUT}초, 읽기: {READ_TIMEOUT}초)")
            if attempt < max_retries:
                print(f"[경고] {last_exception}")
                continue
        except requests.exceptions.ConnectionError as e:
            last_exception = Exception("네트워크 연결 오류. 인터넷 연결을 확인하세요.")
            if attempt < max_retries:
                print(f"[경고] {last_exception}")
                continue
        except requests.exceptions.HTTPError as e:
            # HTTP 에러 발생 시 응답 내용 출력
            error_msg = f"HTTP 오류: {e}"
            try:
                error_response = e.response.text
                print(f"\n[API 응답 내용]\n{error_response}\n")
                error_msg += f"\n응답 내용: {error_response}"
            except:
                pass
            last_exception = Exception(error_msg)
            # HTTP 에러는 재시도하지 않음 (인증 오류 등)
            break
        except KeyError as e:
            last_exception = Exception(f"응답 데이터 형식 오류: {e}")
            break
        except Exception as e:
            last_exception = Exception(f"예상치 못한 오류: {e}")
            if attempt < max_retries:
                print(f"[경고] {last_exception}")
                continue
    
    # 모든 재시도 실패
    raise last_exception


def save_checkpoint(data: Dict, checkpoint_file: str):
    """
    체크포인트 저장
    
    Parameters:
    -----------
    data : dict
        저장할 데이터
    checkpoint_file : str
        체크포인트 파일 경로
    """
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[체크포인트 저장] {checkpoint_file}")
    except Exception as e:
        print(f"[경고] 체크포인트 저장 실패: {e}")


def load_checkpoint(checkpoint_file: str) -> Optional[Dict]:
    """
    체크포인트 로드
    
    Parameters:
    -----------
    checkpoint_file : str
        체크포인트 파일 경로
    
    Returns:
    --------
    dict or None
        저장된 데이터 또는 None
    """
    if not os.path.exists(checkpoint_file):
        return None
    
    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[체크포인트 로드] {checkpoint_file}")
        print(f"  - 이전 진행: 페이지 {data.get('last_page', 0)}, {data.get('total_items', 0)}건 수집")
        return data
    except Exception as e:
        print(f"[경고] 체크포인트 로드 실패: {e}")
        return None


def get_all_hospitals(
    service_key: str,
    use_encoded_key: bool = False,
    sido_cd: Optional[str] = None,
    sggu_cd: Optional[str] = None,
    emdong_nm: Optional[str] = None,
    yadm_nm: Optional[str] = None,
    cl_cd: Optional[str] = None,
    dgsbj_cd: Optional[str] = None,
    max_results: Optional[int] = None,
    enable_checkpoint: bool = ENABLE_CHECKPOINT,
    checkpoint_file: Optional[str] = None
) -> List[Dict]:
    """
    모든 페이지의 병원 정보를 가져오는 함수 (체크포인트 지원)
    
    Parameters:
    -----------
    service_key : str
        공공데이터포털에서 발급받은 인증키
    use_encoded_key : bool
        True: 인코딩 키 사용, False: 디코딩 키 사용
    sido_cd, sggu_cd, emdong_nm, yadm_nm, cl_cd, dgsbj_cd : str, optional
        검색 조건 (get_hospital_list 함수 참조)
    max_results : int, optional
        최대 결과 수 (None이면 전체 조회)
    enable_checkpoint : bool
        체크포인트 기능 활성화 여부
    checkpoint_file : str, optional
        체크포인트 파일 경로 (None이면 자동 생성)
    
    Returns:
    --------
    list
        모든 병원 정보 리스트
    """
    
    # 체크포인트 파일 설정
    if enable_checkpoint and checkpoint_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_file = f"checkpoint_{timestamp}.json"
    
    # 이전 진행상황 로드
    all_items = []
    page_no = 1
    
    if enable_checkpoint and checkpoint_file:
        checkpoint_data = load_checkpoint(checkpoint_file)
        if checkpoint_data:
            all_items = checkpoint_data.get('items', [])
            page_no = checkpoint_data.get('last_page', 0) + 1
            print(f"[재개] 페이지 {page_no}부터 계속 진행합니다.")
    
    num_of_rows = 100  # 한 번에 가져올 최대 개수
    start_time = time.time()
    
    try:
        while True:
            # API 호출
            data = get_hospital_list(
                service_key=service_key,
                use_encoded_key=use_encoded_key,
                sido_cd=sido_cd,
                sggu_cd=sggu_cd,
                emdong_nm=emdong_nm,
                yadm_nm=yadm_nm,
                cl_cd=cl_cd,
                dgsbj_cd=dgsbj_cd,
                page_no=page_no,
                num_of_rows=num_of_rows
            )
            
            # 응답 바디 확인
            body = data['response']['body']
            total_count = body.get('totalCount', 0)
            
            # 진행률 계산
            progress_pct = (len(all_items) / total_count * 100) if total_count > 0 else 0
            elapsed_time = time.time() - start_time
            
            if len(all_items) > 0 and elapsed_time > 0:
                items_per_sec = len(all_items) / elapsed_time
                remaining_items = total_count - len(all_items)
                eta_seconds = remaining_items / items_per_sec if items_per_sec > 0 else 0
                eta_str = f", 예상 남은 시간: {int(eta_seconds)}초"
            else:
                eta_str = ""
            
            print(f"[진행] 전체 {total_count}건 중 {len(all_items)}건 ({progress_pct:.1f}%){eta_str}")
            
            # 아이템 추출
            items = body.get('items', {}).get('item', [])
            
            # 단일 결과인 경우 리스트로 변환
            if isinstance(items, dict):
                items = [items]
            
            # 결과가 없으면 종료
            if not items:
                break
            
            # 결과 추가
            all_items.extend(items)
            
            # 체크포인트 저장 (일정 간격마다)
            if enable_checkpoint and checkpoint_file and page_no % CHECKPOINT_INTERVAL == 0:
                checkpoint_data = {
                    'last_page': page_no,
                    'total_items': len(all_items),
                    'total_count': total_count,
                    'timestamp': datetime.now().isoformat(),
                    'items': all_items
                }
                save_checkpoint(checkpoint_data, checkpoint_file)
            
            # 최대 결과 수 확인
            if max_results and len(all_items) >= max_results:
                all_items = all_items[:max_results]
                break
            
            # 모든 데이터를 가져왔는지 확인
            if len(all_items) >= total_count:
                break
            
            # 다음 페이지로
            page_no += 1
        
        print(f"[완료] 총 {len(all_items)}건 조회 완료")
        
        # 완료 후 체크포인트 파일 삭제
        if enable_checkpoint and checkpoint_file and os.path.exists(checkpoint_file):
            try:
                os.remove(checkpoint_file)
                print(f"[체크포인트 삭제] {checkpoint_file}")
            except:
                pass
        
        return all_items
        
    except Exception as e:
        # 오류 발생 시 현재까지의 데이터 체크포인트 저장
        if enable_checkpoint and checkpoint_file:
            checkpoint_data = {
                'last_page': page_no - 1,
                'total_items': len(all_items),
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'items': all_items
            }
            save_checkpoint(checkpoint_data, checkpoint_file)
            print(f"\n[오류] 진행상황이 저장되었습니다. 다시 실행하면 이어서 진행됩니다.")
        raise


# ============================================================================
# 데이터 처리 함수
# ============================================================================


def save_to_csv(items: List[Dict], filename: str, include_ykiho: bool = True):
    """
    병원 정보를 CSV 파일로 저장 (암호화된 요양기호 포함)
    
    Parameters:
    -----------
    items : list
        병원 정보 리스트
    filename : str
        저장할 파일명 (예: 'hospitals.csv')
    include_ykiho : bool
        암호화된 요양기호 포함 여부 (기본값: True)
    """
    
    if not items:
        print("[경고] 저장할 데이터가 없습니다.")
        return
    
    # 데이터프레임 생성
    df = pd.DataFrame(items)
    
    # 주요 컬럼 선택 (암호화된 요양기호 포함)
    columns = [
        'yadmNm',      # 병원명
        'clCdNm',      # 종별명
        'sidoCdNm',    # 시도명
        'sgguCdNm',    # 시군구명
        'emdongNm',    # 읍면동명
        'addr',        # 주소
        'postNo',      # 우편번호
        'telno',       # 전화번호
        'hospUrl',     # 홈페이지
        'estbDd',      # 개설일자
        'drTotCnt',    # 의사총수
        'mdeptSdrCnt', # 의과전문의
        'detySdrCnt',  # 치과전문의
        'cmdcSdrCnt',  # 한방전문의
        'XPos',        # 경도
        'YPos'         # 위도
    ]
    
    # 암호화된 요양기호 추가
    if include_ykiho and 'ykiho' in df.columns:
        columns.insert(0, 'ykiho')  # 첫 번째 컬럼으로 추가
    
    # 존재하는 컬럼만 선택
    available_columns = [col for col in columns if col in df.columns]
    df_selected = df[available_columns]
    
    # 컬럼명 한글화
    column_names = {
        'ykiho': '암호화요양기호',
        'yadmNm': '병원명',
        'clCdNm': '종별',
        'sidoCdNm': '시도',
        'sgguCdNm': '시군구',
        'emdongNm': '읍면동',
        'addr': '주소',
        'postNo': '우편번호',
        'telno': '전화번호',
        'hospUrl': '홈페이지',
        'estbDd': '개설일자',
        'drTotCnt': '의사총수',
        'mdeptSdrCnt': '의과전문의',
        'detySdrCnt': '치과전문의',
        'cmdcSdrCnt': '한방전문의',
        'XPos': '경도',
        'YPos': '위도'
    }
    df_selected = df_selected.rename(columns=column_names)
    
    # CSV 저장 (UTF-8 with BOM for Excel compatibility)
    df_selected.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"[CSV 저장 완료] {filename} ({len(df_selected)}건)")
    
    # 암호화된 요양기호 포함 여부 확인
    if include_ykiho and '암호화요양기호' in df_selected.columns:
        print(f"  - 암호화된 요양기호 포함됨 (상세정보 조회 API에 사용 가능)")


def print_hospital_info(items: List[Dict], max_display: int = 10):
    """
    병원 정보를 콘솔에 출력
    
    Parameters:
    -----------
    items : list
        병원 정보 리스트
    max_display : int
        최대 출력 개수 (기본값: 10)
    """
    
    if not items:
        print("[결과 없음] 검색 조건에 맞는 병원이 없습니다.")
        return
    
    print(f"\n{'='*80}")
    print(f"검색 결과: 총 {len(items)}건")
    print(f"{'='*80}\n")
    
    for i, item in enumerate(items[:max_display], 1):
        print(f"[{i}] {item.get('yadmNm', '-')}")
        print(f"    종별: {item.get('clCdNm', '-')}")
        print(f"    주소: {item.get('addr', '-')}")
        print(f"    전화: {item.get('telno', '-')}")
        print(f"    의사수: {item.get('drTotCnt', '0')}명")
        print()
    
    if len(items) > max_display:
        print(f"... 외 {len(items) - max_display}건")
        print()


# ============================================================================
# 메인 실행 코드
# ============================================================================

def main():
    """
    메인 실행 함수
    """
    
    print("="*80)
    print("병원정보 조회 프로그램 v2.00")
    print("="*80)
    print()
    
    # ========================================
    # 1. 인증키 확인
    # ========================================
    if SERVICE_KEY == "여기에_발급받은_디코딩_인증키를_입력하세요":
        print("[오류] 인증키를 설정하지 않았습니다.")
        print("스크립트 상단의 SERVICE_KEY 변수에 발급받은 디코딩 인증키를 입력하세요.")
        print()
        print("인증키 발급 방법:")
        print("1. https://www.data.go.kr 접속")
        print("2. 병원정보서비스 API 활용신청")
        print("3. 마이페이지 > 인증키 발급현황에서 '디코딩 인증키' 복사")
        return
    
    # ========================================
    # 2. 검색 조건 설정
    # ========================================
    # 사용자가 설정한 검색 조건을 코드로 변환
    sido_cd = SIDO_CODES.get(SEARCH_SIDO) if SEARCH_SIDO else None
    
    # 시군구 코드 변환 (현재는 서울만 지원, 필요시 다른 지역 추가)
    sggu_cd = None
    if SEARCH_SGGU and SEARCH_SIDO == '서울':
        sggu_cd = SEOUL_SGGU_CODES.get(SEARCH_SGGU)
    
    dgsbj_cd = DGSBJ_CODES.get(SEARCH_DGSBJ) if SEARCH_DGSBJ else None
    cl_cd = CL_CODES.get(SEARCH_CL) if SEARCH_CL else None
    
    # 검색 조건 출력
    print(f"[검색 조건]")
    if SEARCH_SIDO:
        print(f"  - 시도: {SEARCH_SIDO}")
    if SEARCH_SGGU:
        print(f"  - 시군구: {SEARCH_SGGU}")
    if SEARCH_DGSBJ:
        print(f"  - 진료과목: {SEARCH_DGSBJ}")
    if SEARCH_CL:
        print(f"  - 종별: {SEARCH_CL}")
    if SEARCH_YADM_NM:
        print(f"  - 병원명: {SEARCH_YADM_NM}")
    if SEARCH_EMDONG_NM:
        print(f"  - 읍면동: {SEARCH_EMDONG_NM}")
    print()
    
    # ========================================
    # 3. API 호출
    # ========================================
    try:
        # 모든 결과 조회
        hospitals = get_all_hospitals(
            service_key=SERVICE_KEY,
            use_encoded_key=USE_ENCODED_KEY,
            sido_cd=sido_cd,
            sggu_cd=sggu_cd,
            dgsbj_cd=dgsbj_cd,
            cl_cd=cl_cd,
            yadm_nm=SEARCH_YADM_NM,
            emdong_nm=SEARCH_EMDONG_NM
        )
        
        # ========================================
        # 4. 결과 출력
        # ========================================
        print_hospital_info(hospitals, max_display=10)
        
        # ========================================
        # 5. CSV 저장
        # ========================================
        if hospitals:
            # data 폴더 생성 (없으면 생성)
            script_dir = Path(__file__).parent
            output_dir = script_dir / "data"
            output_dir.mkdir(exist_ok=True)
            
            # 파일명 생성 (현재 날짜시간 포함)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 검색 조건을 파일명에 포함
            filename_parts = []
            if SEARCH_SIDO:
                filename_parts.append(SEARCH_SIDO)
            if SEARCH_SGGU:
                filename_parts.append(SEARCH_SGGU)
            if SEARCH_DGSBJ:
                filename_parts.append(SEARCH_DGSBJ)
            if SEARCH_CL:
                filename_parts.append(SEARCH_CL)
            if SEARCH_YADM_NM:
                filename_parts.append(SEARCH_YADM_NM)
            
            filename_prefix = "_".join(filename_parts) if filename_parts else "병원목록"
            csv_filename = output_dir / f"{filename_prefix}_{timestamp}.csv"
            
            # CSV 저장 (암호화된 요양기호 포함)
            save_to_csv(hospitals, str(csv_filename), include_ykiho=OUTPUT_INCLUDE_YKIHO)
        
    except Exception as e:
        print(f"[오류 발생] {e}")
        print()
        print("문제 해결 방법:")
        print("1. 인증키가 올바른지 확인 (디코딩 키 사용)")
        print("2. 인터넷 연결 확인")
        print("3. 인증키 발급 후 30분 이상 경과했는지 확인")


# ============================================================================
# 프로그램 실행
# ============================================================================

if __name__ == "__main__":
    # 메인 함수 실행
    main()
