# 건강보험심사평가원 의료기관별상세정보서비스 API 가이드라인 v2.00

## 📋 목차
1. [서비스 개요](#서비스-개요)
2. [11개 API 통합 조회](#11개-api-통합-조회)
3. [API 인증키 발급](#api-인증키-발급)
4. [API 명세](#api-명세)
5. [요청 파라미터](#요청-파라미터)
6. [응답 데이터 구조](#응답-데이터-구조)
7. [코드 구현 가이드](#코드-구현-가이드)
8. [에러 처리](#에러-처리)
9. [주의사항](#주의사항)

---

## 서비스 개요

### 서비스 정보
- **서비스명**: 의료기관별상세정보서비스 (MadmDtlInfoService2.7)
- **제공기관**: 건강보험심사평가원
- **서비스 설명**: 건강보험심사평가원에서 수집·관리하는 의료기관의 상세정보를 제공하는 서비스
- **인터페이스 표준**: REST API
- **응답 형식**: XML (기본), JSON (옵션)

### 제공 정보
- 시설정보
- 세부정보
- 진료과목정보
- 교통정보
- 의료장비정보
- 식대가산정보
- 간호등급정보
- 특수진료정보 (진료가능분야조회)
- 전문병원지정분야
- 전문과목별전문의수
- 기타인력수 정보

### 엔드포인트
- **Base URL**: `http://apis.data.go.kr/B551182/MadmDtlInfoService2.7`
- **Operation**: `/getDtlInfo` (상세정보 조회)

> [!IMPORTANT]
> **11개 API 통합 조회 권장**
> 
> v2.00 스크립트는 11개 모든 정보 카테고리를 통합 조회합니다. 단일 API만 호출하는 것보다 병원의 전체 정보를 한 번에 수집할 수 있어 효율적입니다.

> [!IMPORTANT]
> **암호화된 요양기호 사용**
> 
> 요양기호는 1:1로 매칭한 암호화된 요양기호로 제공되며, 별도의 복호화 방법 또는 요양기호는 제공하지 않습니다.
> 암호화된 요양기호는 건강보험심사평가원 '병원정보서비스' Open API > 병원기본목록에서 확인 가능합니다.

---

## 11개 API 통합 조회

### 제공되는 11개 API 목록

| 접두사 | Operation | 정보 카테고리 | 설명 |
|--------|-----------|--------------|------|
| `eqp` | `getEqpInfo2.7` | 시설정보 | 병상 수 등 시설 현황 |
| `dtl` | `getDtlInfo2.7` | 세부정보 | 병원명, 주소, 전화번호 등 기본 정보 |
| `dgsbjt` | `getDgsbjtInfo2.7` | 진료과목정보 | 개설된 진료과목 |
| `trnsprt` | `getTrnsprtInfo2.7` | 교통정보 | 주변 교통수단 |
| `medoft` | `getMedOftInfo2.7` | 의료장비정보 | 보유 의료 장비 현황 |
| `foepaddc` | `getFoepAddcInfo2.7` | 식대가산정보 | 입원 환자 식사 제공 가산 |
| `nursiggrd` | `getNursigGrdInfo2.7` | 간호등급정보 | 간호 등급 |
| `spcldiag` | `getSpclDiagInfo2.7` | 특수진료정보 | 전문 진료 가능 분야 |
| `spclhosp` | `getSpclHospAsgFldList2.7` | 전문병원지정분야 | 보건복지부 지정 전문병원 분야 |
| `spcsbtj` | `getSpcSbtjTsdrInfo2.7` | 전문과목별전문의수 | 진료 과목별 전문의 인원 수 |
| `etchst` | `getEtcHstInfo2.7` | 기타인력수정보 | 약사, 물리치료사 등 의료 인력 현황 |

### 통합 조회 전략

#### 1. 순차 호출 방식
- 단일 병원에 대해 11개 API를 순차적으로 호출
- 각 API 호출 간 0.1초 간격 유지 (서버 부하 방지)
- 개별 API 실패 시에도 다른 API는 계속 진행

#### 2. 데이터 통합 방식
- **접두사 기반 평탄화**: 각 API 응답에 고유 접두사 추가
- **예시**: `dtl_yadmNm`, `eqp_hospBdCnt`, `dgsbjt_dgsbjtCdNm`
- **충돌 방지**: 서로 다른 API에서 동일한 필드명이 있어도 접두사로 구분
- **중첩 구조 처리**: 중첩된 딕셔너리는 재귀적으로 평탄화
- **리스트 처리**: 리스트는 JSON 문자열로 변환하여 저장

#### 3. 출력 형식
- **CSV 파일**: 모든 API 응답을 단일 행으로 통합
- **메타데이터**: 자동 생성되는 마크다운 파일로 데이터 품질 분석

---

## API 인증키 발급

### 발급 절차
1. [공공데이터포털](http://data.go.kr) 접속
2. "의료기관별상세정보서비스" 검색
3. 활용신청 버튼 클릭
4. 신청 정보 입력 및 제출
5. 자동승인 (약 30분 후 사용 가능)

### 사용 제한
- **개발계정**: 일 1,000건 트래픽 제공
- **동기화 시간**: 공공데이터포털과 건강보험심사평가원 간 약 30분 소요

---

## API 명세

### 전체 URL 구조
```
http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getDtlInfo?ServiceKey={인증키}&ykiho={암호화된요양기호}&_type={응답형식}
```

### 응답 형식 선택
- **XML (기본)**: `_type` 파라미터 생략
- **JSON**: `_type=json` 추가

#### 예시
```
# XML 응답
http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getDtlInfo?ykiho=암호화된요양기호&ServiceKey=발급받은인증키

# JSON 응답
http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getDtlInfo?ykiho=암호화된요양기호&_type=json&ServiceKey=발급받은인증키
```

---

## 요청 파라미터

### 필수 파라미터

| 파라미터명 | 타입 | 필수여부 | 설명 | 예시 |
|-----------|------|---------|------|------|
| `ServiceKey` | String(400) | 필수 | 공공데이터포털에서 발급받은 인증키 | - |
| `ykiho` | String(400) | 필수 | 암호화된 요양기호 | - |

### 선택 파라미터

| 파라미터명 | 타입 | 필수여부 | 설명 | 예시 |
|-----------|------|---------|------|------|
| `_type` | String | 선택 | 응답 형식 (json 또는 xml) | `json` |

---

## 응답 데이터 구조

### 응답 헤더 (Header)
| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `resultCode` | String(5) | 결과코드 | `00` (정상) |
| `resultMsg` | String(50) | 결과메시지 | `NORMAL SERVICE.` |

### 응답 바디 (Body)
| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `items` | Object | 리스트 항목 | - |
| `items.item` | Object/Array | 세부 항목 | - |

### 병원 상세정보 항목 (Item)

상세정보 항목은 API 응답에 따라 다양하게 제공됩니다. 주요 항목은 다음과 같습니다:

#### 기본 정보
- `yadmNm`: 병원명
- `clCdNm`: 종별명
- `addr`: 주소
- `telno`: 전화번호
- `hospUrl`: 홈페이지

#### 위치 정보
- `sidoCdNm`: 시도명
- `sgguCdNm`: 시군구명
- `emdongNm`: 읍면동명
- `postNo`: 우편번호
- `XPos`: 경도
- `YPos`: 위도

---

## 코드 구현 가이드

### 1. Python 구현 예제

#### 기본 요청 (JSON 응답)
```python
import requests

# API 설정
SERVICE_KEY = "발급받은_인증키"  # 디코딩 키
BASE_URL = "http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getDtlInfo"
YKIHO = "암호화된_요양기호"  # 병원기본목록에서 획득

# 요청 파라미터
params = {
    'ServiceKey': SERVICE_KEY,
    'ykiho': YKIHO,
    '_type': 'json'
}

# API 호출
response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    
    # 응답 헤더 확인
    header = data['response']['header']
    if header['resultCode'] == '00':
        # 상세정보 추출
        body = data['response']['body']
        items = body.get('items', {}).get('item', {})
        
        print(f"병원명: {items.get('yadmNm')}")
        print(f"주소: {items.get('addr')}")
        print(f"전화번호: {items.get('telno')}")
    else:
        print(f"API 오류: {header['resultMsg']}")
else:
    print(f"HTTP 오류: {response.status_code}")
```

#### 11개 API 통합 조회 (v2.00)
```python
import requests
import pandas as pd
from typing import List, Dict
import time

# 11개 API 엔드포인트 설정
API_ENDPOINTS = {
    'eqp': {'operation': 'getEqpInfo2.7', 'name': '시설정보'},
    'dtl': {'operation': 'getDtlInfo2.7', 'name': '세부정보'},
    'dgsbjt': {'operation': 'getDgsbjtInfo2.7', 'name': '진료과목정보'},
    'trnsprt': {'operation': 'getTrnsprtInfo2.7', 'name': '교통정보'},
    'medoft': {'operation': 'getMedOftInfo2.7', 'name': '의료장비정보'},
    'foepaddc': {'operation': 'getFoepAddcInfo2.7', 'name': '식대가산정보'},
    'nursiggrd': {'operation': 'getNursigGrdInfo2.7', 'name': '간호등급정보'},
    'spcldiag': {'operation': 'getSpclDiagInfo2.7', 'name': '특수진료정보'},
    'spclhosp': {'operation': 'getSpclHospAsgFldList2.7', 'name': '전문병원지정분야'},
    'spcsbtj': {'operation': 'getSpcSbtjTsdrInfo2.7', 'name': '전문과목별전문의수'},
    'etchst': {'operation': 'getEtcHstInfo2.7', 'name': '기타인력수정보'}
}

def flatten_dict_with_prefix(data: Dict, prefix: str) -> Dict:
    """딕셔너리 평탄화 및 접두사 추가"""
    items = []
    for k, v in data.items():
        new_key = f"{prefix}_{k}"
        if isinstance(v, dict):
            items.extend(flatten_dict_with_prefix(v, prefix).items())
        elif isinstance(v, list):
            items.append((new_key, json.dumps(v, ensure_ascii=False)))
        else:
            items.append((new_key, v))
    return dict(items)

def get_hospital_all_info(service_key: str, ykiho: str) -> Dict:
    """단일 병원의 모든 정보 조회 (11개 API)"""
    BASE_URL = "http://apis.data.go.kr/B551182/MadmDtlInfoService2.7"
    result = {'원본_기관코드': ykiho}
    
    for prefix, endpoint_info in API_ENDPOINTS.items():
        operation = endpoint_info['operation']
        api_url = f"{BASE_URL}/{operation}"
        
        params = {
            'ServiceKey': service_key,
            'ykiho': ykiho,
            '_type': 'json'
        }
        
        try:
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            header = data['response']['header']
            
            if header['resultCode'] == '00':
                body = data['response']['body']
                items = body.get('items', {}).get('item', {})
                
                if items and isinstance(items, dict):
                    # 접두사 추가하여 평탄화
                    flattened = flatten_dict_with_prefix(items, prefix)
                    result.update(flattened)
                    print(f"  [{prefix}] {endpoint_info['name']}: 성공")
            
        except Exception as e:
            print(f"  [{prefix}] {endpoint_info['name']}: 오류 - {e}")
        
        time.sleep(0.1)  # API 호출 간격
    
    return result

def main():
    SERVICE_KEY = "발급받은_인증키"
    
    # CSV 파일에서 병원 목록 읽기
    df = pd.read_csv('병원목록.csv', encoding='utf-8-sig')
    
    all_results = []
    for idx, row in df.iterrows():
        ykiho = row['ykiho']
        print(f"[{idx+1}/{len(df)}] {row.get('병원명', '')}")
        
        hospital_info = get_hospital_all_info(SERVICE_KEY, ykiho)
        all_results.append(hospital_info)
    
    # 결과 저장
    result_df = pd.DataFrame(all_results)
    result_df.to_csv('병원전체정보.csv', index=False, encoding='utf-8-sig')
    print(f"총 {len(all_results)}건 저장 완료")

if __name__ == "__main__":
    main()
```

---

## 에러 처리

### 공공데이터포털 에러 코드

| 에러코드 | 에러메시지 | 설명 | 해결방법 |
|---------|-----------|------|---------|
| `0` | `NORMAL_CODE` | 정상 | - |
| `3` | `NODATA_ERROR` | 데이터없음 에러 | 요양기호 확인 |
| `22` | `LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR` | 서비스 요청제한횟수 초과에러 | 일일 트래픽 확인 (1,000건) |
| `30` | `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` | 등록되지 않은 서비스키 | 인증키 재확인 |
| `31` | `DEADLINE_HAS_EXPIRED_ERROR` | 기한만료된 서비스키 | 인증키 재발급 |

### Python 에러 처리 예제

```python
import requests
from typing import Optional, Dict

class HospitalDetailAPIError(Exception):
    """병원 상세정보 API 에러"""
    pass

def get_hospital_detail_safe(service_key: str, ykiho: str) -> Optional[Dict]:
    """안전한 API 호출 (에러 처리 포함)"""
    BASE_URL = "http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getDtlInfo"
    
    params = {
        'ServiceKey': service_key,
        'ykiho': ykiho,
        '_type': 'json'
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        header = data['response']['header']
        
        if header['resultCode'] != '00':
            error_code = header['resultCode']
            error_msg = header['resultMsg']
            
            if error_code == '3':
                print("해당 요양기호의 상세정보가 없습니다.")
                return None
            elif error_code == '22':
                raise HospitalDetailAPIError("일일 트래픽 제한 초과 (1,000건)")
            elif error_code == '30':
                raise HospitalDetailAPIError("등록되지 않은 서비스키입니다.")
            else:
                raise HospitalDetailAPIError(f"API Error [{error_code}]: {error_msg}")
        
        return data['response']['body'].get('items', {}).get('item', {})
        
    except requests.exceptions.Timeout:
        print("API 호출 시간 초과. 잠시 후 다시 시도하세요.")
        return None
    except requests.exceptions.ConnectionError:
        print("네트워크 연결 오류. 인터넷 연결을 확인하세요.")
        return None
    except HospitalDetailAPIError as e:
        print(f"API 에러: {e}")
        return None
    except Exception as e:
        print(f"예상치 못한 에러: {e}")
        return None
```

---

## 주의사항

### 1. 인증키 관리
- ⚠️ **인증키는 절대 공개 저장소에 업로드하지 마세요**
- 환경변수 또는 별도 설정 파일로 관리 권장
- `.gitignore`에 설정 파일 추가

```python
# 환경변수 사용 예시
import os
SERVICE_KEY = os.getenv('HOSPITAL_DETAIL_API_KEY')
```

### 2. 암호화된 요양기호 획득
- 병원기본목록 API를 먼저 호출하여 암호화된 요양기호 획득 필요
- 요양기호는 복호화할 수 없으며, API 간 1:1 매칭으로만 사용 가능

### 3. 응답 데이터 처리
- **단일 결과**: `items.item`이 딕셔너리 형태
- **복수 결과**: `items.item`이 리스트 형태 (드물지만 가능)
- 반드시 타입 체크 후 처리

```python
items = body.get('items', {}).get('item', {})
if isinstance(items, list):
    # 복수 결과 처리
    for item in items:
        process(item)
else:
    # 단일 결과 처리
    process(items)
```

### 4. 트래픽 제한
- **개발계정**: 일 1,000건
- 대량 데이터 수집 시 적절한 딜레이 추가 권장
- 운영계정 필요 시 별도 신청

### 5. 데이터 갱신 주기
- 공공데이터포털과 건강보험심사평가원 간 동기화: 약 30분
- 실시간 데이터가 아닐 수 있음

---

## 참고 자료

- [공공데이터포털](http://data.go.kr)
- [건강보험심사평가원](https://www.hira.or.kr)
- [의료기관별상세정보서비스 API 페이지](https://www.data.go.kr/data/15001699/openapi.do)

---

## 버전 정보
- **가이드 버전**: 2.0
- **최종 수정일**: 2026-01-16
- **작성 기준**: 공공데이터포털 API 명세
- **주요 변경**: 11개 API 통합 조회 방식 추가
