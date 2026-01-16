"""
한글 폰트 테스트 스크립트
================================================================================
목적: matplotlib에서 한글 폰트가 제대로 렌더링되는지 테스트
작성일: 2026-01-16
================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# 폰트 파일 경로
font_path = r'C:\Windows\Fonts\malgun.ttf'

# FontProperties 객체 생성
font_prop = fm.FontProperties(fname=font_path)

# 테스트 그래프 생성
fig, ax = plt.subplots(figsize=(8, 6))

# 한글 텍스트 테스트
test_data = ['의원', '병원', '종합병원', '상급종합']
test_values = [1143, 6, 2, 2]

bars = ax.barh(test_data, test_values, color='skyblue')

# 제목과 레이블에 폰트 직접 적용
ax.set_title('한글 폰트 테스트', fontproperties=font_prop, fontsize=16, fontweight='bold')
ax.set_xlabel('병원 수', fontproperties=font_prop, fontsize=12)
ax.set_ylabel('종별', fontproperties=font_prop, fontsize=12)

# Y축 레이블에 폰트 적용
ax.set_yticklabels(test_data, fontproperties=font_prop)

# 값 표시
for i, v in enumerate(test_values):
    ax.text(v + 10, i, f'{v}건', va='center', fontproperties=font_prop, fontsize=10)

plt.tight_layout()

# 저장
output_dir = Path(__file__).parent.parent / 'visualizations'
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'font_test.png', dpi=300, bbox_inches='tight')
print(f"[OK] 테스트 그래프 저장: {output_dir / 'font_test.png'}")
plt.close()

print()
print("폰트 정보:")
print(f"  - 폰트 이름: {font_prop.get_name()}")
print(f"  - 폰트 파일: {font_prop.get_file()}")
print(f"  - 폰트 패밀리: {font_prop.get_family()}")
