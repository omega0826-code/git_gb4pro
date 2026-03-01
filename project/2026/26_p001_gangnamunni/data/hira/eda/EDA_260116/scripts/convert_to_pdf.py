"""
마크다운 리포트를 PDF로 변환하는 스크립트
================================================================================
작성일: 2026-01-16
목적: EDA 리포트 마크다운 파일을 시각화 이미지를 포함한 PDF로 변환
입력: eda_report_20260116_011000.md
출력: eda_report_20260116_011000.pdf
================================================================================
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import re

# ============================================================================
# 설정
# ============================================================================

# 입력 파일
SCRIPT_DIR = Path(__file__).parent
REPORT_DIR = SCRIPT_DIR.parent / "reports"
INPUT_MD = REPORT_DIR / "eda_report_20260116_011000.md"

# 출력 파일
OUTPUT_PDF = REPORT_DIR / "eda_report_20260116_011000.pdf"

# 시각화 폴더
VIZ_DIR = SCRIPT_DIR.parent / "visualizations"

# ============================================================================
# 마크다운 전처리
# ============================================================================

def preprocess_markdown(md_content, viz_dir):
    """
    마크다운 내용 전처리
    - 이미지 경로를 절대 경로로 변환
    - file:/// 프로토콜 제거
    """
    # file:/// 경로를 실제 파일 경로로 변환
    def replace_image_path(match):
        full_path = match.group(2)
        # file:/// 제거
        if full_path.startswith('file:///'):
            full_path = full_path.replace('file:///', '')
            # URL 인코딩 디코딩
            from urllib.parse import unquote
            full_path = unquote(full_path)
        
        # 경로가 존재하는지 확인
        if Path(full_path).exists():
            # 절대 경로로 변환 (Windows 경로)
            abs_path = Path(full_path).absolute().as_posix()
            return f'![{match.group(1)}]({abs_path})'
        else:
            # 파일명만 추출하여 visualizations 폴더에서 찾기
            filename = Path(full_path).name
            viz_path = viz_dir / filename
            if viz_path.exists():
                abs_path = viz_path.absolute().as_posix()
                return f'![{match.group(1)}]({abs_path})'
        
        return match.group(0)
    
    # 이미지 경로 패턴 매칭 및 변환
    md_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image_path, md_content)
    
    return md_content

# ============================================================================
# HTML 생성
# ============================================================================

def markdown_to_html(md_content):
    """
    마크다운을 HTML로 변환
    """
    # 마크다운 확장 기능 활성화
    extensions = [
        'markdown.extensions.tables',      # 테이블 지원
        'markdown.extensions.fenced_code', # 코드 블록 지원
        'markdown.extensions.nl2br',       # 줄바꿈 지원
    ]
    
    html_content = markdown.markdown(md_content, extensions=extensions)
    
    # HTML 템플릿
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>의료기관 데이터 EDA 리포트</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    return html_template

# ============================================================================
# CSS 스타일
# ============================================================================

CSS_STYLE = """
@page {
    size: A4;
    margin: 2cm;
}

body {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    margin-top: 30px;
    font-size: 24pt;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    color: #34495e;
    border-bottom: 2px solid #95a5a6;
    padding-bottom: 8px;
    margin-top: 25px;
    font-size: 18pt;
}

h3 {
    color: #555;
    margin-top: 20px;
    font-size: 14pt;
}

h4 {
    color: #666;
    margin-top: 15px;
    font-size: 12pt;
}

p {
    margin: 10px 0;
    text-align: justify;
}

strong {
    color: #2c3e50;
    font-weight: bold;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 10pt;
}

table th {
    background-color: #3498db;
    color: white;
    padding: 10px;
    text-align: left;
    font-weight: bold;
}

table td {
    border: 1px solid #ddd;
    padding: 8px;
}

table tr:nth-child(even) {
    background-color: #f9f9f9;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    page-break-inside: avoid;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 9pt;
}

pre {
    background-color: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 9pt;
}

blockquote {
    border-left: 4px solid #3498db;
    padding-left: 15px;
    margin: 15px 0;
    color: #555;
    background-color: #f0f8ff;
    padding: 10px 15px;
}

ul, ol {
    margin: 10px 0;
    padding-left: 30px;
}

li {
    margin: 5px 0;
}

hr {
    border: none;
    border-top: 2px solid #ddd;
    margin: 30px 0;
}

/* 페이지 브레이크 제어 */
.page-break {
    page-break-after: always;
}

/* 이미지 캡션 스타일 */
img + em {
    display: block;
    text-align: center;
    font-style: italic;
    color: #666;
    margin-top: -15px;
    margin-bottom: 20px;
}
"""

# ============================================================================
# 메인 실행
# ============================================================================

def main():
    print("=" * 80)
    print("EDA 리포트 PDF 변환")
    print("=" * 80)
    print()
    
    # 1. 마크다운 파일 읽기
    print(f"[1] 마크다운 파일 읽기: {INPUT_MD.name}")
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        md_content = f.read()
    print(f"  [OK] 파일 크기: {len(md_content):,} bytes")
    print()
    
    # 2. 마크다운 전처리
    print("[2] 마크다운 전처리 (이미지 경로 변환)")
    md_content = preprocess_markdown(md_content, VIZ_DIR)
    print("  [OK] 전처리 완료")
    print()
    
    # 3. HTML 변환
    print("[3] HTML 변환")
    html_content = markdown_to_html(md_content)
    print("  [OK] HTML 생성 완료")
    print()
    
    # 4. PDF 생성
    print("[4] PDF 생성")
    try:
        HTML(string=html_content).write_pdf(
            OUTPUT_PDF,
            stylesheets=[CSS(string=CSS_STYLE)]
        )
        print(f"  [OK] PDF 생성 완료: {OUTPUT_PDF}")
        print(f"  [OK] 파일 크기: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"  [ERROR] PDF 생성 실패: {e}")
        return
    
    print()
    print("=" * 80)
    print("PDF 변환 완료")
    print("=" * 80)
    print(f"출력 파일: {OUTPUT_PDF}")
    print()

if __name__ == "__main__":
    main()
