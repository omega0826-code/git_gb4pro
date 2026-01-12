import requests
import pandas as pd
import time
import os
import re
from datetime import datetime
import traceback

# 설정
INPUT_FILE = r"crawling\gangnam\data\gangnam_hospitals_detail_RESUME_20260105_011349.csv"
OUTPUT_DIR = r"crawling\gangnam\data"
BASE_URL = "https://www.gangnamunni.com/hospitals"
SLEEP_TIME = 1.0
SAVE_INTERVAL = 20
MAX_RETRIES = 3 # 최대 재시도 횟수

def get_build_id(retries=3):
    """HTML에서 buildId를 추출합니다. 재시도 로직 포함."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    for attempt in range(retries):
        try:
            response = requests.get(BASE_URL, headers=headers, timeout=10)
            if response.status_code == 200:
                match = re.search(r'"buildId":"(.*?)"', response.text)
                if match:
                    return match.group(1)
            else:
                print(f"Build ID fetch failed. Status: {response.status_code}. Retrying ({attempt+1}/{retries})...")
        except Exception as e:
            print(f"Error getting buildId: {e}. Retrying ({attempt+1}/{retries})...")
        
        time.sleep(2) # 재시도 전 대기
    return None

def crawl_resume():
    build_id = get_build_id()
    if not build_id:
        print("Failed to get buildId after retries. Exiting.")
        return

    print(f"Build ID: {build_id}")

    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    # 데이터 로드
    df = pd.read_csv(INPUT_FILE)
    
    required_cols = ['introduction', 'treatment_tags', 'doctors', 'address', 'crawled']
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
            if col == 'crawled':
                df[col] = False

    df['crawled'] = df['crawled'].apply(lambda x: True if str(x).lower() == 'true' else False)

    target_indices = df[df['crawled'] == False].index
    total_targets = len(target_indices)
    
    if total_targets == 0:
        print("모든 데이터가 이미 수집되었습니다.")
        return

    print(f"총 {len(df)}개 중 {total_targets}개 병원 데이터 수집 재개...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"gangnam_hospitals_detail_RESUME_{timestamp}.csv"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    error_report_path = os.path.join(OUTPUT_DIR, f"error_report_resume_{timestamp}.md")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "x-nextjs-data": "1"
    }

    errors = []
    consecutive_errors = 0
    start_time = time.time()
    processed_count = 0

    try:
        for idx in target_indices:
            row = df.loc[idx]
            h_id = row['id']
            url = f"https://www.gangnamunni.com/_next/data/{build_id}/kr/hospitals/{h_id}.json?hospitalId={h_id}"
            
            success = False
            for attempt in range(MAX_RETRIES):
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        page_props = data.get("pageProps", {})
                        h_data = page_props.get("data", {}).get("hospital", {})
                        doctors_data = page_props.get("data", {}).get("doctors", [])

                        intro = h_data.get("introduction", "")
                        tags = [tag.get("name") for tag in h_data.get("treatmentTags", [])]
                        addr = h_data.get("location", {}).get("address", "")
                        
                        doctors = []
                        for d in doctors_data:
                            d_name = d.get("name", "")
                            d_major = d.get("majorName", "")
                            doctors.append(f"{d_name}({d_major})")

                        # 업데이트
                        df.at[idx, 'introduction'] = intro
                        df.at[idx, 'treatment_tags'] = ", ".join(tags)
                        df.at[idx, 'doctors'] = ", ".join(doctors)
                        df.at[idx, 'address'] = addr
                        df.at[idx, 'crawled'] = True
                        
                        consecutive_errors = 0
                        success = True
                        break # 성공하면 재시도 루프 탈출

                    elif response.status_code == 404:
                        print(f"[{processed_count+1}/{total_targets}] ID {h_id} Not Found (404). Skipping.")
                        df.at[idx, 'crawled'] = True # 404는 수집 완료로 처리
                        errors.append({"index": idx, "id": h_id, "status": 404, "msg": "Page Not Found"})
                        consecutive_errors = 0
                        success = True
                        break

                    else:
                        # 500 등 기타 에러 시 재시도
                        print(f"[{processed_count+1}/{total_targets}] ID {h_id} Error: {response.status_code}. Retrying ({attempt+1}/{MAX_RETRIES})...")
                        time.sleep(2 * (attempt + 1)) # 점진적 대기
                
                except Exception as e:
                    print(f"[{processed_count+1}/{total_targets}] ID {h_id} Exception: {e}. Retrying ({attempt+1}/{MAX_RETRIES})...")
                    time.sleep(2 * (attempt + 1))
            
            if not success:
                # 최대 재시도 후에도 실패 시 에러 기록
                errors.append({"index": idx, "id": h_id, "status": "Failed", "msg": "Max retries exceeded"})
                consecutive_errors += 1
                print(f"[{processed_count+1}/{total_targets}] ID {h_id} Failed after retries.")

            processed_count += 1

            # 연속 에러 체크 (10회 -> 20회로 완화, 재시도 로직이 있으므로)
            if consecutive_errors >= 20:
                print("연속적인 에러 발생으로 작업을 중단합니다.")
                break

            # 진행률
            if processed_count % 10 == 0:
                elapsed = time.time() - start_time
                avg_time = elapsed / processed_count
                remaining = avg_time * (total_targets - processed_count)
                print(f"진행: {processed_count}/{total_targets} - 남은 시간: {remaining/60:.1f}분")

            # 중간 저장
            if processed_count % SAVE_INTERVAL == 0:
                df.to_csv(output_path, index=False, encoding="utf-8-sig")
            
            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        print("사용자에 의해 작업이 중단되었습니다.")

    finally:
        # 최종 저장
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"최종 결과 저장: {output_path}")

        # 에러 리포트
        if errors:
            with open(error_report_path, "w", encoding="utf-8") as f:
                f.write(f"# Gangnam Hospitals Crawling Error Report ({timestamp})\n\n")
                f.write(f"Total processed: {processed_count}\n")
                f.write(f"Total errors: {len(errors)}\n\n")
                f.write("| Index | ID | Status/Error | Message |\n")
                f.write("|---|---|---|---|")
                for err in errors:
                    idx = err.get('index')
                    hid = err.get('id')
                    status = err.get('status')
                    msg = err.get('msg')
                    msg = str(msg).replace("\n", " ")[:100]
                    f.write(f"| {idx} | {hid} | {status} | {msg} |\n")
            
            print(f"에러 리포트 생성: {error_report_path}")

if __name__ == "__main__":
    crawl_resume()