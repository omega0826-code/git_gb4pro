# 파이썬 기반 주소 전처리 및 지오코딩(Geocoding) 가이드라인

> **문서 버전**: V1.0.1
> **최종 업데이트**: 2026-01-25
> **작성자**: EDA Team

---

## 1. 개요 (Overview)
본 문서는 파이썬(Python)을 활용하여 비정형 **도로명 주소**나 **지번 주소**를 데이터 분석에 활용 가능한 형태로 전처리하고, 이를 **위도(Latitude)**와 **경도(Longitude)** 좌표로 변환(Geocoding)하는 표준 절차를 정의합니다.

이 문서는 지속적으로 업데이트되는 살아있는 문서(Living Document)를 지향하므로, 변경 사항 발생 시 반드시 하단의 [버전 관리](#7-버전-관리-revision-history) 섹션을 업데이트해야 합니다.

## 2. 사전 준비 (Prerequisites)
지오코딩 수행을 위해서는 다음 라이브러리와 API 키가 필요합니다.

*   **Python Libraries**: `pandas`, `requests`
*   **API Key**: Kakao Local API (추천), VWorld, 또는 Google Maps API Key
    *   *Kakao API 추천 사유*: 한국 주소지(특히 지번)에 대한 정확도가 가장 높고, 일일 무료 사용량(30만 건)이 여유로움.

## 3. 주소 전처리 가이드 (Address Preprocessing)
지오코딩 API의 성공률(Hit Rate)을 높이기 위해 원본 주소 데이터를 정제해야 합니다.

### 3.1 주요 정제 규칙
1.  **괄호 및 부가 정보 제거**: 
    *   `서울 강남구 강남대로 566 (논현동, 신영와코루빌딩)` 
    *   -> `서울 강남구 강남대로 566`
    *   *(괄호 안의 동 이름이나 건물명은 API 검색 시 노이즈가 될 수 있음)*
2.  **상세 주소 분리**: 
    *   `층`, `호` 등 상세 정보는 검색에 불필요하므로 제외합니다.
3.  **특수문자 제거**: 
    *   콤마(`,`), 탭(`\t`) 등을 공백으로 치환합니다.

### 3.2 Python 구현 예시
```python
import re

def clean_address(addr):
    if not isinstance(addr, str): 
        return ""
    
    # 1. 괄호와 괄호 안의 내용 제거 r'\([^)]*\)'
    addr = re.sub(r'\(.*?\)', '', addr)
    
    # 2. '1층', '지하1층' 등 층수 정보 제거 (선택)
    addr = re.sub(r'\d+층', '', addr)
    addr = re.sub(r'지하\s*\d+층', '', addr)
    
    # 3. 콤마 기준 앞부분만 사용 (예: "주소1, 주소2" -> "주소1")
    if ',' in addr:
        addr = addr.split(',')[0]
        
    # 4. 양끝 공백 및 이중 공백 제거
    addr = " ".join(addr.split())
    
    return addr
```

## 4. 지오코딩 구현 (Geocoding with Kakao API)

### 4.1 기본 코드
```python
import requests
import os
from dotenv import load_dotenv

# .env 파일 활성화 (환경 변수 로드)
load_dotenv()

def geocode_address(address):
    """
    주소를 입력받아 위도(y), 경도(x)를 반환하는 함수
    :param address: 정제된 주소 문자열
    :return: (lat, lon) 튜플 or (None, None)
    """
    # 환경 변수에서 API 키 가져오기
    api_key = os.getenv("KAKAO_API_KEY")
    
    if not api_key:
        raise ValueError("API Key가 설정되지 않았습니다. .env 파일을 확인해주세요.")

    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status() # 4xx, 5xx 에러 체크
        
        result = resp.json()
        if result['documents']:
            # 첫 번째 검색 결과가 가장 정확도 높음
            doc = result['documents'][0]
            x = doc['x'] # 경도 (Longitude)
            y = doc['y'] # 위도 (Latitude)
            return float(y), float(x)
            
    except requests.exceptions.RequestException as e:
        print(f"Network Error converting '{address}': {e}")
    except Exception as e:
        print(f"Error converting '{address}': {e}")
        
    return None, None

### 4.2 대량 데이터 처리 팁
*   `time.sleep()`을 사용하여 API 요청 속도를 조절(Rate Limiting)하십시오.
*   변환 실패(None)한 건은 별도 파일로 저장하여 수동 확인하거나 정제 규칙을 개선하십시오.

### 4.3 사전 테스트 로직 (Pre-run Validation)
대량의 데이터를 처리하기 전, 시스템 설정과 API 유효성을 검토하기 위해 상위 3개 정도의 샘플을 테스트하는 단계를 반드시 포함하십시오.

```python
def validate_geocoding_setup(df, sample_size=3):
    """
    본격적인 실행 전 샘플 데이터를 통해 API 호출 유효성을 검증합니다.
    """
    print(f"--- Pre-run Validation: Testing {sample_size} samples ---")
    samples = df.head(sample_size)
    success_count = 0
    
    for idx, row in samples.iterrows():
        lat, lon = geocode_address(row['geo_address'])
        if lat and lon:
            success_count += 1
            print(f"Success: {row['geo_address']} -> ({lat}, {lon})")
        else:
            print(f"Fail: {row['geo_address']}")
            
    if success_count == 0:
        print("\n[ERROR] 사전 테스트 결과가 0건입니다. API 키 또는 네트워크 상태를 확인하십시오.")
        print("스크립트 실행을 중단합니다.")
        return False
        
    print(f"--- Validation Complete: {success_count}/{sample_size} success --- \n")
    return True
```

## 5. 좌표 변환 실패 시 대응 (Fallback Strategy)
1.  **지번 <-> 도로명 교차 검색**: 도로명으로 실패 시 지번 주소로 재시도.
2.  **범위 축소**: 상세 주소(번지)를 제외하고 '동/읍/면' 단위로 검색하여 대략적인 위치라도 확보 (시각화 목적 시).

## 6. 시각화 연계 권장 사항
*   **라이브러리**: `folium`, `plotly.express` (Mapbox)
*   **데이터 포맷**: 위/경도 데이터는 `float` 형이어야 합니다.

## 7. 버전 관리 (Revision History)
문서 수정 시 아래 내역을 반드시 기입해 주십시오.

| **V1.0.2** | 2026-01-25 | AI Assistant | 사전 테스트 로직(Pre-run Validation) 섹션 추가 |
| **V1.0.1** | 2026-01-25 | AI Assistant | 오타 수정 및 에러 핸들링 로직 강화 |
| **V1.0.0** | 2026-01-24 | Initial | 가이드라인 문서 최초 작성 (전처리, Kakao API) |
| | | | |
| | | | |

---
*Memo: 본 가이드라인은 팀 내 공유 및 교육 목적으로 사용됩니다.*
