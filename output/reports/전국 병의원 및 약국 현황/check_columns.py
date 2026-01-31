import pandas as pd

df = pd.read_csv('d:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/data_260131_0844/서울_병원_통합_2025.12.csv', encoding='utf-8-sig')

print("컬럼 목록:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

print(f"\n진료과목 관련 컬럼:")
dept_cols = [col for col in df.columns if '진료과목' in col or '과목' in col or 'subject' in col.lower()]
for col in dept_cols:
    print(f"  - {col}")
    print(f"    샘플 데이터: {df[col].dropna().head(3).tolist()}")
