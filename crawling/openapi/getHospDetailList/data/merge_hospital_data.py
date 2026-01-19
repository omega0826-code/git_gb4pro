"""
두 병원 데이터 파일 매칭 및 결합
작성 일시: 2026-01-20 00:01
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

print("=" * 80)
print("병원 데이터 매칭 및 결합")
print("=" * 80)

# ============================================================================
# Step 1: 데이터 로드 및 구조 확인
# ============================================================================
print("\n[Step 1] 데이터 로드 중...")

# 파일1: 결측치 처리 완료 데이터
file1_path = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_결측치처리완료_20260119_233319.csv'
df1 = pd.read_csv(file1_path, encoding='utf-8-sig')
print(f"  파일1 (결측치처리완료)")
print(f"    - 건수: {len(df1):,}건")
print(f"    - 컬럼: {len(df1.columns)}개")

# 파일2: 강남 병원 상세 데이터
file2_path = r'd:\git_gb4pro\crawling\gangnam\data\archive\gangnam_hospitals_detail_RESUME_20260105_041227.csv'
df2 = pd.read_csv(file2_path, encoding='utf-8-sig')
print(f"\n  파일2 (gangnam)")
print(f"    - 건수: {len(df2):,}건")
print(f"    - 컬럼: {len(df2.columns)}개")

# 매칭 키 컬럼 확인
print("\n[Step 2] 매칭 키 컬럼 확인...")
print(f"\n  파일1 병원명 컬럼: {[c for c in df1.columns if '병원' in c or '명' in c or '원본' in c][:5]}")
print(f"  파일1 주소 컬럼: {[c for c in df1.columns if '주소' in c or 'addr' in c.lower()][:5]}")
print(f"\n  파일2 병원명 컬럼: {[c for c in df2.columns if '병원' in c or '명' in c or 'name' in c.lower()][:5]}")
print(f"  파일2 주소 컬럼: {[c for c in df2.columns if '주소' in c or 'addr' in c.lower()][:5]}")

# ============================================================================
# Step 3: 매칭 키 정규화
# ============================================================================
print("\n[Step 3] 매칭 키 정규화 중...")

# 파일1 매칭 키 생성
df1['매칭_병원명'] = df1['원본_병원명'].str.strip().str.replace(' ', '')
df1['매칭_주소'] = df1['원본_주소'].str.strip().str.replace(' ', '')

# 파일2 매칭 키 생성
# 파일2의 컬럼명 확인 후 적절한 컬럼 선택
if 'yadmNm' in df2.columns:
    df2['매칭_병원명'] = df2['yadmNm'].str.strip().str.replace(' ', '')
elif '병원명' in df2.columns:
    df2['매칭_병원명'] = df2['병원명'].str.strip().str.replace(' ', '')
else:
    # 첫 번째 병원명 관련 컬럼 사용
    name_cols = [c for c in df2.columns if '명' in c or 'name' in c.lower()]
    if name_cols:
        df2['매칭_병원명'] = df2[name_cols[0]].str.strip().str.replace(' ', '')

if 'addr' in df2.columns:
    df2['매칭_주소'] = df2['addr'].str.strip().str.replace(' ', '')
elif '주소' in df2.columns:
    df2['매칭_주소'] = df2['주소'].str.strip().str.replace(' ', '')
else:
    # 첫 번째 주소 관련 컬럼 사용
    addr_cols = [c for c in df2.columns if '주소' in c or 'addr' in c.lower()]
    if addr_cols:
        df2['매칭_주소'] = df2[addr_cols[0]].str.strip().str.replace(' ', '')

print(f"  파일1 매칭 키 생성 완료")
print(f"  파일2 매칭 키 생성 완료")

# ============================================================================
# Step 4: 데이터 매칭 (병원명 + 주소)
# ============================================================================
print("\n[Step 4] 데이터 매칭 중...")

# 병원명과 주소 모두 일치하는 경우 매칭
merged_df = pd.merge(
    df1, 
    df2, 
    on=['매칭_병원명', '매칭_주소'],
    how='left',
    suffixes=('_file1', '_file2'),
    indicator=True
)

# 매칭 결과 통계
match_stats = merged_df['_merge'].value_counts()
matched_count = (merged_df['_merge'] == 'both').sum()
unmatched_count = (merged_df['_merge'] == 'left_only').sum()

print(f"\n  매칭 결과:")
print(f"    - 매칭 성공: {matched_count:,}건 ({matched_count/len(df1)*100:.1f}%)")
print(f"    - 매칭 실패: {unmatched_count:,}건 ({unmatched_count/len(df1)*100:.1f}%)")

# ============================================================================
# Step 5: 병원명만으로 재매칭 (주소 매칭 실패한 경우)
# ============================================================================
print("\n[Step 5] 병원명만으로 재매칭 시도...")

# 매칭 실패한 데이터
unmatched_df1 = df1[~df1['매칭_병원명'].isin(merged_df[merged_df['_merge'] == 'both']['매칭_병원명'])]

if len(unmatched_df1) > 0:
    # 병원명만으로 매칭
    name_only_match = pd.merge(
        unmatched_df1,
        df2,
        on='매칭_병원명',
        how='inner',
        suffixes=('_file1', '_file2')
    )
    
    additional_matches = len(name_only_match)
    print(f"  병원명만으로 추가 매칭: {additional_matches:,}건")
else:
    additional_matches = 0
    print(f"  추가 매칭 없음")

# ============================================================================
# Step 6: 결과 저장
# ============================================================================
print("\n[Step 6] 결과 저장 중...")

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_dir = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data'

# 결합된 데이터 저장
output_file = f'{output_dir}/병원데이터_결합완료_{timestamp}.csv'
merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"  저장: 병원데이터_결합완료_{timestamp}.csv")

# ============================================================================
# Step 7: 매칭 결과 분석
# ============================================================================
print("\n[Step 7] 매칭 결과 분석 중...")

# 컬럼 중복 분석
file1_cols = [c for c in merged_df.columns if c.endswith('_file1')]
file2_cols = [c for c in merged_df.columns if c.endswith('_file2')]
common_cols = [c.replace('_file1', '') for c in file1_cols if c.replace('_file1', '_file2') in file2_cols]

print(f"\n  컬럼 분석:")
print(f"    - 파일1 전용 컬럼: {len([c for c in merged_df.columns if not c.endswith('_file2') and not c.endswith('_file1')])}개")
print(f"    - 파일2 전용 컬럼: {len(file2_cols)}개")
print(f"    - 중복 컬럼: {len(common_cols)}개")

# 매칭 결과 요약
summary = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'file1': {
        'path': file1_path,
        'total_rows': int(len(df1)),
        'total_columns': int(len(df1.columns))
    },
    'file2': {
        'path': file2_path,
        'total_rows': int(len(df2)),
        'total_columns': int(len(df2.columns))
    },
    'matching_result': {
        'matched': int(matched_count),
        'unmatched': int(unmatched_count),
        'match_rate': float(matched_count / len(df1) * 100),
        'additional_name_only_matches': int(additional_matches)
    },
    'merged_data': {
        'total_rows': int(len(merged_df)),
        'total_columns': int(len(merged_df.columns)),
        'file1_only_columns': int(len([c for c in merged_df.columns if not c.endswith('_file2') and not c.endswith('_file1')])),
        'file2_only_columns': int(len(file2_cols)),
        'common_columns': int(len(common_cols))
    }
}

# JSON 저장
summary_file = f'{output_dir}/매칭결과_요약_{timestamp}.json'
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"  저장: 매칭결과_요약_{timestamp}.json")

# ============================================================================
# 완료
# ============================================================================
print("\n" + "=" * 80)
print("[완료] 데이터 매칭 및 결합 완료!")
print("=" * 80)
print(f"\n생성된 파일:")
print(f"  1. 병원데이터_결합완료_{timestamp}.csv")
print(f"  2. 매칭결과_요약_{timestamp}.json")
print(f"\n저장 위치: {output_dir}")

# 반환 (리포트 생성용)
print(f"\n[매칭 통계]")
print(f"  총 병원 수 (파일1): {len(df1):,}건")
print(f"  총 병원 수 (파일2): {len(df2):,}건")
print(f"  매칭 성공: {matched_count:,}건 ({matched_count/len(df1)*100:.1f}%)")
print(f"  매칭 실패: {unmatched_count:,}건 ({unmatched_count/len(df1)*100:.1f}%)")
