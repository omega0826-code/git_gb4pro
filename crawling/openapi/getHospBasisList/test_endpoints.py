"""
API v2 엔드포인트 테스트
"""
import requests

SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="

# 테스트할 엔드포인트 목록
endpoints = [
    "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList",
    "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList1",
    "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList2",
]

for endpoint in endpoints:
    print("=" * 80)
    print(f"테스트: {endpoint}")
    print("=" * 80)
    
    url = f"{endpoint}?ServiceKey={SERVICE_KEY}&pageNo=1&numOfRows=5&_type=json"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ 성공!")
            print(f"응답 샘플:\n{response.text[:500]}\n")
            break
        else:
            print(f"응답: {response.text[:200]}\n")
    except Exception as e:
        print(f"오류: {e}\n")
