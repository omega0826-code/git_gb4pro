# -*- coding: utf-8 -*-
"""
HTML 보고서의 모든 이미지를 visualizations 폴더의 한글 폰트 이미지로 교체
"""
import base64
import re
from pathlib import Path

print("=" * 80)
print("HTML 보고서 이미지 교체")
print("=" * 80)
print()

# 경로 설정
viz_dir = Path(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\visualizations')
html_path = Path(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html')

# 이미지 파일 목록
image_files = {
    '01_missing_data_heatmap.png': '결측치 히트맵',
    '02_hospital_type_distribution.png': '병원 종별 분포',
    '03_district_distribution.png': '시군구별',
    '05_establishment_year_distribution.png': '설립연도',
    '06_department_distribution.png': '진료과목',
    '07_parking_analysis.png': '주차',
    '08_operating_hours_pattern.png': '진료시간'
}

print("[1] 이미지 파일을 Base64로 인코딩...")
encoded_images = {}
for filename, description in image_files.items():
    img_path = viz_dir / filename
    if img_path.exists():
        with open(img_path, 'rb') as f:
            img_data = f.read()
            encoded = base64.b64encode(img_data).decode('utf-8')
            encoded_images[filename] = encoded
            print(f"  [OK] {filename} ({len(encoded):,} bytes)")
    else:
        print(f"  [SKIP] {filename} (파일 없음)")

print(f"\n총 {len(encoded_images)}개 이미지 인코딩 완료\n")

# HTML 파일 읽기
print("[2] HTML 파일 읽기...")
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
print("  [OK] HTML 파일 로드 완료\n")

# HTML에서 모든 이미지 태그 찾기
print("[3] 이미지 교체 중...")
img_pattern = r'<img alt="([^"]*)" src="data:image/png;base64,([^"]+)" />'
matches = list(re.finditer(img_pattern, html_content))
print(f"  발견된 이미지: {len(matches)}개\n")

# 이미지 순서대로 매칭
image_order = [
    '01_missing_data_heatmap.png',
    '03_district_distribution.png',  # 지역별 분포 (시군구)
    '02_hospital_type_distribution.png',
    '05_establishment_year_distribution.png',
    '06_department_distribution.png',
    '07_parking_analysis.png',
    '08_operating_hours_pattern.png'
]

replaced_count = 0
for idx, match in enumerate(matches):
    if idx < len(image_order):
        img_file = image_order[idx]
        if img_file in encoded_images:
            old_base64 = match.group(2)
            new_base64 = encoded_images[img_file]
            
            # 이미지 교체
            html_content = html_content.replace(
                f'src="data:image/png;base64,{old_base64}"',
                f'src="data:image/png;base64,{new_base64}"',
                1  # 한 번만 교체
            )
            replaced_count += 1
            print(f"  [{idx+1}] {match.group(1)[:30]:30s} → {img_file}")

print(f"\n총 {replaced_count}개 이미지 교체 완료\n")

# HTML 파일 저장
print("[4] HTML 파일 저장...")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("  [OK] 저장 완료\n")

print("=" * 80)
print("작업 완료!")
print(f"업데이트된 파일: {html_path}")
print("=" * 80)
