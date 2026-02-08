# -*- coding: utf-8 -*-
"""
파일 인코딩 확인 및 변환 (chardet 없이)
"""

from pathlib import Path
import sys

file_path = Path(r'd:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\06_종합평가.py')

print(f"파일: {file_path.name}")
print("=" * 80)

# 여러 인코딩으로 시도
encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']

content = None
detected_encoding = None

for enc in encodings:
    try:
        with open(file_path, 'r', encoding=enc) as f:
            content = f.read()
        detected_encoding = enc
        print(f"[OK] 읽기 성공: {enc}")
        break
    except UnicodeDecodeError:
        print(f"[FAIL] 읽기 실패: {enc}")
        continue

if content is None:
    print("\n[ERROR] 모든 인코딩으로 읽기 실패!")
    sys.exit(1)

print(f"\n감지된 인코딩: {detected_encoding}")
print(f"파일 크기: {len(content)} 문자")

# UTF-8로 저장 (BOM 없이)
if detected_encoding != 'utf-8':
    backup_path = file_path.with_suffix('.py.backup')
    
    # 백업 생성
    import shutil
    shutil.copy2(file_path, backup_path)
    print(f"\n[OK] 백업 생성: {backup_path.name}")
    
    # UTF-8로 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] UTF-8로 변환 완료!")
    print(f"\n원본은 {backup_path.name}에 백업되었습니다.")
else:
    print("\n[INFO] 이미 UTF-8 인코딩입니다. 변환 불필요.")
