import pandas as pd
import json

# 데이터 로드
df = pd.read_csv(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260116_212603.csv')

total_count = len(df)
print(f"총 데이터 건수: {total_count}")

# 모든 컬럼에 대한 결측치 정보 수집
missing_info = {}
for col in df.columns:
    missing_count = df[col].isnull().sum()
    missing_pct = (missing_count / total_count * 100)
    missing_info[col] = {
        'total': total_count,
        'missing': int(missing_count),
        'pct': round(missing_pct, 2)
    }

# JSON으로 저장
with open(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\missing value\missing_stats.json', 'w', encoding='utf-8') as f:
    json.dump(missing_info, f, ensure_ascii=False, indent=2)

print("\n결측치 정보가 missing_stats.json에 저장되었습니다.")

# 주요 컬럼 출력 (확인용)
print("\n=== 주요 컬럼 결측치 정보 ===")
for col in sorted(df.columns)[:20]:
    info = missing_info[col]
    print(f"{col}: {info['missing']}건 ({info['pct']}%)")
