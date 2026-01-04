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

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
except Exception as e:
    print(f"Error: {e}")
