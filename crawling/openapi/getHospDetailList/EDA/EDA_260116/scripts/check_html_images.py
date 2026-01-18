"""
HTML 이미지 태그 확인 스크립트
"""
import re
from pathlib import Path

html_file = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 이미지 태그 찾기
img_tags = re.findall(r'<img[^>]*alt="([^"]*)"[^>]*>', content)

print("발견된 이미지 alt 텍스트:")
for i, alt in enumerate(set(img_tags), 1):
    print(f"{i}. {alt}")
