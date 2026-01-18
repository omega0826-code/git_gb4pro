"""
HTML alt 텍스트 상세 확인
"""
import re
from pathlib import Path

html_file = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 이미지 태그 찾기
img_tags = re.findall(r'<img\s+alt="([^"]*)"[^>]*>', content)

print("모든 이미지 alt 텍스트:")
for i, alt in enumerate(img_tags, 1):
    print(f"{i}. '{alt}'")
