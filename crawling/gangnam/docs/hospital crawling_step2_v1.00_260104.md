1. 강남언니 병원정보 (URL : https://www.gangnamunni.com/hospitals)에서 사이트에서 제공하는 개별 병원 정보를 수집해주세요

2. 병원정보는 api 방식으로 제공 되고 있고, 각 병원 URL 마다 정보를 제공하고 있어
    - id 확인 파일 : crawling\gangnam\data\gangnam_hospitals_FULL_20260104F.csv
    - 정보 제공 예시 : id = 250, 디에이성형외과의원 인경우
        https://www.gangnamunni.com/hospitals/250

3. 수집할 정보 목록은 병원 정보, 병원 소개, 진료 항목, 주요 의료진, 주소야

4. 수딥된 데이터는 새로 생성하되 crawling\gangnam\data\gangnam_hospitals_FULL_20260104F.csv의 데이터에 컬럼을 추가해서 만들어


5. 작업시작 전에 대략적인 에상시간을 알려주세요.

6. 작업하다가 시간이 많이 걸릴꺼 같으면 중간 저장을 해서 에러가 발생해도 다음부터 이어서 할 수 있게 하고, 에러 리포트 md 파일를 만들어줘

7. api 과다 호출이나 너무 빠른 호출로 해당 홈페이지에 부담이 되지 않게 해줘.

8. 생성한 파일 앞에는 gangnam_을 받드시 붙여주세요.

9. 수집에 생성된 코드, 수집된 데이터 등의 산출물은  crawling\gangnam\data에 저장해주세요

10. 수집방법, 수집에 사용된 도구, 수집결과, 산출물 등에 대한 정보는 report_gangnam_데이터 파일명.md 파일에 작성해주세요

11. 수집에는 다음의 정보를 참고해 주세요.
    
    a. 네트워크를 통해 실제 데이터를 가져오는 URL
        Request URL
        https://api2.amplitude.com/2/httpapi
        Request Method
        POST
        Status Code
        200 OK
        Remote Address
        54.68.213.171:443
        Referrer Policy
        strict-origin-when-cross-origin
    
    b. 해당 Requset에 대한 Header 정보
        :authority
        api2.amplitude.com
        :method
        POST
        :path
        /2/httpapi
        :scheme
        https
        accept
        */*
        accept-encoding
        gzip, deflate, br, zstd
        accept-language
        ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
        content-length
        1289
        content-type
        application/json
        origin
        https://www.gangnamunni.com
        priority
        u=1, i
        referer
        https://www.gangnamunni.com/
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
        cross-site
        user-agent
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36



        



    c. Payload
        {api_key: "6d6736a26b0b1ecd2b7d8a38c6dbf388", events: [,…], options: {},…}
        api_key
        : 
        "6d6736a26b0b1ecd2b7d8a38c6dbf388"
        client_upload_time
        : 
        "2026-01-04T15:06:48.447Z"
        events
        : 
        [,…]
        options
        : 
        {}
        request_metadata
        : 
        {sdk: {metrics: {histogram: {}}}}



    d. 응답 예시
            {
    "code": 200,
    "server_upload_time": 1767539208880,
    "payload_size_bytes": 1289,
    "events_ingested": 1
}






