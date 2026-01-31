"""
HIRA + 강남언니 데이터 결합 스크립트
작성일: 2026-01-31
"""

import pandas as pd
import re
import logging
from datetime import datetime
import os

# ============================================================================
# 1. 로그 설정
# ============================================================================

# 타임스탬프 생성
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
date_str = datetime.now().strftime('%Y%m%d')

# reports 폴더 생성 (하위폴더 없이)
os.makedirs('reports', exist_ok=True)

# 로그 파일 설정 (reports 폴더에 직접 저장)
log_file = f'reports/merge_log_{timestamp}.txt'

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.info("=== HIRA + 강남언니 데이터 결합 시작 ===\n")

# ============================================================================
# 2. 데이터 로드
# ============================================================================

logging.info("데이터 로드 시작")

# HIRA 데이터
hira_file = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/data_260131_0844/서울_병원_통합_2025.12.csv'
df_hira = pd.read_csv(hira_file, encoding='utf-8-sig')
logging.info(f"HIRA 데이터 로드 완료: {len(df_hira):,}행 × {len(df_hira.columns)}열")

# 강남언니 데이터
gangnam_file = 'd:/git_gb4pro/crawling/gangnam/data/processed/gangnam_hospitals_final_20260105_065921_update_v1.0.csv'
df_gangnam = pd.read_csv(gangnam_file, encoding='utf-8-sig')
logging.info(f"강남언니 데이터 로드 완료: {len(df_gangnam):,}행 × {len(df_gangnam.columns)}열\n")

# ============================================================================
# 3. 병원명 정제 함수
# ============================================================================

def normalize_hospital_name(name):
    """병원명 정제"""
    if pd.isna(name):
        return ""
    
    name = str(name).strip()
    
    # 법인 표기 제거
    name = re.sub(r'\(주\)|\(의\)|\(재\)|\(사\)', '', name)
    
    # 공백 제거
    name = re.sub(r'\s+', '', name)
    
    # 특수문자 제거 (한글, 영문, 숫자만 유지)
    name = re.sub(r'[^\w가-힣]', '', name)
    
    # 의원/병원 통일
    name = re.sub(r'의원$', '', name)
    name = re.sub(r'병원$', '', name)
    
    return name

logging.info("병원명 정제 시작")

df_hira['병원명_정제'] = df_hira['요양기관명'].apply(normalize_hospital_name)
df_gangnam['병원명_정제'] = df_gangnam['hospital_name'].apply(normalize_hospital_name)

logging.info("병원명 정제 완료\n")

# ============================================================================
# 4. 데이터 결합 (Left Join)
# ============================================================================

logging.info("매칭 시작")

# 완전 일치 매칭
df_merged = df_hira.merge(
    df_gangnam,
    left_on='병원명_정제',
    right_on='병원명_정제',
    how='left',
    suffixes=('', '_강남언니'),
    indicator=True
)

# 매칭 결과 확인
matched_count = (df_merged['_merge'] == 'both').sum()
match_rate = matched_count / len(df_hira) * 100

logging.info(f"완전 일치 매칭 완료: {matched_count:,}개 ({match_rate:.1f}%)")

# ============================================================================
# 5. 생성 컬럼 추가
# ============================================================================

logging.info("생성 컬럼 추가 시작")

# 강남언니 등록 플래그
df_merged['강남언니_등록'] = df_merged['_merge'] == 'both'

# 매칭 유형
df_merged['매칭_유형'] = df_merged.apply(
    lambda row: 'exact' if row['_merge'] == 'both' else None,
    axis=1
)

# 매칭 신뢰도 (완전 일치는 100)
df_merged['매칭_신뢰도'] = df_merged.apply(
    lambda row: 100.0 if row['_merge'] == 'both' else None,
    axis=1
)

# _merge 컬럼 제거
df_merged = df_merged.drop('_merge', axis=1)

logging.info("생성 컬럼 추가 완료\n")

# ============================================================================
# 6. 결측치 처리
# ============================================================================

logging.info("결측치 처리 시작")

# 처리 전 결측치 수
missing_before = df_merged.isnull().sum().sum()

# 강남언니 관련 컬럼 (미등록 병원)
gangnam_cols = ['rating', 'review_count', 'event_count']

for col in gangnam_cols:
    if col in df_merged.columns:
        df_merged.loc[df_merged['강남언니_등록'] == False, col] = 0

# 텍스트 컬럼
text_cols = ['treatment_tags', 'doctors', 'introduction']
for col in text_cols:
    if col in df_merged.columns:
        df_merged.loc[df_merged['강남언니_등록'] == False, col] = '정보없음'

# 처리 후 결측치 수
missing_after = df_merged.isnull().sum().sum()
processed = missing_before - missing_after
process_rate = (processed / missing_before * 100) if missing_before > 0 else 0

logging.info(f"결측치 처리 완료: {processed:,}개 처리 ({process_rate:.1f}%)\n")

# ============================================================================
# 7. 데이터 저장
# ============================================================================

logging.info("데이터 저장 시작")

# 폴더 생성
os.makedirs('merged', exist_ok=True)
os.makedirs('merged/archive', exist_ok=True)

# 타임스탬프 버전 저장
output_file = f'merged/HIRA_강남언니_결합_{timestamp}.csv'
df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
logging.info(f"저장 완료: {output_file}")

# 최종 버전 저장
final_file = 'merged/HIRA_강남언니_결합_최종.csv'
df_merged.to_csv(final_file, index=False, encoding='utf-8-sig')
logging.info(f"최종 버전 저장: {final_file}\n")

# ============================================================================
# 8. 데이터 검증
# ============================================================================

logging.info("검증 시작")

# 8.1 매칭 품질 검증
total = len(df_merged)
matched = df_merged['강남언니_등록'].sum()
match_rate = matched / total * 100

logging.info(f"매칭 품질 검증:")
logging.info(f"  - 매칭률: {match_rate:.1f}% ({matched:,}/{total:,})")

if 50 <= match_rate <= 90:
    logging.info("  - 매칭률: ✅ 정상 범위")
else:
    logging.warning(f"  - 매칭률: ⚠️ 비정상 ({match_rate:.1f}%)")

# 8.2 데이터 일관성 검증
expected_rows = len(df_hira)
actual_rows = len(df_merged)

if expected_rows == actual_rows:
    logging.info(f"데이터 일관성 검증: ✅ 통과 ({actual_rows:,}행)")
else:
    logging.error(f"데이터 일관성 검증: ❌ 실패 (예상: {expected_rows:,}, 실제: {actual_rows:,})")

# 8.3 중복 확인
duplicates = df_merged['암호화요양기호'].duplicated().sum()
if duplicates == 0:
    logging.info(f"중복 확인: ✅ 중복 없음")
else:
    logging.warning(f"중복 확인: ⚠️ {duplicates}건 발견")

logging.info("")

# ============================================================================
# 9. 통계 리포트 생성
# ============================================================================

logging.info("통계 리포트 생성 시작")

os.makedirs('reports', exist_ok=True)

report_file = f'reports/결합_통계_리포트_{date_str}.md'

with open(report_file, 'w', encoding='utf-8') as f:
    f.write("# HIRA + 강남언니 데이터 결합 통계 리포트\n\n")
    f.write(f"> **작성일**: {datetime.now().strftime('%Y-%m-%d')}  \n")
    f.write("> **데이터 기준일**: 2025년 12월  \n\n")
    
    f.write("## 1. 결합 개요\n\n")
    f.write(f"- **HIRA 총 병원 수**: {total:,}개\n")
    f.write(f"- **강남언니 등록 병원**: {matched:,}개 ({match_rate:.1f}%)\n")
    f.write(f"- **미등록 병원**: {total - matched:,}개 ({100 - match_rate:.1f}%)\n\n")
    
    f.write("## 2. 매칭 결과\n\n")
    f.write("### 2.1 매칭 유형별 분포\n")
    f.write(f"- 완전 일치 (exact): {matched:,}개 (100%)\n\n")
    
    f.write("## 3. 지역별 분석\n\n")
    district_stats = df_merged.groupby('시군구코드명').agg({
        '강남언니_등록': ['count', 'sum']
    }).reset_index()
    district_stats.columns = ['구', '전체', '등록']
    district_stats['등록률'] = (district_stats['등록'] / district_stats['전체'] * 100).round(1)
    district_stats = district_stats.sort_values('등록률', ascending=False).head(10)
    
    f.write("| 구 | 전체 병원 | 등록 병원 | 등록률(%) |\n")
    f.write("|----|----------|----------|----------|\n")
    for _, row in district_stats.iterrows():
        f.write(f"| {row['구']} | {row['전체']:,} | {row['등록']:,} | {row['등록률']:.1f} |\n")
    
    f.write("\n## 4. 종별 분석\n\n")
    type_stats = df_merged.groupby('종별코드명').agg({
        '강남언니_등록': ['count', 'sum']
    }).reset_index()
    type_stats.columns = ['종별', '전체', '등록']
    type_stats['등록률'] = (type_stats['등록'] / type_stats['전체'] * 100).round(1)
    type_stats = type_stats.sort_values('등록률', ascending=False)
    
    f.write("| 종별 | 전체 | 등록 | 등록률(%) |\n")
    f.write("|------|------|------|----------|\n")
    for _, row in type_stats.iterrows():
        f.write(f"| {row['종별']} | {row['전체']:,} | {row['등록']:,} | {row['등록률']:.1f} |\n")

logging.info(f"통계 리포트 생성 완료: {report_file}\n")

# ============================================================================
# 10. 작업 완료
# ============================================================================

end_time = datetime.now()
logging.info(f"종료 시간: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
logging.info("\n=== 작업 완료 ===")

print(f"\n{'='*60}")
print(f"[완료] HIRA + 강남언니 데이터 결합 완료!")
print(f"{'='*60}")
print(f"\n[산출물]:")
print(f"  1. 결합 데이터: {output_file}")
print(f"  2. 최종 버전: {final_file}")
print(f"  3. 통계 리포트: {report_file}")
print(f"  4. 실행 로그: {log_file}")
print(f"\n[결과]:")
print(f"  - HIRA 총 병원: {total:,}개")
print(f"  - 강남언니 등록: {matched:,}개 ({match_rate:.1f}%)")
print(f"  - 미등록: {total - matched:,}개")
print(f"\n{'='*60}\n")
