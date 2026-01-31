import pandas as pd
import os
import glob
import time
import sys
from datetime import datetime

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def format_time(seconds):
    """시간을 읽기 쉬운 형식으로 변환"""
    if seconds < 60:
        return f"{seconds:.1f}초"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}분"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}시간"

def format_size(bytes_size):
    """파일 크기를 읽기 쉬운 형식으로 변환"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}TB"

def convert_xlsx_to_csv():
    """Excel 파일을 CSV로 변환 (개선 버전)"""
    
    # 경로 설정
    source_dir = r"d:\git_gb4pro\data\전국 병의원 및 약국 현황 2025.12"
    output_dir = os.path.join(source_dir, "CSV")
    log_dir = r"d:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\scripts_260131_0823"
    
    # 출력 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[OK] CSV 저장 디렉토리 생성: {output_dir}\n")
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Excel 파일 목록 가져오기
    xlsx_files = glob.glob(os.path.join(source_dir, "*.xlsx"))
    
    if not xlsx_files:
        print("[ERROR] 변환할 .xlsx 파일을 찾을 수 없습니다.")
        return
    
    # 파일 크기 순으로 정렬 (큰 파일 먼저 처리하여 진행 상황 파악 용이)
    xlsx_files_with_size = [(f, os.path.getsize(f)) for f in xlsx_files]
    xlsx_files_with_size.sort(key=lambda x: x[1], reverse=True)
    
    total_files = len(xlsx_files)
    total_size = sum(size for _, size in xlsx_files_with_size)
    
    print("=" * 80)
    print(f"[INFO] Excel to CSV 변환 작업 시작")
    print("=" * 80)
    print(f"[DIR] 원본 디렉토리: {source_dir}")
    print(f"[OUT] CSV 저장 위치: {output_dir}")
    print(f"[CNT] 총 파일 개수: {total_files}개")
    print(f"[SIZE] 총 파일 크기: {format_size(total_size)}")
    print("=" * 80)
    print()
    
    # 변환 시작
    start_time = time.time()
    success_count = 0
    fail_count = 0
    conversion_log = []
    
    for i, (file_path, file_size) in enumerate(xlsx_files_with_size, 1):
        file_name = os.path.basename(file_path)
        csv_name = os.path.splitext(file_name)[0] + ".csv"
        csv_path = os.path.join(output_dir, csv_name)
        
        print(f"[{i}/{total_files}] 변환 중: {file_name}")
        print(f"     파일 크기: {format_size(file_size)}")
        
        file_start_time = time.time()
        
        try:
            # Excel 파일 읽기
            df = pd.read_excel(file_path, engine='openpyxl')
            
            rows, cols = df.shape
            
            # CSV로 저장 (한글 지원을 위해 utf-8-sig 인코딩 사용)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            # 메모리 해제
            del df
            
            file_elapsed = time.time() - file_start_time
            csv_size = os.path.getsize(csv_path)
            
            print(f"     [OK] 성공: {rows:,}행 x {cols}열 -> {format_size(csv_size)}")
            print(f"     소요 시간: {format_time(file_elapsed)}")
            print()
            
            success_count += 1
            conversion_log.append({
                'status': 'SUCCESS',
                'file': file_name,
                'rows': rows,
                'cols': cols,
                'original_size': file_size,
                'csv_size': csv_size,
                'time': file_elapsed
            })
            
        except Exception as e:
            file_elapsed = time.time() - file_start_time
            print(f"     [ERROR] 실패: {str(e)}")
            print(f"     소요 시간: {format_time(file_elapsed)}")
            print()
            
            fail_count += 1
            conversion_log.append({
                'status': 'FAILED',
                'file': file_name,
                'error': str(e),
                'time': file_elapsed
            })
    
    # 전체 작업 완료
    total_elapsed = time.time() - start_time
    
    print("=" * 80)
    print(f"[DONE] 변환 작업 완료!")
    print("=" * 80)
    print(f"[OK] 성공: {success_count}개")
    print(f"[FAIL] 실패: {fail_count}개")
    print(f"[TIME] 총 소요 시간: {format_time(total_elapsed)}")
    print(f"[OUT] CSV 파일 저장 위치: {output_dir}")
    print("=" * 80)
    
    # 로그 파일 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"conversion_log_{timestamp}.txt")
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("Excel to CSV 변환 로그\n")
        f.write("=" * 80 + "\n")
        f.write(f"작업 시작: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"작업 종료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"총 소요 시간: {format_time(total_elapsed)}\n")
        f.write(f"성공: {success_count}개 / 실패: {fail_count}개\n")
        f.write("=" * 80 + "\n\n")
        
        for log in conversion_log:
            f.write(f"파일: {log['file']}\n")
            f.write(f"상태: {log['status']}\n")
            
            if log['status'] == 'SUCCESS':
                f.write(f"  - 행/열: {log['rows']:,}행 × {log['cols']}열\n")
                f.write(f"  - 원본 크기: {format_size(log['original_size'])}\n")
                f.write(f"  - CSV 크기: {format_size(log['csv_size'])}\n")
                f.write(f"  - 소요 시간: {format_time(log['time'])}\n")
            else:
                f.write(f"  - 에러: {log['error']}\n")
                f.write(f"  - 소요 시간: {format_time(log['time'])}\n")
            
            f.write("\n")
    
    print(f"\n[LOG] 상세 로그 저장: {log_file}")
    
    return success_count, fail_count

if __name__ == "__main__":
    try:
        convert_xlsx_to_csv()
    except KeyboardInterrupt:
        print("\n\n[WARN] 사용자에 의해 작업이 중단되었습니다.")
    except Exception as e:
        print(f"\n\n[ERROR] 예상치 못한 오류 발생: {e}")
