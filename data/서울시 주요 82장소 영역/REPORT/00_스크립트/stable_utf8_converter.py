# -*- coding: utf-8 -*-
import os

def convert_to_utf8(filename):
    if not os.path.exists(filename):
        print(f"[SKIP] File not found: {filename}")
        return

    # Try encodings sequentially
    encodings = ['utf-8-sig', 'cp949', 'utf-8']
    content = None
    
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                content = f.read()
            print(f"[*] Decoded {filename} using {enc}")
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        print(f"[ERROR] Failed to decode {filename} with any encoding")
        return

    # Write as UTF-8 (without BOM for consistency)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Converted {filename} to UTF-8")

    # Write as UTF-8
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Converted {filename} to UTF-8")

def main():
    # Process ALL .py files in the current directory
    files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'stable_utf8_converter.py']
    
    print(f"[*] Found {len(files)} python files to check")
    for f in files:
        convert_to_utf8(f)

if __name__ == "__main__":
    main()
