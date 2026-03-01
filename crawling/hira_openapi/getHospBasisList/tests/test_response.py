"""
API 응답 구조 확인
"""
import requests
import json

SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="
API_BASE_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

# 테스트 1: 최소 파라미터
print("=" * 80)
print("테스트 1: 최소 파라미터 (전체 조회)")
print("=" * 80)
params1 = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json'
}
response1 = requests.get(API_BASE_URL, params=params1, timeout=30)
print(f"상태 코드: {response1.status_code}")
data1 = response1.json()
print(json.dumps(data1, indent=2, ensure_ascii=False))

# 테스트 2: 서울 강남구 피부과
print("\n" + "=" * 80)
print("테스트 2: 서울 강남구 피부과")
print("=" * 80)
params2 = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json',
    'sidoCd': '110000',
    'sgguCd': '110033',
    'dgsbjtCd': '14'
}
response2 = requests.get(API_BASE_URL, params=params2, timeout=30)
print(f"상태 코드: {response2.status_code}")
data2 = response2.json()
print(json.dumps(data2, indent=2, ensure_ascii=False))
