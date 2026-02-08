
import os

files_to_convert = [
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\00_환경진단.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\01_데이터로딩.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\02_경쟁환경분석.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\03_고객분석.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\04_인구유동분석.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\05_입지조건분석.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\06_종합평가.py",
    r"d:\git_gb4pro\data\서울시 주요 82장소 영역\REPORT\00_스크립트\99_전체실행.py"
]

def convert_to_utf8(file_path):
    try:
        # Try reading with cp949
        with open(file_path, 'r', encoding='cp949') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            # Try reading with utf-8
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Failed to decode {file_path}")
            return

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Converted {file_path} to UTF-8")

for file_path in files_to_convert:
    if os.path.exists(file_path):
        convert_to_utf8(file_path)
    else:
        print(f"File not found: {file_path}")
