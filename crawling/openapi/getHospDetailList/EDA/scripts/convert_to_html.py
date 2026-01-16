"""
마크다운 리포트를 HTML로 변환하는 스크립트 (브라우저 PDF 인쇄용)
================================================================================
작성일: 2026-01-16
목적: EDA 리포트 마크다운 파일을 시각화 이미지를 포함한 HTML로 변환
      브라우저에서 Ctrl+P로 PDF 저장 가능
입력: eda_report_20260116_011000.md
출력: eda_report_20260116_011000.html
================================================================================
"""

import markdown
from pathlib import Path
import re
import base64

# ============================================================================
# 설정
# ============================================================================

# 입력 파일
SCRIPT_DIR = Path(__file__).parent
REPORT_DIR = SCRIPT_DIR.parent / "reports"
INPUT_MD = REPORT_DIR / "eda_report_20260116_011000.md"

# 출력 파일
OUTPUT_HTML = REPORT_DIR / "eda_report_20260116_011000.html"

# 시각화 폴더
VIZ_DIR = SCRIPT_DIR.parent / "visualizations"

# ============================================================================
# 이미지를 Base64로 인코딩
# ============================================================================

def image_to_base64(image_path):
    """
    이미지 파일을 Base64 문자열로 변환
    """
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        # 파일 확장자로 MIME 타입 결정
        ext = Path(image_path).suffix.lower()
        mime_type = 'image/png' if ext == '.png' else 'image/jpeg'
        return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"  [WARNING] 이미지 변환 실패: {image_path} - {e}")
        return None

# ============================================================================
# 마크다운 전처리
# ============================================================================

def preprocess_markdown(md_content, viz_dir):
    """
    마크다운 내용 전처리
    - 이미지 경로를 Base64 데이터 URL로 변환 (HTML 파일에 이미지 임베딩)
    """
    def replace_image_path(match):
        alt_text = match.group(1)
        full_path = match.group(2)
        
        # file:/// 제거
        if full_path.startswith('file:///'):
            full_path = full_path.replace('file:///', '')
            # URL 인코딩 디코딩
            from urllib.parse import unquote
            full_path = unquote(full_path)
        
        # 경로가 존재하는지 확인
        image_path = None
        if Path(full_path).exists():
            image_path = Path(full_path)
        else:
            # 파일명만 추출하여 visualizations 폴더에서 찾기
            filename = Path(full_path).name
            viz_path = viz_dir / filename
            if viz_path.exists():
                image_path = viz_path
        
        if image_path:
            # 이미지를 Base64로 변환
            base64_url = image_to_base64(image_path)
            if base64_url:
                return f'![{alt_text}]({base64_url})'
        
        return match.group(0)
    
    # 이미지 경로 패턴 매칭 및 변환
    md_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image_path, md_content)
    
    return md_content

# ============================================================================
# HTML 템플릿
# ============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>의료기관 데이터 EDA 리포트</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 2cm;
            }}
            
            body {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}
            
            h1 {{
                page-break-before: always;
            }}
            
            h1:first-of-type {{
                page-break-before: avoid;
            }}
            
            img {{
                page-break-inside: avoid;
                max-width: 100%;
            }}
            
            table {{
                page-break-inside: avoid;
            }}
        }}
        
        body {{
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
            font-size: 28pt;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
            font-size: 20pt;
        }}
        
        h3 {{
            color: #555;
            margin-top: 25px;
            font-size: 16pt;
        }}
        
        h4 {{
            color: #666;
            margin-top: 20px;
            font-size: 13pt;
        }}
        
        p {{
            margin: 12px 0;
            text-align: justify;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: bold;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
        }}
        
        table th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        
        table td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        
        table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 25px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
        }}
        
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
            border: 1px solid #ddd;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 20px 0;
            color: #555;
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 3px;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 40px 0;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        
        .header h1 {{
            margin: 0;
            border: none;
            color: white;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            border-top: 2px solid #ddd;
            color: #666;
            font-size: 9pt;
        }}
        
        @media screen {{
            body {{
                background-color: #f5f5f5;
            }}
            
            .container {{
                background-color: white;
                padding: 40px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                border-radius: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>의료기관 데이터 EDA 리포트</h1>
            <p>서울 강남구 피부과 의료기관 탐색적 데이터 분석</p>
        </div>
        
        {content}
        
        <div class="footer">
            <p>생성일시: 2026-01-16 | 분석 도구: Python (pandas, matplotlib, seaborn)</p>
            <p>© 2026 의료기관 데이터 분석 프로젝트</p>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# 메인 실행
# ============================================================================

def main():
    print("=" * 80)
    print("EDA 리포트 HTML 변환 (PDF 인쇄용)")
    print("=" * 80)
    print()
    
    # 1. 마크다운 파일 읽기
    print(f"[1] 마크다운 파일 읽기: {INPUT_MD.name}")
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        md_content = f.read()
    print(f"  [OK] 파일 크기: {len(md_content):,} bytes")
    print()
    
    # 2. 마크다운 전처리 (이미지를 Base64로 변환)
    print("[2] 마크다운 전처리 (이미지 Base64 변환)")
    md_content = preprocess_markdown(md_content, VIZ_DIR)
    print("  [OK] 전처리 완료")
    print()
    
    # 3. HTML 변환
    print("[3] HTML 변환")
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.nl2br',
    ]
    html_content = markdown.markdown(md_content, extensions=extensions)
    print("  [OK] HTML 생성 완료")
    print()
    
    # 4. HTML 파일 저장
    print("[4] HTML 파일 저장")
    final_html = HTML_TEMPLATE.format(content=html_content)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"  [OK] HTML 저장 완료: {OUTPUT_HTML}")
    print(f"  [OK] 파일 크기: {OUTPUT_HTML.stat().st_size / 1024:.1f} KB")
    print()
    
    print("=" * 80)
    print("HTML 변환 완료")
    print("=" * 80)
    print(f"출력 파일: {OUTPUT_HTML}")
    print()
    print("PDF 저장 방법:")
    print("1. 생성된 HTML 파일을 브라우저(Chrome, Edge 등)로 열기")
    print("2. Ctrl+P (인쇄) 누르기")
    print("3. '대상'에서 'PDF로 저장' 선택")
    print("4. '저장' 버튼 클릭")
    print()

if __name__ == "__main__":
    main()
