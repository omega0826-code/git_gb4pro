# -*- coding: utf-8 -*-
"""
한글 폰트 설정 유틸리티
matplotlib에서 한글을 제대로 표시하기 위한 폰트 설정
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

def setup_korean_font():
    """
    한글 폰트를 설정합니다.
    우선순위: Malgun Gothic > NanumGothic > AppleGothic
    """
    # 사용 가능한 폰트 목록
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 한글 폰트 우선순위
    korean_fonts = ['Malgun Gothic', 'NanumGothic', 'NanumBarunGothic', 'AppleGothic', 'Gulim']
    
    selected_font = None
    for font in korean_fonts:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False
        print(f"[OK] 한글 폰트 설정: {selected_font}")
        return True
    else:
        # 폰트를 찾지 못한 경우 경고만 출력하고 계속 진행
        warnings.warn("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        plt.rcParams['axes.unicode_minus'] = False
        return False

if __name__ == "__main__":
    setup_korean_font()
    
    # 테스트
    import numpy as np
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.arange(5)
    y = [10, 20, 15, 25, 30]
    labels = ['강남역', '역삼역', '양재역', '선릉역', '가로수길']
    
    ax.bar(x, y)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title('한글 폰트 테스트')
    ax.set_xlabel('상권명')
    ax.set_ylabel('값')
    
    plt.tight_layout()
    plt.savefig('d:/git_gb4pro/data/서울시 주요 82장소 영역/REPORT/00_스크립트/font_test.png', dpi=150)
    print("[OK] 테스트 이미지 저장: font_test.png")
    plt.close()
