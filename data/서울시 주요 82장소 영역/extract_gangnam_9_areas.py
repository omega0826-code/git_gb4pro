# -*- coding: utf-8 -*-
"""
강남 지역 9개 주요 상권 데이터 추출 스크립트
서울시 전체 상권 데이터에서 9개 상권만 필터링하여 저장
"""

import pandas as pd
from pathlib import Path
import sys

# 경로 설정
base_path = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역')
source_dir = base_path / '서울시 상권'
output_dir = base_path / 'Gangnam_9_Areas'

# 출력 디렉토리 생성
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("강남 지역 9개 주요 상권 데이터 추출")
print("=" * 80)
print()

# 9개 상권 코드 (영역-상권.csv에서 확인 필요)
# 먼저 영역 파일을 읽어서 상권 코드 확인
print("[1/10] 상권 코드 확인 중...")
area_file = source_dir / '서울시 상권분석서비스(영역-상권).csv'
df_area = pd.read_csv(area_file, encoding='utf-8-sig')

# 9개 상권 이름 (정확한 이름으로 수정)
target_areas = [
    '강남 마이스 관광특구',  # MICE가 아니라 마이스
    '강남역',
    '선릉역',
    '신논현역',
    '양재역',
    '역삼역',
    '가로수길',
    '압구정로데오',  # 정확한 이름: 압구정로데오역(압구정로데오)
    '청담사거리'     # 정확한 이름: 청담사거리(청담동명품거리)
]

# 상권 코드 추출
area_codes = []
found_areas = []

for area_name in target_areas:
    matching = df_area[df_area['상권_코드_명'].str.contains(area_name, na=False)]
    if len(matching) > 0:
        code = matching.iloc[0]['상권_코드']
        area_codes.append(code)
        found_areas.append(area_name)
        print(f"  [OK] {area_name}: {code}")
    else:
        print(f"  [X] {area_name}: 찾을 수 없음")

print(f"\n찾은 상권: {len(found_areas)}/{len(target_areas)}개")
print(f"상권 코드: {area_codes}")
print()

if len(area_codes) == 0:
    print("[ERROR] 상권을 찾을 수 없습니다. 프로그램을 종료합니다.")
    sys.exit(1)

# CSV 파일 목록
csv_files = [
    '서울시 상권분석서비스(길단위인구-상권).csv',
    '서울시 상권분석서비스(상권변화지표-상권).csv',
    '서울시 상권분석서비스(상주인구-상권).csv',
    '서울시 상권분석서비스(소득소비-상권).csv',
    '서울시 상권분석서비스(영역-상권).csv',
    '서울시 상권분석서비스(점포-상권)_2022년 1분기~2024년 4분기.csv',
    '서울시 상권분석서비스(직장인구-상권).csv',
    '서울시 상권분석서비스(집객시설-상권).csv',
    '서울시 상권분석서비스(추정매출-상권)__2022년 1분기~2024년 4분기.csv'
]

# 각 파일 처리
for idx, csv_file in enumerate(csv_files, 2):
    print(f"[{idx}/10] {csv_file} 처리 중...")
    
    try:
        # 파일 읽기
        source_file = source_dir / csv_file
        df = pd.read_csv(source_file, encoding='utf-8-sig')
        
        print(f"  원본 데이터: {len(df):,}행")
        
        # 상권 코드로 필터링
        df_filtered = df[df['상권_코드'].isin(area_codes)]
        
        print(f"  필터링 후: {len(df_filtered):,}행")
        
        # 저장
        output_file = output_dir / f"gangnam_{csv_file}"
        df_filtered.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"  [OK] 저장 완료: {output_file.name}")
        
    except Exception as e:
        print(f"  [ERROR] 처리 실패: {e}")
    
    print()

print("=" * 80)
print(f"[완료] 9개 상권 데이터 추출 완료!")
print("=" * 80)
print()
print(f"출력 디렉토리: {output_dir}")
print(f"추출된 상권: {', '.join(found_areas)}")
print()
