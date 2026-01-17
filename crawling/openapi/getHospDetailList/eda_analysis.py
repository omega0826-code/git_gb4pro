"""
병원 전체정보 데이터 EDA 분석 스크립트
================================================================================
작성일: 2026-01-17
목적: 병원전체정보_20260116_212603.csv 파일에 대한 탐색적 데이터 분석
================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# 파일 경로
INPUT_FILE = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260116_212603.csv"
OUTPUT_DIR = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\REPORT"

# 출력 파일명
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = Path(OUTPUT_DIR) / f"EDA_분석결과_{timestamp}.md"

print("="*80)
print("병원 전체정보 데이터 EDA 분석")
print("="*80)
print()

# ============================================================================
# 1. 데이터 로드
# ============================================================================
print("[1단계] 데이터 로드 중...")
df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
print(f"[완료] 데이터 로드 완료: {len(df)}건, {len(df.columns)}개 컬럼")
print()

# ============================================================================
# 2. 기본 정보 분석
# ============================================================================
print("[2단계] 기본 정보 분석 중...")

# 데이터 크기
total_records = len(df)
total_columns = len(df.columns)
memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024

# 컬럼 분류 (API별)
api_prefixes = {
    '원본': ['원본_'],
    'eqp': ['eqp_'],
    'dtl': ['dtl_'],
    'dgsbjt': ['dgsbjt_'],
    'trnsprt': ['trnsprt_'],
    'medoft': ['medoft_'],
    'foepaddc': ['foepaddc_'],
    'nursiggrd': ['nursiggrd_'],
    'spcldiag': ['spcldiag_'],
    'etchst': ['etchst_']
}

api_column_counts = {}
for api_name, prefixes in api_prefixes.items():
    count = sum(1 for col in df.columns if any(col.startswith(prefix) for prefix in prefixes))
    api_column_counts[api_name] = count

print(f"[완료] 기본 정보 분석 완료")
print()

# ============================================================================
# 3. 결측치 분석
# ============================================================================
print("[3단계] 결측치 분석 중...")

# 전체 결측치
total_missing = df.isnull().sum().sum()
total_cells = total_records * total_columns
missing_rate = (total_missing / total_cells) * 100

# 컬럼별 결측치
missing_by_column = df.isnull().sum()
missing_columns = missing_by_column[missing_by_column > 0].sort_values(ascending=False)

# API별 결측치
api_missing = {}
for api_name, prefixes in api_prefixes.items():
    api_cols = [col for col in df.columns if any(col.startswith(prefix) for prefix in prefixes)]
    if api_cols:
        api_df = df[api_cols]
        api_total_missing = api_df.isnull().sum().sum()
        api_total_cells = len(api_df) * len(api_cols)
        api_missing_rate = (api_total_missing / api_total_cells) * 100 if api_total_cells > 0 else 0
        api_missing[api_name] = {
            'total_missing': api_total_missing,
            'total_cells': api_total_cells,
            'missing_rate': api_missing_rate
        }

print(f"[완료] 결측치 분석 완료")
print()

# ============================================================================
# 4. API별 응답률 분석
# ============================================================================
print("[4단계] API별 응답률 분석 중...")

# 각 API별로 최소 1개 이상의 값이 있는 레코드 수 계산
api_response_rates = {}
for api_name, prefixes in api_prefixes.items():
    if api_name == '원본':
        continue
    api_cols = [col for col in df.columns if any(col.startswith(prefix) for prefix in prefixes)]
    if api_cols:
        # 해당 API의 모든 컬럼이 NaN이 아닌 레코드 수
        has_data = df[api_cols].notna().any(axis=1).sum()
        response_rate = (has_data / total_records) * 100
        api_response_rates[api_name] = {
            'records_with_data': has_data,
            'response_rate': response_rate
        }

print(f"[완료] API별 응답률 분석 완료")
print()

# ============================================================================
# 5. 주요 컬럼 통계 분석
# ============================================================================
print("[5단계] 주요 컬럼 통계 분석 중...")

# 숫자형 컬럼 통계
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_stats = {}

# 주요 숫자형 컬럼 선택
key_numeric_cols = [
    'eqp_stdSickbdCnt',  # 일반병상수
    'eqp_hghrSickbdCnt',  # 상급병상수
    'eqp_emymCnt',  # 응급실수
    'medoft_oftCnt',  # 의료장비수
    'nursiggrd_careGrd',  # 간호등급
]

for col in key_numeric_cols:
    if col in df.columns:
        # 숫자로 변환 시도 (문자열이 섞여 있을 수 있음)
        col_data = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(col_data) > 0:
            numeric_stats[col] = {
                'count': len(col_data),
                'mean': col_data.mean(),
                'std': col_data.std(),
                'min': col_data.min(),
                'max': col_data.max(),
                'median': col_data.median()
            }

print(f"[완료] 주요 컬럼 통계 분석 완료")
print()

# ============================================================================
# 6. 범주형 데이터 분석
# ============================================================================
print("[6단계] 범주형 데이터 분석 중...")

# 주요 범주형 컬럼
key_categorical_cols = [
    'eqp_clCdNm',  # 종별
    'eqp_sidoCdNm',  # 시도
    'eqp_sgguCdNm',  # 시군구
]

categorical_stats = {}
for col in key_categorical_cols:
    if col in df.columns:
        value_counts = df[col].value_counts()
        categorical_stats[col] = {
            'unique_count': len(value_counts),
            'top_5': value_counts.head(5).to_dict()
        }

print(f"[완료] 범주형 데이터 분석 완료")
print()

# ============================================================================
# 7. 마크다운 보고서 생성
# ============================================================================
print("[7단계] 마크다운 보고서 생성 중...")

md_content = f"""# 병원 전체정보 데이터 EDA 분석 보고서

**분석일시**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**데이터 파일**: `병원전체정보_20260116_212603.csv`  
**분석 도구**: Python pandas

---

## 📊 1. 데이터 개요

### 기본 정보
- **총 레코드 수**: {total_records:,}건
- **총 컬럼 수**: {total_columns}개
- **메모리 사용량**: {memory_usage:.2f} MB
- **전체 결측치**: {total_missing:,}개 ({missing_rate:.2f}%)

### API별 컬럼 수

| API | 컬럼 수 | 설명 |
|-----|---------|------|
"""

# API별 컬럼 수 테이블
api_descriptions = {
    '원본': '원본 데이터 (기관코드, 병원명, 주소)',
    'eqp': '시설정보 (병상수, 응급실 등)',
    'dtl': '세부정보 (진료시간, 주차정보 등)',
    'dgsbjt': '진료과목정보',
    'trnsprt': '교통정보',
    'medoft': '의료장비정보',
    'foepaddc': '식대가산정보',
    'nursiggrd': '간호등급정보',
    'spcldiag': '특수진료정보',
    'etchst': '기타인력수정보'
}

for api_name in ['원본', 'eqp', 'dtl', 'dgsbjt', 'trnsprt', 'medoft', 'foepaddc', 'nursiggrd', 'spcldiag', 'etchst']:
    count = api_column_counts.get(api_name, 0)
    desc = api_descriptions.get(api_name, '')
    md_content += f"| {api_name} | {count} | {desc} |\n"

md_content += """
---

## 📈 2. API별 응답률 분석

각 API별로 데이터가 존재하는 레코드의 비율을 분석했습니다.

| API | 데이터 존재 레코드 수 | 응답률 |
|-----|---------------------|--------|
"""

for api_name in ['eqp', 'dtl', 'dgsbjt', 'trnsprt', 'medoft', 'foepaddc', 'nursiggrd', 'spcldiag', 'etchst']:
    if api_name in api_response_rates:
        stats = api_response_rates[api_name]
        md_content += f"| {api_name} | {stats['records_with_data']:,}건 | {stats['response_rate']:.1f}% |\n"

md_content += """
### 분석 결과

"""

# 응답률 기준 분류
high_response = [api for api, stats in api_response_rates.items() if stats['response_rate'] >= 80]
medium_response = [api for api, stats in api_response_rates.items() if 50 <= stats['response_rate'] < 80]
low_response = [api for api, stats in api_response_rates.items() if stats['response_rate'] < 50]

if high_response:
    md_content += f"- **높은 응답률 (≥80%)**: {', '.join(high_response)}\n"
if medium_response:
    md_content += f"- **중간 응답률 (50-80%)**: {', '.join(medium_response)}\n"
if low_response:
    md_content += f"- **낮은 응답률 (<50%)**: {', '.join(low_response)}\n"

md_content += """
---

## 🔍 3. 결측치 분석

### API별 결측치 현황

| API | 결측치 수 | 전체 셀 수 | 결측률 |
|-----|----------|-----------|--------|
"""

for api_name in ['원본', 'eqp', 'dtl', 'dgsbjt', 'trnsprt', 'medoft', 'foepaddc', 'nursiggrd', 'spcldiag', 'etchst']:
    if api_name in api_missing:
        stats = api_missing[api_name]
        md_content += f"| {api_name} | {stats['total_missing']:,} | {stats['total_cells']:,} | {stats['missing_rate']:.1f}% |\n"

md_content += f"""
### 결측치가 많은 상위 10개 컬럼

| 순위 | 컬럼명 | 결측치 수 | 결측률 |
|------|--------|----------|--------|
"""

for idx, (col, count) in enumerate(missing_columns.head(10).items(), 1):
    missing_pct = (count / total_records) * 100
    md_content += f"| {idx} | `{col}` | {count:,} | {missing_pct:.1f}% |\n"

md_content += """
---

## 📊 4. 주요 컬럼 통계 분석

### 숫자형 컬럼 통계

"""

for col, stats in numeric_stats.items():
    md_content += f"""
#### {col}

| 통계량 | 값 |
|--------|-----|
| 데이터 수 | {stats['count']:,} |
| 평균 | {stats['mean']:.2f} |
| 표준편차 | {stats['std']:.2f} |
| 최솟값 | {stats['min']:.2f} |
| 중앙값 | {stats['median']:.2f} |
| 최댓값 | {stats['max']:.2f} |

"""

md_content += """
---

## 📋 5. 범주형 데이터 분석

"""

for col, stats in categorical_stats.items():
    md_content += f"""
### {col}

- **고유값 수**: {stats['unique_count']}개

**상위 5개 값**:

| 순위 | 값 | 건수 |
|------|-----|------|
"""
    for idx, (value, count) in enumerate(stats['top_5'].items(), 1):
        md_content += f"| {idx} | {value} | {count:,} |\n"
    
    md_content += "\n"

md_content += """
---

## 💡 6. 주요 발견사항 및 권장사항

### 주요 발견사항

"""

# 자동 발견사항 생성
findings = []

# 1. 응답률 관련
if low_response:
    findings.append(f"1. **낮은 응답률 API**: {', '.join(low_response)} API는 응답률이 50% 미만입니다. 이는 해당 정보를 제공하지 않는 병원이 많다는 것을 의미합니다.")

# 2. 결측치 관련
high_missing_cols = [col for col, count in missing_columns.items() if (count / total_records) > 0.5]
if high_missing_cols:
    findings.append(f"2. **높은 결측률 컬럼**: {len(high_missing_cols)}개 컬럼이 50% 이상의 결측률을 보입니다.")

# 3. 데이터 품질
if missing_rate < 30:
    findings.append(f"3. **전체 데이터 품질**: 전체 결측률이 {missing_rate:.1f}%로 양호한 편입니다.")
elif missing_rate > 50:
    findings.append(f"3. **전체 데이터 품질**: 전체 결측률이 {missing_rate:.1f}%로 높은 편입니다. 데이터 수집 과정을 검토해야 합니다.")

for idx, finding in enumerate(findings, 1):
    md_content += f"{finding}\n\n"

md_content += """
### 권장사항

1. **결측치 처리**: 분석 목적에 따라 결측치가 많은 컬럼은 제외하거나 대체값을 사용하는 것을 고려하세요.
2. **API 응답률 개선**: 응답률이 낮은 API의 경우, 해당 정보를 제공하는 병원만 대상으로 분석하는 것이 적절합니다.
3. **데이터 검증**: 숫자형 데이터의 이상치(outlier)를 확인하고 필요시 제거하세요.
4. **추가 분석**: 지역별, 종별별 분석을 통해 더 깊은 인사이트를 얻을 수 있습니다.

---

## 📝 부록: 전체 컬럼 목록

<details>
<summary>전체 {total_columns}개 컬럼 보기 (클릭하여 펼치기)</summary>

"""

for idx, col in enumerate(df.columns, 1):
    md_content += f"{idx}. `{col}`\n"

md_content += """
</details>

---

**보고서 생성일시**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**분석 도구**: Python pandas  
**데이터 파일**: `병원전체정보_20260116_212603.csv`
"""

# 파일 저장
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"[완료] 마크다운 보고서 생성 완료")
print(f"  저장 위치: {OUTPUT_FILE}")
print()

print("="*80)
print("EDA 분석 완료!")
print("="*80)
print()
print(f"보고서 파일: {OUTPUT_FILE}")
