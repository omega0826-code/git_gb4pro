# -*- coding: utf-8 -*-
"""
TOP3 비교 리포트 HTML 변환 스크립트
================================================================================
작성일: 2026-01-27
목적: TOP3_COMPARISON_REPORT.md를 고품질 HTML로 변환
가이드라인: markdown_to_html_guideline.md 준수
================================================================================
"""

import markdown
import base64
import os
import re
from pathlib import Path
from datetime import datetime

# ============================================================================
# 경로 설정
# ============================================================================
BASE_DIR = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA260127\TOP3")
INPUT_MD = BASE_DIR / "TOP3_COMPARISON_REPORT.md"
OUTPUT_HTML = BASE_DIR / "TOP3_COMPARISON_REPORT.html"
VIZ_DIR = BASE_DIR / "visualizations"

print("=" * 80)
print("TOP3 비교 리포트 HTML 변환")
print("=" * 80)
print(f"입력 파일: {INPUT_MD}")
print(f"출력 파일: {OUTPUT_HTML}")
print()

# ============================================================================
# HTML 엔티티
# ============================================================================
HTML_ENTITIES = {
    '→': '&rarr;',
    '←': '&larr;',
    '•': '&bull;',
    '💡': '&#128161;',
    '📌': '&#128204;',
    '📊': '&#128202;',
    '🔍': '&#128269;',
    '📈': '&#128200;',
    '✅': '&#9989;',
    '⚠️': '&#9888;',
    '🎯': '&#127919;',
}

def safe_encode(text):
    """특수 문자를 HTML 엔티티로 변환"""
    for char, entity in HTML_ENTITIES.items():
        text = text.replace(char, entity)
    return text

# ============================================================================
# 이미지 처리 (Base64)
# ============================================================================
def get_base64_image(image_name):
    """이미지를 Base64로 인코딩"""
    # visualizations/ 경로가 포함된 경우 제거
    if image_name.startswith('visualizations/'):
        image_name = image_name.replace('visualizations/', '')
    
    image_path = VIZ_DIR / image_name
    if not image_path.exists():
        print(f"  [WARNING] 이미지 없음: {image_path}")
        return ""
    
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
        ext = image_path.suffix.lower().replace('.', '')
        return f"data:image/{ext};base64,{data}"

def embed_images(md_content):
    """마크다운의 이미지를 Base64로 임베딩"""
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def replace_img(match):
        alt = match.group(1)
        src = match.group(2)
        base64_data = get_base64_image(src)
        if base64_data:
            return f'<div class="image-container"><img src="{base64_data}" alt="{alt}"><div class="image-caption">{alt}</div></div>'
        return match.group(0)
    
    return re.sub(img_pattern, replace_img, md_content)

# ============================================================================
# CSS 스타일 (비교 분석 특화)
# ============================================================================
CSS_STYLE = """
:root {
    --primary-color: #2E86DE;
    --secondary-color: #FF6B6B;
    --tertiary-color: #95A5A6;
    --bg-gradient: linear-gradient(135deg, #2E86DE 0%, #1E5FA8 100%);
    --text-primary: #2d3436;
    --text-secondary: #636e72;
    --bg-light: #f9f9f9;
    --card-bg: #ffffff;
    --accent: #00d2d3;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.8;
    color: var(--text-primary);
    background-color: var(--bg-light);
    padding: 40px 20px;
}

.report-container {
    max-width: 1100px;
    margin: 0 auto;
    background: var(--card-bg);
    padding: 60px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

header {
    background: var(--bg-gradient);
    color: white;
    padding: 50px;
    border-radius: 15px;
    margin-bottom: 50px;
    text-align: center;
}

header h1 { 
    font-size: 2.8em; 
    margin-bottom: 15px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

header .meta { 
    font-size: 1em; 
    opacity: 0.95;
    margin-top: 20px;
    line-height: 1.6;
}

h2 {
    font-size: 1.9em;
    color: var(--primary-color);
    border-left: 6px solid var(--primary-color);
    padding-left: 15px;
    margin: 50px 0 25px;
    background: rgba(46, 134, 222, 0.05);
    padding-top: 12px;
    padding-bottom: 12px;
}

h3 {
    font-size: 1.5em;
    margin: 35px 0 18px;
    color: #444;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
}

h4 {
    font-size: 1.3em;
    margin: 28px 0 14px;
    color: #555;
}

p { 
    margin-bottom: 18px;
    text-align: justify;
}

ul, ol { 
    margin-left: 30px; 
    margin-bottom: 22px; 
}

li { 
    margin-bottom: 10px;
    line-height: 1.7;
}

blockquote {
    background: #e7f3ff;
    border-left: 5px solid var(--primary-color);
    padding: 22px;
    margin: 35px 0;
    border-radius: 0 10px 10px 0;
    font-weight: 500;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 35px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-radius: 8px;
    overflow: hidden;
}

th {
    background: var(--bg-gradient);
    color: white;
    padding: 16px;
    text-align: left;
    font-weight: 600;
}

td {
    padding: 14px 16px;
    border-bottom: 1px solid #eee;
}

tr:nth-child(even) { 
    background-color: #fcfcfc; 
}

tr:hover { 
    background-color: #f5f7fa; 
}

/* 피부과 강조 스타일 */
tr td:first-child strong,
td strong {
    color: var(--primary-color);
    font-weight: 700;
}

.image-container {
    margin: 45px 0;
    text-align: center;
    page-break-inside: avoid;
}

.image-container img {
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    border: 1px solid #eee;
}

.image-caption {
    margin-top: 14px;
    font-size: 0.95em;
    color: var(--text-secondary);
    font-style: italic;
}

hr {
    border: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, #ddd, transparent);
    margin: 45px 0;
}

strong {
    color: var(--primary-color);
    font-weight: 600;
}

code {
    background: #f4f4f4;
    padding: 3px 7px;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
}

/* 체크 마크 스타일 */
li:has(> :first-child:is(✅)) {
    list-style-type: none;
    margin-left: -20px;
}

footer {
    margin-top: 70px;
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.9em;
    padding-top: 35px;
    border-top: 2px solid #eee;
}

/* 인쇄 최적화 */
@media print {
    body {
        background: white;
        padding: 0;
    }
    
    .report-container {
        box-shadow: none;
        padding: 20px;
    }
    
    h2 {
        page-break-after: avoid;
    }
    
    .image-container {
        page-break-inside: avoid;
    }
}

/* 반응형 */
@media (max-width: 768px) {
    .report-container { 
        padding: 30px 20px; 
    }
    
    header h1 { 
        font-size: 2em; 
    }
    
    h2 {
        font-size: 1.6em;
    }
}
"""

# ============================================================================
# 메인 로직
# ============================================================================
def convert():
    print("[1] 마크다운 파일 읽기")
    with open(INPUT_MD, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  - 파일 크기: {len(content):,} bytes")
    
    # 특수 문자 치환
    print("[2] 특수 문자 처리")
    content = safe_encode(content)
    
    # 이미지 임베딩
    print("[3] 이미지 Base64 임베딩")
    content = embed_images(content)
    
    # 마크다운 변환
    print("[4] HTML 변환")
    extensions = ['tables', 'fenced_code', 'nl2br', 'toc']
    html_body = markdown.markdown(content, extensions=extensions)
    
    # 전체 HTML 구성
    print("[5] 최종 HTML 생성")
    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>피부과 중심 TOP3 진료과목 비교 분석</title>
    <style>{CSS_STYLE}</style>
</head>
<body>
    <div class="report-container">
        <header>
            <h1>&#128202; 피부과 중심 TOP3 진료과목 비교 분석</h1>
            <div class="meta">
                발행일: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
                분석대상: 성형외과(412개), 피부과(333개), 내과(300개) - 총 1,045개<br>
                메인 분석: <strong style="color: white;">피부과</strong>
            </div>
        </header>
        
        <main>
            {html_body}
        </main>
        
        <footer>
            <p>&copy; 2026 EDA Analysis Project | TOP3 Department Comparison</p>
            <p>분석 도구: Python (pandas, matplotlib, seaborn)</p>
            <p>가이드라인: markdown_to_html_guideline.md 기반 생성</p>
        </footer>
    </div>
</body>
</html>"""

    # 저장
    print("[6] HTML 파일 저장")
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    file_size = OUTPUT_HTML.stat().st_size / 1024
    print(f"  - 저장 완료: {OUTPUT_HTML}")
    print(f"  - 파일 크기: {file_size:.1f} KB")
    print()
    print("=" * 80)
    print("HTML 변환 완료!")
    print("=" * 80)

if __name__ == "__main__":
    convert()
