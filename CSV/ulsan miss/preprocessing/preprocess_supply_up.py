# -*- coding: utf-8 -*-
"""
울산 산업별 구인인원 데이터 전처리 스크립트
전처리 계획서: preprecedd_ulsan industry.md (STEP 1~10)
"""

import pandas as pd
import os
import sys
from datetime import datetime

# ============================================================
# 경로 설정
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_FILE = os.path.join(BASE_DIR, 'raw_supply_up.csv')
MAPPING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'industry_mapping.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 로그 기록용
log_lines = []
def log(msg):
    print(msg)
    log_lines.append(msg)

log(f"[시작] 전처리 실행: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"원본 파일: {RAW_FILE}")

# ============================================================
# STEP 1: 데이터 로드 및 헤더 정리
# ============================================================
log("\n===== STEP 1: 데이터 로드 및 헤더 정리 =====")

df_raw = pd.read_csv(RAW_FILE, header=None, encoding='utf-8-sig')
log(f"원본 shape: {df_raw.shape}")

# 1행: 연월 라벨, 2행: 컬럼명 → 결합하여 컬럼명 생성
row_dates = df_raw.iloc[0].tolist()   # 연월 라벨
row_names = df_raw.iloc[1].tolist()   # 컬럼명

# 앞 3열: 시도, 산업_대분류, 학력
columns = ['시도', '산업_대분류', '학력']

# 4열부터: "YYYY년 MM월" → "YYYY-MM" 변환
for i in range(3, len(row_dates)):
    date_str = str(row_dates[i]).strip()
    if '년' in date_str and '월' in date_str:
        parts = date_str.replace('년', '').replace('월', '').split()
        if len(parts) == 2:
            col_name = f"{parts[0]}-{parts[1].zfill(2)}"
            columns.append(col_name)
        else:
            columns.append(f"col_{i}")
    else:
        columns.append(f"col_{i}")

# 데이터 행만 추출 (3행부터)
df = df_raw.iloc[2:].copy()
df.columns = columns
df = df.reset_index(drop=True)

month_columns = [c for c in columns if c not in ['시도', '산업_대분류', '학력']]
log(f"월별 컬럼 수: {len(month_columns)}")
log(f"데이터 행 수: {len(df)}")
log(f"월별 컬럼 예시: {month_columns[:3]} ... {month_columns[-3:]}")

# ============================================================
# STEP 2: 계층적 행 구조 해소 (Forward Fill)
# ============================================================
log("\n===== STEP 2: Forward Fill =====")

df['시도'] = df['시도'].replace('', pd.NA).ffill()
df['산업_대분류'] = df['산업_대분류'].replace('', pd.NA).ffill()
df['학력'] = df['학력'].replace('', pd.NA)

log(f"시도 고유값: {df['시도'].unique().tolist()}")
log(f"산업_대분류 고유값 수: {df['산업_대분류'].nunique()}")

# ============================================================
# STEP 3: 소계/총계 행 분리 및 제거
# ============================================================
log("\n===== STEP 3: 소계/총계 행 분리 및 제거 =====")

# 총계/울산 전체 행 식별
mask_total = df['시도'].isin(['총계', '울산 전체'])
# 산업별 소계 행 식별 ("전체" 포함)
mask_subtotal = df['산업_대분류'].str.contains('전체', na=False)

# 소계/총계 행 저장
df_subtotals = df[mask_total | mask_subtotal].copy()
log(f"소계/총계 행 수: {len(df_subtotals)}")

# 본 데이터에서 제거
df = df[~(mask_total | mask_subtotal)].copy()
df = df.reset_index(drop=True)
log(f"제거 후 데이터 행 수: {len(df)}")

# ============================================================
# STEP 4: 값 클렌징 — 천단위 쉼표 제거 및 숫자 변환
# ============================================================
log("\n===== STEP 4: 천단위 쉼표 제거 및 숫자 변환 =====")

for col in month_columns:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# 소계 데이터도 동일 처리
for col in month_columns:
    df_subtotals[col] = df_subtotals[col].astype(str).str.replace(',', '', regex=False).str.strip()
    df_subtotals[col] = pd.to_numeric(df_subtotals[col], errors='coerce').fillna(0).astype(int)

log(f"숫자 변환 완료 (컬럼 수: {len(month_columns)})")

# ============================================================
# STEP 5: 산업분류 체계 통합 (10차 → 11차 기준)
# ============================================================
log("\n===== STEP 5: 산업분류 체계 통합 =====")

# 매핑 테이블 로드
mapping_df = pd.read_csv(MAPPING_FILE, encoding='utf-8')
mapping_dict = dict(zip(mapping_df['원본_산업명'], mapping_df['통합_산업명']))

# 산업_대분류에서 "11차_" 또는 "10차_" 접두어 제거 후 매핑
# 먼저 원본 컬럼 보존
df['산업_대분류_원본'] = df['산업_대분류']

# 통합_산업명 매핑
df['통합_산업명'] = df['산업_대분류'].map(mapping_dict)

# 매핑 안 된 행 확인
unmapped = df[df['통합_산업명'].isna()]['산업_대분류'].unique()
if len(unmapped) > 0:
    log(f"[경고] 매핑 안 된 산업분류: {unmapped.tolist()}")
    # 매핑 안 된 값은 원본 그대로 사용
    df['통합_산업명'] = df['통합_산업명'].fillna(df['산업_대분류'])

# 분류체계 컬럼 추가
df['분류체계'] = df['산업_대분류'].apply(
    lambda x: '11차' if str(x).startswith('11차_') else ('10차' if str(x).startswith('10차_') else '기타')
)

log(f"통합_산업명 고유값 수: {df['통합_산업명'].nunique()}")
log(f"통합_산업명 목록:\n{df['통합_산업명'].unique().tolist()}")
log(f"분류체계 분포:\n{df['분류체계'].value_counts().to_string()}")

# ============================================================
# STEP 6: Wide → Long 변환
# ============================================================
log("\n===== STEP 6: Wide → Long 변환 =====")

id_vars = ['시도', '통합_산업명', '산업_대분류_원본', '학력', '분류체계']

df_long = df.melt(
    id_vars=id_vars,
    value_vars=month_columns,
    var_name='연월',
    value_name='구인인원'
)

log(f"Long 변환 후 shape: {df_long.shape}")

# ============================================================
# STEP 7: 날짜 파생 변수 생성
# ============================================================
log("\n===== STEP 7: 날짜 파생 변수 생성 =====")

df_long['연도'] = df_long['연월'].str[:4].astype(int)
df_long['월'] = df_long['연월'].str[5:7].astype(int)
df_long['분기'] = (df_long['월'] - 1) // 3 + 1
df_long['반기'] = df_long['월'].apply(lambda x: '상반기' if x <= 6 else '하반기')

log(f"연도 범위: {df_long['연도'].min()} ~ {df_long['연도'].max()}")
log(f"월 범위: {df_long['월'].min()} ~ {df_long['월'].max()}")

# ============================================================
# STEP 8: 연간 데이터(월별 합계) 생성
# ============================================================
log("\n===== STEP 8: 연간 데이터(월별 합계) 생성 =====")

df_annual = df_long.groupby(
    ['통합_산업명', '학력', '연도']
)['구인인원'].sum().reset_index()
df_annual.rename(columns={'구인인원': '연간데이터_월별합계'}, inplace=True)

df_long = df_long.merge(df_annual, on=['통합_산업명', '학력', '연도'], how='left')

log(f"연간데이터 예시 (제조업-학력무관):")
sample = df_annual[
    (df_annual['통합_산업명'].str.contains('제조업', na=False)) & 
    (df_annual['학력'] == '학력무관')
]
if len(sample) > 0:
    log(sample.to_string(index=False))

# ============================================================
# STEP 9: 학력 그룹핑
# ============================================================
log("\n===== STEP 9: 학력 그룹핑 =====")

education_group_map = {
    '초졸': '고졸이하',
    '중졸': '고졸이하',
    '고졸': '고졸이하',
    '전문대졸': '전문대졸',
    '대졸': '대졸',
    '대학원졸(석사)': '대학원졸',
    '대학원졸(박사)': '대학원졸',
    '학력무관': '학력무관',
    '분류불능': '기타',
}

df_long['학력_그룹'] = df_long['학력'].map(education_group_map).fillna('기타')

log(f"학력_그룹 분포:\n{df_long['학력_그룹'].value_counts().to_string()}")

# ============================================================
# STEP 10: 불필요 행 제거 및 최종 품질 검증
# ============================================================
log("\n===== STEP 10: 품질 검증 및 최종 정리 =====")

# 전값 행(all-zero) 제거: 해당 산업-학력 조합이 전 기간 0인 경우
zero_mask = df_long.groupby(['통합_산업명', '학력'])['구인인원'].transform('sum') == 0
zero_count = zero_mask.sum()
if zero_count > 0:
    zero_items = df_long[zero_mask][['통합_산업명', '학력']].drop_duplicates()
    log(f"전값 행(all-zero) 제거: {zero_count}행")
    log(f"  대상: {zero_items.values.tolist()}")
    df_long = df_long[~zero_mask].copy()

# 최종 컬럼 순서 정리
final_columns = [
    '시도', '통합_산업명', '산업_대분류_원본', '분류체계',
    '학력', '학력_그룹',
    '연월', '연도', '월', '분기', '반기',
    '구인인원', '연간데이터_월별합계'
]
df_long = df_long[final_columns]

log(f"\n최종 데이터 shape: {df_long.shape}")
log(f"컬럼 목록: {df_long.columns.tolist()}")
log(f"\n통합_산업명별 행 수:\n{df_long.groupby('통합_산업명').size().to_string()}")
log(f"\n연도별 행 수:\n{df_long.groupby('연도').size().to_string()}")

# ============================================================
# 산출물 저장
# ============================================================
log("\n===== 산출물 저장 =====")

# 1. 전처리 완료 데이터
output_path = os.path.join(OUTPUT_DIR, 'preprocessed_supply_up.csv')
df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
log(f"[저장] {output_path} ({len(df_long)}행)")

# 2. 소계/총계 검증용 데이터
subtotals_path = os.path.join(OUTPUT_DIR, 'supply_up_subtotals.csv')
df_subtotals.to_csv(subtotals_path, index=False, encoding='utf-8-sig')
log(f"[저장] {subtotals_path} ({len(df_subtotals)}행)")

# 3. 전처리 로그
log_path = os.path.join(OUTPUT_DIR, 'preprocess_log.txt')
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))
log(f"[저장] {log_path}")

log(f"\n[완료] 전처리 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
