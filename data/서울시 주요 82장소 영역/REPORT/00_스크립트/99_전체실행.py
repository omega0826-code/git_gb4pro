# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 전체 파이프라인 실행
작성일: 2026-02-03
버전: 5.01 (이모지 제거 - Windows 터미널 호환성 개선)
"""

import sys
import os
import subprocess
from datetime import datetime
import time

def run_script(script_name):
    print(f"\n>>> 실행 중: {script_name}")
    start_time = time.time()
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    # subprocess를 사용하여 별도 프로세스로 실행
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False,
        text=True,
        encoding='utf-8'
    )
    
    elapsed = time.time() - start_time
    if result.returncode == 0:
        print(f"[OK] 완료: {script_name} (소요시간: {elapsed:.1f}초)")
        return True
    else:
        print(f"[ERROR] 실패: {script_name} (에러 코드: {result.returncode})")
        return False

def main():
    print("=" * 80)
    print("의원급 피부과 입지 분석 전체 파이프라인 실행")
    print("=" * 80)
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    pipeline = [
        '01_데이터로딩.py',
        '02_경쟁환경분석.py',
        '03_고객분석.py',
        '04_인구유동분석.py',
        '05_입지조건분석.py',
        '06_종합평가.py',
        '07_리포트생성.py'
    ]
    
    total_start = time.time()
    for script in pipeline:
        if not run_script(script):
            print("\n[ALERT] 파이프라인 실행 중 오류가 발생하여 중단합니다.")
            sys.exit(1)
            
    total_elapsed = time.time() - total_start
    print("\n" + "=" * 80)
    print("SUCCESS: 모든 분석 단계가 성공적으로 완료되었습니다!")
    print(f"총 소요 시간: {total_elapsed:.1f}초")
    print(f"종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print("\n최종 리포트 경로: d:/git_gb4pro/data/서울시 주요 82장소 영역/REPORT/06_최종리포트/최종리포트.html")

if __name__ == "__main__":
    main()
