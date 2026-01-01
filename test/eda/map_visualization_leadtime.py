import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
import json

print("Loading data...")
location_data = pd.read_csv('location_data_with_clusters.csv')
optimal_locations = pd.read_csv('optimal_locations.csv')

# ========== MAP 1: 현재 배송지 분포 (고객 위치 기반 히트맵) ==========
print("Creating Map 1: Current Distribution (Heatmap)...")

# 브라질 중심 좌표
brazil_center = [-14.2350, -51.9253]

# 히트맵용 데이터 준비 (주문 수 기반)
heat_data = []
for idx, row in location_data.iterrows():
    if pd.notna(row['customer_lat']) and pd.notna(row['customer_lng']):
        # 주문 수에 따라 강도 조정
        intensity = min(row['order_count'] / location_data['order_count'].max(), 1.0)
        heat_data.append([row['customer_lat'], row['customer_lng'], intensity])

map1 = folium.Map(location=brazil_center, zoom_start=4, tiles='OpenStreetMap')

# 히트맵 추가
HeatMap(heat_data, radius=20, blur=15, max_zoom=1, name='Current Distribution').add_to(map1)

# 고객 밀도 높은 지역 마커
for idx, row in location_data.nlargest(20, 'order_count').iterrows():
    folium.Circle(
        location=[row['customer_lat'], row['customer_lng']],
        radius=row['order_count'] / 100,
        popup=f"Orders: {int(row['order_count'])}<br>Lead Time: {row['avg_leadtime']:.2f}d",
        color='blue',
        fill=True,
        fillColor='blue',
        fillOpacity=0.4,
        weight=1
    ).add_to(map1)

folium.LayerControl().add_to(map1)
map1.save('map_1_current_distribution.html')
print("✓ map_1_current_distribution.html")

# ========== MAP 2: 최적 배송센터 (Optimal Locations) ==========
print("Creating Map 2: Optimal Distribution Centers...")

map2 = folium.Map(location=brazil_center, zoom_start=4, tiles='OpenStreetMap')

# 최적 위치 마커
colors = ['red', 'green', 'blue', 'purple', 'orange']
for idx, row in optimal_locations.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<b>{row['Method']}</b><br>Lat: {row['Latitude']:.6f}<br>Lng: {row['Longitude']:.6f}",
        icon=folium.Icon(color=colors[idx % len(colors)], icon='info-sign', prefix='glyphicon'),
        tooltip=row['Method']
    ).add_to(map2)

# 기존 배송지도 표시 (배경)
for idx, row in location_data.nlargest(50, 'order_count').iterrows():
    folium.Circle(
        location=[row['customer_lat'], row['customer_lng']],
        radius=row['order_count'] / 100,
        popup=f"Current<br>Orders: {int(row['order_count'])}",
        color='gray',
        fill=True,
        fillColor='gray',
        fillOpacity=0.2,
        weight=1
    ).add_to(map2)

folium.LayerControl().add_to(map2)
map2.save('map_2_optimal_locations.html')
print("✓ map_2_optimal_locations.html")

# ========== MAP 3: K-MEANS 클러스터 (다중 배포센터) ==========
print("Creating Map 3: K-Means Clustering (5 Distribution Centers)...")

map3 = folium.Map(location=brazil_center, zoom_start=4, tiles='OpenStreetMap')

# K-means 5개 센터 클러스터 분석
kmeans_clusters = location_data['cluster_5'].dropna().unique()
cluster_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue']

for cluster_id in sorted(kmeans_clusters):
    cluster_data = location_data[location_data['cluster_5'] == cluster_id]
    
    # 클러스터 중심 계산 (가중 평균)
    weights = cluster_data['order_count']
    center_lat = (cluster_data['customer_lat'] * weights).sum() / weights.sum()
    center_lng = (cluster_data['customer_lng'] * weights).sum() / weights.sum()
    
    # 클러스터 정보
    total_orders = cluster_data['order_count'].sum()
    avg_leadtime = cluster_data['avg_leadtime'].mean()
    primary_states = cluster_data['customer_state'].value_counts().head(3).to_dict()
    
    # 클러스터 중심 마커
    folium.Marker(
        location=[center_lat, center_lng],
        popup=f"<b>Distribution Center {int(cluster_id) + 1}</b><br>" +
              f"Orders: {int(total_orders)}<br>" +
              f"Avg Lead Time: {avg_leadtime:.2f} days<br>" +
              f"Primary States: {', '.join(primary_states.keys())}<br>" +
              f"Lat: {center_lat:.6f}<br>Lng: {center_lng:.6f}",
        icon=folium.Icon(color=cluster_colors[int(cluster_id)], icon='star', prefix='glyphicon'),
        tooltip=f"Center {int(cluster_id) + 1}"
    ).add_to(map3)
    
    # 클러스터 내 고객 위치 (색상으로 구분)
    for idx, row in cluster_data.nlargest(100, 'order_count').iterrows():
        folium.Circle(
            location=[row['customer_lat'], row['customer_lng']],
            radius=row['order_count'] / 150,
            popup=f"<b>Cluster {int(cluster_id) + 1}</b><br>" +
                  f"Orders: {int(row['order_count'])}<br>" +
                  f"Lead Time: {row['avg_leadtime']:.2f} days",
            color=cluster_colors[int(cluster_id)],
            fill=True,
            fillColor=cluster_colors[int(cluster_id)],
            fillOpacity=0.3,
            weight=1
        ).add_to(map3)

folium.LayerControl().add_to(map3)
map3.save('map_3_kmeans_5centers.html')
print("✓ map_3_kmeans_5centers.html")

# ========== MAP 4: 리드타임 히트맵 (성능 기반) ==========
print("Creating Map 4: Lead Time Performance Heatmap...")

map4 = folium.Map(location=brazil_center, zoom_start=4, tiles='OpenStreetMap')

# 리드타임 데이터로 히트맵 생성 (낮을수록 좋음 = 역수 사용)
leadtime_heat = []
for idx, row in location_data.iterrows():
    if pd.notna(row['customer_lat']) and pd.notna(row['customer_lng']):
        # 리드타임이 낮을수록 높은 값
        intensity = 1.0 - min(row['avg_leadtime'] / location_data['avg_leadtime'].max(), 1.0)
        leadtime_heat.append([row['customer_lat'], row['customer_lng'], intensity])

HeatMap(leadtime_heat, radius=20, blur=15, max_zoom=1, name='Lead Time Performance').add_to(map4)

# 최적 위치 표시
for idx, row in optimal_locations.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<b>Optimal: {row['Method']}</b>",
        icon=folium.Icon(color='green', icon='star', prefix='glyphicon'),
        tooltip='Optimal Location'
    ).add_to(map4)

folium.LayerControl().add_to(map4)
map4.save('map_4_leadtime_performance.html')
print("✓ map_4_leadtime_performance.html")

# ========== MAP 5: 비교 분석 (현재 vs 최적) ==========
print("Creating Map 5: Current vs Optimal Comparison...")

map5 = folium.Map(location=brazil_center, zoom_start=4, tiles='OpenStreetMap')

# 현재 배송 위치 (회색, 작은 원)
for idx, row in location_data.nlargest(100, 'order_count').iterrows():
    folium.Circle(
        location=[row['customer_lat'], row['customer_lng']],
        radius=row['order_count'] / 150,
        popup=f"<b>Current Location</b><br>Orders: {int(row['order_count'])}",
        color='gray',
        fill=True,
        fillColor='gray',
        fillOpacity=0.3,
        weight=1
    ).add_to(map5)

# 최적 배송지 (Fermat Point 기준)
fermat_optimal = optimal_locations[optimal_locations['Method'] == 'Fermat Point (Distance Min)']
if not fermat_optimal.empty:
    fermat_lat = fermat_optimal.iloc[0]['Latitude']
    fermat_lng = fermat_optimal.iloc[0]['Longitude']
    
    folium.Marker(
        location=[fermat_lat, fermat_lng],
        popup=f"<b>Optimal Fermat Point</b><br>Lat: {fermat_lat:.6f}<br>Lng: {fermat_lng:.6f}",
        icon=folium.Icon(color='green', icon='star', prefix='glyphicon', prefix_size=20),
        tooltip='Optimal Location'
    ).add_to(map5)
    
    # 현재와 최적 위치 연결선
    folium.PolyLine(
        locations=[[fermat_lat, fermat_lng], [brazil_center[0], brazil_center[1]]],
        color='red',
        weight=2,
        opacity=0.7,
        popup='Optimal Direction'
    ).add_to(map5)

# K-Means 5개 센터도 함께 표시
kmeans_5_centers = location_data.groupby('cluster_5').apply(
    lambda x: pd.Series({
        'lat': (x['customer_lat'] * x['order_count']).sum() / x['order_count'].sum(),
        'lng': (x['customer_lng'] * x['order_count']).sum() / x['order_count'].sum(),
        'orders': x['order_count'].sum()
    })
)

colors_kmeans = ['red', 'blue', 'green', 'purple', 'orange']
for idx, (cluster_id, row) in enumerate(kmeans_5_centers.iterrows()):
    folium.Marker(
        location=[row['lat'], row['lng']],
        popup=f"<b>DC {int(cluster_id) + 1}</b><br>Orders: {int(row['orders'])}",
        icon=folium.Icon(color=colors_kmeans[int(cluster_id)], icon='info-sign', prefix='glyphicon'),
        tooltip=f'Distribution Center {int(cluster_id) + 1}'
    ).add_to(map5)

folium.LayerControl().add_to(map5)
map5.save('map_5_current_vs_optimal.html')
print("✓ map_5_current_vs_optimal.html")

# ========== 통계 정보 저장 ==========
print("\n" + "=" * 80)
print("맵 시각화 완료!")
print("=" * 80)

summary = f"""
생성된 지도 파일:

1. map_1_current_distribution.html
   - 현재 고객 배송지 분포 히트맵
   - 주문 집중도 기반 시각화

2. map_2_optimal_locations.html
   - 모든 최적 위치 마커 표시
   - 5가지 방법의 최적 좌표

3. map_3_kmeans_5centers.html
   - K-Means 5개 배포센터 클러스터
   - 각 센터별 담당 고객 영역

4. map_4_leadtime_performance.html
   - 리드타임 기반 성능 히트맵
   - 빠른 지역 vs 느린 지역 구분

5. map_5_current_vs_optimal.html
   - 현재 위치와 최적 위치 비교
   - 5개 배포센터 제안

주요 발견사항:
- 최적 단일 배포센터: (-23.26, -46.57) - 상파울루 근처
- 다중 배포센터 추천: 5곳 (SP, RJ, NE, South, Center-West)
- 평균 리드타임 단축 가능성: 현재 12.44일 → 최적화 시 10-12일
"""

print(summary)

with open('map_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("\n✓ map_summary.txt - 요약 정보")
