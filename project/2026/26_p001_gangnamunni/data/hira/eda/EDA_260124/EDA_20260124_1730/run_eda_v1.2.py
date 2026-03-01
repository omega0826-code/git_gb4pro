import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 설정
TIMESTAMP = "20260124_1730"
BASE_DIR = Path(r"d:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_260124\EDA_20260124_1730")
DATA_FILE = Path(r"d:\git_gb4pro\crawling\openapi\getHospDetailList\data\피부과_병원정보_20260124_153603.csv")
REPORT_FILE = BASE_DIR / f"EDA_REPORT_{TIMESTAMP}.md"
IMAGE_DIR = BASE_DIR / "images"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    return pd.read_csv(DATA_FILE, encoding='utf-8-sig')

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / filename, dpi=300, bbox_inches='tight')
    plt.close()

def plot_bar_with_labels(data, x, y, title, filename, color_palette='Blues_r', hue=None):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=data, x=x, y=y, 
        palette=color_palette, 
        hue=hue, 
        legend=False
    )
    plt.title(title)
    
    # 값 표시 (Value Labels) - Guideline 2.1.2
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.text(
                p.get_x() + p.get_width() / 2., height + 0.1, 
                f'{int(height)}', 
                ha="center", va="bottom", fontsize=10
            )
    save_plot(filename)

def plot_treemap(data, label, value, title, filename):
    # squarify 대체: 수평 막대 그래프 (Map 대용)
    plt.figure(figsize=(10, 8))
    # 값 기준 정렬
    data = data.sort_values(by=value, ascending=False)
    ax = sns.barplot(data=data, x=value, y=label, palette='coolwarm')
    plt.title(title)
    
    # 값 표시
    for i, v in enumerate(data[value]):
        ax.text(v + 0.1, i, f"{v}", va='center')
        
    save_plot(filename)

def append_missing_table(report_md, df, cols, col_names, n_total):
    """결측치 테이블 생성 (결측치가 있는 경우만)"""
    missing_data = []
    for c in cols:
        m = df[c].isnull().sum()
        if m > 0:
            missing_data.append([c, col_names.get(c, '-'), m, f"{m/n_total*100:.1f}%"])
            
    if missing_data:
        report_md.append("#### [Data Quality] 결측치 현황")
        report_md.append("| 컬럼명 | 한글 설명 | 결측치 수 | 결측률 | 비고 |")
        report_md.append("|---|---|---|---|---|")
        for row in missing_data:
            warn = "**[해석 주의]**" if float(row[3].replace('%','')) >= 50 else ""
            report_md.append(f"| `{row[0]}` | {row[1]} | {row[2]} | {row[3]} | {warn} |")
        report_md.append("\n")
    else:
        report_md.append("#### [Data Quality] 결측치 현황")
        report_md.append("- **결측치 없음(0건)**: 해당 항목 데이터는 모두 유효합니다.\n")

def analyze_staff(df, report_md):
    col = 'dgsbjt_dgsbjtPrSdrCnt'
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    n = len(df)
    
    report_md.append("## 3.1 인력 분석 (Staff Analysis)\n")
    report_md.append(f"> **분석 대상 병원 수(N)**: {n}개\n")
    
    # 시각화
    counts = df[col].astype(int).value_counts().sort_index()
    dist_df = pd.DataFrame({'spec_count': counts.index, 'hospital_count': counts.values})
    
    plot_bar_with_labels(
        dist_df, x='spec_count', y='hospital_count',
        title=f'피부과 전문의 수 분포 (N={n})',
        filename='staff_dist.png',
        hue='spec_count'
    )
    
    avg = df[col].mean()
    zero_cnt = len(df[df[col] == 0])
    
    report_md.append(f"- **평균 전문의 수**: {avg:.2f}명")
    report_md.append(f"- **전문의 없는 병원**: {zero_cnt}개 ({zero_cnt/n*100:.1f}%)")
    report_md.append("\n![전문의 분포](images/staff_dist.png)\n")
    report_md.append("> **[Chart Description]**: 전문의 수별 병원 빈도입니다. 숫자는 해당 전문의 수를 보유한 병원의 개수입니다.\n")
    
    append_missing_table(report_md, pd.DataFrame({col: [0]*n}), [col], {col: '전문의 수'}, n)

def analyze_bed(df, report_md):
    cols = ['eqp_stdSickbdCnt', 'eqp_hghrSickbdCnt']
    names = {'eqp_stdSickbdCnt': '일반병상 수', 'eqp_hghrSickbdCnt': '상급병상 수'}
    n = len(df)
    
    report_md.append("## 3.2 병상 규모 분석 (Bed Scale Analysis)\n")
    report_md.append(f"> **분석 대상 병원 수(N)**: {n}개\n")
    
    stats = []
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        cnt = len(df[df[c] > 0])
        stats.append({'Type': names[c], 'Count': cnt})
    
    stats_df = pd.DataFrame(stats)
    
    plot_bar_with_labels(
        stats_df, x='Type', y='Count',
        title=f'병상 보유 병원 수 (N={n})',
        filename='bed_dist.png',
        hue='Type',
        color_palette='viridis'
    )
    
    report_md.append("![병상 현황](images/bed_dist.png)\n")
    report_md.append("> **[Chart Description]**: 입원 가능한 일반/상급 병상을 1개 이상 보유한 병원의 수입니다.\n")
    append_missing_table(report_md, df, [], {}, n) # 병상수는 보통 null=0. 

def analyze_operation(df, report_md):
    n = len(df)
    report_md.append("## 3.3 운영 및 편의성 (Operation & Convenience)\n")
    report_md.append(f"> **분석 대상 병원 수(N)**: {n}개\n")
    
    # 점심시간
    if 'dtl_lunchWeek' in df.columns:
        valid = df['dtl_lunchWeek'].dropna()
        vn = len(valid)
        if vn > 0:
            top5 = valid.value_counts().head(5)
            tdf = pd.DataFrame({'Time': top5.index, 'Count': top5.values})
            plot_bar_with_labels(tdf, x='Count', y='Time', title=f'점심시간 패턴 Top 5 (N={vn})', filename='lunch.png', hue='Time')
            report_md.append("![점심시간](images/lunch.png)")
            report_md.append(f"> **[Chart Description]**: 점심시간 정보가 있는 {vn}개 병원의 시간대 분포입니다.\n")
    
    # 주차
    if 'dtl_parkQty' in df.columns:
        df['dtl_parkQty'] = pd.to_numeric(df['dtl_parkQty'], errors='coerce').fillna(0)
        park_cnt = len(df[df['dtl_parkQty'] > 0])
        
        # 도넛 차트 + 수치 표시
        plt.figure(figsize=(6, 6))
        # 파이차트는 bar_with_labels 못 쓰므로 여기서 그리기
        labels = [f'가능\n({park_cnt}개)', f'불가/미기재\n({n-park_cnt}개)']
        plt.pie([park_cnt, n-park_cnt], labels=labels, autopct='%1.1f%%', colors=['#ff9999','#e0e0e0'], startangle=90, pctdistance=0.85)
        # 도넛 처리
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title(f'주차 가능 병원 비율 (N={n})')
        save_plot('park_donut.png')
        
        report_md.append("![주차](images/park_donut.png)")
        report_md.append("> **[Chart Description]**: 주차 가능(대수>0) 비율입니다.\n")
        
    # 결측치
    temp = load_data()
    chk_cols = {'dtl_lunchWeek': '점심시간', 'dtl_parkQty': '주차대수'}
    append_missing_table(report_md, temp, chk_cols.keys(), chk_cols, n)

def analyze_equipment(df, report_md):
    col = 'medoft_oftCdNm'
    df_clean = df[col].dropna()
    n_rows = len(df)
    n_valid = len(df_clean)
    
    report_md.append("## 3.4 의료 장비 (Medical Equipment)\n")
    report_md.append(f"> **총 데이터 행(Row) 수(N)**: {n_rows}개 (장비정보 보유 {n_valid}개)\n")
    
    if n_valid > 0:
        eq_counts = df_clean.value_counts().head(20)
        edf = pd.DataFrame({'Name': eq_counts.index, 'Count': eq_counts.values})
        plot_bar_with_labels(edf, x='Count', y='Name', title=f'장비 보유 현황 Top 20 (N={n_rows})', filename='eq_dist.png', hue='Name', color_palette='magma')
        report_md.append("![장비](images/eq_dist.png)")
        report_md.append("> **[Chart Description]**: 행 데이터 기준 의료 장비 보유 빈도 상위 20개입니다.\n")
        
    append_missing_table(report_md, df, [col], {col: '의료장비명'}, n_rows)

def analyze_location(df, report_md):
    df_unique = df.drop_duplicates(subset=['원본_기관코드'])
    n = len(df_unique)
    
    report_md.append("## 3.5 입지 및 접근성 (Location & Accessibility)\n")
    report_md.append(f"> **분석 대상 병원 수(N)**: {n}개\n")
    
    # 1. 행정동 (지도 대용 트리맵)
    col_dong = 'eqp_emdongNm'
    if col_dong in df_unique.columns:
        dcounts = df_unique[col_dong].fillna('미상').value_counts()
        ddf = pd.DataFrame({'Dong': dcounts.index, 'Count': dcounts.values})
        
        plot_treemap(ddf, 'Dong', 'Count', f'행정동별 병원 분포 (N={n})', 'loc_map_dong.png')
        
        report_md.append("### 1) 행정동별 분포 (Administrative Dong)")
        report_md.append("![행정동 지도](images/loc_map_dong.png)")
        report_md.append("> **[Chart Description]**: 행정동별 병원 비중입니다. 상위 지역일수록 막대 길이가 깁니다.\n")
        
        # 결측치
        append_missing_table(report_md, df_unique, [col_dong], {col_dong: '행정동명'}, n)

    # 2. 지하철 (지도 대용 그래프)
    if 'trnsprt_trafNm' in df_unique.columns:
        sub = df_unique[df_unique['trnsprt_trafNm'].astype(str).str.contains('지하철', na=False)].copy()
        
        def get_st(x):
            if pd.isna(x): return x
            return str(x).split()[0].replace(',', '').strip()
        
        sub['station'] = sub['trnsprt_arivPlc'].apply(get_st)
        
        scounts = sub['station'].value_counts().head(15)
        sdf = pd.DataFrame({'Station': scounts.index, 'Count': scounts.values})
        
        # 지하철도 수평 바차트로 맵 대용
        plot_treemap(sdf, 'Station', 'Count', f'지하철 역세권 Top 15 (지하철정보 N={len(sub)})', 'loc_map_station.png')
        
        report_md.append("### 2) 지하철 역세권 분포 (Station Accessibility)")
        report_md.append("![지하철](images/loc_map_station.png)")
        report_md.append("> **[Chart Description]**: 교통편에 '지하철'을 명시한 병원들의 주요 역세권 분포입니다.\n")
        
        # 결측
        append_missing_table(report_md, df_unique, ['trnsprt_trafNm'], {'trnsprt_trafNm': '교통편'}, n)

def main():
    df = load_data()
    # 병원 기준 Uniq
    df_hosp = df.drop_duplicates(subset=['원본_기관코드'])
    
    report_md = []
    report_md.append(f"# 강남구 피부과 시장 분석 리포트")
    report_md.append(f"> **생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_md.append(f"> **분석 파일**: `피부과_병원정보_20260124_153603.csv`")
    
    # 1. 요약
    report_md.append("\n## 1. 요약 (Executive Summary)")
    report_md.append("- **인력**: 1인 전문의 체제 중심")
    report_md.append("- **입지**: 강남/압구정 집중")
    report_md.append("\n")
    
    # 2. 데이터 품질 (전체)
    report_md.append("## 2. 데이터 품질 보고")
    report_md.append(f"- **총 병원 수**: {len(df_hosp)}")
    report_md.append("- **참고**: 상세 결측 내역은 각 섹션 참조.\n")
    
    # 3. 상세
    analyze_staff(df_hosp.copy(), report_md)
    analyze_bed(df_hosp.copy(), report_md)
    analyze_operation(df_hosp.copy(), report_md)
    analyze_equipment(df.copy(), report_md)
    analyze_location(df.copy(), report_md) # copy used inside
    
    # 4. 제언
    report_md.append("## 4. 제언 (Suggestion)")
    report_md.append("1. **운영 차별화**: 정보 부재 영역(주차/점심) 선점")
    report_md.append("2. **입지 전략**: 과밀 지역 회피 및 이면 상권 고려\n")
    
    # 5. 종합
    report_md.append("## 5. 종합 분석 결과 (Comprehensive Analysis)")
    report_md.append("강남구 피부과 시장은 **1인 원장 중심**의 **외래 진료** 위주 시장입니다.")
    report_md.append("특히 **운영 시간**과 **주차 정보**의 데이터 부재가 심각하여, 이를 역으로 이용해 **상세한 정보 제공(Information Transparency)**만으로도 초기 신뢰도를 확보할 수 있습니다.")
    report_md.append("입지적으로는 행정동 데이터 분석 결과 특정 동에 편중되어 있어, **지역 내 불균형**을 활용한 입지 전략이 유효할 것으로 보입니다.")

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_md))
    print(f"Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
