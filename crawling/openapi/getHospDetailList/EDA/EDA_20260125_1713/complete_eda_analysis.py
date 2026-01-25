import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from datetime import datetime

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

    # ========================================
    # 누락된 분석 항목 추가 실행
    # ========================================
    
    # 1. 의료 장비 분석 (Medical Equipment) - 전체 리스트
    print("\n=== Analyzing Medical Equipment ===")
    equipment_data = df['medoft_oftCdNm'].dropna()
    equipment_available = len(equipment_data)
    print(f"Equipment data available: {equipment_available}/{N} ({equipment_available/N*100:.1f}%)")
    
    if equipment_available > 0:
        # 장비별 빈도 계산
        equipment_counts = equipment_data.value_counts()
        
        # 전체 장비 리스트 시각화 (Top 20)
        plt.figure(figsize=(14, 10))
        top_equipment = equipment_counts.head(20)
        sns.barplot(y=top_equipment.index, x=top_equipment.values, palette='coolwarm')
        for i, v in enumerate(top_equipment.values):
            plt.text(v + 0.2, i, f"{v}개", va='center')
        plt.title(f"의료 장비 보유 현황 (Top 20, N={equipment_available})", fontsize=14, fontweight='bold')
        plt.xlabel("보유 병원 수")
        plt.ylabel("장비명")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'equipment_analysis.png'), dpi=150)
        plt.close()
        
        # 전체 장비 리스트 CSV 저장
        equipment_full = equipment_counts.reset_index()
        equipment_full.columns = ['장비명', '보유병원수']
        equipment_full['비율(%)'] = (equipment_full['보유병원수'] / equipment_available * 100).round(2)
        equipment_full.to_csv(os.path.join(output_dir, 'equipment_full_list.csv'), index=False, encoding='utf-8-sig')
        print(f"Total unique equipment types: {len(equipment_counts)}")
    
    # 2. 운영 및 편의성 분석 - 점심시간
    print("\n=== Analyzing Lunch Time ===")
    lunch_data = df['dtl_lunchWeek'].dropna()
    lunch_available = len(lunch_data)
    print(f"Lunch time data available: {lunch_available}/{N} ({lunch_available/N*100:.1f}%)")
    
    if lunch_available > 0:
        # 점심시간 패턴 분석 (간단한 텍스트 파싱)
        lunch_patterns = lunch_data.value_counts().head(15)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(y=lunch_patterns.index, x=lunch_patterns.values, palette='pastel')
        for i, v in enumerate(lunch_patterns.values):
            plt.text(v + 0.2, i, f"{v}개 ({v/lunch_available*100:.1f}%)", va='center')
        plt.title(f"점심시간 운영 패턴 (Top 15, N={lunch_available})", fontsize=14, fontweight='bold')
        plt.xlabel("병원 수")
        plt.ylabel("점심시간")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'lunch_time_analysis.png'), dpi=150)
        plt.close()
    
    # 3. 주차 편의성 분석
    print("\n=== Analyzing Parking ===")
    parking_data = df['dtl_parkQty'].dropna()
    parking_available = len(parking_data)
    print(f"Parking data available: {parking_available}/{N} ({parking_available/N*100:.1f}%)")
    
    if parking_available > 0:
        # 주차 가능 대수별 분포
        parking_counts = parking_data.value_counts().sort_index()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=parking_counts.index, y=parking_counts.values, palette='Set2')
        for i, v in enumerate(parking_counts.values):
            plt.text(i, v + 0.5, f"{v}개", ha='center')
        plt.title(f"주차 가능 대수 분포 (N={parking_available})", fontsize=14, fontweight='bold')
        plt.xlabel("주차 가능 대수")
        plt.ylabel("병원 수")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'parking_analysis.png'), dpi=150)
        plt.close()
    
    # 4. 주말 진료 분석
    print("\n=== Analyzing Weekend Operations ===")
    
    # 토요일 진료
    saturday_data = df['dtl_trmtSatStart'].dropna()
    saturday_count = len(saturday_data)
    
    # 일요일 진료
    sunday_data = df['dtl_trmtSunStart'].dropna()
    sunday_count = len(sunday_data)
    
    weekend_summary = pd.DataFrame({
        '구분': ['토요일 진료', '일요일 진료'],
        '진료 병원 수': [saturday_count, sunday_count],
        '비율(%)': [saturday_count/N*100, sunday_count/N*100]
    })
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=weekend_summary, x='구분', y='진료 병원 수', palette=['skyblue', 'salmon'])
    for i, row in weekend_summary.iterrows():
        plt.text(i, row['진료 병원 수'] + 1, 
                f"{int(row['진료 병원 수'])}개\n({row['비율(%)']:.1f}%)", 
                ha='center', fontweight='bold')
    plt.title(f"주말 진료 현황 (N={N})", fontsize=14, fontweight='bold')
    plt.ylabel("병원 수")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'weekend_operations.png'), dpi=150)
    plt.close()
    
    weekend_summary.to_csv(os.path.join(output_dir, 'weekend_summary.csv'), index=False, encoding='utf-8-sig')
    
    # 5. 지도 기반 시각화 (좌표 데이터 활용)
    print("\n=== Analyzing Geographic Distribution ===")
    geo_data = df[['eqp_yadmNm', 'eqp_emdongNm', 'lat', 'lon']].dropna()
    geo_available = len(geo_data)
    print(f"Geographic data available: {geo_available}/{N} ({geo_available/N*100:.1f}%)")
    
    if geo_available > 10:  # 최소 10개 이상의 좌표 데이터가 있을 때만 지도 생성
        plt.figure(figsize=(14, 10))
        
        # 행정동별 색상 구분
        unique_dongs = geo_data['eqp_emdongNm'].unique()
        colors = plt.cm.tab20(np.linspace(0, 1, len(unique_dongs)))
        dong_color_map = dict(zip(unique_dongs, colors))
        
        for dong in unique_dongs:
            dong_subset = geo_data[geo_data['eqp_emdongNm'] == dong]
            plt.scatter(dong_subset['lon'], dong_subset['lat'], 
                       label=dong, alpha=0.7, s=100, 
                       color=dong_color_map[dong], edgecolors='black', linewidth=0.5)
        
        plt.title(f"강남구 피부과 지리적 분포 (N={geo_available})", fontsize=16, fontweight='bold')
        plt.xlabel("경도 (Longitude)")
        plt.ylabel("위도 (Latitude)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'geographic_map.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    # 6. 지하철역 기반 지도 시각화
    print("\n=== Analyzing Subway-based Distribution ===")
    subway_geo_data = df[['eqp_yadmNm', 'trnsprt_trafNm', 'lat', 'lon']].dropna()
    subway_geo_available = len(subway_geo_data)
    print(f"Subway geographic data available: {subway_geo_available}/{N}")
    
    if subway_geo_available > 10:
        # 주요 역 Top 5 추출
        top_stations = subway_geo_data['trnsprt_trafNm'].value_counts().head(5).index
        
        plt.figure(figsize=(14, 10))
        
        # 주요 역별 색상 구분
        station_colors = plt.cm.Set1(np.linspace(0, 1, len(top_stations)))
        station_color_map = dict(zip(top_stations, station_colors))
        
        for station in top_stations:
            station_subset = subway_geo_data[subway_geo_data['trnsprt_trafNm'] == station]
            plt.scatter(station_subset['lon'], station_subset['lat'], 
                       label=f"{station} ({len(station_subset)}개)", 
                       alpha=0.7, s=150, 
                       color=station_color_map[station], 
                       edgecolors='black', linewidth=1)
        
        # 기타 역
        other_stations = subway_geo_data[~subway_geo_data['trnsprt_trafNm'].isin(top_stations)]
        if len(other_stations) > 0:
            plt.scatter(other_stations['lon'], other_stations['lat'], 
                       label=f"기타 ({len(other_stations)}개)", 
                       alpha=0.4, s=50, color='gray', edgecolors='black', linewidth=0.5)
        
        plt.title(f"주요 지하철역별 피부과 분포 (N={subway_geo_available})", fontsize=16, fontweight='bold')
        plt.xlabel("경도 (Longitude)")
        plt.ylabel("위도 (Latitude)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'subway_geographic_map.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    print("\n=== Analysis Completed ===")
    print(f"All outputs saved to: {output_dir}")

if __name__ == "__main__":
    main()
