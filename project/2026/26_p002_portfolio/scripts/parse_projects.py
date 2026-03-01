"""
포트폴리오 프로젝트 — HWPX 프로젝트 현황 파싱 스크립트.

범용 hwpx_table_parser 모듈을 사용하여:
1. Project Progress Status HWPX 파일 파싱
2. 특정 담당자 이름으로 필터링
3. CSV 저장 + 리포트 생성

Usage:
    python parse_projects.py
    python parse_projects.py --name "홍길동"
    python parse_projects.py --name "홍길동" --col 5
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

# 범용 모듈 import를 위한 경로 추가
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # git_gb4pro/
sys.path.insert(0, str(PROJECT_ROOT))

from automation.hwp.hwpx_table_parser import HwpxTableParser, generate_report

# ============================================================================
# 프로젝트 상수
# ============================================================================
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_DIR / "data" / "raw"
DATA_PROCESSED = PROJECT_DIR / "data" / "processed"
REPORTS_DIR = PROJECT_DIR / "reports"

DEFAULT_HWPX = DATA_RAW / "Project Progress Status_260224_v1.hwpx"
DEFAULT_FILTER_NAME = "여정욱"
DEFAULT_FILTER_COL = 8  # 담당자 컬럼 (0-based)


def main():
    """메인 실행 함수."""
    ap = argparse.ArgumentParser(
        description='프로젝트 현황 HWPX에서 담당자별 프로젝트를 추출합니다.')
    ap.add_argument('--input', type=str, default=str(DEFAULT_HWPX),
                    help=f'HWPX 파일 경로 (기본: {DEFAULT_HWPX.name})')
    ap.add_argument('--name', type=str, default=DEFAULT_FILTER_NAME,
                    help=f'필터링할 담당자 이름 (기본: {DEFAULT_FILTER_NAME})')
    ap.add_argument('--col', type=int, default=DEFAULT_FILTER_COL,
                    help=f'담당자 컬럼 인덱스 (기본: {DEFAULT_FILTER_COL})')
    args = ap.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 파싱
    print(f"파싱 시작: {Path(args.input).name}")
    parser = HwpxTableParser(args.input)
    tables = parser.parse_all_tables()
    print(parser.summary())

    # 2. 모든 테이블에서 필터링 후 합산
    total_rows = sum(t.row_count for t in tables)
    filtered_tables = [t.filter(args.name, column=args.col) for t in tables]

    # 합산
    merged_headers = filtered_tables[0].headers if filtered_tables else []
    merged_rows = []
    for t in filtered_tables:
        merged_rows.extend(t.rows)

    from automation.hwp.hwpx_table_parser import Table
    merged = Table.__new__(Table)
    merged.headers = merged_headers
    merged.rows = merged_rows

    print(f"\n전체 {total_rows}건 → '{args.name}' 포함 {merged.row_count}건")

    # 3. CSV 저장
    csv_path = DATA_PROCESSED / f"projects_{args.name}_{timestamp}.csv"
    merged.to_csv(str(csv_path))
    print(f"CSV: {csv_path}")

    # 4. 리포트 생성
    report_path = REPORTS_DIR / f"report_projects_{args.name}_{timestamp}.md"
    generate_report(parser, merged, args.name, args.col,
                    total_rows, str(csv_path), str(report_path))
    print(f"리포트: {report_path}")


if __name__ == "__main__":
    main()
