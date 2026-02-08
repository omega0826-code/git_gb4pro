# -*- coding: utf-8 -*-
"""
의원급 피부과 입지 분석 - 데이터 로딩 및 초기 설정
작성일: 2026-02-04
버전: 5.03 (Date Logic Fix)
"""

import pandas as pd
import numpy as np
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# 인코딩 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except: pass

BASE_DIR = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
REPORT_DIR = BASE_DIR / 'REPORT'
HEARTBEAT_FILE = REPORT_DIR / 'heartbeat.txt'

def write_heartbeat(message):
    try:
        with open(HEARTBEAT_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    except: pass

REPORT_DIR.mkdir(parents=True, exist_ok=True)
with open(HEARTBEAT_FILE, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\nExecution Log\n" + "=" * 80 + "\n")

def load_data():
    data_path = BASE_DIR / 'Gangnam_9_Areas'
    dirs = ['01_경쟁환경분석', '02_고객분석', '03_인구유동분석', '04_입지조건분석', '05_종합평가', '06_최종리포트']
    for d in dirs: (REPORT_DIR / d).mkdir(parents=True, exist_ok=True)

    files = [
        ('영역-상권', 'gangnam_서울시 상권분석서비스(영역-상권).csv'),
        ('점포-상권', 'gangnam_서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv'),
        ('추정매출-상권', 'gangnam_서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv'),
        ('상주인구-상권', 'gangnam_서울시 상권분석서비스(상주인구-상권).csv'),
        ('직장인구-상권', 'gangnam_서울시 상권분석서비스(직장인구-상권).csv'),
        ('집객시설-상권', 'gangnam_서울시 상권분석서비스(집객시설-상권).csv')
    ]

    print(f"\n[1/2] 데이터 로딩 중...")
    dataframes = {}
    for name, filename in files:
        try:
            df = pd.read_csv(data_path / filename, encoding='utf-8-sig')
            dataframes[name] = df
            print(f"  - {name} OK")
        except Exception as e:
            print(f"  - {name} FAILED: {e}")
    return dataframes

if __name__ == "__main__":
    load_data()
    write_heartbeat("SUCCESS - 데이터 로딩 완료")
