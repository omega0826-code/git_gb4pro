import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
import re

# 한글 폰트 설정 (Windows 기준 Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 경로 설정
    input_path = r'd:\git_gb4pro\gis\geocoding\hospital\data\output\강남구_피부과_데이터_20260125_170356.csv'
    output_dir = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_20260125_1713'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading data: {input_path}")
    df = pd.read_csv(input_path, encoding='utf-8-sig')
    N = len(df)
    print(f"Analysis target: N={N}")

    # 1. 인력 분석 (Staff Analysis)
    # dgsbjt_dgsbjtPrSdrCnt (전문의 수)
    print("Analyzing Staff...")
    plt.figure(figsize=(10, 6))
    staff_counts = df['dgsbjt_dgsbjtPrSdrCnt'].value_counts().sort_index()
    sns.barplot(x=staff_counts.index, y=staff_counts.values, color='skyblue')
    for i, v in enumerate(staff_counts.values):
        plt.text(i, v + 0.5, str(v), ha='center')
    plt.title(f"피부과 전문의 수 분포 (N={N})")
    plt.xlabel("전문의 수")
    plt.ylabel("병원 수")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, 'staff_distribution.png'))
    plt.close()

    # 2. 병상 규모 분석 (Bed Scale Analysis)
    print("Analyzing Bed Scale...")
    df['has_bed'] = df['eqp_stdSickbdCnt'].fillna(0) > 0
    bed_count = df['has_bed'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(bed_count, labels=['병상 없음', '병상 보유'], autopct=lambda p: '{:.1f}%({:.0f})'.format(p, p * sum(bed_count) / 100), colors=['lightgrey', 'salmon'])
    plt.title(f"병상 보유 여부 현황 (N={N})")
    plt.savefig(os.path.join(output_dir, 'bed_scale.png'))
    plt.close()

    # 3. 운영 (Operation) - 점심시간 (텍스트 파싱 필요하지만 일단 존재 여부 및 패턴 확인용 빈도)
    print("Analyzing Operation (Lunch Time)...")
    lunch_data = df['dtl_lunchWeek'].dropna()
    print(f"Lunch data availability: {len(lunch_data)}/{N}")
    
    # 4. 행정동별 분포 (Location)
    print("Analyzing Location...")
    plt.figure(figsize=(12, 6))
    dong_counts = df['eqp_emdongNm'].value_counts().head(10)
    sns.barplot(x=dong_counts.index, y=dong_counts.values, palette='viridis')
    for i, v in enumerate(dong_counts.values):
        plt.text(i, v + 0.5, f"{v} ({v/N*100:.1f}%)", ha='center')
    plt.title(f"강남구 행정동별 피부과 분포 (Top 10, N={N})")
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, 'location_distribution.png'))
    plt.close()

    # 5. 지하철역별 분포
    print("Analyzing Subway Stations...")
    plt.figure(figsize=(12, 6))
    subway_counts = df['trnsprt_trafNm'].value_counts().head(10)
    sns.barplot(x=subway_counts.index, y=subway_counts.values, palette='magma')
    for i, v in enumerate(subway_counts.values):
        percent = (v / N) * 100
        plt.text(i, v + 0.5, f"{v} ({percent:.1f}%)", ha='center')
    plt.title(f"주요 지하철역별 병원 밀집도 (Top 10, N={N})")
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, 'subway_distribution.png'))
    plt.close()

    # 결측치 요약
    print("Generating Quality Report...")
    missing_info = df.isnull().sum()
    missing_df = missing_info[missing_info > 0].reset_index()
    missing_df.columns = ['Column', 'MissingCount']
    missing_df['Ratio'] = (missing_df['MissingCount'] / N) * 100
    missing_df.to_csv(os.path.join(output_dir, 'quality_report.csv'), index=False, encoding='utf-8-sig')

    print("EDA Process Completed.")

if __name__ == "__main__":
    main()
