"""
강남구 병원 상세 확인
"""
import requests
import json

SERVICE_KEY = "Bk8LikYxwbpxf1OKF0mYYonK9RNmYo/mmgtNsZ41rRNxMuIh5s7RgflEXp+Xwp3R0FDR2j01gx62Hc++Jzc2pw=="
API_BASE_URL = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"

# 서울 전체 조회해서 강남구 병원 찾기
params = {
    'ServiceKey': SERVICE_KEY,
    'pageNo': 1,
    'numOfRows': 100,
    '_type': 'json',
    'sidoCd': '110000'
}

print("서울 지역 시군구 코드 매핑:")
print("=" * 80)

sggu_map = {}
for page in range(1, 50):  # 5000건 조회
    params['pageNo'] = page
    response = requests.get(API_BASE_URL, params=params, timeout=30)
    data = response.json()
    items = data['response']['body']['items']['item']
    
    for item in items:
        sggu_cd = item.get('sgguCd')
        sggu_nm = item.get('sgguCdNm', '')
        
        if sggu_cd and sggu_nm:
            if sggu_cd not in sggu_map:
                sggu_map[sggu_cd] = sggu_nm
                print(f"{sggu_nm:10s}: {sggu_cd}")
                
                # 강남구 찾으면 상세 정보 출력
                if '강남' in sggu_nm:
                    print(f"\n[OK] 강남구 발견!")
                    print(f"  코드: {sggu_cd}")
                    print(f"  예시 병원: {item.get('yadmNm')}")
                    print(f"  주소: {item.get('addr')}\n")
    
    if len(sggu_map) >= 25:  # 서울 25개 구
        break

print(f"\n총 {len(sggu_map)}개 시군구 발견")

# 강남구로 검색
if any('강남' in name for name in sggu_map.values()):
    gangnam_code = [code for code, name in sggu_map.items() if '강남' in name][0]
    print(f"\n강남구 코드 {gangnam_code}로 피부과 검색:")
    print("=" * 80)
    
    search_params = {
        'ServiceKey': SERVICE_KEY,
        'pageNo': 1,
        'numOfRows': 10,
        '_type': 'json',
        'sidoCd': '110000',
        'sgguCd': str(gangnam_code),
        'dgsbjtCd': '14'
    }
    
    response = requests.get(API_BASE_URL, params=search_params, timeout=30)
    data = response.json()
    total = data['response']['body']['totalCount']
    print(f"검색 결과: {total}건")
    
    if total > 0:
        items = data['response']['body']['items']['item']
        if not isinstance(items, list):
            items = [items]
        
        print(f"\n처음 5개 병원:")
        for i, item in enumerate(items[:5], 1):
            print(f"{i}. {item.get('yadmNm')} - {item.get('addr')}")
