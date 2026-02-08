# -*- coding: utf-8 -*-
import os

files = [
    '01_데이터로딩.py',
    '02_경쟁환경분석.py',
    '03_고객분석.py',
    '04_인구유동분석.py',
    '05_입지조건분석.py',
    '06_종합평가.py',
    '07_리포트생성.py',
    '99_전체실행.py'
]

for f in files:
    if os.path.exists(f):
        recovered_name = f.replace('.py', '_recovered.py')
        print(f"[*] Recovering {f} -> {recovered_name}")
        try:
            with open(f, 'rb') as fin:
                data = fin.read()
                # Try decoding with ignore to get the text part
                text = data.decode('utf-8', errors='ignore')
                
                with open(recovered_name, 'w', encoding='utf-8') as fout:
                    fout.write(text)
                print(f"[OK] Saved {recovered_name}")
        except Exception as e:
            print(f"[ERROR] Failed to recover {f}: {e}")
