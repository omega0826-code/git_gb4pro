# HWP/HWPX 자동화 도구

한글(Hancom Office) 문서 관련 자동화 도구 모음입니다.

## 도구 목록

| 도구                 | 파일                   | 설명                                    |
| -------------------- | ---------------------- | --------------------------------------- |
| **HWPX 테이블 파서** | `hwpx_table_parser.py` | HWPX 파일에서 테이블 데이터 추출 (범용) |
| **교정 도구**        | `Proofreading/`        | 문서 맞춤법·문법 교정                   |
| **오타 검출**        | `Typo checker/`        | 오타 자동 검출                          |

## HWPX 테이블 파서

HWPX(ZIP 기반 OWPML) 파일에서 테이블 데이터를 추출하는 범용 파서.

### 의존성
```
lxml>=4.9.0
```

### CLI 사용법
```bash
# 테이블 구조 확인
python hwpx_table_parser.py input.hwpx --info

# CSV로 추출
python hwpx_table_parser.py input.hwpx -o output.csv

# 필터링 (특정 컬럼)
python hwpx_table_parser.py input.hwpx -o output.csv -f "검색어" -c 8

# 리포트 포함
python hwpx_table_parser.py input.hwpx -o output.csv -f "검색어" --report
```

### Python API
```python
from automation.hwp.hwpx_table_parser import HwpxTableParser

parser = HwpxTableParser("document.hwpx")
tables = parser.parse_all_tables()
result = tables[0].filter("여정욱", column=8)
result.to_csv("output.csv")
```

### 주요 기능
- 셀 병합(rowSpan/colSpan) 자동 정규화
- 다중 테이블·다중 section 지원
- Windows cp949 인코딩 충돌 방지
- CSV, DataFrame, Markdown 출력

상세 가이드: [`docs/hwpx_table_parser_guide.md`](../../docs/hwpx_table_parser_guide.md)

---

## 변경 이력

| 날짜       | 버전 | 변경 내용                                                                       |
| ---------- | ---- | ------------------------------------------------------------------------------- |
| 2026-03-01 | v1.0 | `hwpx_table_parser.py` 신규 생성 — 범용 HWPX 테이블 파서 (CLI + API, span 처리) |
| 2026-03-01 | v1.0 | `README.md` 신규 생성                                                           |
