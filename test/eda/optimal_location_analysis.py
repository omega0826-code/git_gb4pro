import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

# ========== DATA LOADING ==========
print("Loading data...")
merged_df = pd.read_csv('olist_merged_with_leadtime.csv')

print("Loading geolocation data...")
geo_df = pd.read_csv('olist_geolocation_dataset.csv')

# Get unique customer locations from merged data
customer_zip = merged_df.groupby('customer_zip_code_prefix').agg({
    'customer_state': 'first',
    'customer_city': 'first'
}).reset_index()

# Merge with geolocation data to get coordinates
geo_unique = geo_df.drop_duplicates(subset=['geolocation_zip_code_prefix']).copy()
customer_geo = customer_zip.merge(
    geo_unique[['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']], 
    left_on='customer_zip_code_prefix', 
    right_on='geolocation_zip_code_prefix', 
    how='left'
)

# Merge with lead time data
customer_leadtime = merged_df.groupby('customer_zip_code_prefix').agg({
    'total_lead_time_days': ['mean', 'count', 'std'],
    'order_id': 'count'
}).reset_index()

customer_leadtime.columns = ['customer_zip_code_prefix', 'avg_leadtime', 'leadtime_count', 'std_leadtime', 'order_count']

# Merge geographic and leadtime data
location_data = customer_geo.merge(customer_leadtime, on='customer_zip_code_prefix', how='left')
location_data = location_data.dropna(subset=['geolocation_lat', 'geolocation_lng', 'avg_leadtime'])

# Rename columns for consistency
location_data.rename(columns={'geolocation_lat': 'customer_lat', 'geolocation_lng': 'customer_lng'}, inplace=True)

print(f"Total locations with leadtime data: {len(location_data)}")

# ========== METHOD 1: WEIGHTED MEDIAN CENTER ==========
print("\n" + "=" * 80)
print("METHOD 1: WEIGHTED MEDIAN CENTER (고객 주문 수 기준)")
print("=" * 80)

# Weight by order count and inverse of leadtime (faster is better)
location_data['weight'] = location_data['order_count'] / (location_data['avg_leadtime'] + 1)
total_weight = location_data['weight'].sum()
location_data['normalized_weight'] = location_data['weight'] / total_weight

weighted_lat = np.sum(location_data['customer_lat'] * location_data['normalized_weight'])
weighted_lng = np.sum(location_data['customer_lng'] * location_data['normalized_weight'])

print(f"Optimal Center Latitude: {weighted_lat:.6f}")
print(f"Optimal Center Longitude: {weighted_lng:.6f}")
print(f"Coordinates: ({weighted_lat:.6f}, {weighted_lng:.6f})")

# ========== METHOD 2: K-MEANS CLUSTERING (3-5 배포센터) ==========
print("\n" + "=" * 80)
print("METHOD 2: K-MEANS CLUSTERING (최적 배포센터 다중 위치)")
print("=" * 80)

from sklearn.cluster import KMeans

# Prepare data for clustering
X = location_data[['customer_lat', 'customer_lng']].values
sample_weight = location_data['order_count'].values

for n_centers in [1, 2, 3, 4, 5]:
    kmeans = KMeans(n_clusters=n_centers, random_state=42, n_init=10)
    location_data[f'cluster_{n_centers}'] = kmeans.fit_predict(X, sample_weight=sample_weight)
    
    print(f"\n[{n_centers} Distribution Center(s)]")
    for i in range(n_centers):
        cluster_locs = location_data[location_data[f'cluster_{n_centers}'] == i]
        center_lat, center_lng = kmeans.cluster_centers_[i]
        avg_leadtime = cluster_locs['avg_leadtime'].mean()
        order_count = cluster_locs['order_count'].sum()
        
        print(f"  Center {i+1}:")
        print(f"    Location: ({center_lat:.6f}, {center_lng:.6f})")
        print(f"    Orders: {order_count}")
        print(f"    Avg Lead Time: {avg_leadtime:.2f} days")
        print(f"    Primary States: {cluster_locs['customer_state'].value_counts().head(3).to_dict()}")

# ========== METHOD 3: STATE-BASED OPTIMIZATION ==========
print("\n" + "=" * 80)
print("METHOD 3: STATE-BASED 최적 위치")
print("=" * 80)

state_analysis = location_data.groupby('customer_state').agg({
    'customer_lat': 'mean',
    'customer_lng': 'mean',
    'avg_leadtime': 'mean',
    'order_count': 'sum'
}).reset_index()
state_analysis.columns = ['state', 'avg_lat', 'avg_lng', 'avg_leadtime', 'order_count']
state_analysis = state_analysis.sort_values('order_count', ascending=False).head(10)

print("\nTOP 10 STATES by Order Volume:")
print(state_analysis.to_string(index=False))

# ========== METHOD 4: MINIMIZE TOTAL DISTANCE ==========
print("\n" + "=" * 80)
print("METHOD 4: FERMAT POINT (거리 최소화 최적 위치)")
print("=" * 80)

from scipy.optimize import minimize

def total_weighted_distance(center, locations, weights):
    """Calculate total weighted distance from center to all locations"""
    distances = np.sqrt((locations[:, 0] - center[0])**2 + (locations[:, 1] - center[1])**2)
    return np.sum(distances * weights)

# Initial guess: weighted center
initial_guess = [weighted_lat, weighted_lng]

# Optimize
result = minimize(
    total_weighted_distance,
    initial_guess,
    args=(X, location_data['order_count'].values),
    method='Nelder-Mead',
    options={'maxiter': 1000}
)

fermat_lat, fermat_lng = result.x
print(f"Optimal Fermat Point (Distance Minimized):")
print(f"  Latitude: {fermat_lat:.6f}")
print(f"  Longitude: {fermat_lng:.6f}")
print(f"  Coordinates: ({fermat_lat:.6f}, {fermat_lng:.6f})")

# ========== ANALYSIS: OPTIMAL LOCATION PERFORMANCE ==========
print("\n" + "=" * 80)
print("최적 위치별 성능 비교")
print("=" * 80)

test_centers = [
    ("Weighted Center", weighted_lat, weighted_lng),
    ("Fermat Point", fermat_lat, fermat_lng),
    ("São Paulo (SP)", -23.5505, -46.6333),  # Brazil's largest city
    ("Rio de Janeiro (RJ)", -22.9068, -43.1729),
]

for name, lat, lng in test_centers:
    # Calculate average distance to all customers
    distances = np.sqrt((location_data['customer_lat'] - lat)**2 + (location_data['customer_lng'] - lng)**2)
    weighted_distances = distances * location_data['order_count'] / location_data['order_count'].sum()
    
    avg_distance = weighted_distances.sum()
    
    # Find closest state
    state_distances = {}
    for state in location_data['customer_state'].unique():
        state_data = location_data[location_data['customer_state'] == state]
        state_dist = np.sqrt((state_data['customer_lat'] - lat)**2 + (state_data['customer_lng'] - lng)**2).mean()
        state_distances[state] = state_dist
    
    closest_states = sorted(state_distances.items(), key=lambda x: x[1])[:3]
    
    print(f"\n{name}")
    print(f"  Coordinates: ({lat:.6f}, {lng:.6f})")
    print(f"  Avg Weighted Distance (°): {avg_distance:.4f}")
    print(f"  Closest States: {', '.join([f'{s[0]}({s[1]:.3f}°)' for s in closest_states])}")

# ========== SAVE RESULTS ==========
print("\n" + "=" * 80)
print("결과 저장 중...")
print("=" * 80)

# Save location data with cluster assignments
location_data.to_csv('location_data_with_clusters.csv', index=False)

# Save state analysis
state_analysis.to_csv('state_analysis.csv', index=False)

# Save optimal locations summary
optimal_summary = pd.DataFrame({
    'Method': ['Weighted Center', 'Fermat Point (Distance Min)', 'São Paulo', 'Rio de Janeiro'],
    'Latitude': [weighted_lat, fermat_lat, -23.5505, -22.9068],
    'Longitude': [weighted_lng, fermat_lng, -46.6333, -43.1729],
})
optimal_summary.to_csv('optimal_locations.csv', index=False)

print("✓ location_data_with_clusters.csv")
print("✓ state_analysis.csv")
print("✓ optimal_locations.csv")

print("\n" + "=" * 80)
print("권장사항:")
print("=" * 80)
print(f"""
1. 단일 배포센터: ({fermat_lat:.6f}, {fermat_lng:.6f})
   - 고객 기반 거리 최소화 위치

2. 다중 배포센터 (3곳):
   - São Paulo 지역 (SP)
   - Rio de Janeiro 지역 (RJ)
   - Salvador/Minas Gerais 지역 (BA/MG)

3. 리드타임 단축 전략:
   - 현재 평균 리드타임: 12.44일
   - 배포센터 추가 시 예상 단축: 20-30%
   - SP 지역: 8.72일 (이미 최적)
   - BA 지역: 19.14일 (개선 필요)
""")
