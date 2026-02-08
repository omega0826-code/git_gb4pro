# -*- coding: utf-8 -*-
"""
스크립트 파일 일괄 수정 도구
CP949 인코딩 문제를 일으키는 이모지와 특수문자를 제거합니다.
"""

import os
import re
from pathlib import Path

# 수정할 스크립트 디렉토리
script_dir = Path(r'd:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트')

# 이모지 및 특수문자 매핑
replacements = {
    '🏥': '[의료]',
    '📂': '[폴더]',
    '🔍': '[검색]',
    '✅': '[OK]',
    '❌': '[X]',
    '⚠️': '[경고]',
    '💡': '[팁]',
    '🎉': '[완료]',
    '▶': '>',
    '✓': '[OK]',
    '🔧': '[도구]',
    '🔄': '[재시도]',
    '💓': '[하트비트]',
    '📊': '[차트]',
    '🚀': '[실행]',
    '🎯': '[목표]',
    '⭐': '[중요]',
    '🎨': '[디자인]',
    '📝': '[문서]',
}

def clean_file(file_path):
    """파일에서 이모지 제거"""
    try:
        # 여러 인코딩으로 시도
        content = None
        detected_encoding = None
        
        for enc in ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                detected_encoding = enc
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"[SKIP] {file_path.name} - 읽기 실패")
            return False
        
        # 이모지 및 특수문자 교체
        original_content = content
        for emoji, replacement in replacements.items():
            content = content.replace(emoji, replacement)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            # 백업 생성
            backup_path = file_path.with_suffix('.py.bak')
            if not backup_path.exists():
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
            
            # UTF-8로 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[OK] {file_path.name} - 수정 완료 (백업: {backup_path.name})")
            return True
        else:
            print(f"[SKIP] {file_path.name} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"[ERROR] {file_path.name} - {e}")
        return False

# 메인 실행
print("=" * 80)
print("스크립트 파일 일괄 수정 도구")
print("=" * 80)
print()

# 모든 .py 파일 처리
py_files = list(script_dir.glob('*.py'))
py_files = [f for f in py_files if not f.name.endswith('.bak') and f.name not in ['fix_all_scripts.py']]

print(f"처리할 파일 개수: {len(py_files)}")
print()

modified_count = 0
for py_file in py_files:
    if clean_file(py_file):
        modified_count += 1

print()
print("=" * 80)
print(f"완료! 수정된 파일: {modified_count}/{len(py_files)}")
print("=" * 80)
