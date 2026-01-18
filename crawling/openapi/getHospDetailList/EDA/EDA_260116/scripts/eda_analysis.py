"""
의료기관 전체정보 데이터 EDA (Exploratory Data Analysis)
================================================================================
작성일: 2026-01-16
목적: 서울 강남구 피부과 의료기관 데이터 탐색적 분석 및 시각화
입력: 병원전체정보_20260115_235745.csv
출력: 시각화 PNG 파일 (visualizations 폴더)
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (강화 버전 - rc() 함수 사용)
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
import shutil
from matplotlib import font_manager

def setup_korean_font():
    """
    한글 폰트 설정 및 캐시 관리
    Python 3.12+ 환경에서 안정적인 한글 렌더링 보장
    matplotlib.rc() 함수를 사용하여 전역 설정 강화
    """
    # 1. 폰트 캐시 문제 해결: 필요시 캐시 삭제
    cache_dir = mpl.get_cachedir()
    cache_path = Path(cache_dir)
    
    # fontlist 캐시 파일이 있으면 삭제 (폰트 인식 문제 해결)
    fontlist_cache = cache_path / 'fontlist-v330.json'
    if fontlist_cache.exists():
        try:
            fontlist_cache.unlink()
        except:
            pass
    
    # 2. 폰트 매니저 재빌드
    fm._load_fontmanager(try_read_cache=False)
    
    # 3. 한글 폰트 파일 경로 찾기
    korean_font_paths = {
        'Malgun Gothic': r'C:\Windows\Fonts\malgun.ttf',
        'Malgun Gothic Bold': r'C:\Windows\Fonts\malgunbd.ttf',
        'NanumGothic': r'C:\Windows\Fonts\NanumGothic.ttf',
        'Gulim': r'C:\Windows\Fonts\gulim.ttc',
        'Batang': r'C:\Windows\Fonts\batang.ttc',
    }
    
    selected_font = None
    selected_font_path = None
    
    # 4. 존재하는 폰트 파일 찾기
    for font_name, font_path in korean_font_paths.items():
        if Path(font_path).exists():
            selected_font = font_name
            selected_font_path = font_path
            break
    
    if selected_font_path:
        # 5. 폰트 파일을 matplotlib에 등록
        font_manager.fontManager.addfont(selected_font_path)
        
        # 6. 폰트 속성 객체 생성
        font_prop = fm.FontProperties(fname=selected_font_path)
        font_name_from_file = font_prop.get_name()
        
        # 7. matplotlib 전역 설정 (rc 함수 사용)
        plt.rc('font', family=font_name_from_file)
        plt.rc('axes', unicode_minus=False)
        
        # 8. rcParams도 함께 설정 (이중 보장)
        plt.rcParams['font.family'] = font_name_from_file
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.dpi'] = 100
        
        # 9. 추가 텍스트 요소 설정
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
        
        return selected_font, selected_font_path
    else:
        # 폴백: 기본 폰트 사용
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        return 'DejaVu Sans', None

korean_font_info = setup_korean_font()
if korean_font_info[1]:
    print(f"[폰트 설정] {korean_font_info[0]} 폰트 적용 완료")
    print(f"[폰트 경로] {korean_font_info[1]}")
else:
    print(f"[폰트 설정] {korean_font_info[0]} 폰트 사용 (한글 폰트 없음)")
print()



# ============================================================================
# 설정
# ============================================================================

# 데이터 파일 경로
DATA_FILE = r"D:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260115_235745.csv"

# 출력 폴더
SCRIPT_DIR = Path(__file__).parent
VIZ_DIR = SCRIPT_DIR.parent / "visualizations"
VIZ_DIR.mkdir(exist_ok=True)

# 시각화 스타일 (Seaborn 먼저 설정)
sns.set_style("whitegrid")
sns.set_palette("husl")

# Seaborn이 폰트 설정을 덮어쓰므로, 여기서 다시 한글 폰트 적용
if korean_font_info[1]:
    font_prop = fm.FontProperties(fname=korean_font_info[1])
    font_name = font_prop.get_name()
    
    plt.rc('font', family=font_name)
    plt.rc('axes', unicode_minus=False)
    plt.rcParams['font.family'] = font_name
    plt.rcParams['axes.unicode_minus'] = False
    
    print(f"[폰트 재적용] Seaborn 스타일 설정 후 {korean_font_info[0]} 폰트 재적용 완료")
    print()

# ============================================================================
# 데이터 로딩
# ============================================================================

print("=" * 80)
print("의료기관 전체정보 데이터 EDA")
print("=" * 80)
print()

print("[1] 데이터 로딩...")
df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
print(f"  [OK] 데이터 로딩 완료: {len(df):,}건, {len(df.columns)}개 컬럼")
print()

# ============================================================================
# 기본 정보 분석
# ============================================================================

print("[2] 기본 정보 분석")
print("-" * 80)
print(f"데이터 형태: {df.shape}")
print(f"총 레코드 수: {len(df):,}건")
print(f"총 컬럼 수: {len(df.columns)}개")
print()

# 데이터 타입 분포
print("데이터 타입 분포:")
dtype_counts = df.dtypes.value_counts()
for dtype, count in dtype_counts.items():
    print(f"  - {dtype}: {count}개")
print()

# 메모리 사용량
memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024
print(f"메모리 사용량: {memory_usage:.2f} MB")
print()

# ============================================================================
# API별 컬럼 그룹화
# ============================================================================

print("[3] API별 컬럼 그룹화")
print("-" * 80)

api_prefixes = {
    'eqp': '시설정보',
    'dtl': '세부정보',
    'dgsbjt': '진료과목정보',
    'trnsprt': '교통정보',
    'medoft': '의료장비정보',
    'foepaddc': '식대가산정보',
    'nursiggrd': '간호등급정보',
    'spcldiag': '특수진료정보',
    'spclhosp': '전문병원지정분야',
    'spcsbtj': '전문과목별전문의수',
    'etchst': '기타인력수정보'
}

api_columns = {}
for prefix, name in api_prefixes.items():
    cols = [col for col in df.columns if col.startswith(f"{prefix}_")]
    api_columns[prefix] = cols
    print(f"  - {name} ({prefix}): {len(cols)}개 컬럼")

# 원본 컬럼
original_cols = [col for col in df.columns if col.startswith('원본_')]
print(f"  - 원본 데이터: {len(original_cols)}개 컬럼")
print()

# ============================================================================
# 결측치 분석
# ============================================================================

print("[4] 결측치 분석")
print("-" * 80)

missing_data = df.isnull().sum()
missing_pct = (missing_data / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    '컬럼명': missing_data.index,
    '결측치 수': missing_data.values,
    '결측치 비율(%)': missing_pct.values
})
missing_df = missing_df[missing_df['결측치 수'] > 0].sort_values('결측치 수', ascending=False)

print(f"결측치가 있는 컬럼 수: {len(missing_df)}개 / {len(df.columns)}개")
print(f"전체 결측치 비율: {(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100):.2f}%")
print()

# 결측치 상위 10개 컬럼
print("결측치 상위 10개 컬럼:")
for idx, row in missing_df.head(10).iterrows():
    print(f"  {row['컬럼명']}: {row['결측치 수']:,}건 ({row['결측치 비율(%)']:.1f}%)")
print()

# 시각화 1: 결측치 히트맵 (상위 30개 컬럼)
print("[시각화] 결측치 히트맵 생성 중...")
fig, ax = plt.subplots(figsize=(12, 10))
top_missing_cols = missing_df.head(30)['컬럼명'].tolist()
if top_missing_cols:
    sns.heatmap(df[top_missing_cols].isnull(), cbar=True, yticklabels=False, 
                cmap='YlOrRd', ax=ax)
    ax.set_title('결측치 히트맵 (상위 30개 컬럼)', fontsize=16, fontweight='bold')
    ax.set_xlabel('컬럼명', fontsize=12)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "01_missing_data_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 저장: 01_missing_data_heatmap.png")
print()

# ============================================================================
# 주요 범주형 변수 분석
# ============================================================================

print("[5] 주요 범주형 변수 분석")
print("-" * 80)

# 5-1. 병원 종별 분포
if 'eqp_clCdNm' in df.columns:
    print("병원 종별 분포 (eqp_clCdNm):")
    type_dist = df['eqp_clCdNm'].value_counts()
    for idx, (type_name, count) in enumerate(type_dist.items(), 1):
        pct = (count / len(df) * 100)
        print(f"  {idx}. {type_name}: {count}건 ({pct:.1f}%)")
    print()
    
    # 시각화 2: 병원 종별 분포
    print("[시각화] 병원 종별 분포 차트 생성 중...")
    fig, ax = plt.subplots(figsize=(10, 6))
    type_dist.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title('병원 종별 분포', fontsize=16, fontweight='bold')
    ax.set_xlabel('병원 수', fontsize=12)
    ax.set_ylabel('종별', fontsize=12)
    for i, v in enumerate(type_dist.values):
        ax.text(v + 5, i, f'{v}건', va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "02_hospital_type_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 저장: 02_hospital_type_distribution.png")
    print()

# 5-2. 시군구별 분포
if 'eqp_sgguCdNm' in df.columns:
    print("시군구별 분포 (eqp_sgguCdNm):")
    district_dist = df['eqp_sgguCdNm'].value_counts()
    for idx, (district, count) in enumerate(district_dist.items(), 1):
        pct = (count / len(df) * 100)
        print(f"  {idx}. {district}: {count}건 ({pct:.1f}%)")
    print()
    
    # 시각화 3: 시군구별 분포
    print("[시각화] 시군구별 분포 차트 생성 중...")
    fig, ax = plt.subplots(figsize=(10, 6))
    district_dist.plot(kind='barh', ax=ax, color='lightcoral')
    ax.set_title('시군구별 의료기관 분포', fontsize=16, fontweight='bold')
    ax.set_xlabel('병원 수', fontsize=12)
    ax.set_ylabel('시군구', fontsize=12)
    for i, v in enumerate(district_dist.values):
        ax.text(v + 5, i, f'{v}건', va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "03_district_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 저장: 03_district_distribution.png")
    print()

# ============================================================================
# 주요 수치형 변수 분석
# ============================================================================

print("[6] 주요 수치형 변수 분석")
print("-" * 80)

# 6-1. 병상수 분포
if 'eqp_totBdCnt' in df.columns:
    bed_count = df['eqp_totBdCnt'].dropna()
    if len(bed_count) > 0:
        print(f"총 병상수 (eqp_totBdCnt) 통계:")
        print(f"  - 평균: {bed_count.mean():.2f}개")
        print(f"  - 중앙값: {bed_count.median():.2f}개")
        print(f"  - 최소: {bed_count.min():.0f}개")
        print(f"  - 최대: {bed_count.max():.0f}개")
        print(f"  - 표준편차: {bed_count.std():.2f}개")
        print()
        
        # 시각화 4: 병상수 분포
        print("[시각화] 병상수 분포 히스토그램 생성 중...")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 히스토그램
        ax1.hist(bed_count, bins=30, color='lightgreen', edgecolor='black', alpha=0.7)
        ax1.set_title('병상수 분포', fontsize=14, fontweight='bold')
        ax1.set_xlabel('병상수', fontsize=12)
        ax1.set_ylabel('병원 수', fontsize=12)
        ax1.axvline(bed_count.mean(), color='red', linestyle='--', linewidth=2, label=f'평균: {bed_count.mean():.1f}')
        ax1.axvline(bed_count.median(), color='blue', linestyle='--', linewidth=2, label=f'중앙값: {bed_count.median():.1f}')
        ax1.legend()
        
        # 박스플롯
        ax2.boxplot(bed_count, vert=True)
        ax2.set_title('병상수 박스플롯', fontsize=14, fontweight='bold')
        ax2.set_ylabel('병상수', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(VIZ_DIR / "04_bed_count_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] 저장: 04_bed_count_distribution.png")
        print()

# 6-2. 설립연도 분석
if 'eqp_estbDd' in df.columns:
    # 설립일자를 연도로 변환 (YYYYMMDD 형식)
    df['설립연도'] = df['eqp_estbDd'].astype(str).str[:4]
    df['설립연도'] = pd.to_numeric(df['설립연도'], errors='coerce')
    
    estb_year = df['설립연도'].dropna()
    # 유효한 연도만 필터링 (1900-2026)
    estb_year = estb_year[(estb_year >= 1900) & (estb_year <= 2026)]
    
    if len(estb_year) > 0:
        print(f"설립연도 통계:")
        print(f"  - 평균: {estb_year.mean():.0f}년")
        print(f"  - 중앙값: {estb_year.median():.0f}년")
        print(f"  - 최소: {estb_year.min():.0f}년")
        print(f"  - 최대: {estb_year.max():.0f}년")
        print()
        
        # 시각화 5: 설립연도 분포
        print("[시각화] 설립연도 분포 차트 생성 중...")
        fig, ax = plt.subplots(figsize=(12, 6))
        year_counts = estb_year.value_counts().sort_index()
        ax.bar(year_counts.index, year_counts.values, color='mediumpurple', alpha=0.7)
        ax.set_title('설립연도별 의료기관 수', fontsize=16, fontweight='bold')
        ax.set_xlabel('설립연도', fontsize=12)
        ax.set_ylabel('병원 수', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(VIZ_DIR / "05_establishment_year_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] 저장: 05_establishment_year_distribution.png")
        print()

# ============================================================================
# 진료과목 분석
# ============================================================================

print("[7] 진료과목 분석")
print("-" * 80)

if 'dgsbjt_dgsbjtCdNm' in df.columns:
    # 진료과목은 쉼표로 구분된 문자열일 수 있음
    dept_data = df['dgsbjt_dgsbjtCdNm'].dropna()
    
    # 모든 진료과목 추출
    all_depts = []
    for depts in dept_data:
        if isinstance(depts, str):
            # 쉼표, 세미콜론, 슬래시 등으로 구분
            dept_list = str(depts).replace(';', ',').replace('/', ',').split(',')
            all_depts.extend([d.strip() for d in dept_list if d.strip()])
    
    if all_depts:
        dept_counts = pd.Series(all_depts).value_counts()
        print(f"총 진료과목 종류: {len(dept_counts)}개")
        print(f"진료과목 상위 10개:")
        for idx, (dept, count) in enumerate(dept_counts.head(10).items(), 1):
            pct = (count / len(df) * 100)
            print(f"  {idx}. {dept}: {count}건 ({pct:.1f}%)")
        print()
        
        # 시각화 6: 진료과목 분포 (상위 15개)
        print("[시각화] 진료과목 분포 차트 생성 중...")
        fig, ax = plt.subplots(figsize=(12, 8))
        top_depts = dept_counts.head(15)
        top_depts.plot(kind='barh', ax=ax, color='orange', alpha=0.7)
        ax.set_title('진료과목 분포 (상위 15개)', fontsize=16, fontweight='bold')
        ax.set_xlabel('병원 수', fontsize=12)
        ax.set_ylabel('진료과목', fontsize=12)
        for i, v in enumerate(top_depts.values):
            ax.text(v + 1, i, f'{v}건', va='center', fontsize=9)
        plt.tight_layout()
        plt.savefig(VIZ_DIR / "06_department_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] 저장: 06_department_distribution.png")
        print()

# ============================================================================
# 주차 정보 분석
# ============================================================================

print("[8] 주차 정보 분석")
print("-" * 80)

parking_info = {}
if 'dtl_parkQty' in df.columns:
    park_qty = df['dtl_parkQty'].dropna()
    if len(park_qty) > 0:
        parking_info['주차 가능 대수'] = {
            '평균': park_qty.mean(),
            '중앙값': park_qty.median(),
            '최소': park_qty.min(),
            '최대': park_qty.max()
        }
        print(f"주차 가능 대수 통계:")
        print(f"  - 평균: {park_qty.mean():.1f}대")
        print(f"  - 중앙값: {park_qty.median():.1f}대")
        print(f"  - 최소: {park_qty.min():.0f}대")
        print(f"  - 최대: {park_qty.max():.0f}대")
        print()

if 'dtl_parkXpnsYn' in df.columns:
    park_fee = df['dtl_parkXpnsYn'].value_counts()
    print(f"주차비 유무:")
    for fee_type, count in park_fee.items():
        pct = (count / len(df) * 100)
        print(f"  - {fee_type}: {count}건 ({pct:.1f}%)")
    print()
    
    # 시각화 7: 주차 정보 분석
    print("[시각화] 주차 정보 분석 차트 생성 중...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # 주차 가능 대수 분포
    if 'dtl_parkQty' in df.columns and len(park_qty) > 0:
        ax1.hist(park_qty, bins=30, color='teal', edgecolor='black', alpha=0.7)
        ax1.set_title('주차 가능 대수 분포', fontsize=14, fontweight='bold')
        ax1.set_xlabel('주차 가능 대수', fontsize=12)
        ax1.set_ylabel('병원 수', fontsize=12)
        ax1.axvline(park_qty.mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'평균: {park_qty.mean():.1f}대')
        ax1.legend()
    
    # 주차비 유무
    if 'dtl_parkXpnsYn' in df.columns:
        park_fee.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90, 
                     colors=['lightblue', 'lightcoral'])
        ax2.set_title('주차비 유무', fontsize=14, fontweight='bold')
        ax2.set_ylabel('')
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "07_parking_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 저장: 07_parking_analysis.png")
    print()

# ============================================================================
# 진료시간 패턴 분석
# ============================================================================

print("[9] 진료시간 패턴 분석")
print("-" * 80)

# 요일별 진료 시작/종료 시간 컬럼
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday_names = ['월', '화', '수', '목', '금', '토', '일']

operating_hours = {}
for day, day_kr in zip(weekdays, weekday_names):
    start_col = f'dtl_trmt{day}Start'
    end_col = f'dtl_trmt{day}End'
    
    if start_col in df.columns and end_col in df.columns:
        start_times = df[start_col].dropna()
        end_times = df[end_col].dropna()
        
        if len(start_times) > 0:
            operating_hours[day_kr] = {
                '시작': start_times.mode()[0] if len(start_times.mode()) > 0 else None,
                '종료': end_times.mode()[0] if len(end_times.mode()) > 0 else None,
                '데이터 수': len(start_times)
            }

if operating_hours:
    print("요일별 진료시간 (최빈값):")
    for day, times in operating_hours.items():
        if times['시작'] and times['종료']:
            print(f"  - {day}요일: {times['시작']} ~ {times['종료']} ({times['데이터 수']}건)")
    print()
    
    # 시각화 8: 진료시간 패턴
    print("[시각화] 진료시간 패턴 차트 생성 중...")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    days = list(operating_hours.keys())
    data_counts = [operating_hours[day]['데이터 수'] for day in days]
    
    ax.bar(days, data_counts, color='steelblue', alpha=0.7)
    ax.set_title('요일별 진료시간 정보 제공 현황', fontsize=16, fontweight='bold')
    ax.set_xlabel('요일', fontsize=12)
    ax.set_ylabel('데이터 제공 병원 수', fontsize=12)
    
    for i, (day, count) in enumerate(zip(days, data_counts)):
        ax.text(i, count + 5, f'{count}건', ha='center', fontsize=10)
        if operating_hours[day]['시작'] and operating_hours[day]['종료']:
            time_text = f"{operating_hours[day]['시작']}\n~\n{operating_hours[day]['종료']}"
            ax.text(i, count/2, time_text, ha='center', va='center', 
                   fontsize=8, color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "08_operating_hours_pattern.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 저장: 08_operating_hours_pattern.png")
    print()

# ============================================================================
# API별 데이터 완성도 분석
# ============================================================================

print("[10] API별 데이터 완성도 분석")
print("-" * 80)

api_completeness = {}
for prefix, name in api_prefixes.items():
    cols = api_columns[prefix]
    if cols:
        total_cells = len(df) * len(cols)
        missing_cells = df[cols].isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells * 100)
        api_completeness[name] = {
            '컬럼 수': len(cols),
            '완성도(%)': completeness,
            '결측 셀': missing_cells
        }

print("API별 데이터 완성도:")
for api_name, stats in sorted(api_completeness.items(), key=lambda x: x[1]['완성도(%)'], reverse=True):
    print(f"  - {api_name}: {stats['완성도(%)']:.1f}% (컬럼: {stats['컬럼 수']}개, 결측: {stats['결측 셀']:,}개)")
print()

# ============================================================================
# 요약 통계
# ============================================================================

print("=" * 80)
print("EDA 완료 요약")
print("=" * 80)
print(f"[OK] 총 데이터: {len(df):,}건")
print(f"[OK] 총 컬럼: {len(df.columns)}개")
print(f"[OK] 생성된 시각화: 8개")
print(f"[OK] 저장 위치: {VIZ_DIR}")
print()
print("생성된 시각화 파일:")
viz_files = [
    "01_missing_data_heatmap.png",
    "02_hospital_type_distribution.png",
    "03_district_distribution.png",
    "04_bed_count_distribution.png",
    "05_establishment_year_distribution.png",
    "06_department_distribution.png",
    "07_parking_analysis.png",
    "08_operating_hours_pattern.png"
]
for viz_file in viz_files:
    print(f"  - {viz_file}")
print()
print("=" * 80)
