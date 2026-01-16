"""
HTML을 PDF로 변환하는 스크립트 (pdfkit 사용)
================================================================================
작성일: 2026-01-16
목적: EDA 리포트 HTML 파일을 PDF로 변환
입력: eda_report_20260116_011000.html
출력: eda_report_20260116_011000.pdf
================================================================================
"""

import pdfkit
from pathlib import Path

# ============================================================================
# 설정
# ============================================================================

# 입력 파일
SCRIPT_DIR = Path(__file__).parent
REPORT_DIR = SCRIPT_DIR.parent / "reports"
INPUT_HTML = REPORT_DIR / "eda_report_20260116_011000.html"

# 출력 파일
OUTPUT_PDF = REPORT_DIR / "eda_report_20260116_011000.pdf"

# pdfkit 옵션
OPTIONS = {
    'page-size': 'A4',
    'margin-top': '20mm',
    'margin-right': '20mm',
    'margin-bottom': '20mm',
    'margin-left': '20mm',
    'encoding': 'UTF-8',
    'enable-local-file-access': None,  # 로컬 파일 접근 허용
    'print-media-type': None,  # 인쇄 미디어 타입 사용
}

# ============================================================================
# 메인 실행
# ============================================================================

def main():
    print("=" * 80)
    print("EDA 리포트 PDF 변환 (pdfkit)")
    print("=" * 80)
    print()
    
    # 1. HTML 파일 확인
    print(f"[1] HTML 파일 확인: {INPUT_HTML.name}")
    if not INPUT_HTML.exists():
        print(f"  [ERROR] HTML 파일을 찾을 수 없습니다: {INPUT_HTML}")
        return
    print(f"  [OK] 파일 크기: {INPUT_HTML.stat().st_size / 1024:.1f} KB")
    print()
    
    # 2. PDF 변환
    print("[2] PDF 변환 중...")
    try:
        pdfkit.from_file(str(INPUT_HTML), str(OUTPUT_PDF), options=OPTIONS)
        print(f"  [OK] PDF 생성 완료: {OUTPUT_PDF}")
        print(f"  [OK] 파일 크기: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")
    except OSError as e:
        if 'wkhtmltopdf' in str(e):
            print(f"  [ERROR] wkhtmltopdf가 설치되지 않았습니다.")
            print()
            print("해결 방법:")
            print("1. wkhtmltopdf 다운로드: https://wkhtmltopdf.org/downloads.html")
            print("2. Windows 버전 설치")
            print("3. 환경 변수 PATH에 wkhtmltopdf 경로 추가")
            print()
            print("또는 HTML 파일을 브라우저에서 직접 PDF로 저장:")
            print(f"1. {INPUT_HTML} 파일을 브라우저로 열기")
            print("2. Ctrl+P 누르기")
            print("3. '대상'에서 'PDF로 저장' 선택")
            print("4. 저장 버튼 클릭")
            return
        else:
            print(f"  [ERROR] PDF 생성 실패: {e}")
            return
    except Exception as e:
        print(f"  [ERROR] 예상치 못한 오류: {e}")
        return
    
    print()
    print("=" * 80)
    print("PDF 변환 완료")
    print("=" * 80)
    print(f"출력 파일: {OUTPUT_PDF}")
    print()

if __name__ == "__main__":
    main()
