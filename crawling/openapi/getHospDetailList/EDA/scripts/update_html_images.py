"""
HTML 보고서 이미지 업데이트 스크립트 (수정 버전)
================================================================================
목적: HTML 보고서의 Base64 인코딩된 이미지를 새로운 한글 폰트 적용 이미지로 교체
작성일: 2026-01-16
================================================================================
"""

import base64
import re
from pathlib import Path

# 경로 설정
html_file = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html")
viz_dir = Path(r"D:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\visualizations")

# 이미지 파일 매핑 (alt 텍스트 -> 파일명)
image_mapping = {
    "결측치 히트맵": "01_missing_data_heatmap.png",
    "병원 종별 분포": "02_hospital_type_distribution.png",
    "시군구별 분포": "03_district_distribution.png",
    "설립연도": "05_establishment_year_distribution.png",
    "진료과목": "06_department_distribution.png",
    "주차 정보 분석": "07_parking_analysis.png",
    "진료시간": "08_operating_hours_pattern.png"
}

print("=" * 80)
print("HTML 보고서 이미지 업데이트")
print("=" * 80)
print()

# HTML 파일 읽기
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 각 이미지를 Base64로 인코딩하여 교체
updated_count = 0
for alt_text, img_file in image_mapping.items():
    img_path = viz_dir / img_file
    
    if not img_path.exists():
        print(f"[WARNING] 이미지 파일을 찾을 수 없습니다: {img_file}")
        continue
    
    # 이미지를 Base64로 인코딩
    with open(img_path, 'rb') as f:
        img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
    
    # HTML에서 해당 이미지의 Base64 데이터 찾기 및 교체
    # 패턴: <img alt="..." src="data:image/png;base64,..." />
    pattern = rf'(<img\s+alt="{re.escape(alt_text)}"\s+src="data:image/png;base64,)[^"]*(")'
    
    def replace_base64(match):
        return match.group(1) + img_base64 + match.group(2)
    
    html_content, count = re.subn(pattern, replace_base64, html_content)
    
    if count > 0:
        print(f"[OK] {alt_text} ({img_file}) 업데이트 완료 ({count}개 교체)")
        updated_count += count
    else:
        print(f"[WARNING] '{alt_text}'에 해당하는 이미지를 HTML에서 찾을 수 없습니다")

# 업데이트된 HTML 파일 저장
if updated_count > 0:
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print()
    print(f"[OK] HTML 보고서 업데이트 완료 (총 {updated_count}개 이미지 교체)")
    print(f"[OK] 저장 위치: {html_file}")
else:
    print()
    print("[WARNING] 업데이트된 이미지가 없습니다")

print()
print("=" * 80)
