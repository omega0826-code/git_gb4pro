"""
시군구 코드 형식 테스트
"""
import requests
import json

SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="
API_BASE_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

# 서울 동대문구 병원 하나 가져와서 실제 코드 확인
print("=" * 80)
print("실제 데이터에서 코드 확인")
print("=" * 80)
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 10,
    '_type': 'json',
    'sidoCd': '110000'
}
response = requests.get(API_BASE_URL, params=params, timeout=30)
data = response.json()
items = data['response']['body']['items']['item']

# 강남구 병원 찾기
print("서울 지역 병원들의 시군구 코드:")
seen_sggu = set()
for item in items:
    sggu_cd = item.get('sgguCd')
    sggu_nm = item.get('sgguCdNm', '')
    if sggu_cd and sggu_cd not in seen_sggu:
        print(f"  {sggu_nm}: {sggu_cd} (타입: {type(sggu_cd)})")
        seen_sggu.add(sggu_cd)

# 더 많은 데이터 가져와서 강남구 찾기
print("\n강남구 병원 찾기...")
for page in range(1, 20):
    params['pageNo'] = page
    response = requests.get(API_BASE_URL, params=params, timeout=30)
    data = response.json()
    items = data['response']['body']['items']['item']
    
    for item in items:
        if '강남' in item.get('sgguCdNm', ''):
            print(f"\n강남구 병원 발견!")
            print(f"  병원명: {item.get('yadmNm')}")
            print(f"  시군구코드: {item.get('sgguCd')} (타입: {type(item.get('sgguCd'))})")
            print(f"  시군구명: {item.get('sgguCdNm')}")
            
            # 이 코드로 검색 테스트
            gangnam_code = item.get('sgguCd')
            print(f"\n이 코드로 검색 테스트: {gangnam_code}")
            
            test_params = {
                'ServiceKey': SERVICE_KEY,
                'pageNo': 1,
                'numOfRows': 5,
                '_type': 'json',
                'sidoCd': '110000',
                'sgguCd': str(gangnam_code)
            }
            test_response = requests.get(API_BASE_URL, params=test_params, timeout=30)
            test_data = test_response.json()
            total = test_data['response']['body']['totalCount']
            print(f"검색 결과: {total}건")
            
            exit(0)
