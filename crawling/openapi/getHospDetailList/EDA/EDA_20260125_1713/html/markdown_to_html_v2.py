# -*- coding: utf-8 -*-
"""
EDA 리포트 HTML 변환 스크립트 v2.0
================================================================================
작성일: 2026-01-26
목적: markdown_to_html_guideline.md를 준수하는 프리미엄 HTML 리포트 생성
특징: 단일 파일(Base64 이미지), 반응형 디자인, 그라데이션 스타일, 인코딩 안전 엔티티
================================================================================
"""

import markdown
import base64
import os
import re
from pathlib import Path
from datetime import datetime

# ============================================================================
# 설정 (파일 경로)
# ============================================================================
BASE_DIR = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_20260125_1713")
INPUT_MD = BASE_DIR / "EDA_REPORT_20260125_1713.md"
OUTPUT_HTML = BASE_DIR / "html" / "EDA_REPORT_20260125_1713.html"
IMAGE_DIR = BASE_DIR

# ============================================================================
# HTML 엔티티 (인코딩 안전)
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
}

def safe_encode(text):
    for char, entity in HTML_ENTITIES.items():
        text = text.replace(char, entity)
    return text

# ============================================================================
# 이미지 처리 (Base64)
# ============================================================================
def get_base64_image(image_name):
    image_path = IMAGE_DIR / image_name
    if not image_path.exists():
        print(f"Warning: Image not found - {image_path}")
        return ""
    
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
        ext = image_path.suffix.lower().replace('.', '')
        return f"data:image/{ext};base64,{data}"

def embed_images(md_content):
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
# 스타일 정의
# ============================================================================
CSS_STYLE = """
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --text-primary: #2d3436;
    --text-secondary: #636e72;
    --bg-light: #f9f9f9;
    --card-bg: #ffffff;
    --accent: #ff7675;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Malgun Gothic', -apple-system, sans-serif;
    line-height: 1.8;
    color: var(--text-primary);
    background-color: var(--bg-light);
    padding: 40px 20px;
}

.report-container {
    max-width: 1000px;
    margin: 0 auto;
    background: var(--card-bg);
    padding: 60px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

header {
    background: var(--bg-gradient);
    color: white;
    padding: 40px;
    border-radius: 15px;
    margin-bottom: 50px;
    text-align: center;
}

header h1 { font-size: 2.5em; margin-bottom: 10px; }
header .meta { font-size: 0.9em; opacity: 0.9; }

h2 {
    font-size: 1.8em;
    color: var(--secondary-color);
    border-left: 6px solid var(--primary-color);
    padding-left: 15px;
    margin: 40px 0 20px;
    background: rgba(102, 126, 234, 0.05);
    padding-top: 5px;
    padding-bottom: 5px;
}

h3 {
    font-size: 1.4em;
    margin: 30px 0 15px;
    color: #444;
}

p { margin-bottom: 15px; }

ul, ol { margin-left: 25px; margin-bottom: 20px; }
li { margin-bottom: 8px; }

blockquote {
    background: #e7f3ff;
    border-left: 5px solid var(--primary-color);
    padding: 20px;
    margin: 30px 0;
    border-radius: 0 10px 10px 0;
    font-weight: 500;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 30px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

th {
    background: var(--bg-gradient);
    color: white;
    padding: 15px;
    text-align: left;
}

td {
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
}

tr:nth-child(even) { background-color: #fcfcfc; }
tr:hover { background-color: #f5f7fa; }

.image-container {
    margin: 40px 0;
    text-align: center;
}

.image-container img {
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    border: 1px solid #eee;
}

.image-caption {
    margin-top: 12px;
    font-size: 0.9em;
    color: var(--text-secondary);
    font-style: italic;
}

hr {
    border: 0;
    height: 1px;
    background: #eee;
    margin: 40px 0;
}

/* 통계 카드 그리드 (자동 전환) */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.stat-item {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #eee;
    text-align: center;
}

footer {
    margin-top: 60px;
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.85em;
}

@media (max-width: 768px) {
    .report-container { padding: 30px; }
    header h1 { font-size: 1.8em; }
}
"""

# ============================================================================
# 메인 로직
# ============================================================================
def convert():
    print(f"Reading: {INPUT_MD}")
    with open(INPUT_MD, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. 특수 문자 치환 (엔티티)
    content = safe_encode(content)
    
    # 2. 이미지 임베딩 (Base64)
    content = embed_images(content)
    
    # 3. 마크다운 변환
    extensions = ['tables', 'fenced_code', 'nl2br', 'toc']
    html_body = markdown.markdown(content, extensions=extensions)
    
    # 4. 전체 HTML 구성
    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>강남구 피부과 분석 리포트</title>
    <style>{CSS_STYLE}</style>
</head>
<body>
    <div class="report-container">
        <header>
            <h1>강남구 피부과 의료기관 분석</h1>
            <div class="meta">발행일: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 분석대상: N=333</div>
        </header>
        
        <main>
            {html_body}
        </main>
        
        <footer>
            <p>© 2026 EDA Analysis Project | markdown_to_html_guideline.md 기반 생성</p>
        </footer>
    </div>
</body>
</html>"""

    # 5. 출력 디렉토리 확인 및 저장
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print(f"Success! HTML saved to: {OUTPUT_HTML}")
    print(f"File size: {OUTPUT_HTML.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    convert()
