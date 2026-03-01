# -*- coding: utf-8 -*-
"""
한글 폰트가 적용된 지역별 분포 차트를 생성하고 HTML 보고서를 업데이트하는 통합 스크립트
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import base64
from io import BytesIO
import re

print("=" * 80)
print("한글 폰트 차트 생성 및 HTML 업데이트")
print("=" * 80)
print()

# 1. 한글 폰트 설정
print("[1] 한글 폰트 설정...")
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
print(f"  [OK] 폰트: {font_prop.get_name()}")
print()

# 2. 데이터 로드
print("[2] 데이터 로드...")
df = pd.read_csv(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260115_235745.csv', encoding='utf-8-sig')
print(f"  [OK] 데이터: {len(df):,}건")
print()

# 3. 지역별 분포 계산
print("[3] 지역별 분포 계산...")
region_counts = df['eqp_sidoCdNm'].value_counts()
print(f"  [OK] 지역 수: {len(region_counts)}개")
print()

# 4. 그래프 생성
print("[4] 그래프 생성...")
fig, ax = plt.subplots(figsize=(10, 6))
region_counts.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('지역별 의료기관 분포', fontproperties=font_prop, fontsize=16, pad=20)
ax.set_xlabel('지역', fontproperties=font_prop, fontsize=12)
ax.set_ylabel('의료기관 수', fontproperties=font_prop, fontsize=12)
ax.tick_params(axis='x', rotation=45)

# x축 레이블에 한글 폰트 적용
for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Base64로 인코딩
buffer = BytesIO()
plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
buffer.seek(0)
new_base64 = base64.b64encode(buffer.read()).decode()
plt.close()
print("  [OK] 차트 생성 완료")
print()

# 5. HTML 파일 업데이트
print("[5] HTML 파일 업데이트...")
html_path = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\reports\eda_report_20260116_011000.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# HTML에서 이미지 찾기
img_pattern = r'<img alt="([^"]*)" src="data:image/png;base64,([^"]+)" />'
matches = list(re.finditer(img_pattern, html_content))

if len(matches) >= 2:
    # 두 번째 이미지를 교체 (첫 번째는 결측치 히트맵)
    second_img = matches[1]
    old_base64 = second_img.group(2)
    
    # 이미지 교체
    html_content = html_content.replace(
        f'src="data:image/png;base64,{old_base64}"',
        f'src="data:image/png;base64,{new_base64}"'
    )
    
    # HTML 파일 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("  [OK] HTML 파일 업데이트 완료")
    print()
    print("=" * 80)
    print("작업 완료!")
    print(f"업데이트된 파일: {html_path}")
    print("=" * 80)
else:
    print("  [ERROR] 이미지를 찾을 수 없습니다.")
    print(f"  발견된 이미지 수: {len(matches)}개")
