import os
import requests
from dotenv import load_dotenv
import sys

# Force UTF-8 for stdout if possible, but safer to just avoid emojis
sys.stdout.reconfigure(encoding='utf-8')

def verify_api_key():
    # Load .env from current or parent directories
    load_dotenv()
    api_key = os.getenv("KAKAO_API_KEY")
    
    print(f"Checking for API Key...")
    if not api_key:
        print("[FAIL] API Key not found in environment variables.")
        return False
        
    print(f"[OK] API Key found: {api_key[:4]}****")
    
    # Test API call
    address = "서울시청"
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    
    print(f"Testing API call with address: {address}")
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result['documents']:
                doc = result['documents'][0]
                print(f"[SUCCESS] Geocoding Successful! Coordinates: {doc['y']}, {doc['x']}")
                return True
            else:
                print("[WARNING] API call succeeded but no results found (unexpected for '서울시청').")
                print(f"Response: {result}")
                return True # Key is valid, just no result
        elif resp.status_code == 401:
            print("[FAIL] Unauthorized (401). Invalid API Key or referrer restrictions.")
            print(f"Response: {resp.text}")
            return False
        elif resp.status_code == 403:
            print("[FAIL] Forbidden (403). Quota exceeded or permission denied.")
            print(f"Response: {resp.text}")
            return False
        else:
            print(f"[FAIL] API Error: {resp.status_code}")
            print(f"Response: {resp.text}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Exception during API call: {e}")
        return False

if __name__ == "__main__":
    verify_api_key()
