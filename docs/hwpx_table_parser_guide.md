# HWPX 테이블 파서 사용 가이드

**위치**: `automation/hwp/hwpx_table_parser.py`
**의존성**: `lxml` (pip install lxml)

## CLI 사용법

```bash
# 테이블 구조 확인
python automation/hwp/hwpx_table_parser.py input.hwpx --info

# 전체 데이터 CSV 추출
python automation/hwp/hwpx_table_parser.py input.hwpx -o output.csv

# 필터링 (전체 행 검색)
python automation/hwp/hwpx_table_parser.py input.hwpx -o output.csv -f "검색어"

# 필터링 (특정 컬럼만)
python automation/hwp/hwpx_table_parser.py input.hwpx -o output.csv -f "검색어" -c 8

# 리포트 생성
python automation/hwp/hwpx_table_parser.py input.hwpx -o output.csv -f "검색어" --report
```

## Python API 사용법

```python
from automation.hwp.hwpx_table_parser import HwpxTableParser

parser = HwpxTableParser("document.hwpx")
tables = parser.parse_all_tables()

# 테이블 정보 확인
print(parser.summary())

# 필터링
result = tables[0].filter("여정욱", column=8)

# 내보내기
result.to_csv("output.csv")
df = result.to_dataframe()  # pandas DataFrame
print(result.to_markdown())  # 마크다운 테이블
```

## 기능

- **셀 병합 처리**: rowSpan/colSpan 자동 정규화
- **다중 테이블 지원**: section0.xml 내 모든 테이블 파싱
- **인코딩 표준화**: Windows cp949 충돌 방지 (UTF-8)
- **다양한 출력**: CSV, DataFrame, Markdown
