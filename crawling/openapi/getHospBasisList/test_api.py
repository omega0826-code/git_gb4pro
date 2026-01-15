"""
API 테스트 스크립트
"""
import requests

# 인증키
SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="

# API URL
API_BASE_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList1"

# 테스트 1: 최소 파라미터로 호출
print("=" * 80)
print("테스트 1: 최소 파라미터")
print("=" * 80)

url = f"{API_BASE_URL}?ServiceKey={SERVICE_KEY}&pageNo=1&numOfRows=10&_type=json"
print(f"URL: {url}\n")

response = requests.get(url, timeout=30)
print(f"상태 코드: {response.status_code}")
print(f"응답 내용:\n{response.text}\n")

# 테스트 2: 서울 지역 조회
print("=" * 80)
print("테스트 2: 서울 지역 조회")
print("=" * 80)

params = {
    'pageNo': 1,
    'numOfRows': 10,
    '_type': 'json',
    'sidoCd': '110000'
}

url_with_key = f"{API_BASE_URL}?ServiceKey={SERVICE_KEY}"
print(f"URL: {url_with_key}")
print(f"Params: {params}\n")

response = requests.get(url_with_key, params=params, timeout=30)
print(f"상태 코드: {response.status_code}")
print(f"응답 내용:\n{response.text}\n")
