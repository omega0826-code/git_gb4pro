# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 데이터 로딩 및 초기 설정
작성일: 2026-02-03
버전: 5.01 (UTF-8 안정화 버전)
"""

import pandas as pd
import numpy as np
import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

# ============================================================================
# 인코딩 환경 설정
# ============================================================================
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"인코딩 설정 경고: {e}", flush=True)

# ============================================================================
# 하트비트 및 로그 설정
# ============================================================================
BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
REPORT_DIR = BASE_DIR / 'REPORT'
HEARTBEAT_FILE = REPORT_DIR / 'heartbeat.txt'

def write_heartbeat(message):
    try:
        with open(HEARTBEAT_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
            f.flush()
    except:
        pass

# 초기화
REPORT_DIR.mkdir(parents=True, exist_ok=True)
with open(HEARTBEAT_FILE, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("Data Loading Execution Log\n")
    f.write("=" * 80 + "\n")

write_heartbeat("START - 데이터 로딩 시작")

# ============================================================================
# 폰트 및 데이터 로딩 함수
# ============================================================================
def load_csv_with_retry(file_path, max_retries=3, encoding='utf-8-sig'):
    for attempt in range(1, max_retries + 1):
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                raise Exception(f"Failed to load {file_path.name}: {e}")

def load_data():
    data_path = BASE_DIR / 'Gangnam_9_Areas'
    
    # 출력 디렉토리 생성
    print("[1/3] 출력 디렉토리 생성 중...", end=' ', flush=True)
    dirs = ['01_경쟁환경분석', '02_고객분석', '03_인구유동분석', '04_입지조건분석', '05_종합평가', '06_최종리포트']
    for d in dirs:
        (REPORT_DIR / d).mkdir(parents=True, exist_ok=True)
    print("완료")

    # 파일 목록
    files_to_load = [
        ('영역-상권', 'gangnam_서울시 상권분석서비스(영역-상권).csv'),
        ('상권변화지표', 'gangnam_서울시 상권분석서비스(상권변화지표-상권).csv'),
        ('점포-상권', 'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv'),
        ('추정매출-상권', 'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv'),
        ('상주인구-상권', 'gangnam_서울시 상권분석서비스(상주인구-상권).csv'),
        ('직장인구-상권', 'gangnam_서울시 상권분석서비스(직장인구-상권).csv'),
        ('소득소비-상권', 'gangnam_서울시 상권분석서비스(소득소비-상권).csv'),
        ('집객시설-상권', 'gangnam_서울시 상권분석서비스(집객시설-상권).csv'),
        ('길단위인구-상권', 'gangnam_서울시 상권분석서비스(길단위인구-상권).csv')
    ]

    print(f"\n[2/3] 데이터 로딩 시작 ({len(files_to_load)}개 파일)...")
    dataframes = {}
    
    for idx, (name, filename) in enumerate(files_to_load, 1):
        print(f"  [{idx}/{len(files_to_load)}] {name} 로딩 중...", end=' ', flush=True)
        try:
            df = load_csv_with_retry(data_path / filename)
            dataframes[name] = df
            print(f"OK ({len(df):,}행)")
            write_heartbeat(f"Loaded {name}: {len(df):,} rows")
        except Exception as e:
            print(f"실패: {e}")
            write_heartbeat(f"FAILED {name}: {e}")
            sys.exit(1)

    # 전처리
    print("\n[3/3] 기초 데이터 전처리 중...", end=' ', flush=True)
    for df in dataframes.values():
        if '기준_년_분기_코드' in df.columns:
            df['기준_년_분기_코드'] = df['기준_년_분기_코드'].astype(str)
            df['연도'] = df['기준_년_분기_코드'].str[:4].astype(int)
            df['분기'] = df['기준_년_분기_코드'].str[4:].astype(int)
    print("완료")

    return dataframes

if __name__ == "__main__":
    print("=" * 70)
    print("의원급 피부과 입지 분석 - 데이터 로딩 단계")
    print("=" * 70)
    dataframes = load_data()
    print("\n[NOTICE] 데이터 로딩이 완료되었습니다.")
    write_heartbeat("SUCCESS - 데이터 로딩 완료")
