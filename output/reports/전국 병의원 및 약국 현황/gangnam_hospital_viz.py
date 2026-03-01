import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows 기준 Malgun Gothic)
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# 1. 파일 경로 설정
DATA_PATH = r"d:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\data_260131_0844\서울_강남구_병원_2025.12.csv"
OUTPUT_DIR = r"d:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\analysis_260216_gangnam"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. 데이터 로드 및 전처리
print(f"Loading data from {DATA_PATH}...")
df = pd.read_csv(DATA_PATH, encoding='utf-8-sig')

# 시각화 설정
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

# 3. 시각화 생성 함수
def generate_visualizations(df, output_dir):
    viz_files = []

    # [V1] 동별 병원 수 분포 (Horizontal Bar Chart)
    plt.figure(figsize=(10, 8))
    dong_counts = df['읍면동'].value_counts().head(20)
    ax = sns.barplot(x=dong_counts.values, y=dong_counts.index, hue=dong_counts.index, palette="viridis", legend=False)
    
    # 데이터 라벨 추가
    for i, v in enumerate(dong_counts.values):
        ax.text(v + 3, i, f'{int(v):,}건', va='center', fontweight='bold')
        
    plt.title("강남구 행정동별 병원 수 (TOP 20)", fontsize=15)
    plt.xlabel("병원 수")
    plt.ylabel("행정동")
    path = os.path.join(output_dir, "v1_dong_distribution.png")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()
    viz_files.append(("행정동별 병원 수 분포", "v1_dong_distribution.png", "강남구 내 주요 행정동별 병원 밀집도를 보여줍니다. 신사동, 역삼동, 압구정동 순으로 높은 밀집도를 보입니다."))

    # [V2] 병원 종별 비중 (Pie Chart)
    plt.figure(figsize=(10, 7))
    type_counts = df['종별코드명'].value_counts()
    
    def func(pct, allvals):
        absolute = int(round(pct/100.*sum(allvals)))
        return f"{pct:.1f}%\n({absolute:,}건)"

    plt.pie(type_counts, labels=type_counts.index, autopct=lambda pct: func(pct, type_counts), 
            startangle=140, colors=sns.color_palette("pastel"))
    plt.title("강남구 병원 종별 비중", fontsize=15)
    path = os.path.join(output_dir, "v2_type_distribution.png")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()
    viz_files.append(("병원 종별 비중", "v2_type_distribution.png", "상급종합, 종합병원, 의원 등 병원 종별 구성을 나타냅니다. 의원급이 압도적인 비중을 차지합니다."))

    # [V3] 주요 진료과목 TOP 15 (Bar Chart)
    dept_cols = [col for col in df.columns if col.startswith('진료과목_') and col not in ['진료과목_개수', '진료과목_내과계', '진료과목_외과계', '진료과목_미용계']]
    if dept_cols:
        dept_sum = df[dept_cols].sum().sort_values(ascending=False).head(15)
        dept_sum.index = [idx.replace('진료과목_', '') for idx in dept_sum.index]

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x=dept_sum.index, y=dept_sum.values, hue=dept_sum.index, palette="magma", legend=False)
        
        # 데이터 라벨 추가
        for i, v in enumerate(dept_sum.values):
            ax.text(i, v + 5, f'{int(v):,}건', ha='center', fontweight='bold')

        plt.title("강남구 주요 진료과목 현황 (TOP 15)", fontsize=15)
        plt.xlabel("진료과목")
        plt.ylabel("병원 수")
        plt.xticks(rotation=45)
        path = os.path.join(output_dir, "v3_dept_ranking.png")
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()
        viz_files.append(("주요 진료과목 순위", "v3_dept_ranking.png", "강남구 내 병원들이 운영하는 주요 진료과목 분포입니다. 피부과와 성형외과가 상위권을 차지합니다."))

    # [V4] 병원 규모별 분포 (의사 수 기준)
    if '총의사수' in df.columns:
        def categorize_size(x):
            if x <= 1: return '소형 (1인)'
            if x <= 3: return '중소형 (2-3인)'
            if x <= 10: return '중형 (4-10인)'
            return '대형 (11인 이상)'
        
        df['병원규모_derived'] = df['총의사수'].apply(categorize_size)
        plt.figure(figsize=(10, 6))
        size_counts = df['병원규모_derived'].value_counts().reindex(['소형 (1인)', '중소형 (2-3인)', '중형 (4-10인)', '대형 (11인 이상)']).fillna(0)
        ax = sns.barplot(x=size_counts.index, y=size_counts.values, hue=size_counts.index, palette="coolwarm", legend=False)
        
        # 데이터 라벨 추가
        for i, v in enumerate(size_counts.values):
            ax.text(i, v + 20, f'{int(v):,}건', ha='center', fontweight='bold')

        plt.title("강남구 병원 규모별 분포 (의사 수 기준)", fontsize=15)
        plt.xlabel("규모")
        plt.ylabel("병원 수")
        path = os.path.join(output_dir, "v4_size_distribution.png")
        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()
        viz_files.append(("병원 규모별 분포", "v4_size_distribution.png", "의사 수에 따른 병원 규모 분포입니다. 대부분의 병원이 1인 중심의 소형 병원입니다."))

    # [V5] 연도별 개원 추이 (Line Chart)
    if '개설일자' in df.columns:
        # 날짜 형식이 YYYY-MM-DD 또는 YYYYMMDD일 수 있으므로 유연하게 처리
        df['설립연도_derived'] = pd.to_datetime(df['개설일자'], errors='coerce').dt.year
        
        # 유효한 연도만 추출 (1990년 이후 ~ 현재)
        current_year = datetime.now().year
        year_counts = df[(df['설립연도_derived'] >= 1990) & (df['설립연도_derived'] <= current_year)]['설립연도_derived'].value_counts().sort_index()
        
        if not year_counts.empty:
            plt.figure(figsize=(14, 7))
            
            # 연도별 개원 수 (Bar)
            ax1 = sns.barplot(x=year_counts.index, y=year_counts.values, alpha=0.6, color='skyblue', label='연도별 개원 수')
            
            # 바 위에 수치 추가
            for i, v in enumerate(year_counts.values):
                ax1.text(i, v + 2, str(int(v)), ha='center', fontsize=9, fontweight='bold')

            # 누적 개원 수 (Line)
            ax2 = ax1.twinx()
            cumulative_counts = year_counts.cumsum()
            ax2.plot(range(len(year_counts)), cumulative_counts.values, marker='o', color='darkblue', linewidth=2, label='누적 병원 수')
            
            # 누적 수치 라벨 추가 (일부 지점만)
            for i, v in enumerate(cumulative_counts.values):
                if i % 2 == 0 or i == len(cumulative_counts) - 1:
                    ax2.text(i, v + 50, f'{int(v):,}', ha='center', color='darkblue', fontsize=9, fontweight='bold')

            plt.title("강남구 연도별 병원 개원 추이 및 누적 현황 (1990년 이후)", fontsize=15)
            ax1.set_xlabel("개설 연도")
            ax1.set_ylabel("신규 개원 수")
            ax2.set_ylabel("누적 병원 수")
            
            # X축 레이블 간격 조정 (너무 많으면 겹치므로)
            ax1.set_xticks(range(0, len(year_counts), 2))
            ax1.set_xticklabels(year_counts.index[::2], rotation=45)
            
            path = os.path.join(output_dir, "v5_opening_trend.png")
            plt.tight_layout()
            plt.savefig(path, dpi=300)
            plt.close()
            viz_files.append(("연도별 개원 추이", "v5_opening_trend.png", "강남구의 연도별 신규 개원 현황과 누적 병원 수 추이입니다. 최근으로 올수록 개원 속도가 빨라지며 시장이 성숙해지는 과정을 볼 수 있습니다."))

    return viz_files

# 4. HTML 보고서 생성 함수
def create_html_report(viz_files, output_dir):
    report_path = os.path.join(output_dir, "강남구_병원_현황_보고서.html")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>강남구 병원 현황 시각화 보고서</title>
        <style>
            body {{ font-family: 'Malgun Gothic', dotum, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; }}
            h1 {{ text-align: center; color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }}
            .summary {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px; }}
            .chart-container {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px; text-align: center; }}
            .chart-title {{ font-size: 1.2em; font-weight: bold; color: #2980b9; margin-bottom: 15px; }}
            .chart-desc {{ color: #666; font-size: 0.9em; margin-top: 10px; text-align: left; }}
            img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }}
            .footer {{ text-align: center; color: #7f8c8d; font-size: 0.8em; margin-top: 50px; }}
        </style>
    </head>
    <body>
        <h1>강남구 병원 현황 시각화 보고서</h1>
        
        <div class="summary">
            <h2>데이터 요약</h2>
            <ul>
                <li><strong>지역</strong>: 서울특별시 강남구</li>
                <li><strong>기준 시점</strong>: 2025년 12월</li>
                <li><strong>총 병원 수</strong>: {len(df):,}개</li>
                <li><strong>분석 항목</strong>: 행정동별 분포, 종별 비중, 주요 진료과목, 규모 분포, 개원 추이</li>
            </ul>
        </div>
    """

    for title, filename, desc in viz_files:
        html_content += f"""
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <img src="{filename}" alt="{title}">
            <div class="chart-desc">{desc}</div>
        </div>
        """

    html_content += f"""
        <div class="footer">
            본 보고서는 Antigravity AI Assistant에 의해 생성되었습니다. ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        </div>
    </body>
    </html>
    """

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Report generated: {report_path}")

# 실행
if __name__ == "__main__":
    print("Generating visualizations...")
    viz_files = generate_visualizations(df, OUTPUT_DIR)
    
    print("Creating HTML report...")
    create_html_report(viz_files, OUTPUT_DIR)
    
    print("All tasks completed successfully.")
