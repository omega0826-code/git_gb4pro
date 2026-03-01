"""
HWPX 테이블 파서 — 범용 모듈

HWPX(ZIP 기반 OWPML) 파일에서 테이블 데이터를 추출하는 범용 파서.
CLI 및 Python API로 사용 가능.

Usage (CLI):
    python hwpx_table_parser.py input.hwpx --info
    python hwpx_table_parser.py input.hwpx -o output.csv
    python hwpx_table_parser.py input.hwpx -o output.csv -f "여정욱" -c 8
    python hwpx_table_parser.py input.hwpx -o output.csv -f "여정욱" --report

Usage (Python API):
    from automation.hwp.hwpx_table_parser import HwpxTableParser
    parser = HwpxTableParser("document.hwpx")
    tables = parser.parse_all_tables()
    filtered = tables[0].filter("여정욱", column=8)
    filtered.to_csv("output.csv")
"""
import argparse
import csv
import io
import os
import platform
import sys
import textwrap
import zipfile
from copy import deepcopy
from datetime import datetime
from typing import List, Optional, Tuple

from lxml import etree

# ============================================================================
# Windows 콘솔 UTF-8 인코딩 설정
# ============================================================================
if platform.system() == 'Windows':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ============================================================================
# 상수
# ============================================================================
HP_NS = '{http://www.hancom.co.kr/hwpml/2011/paragraph}'
HS_NS = '{http://www.hancom.co.kr/hwpml/2011/section}'

TAG_TBL = f'{HP_NS}tbl'
TAG_TR = f'{HP_NS}tr'
TAG_TC = f'{HP_NS}tc'
TAG_T = f'{HP_NS}t'
TAG_CELL_SPAN = f'{HP_NS}cellSpan'
TAG_CELL_ADDR = f'{HP_NS}cellAddr'


# ============================================================================
# 데이터 클래스
# ============================================================================
class CellData:
    """파싱된 셀 데이터.

    Attributes:
        text: 셀 텍스트
        col_span: 열 병합 수 (기본 1)
        row_span: 행 병합 수 (기본 1)
        col_addr: 열 주소
        row_addr: 행 주소
    """

    def __init__(self, text: str = '', col_span: int = 1, row_span: int = 1,
                 col_addr: int = 0, row_addr: int = 0):
        self.text = text
        self.col_span = col_span
        self.row_span = row_span
        self.col_addr = col_addr
        self.row_addr = row_addr


class Table:
    """파싱된 테이블 데이터.

    Attributes:
        headers: 헤더 행 (첫 행에서 자동 분리)
        rows: 데이터 행 목록
        row_count: 데이터 행 수
        col_count: 열 수
    """

    def __init__(self, raw_rows: List[List[str]],
                 auto_detect_header: bool = True):
        """테이블 초기화.

        Args:
            raw_rows: 원시 행 데이터
            auto_detect_header: True이면 첫 행을 헤더로 분리
        """
        if not raw_rows:
            self.headers = []
            self.rows = []
        elif auto_detect_header and len(raw_rows) > 1:
            self.headers = raw_rows[0]
            self.rows = raw_rows[1:]
        else:
            self.headers = []
            self.rows = raw_rows

    @property
    def row_count(self) -> int:
        """데이터 행 수."""
        return len(self.rows)

    @property
    def col_count(self) -> int:
        """열 수."""
        if self.headers:
            return len(self.headers)
        if self.rows:
            return max(len(r) for r in self.rows)
        return 0

    def filter(self, value: str, column: int = None) -> 'Table':
        """특정 값이 포함된 행만 필터링한 새 Table 반환.

        Args:
            value: 검색할 문자열
            column: 검색할 컬럼 인덱스 (None이면 전체 행 검색)

        Returns:
            필터링된 새 Table 객체
        """
        filtered = []
        for row in self.rows:
            if column is not None:
                if column < len(row) and value in row[column]:
                    filtered.append(row)
            else:
                row_text = ' '.join(row)
                if value in row_text:
                    filtered.append(row)

        result = Table.__new__(Table)
        result.headers = list(self.headers) if self.headers else []
        result.rows = filtered
        return result

    def to_csv(self, path: str, encoding: str = 'utf-8-sig') -> None:
        """CSV 파일로 저장.

        Args:
            path: 출력 파일 경로
            encoding: 인코딩 (기본 utf-8-sig, Excel 한글 호환)
        """
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', newline='', encoding=encoding) as f:
            writer = csv.writer(f)
            if self.headers:
                writer.writerow(self.headers)
            for row in self.rows:
                writer.writerow(row)

    def to_dataframe(self):
        """pandas DataFrame으로 변환.

        Returns:
            pd.DataFrame
        
        Raises:
            ImportError: pandas 미설치 시
        """
        import pandas as pd
        if self.headers:
            return pd.DataFrame(self.rows, columns=self.headers)
        return pd.DataFrame(self.rows)

    def to_markdown(self) -> str:
        """마크다운 테이블 문자열로 변환.

        Returns:
            마크다운 형식의 테이블 문자열
        """
        if not self.rows and not self.headers:
            return '(빈 테이블)'

        lines = []
        col_count = self.col_count

        if self.headers:
            h = [c.replace('|', '\\|') for c in self.headers]
            lines.append('| ' + ' | '.join(h) + ' |')
            lines.append('|' + '|'.join(['---'] * col_count) + '|')

        for row in self.rows:
            cells = [c.replace('|', '\\|') for c in row]
            # 열 수 맞추기
            while len(cells) < col_count:
                cells.append('')
            lines.append('| ' + ' | '.join(cells[:col_count]) + ' |')

        return '\n'.join(lines)

    def __repr__(self) -> str:
        header_preview = ', '.join(self.headers[:3]) if self.headers else '없음'
        return f"Table({self.row_count}행 x {self.col_count}열, 헤더=[{header_preview}, ...])"


# ============================================================================
# 메인 파서
# ============================================================================
class HwpxTableParser:
    """HWPX 파일에서 테이블 데이터를 추출하는 범용 파서.

    Args:
        hwpx_path: HWPX 파일 경로

    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        zipfile.BadZipFile: 유효하지 않은 ZIP 파일일 때
    """

    def __init__(self, hwpx_path: str):
        if not os.path.exists(hwpx_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {hwpx_path}")

        self.hwpx_path = hwpx_path
        self._tables: Optional[List[Table]] = None

    def parse_all_tables(self) -> List[Table]:
        """파일 내 모든 테이블을 파싱하여 반환.

        Returns:
            Table 객체 목록
        """
        if self._tables is not None:
            return self._tables

        raw_tables = []

        with zipfile.ZipFile(self.hwpx_path, 'r') as z:
            section_files = sorted([
                n for n in z.namelist()
                if 'section' in n.lower() and n.endswith('.xml')
            ])

            for sf in section_files:
                content = z.read(sf)
                root = etree.fromstring(content)

                for tbl_elem in root.iter(TAG_TBL):
                    raw_rows = self._parse_table_element(tbl_elem)
                    if raw_rows:
                        # 셀 병합 처리
                        normalized = self._normalize_spans(raw_rows)
                        text_rows = [[cell.text for cell in row] for row in normalized]
                        raw_tables.append(Table(text_rows))

        self._tables = raw_tables
        return self._tables

    def get_table(self, index: int) -> Table:
        """특정 인덱스의 테이블 반환.

        Args:
            index: 테이블 인덱스 (0-based)

        Returns:
            Table 객체

        Raises:
            IndexError: 인덱스 범위 초과
        """
        tables = self.parse_all_tables()
        if index < 0 or index >= len(tables):
            raise IndexError(
                f"테이블 인덱스 {index}이 범위를 벗어났습니다. "
                f"(전체 {len(tables)}개)"
            )
        return tables[index]

    def summary(self) -> str:
        """모든 테이블의 요약 정보 반환.

        Returns:
            요약 문자열
        """
        tables = self.parse_all_tables()
        lines = [f"파일: {os.path.basename(self.hwpx_path)}",
                 f"테이블 수: {len(tables)}개", ""]
        for i, table in enumerate(tables):
            header_str = ', '.join(table.headers[:4]) if table.headers else '없음'
            lines.append(
                f"  테이블 {i}: {table.row_count}행 x {table.col_count}열 "
                f"(헤더: {header_str}...)"
            )
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # 내부 메서드
    # ------------------------------------------------------------------
    def _extract_cell_text(self, cell_elem) -> str:
        """셀 엘리먼트에서 텍스트 추출.

        Args:
            cell_elem: lxml Element (hp:tc)

        Returns:
            셀 내 모든 텍스트를 공백으로 연결한 문자열
        """
        texts = []
        for elem in cell_elem.iter():
            if elem.tag == TAG_T and elem.text:
                texts.append(elem.text.strip())
        return ' '.join(texts).strip()

    def _parse_cell_span(self, cell_elem) -> Tuple[int, int]:
        """셀의 rowSpan, colSpan 속성 파싱.

        Args:
            cell_elem: lxml Element (hp:tc)

        Returns:
            (colSpan, rowSpan) 튜플
        """
        span_elem = cell_elem.find(TAG_CELL_SPAN)
        if span_elem is not None:
            col_span = int(span_elem.get('colSpan', '1'))
            row_span = int(span_elem.get('rowSpan', '1'))
            return col_span, row_span
        return 1, 1

    def _parse_cell_addr(self, cell_elem) -> Tuple[int, int]:
        """셀의 행/열 주소 파싱.

        Args:
            cell_elem: lxml Element (hp:tc)

        Returns:
            (colAddr, rowAddr) 튜플
        """
        addr_elem = cell_elem.find(TAG_CELL_ADDR)
        if addr_elem is not None:
            col_addr = int(addr_elem.get('colAddr', '0'))
            row_addr = int(addr_elem.get('rowAddr', '0'))
            return col_addr, row_addr
        return 0, 0

    def _parse_table_element(self, tbl_elem) -> List[List[CellData]]:
        """테이블 엘리먼트를 CellData 2D 리스트로 파싱.

        Args:
            tbl_elem: lxml Element (hp:tbl)

        Returns:
            CellData의 2D 리스트
        """
        rows = []
        for tr_elem in tbl_elem.iter(TAG_TR):
            row = []
            for tc_elem in tr_elem.findall(TAG_TC):
                text = self._extract_cell_text(tc_elem)
                col_span, row_span = self._parse_cell_span(tc_elem)
                col_addr, row_addr = self._parse_cell_addr(tc_elem)
                row.append(CellData(
                    text=text,
                    col_span=col_span,
                    row_span=row_span,
                    col_addr=col_addr,
                    row_addr=row_addr,
                ))
            if row:
                rows.append(row)
        return rows

    def _normalize_spans(self, raw_rows: List[List[CellData]]) -> List[List[CellData]]:
        """셀 병합(rowSpan/colSpan)을 처리하여 정규화된 2D 배열 반환.

        colSpan > 1: 오른쪽으로 동일 텍스트 복제
        rowSpan > 1: 아래 행에 동일 텍스트 전파

        Args:
            raw_rows: CellData의 2D 리스트

        Returns:
            정규화된 CellData의 2D 리스트
        """
        if not raw_rows:
            return raw_rows

        # 최대 열 수 계산 (colSpan 포함)
        max_cols = 0
        for row in raw_rows:
            total = sum(cell.col_span for cell in row)
            max_cols = max(max_cols, total)

        num_rows = len(raw_rows)

        # 정규화된 그리드 생성 (None으로 초기화)
        grid: List[List[Optional[CellData]]] = [
            [None] * max_cols for _ in range(num_rows)
        ]

        for r_idx, row in enumerate(raw_rows):
            c_idx = 0
            for cell in row:
                # 이미 채워진 셀(rowSpan으로 전파된) 건너뛰기
                while c_idx < max_cols and grid[r_idx][c_idx] is not None:
                    c_idx += 1
                if c_idx >= max_cols:
                    break

                # colSpan/rowSpan 처리
                for dr in range(cell.row_span):
                    for dc in range(cell.col_span):
                        target_r = r_idx + dr
                        target_c = c_idx + dc
                        if target_r < num_rows and target_c < max_cols:
                            grid[target_r][target_c] = CellData(
                                text=cell.text,
                                col_span=1,
                                row_span=1,
                                col_addr=target_c,
                                row_addr=target_r,
                            )
                c_idx += cell.col_span

        # None 셀을 빈 CellData로 채우기
        for r_idx in range(num_rows):
            for c_idx in range(max_cols):
                if grid[r_idx][c_idx] is None:
                    grid[r_idx][c_idx] = CellData(text='')

        return grid


# ============================================================================
# 리포트 생성
# ============================================================================
def generate_report(parser: HwpxTableParser, table: Table,
                    filter_value: str, filter_col: Optional[int],
                    total_count: int, csv_path: str,
                    report_path: str) -> None:
    """마크다운 리포트 생성.

    Args:
        parser: HwpxTableParser 인스턴스
        table: 필터링된 Table
        filter_value: 필터 조건
        filter_col: 필터 컬럼 (None이면 전체)
        total_count: 전체 행 수
        csv_path: CSV 출력 경로
        report_path: 리포트 출력 경로
    """
    col_info = f"컬럼 {filter_col}" if filter_col is not None else "전체"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report = f"""# HWPX 테이블 파싱 결과 리포트

**생성일시**: {timestamp}
**원본 파일**: `{os.path.basename(parser.hwpx_path)}`
**필터 조건**: `{filter_value}` ({col_info})

---

## 파싱 결과 요약

{parser.summary()}

## 필터링 결과

| 항목 | 값 |
|------|-----|
| 전체 행 수 | {total_count}개 |
| 필터링 결과 | {table.row_count}개 |
| 출력 파일 | `{os.path.basename(csv_path)}` |

## 데이터

{table.to_markdown()}
"""
    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)


# ============================================================================
# CLI
# ============================================================================
def main():
    """커맨드라인 인터페이스."""
    ap = argparse.ArgumentParser(
        description='HWPX 파일에서 테이블 데이터를 추출합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        사용 예시:
          # 테이블 구조 확인
          python hwpx_table_parser.py input.hwpx --info

          # 모든 데이터를 CSV로 추출
          python hwpx_table_parser.py input.hwpx -o output.csv

          # 특정 이름 필터링 (전체 행 검색)
          python hwpx_table_parser.py input.hwpx -o output.csv -f "여정욱"

          # 특정 컬럼에서만 검색 (담당자 컬럼 = 8)
          python hwpx_table_parser.py input.hwpx -o output.csv -f "여정욱" -c 8

          # 리포트 생성
          python hwpx_table_parser.py input.hwpx -o output.csv -f "여정욱" --report
        """))

    ap.add_argument('input', help='HWPX 파일 경로')
    ap.add_argument('-o', '--output', help='출력 CSV 파일 경로')
    ap.add_argument('-f', '--filter', help='필터링할 텍스트')
    ap.add_argument('-c', '--filter-col', type=int, default=None,
                    help='필터링할 컬럼 인덱스 (0-based)')
    ap.add_argument('-t', '--table-index', type=int, default=None,
                    help='추출할 테이블 인덱스 (0-based, 생략 시 전체)')
    ap.add_argument('--info', action='store_true',
                    help='테이블 구조 정보만 출력')
    ap.add_argument('--report', action='store_true',
                    help='마크다운 리포트 함께 생성')
    ap.add_argument('--encoding', default='utf-8-sig',
                    help='출력 CSV 인코딩 (기본: utf-8-sig)')

    args = ap.parse_args()

    # 파싱
    parser = HwpxTableParser(args.input)
    tables = parser.parse_all_tables()

    # --info 모드
    if args.info:
        print(parser.summary())
        return

    # 테이블 선택
    if args.table_index is not None:
        selected = [parser.get_table(args.table_index)]
    else:
        selected = tables

    # 필터링 및 합산
    total_rows = sum(t.row_count for t in selected)
    if args.filter:
        filtered_tables = [t.filter(args.filter, args.filter_col) for t in selected]
    else:
        filtered_tables = selected

    # 합산 Table 생성
    if filtered_tables:
        merged_headers = filtered_tables[0].headers
        merged_rows = []
        for t in filtered_tables:
            merged_rows.extend(t.rows)

        merged = Table.__new__(Table)
        merged.headers = merged_headers
        merged.rows = merged_rows
    else:
        merged = Table([])

    # 결과 출력
    filter_info = f" (필터: '{args.filter}'" + \
                  (f", 컬럼 {args.filter_col}" if args.filter_col is not None else "") + \
                  ")" if args.filter else ""
    print(f"전체: {total_rows}건 → 결과: {merged.row_count}건{filter_info}")

    # CSV 저장
    if args.output:
        merged.to_csv(args.output, encoding=args.encoding)
        print(f"CSV 저장: {args.output}")

        # 리포트 생성
        if args.report:
            report_path = args.output.rsplit('.', 1)[0] + '_report.md'
            generate_report(parser, merged, args.filter or '없음',
                            args.filter_col, total_rows,
                            args.output, report_path)
            print(f"리포트 저장: {report_path}")
    else:
        # CSV 미지정 시 마크다운으로 출력
        print()
        print(merged.to_markdown())


if __name__ == '__main__':
    main()
