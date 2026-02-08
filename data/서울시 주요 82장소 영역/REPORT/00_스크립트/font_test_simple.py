# -*- coding: utf-8 -*-
"""
간단한 폰트 설정 테스트
matplotlib에서 한글이 제대로 표시되는지 확인
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 한글 폰트 설정
available_fonts = [f.name for f in fm.fontManager.ttflist]
korean_fonts = ['Malgun Gothic', 'NanumGothic', 'Gulim', 'Batang']

selected_font = None
for font in korean_fonts:
    if font in available_fonts:
        selected_font = font
        break

if selected_font:
    plt.rcParams['font.family'] = selected_font
    plt.rcParams['axes.unicode_minus'] = False
    print(f"[OK] 한글 폰트 설정: {selected_font}")
else:
    print("[WARNING] 한글 폰트를 찾을 수 없습니다.")

# 테스트 그래프 생성
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 1. 막대 그래프
ax1 = axes[0]
categories = ['강남역', '역삼역', '가로수길', '강남구청', '양재역']
values = [175.8, 389, 3963.905, 4791.223, 50]

ax1.barh(categories, values, color='orange')
ax1.set_xlabel('상권별 집계시설 수')
ax1.set_title('상권별 집계시설 수')

# 2. 레이더 차트
ax2 = axes[1]
categories2 = ['경쟁 환경', '고객 수요', '기초수요', '강남역']
angles = np.linspace(0, 2 * np.pi, len(categories2), endpoint=False).tolist()
angles += angles[:1]

values2 = [80, 90, 70, 85]
values2 += values2[:1]

ax2.plot(angles, values2, 'o-', linewidth=2, label='테스트')
ax2.fill(angles, values2, alpha=0.25)
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories2)
ax2.set_ylim(0, 100)
ax2.set_title('상권별 평균 소득')
ax2.legend()

plt.tight_layout()
plt.savefig('d:/git_gb4pro/data/서울시 주요 82장소 영역/REPORT/00_스크립트/font_test_result.png', 
            dpi=150, bbox_inches='tight')
print("[OK] 테스트 그래프 저장: font_test_result.png")
plt.close()

print("\n[결과] 저장된 이미지를 확인하여 한글이 제대로 표시되는지 확인하세요.")
