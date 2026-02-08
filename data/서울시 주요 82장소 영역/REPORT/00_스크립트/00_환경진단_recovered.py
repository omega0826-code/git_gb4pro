# -*- coding: utf-8 -*-
"""
?원?????? 분석 - ?경 진단 ?크립트
?성?? 2026-02-03
버전: 1.0
?명: ?행 ???수 ?경??검증하??무한 로딩 ??류??전??방??니??
"""

import sys
import os
from datetime import datetime
from pathlib import Path

print("=" * 80)
print("? ?경 진단 ?크립트 ?행 ?..")
print("=" * 80)
print(f"진단 ?작 ?간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# 진단 결과 ???
results = []
errors = []
warnings = []

# ============================================================================
# 1. Python 버전 ?인
# ============================================================================
print("[1/5] Python 버전 ?인...", end=' ', flush=True)
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"??Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    results.append(f"??Python 버전: {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"??Python {python_version.major}.{python_version.minor}.{python_version.micro} (3.8 ?상 ?요)")
    errors.append(f"??Python 버전 부? {python_version.major}.{python_version.minor}.{python_version.micro} (3.8 ?상 ?요)")

# ============================================================================
# 2. ?수 ?이브러??인
# ============================================================================
print("[2/5] ?수 ?이브러??인...", flush=True)

required_libraries = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
}

optional_libraries = {
    'koreanize_matplotlib': 'koreanize_matplotlib',
    'psutil': 'psutil',
}

missing_required = []
missing_optional = []

for name, import_name in required_libraries.items():
    try:
        __import__(import_name)
        print(f"  ??{name:25s} ?치??, flush=True)
        results.append(f"  ??{name} ?치??)
    except ImportError:
        print(f"  ??{name:25s} 미설?, flush=True)
        missing_required.append(name)
        errors.append(f"  ??{name} 미설?(?수)")

for name, import_name in optional_libraries.items():
    try:
        __import__(import_name)
        print(f"  ??{name:25s} ?치??(?택)", flush=True)
        results.append(f"  ??{name} ?치??(?택)")
    except ImportError:
        print(f"  ??{name:25s} 미설?(?택)", flush=True)
        missing_optional.append(name)
        warnings.append(f"  ??{name} 미설?(?택?항)")

# ============================================================================
# 3. 메모??인
# ============================================================================
print("\n[3/5] ?스??메모??인...", end=' ', flush=True)
try:
    import psutil
    memory = psutil.virtual_memory()
    available_gb = memory.available / (1024 ** 3)
    total_gb = memory.total / (1024 ** 3)
    
    if available_gb >= 4.0:
        print(f"???용 가?? {available_gb:.1f}GB / {total_gb:.1f}GB")
        results.append(f"??메모? {available_gb:.1f}GB ?용 가??)
    elif available_gb >= 2.0:
        print(f"???용 가?? {available_gb:.1f}GB / {total_gb:.1f}GB (4GB ?상 권장)")
        warnings.append(f"??메모? {available_gb:.1f}GB (4GB ?상 권장)")
    else:
        print(f"???용 가?? {available_gb:.1f}GB / {total_gb:.1f}GB (부?")
        errors.append(f"??메모?부? {available_gb:.1f}GB (최소 2GB ?요)")
except ImportError:
    print("??psutil 미설치로 ?인 불? (?택?항)")
    warnings.append("??메모??인 불? (psutil 미설?")

# ============================================================================
# 4. ?이???일 ?인
# ============================================================================
print("\n[4/5] ?이???일 ?인...", flush=True)

data_path = Path('d:/git_gb4pro/data/?울??주요 82?소 ?역/Gangnam_CSV_20260203_094620/')

if not data_path.exists():
    print(f"  ???이???렉?리 ?음: {data_path}")
    errors.append(f"  ???이???렉?리 ?음: {data_path}")
else:
    required_files = [
        'gangnam_?울???권분석?비???역-?권).csv',
        'gangnam_?울???권분석?비???포-?권)_2022??1분기~2024??4분기.csv',
        'gangnam_?울???권분석?비??추정매출-?권)__2022??1분기~2024??4분기.csv',
        'gangnam_?울???권분석?비???주?구-?권).csv',
        'gangnam_?울???권분석?비??직장?구-?권).csv',
        'gangnam_?울???권분석?비???득?비-?권).csv',
        'gangnam_?울???권분석?비??집객?설-?권).csv',
        'gangnam_?울???권분석?비??길단?인??권).csv'
    ]
    
    total_size = 0
    missing_files = []
    
    for filename in required_files:
        file_path = data_path / filename
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 ** 2)
            total_size += size_mb
            print(f"  ??{filename[:30]:30s}... ({size_mb:.1f}MB)", flush=True)
            results.append(f"  ??{filename} ({size_mb:.1f}MB)")
        else:
            print(f"  ??{filename[:30]:30s}... (?음)", flush=True)
            missing_files.append(filename)
            errors.append(f"  ???일 ?음: {filename}")
    
    if not missing_files:
        print(f"\n  ??이???기: {total_size:.1f}MB")
        results.append(f"  ??이???기: {total_size:.1f}MB")

# ============================================================================
# 5. ?스??공간 ?인
# ============================================================================
print("\n[5/5] ?스??공간 ?인...", end=' ', flush=True)
try:
    import psutil
    output_path = Path('d:/git_gb4pro/data/?울??주요 82?소 ?역/REPORT/')
    disk_usage = psutil.disk_usage(str(output_path))
    free_gb = disk_usage.free / (1024 ** 3)
    
    if free_gb >= 1.0:
        print(f"???유 공간: {free_gb:.1f}GB")
        results.append(f"???스???유 공간: {free_gb:.1f}GB")
    else:
        print(f"???유 공간: {free_gb:.1f}GB (1GB ?상 권장)")
        warnings.append(f"???스??공간: {free_gb:.1f}GB (1GB ?상 권장)")
except ImportError:
    print("??psutil 미설치로 ?인 불?")
    warnings.append("???스??공간 ?인 불? (psutil 미설?")

# ============================================================================
# 진단 결과 ?약
# ============================================================================
print("\n" + "=" * 80)
print("? 진단 결과 ?약")
print("=" * 80)

if not errors:
    print("??모든 ?수 ?? ?과! ?크립트 ?행 가?합?다.\n")
else:
    print(f"??{len(errors)}개의 ?류 발견! ?래 문제??결?야 ?니??\n")
    for error in errors:
        print(error)

if warnings:
    print(f"\n?️  {len(warnings)}개의 경고 ?항:\n")
    for warning in warnings:
        print(warning)

# ============================================================================
# ?결 방법 ?내
# ============================================================================
if missing_required:
    print("\n" + "=" * 80)
    print("? ?수 ?이브러??치 방법")
    print("=" * 80)
    print("?음 명령?? ?행?세??\n")
    print(f"pip install {' '.join(missing_required)}")

if missing_optional:
    print("\n" + "=" * 80)
    print("? ?택 ?이브러??치 방법 (권장)")
    print("=" * 80)
    print("?음 명령?? ?행?세??\n")
    print(f"pip install {' '.join(missing_optional)}")

# ============================================================================
# 결과 ?일 ???
# ============================================================================
output_file = Path('d:/git_gb4pro/data/?울??주요 82?소 ?역/REPORT/?경진단_결과.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("?경 진단 결과\n")
    f.write("=" * 80 + "\n")
    f.write(f"진단 ?간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("???과 ??:\n")
    for result in results:
        f.write(result + "\n")
    
    if warnings:
        f.write("\n?️  경고 ??:\n")
        for warning in warnings:
            f.write(warning + "\n")
    
    if errors:
        f.write("\n???류 ??:\n")
        for error in errors:
            f.write(error + "\n")
    
    if missing_required:
        f.write("\n?수 ?이브러??치 명령:\n")
        f.write(f"pip install {' '.join(missing_required)}\n")
    
    if missing_optional:
        f.write("\n?택 ?이브러??치 명령:\n")
        f.write(f"pip install {' '.join(missing_optional)}\n")

print(f"\n? 진단 결과가 ??되?습?다: {output_file}")
print("=" * 80)

# 종료 코드 반환
sys.exit(0 if not errors else 1)
