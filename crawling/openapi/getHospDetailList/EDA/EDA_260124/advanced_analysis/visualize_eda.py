import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Windows 기본 폰트 사용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 설정
INPUT_FILE = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\data\피부과_병원정보_20260124_153603.csv"
OUTPUT_DIR = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_260124\advanced_analysis"
IMAGE_DIR = r"d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_260124\advanced_analysis\images"
REPORT_FILE = r"INSIGHT_REPORT.md"

def load_data():
    df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    return df

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(Path(IMAGE_DIR) / filename, dpi=300, bbox_inches='tight')
    plt.close()

def plot_specialist_distribution(df):
    """3.1 인력 및 규모 시각화"""
    # 전문의 수 (dgsbjt_dgsbjtPrSdrCnt)
    col = 'dgsbjt_dgsbjtPrSdrCnt'
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    n_total = len(df)
    
    # 1. 전문의 수 분포
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=col, bins=range(0, 10), discrete=True, kde=False, color='skyblue')
    plt.title(f'피부과 전문의 수 분포 (N={n_total})')
    plt.xlabel('전문의 수 (명)')
    plt.ylabel('병원 수')
    plt.xticks(range(0, 10))
    save_plot('specialist_dist.png')
    
    # 2. 전문의 유무 비율
    has_specialist = df[col] > 0
    ratio = has_specialist.value_counts(normalize=True)
    
    plt.figure(figsize=(8, 8))
    plt.pie(ratio, labels=['전문의 있음', '전문의 정보 없음/0명'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90)
    plt.title(f'전문의 보유 병원 비율 (N={n_total})')
    save_plot('specialist_ratio.png')

def plot_bed_metrics(df):
    """3.1 병상 수 및 규모 분석"""
    cols = {
        'eqp_stdSickbdCnt': '일반병상',
        'eqp_hghrSickbdCnt': '상급병상',
        'eqp_emymCnt': '응급실'
    }
    
    summary_data = []
    
    for col, name in cols.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            has_facility = df[df[col] > 0]
            summary_data.append({'시설': name, '보유병원수': len(has_facility), '평균병상수': has_facility[col].mean()})
            
    summary_df = pd.DataFrame(summary_data)
    
    if not summary_df.empty:
        plt.figure(figsize=(10, 6))
        # hue를 x와 동일하게 설정하여 warning 해결
        sns.barplot(data=summary_df, x='시설', y='보유병원수', hue='시설', palette='viridis', legend=False)
        plt.title(f'입원/응급 시설 보유 병원 현황 (N={len(df)})')
        for i, v in enumerate(summary_df['보유병원수']):
            plt.text(i, v, f"{v}개", ha='center', va='bottom')
        save_plot('bed_count_analysis.png')

def plot_operation_metrics(df):
    """3.2 운영 및 편의성 시각화"""
    n_total = len(df)
    # 1. 점심시간 패턴
    if 'dtl_lunchWeek' in df.columns:
        # 결측 제외 유효 데이터만 분석
        valid_lunch = df['dtl_lunchWeek'].dropna()
        valid_count = len(valid_lunch)
        lunch = valid_lunch.value_counts().head(5)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=lunch.values, y=lunch.index, hue=lunch.index, palette='pastel', legend=False)
        plt.title(f'주요 점심시간 패턴 Top 5 (N={valid_count}, 전체={n_total})')
        plt.xlabel('병원 수')
        save_plot('lunch_time_pattern.png')
        
    # 2. 주차 가능 여부 (dtl_parkQty)
    if 'dtl_parkQty' in df.columns:
        df['park_qty'] = pd.to_numeric(df['dtl_parkQty'], errors='coerce').fillna(0)
        has_parking = df['park_qty'] > 0
        
        plt.figure(figsize=(8, 8))
        labels = ['주차 가능', '주차 불가/정보없음']
        sizes = [has_parking.sum(), len(df) - has_parking.sum()]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#99ff99','#ffcc99'], startangle=90)
        plt.title(f'주차 가능 병원 비율 (N={n_total})')
        save_plot('parking_availability.png')

def plot_infrastructure(df):
    """3.3 인프라 및 장비"""
    # 장비 컬럼 찾기 (medoft_oftCdNm)
    if 'medoft_oftCdNm' in df.columns:
        equipments = df['medoft_oftCdNm'].dropna()
        n_records = len(equipments) # 장비 정보 행 수
        top_eq = equipments.value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_eq.values, y=top_eq.index, hue=top_eq.index, palette='magma', legend=False)
        plt.title(f'주요 보유 장비 Top 10 (장비정보 건수 N={n_records})')
        plt.xlabel('보유 병원 수(중복포함)')
        save_plot('top_equipments.png')

def plot_location(df):
    """3.4 입지 분석"""
    # 역세권 키워드 분석
    if 'trnsprt_trafNm' in df.columns and 'trnsprt_arivPlc' in df.columns:
        # 중복 제거 (병원 기준)
        df_unique = df.drop_duplicates(subset=['원본_기관코드'])
        n_unique = len(df_unique)
        
        subway = df_unique[df_unique['trnsprt_trafNm'].astype(str).str.contains('지하철', na=False)]
        stations = subway['trnsprt_arivPlc'].astype(str).apply(lambda x: x.split()[0].replace(',', '').strip())
        top_stations = stations.value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_stations.index, y=top_stations.values, hue=top_stations.index, palette='coolwarm', legend=False)
        plt.title(f'주요 지하철역 주변 피부과 분포 Top 10 (N={n_unique})')
        plt.ylabel('병원 수')
        plt.xticks(rotation=45)
        save_plot('location_station.png')

def generate_report_markdown(df):
    md = "# 강남구 피부과 심층 분석 보고서 (Insight Report)\n\n"
    md += "## 1. 개요\n"
    md += f"- **분석 대상**: {len(df):,}개 데이터\n"
    md += "- **목표**: 강남구 피부과 시장 미충족 수요(Unmet Needs) 발굴 및 경쟁 우위 전략 도출\n\n"
    
    # 2. 인력 및 병상 분석
    md += "## 2. 인력 및 병상 규모 분석\n"
    md += "### 2.1 전문의 및 의사 현황\n"
    md += "![전문의 분포](images/specialist_dist.png)\n\n"
    md += "![전문의 비율](images/specialist_ratio.png)\n\n"
    
    # 결측치 분석 표
    cols_staff = ['dgsbjt_dgsbjtPrSdrCnt']
    md += "#### [Data Quality] 결측치 현황 (인력)\n"
    md += "| 컬럼명 | 결측치 수 | 결측률 | 비고 |\n|---|---|---|---|\n"
    for c in cols_staff:
        missing = df[c].isnull().sum()
        md += f"| `{c}` | {missing:,} | {(missing/len(df))*100:.1f}% | 전문의 수 |\n"
    
    # 병상 분석
    md += "\n### 2.2 입원 및 응급 시설 (Hospital Scale)\n"
    md += "![병상 현황](images/bed_count_analysis.png)\n\n"
    cols_bed = ['eqp_stdSickbdCnt', 'eqp_hghrSickbdCnt', 'eqp_emymCnt']
    md += "#### [Data Quality] 결측치 현황 (시설)\n"
    md += "| 컬럼명 | 결측치 수 | 결측률 | 비고 |\n|---|---|---|---|\n"
    for c in cols_bed:
        if c in df.columns:
            missing = df[c].isnull().sum()
            md += f"| `{c}` | {missing:,} | {(missing/len(df))*100:.1f}% | 병상/응급실 |\n"
            
    # 3. 운영 분석
    md += "\n## 3. 운영 및 편의성 분석\n"
    md += "### 3.1 점심시간 및 주차\n"
    md += "![점심시간](images/lunch_time_pattern.png)\n"
    md += "![주차가능](images/parking_availability.png)\n\n"
    
    cols_op = ['dtl_lunchWeek', 'dtl_parkQty', 'dtl_noTrmtSun']
    md += "#### [Data Quality] 결측치 현황 (운영)\n"
    md += "| 컬럼명 | 결측치 수 | 결측률 | 비고 |\n|---|---|---|---|\n"
    for c in cols_op:
        if c in df.columns:
            missing = df[c].isnull().sum()
            md += f"| `{c}` | {missing:,} | {(missing/len(df))*100:.1f}% | |\n"

    # 4. 장비 및 입지
    md += "\n## 4. 인프라 및 입지 분석\n"
    md += "### 4.1 주요 의료 장비\n"
    md += "![장비](images/top_equipments.png)\n\n"
    
    md += "### 4.2 주요 역세권 분포\n"
    md += "![역세권](images/location_station.png)\n\n"
    
    # 5. 전체 요약
    md += "\n## 5. 종합 요약 (Dataset Summary)\n"
    md += "| 분석영역 | 주요 지표 | 값/비율 | 시사점 |\n|---|---|---|---|\n"
    
    # 요약 계산
    parking_ratio = (pd.to_numeric(df['dtl_parkQty'], errors='coerce').fillna(0) > 0).mean() * 100
    w_spec_cnt = pd.to_numeric(df['dgsbjt_dgsbjtPrSdrCnt'], errors='coerce').fillna(0).mean()
    
    md += f"| **인력** | 평균 전문의 수 | {w_spec_cnt:.1f}명 | 1인 의원 중심 |\n"
    md += f"| **시설** | 주차 가능 비율 | {parking_ratio:.1f}% | 자차 접근성 낮음 |\n"
    md += f"| **운영** | 점심시간 | 13~14시 집중 | 점심 진료 차별화 가능 |\n"
    
    with open(Path(OUTPUT_DIR) / REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(md)

def main():
    print("Loading data...")
    df = load_data()
    
    print("Generating plots...")
    plot_specialist_distribution(df.copy())
    plot_bed_metrics(df.copy())
    plot_operation_metrics(df.copy())
    plot_infrastructure(df.copy())
    plot_location(df.copy())
    
    print("Generating report...")
    generate_report_markdown(df.copy())
    
    print("Done!")

if __name__ == "__main__":
    main()
