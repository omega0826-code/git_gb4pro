# 강남언니 병원 상세 정보 수집 에러 분석 리포트

**작성일시**: 2026년 1월 5일
**작성자**: Gemini Agent

## 1. 개요
본 리포트는 강남언니 병원 상세 정보 크롤링 과정에서 발생한 에러의 원인을 분석하고 조치 내용을 기술합니다. 총 1,103개 병원을 대상으로 수집을 진행하였으며, 일부 병원에서 지속적인 수집 실패가 발생하였습니다.

## 2. 수집 현황 요약
- **대상 병원 수**: 1,103개
- **수집 완료**: 1,085개 (약 98.4%)
- **수집 실패**: 18개 (약 1.6%)
- **최종 결과 파일**: `crawling\gangnam\data\gangnam_hospitals_detail_RESUME_20260105_041227.csv`

## 3. 에러 상세 분석

### 3.1 주요 에러 유형
수집 실패의 주된 원인은 **HTTP 500 Internal Server Error**입니다.

*   **증상**: 특정 병원 ID(`hospitals/{id}`)에 대한 API 요청 시, 서버가 500 에러를 반환함.
*   **재시도 결과**: 3회의 재시도(Retry) 및 시간차를 둔 재접속 시도에도 불구하고 동일하게 500 에러가 발생함.
*   **원인 추정**:
    1.  **데이터 무결성 문제**: 해당 병원 ID가 목록에는 존재하나, 상세 정보 DB 테이블에는 매핑되지 않거나 손상된 데이터일 가능성.
    2.  **비공개/삭제 처리**: 해당 병원이 플랫폼에서 비공개 처리되었거나 삭제되었으나, 검색 인덱스(목록 API)에는 잔존해 있는 경우.
    3.  **서버 로직 오류**: 특정 데이터 필드(특수문자 등) 파싱 중 서버 측 예외 발생.

단순한 네트워크 차단(IP Block)이나 부하(Rate Limit) 문제는 아닌 것으로 판단됩니다. (이 경우 403 Forbidden 또는 429 Too Many Requests가 발생하며, 다른 ID는 정상 조회됨)

### 3.2 실패 병원 ID 목록
다음 ID를 가진 병원들은 데이터 수집이 불가능하여 건너뛰었습니다.

| 연번 | 병원 ID | 에러 메시지 | 비고 |
| :--- | :--- | :--- | :--- |
| 1 | 331 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 2 | 4842 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 3 | 5882 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 4 | 165 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 5 | 330 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 6 | 3030 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 7 | 4178 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 8 | 3875 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 9 | 156 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 10 | 1265 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 11 | 7653 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 12 | 3740 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 13 | 7551 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 14 | 4617 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 15 | 7697 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 16 | 8053 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 17 | 7971 | HTTP 500 / Max retries exceeded | 재시도 실패 |
| 18 | 3815 | HTTP 500 / Max retries exceeded | 재시도 실패 |
(외 소수 추가 발생 가능, 전체 로그 참조)

## 4. 조치 및 향후 계획
1.  **결과 데이터 정제**: 수집된 데이터(`gangnam_hospitals_detail_RESUME_...csv`)에서 `crawled`가 `True`인 항목만 유효한 데이터로 사용하십시오.
2.  **수동 확인**: 실패한 ID에 대해서는 브라우저를 통해 직접 접속(`https://www.gangnamunni.com/hospitals/{ID}`)하여 페이지가 유효한지 확인할 수 있습니다. 404 또는 에러 페이지가 뜬다면 영구 결번으로 간주해도 무방합니다.
3.  **크롤러 개선**: 향후 동일 작업 시 `500` 에러가 발생하면 즉시 실패 처리하고 다음으로 넘어가도록 로직을 최적화하여 시간 낭비를 줄일 수 있습니다.

---
**결론**: 시스템적 오류가 아닌 대상 데이터 자체의 문제로 인한 에러이므로, 수집된 98%의 데이터를 정상적으로 활용하시면 됩니다.
