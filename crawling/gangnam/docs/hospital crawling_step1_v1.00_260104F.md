1. 강남언니 병원정보 (URL : https://www.gangnamunni.com/hospitals)에서 병원 목록, 별 평점, 평가 개수, 이벤트 개수를 수집해주세요.

2. 생성한 파일 앞에는 gangnam_을 받드시 붙여주세요.

3. 수집에 생성된 코드, 수집된 데이터 등의 산출물은  crawling\gangnam\data에 저장해주세요

4. 수집방법, 수집에 사용된 도구, 수집결과, 산출물 등에 대한 정보는 report.md 파일에 작성해주세요

5. 다음의 정보를 참고해 주세요.
    a. 네트워크를 통해 실제 데이터를 가져오는 URL
    https://www.gangnamunni.com/api/solar/search/hospitals?q=&sort=rcmd&districtCodeList=N1101,N1102,N1103,N1104,N1105,N1106,N1107,N1108,N1109,N1110,N1111,N1112,N1113,N1114,N1115,N1116,N1117,N1118,N1119,N1120,N1121,N1201,N1202,N1203,N1204,N1205,N1206,N1207,N1208,N1209,N1210,N1211,N1212,N1213,N1214,N1301,N1302,N1303,N1304,N1305,N1306,N1401,N1402,N1403,N1404,N1405,N1406,N1501,N1502,N1503,N1504,N1505,N1506,N1507,N1508,N1601,N1602,N1603,N1604,N1701,N1702,N1703,N1704,N1801,N1802,N1901,N1902,N1903,N1904,N1905,N1906,N1907,N2001,N2002,N2003,N2004,N2005,N2101,N2102,N2103,N2104,N2105,N2106,N2107,N2201,N2202,N2203,N2204,N2205,N2301,N2302,N2303,N2304,N2305,N2306,N2307,N2308,N2401,N2402,N2403,N2404,N2405,N2406,N2407,N2501,N2502,N2503,N2504,N2505,N2506,N2507,N2508,N2509,N2601,N2602&start=80&length=20
    
    b. 해당 Requset에 대한 Header 정보
        :authority
        www.gangnamunni.com
        :method
        GET
        :path
        /api/solar/search/hospitals?q=&sort=rcmd&districtCodeList=N1101,N1102,N1103,N1104,N1105,N1106,N1107,N1108,N1109,N1110,N1111,N1112,N1113,N1114,N1115,N1116,N1117,N1118,N1119,N1120,N1121,N1201,N1202,N1203,N1204,N1205,N1206,N1207,N1208,N1209,N1210,N1211,N1212,N1213,N1214,N1301,N1302,N1303,N1304,N1305,N1306,N1401,N1402,N1403,N1404,N1405,N1406,N1501,N1502,N1503,N1504,N1505,N1506,N1507,N1508,N1601,N1602,N1603,N1604,N1701,N1702,N1703,N1704,N1801,N1802,N1901,N1902,N1903,N1904,N1905,N1906,N1907,N2001,N2002,N2003,N2004,N2005,N2101,N2102,N2103,N2104,N2105,N2106,N2107,N2201,N2202,N2203,N2204,N2205,N2301,N2302,N2303,N2304,N2305,N2306,N2307,N2308,N2401,N2402,N2403,N2404,N2405,N2406,N2407,N2501,N2502,N2503,N2504,N2505,N2506,N2507,N2508,N2509,N2601,N2602&start=80&length=20
        :scheme
        https
        accept
        application/json, text/plain, */*
        accept-encoding
        gzip, deflate, br, zstd
        accept-language
        ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
        cookie
        [MASKED_COOKIE_DATA]
        if-none-match
        "6622tk8m13xtu"
        priority
        u=1, i
        referer
        https://www.gangnamunni.com/hospitals
        sec-ch-ua
        "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"
        sec-ch-ua-mobile
        ?0
        sec-ch-ua-platform
        "Windows"
        sec-fetch-dest
        empty
        sec-fetch-mode
        cors
        sec-fetch-site
        same-origin
        traceparent
        00-0000000000000000386a6b0b6fdb9521-689d6e2f355b8844-00
        user-agent
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
        x-accept-language
        ko-KR
        x-datadog-origin
        rum
        x-datadog-parent-id
        7538302500325787716
        x-datadog-sampling-priority
        0
        x-datadog-trace-id
        4065179310520767777


    c. Payload
        q
        sort
        rcmd
        districtCodeList
        N1101,N1102,N1103,N1104,N1105,N1106,N1107,N1108,N1109,N1110,N1111,N1112,N1113,N1114,N1115,N1116,N1117,N1118,N1119,N1120,N1121,N1201,N1202,N1203,N1204,N1205,N1206,N1207,N1208,N1209,N1210,N1211,N1212,N1213,N1214,N1301,N1302,N1303,N1304,N1305,N1306,N1401,N1402,N1403,N1404,N1405,N1406,N1501,N1502,N1503,N1504,N1505,N1506,N1507,N1508,N1601,N1602,N1603,N1604,N1701,N1702,N1703,N1704,N1801,N1802,N1901,N1902,N1903,N1904,N1905,N1906,N1907,N2001,N2002,N2003,N2004,N2005,N2101,N2102,N2103,N2104,N2105,N2106,N2107,N2201,N2202,N2203,N2204,N2205,N2301,N2302,N2303,N2304,N2305,N2306,N2307,N2308,N2401,N2402,N2403,N2404,N2405,N2406,N2407,N2501,N2502,N2503,N2504,N2505,N2506,N2507,N2508,N2509,N2601,N2602
        start
        80
        length
        20



    d. 응답 예시
            {
                "reason": "SUCCESS",
                "msgCode": null,
                "data": [
                    {
                        "id": 69,
                        "name": "리엔장성형외과피부과",
                        "profileImage": "https://image2.gnsister.com/images/direct/1708329556763_f24f66787dab4d23822aecfa674876fe.jpg?originalImageWidth=88&originalImageHeight=88",
                        "mainImage": "https://image2.gnsister.com/images/direct/1694666837805_5ab3b61b7eca4a75a796725ebeb6f5ec.jpg?originalImageWidth=600&originalImageHeight=240",
                        "otherImages": null,
                        "cardLevel": 0,
                        "sigunguCode": "",
                        "sido": null,
                        "assessmentState": "EFFORT",
                        "pageCount": 45,
                        "eventCount": 45,
                        "reviewCount": 5332,
                        "ratingShow": true,
                        "country": "KR",
                        "rating": 8.8,
                        "ratingCount": 2681,
                        "integratedReviewCount": 5332,
                        "districtName": "신논현역",
                        "supportingLangList": [
                            "ja",
                            "ko"
                        ],
                        "tagReviewCount": null,
                        "badges": null,
                        "addedInWishList": false,
                        "subwayStationName": null,
                        "popularTreatments": [],
                        "filteredEvents": [],
                        "doctors": [
                            {
                                "id": 2031,
                                "name": "Jeongbae Kim",
                                "profileImage": "https://image2.gnsister.com/images/direct/1594191654990_5133a80cb9c447b49cb431b312a81215.jpg?originalImageWidth=500&originalImageHeight=500",
                                "activist": false
                            },
                            {
                                "id": 2034,
                                "name": "Sangrok Choi",
                                "profileImage": "https://image2.gnsister.com/images/direct/1594193832288_18bb608e2d6948d891a8d2686a8c992c.jpg?originalImageWidth=500&originalImageHeight=500",
                                "activist": false
                            },
                            {
                                "id": 2035,
                                "name": "Wonil Choi",
                                "profileImage": "https://image2.gnsister.com/images/direct/1594194264417_2664eb50e9c2482fb78b0125c293ca55.jpg?originalImageWidth=500&originalImageHeight=500",
                                "activist": false
                            },
                            {
                                "id": 2044,
                                "name": "Sehyeon Lee",
                                "profileImage": "https://image2.gnsister.com/images/direct/1594196882886_1339ec629ad64912ae85c66f9f49473e.jpg?originalImageWidth=300&originalImageHeight=300",
                                "activist": false
                            },
                            {
                                "id": 2045,
                                "name": "Wonjong Oh",
                                "profileImage": "https://image2.gnsister.com/images/direct/1594196939211_8e1e3bb92bde494c918bb0e8482f276d.jpg?originalImageWidth=300&originalImageHeight=300",
                                "activist": false
                            },
                            {
                                "id": 2046,
                                "name": "Ingwon Yeo",
                                "profileImage": "https://image2.gnsister.com/images/direct/1594197011914_4dcb4a4d22804063ac9c3414a841f1fe.jpg?originalImageWidth=300&originalImageHeight=300",
                                "activist": false
                            },
                            {
                                "id": 2947,
                                "name": "Jeongbae Kim",
                                "profileImage": "https://image2.gnsister.com/images/direct/1629250355047_7425ed1b672042629c279416c166fde3.jpg?originalImageWidth=800&originalImageHeight=800",
                                "activist": false
                            },
                            {
                                "id": 5207,
                                "name": "Hyeonguk Jang",
                                "profileImage": "https://image2.gnsister.com/images/direct/1682387541090_e7e0d833c0c84fda9b0aa5b77779a87f.png?originalImageWidth=300&originalImageHeight=300",
                                "activist": false
                            },
                            {
                                "id": 5208,
                                "name": "Seonghee Jo",
                                "profileImage": "https://image2.gnsister.com/images/direct/1682389687775_01d84b0ff0c7428382875eee9566e77a.png?originalImageWidth=300&originalImageHeight=300",
                                "activist": false
                            },
                            {
                                "id": 5285,
                                "name": "Yunmin Lim",
                                "profileImage": "https://image2.gnsister.com/images/hospital/5c94c9c6a42c4d0aba5b70bd731beecc_1c337c6c-450e-4b7c-81aa-1b0613f95506",
                                "activist": false
                            },
                            {
                                "id": 7002,
                                "name": "Jaeyoung Min",
                                "profileImage": "https://image2.gnsister.com/images/direct/1718161812975_e2271b5c5ec3486893ce7e8a4faa45f1.jpg?originalImageWidth=300&originalImageHeight=268",
                                "activist": false
                            },
                            {
                                "id": 7003,
                                "name": "Woojin Lee",
                                "profileImage": "https://image2.gnsister.com/images/direct/1718167224736_58b3fc4545784ec0b11e99c0ad35511e.jpg?originalImageWidth=292&originalImageHeight=290",
                                "activist": false
                            },
                            {
                                "id": 7005,
                                "name": "Seha Park",
                                "profileImage": "https://image2.gnsister.com/images/direct/1718168654165_05dbcfba9a8e4f9e99b5ad8d8ccafa2c.jpg?originalImageWidth=260&originalImageHeight=300",
                                "activist": false
                            }
                        ]
                    },
                    {
                        "id": 3084,
                        "name": "아이노유성형외과의원",
                        "profileImage": "https://image2.gnsister.com/images/direct/1706760895275_b7ceebd41fd5477f8b97adb31e24ead9.jpg?originalImageWidth=300&originalImageHeight=300",
                        "mainImage": "https://image2.gnsister.com/images/direct/1672281479065_163a58dc851c46b3b45116eb705e1e37.jpg?originalImageWidth=600&originalImageHeight=240",
                        "otherImages": null,
                        "cardLevel": 0,
                        "sigunguCode": "",
                        "sido": null,
                        "assessmentState": "EFFORT",
                        "pageCount": 25,
                        "eventCount": 25,
                        "reviewCount": 5310,
                        "ratingShow": true,
                        "country": "KR",
                        "rating": 9.1,
                        "ratingCount": 617,
                        "integratedReviewCount": 5310,
                        "districtName": "서면",
                        "supportingLangList": [
                            "ko",
                            "ja",
                            "en"
                        ],
                        "tagReviewCount": null,
                        "badges": null,
                        "addedInWishList": false,
                        "subwayStationName": null,
                        "popularTreatments": [],
                        "filteredEvents": [],
                        "doctors": [
                            {
                                "id": 1299,
                                "name": "Joohyun Oh",
                                "profileImage": "https://image2.gnsister.com/images/direct/1666169217796_d62ec6c3f6e844718246b72a34c39c7c.jpg?originalImageWidth=300&originalImageHeight=300",
                                "activist": false
                            },
                            {
                                "id": 9074,
                                "name": "Hyegwang Moon",
                                "profileImage": "https://image2.gnsister.com/images/hospital/5ff4135e41ab495e92fb7783249eb95a_5e8fe297-8439-45f4-a73a-48a5d5b8b14d",
                                "activist": false
                            }
                        ]
                    },
                    {
                        "id": 3829,
                        "name": "저스트성형외과의원",
                        "profileImage": "https://image2.gnsister.com/images/direct/1652064186925_43b31020bca441c19541c7743b80ce34.jpg?originalImageWidth=300&originalImageHeight=300",
                        "mainImage": "https://image2.gnsister.com/images/direct/1713405084435_5c87d69fff3d4f22b24d6fc7fc597315.jpg?originalImageWidth=600&originalImageHeight=240",
                        "otherImages": null,
                        "cardLevel": 0,
                        "sigunguCode": "",
                        "sido": null,
                        "assessmentState": "EFFORT",
                        "pageCount": 20,
                        "eventCount": 20,
                        "reviewCount": 5122,
                        "ratingShow": true,
                        "country": "KR",
                        "rating": 9,
                        "ratingCount": 1198,
                        "integratedReviewCount": 5122,
                        "districtName": "신논현역",
                        "supportingLangList": [
                            "ko",
                            "ja",
                            "en"
                        ],
                        "tagReviewCount": null,
                        "badges": null,
                        "addedInWishList": false,
                        "subwayStationName": null,
                        "popularTreatments": [],
                        "filteredEvents": [
                            {
                                "id": 31183,
                                "title": "저스트 피치리프팅",
                                "titleImage": "https://image2.gnsister.com/images/direct/1764551951631_caf934423cd3429f9f24ae87818fea0c.jpg?originalImageWidth=1080&originalImageHeight=1080",
                                "rating": 9,
                                "ratingCount": 39,
                                "originalMoney": {
                                    "currency": "KRW",
                                    "amount": 539000
                                },
                                "discountedMoney": {
                                    "currency": "KRW",
                                    "amount": 539000
                                },
                                "exchangeRateAppliedOriginalMoney": null,
                                "exchangeRateAppliedDiscountedMoney": {
                                    "currency": "KRW",
                                    "amount": 539000
                                },
                                "discountPercentage": 0,
                                "specialOffer": true,
                                "includeVat": true,
                                "serviceOfferType": "EVENT",
                                "eventPrice": {
                                    "original": {
                                        "currency": "KRW",
                                        "amount": 539000
                                    },
                                    "discount": {
                                        "currency": "KRW",
                                        "amount": 539000
                                    }
                                }
                            },






