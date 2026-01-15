"""
파라미터 테스트
"""
import requests
import json

SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="
API_BASE_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

# 테스트 1: 서울만
print("=" * 80)
print("테스트 1: 서울만")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json',
    'sidoCd': '110000'
}
response = requests.get(API_BASE_URL, params=params, timeout=30)
data = response.json()
total = data['response']['body']['totalCount']
print(f"결과: {total}건\n")

# 테스트 2: 서울 + 강남구
print("=" * 80)
print("테스트 2: 서울 + 강남구")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json',
    'sidoCd': '110000',
    'sgguCd': '110033'
}
response = requests.get(API_BASE_URL, params=params, timeout=30)
data = response.json()
total = data['response']['body']['totalCount']
print(f"결과: {total}건\n")

# 테스트 3: 피부과만
print("=" * 80)
print("테스트 3: 피부과만 (dgsbjtCd=14)")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json',
    'dgsbjtCd': '14'
}
response = requests.get(API_BASE_URL, params=params, timeout=30)
data = response.json()
total = data['response']['body']['totalCount']
print(f"결과: {total}건")
if total > 0:
    items = data['response']['body']['items']['item']
    if isinstance(items, list):
        print(f"첫 번째 병원: {items[0].get('yadmNm', 'N/A')}")
        print(f"주소: {items[0].get('addr', 'N/A')}\n")

# 테스트 4: 의원 종별만
print("=" * 80)
print("테스트 4: 의원 종별만 (clCd=31)")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json',
    'clCd': '31'
}
response = requests.get(API_BASE_URL, params=params, timeout=30)
data = response.json()
total = data['response']['body']['totalCount']
print(f"결과: {total}건\n")

# 테스트 5: 서울 + 의원
print("=" * 80)
print("테스트 5: 서울 + 의원")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json',
    'sidoCd': '110000',
    'clCd': '31'
}
response = requests.get(API_BASE_URL, params=params, timeout=30)
data = response.json()
total = data['response']['body']['totalCount']
print(f"결과: {total}건\n")
