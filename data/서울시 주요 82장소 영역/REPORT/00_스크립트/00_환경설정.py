# -*- coding: utf-8 -*-
"""
의원급 피부과 입지분석 EDA - 환경 설정
작성일: 2026-02-04
목적: 한글 폰트 설정, 필수 라이브러리 확인, 데이터 파일 검증
"""

import sys
import os
from pathlib import Path

def setup_korean_font():
    """한글 폰트 자동 감지 및 설정"""
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    
    print("\n[1/4] 한글 폰트 설정 중...")
    
    # 사용 가능한 한글 폰트 목록
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    korean_fonts = ['Malgun Gothic', 'NanumGothic', 'Gulim', 'Batang', 'AppleGothic']
    
    selected_font = None
    for font in korean_fonts:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False
        print(f"   [OK] 한글 폰트 설정 완료: {selected_font}")
        return True
    else:
        print("   ⚠ 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        plt.rcParams['axes.unicode_minus'] = False
        return False

def check_libraries():
    """필수 라이브러리 확인"""
    print("\n[2/4] 필수 라이브러리 확인 중...")
    
    required_libs = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn'
    }
    
    missing_libs = []
    
    for lib_name, import_name in required_libs.items():
        try:
            __import__(import_name)
            print(f"   [OK] {lib_name} 설치됨")
        except ImportError:
            print(f"   ✗ {lib_name} 미설치")
            missing_libs.append(lib_name)
    
    if missing_libs:
        print(f"\n   ⚠ 다음 라이브러리를 설치해주세요:")
        print(f"   pip install {' '.join(missing_libs)}")
        return False
    
    print("   [OK] 모든 필수 라이브러리 확인 완료")
    return True

def check_data_files():
    """데이터 파일 존재 확인"""
    print("\n[3/4] 데이터 파일 확인 중...")
    
    base_path = Path(__file__).parent.parent.parent
    data_dir = base_path / 'Gangnam_9_Areas'
    
    required_files = [
        'gangnam_서울시 상권분석서비스(영역-상권).csv',
        'gangnam_서울시 상권분석서비스(상주인구-상권).csv',
        'gangnam_서울시 상권분석서비스(직장인구-상권).csv',
        'gangnam_서울시 상권분석서비스(길단위인구-상권).csv',
        'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv',
        'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv',
        'gangnam_서울시 상권분석서비스(집객시설-상권).csv',
        'gangnam_서울시 상권분석서비스(소득소비-상권).csv',
        'gangnam_서울시 상권분석서비스(상권변화지표-상권).csv'
    ]
    
    missing_files = []
    
    for file_name in required_files:
        file_path = data_dir / file_name
        if file_path.exists():
            file_size = file_path.stat().st_size / 1024  # KB
            print(f"   [OK] {file_name[:40]}... ({file_size:.1f} KB)")
        else:
            print(f"   ✗ {file_name} 없음")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n   ⚠ {len(missing_files)}개 파일이 누락되었습니다.")
        return False
    
    print(f"   [OK] 모든 데이터 파일 확인 완료 (총 {len(required_files)}개)")
    return True

def verify_output_directories():
    """출력 디렉토리 확인"""
    print("\n[4/4] 출력 디렉토리 확인 중...")
    
    base_path = Path(__file__).parent.parent
    
    required_dirs = [
        '00_스크립트',
        '01_경쟁환경분석',
        '02_고객분석',
        '03_인구유동분석',
        '04_입지조건분석',
        '05_종합평가',
        '06_최종리포트'
    ]
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"   [OK] {dir_name}")
        else:
            print(f"   ⚠ {dir_name} 디렉토리가 없습니다. 생성 중...")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   [OK] {dir_name} 생성 완료")
    
    print("   [OK] 모든 출력 디렉토리 확인 완료")
    return True

def main():
    """환경 설정 메인 함수"""
    print("=" * 70)
    print("의원급 피부과 입지분석 EDA - 환경 설정")
    print("=" * 70)
    
    # 1. 한글 폰트 설정
    font_ok = setup_korean_font()
    
    # 2. 필수 라이브러리 확인
    libs_ok = check_libraries()
    
    # 3. 데이터 파일 확인
    data_ok = check_data_files()
    
    # 4. 출력 디렉토리 확인
    dirs_ok = verify_output_directories()
    
    # 최종 결과
    print("\n" + "=" * 70)
    if font_ok and libs_ok and data_ok and dirs_ok:
        print("[OK] 환경 설정 완료! 분석을 시작할 수 있습니다.")
        print("=" * 70)
        return 0
    else:
        print("⚠ 환경 설정 중 문제가 발생했습니다. 위의 메시지를 확인해주세요.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
