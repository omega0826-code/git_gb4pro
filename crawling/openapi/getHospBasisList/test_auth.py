"""
인증 방식 테스트
"""
import requests
from urllib.parse import quote, quote_plus

SERVICE_KEY_DECODED = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="
SERVICE_KEY_ENCODED = quote(SERVICE_KEY_DECODED, safe='')

endpoint = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

print("=" * 80)
print("테스트 1: 디코딩 키를 URL에 직접 포함")
print("=" * 80)
url1 = f"{endpoint}?ServiceKey={SERVICE_KEY_DECODED}&pageNo=1&numOfRows=5&_type=json"
print(f"URL: {url1[:100]}...")
response1 = requests.get(url1, timeout=10)
print(f"상태 코드: {response1.status_code}")
print(f"응답: {response1.text[:300]}\n")

print("=" * 80)
print("테스트 2: 인코딩된 키를 URL에 직접 포함")
print("=" * 80)
url2 = f"{endpoint}?ServiceKey={SERVICE_KEY_ENCODED}&pageNo=1&numOfRows=5&_type=json"
print(f"URL: {url2[:100]}...")
response2 = requests.get(url2, timeout=10)
print(f"상태 코드: {response2.status_code}")
print(f"응답: {response2.text[:300]}\n")

print("=" * 80)
print("테스트 3: params로 전달 (requests가 자동 인코딩)")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY_DECODED,
    'pageNo': 1,
    'numOfRows': 5,
    '_type': 'json'
}
response3 = requests.get(endpoint, params=params, timeout=10)
print(f"실제 URL: {response3.url[:100]}...")
print(f"상태 코드: {response3.status_code}")
print(f"응답: {response3.text[:300]}\n")

# 성공한 경우 전체 응답 출력
for i, response in enumerate([response1, response2, response3], 1):
    if response.status_code == 200:
        print("=" * 80)
        print(f"✓ 테스트 {i} 성공!")
        print("=" * 80)
        print(response.text)
        break
