import requests
import re
import json

def get_build_id():
    url = "https://www.gangnamunni.com/hospitals"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            match = re.search(r'"buildId":"(.*?)"', response.text)
            if match:
                return match.group(1)
            else:
                print("Regex match failed. HTML snippet:", response.text[:500])
    except Exception as e:
        print(f"Error getting buildId: {e}")
    return None

def test_hospital(h_id):
    build_id = get_build_id()
    if not build_id:
        print("Failed to fetch Build ID")
        return

    print(f"Build ID: {build_id}")
    url = f"https://www.gangnamunni.com/_next/data/{build_id}/kr/hospitals/{h_id}.json?hospitalId={h_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "x-nextjs-data": "1"
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Hospital ID: {h_id}, Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success")
        else:
            print("Response text snippet:", response.text[:1000])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hospital("331")
