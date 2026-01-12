import requests
import pandas as pd
import time
import os
from datetime import datetime

def crawl_gangnam_hospitals():
    url = "https://www.gangnamunni.com/api/solar/search/hospitals"
    
    headers = {
        "authority": "www.gangnamunni.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://www.gangnamunni.com/hospitals",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "x-accept-language": "ko-KR",
        "cookie": (
            "_fbp=fb.1.1767421640579.76076189282473468; "
            "airbridge_migration_metadata__gangnamunni=%7B%22version%22%3A%221.10.80%22%7D; "
            "ab180ClientId=26b31da5-9c29-474b-ad25-132e73acf01b; "
            "ch-veil-id=43dcdd8c-d356-4458-aa3d-40600efa73b5; "
            "_gid=GA1.2.1492892469.1767530252; "
            "airbridge_touchpoint=%7B%22channel%22%3A%22www.google.com%22%2C%22parameter%22%3A%7B%7D%2C%22generationType%22%3A1224%2C%22url%22%3A%22https%3A//www.gangnamunni.com/signin%22%2C%22timestamp%22%3A1767530356478%7D; "
            "signupTarget=kakao; "
            "signupCode=hpwT06PrPq2gRmTB2NoyR7Sn5_r-sgu2V6PZT_gpqZNl7O445FuRegAAAAQKDSKZAAABm4kGeaIh5oEAb4_jFQ; "
            "AMP_MKTG_6d6736a26b=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRmthdXRoLmtha2FvLmNvbSUyRiUyMiUyQyUyMnJlZmVycmluZ19kb21haW4lMjIlM0ElMjJrYXV0aC5rYWthby5jb20lMjIlN0Q=; "
            "token=a368f79e3ea645d1b1f7be0a63fd94b8; "
            "hashedToken=dWC7cqGVmTBHtxoYLEg2lH; "
            "return_url=%2Fdistrict-filter%3Ftarget%3Dhospitals%26district%3DN11; "
            "cto_bundle=ahAHel9rODZwS2VQWmIwOGJHUTNkczgwTTFvWjRUbno1cjdmdUgyejNLeFdxWTJuR0hGc3Bycm5VTFRXeUoyczJSWExTRnBuSEpIMFFmVHBTb2ZXcERCNXQ1VHVFZ3ElMkJoYWxmZW51WEN1UkRTb0VyT2dIVThUU1Q3TW03b1hGTjNUNGI2a2JPWjVXakZvb0dXbiUyQld1VEJOTkpRJTNEJTNE; "
            "_ga=GA1.1.937460766.1767421641; "
            "airbridge_user=%7B%22externalUserID%22%3A%228704487%22%2C%22attributes%22%3A%7B%22myHospitalDistrictId%22%3A%22N1501%22%2C%22country%22%3A%22KR%22%2C%22age%22%3A44%7D%7D; "
            "airbridge_device_alias=%7B%22amplitude_device_id%22%3A%2213555a23-1930-4f2c-8986-af08eced66c0%22%7D; "
            "_gat=1; _gcl_au=1.1.1631972134.1767421641.1080322853.1767535125.1767535124; "
            "rlState=eyJ3IjoxNzY3NTM1MTgzMzYwLCJjIjoyLCJiIjowfQ==; "
            "_ga_GXB8082VP1=GS2.1.s1767535124$o4$g1$t1767535138$j46$l0$h316778212; "
            "airbridge_session=%7B%22id%22%3A%22d9736bbb-60c7-41ab-a708-48ddc57d4bde%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1767535123645%2C%22end%22%3A1767535138585%7D"
        )
    }
    
    district_codes_str = "N1101,N1102,N1103,N1104,N1105,N1106,N1107,N1108,N1109,N1110,N1111,N1112,N1113,N1114,N1115,N1116,N1117,N1118,N1119,N1120,N1121,N1201,N1202,N1203,N1204,N1205,N1206,N1207,N1208,N1209,N1210,N1211,N1212,N1213,N1214,N1301,N1302,N1303,N1304,N1305,N1306,N1401,N1402,N1403,N1404,N1405,N1406,N1501,N1502,N1503,N1504,N1505,N1506,N1507,N1508,N1601,N1602,N1603,N1604,N1701,N1702,N1703,N1704,N1801,N1802,N1901,N1902,N1903,N1904,N1905,N1906,N1907,N2001,N2002,N2003,N2004,N2005,N2101,N2102,N2103,N2104,N2105,N2106,N2107,N2201,N2202,N2203,N2204,N2205,N2301,N2302,N2303,N2304,N2305,N2306,N2307,N2308,N2401,N2402,N2403,N2404,N2405,N2406,N2407,N2501,N2502,N2503,N2504,N2505,N2506,N2507,N2508,N2509,N2601,N2602"
    district_list = district_codes_str.split(',')
    
    all_hospitals = []
    seen_ids = set() # 중복 방지를 위한 ID 집합
    
    print(f"총 {len(district_list)}개 지역 코드에 대해 순차 수집을 시작합니다.")
    print("전체 데이터 수집에는 시간이 다소 소요될 수 있습니다.")
    
    total_start_time = time.time()
    
    for idx, district_code in enumerate(district_list):
        start = 0
        length = 20
        # 진행 상황 표시 (너무 자주는 아니게, 지역 단위로)
        # print(f"[{idx+1}/{len(district_list)}] 지역 코드 {district_code} 수집 시작...")
        
        while True:
            params = {
                "q": "",
                "sort": "rcmd",
                "districtCodeList": district_code, # 단일 지역 코드로 요청
                "start": start,
                "length": length
            }
            
            try:
                response = requests.get(url, headers=headers, params=params)
                
                # 오류 발생 시 잠시 대기 후 재시도 또는 건너뛰기 로직을 넣을 수도 있으나,
                # 여기서는 간단히 로그 찍고 해당 지역 루프 중단
                if response.status_code != 200:
                    print(f"[{district_code}] 오류 발생: {response.status_code}")
                    break
                
                json_data = response.json()
                data = json_data.get("data", [])
                
                if not data:
                    # 더 이상 데이터가 없으면 다음 지역으로
                    break
                    
                new_count = 0
                for hospital in data:
                    h_id = hospital.get("id")
                    
                    # 중복되지 않은 병원만 추가
                    if h_id not in seen_ids:
                        seen_ids.add(h_id)
                        h_info = {
                            "id": h_id,
                            "hospital_name": hospital.get("name"),
                            "rating": hospital.get("rating"),
                            "review_count": hospital.get("ratingCount"),
                            "event_count": hospital.get("eventCount"),
                            "district_code": district_code # 어느 지역 코드에서 발견되었는지 (참고용, 중복 시 첫 발견 기준)
                        }
                        all_hospitals.append(h_info)
                        new_count += 1
                
                # print(f"  - start={start}: {len(data)}개 가져옴, 신규 {new_count}개 추가 (누적 {len(all_hospitals)}개)")
                
                start += length
                time.sleep(0.2) # 너무 빠른 요청 방지
                
            except Exception as e:
                print(f"[{district_code}] 예외 발생: {e}")
                break
        
        # 지역 하나 끝날 때마다 진행 상황 간략 출력
        if (idx + 1) % 10 == 0:
            print(f"진행률: {idx+1}/{len(district_list)} 지역 완료. 현재 누적 병원 수: {len(all_hospitals)}개")

    total_elapsed = time.time() - total_start_time
    print(f"모든 수집이 완료되었습니다. (소요 시간: {total_elapsed:.1f}초)")
    
    if all_hospitals:
        df = pd.DataFrame(all_hospitals)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gangnam_hospitals_FULL_{timestamp}.csv"
        filepath = os.path.join("crawling", "gangnam", "data", filename)
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        print(f"최종 결과: 총 {len(df)}개 데이터를 {filepath}에 저장하였습니다.")
        return filepath
    else:
        print("수집된 데이터가 없습니다.")
        return None

if __name__ == "__main__":
    crawl_gangnam_hospitals()
