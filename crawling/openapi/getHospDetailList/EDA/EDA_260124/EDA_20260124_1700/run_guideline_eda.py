import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from pathlib import Path
from datetime import datetime

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 설정
BASE_DIR = Path(r"d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_260124\EDA_20260124_1700")
DATA_FILE = Path(r"d:\git_gb4pro\crawling\openapi\getHospDetailList\data\피부과_병원정보_20260124_153603.csv")
REPORT_FILE = BASE_DIR / "EDA_REPORT.md"
IMAGE_DIR = BASE_DIR / "images"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    return pd.read_csv(DATA_FILE, encoding='utf-8-sig')

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / filename, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_staff(df, report_md):
    """3.1 인력 분석"""
    col = 'dgsbjt_dgsbjtPrSdrCnt'
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    n = len(df)
    
    # 시각화
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=col, bins=range(0, 10), discrete=True, kde=False, color='skyblue')
    plt.title(f'피부과 전문의 수 분포 (N={n})')
    plt.xlabel('전문의 수 (명)')
    plt.ylabel('병원 수')
    plt.xticks(range(0, 10))
    save_plot('staff_specialist_dist.png')
    
    avg_spec = df[col].mean()
    zero_spec = len(df[df[col] == 0])
    
    report_md.append("## 3.1 인력 분석 (Staff Analysis)\n")
    report_md.append(f"- **분석 대상**: {n}개 병원")
    report_md.append(f"- **평균 전문의 수**: {avg_spec:.2f}명")
    report_md.append(f"- **전문의 없는(0명) 병원**: {zero_spec}개 ({zero_spec/n*100:.1f}%)")
    report_md.append("\n![전문의 분포](images/staff_specialist_dist.png)\n")
    
    # 결측치 표
    report_md.append("#### [Data Quality] 결측치 현황")
    report_md.append("| 컬럼명 | 결측치 수 | 결측률 | 비고 |")
    report_md.append("|---|---|---|---|")
    missing = df[col].isnull().sum() # fillna 전이 아니라 원본 기준이어야 하는데 위에서 fillna함. 
    # 다시 확인: 위에서 fillna(0) 했으므로 0으로 간주. 원본 로딩 다시 해서 확인
    orig_missing = pd.read_csv(DATA_FILE, usecols=[col], encoding='utf-8-sig')[col].isnull().sum()
    report_md.append(f"| `{col}` | {orig_missing} | {orig_missing/n*100:.1f}% | |")
    report_md.append("\n")

def analyze_bed(df, report_md):
    """3.2 병상 규모 분석 (응급실 제외)"""
    cols = ['eqp_stdSickbdCnt', 'eqp_hghrSickbdCnt']
    col_names = {'eqp_stdSickbdCnt': '일반병상', 'eqp_hghrSickbdCnt': '상급병상'}
    
    report_md.append("## 3.2 병상 규모 분석 (Bed Scale Analysis)\n")
    report_md.append("> **기준**: 응급실 제외, 일반/상급 병상 보유 현황 분석\n")
    
    summary = []
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        has_bed = df[df[c] > 0]
        count = len(has_bed)
        summary.append({'Type': col_names[c], 'Count': count})
        
    summ_df = pd.DataFrame(summary)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(data=summ_df, x='Type', y='Count', palette='viridis', hue='Type', legend=False)
    plt.title(f'병상 보유 병원 수 (N={len(df)})')
    save_plot('bed_status.png')
    
    report_md.append("![병상 현황](images/bed_status.png)\n")
    
    # 결측치 표
    report_md.append("#### [Data Quality] 결측치 현황")
    report_md.append("| 컬럼명 | 결측치 수 | 결측률 | 비고 |")
    report_md.append("|---|---|---|---|")
    temp_df = pd.read_csv(DATA_FILE, usecols=cols, encoding='utf-8-sig')
    for c in cols:
        m = temp_df[c].isnull().sum()
        report_md.append(f"| `{c}` | {m} | {m/len(df)*100:.1f}% | |")
    report_md.append("\n")

def analyze_equipment(df, report_md):
    """3.4 의료 장비 (전체 리스트)"""
    col = 'medoft_oftCdNm'
    
    if col in df.columns:
        # 중복 포함해서 카운트 (한 병원이 여러 장비 가질 수 있음 - 데이터 구조상 행 분리 여부 확인 필요)
        # 가이드라인: "데이터 구조상(1병원 다수장비) 중복 집계 가능성을 고려"
        # 여기서는 전체 리스트 빈도 분석
        eq_counts = df[col].dropna().value_counts()
        n_total_records = len(df) # 행 기준 N
        
        # 전체 리스트 시각화 (너무 많으면 상위 20개 + 워드클라우드 등 고려, 여기서는 상위 20개 바차트)
        top_n = 20
        top_eq = eq_counts.head(top_n)
        
        plt.figure(figsize=(10, 8))
        sns.barplot(x=top_eq.values, y=top_eq.index, palette='magma', hue=top_eq.index, legend=False)
        plt.title(f'주요 의료장비 보유 현황 (Top {top_n}) (총 데이터 행 N={n_total_records})')
        plt.xlabel('보유 건수')
        save_plot('equipment_full_dist.png')
        
        report_md.append("## 3.4 의료 장비 (Medical Equipment)\n")
        report_md.append(f"- **분석 장비 종류**: 총 {len(eq_counts)}종")
        report_md.append(f"- **전체 장비 데이터 건수**: {len(df[col].dropna())}건")
        report_md.append(f"\n![장비 보유](images/equipment_full_dist.png)\n")
        
        # 전체 리스트 표 (Top 20만 표시하고 나머지는 생략 언급)
        report_md.append("#### [상세] 보유 장비 목록 (Top 20)")
        report_md.append("| 순위 | 장비명 | 보유 건수 | 비율(전체행 대비) |")
        report_md.append("|---|---|---|---|")
        for i, (name, cnt) in enumerate(top_eq.items(), 1):
            report_md.append(f"| {i} | {name} | {cnt} | {cnt/n_total_records*100:.1f}% |")
        report_md.append("\n")
    else:
        report_md.append("## 3.4 의료 장비\n 데이터 없음\n")

def analyze_location(df, report_md):
    """3.5 입지 및 접근성 (행정동 / 지하철 분리)"""
    # 원본 병원 기준 유니크 (행정동 분석용)
    df_unique = df.drop_duplicates(subset=['원본_기관코드'])
    n = len(df_unique)
    
    # 1. 행정동 분석
    col_dong = 'eqp_emdongNm'
    if col_dong in df.columns:
        dong_counts = df_unique[col_dong].value_counts().head(10)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=dong_counts.values, y=dong_counts.index, palette='coolwarm', hue=dong_counts.index, legend=False)
        plt.title(f'행정동별 병원 분포 Top 10 (N={n})')
        save_plot('location_dong.png')
        
        report_md.append("## 3.5 입지 및 접근성 (Location)\n")
        report_md.append("### 1) 행정동별 분포")
        report_md.append("![행정동](images/location_dong.png)\n")

    # 2. 지하철역 분석
    # 지하철 정보가 있는 행만 추출 (중복 제거된 df_unique에서 찾거나, 교통정보가 별도 행이면 전체 df에서 찾거나)
    # trnsprt_trafNm, trnsprt_arivPlc
    # 교통 정보는 병원별로 여러 개일 수 있으므로 전체 df 사용하되 병원 기준 중복 제거 필요할 수 있음
    # 여기서는 "병원당 가장 가까운 역 1개"가 아니라 "정보에 있는 모든 역"을 카운트?
    # 보통 병원 상세 정보에 교통편이 여러 줄 있을 수 있음.
    # 하지만 일단 병원별 중복 제거된 데이터(`df_unique`) 기준으로는 1개 값만 남으므로(first), 
    # 정확한 분석을 위해선 중복 포함 df에서 교통정보만 따로 떼서 분석하거나, 
    # `df_unique`에 있는 대표값만 분석. 여기서는 `df_unique` 사용 (단순화).
    
    col_traf = 'trnsprt_trafNm'
    col_spot = 'trnsprt_arivPlc'
    
    if col_traf in df.columns and col_spot in df.columns:
        subway_df = df_unique[df_unique[col_traf].astype(str).str.contains('지하철', na=False)].copy()
        
        def clean_station(x):
            if pd.isna(x): return x
            x = str(x).split()[0].replace(',', '').strip()
            if not x.endswith('역'): # 역으로 안끝나는 경우 (예: "강남") 처리 보류 또는 그대로
                pass 
            return x

        subway_df['station'] = subway_df[col_spot].apply(clean_station)
        st_counts = subway_df['station'].value_counts().head(10)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=st_counts.values, y=st_counts.index, palette='Blues_r', hue=st_counts.index, legend=False)
        plt.title(f'지하철역(역세권) 병원 분포 Top 10 (N={len(subway_df)})')
        save_plot('location_station.png')
        
        report_md.append("### 2) 지하철 역세권 분포")
        report_md.append(f"- **분석 대상**: 교통정보에 '지하철'이 명시된 병원 {len(subway_df)}개")
        report_md.append("![지하철](images/location_station.png)\n")

def main():
    df = load_data()
    report_md = []
    
    report_md.append(f"# 강남구 피부과 시장 분석 리포트")
    report_md.append(f"> **생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_md.append(f"> **분석 파일**: `{DATA_FILE.name}`")
    report_md.append("---\n")
    
    # 분석 순서대로 실행
    analyze_staff(df.drop_duplicates(subset=['원본_기관코드']), report_md)
    analyze_bed(df.drop_duplicates(subset=['원본_기관코드']), report_md)
    # 장비는 전체 df 사용 (중복 허용)
    analyze_equipment(df, report_md)
    analyze_location(df, report_md)
    
    # 파일 저장
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_md))
    print(f"Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
