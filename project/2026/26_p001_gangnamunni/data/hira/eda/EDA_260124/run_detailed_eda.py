import pandas as pd
import numpy as np
from pathlib import Path
import re

# 설정
INPUT_FILE = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\data\피부과_병원정보_20260124_153603.csv"
OUTPUT_DIR = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_260124"
OUTPUT_FILE = r"REPORT_강남구_피부과_심층분석.md"

def load_data(filepath):
    # CSV 로드 (encoding='utf-8-sig' for Korean)
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def analyze_basic_info(df):
    report = "## 1. 데이터 개요 및 구조\n\n"
    report += f"- **총 데이터 건수**: {len(df):,}건\n"
    report += f"- **총 컬럼 수**: {len(df.columns)}개\n\n"
    
    # 주요 접두어별 컬럼 수 확인
    prefixes = ['원본_', 'eqp_', 'dtl_', 'dgsbjt_', 'medoft_', 'trnsprt_', 'spcldiag_']
    report += "| 접두어 | 설명 | 컬럼 수 |\n|---|---|---|\n"
    desc_map = {
        '원본_': '수집 원본', 'eqp_': '기본 시설', 'dtl_': '세부 정보', 
        'dgsbjt_': '진료 과목', 'medoft_': '의료 장비', 'trnsprt_': '교통 정보', 
        'spcldiag_': '특수 진료'
    }
    for p in prefixes:
        count = len([c for c in df.columns if c.startswith(p)])
        report += f"| `{p}` | {desc_map.get(p, '-')} | {count} |\n"
    report += "\n---\n\n"
    return report

def analyze_scale_and_staff(df):
    report = "## 2.1 [기본] 의료기관 규모 및 인력 분석\n\n"
    
    # eqp_drTotCnt(의사총수) 컬럼이 없는 것으로 확인됨 (CSV 헤더 기반 확인).
    # 대신 dgsbjt_dgsbjtPrSdrCnt (진료과목별 전문의 수)를 활용하여 분석 시도.
    
    has_total_doc = 'eqp_drTotCnt' in df.columns
    has_spec_doc = 'dgsbjt_dgsbjtPrSdrCnt' in df.columns
    
    report += f"> **참고**: '의사총수'(`eqp_drTotCnt`) 정보가 데이터에 {'포함되어 있습니다' if has_total_doc else '포함되어 있지 않습니다'}.\n"
    if not has_total_doc and has_spec_doc:
        report += "> 대안으로 **'진료과목별 전문의 수'**(`dgsbjt_dgsbjtPrSdrCnt`)를 분석합니다.\n\n"
        target_col = 'dgsbjt_dgsbjtPrSdrCnt'
        col_name = "전문의 수"
    elif has_total_doc:
        target_col = 'eqp_drTotCnt'
        col_name = "의사 수"
    else:
        report += "\n**분석 불가**: 의사 관련 컬럼을 찾을 수 없습니다.\n\n---\n\n"
        return report

    # 데이터 타입 변환
    df[target_col] = pd.to_numeric(df[target_col], errors='coerce').fillna(0)

    # 1. 통계
    stats = df[target_col].describe()
    report += f"### 2.1.1 {col_name} 기초 통계\n"
    report += f"- **평균**: {stats['mean']:.2f}명\n"
    report += f"- **중앙값**: {stats['50%']:.0f}명\n"
    report += f"- **최대**: {stats['max']:.0f}명\n"
    report += f"- **합계**: {df[target_col].sum():,.0f}명\n\n"

    # 2. 분포
    report += f"### 2.1.2 {col_name} 분포 현황\n"
    # 0명, 1명, 2~3명, 4명 이상
    bins = [-1, 0, 1, 3, 1000]
    labels = ['정보없음(0명)', '1명', '2~3명', '4명 이상']
    
    df['doc_cat'] = pd.cut(df[target_col], bins=bins, labels=labels, right=True)
    counts = df['doc_cat'].value_counts().sort_index()
    
    report += "| 구분 | 병원 수 | 비율 |\n|---|---|---|\n"
    total = len(df)
    for label, count in counts.items():
        if count > 0:
            ratio = (count / total) * 100
            report += f"| {label} | {count:,} | {ratio:.1f}% |\n"
            
    report += "\n---\n\n"
    return report

def analyze_operation(df):
    report = "## 2.2 [운영] 진료 시간 및 편의성 분석\n\n"
    
    # 1. 점심시간 패턴
    if 'dtl_lunchWeek' in df.columns:
        lunch_counts = df['dtl_lunchWeek'].fillna('정보없음').value_counts().head(5)
        report += "### 2.2.1 주요 점심시간 패턴 (Top 5)\n"
        report += "| 점심시간 | 병원 수 |\n|---|---|\n"
        for time, count in lunch_counts.items():
            report += f"| {time} | {count:,} |\n"
        report += "\n"

    # 2. 주말 진료 (토요일/일요일)
    # 토요일: dtl_trmtSatStart, dtl_trmtSatEnd 값이 있는 경우
    # 일요일: dtl_trmtSunStart, dtl_trmtSunEnd 값이 있는 경우
    sat_col = 'dtl_trmtSatEnd'
    sun_col = 'dtl_trmtSunEnd'
    
    sat_open = df[sat_col].notna().sum() if sat_col in df.columns else 0
    sun_open = df[sun_col].notna().sum() if sun_col in df.columns else 0
    
    report += "### 2.2.2 주말 진료 현황\n"
    report += f"- **토요일 진료 병원**: {sat_open:,}개 ({(sat_open/len(df))*100:.1f}%)\n"
    report += f"- **일요일 진료 병원**: {sun_open:,}개 ({(sun_open/len(df))*100:.1f}%)\n"
    
    # 3. 주차 편의성
    if 'dtl_parkQty' in df.columns:
        df['park_qty'] = pd.to_numeric(df['dtl_parkQty'], errors='coerce').fillna(0)
        has_parking = len(df[df['park_qty'] > 0])
        avg_parking = df[df['park_qty'] > 0]['park_qty'].mean()
        
        report += "\n### 2.2.3 주차 편의성\n"
        report += f"- **주차 가능 병원**: {has_parking:,}개 ({(has_parking/len(df))*100:.1f}%)\n"
        report += f"- **평균 주차 가능 대수**: {avg_parking:.1f}대 (주차 가능 병원 기준)\n"
    
    report += "\n---\n\n"
    return report

def analyze_infrastructure(df):
    report = "## 2.3 [인프라] 의료 장비 분석\n\n"
    
    # 장비 데이터는 보통 medoft_oftCdNm 같은 컬럼에 있을 것으로 추정되지만
    # CSV 구조를 보면 병원마다 여러 장비가 있으면 컬럼이 여러 개일 수도 있고,
    # 행이 늘어났을 수도 있음 (1:N). 
    # 그런데 현재 CSV는 'eqp_yadmNm'이 Unique한지 확인 필요.
    # 만약 1:N이라면 groupby 후 집계해야 함. 
    # 일단 CSV header를 보면 한 행에 medoft_oftCnt 등이 있음.
    # medoft_oftCdNm 컬럼이 있는지 확인.
    
    if 'medoft_oftCdNm' in df.columns:
        # 장비명 리스트 추출 (결측 제외)
        equipments = df['medoft_oftCdNm'].dropna()
        eq_counts = equipments.value_counts().head(10)
        
        report += "### 2.3.1 주요 보유 장비 Top 10\n"
        report += "| 순위 | 장비명 | 보유 병원 수 |\n|---|---|---|\n"
        for idx, (eq, cnt) in enumerate(eq_counts.items(), 1):
            report += f"| {idx} | {eq} | {cnt:,} |\n"
            
        # 병원별 총 장비 수 계산 (medoft_oftCnt 합계? 행별로 다른 장비라면 group by 필요)
        # 병원명(eqp_yadmNm) 기준 데이터가 중복되어 있는지 확인
        dups = df.duplicated(subset=['eqp_yadmNm']).sum()
        if dups > 0:
            report += f"\n> **참고**: 데이터에 병원명 중복이 {dups}건 있습니다. 이는 한 병원이 여러 장비/과목 정보를 가져 행이 분리된 것으로 추정됩니다. 위 장비 보유 수는 단순 행 카운트입니다.\n"
    else:
        report += "장비명 컬럼(`medoft_oftCdNm`)을 찾을 수 없습니다.\n"
        
    report += "\n---\n\n"
    return report

def analyze_accessibility(df):
    report = "## 2.4 [접근성] 교통 및 입지 분석\n\n"
    
    # 역세권 분석
    # trnsprt_trafNm(교통편)에서 '지하철' 찾기 + trnsprt_arivPlc(하차지점) 분석
    if 'trnsprt_arivPlc' in df.columns:
        subway_stations = df[df['trnsprt_trafNm'].astype(str).str.contains('지하철', na=False)]['trnsprt_arivPlc']
        # 텍스트 정제 (역 이름만 추출)
        # 예: "강남역 1번출구" -> "강남역"
        def clean_station(x):
            if not isinstance(x, str): return x
            # '역'으로 끝나는 단어 찾기, 혹은 일반적인 주요 역명
            # 간단히 공백 기준 첫 단어만 추출해보고 '역'이 없으면 붙여보기 등
            # 여기서는 단순 빈도 분석
            return x.split()[0].replace(',', '').strip()

        stations = subway_stations.apply(clean_station)
        top_stations = stations.value_counts().head(10)
        
        report += "### 2.4.1 주요 역세권 병원 분포 (Top 10)\n"
        report += "| 지하철역 | 병원 수 (추정) |\n|---|---|\n"
        for st, cnt in top_stations.items():
            report += f"| {st} | {cnt:,} |\n"
            
    report += "\n---\n\n"
    return report

def analyze_specialty(df):
    report = "## 2.5 [특화] 진료 과목 특성\n\n"
    
    # 진료 과목 dgsbjt_dgsbjtCdNm
    if 'dgsbjt_dgsbjtCdNm' in df.columns:
        subjects = df['dgsbjt_dgsbjtCdNm'].dropna()
        # '피부과'는 당연히 많을 테니 피부과 제외하고 카운트
        other_subjects = subjects[subjects != '피부과']
        sub_counts = other_subjects.value_counts().head(10)
        
        report += "### 2.5.1 피부과 외 주요 진료 과목 (병행 진료)\n"
        report += "| 진료과목 | 병원 수 |\n|---|---|\n"
        for sub, cnt in sub_counts.items():
            report += f"| {sub} | {cnt:,} |\n"
            
    report += "\n---\n\n"
    return report

def main():
    print("Loading data...")
    df = load_data(INPUT_FILE)
    if df is None:
        return

    # 병원명 기준 중복 제거한 DF (기본 정보 분석용)
    # 장비나 진료과목 등 1:N 데이터가 있어 행이 중복될 수 있으므로,
    # 병원 기본 정보(인력, 주차 등)는 중복 제거 후 분석해야 정확함.
    df_unique = df.drop_duplicates(subset=['eqp_ykiho']) if 'eqp_ykiho' in df.columns else df.drop_duplicates(subset=['원본_기관코드'])
    
    print(f"Original Records: {len(df)}")
    print(f"Unique Hospitals: {len(df_unique)}")

    content = "# 강남구 피부과 심층 EDA 보고서\n\n"
    content += f"**분석 일시**: 2026-01-24\n"
    content += f"**데이터 출처**: {INPUT_FILE}\n"
    content += "---\n\n"
    
    content += analyze_basic_info(df_unique)
    content += analyze_scale_and_staff(df_unique)
    content += analyze_operation(df_unique)
    
    # 인프라(장비)와 특화(진료과목)는 중복 허용 DF 사용 (전체 리스트)
    content += analyze_infrastructure(df) 
    
    content += analyze_accessibility(df_unique) # 역세권은 병원당 하나만 잡는게 맞을듯 (주요역)
    content += analyze_specialty(df) # 진료과목도 병행과목 다 봐야하니 원본 사용

    # 저장
    out_path = Path(OUTPUT_DIR) / OUTPUT_FILE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Report saved to {out_path}")

if __name__ == "__main__":
    main()
