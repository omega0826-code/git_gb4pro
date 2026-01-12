import requests
import pandas as pd
import json
import time
import os
import re
from datetime import datetime

# 설정
INPUT_FILE = r"crawling\gangnam\data\gangnam_hospitals_FULL_20260104F.csv"
OUTPUT_DIR = r"crawling\gangnam\data"
BASE_URL = "https://www.gangnamunni.com/hospitals"
SLEEP_TIME = 0.5
SAVE_INTERVAL = 50

def get_build_id():
    """HTML에서 buildId를 추출합니다."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(BASE_URL, headers=headers)
        if response.status_code == 200:
            match = re.search(r'"buildId":"(.*?)"', response.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error getting buildId: {e}")
    return None

def crawl_hospital_details():
    build_id = get_build_id()
    if not build_id:
        print("Failed to get buildId. Exiting.")
        return

    print(f"Build ID: {build_id}")

    # 데이터 로드
    df = pd.read_csv(INPUT_FILE)
    if 'introduction' not in df.columns:
        df['introduction'] = ""
    if 'treatment_tags' not in df.columns:
        df['treatment_tags'] = ""
    if 'doctors' not in df.columns:
        df['doctors'] = ""
    if 'address' not in df.columns:
        df['address'] = ""
    if 'crawled' not in df.columns:
        df['crawled'] = False

    total = len(df)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"gangnam_hospitals_detail_{timestamp}.csv"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    error_report_path = os.path.join(OUTPUT_DIR, f"error_report_gangnam_{timestamp}.md")

    errors = []

    print(f"총 {total}개 병원 중 미수집 데이터 수집 시작...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "x-nextjs-data": "1"
    }

    start_time = time.time()

    for i, row in df.iterrows():
        if row.get('crawled') == True:
            continue

        h_id = row['id']
        # data url: https://www.gangnamunni.com/_next/data/{build_id}/kr/hospitals/{h_id}.json?hospitalId={h_id}
        url = f"https://www.gangnamunni.com/_next/data/{build_id}/kr/hospitals/{h_id}.json?hospitalId={h_id}"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                page_props = data.get("pageProps", {})
                h_data = page_props.get("data", {}).get("hospital", {})
                doctors_data = page_props.get("data", {}).get("doctors", [])

                # 정보 추출
                intro = h_data.get("introduction", "")
                tags = [tag.get("name") for tag in h_data.get("treatmentTags", [])]
                addr = h_data.get("location", {}).get("address", "")
                
                doctors = []
                for d in doctors_data:
                    d_name = d.get("name", "")
                    d_major = d.get("majorName", "")
                    doctors.append(f"{d_name}({d_major})")

                # 데이터 프레임 업데이트
                df.at[i, 'introduction'] = intro
                df.at[i, 'treatment_tags'] = ", ".join(tags)
                df.at[i, 'doctors'] = ", ".join(doctors)
                df.at[i, 'address'] = addr
                df.at[i, 'crawled'] = True

            else:
                print(f"[{i+1}/{total}] ID {h_id} Error: {response.status_code}")
                errors.append({"index": i, "id": h_id, "status": response.status_code})

        except Exception as e:
            print(f"[{i+1}/{total}] ID {h_id} Exception: {e}")
            errors.append({"index": i, "id": h_id, "error": str(e)})

        # 진행률 표시
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / (i + 1)
            remaining = avg_time * (total - (i + 1))
            print(f"진행: {i+1}/{total} ({(i+1)/total*100:.1f}%) - 남은 예상 시간: {remaining/60:.1f}분")

        # 중간 저장
        if (i + 1) % SAVE_INTERVAL == 0:
            df.to_csv(output_path, index=False, encoding="utf-8-sig")

        time.sleep(SLEEP_TIME)

    # 최종 저장
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    
    # 에러 리포트 생성
    if errors:
        with open(error_report_path, "w", encoding="utf-8") as f:
            f.write(f"# Gangnam Hospitals Crawling Error Report ({timestamp})\n\n")
            f.write(f"- Total attempts: {total}\n")
            f.write(f"- Total errors: {len(errors)}\n\n")
            f.write("| Index | ID | Error/Status |\n")
            f.write("|---|---|---|")
            for err in errors:
                f.write(f"| {err.get('index')} | {err.get('id')} | {err.get('status') or err.get('error')} |\n")
    
    print(f"수집 완료. 결과 저장: {output_path}")
    return output_path, error_report_path

if __name__ == "__main__":
    crawl_hospital_details()
