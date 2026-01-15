"""
의료기관별상세정보 조회 API 호출 스크립트 (디버그 버전)
================================================================================
작성일: 2026-01-15
목적: API 응답 디버깅을 위한 테스트 스크립트
입력: 병원기본목록 CSV 파일 (암호화된 요양기호 포함)
출력: API 응답 상세 로그
================================================================================
"""

import requests
import json
from typing import Dict
import pandas as pd
from datetime import datetime
import time
import os
from pathlib import Path
from urllib.parse import quote
import base64

# ============================================================================
# 설정 (Configuration)
# ============================================================================

# API 기본 정보
API_BASE_URL = "http://apis.data.go.kr/B551182/MadmDtlInfoService2.7/getDtlInfo2.7"

# 인증키 설정
SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="

# API 키 타입 설정
USE_ENCODED_KEY = False

# 타임아웃 설정
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 60

# 입력 파일 설정
INPUT_CSV_FILE = r"D:\git_gb4pro\crawling\openapi\getHospDetailList\data\서울_강남구_피부과_20260115_212757.csv"

# 테스트 건수 (처음 몇 건만 테스트)
TEST_COUNT = 5

# ============================================================================
# API 호출 함수
# ============================================================================

def test_api_call(service_key: str, use_encoded_key: bool, ykiho: str, index: int) -> None:
    """
    API 호출 테스트 및 상세 로그 출력
    """
    
    print(f"\n{'='*80}")
    print(f"테스트 #{index + 1}")
    print(f"{'='*80}")
    print(f"요양기호 (원본): {ykiho}")
    print(f"요양기호 길이: {len(ykiho)}")
    
    # Base64 디코딩 시도
    try:
        decoded = base64.b64decode(ykiho).decode('utf-8')
        print(f"Base64 디코딩 결과: {decoded}")
    except Exception as e:
        print(f"Base64 디코딩 실패: {e}")
    
    # 요청 파라미터 구성
    params = {
        'ykiho': ykiho,
        '_type': 'json'
    }
    
    # API 키 처리
    if use_encoded_key:
        encoded_key = quote(service_key, safe='')
        api_url = f"{API_BASE_URL}?ServiceKey={encoded_key}"
    else:
        api_url = API_BASE_URL
        params['ServiceKey'] = service_key
    
    print(f"\nAPI URL: {api_url}")
    print(f"파라미터: {json.dumps(params, ensure_ascii=False, indent=2)}")
    
    try:
        # API 호출
        print(f"\nAPI 호출 중...")
        response = requests.get(
            api_url, 
            params=params, 
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        
        print(f"HTTP 상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        
        # 응답 내용 출력
        print(f"\n응답 내용 (텍스트):")
        print(response.text[:1000])  # 처음 1000자만 출력
        
        # JSON 파싱 시도
        try:
            data = response.json()
            print(f"\nJSON 파싱 성공:")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])  # 처음 2000자만
            
            # 응답 구조 분석
            if 'response' in data:
                header = data['response'].get('header', {})
                body = data['response'].get('body', {})
                
                print(f"\n응답 헤더:")
                print(f"  - resultCode: {header.get('resultCode')}")
                print(f"  - resultMsg: {header.get('resultMsg')}")
                
                print(f"\n응답 바디:")
                print(f"  - items 타입: {type(body.get('items'))}")
                print(f"  - items 값: {body.get('items')}")
                
                if body.get('items'):
                    items = body['items']
                    if isinstance(items, dict):
                        print(f"  - item 타입: {type(items.get('item'))}")
                        print(f"  - item 값: {items.get('item')}")
                
        except json.JSONDecodeError as e:
            print(f"\nJSON 파싱 실패: {e}")
        
    except requests.exceptions.Timeout as e:
        print(f"\n타임아웃 오류: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"\n연결 오류: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"\nHTTP 오류: {e}")
    except Exception as e:
        print(f"\n예상치 못한 오류: {e}")
    
    print(f"\n{'='*80}\n")
    time.sleep(1)  # API 호출 간격


def main():
    """
    메인 실행 함수
    """
    
    print("="*80)
    print("의료기관별상세정보 조회 API 디버그 테스트")
    print("="*80)
    print()
    
    # CSV 파일 읽기
    print(f"[CSV 읽기] {INPUT_CSV_FILE}")
    
    encodings = ['utf-8-sig', 'cp949', 'utf-8', 'euc-kr']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(INPUT_CSV_FILE, encoding=encoding)
            print(f"  - 인코딩: {encoding} (성공)")
            break
        except Exception as e:
            continue
    
    if df is None:
        print("[오류] CSV 파일을 읽을 수 없습니다.")
        return
    
    print(f"  - 총 {len(df)}건")
    print(f"  - 컬럼: {', '.join(df.columns.tolist())}")
    
    # 요양기호 컬럼 찾기
    ykiho_column = None
    possible_columns = ['ykiho', '암호화요양기호', '요양기호', 'YKIHO', 'ykiho_enc']
    
    for col in possible_columns:
        if col in df.columns:
            ykiho_column = col
            print(f"  - 요양기호 컬럼: {ykiho_column}")
            break
    
    if ykiho_column is None:
        print(f"[오류] 요양기호 컬럼을 찾을 수 없습니다.")
        print(f"사용 가능한 컬럼: {df.columns.tolist()}")
        return
    
    # 처음 몇 건만 테스트
    test_count = min(TEST_COUNT, len(df))
    print(f"\n처음 {test_count}건 테스트 시작...\n")
    
    for idx in range(test_count):
        row = df.iloc[idx]
        ykiho = row[ykiho_column]
        
        if pd.isna(ykiho) or str(ykiho).strip() == '':
            print(f"[건너뜀] 인덱스 {idx}: 요양기호가 비어있습니다.")
            continue
        
        test_api_call(SERVICE_KEY, USE_ENCODED_KEY, ykiho, idx)
    
    print("\n테스트 완료!")


if __name__ == "__main__":
    main()
