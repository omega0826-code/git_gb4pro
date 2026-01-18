# -*- coding: utf-8 -*-
import re

# Base64 이미지 읽기
with open(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\temp_base64.txt', 'r') as f:

    new_base64 = f.read().strip()

# HTML 파일 읽기
html_path = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# "지역별" 또는 "시도" 관련 이미지 태그 찾기
# HTML에서 img 태그를 찾아 base64 이미지를 교체
pattern = r'(\u003cimg alt="[^"]*지역[^"]*"[^\u003e]*src="data:image/png;base64,)([^"]+)(")'
match = re.search(pattern, html_content)

if match:
    # 기존 base64 이미지를 새로운 것으로 교체
    html_content = re.sub(pattern, r'\1' + new_base64 + r'\3', html_content)
    
    # HTML 파일 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("SUCCESS: HTML 파일이 성공적으로 업데이트되었습니다.")
else:
    print("ERROR: 지역별 분포 이미지를 찾을 수 없습니다.")
    print("다른 패턴으로 시도합니다...")
    
    # 결측치 히트맵 다음에 오는 이미지를 찾기
    pattern2 = r'(결측치 히트맵.*?\u003c/p\u003e\s*\u003cp\u003e\u003cimg[^\u003e]*src="data:image/png;base64,)([^"]+)(")'
    if re.search(pattern2, html_content, re.DOTALL):
        html_content = re.sub(pattern2, r'\1' + new_base64 + r'\3', html_content, flags=re.DOTALL)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("SUCCESS: HTML 파일이 성공적으로 업데이트되었습니다 (패턴2).")
    else:
        print("ERROR: 이미지를 찾을 수 없습니다.")
