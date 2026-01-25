# 병원 정보 지오코딩 수행 계획

본 문서는 `gis/geocoding/geocoding_guideline.md` 를 준수하여 `병원전체정보_20260116_212603.csv` 파일의 병원 주소를 지오코딩(위경도 변환)하기 위한 상세 계획입니다.

## 1. 개요
- **목적**: 병원 주소 데이터를 기반으로 위도(Latitude), 경도(Longitude) 좌표를 생성하여 공간 분석 및 시각화 데이터로 활용
- **대상 파일**: `crawling/openapi/getHospDetailList/data/병원전체정보_20260116_212603.csv`
- **사용 API**: Kakao Local API (주소 검색)

## 2. 작업 절차 (Workflow)

### 2.1 사전 준비
- [ ] **API 키 확인**: `.env` 파일 내 `KAKAO_API_KEY` 존재 여부 및 유효성 확인
- [ ] **라이브러리 확인**: `pandas`, `requests`, `python-dotenv` 설치 확인

### 2.2 디렉토리 및 파일 관리 (Directory & File Management) [NEW]
- **기본 경로 설정**: 스크립트 실행 위치 기준 상대 경로 사용
    - `data/input`: 분석 대상 원본 파일 위치
    - `data/output`: 지오코딩 완료 결과 파일 저장 위치
    - `logs`: 처리 로그 저장 위치
- **자동 생성**: 스크립트 실행 시 `output` 및 `logs` 폴더가 없으면 자동 생성 로직 포함
- **파일 이동/복사**: 
    - 원본 파일(`crawling/openapi/getHospDetailList/data/병원전체정보_20260116_212603.csv`)을 `gis/geocoding/hospital/data/input/`으로 복사하여 작업 수행 권장 (원본 보존)

### 2.3 데이터 로딩 및 분석
- **입력 데이터 로딩**: `data/input` 폴더 내 대상 파일 읽기
- **주소 컬럼 식별**: `원본_주소` 컬럼을 주요 처리 대상으로 설정
- **데이터 샘플링**: 상위 10건을 추출하여 주소 패턴 분석

### 2.4 주소 전처리 (Preprocessing)
가이드라인(`geocoding_guideline.md`)의 3.1항 규칙 적용:
1.  **괄호 제거**: 정규표현식 `r'\(.*?\)'` 사용하여 괄호 및 내부 내용 삭제
2.  **불필요 문자 제거**: 콤마(`,`) 제거 또는 공백 치환
3.  **층/호수 제거**: `지하`, `층`, `호` 등 상세 주소 정보 제거 (검색 정확도 향상 목적)
4.  **공백 정리**: 다중 공백을 단일 공백으로 치환

### 2.4 지오코딩 실행 (Geocoding)
- **함수 구현**: `geocode_address(address)` 함수 작성 (가이드라인 4.1 참고)
- **API 요청**: `https://dapi.kakao.com/v2/local/search/address.json` 엔드포인트 사용
- **반환값 처리**:
    - 성공: `lat` (y), `lon` (x) 반환
    - 실패: `None`, `None` 반환 및 에러 로그 기록
- **Rate Limiting**: `time.sleep()` 사용하여 API 호출 간격 불균형 방지 (선택 사항, 대량 처리 시 고려)

### 2.5 사전 테스트 및 실행 차단 (Pre-run Validation) [NEW]
- **테스트 호출**: 전체 루프 실행 전 상위 3개 행에 대해 지오코딩 시도
- **중단 조건**: 3개 샘플 모두 실패 시 `sys.exit()` 또는 `return False`를 통해 스크립트 실행 즉시 중단
- **메시지**: 실패 원인(API 키 오류, 네트워크 문제 등)을 콘솔에 명시적으로 출력

### 2.6 예외 처리 및 검증 (Fallback & Validation)
- **실패 건수 재처리**: 1차 변환 실패 시, 상세 주소(번지 등)를 제외하고 `동/읍/면` 단위로 2차 검색 시도 (선택 사항)
- **결과 검증**: 
    - 변환율(Hit Rate) 계산 (성공 건수 / 전체 건수)
    - 주요 병원 샘플링하여 좌표 정확성 수동 확인

### 2.7 결과 저장
- **저장 경로**: `data/output/`
- **저장 파일명**: `병원전체정보_20260116_212603_geocoded.csv` (Time stamp는 실행 시점 기준 적용 가능)
- **저장 포맷**: CSV (`utf-8-sig`)
- **포함 컬럼**: 원본 데이터 전량 + `lat` (위도), `lon` (경도), `geo_address` (전처리된 주소)

## 3. 실행 스크립트 (예정)
- 스크립트 경로: `gis/geocoding/hospital/run_hospital_geocoding.py` (신규 생성)
- 주요 기능:
    - **디렉토리 초기화 (Init Directories)**
    - 데이터 로드
    - 전처리 로직 적용
    - API 호출 및 좌표 매핑
    - 결과 저장 및 로그 출력

## 4. 검토 요청 사항
- 위 절차 중 추가적인 전처리 규칙이 필요한지 확인
- API 호출 제한(일일 쿼터)에 따른 분할 처리 필요 여부 확인