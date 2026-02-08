# -*- coding: utf-8 -*-
import os

files = ['00_환경진단.py', '01_데이터로딩.py', '04_인구유동분석.py']

for f in files:
    if os.path.exists(f):
        print(f"--- {f} ---")
        try:
            with open(f, 'rb') as fin:
                data = fin.read(100)
                print(data)
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        # Try finding it with partial match
        print(f"{f} does not exist directly. Listing similar files:")
        for real_f in os.listdir('.'):
            if real_f.startswith(f[:3]):
                print(f"Match found: {real_f}")
