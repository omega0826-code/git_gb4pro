# -*- coding: utf-8 -*-
"""
파일 인코딩 변환 스크립트
CP949 또는 기타 인코딩으로 저장된 파일을 UTF-8로 변환
"""

import chardet
from pathlib import Path

# 변환할 파일 경로
file_path = Path(r'd:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\06_종합평가.py')

# 1. 현재 인코딩 감지
print(f"파일: {file_path.name}")
print("=" * 80)

with open(file_path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    current_encoding = result['encoding']
    confidence = result['confidence']
    
print(f"현재 인코딩: {current_encoding} (신뢰도: {confidence:.2%})")

# 2. UTF-8로 변환
try:
    # 원본 파일 읽기 (감지된 인코딩 사용)
    with open(file_path, 'r', encoding=current_encoding) as f:
        content = f.read()
    
    # UTF-8로 저장 (백업 생성)
    backup_path = file_path.with_suffix('.py.bak')
    file_path.rename(backup_path)
    print(f"\n[OK] 백업 생성: {backup_path.name}")
    
    # UTF-8로 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] UTF-8로 변환 완료: {file_path.name}")
    print(f"\n변환 완료! 원본은 {backup_path.name}에 백업되었습니다.")
    
except Exception as e:
    print(f"\n[ERROR] 변환 실패: {e}")
    if backup_path.exists():
        backup_path.rename(file_path)
        print("[OK] 백업에서 복원했습니다.")
