# -*- coding: utf-8 -*-
"""
한글 폰트 진단 스크립트
matplotlib에서 사용 가능한 한글 폰트를 확인합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import sys

print("=" * 80)
print("한글 폰트 진단")
print("=" * 80)

# 1. 시스템 인코딩 확인
print(f"\n1. 시스템 인코딩: {sys.stdout.encoding}")

# 2. 사용 가능한 모든 폰트 목록
available_fonts = sorted([f.name for f in fm.fontManager.ttflist])
print(f"\n2. 사용 가능한 폰트 개수: {len(available_fonts)}")

# 3. 한글 폰트 검색
korean_fonts = ['Malgun Gothic', 'NanumGothic', 'NanumBarunGothic', 'AppleGothic', 'Gulim', 'Batang', 'Dotum']
print(f"\n3. 한글 폰트 검색 결과:")
found_fonts = []
for font in korean_fonts:
    if font in available_fonts:
        found_fonts.append(font)
        print(f"   [O] {font}")
    else:
        print(f"   [X] {font}")

# 4. 현재 matplotlib 폰트 설정
print(f"\n4. 현재 matplotlib 폰트 설정:")
print(f"   font.family: {plt.rcParams['font.family']}")
print(f"   axes.unicode_minus: {plt.rcParams['axes.unicode_minus']}")

# 5. 권장사항
print(f"\n5. 권장사항:")
if found_fonts:
    print(f"   - 사용 가능한 한글 폰트: {', '.join(found_fonts)}")
    print(f"   - 권장 폰트: {found_fonts[0]}")
else:
    print("   [경고] 한글 폰트를 찾을 수 없습니다!")
    print("   - 해결방법 1: 나눔고딕 폰트 설치 (https://hangeul.naver.com/font)")
    print("   - 해결방법 2: matplotlib 폰트 캐시 삭제 후 재시작")

print("\n" + "=" * 80)
