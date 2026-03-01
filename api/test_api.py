import requests
import json

url = "https://www.gangnamunni.com/api/hospitals/250"
headers = {
    "authority": "www.gangnamunni.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "referer": "https://www.gangnamunni.com/hospitals/250",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "x-accept-language": "ko-KR",
    "cookie": os.getenv("GANGNAMUNNI_COOKIE", "[MASKED_COOKIE_DATA]")
}

# Import os for env var
import os

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
except Exception as e:
    print(f"Error: {e}")
