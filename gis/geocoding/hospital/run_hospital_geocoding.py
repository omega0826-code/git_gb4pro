import pandas as pd
import requests
import os
import time
import re
import sys
from dotenv import load_dotenv

# .env 파일 활성화
load_dotenv()

def clean_address(addr):
    if not isinstance(addr, str): 
        return ""
    addr = re.sub(r'\(.*?\)', '', addr)
    addr = re.sub(r'\d+층', '', addr)
    addr = re.sub(r'지하\s*\d+층', '', addr)
    if ',' in addr:
        addr = addr.split(',')[0]
    addr = " ".join(addr.split())
    return addr

def geocode_address(address):
    api_key = os.getenv("KAKAO_API_KEY")
    if not api_key:
        return None, None
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        result = resp.json()
        if result['documents']:
            doc = result['documents'][0]
            return float(doc['y']), float(doc['x'])
    except Exception:
        pass
    return None, None

def validate_geocoding_setup(df, sample_size=3):
    print(f"--- Pre-run Validation: Testing {sample_size} samples ---", flush=True)
    samples = df.head(sample_size)
    success_count = 0
    for idx, row in samples.iterrows():
        clean_addr = clean_address(row['원본_주소'])
        lat, lon = geocode_address(clean_addr)
        if lat and lon:
            success_count += 1
            print(f"Success: {clean_addr} -> ({lat}, {lon})", flush=True)
        else:
            print(f"Fail: {clean_addr}", flush=True)
    if success_count == 0:
        print("\n[ERROR] 사전 테스트 결과가 0건입니다. API 키 또는 네트워크 상태를 확인하십시오.", flush=True)
        return False
    print(f"--- Validation Complete: {success_count}/{sample_size} success --- \n", flush=True)
    return True

def main():
    input_path = 'gis/geocoding/hospital/data/input/병원전체정보_20260116_212603.csv'
    output_dir = 'gis/geocoding/hospital/data/output'
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f'병원전체정보_20260116_212603_geocoded_{timestamp}.csv')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading data: {input_path}", flush=True)
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception:
        df = pd.read_csv(input_path, encoding='cp949')
    
    if not validate_geocoding_setup(df, sample_size=3):
        sys.exit(1)
        
    print(f"Starting bulk geocoding process for {len(df)} rows...", flush=True)
    df['geo_address'] = df['원본_주소'].apply(clean_address)
    
    results = []
    total = len(df)
    for idx, row in df.iterrows():
        lat, lon = geocode_address(row['geo_address'])
        results.append({'lat': lat, 'lon': lon})
        if (idx + 1) % 50 == 0 or (idx + 1) == total:
            print(f"Progress: {idx + 1}/{total} ({(idx+1)/total*100:.1f}%)", flush=True)
        time.sleep(0.05)
        
    res_df = pd.DataFrame(results)
    df['lat'] = res_df['lat']
    df['lon'] = res_df['lon']
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nProcessing Complete. Result saved to: {output_path}", flush=True)
    success_rate = (df['lat'].notnull().sum() / total) * 100
    print(f"Hit Rate: {success_rate:.2f}%", flush=True)

if __name__ == "__main__":
    main()
