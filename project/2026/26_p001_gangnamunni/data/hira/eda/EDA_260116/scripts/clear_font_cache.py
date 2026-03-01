"""
Matplotlib 폰트 캐시 삭제 스크립트
================================================================================
목적: 한글 폰트 렌더링 문제 해결을 위한 matplotlib 폰트 캐시 삭제
작성일: 2026-01-16
================================================================================
"""

import matplotlib as mpl
import shutil
from pathlib import Path

def clear_matplotlib_cache():
    """Matplotlib 폰트 캐시 디렉토리 삭제"""
    cache_dir = mpl.get_cachedir()
    cache_path = Path(cache_dir)
    
    print("=" * 80)
    print("Matplotlib 폰트 캐시 삭제")
    print("=" * 80)
    print()
    print(f"캐시 디렉토리: {cache_dir}")
    print()
    
    if cache_path.exists():
        try:
            shutil.rmtree(cache_dir, ignore_errors=True)
            print("[OK] 폰트 캐시가 성공적으로 삭제되었습니다.")
            print()
            print("다음 단계:")
            print("  1. Python 인터프리터를 재시작하세요.")
            print("  2. EDA 스크립트를 다시 실행하세요.")
        except Exception as e:
            print(f"[ERROR] 캐시 삭제 실패: {e}")
    else:
        print("[INFO] 캐시 디렉토리가 존재하지 않습니다.")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    clear_matplotlib_cache()
