import requests
import pandas as pd
import json
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime

# 설정
# _copy 파일이 있다면 그것을 사용하고, 아니면 원본 사용
INPUT_FILE = r"crawling\gangnam\data\gangnam_hospitals_detail_RESUME_20260105_041227_copy.csv"
if not os.path.exists(INPUT_FILE):
    print(f"Warning: {INPUT_FILE} not found. Using original file.")
    INPUT_FILE = r"crawling\gangnam\data\gangnam_hospitals_detail_RESUME_20260105_041227.csv"

OUTPUT_DIR = r"crawling\gangnam\data"
# 헤더 설정 (브라우저처럼 보이게)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.gangnamunni.com/hospitals",
    "Upgrade-Insecure-Requests": "1"
}

def crawl_failed_hospitals():
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # crawled가 False이거나 비어있는 행 찾기
    # 문자열 'False'일 수도 있으므로 처리
    df['crawled'] = df['crawled'].apply(lambda x: str(x).lower() == 'true')
    
    target_indices = df[df['crawled'] == False].index
    total_targets = len(target_indices)
    
    print(f"Found {total_targets} failed items. Starting retry with HTML parsing...")
    
    success_count = 0
    fail_count = 0
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_output_path = os.path.join(OUTPUT_DIR, f"gangnam_hospitals_final_{timestamp}.csv")
    report_path = os.path.join(OUTPUT_DIR, f"report_gangnam_final_{timestamp}.md")
    
    errors = []

    for idx in target_indices:
        h_id = df.loc[idx, 'id']
        url = f"https://www.gangnamunni.com/hospitals/{h_id}"
        
        print(f"[{success_count + fail_count + 1}/{total_targets}] Retrying ID {h_id} via HTML...")
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # __NEXT_DATA__ JSON 추출 시도
                next_data_tag = soup.find('script', id='__NEXT_DATA__')
                
                if next_data_tag:
                    try:
                        json_data = json.loads(next_data_tag.string)
                        page_props = json_data.get('props', {}).get('pageProps', {})
                        h_data = page_props.get('data', {}).get('hospital', {})
                        doctors_data = page_props.get('data', {}).get('doctors', [])
                        
                        # 데이터 추출
                        intro = h_data.get("introduction", "")
                        tags = [tag.get("name") for tag in h_data.get("treatmentTags", [])]
                        addr = h_data.get("location", {}).get("address", "")
                        
                        doctors = []
                        for d in doctors_data:
                            d_name = d.get("name", "")
                            d_major = d.get("majorName", "")
                            doctors.append(f"{d_name}({d_major})")
                            
                        # DataFrame 업데이트
                        df.at[idx, 'introduction'] = intro
                        df.at[idx, 'treatment_tags'] = ", ".join(tags)
                        df.at[idx, 'doctors'] = ", ".join(doctors)
                        df.at[idx, 'address'] = addr
                        df.at[idx, 'crawled'] = True
                        
                        print(f"  -> Success: {h_data.get('name')}")
                        success_count += 1
                        
                    except json.JSONDecodeError:
                        print("  -> Failed to parse __NEXT_DATA__ JSON")
                        errors.append({'id': h_id, 'reason': 'JSON Parse Error'})
                        fail_count += 1
                else:
                    # __NEXT_DATA__가 없으면 직접 HTML 태그 파싱 (Fallback)
                    print("  -> __NEXT_DATA__ not found. Trying manual HTML parsing...")
                    # TODO: 필요 시 BeautifulSoup select 로직 추가 구현 가능
                    # 현재는 JSON 추출이 가장 확실하므로 실패 처리
                    errors.append({'id': h_id, 'reason': '__NEXT_DATA__ tag not found'})
                    fail_count += 1
                    
            elif response.status_code == 404:
                print("  -> 404 Not Found (Invalid ID)")
                df.at[idx, 'crawled'] = True # 없는 데이터도 처리 완료로 간주
                # 단, 내용은 비워둠
                success_count += 1
            else:
                print(f"  -> HTTP Error {response.status_code}")
                errors.append({'id': h_id, 'reason': f'HTTP {response.status_code}'})
                fail_count += 1
                
        except Exception as e:
            print(f"  -> Exception: {e}")
            errors.append({'id': h_id, 'reason': str(e)})
            fail_count += 1
            
        time.sleep(1) # 부하 방지

    # 최종 결과 저장
    df.to_csv(final_output_path, index=False, encoding="utf-8-sig")
    print(f"\nCompleted. Success: {success_count}, Failed: {fail_count}")
    print(f"Saved to {final_output_path}")
    
    # 통합 리포트 작성
    create_final_report(report_path, len(df), success_count, fail_count, errors, final_output_path)

def create_final_report(filepath, total, fixed, failed, errors, csv_path):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# 강남언니 병원 정보 수집 최종 결과 리포트\n\n")
        f.write(f"**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 1. 수집 개요\n")
        f.write(f"- **대상 데이터**: 총 {total}개 병원\n")
        f.write(f"- **수집 완료**: {total - failed}개 (재시도 성공 {fixed}개 포함)\n")
        f.write(f"- **수집 실패**: {failed}개\n")
        f.write(f"- **최종 데이터 파일**: `{csv_path}`\n\n")
        
        f.write("## 2. 수집 방식 변경 사항\n")
        f.write("- **기존 방식**: Next.js Data API (`/_next/data/...`) 호출\n")
        f.write("- **변경 방식**: API 호출 실패 건에 대해 **HTML 직접 접속 후 `__NEXT_DATA__` 스크립트 파싱** 방식으로 전환하여 성공률을 높임.\n\n")
        
        f.write("## 3. 에러 상세 (최종 실패)\n")
        if failed > 0:
            f.write("| ID | 실패 사유 |\n")
            f.write("|---|---|\n")
            for err in errors:
                f.write(f"| {err['id']} | {err['reason']} |\n")
        else:
            f.write("모든 대상 병원의 정보를 성공적으로 수집하였습니다.\n")

if __name__ == "__main__":
    crawl_failed_hospitals()
