import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# 한글 폰트 설정
if os.name == 'nt':
    plt.rc('font', family='Malgun Gothic')
elif sys.platform == 'darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rc('axes', unicode_minus=False)

# 경로 설정
DATA_PATH = r'crawling/gangnam/data/gangnam_hospitals_final_20260105_065921.csv'
REPORT_PATH = r'eda/eda_step1_report.md'
IMAGE_DIR = r'eda/images'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 리포트 파일 열기
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    def write_report(text):
        f.write(text + '\n')
        print(text)

    write_report("# 1차 EDA 분석 리포트")
    write_report("## 1. 데이터 개요")

    # 데이터 로드
    try:
        # encoding='utf-8'로 읽기
        df = pd.read_csv(DATA_PATH, encoding='utf-8')
    except UnicodeDecodeError:
        write_report("utf-8 로드 실패, cp949 시도...")
        try:
            df = pd.read_csv(DATA_PATH, encoding='cp949')
        except Exception as e:
            write_report(f"데이터 로드 실패: {e}")
            sys.exit()
    except Exception as e:
        write_report(f"데이터 로드 에러: {e}")
        sys.exit()

    write_report(f"- 데이터 크기: {df.shape}")
    write_report(f"- 컬럼 목록: {df.columns.tolist()}")
    
    # 마크다운 테이블 출력을 위해 to_markdown() 사용. (tabulate 라이브러리 필요할 수 있음. 없으면 문자열로)
    try:
        write_report("\n### 데이터 샘플")
        write_report(df.head().to_markdown())
    except:
        write_report("\n### 데이터 샘플 (Markdown 변환 실패)")
        write_report(str(df.head()))

    write_report("\n## 2. 결측치 분석")
    missing = df.isnull().sum()
    missing_ratio = (missing / len(df)) * 100
    missing_df = pd.DataFrame({'Missing Count': missing, 'Ratio (%)': missing_ratio})
    
    try:
        write_report(missing_df.to_markdown())
    except:
        write_report(str(missing_df))

    # 결측치 시각화
    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing.index, y=missing.values)
    plt.xticks(rotation=45)
    plt.title('컬럼별 결측치 수')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'missing_values.png'))
    plt.close()
    write_report("\n![Missing Values](images/missing_values.png)")

    write_report("\n## 3. 기초 통계량 (수치형)")
    try:
        write_report(df.describe().to_markdown())
    except:
        write_report(str(df.describe()))

    write_report("\n## 4. 컬럼별 상세 분석")

    # Rating
    write_report("\n### Rating (평점)")
    try:
        write_report(df['rating'].describe().to_markdown())
    except:
        write_report(str(df['rating'].describe()))
    
    plt.figure(figsize=(10, 5))
    sns.histplot(df['rating'], bins=20, kde=True)
    plt.title('평점 분포')
    plt.savefig(os.path.join(IMAGE_DIR, 'rating_dist.png'))
    plt.close()
    write_report("\n![Rating Distribution](images/rating_dist.png)")

    # Review Count
    write_report("\n### Review Count (리뷰 수)")
    try:
        write_report(df['review_count'].describe().to_markdown())
    except:
        write_report(str(df['review_count'].describe()))
    
    plt.figure(figsize=(10, 5))
    sns.histplot(df['review_count'], bins=50, kde=True)
    plt.title('리뷰 수 분포')
    plt.xlabel('리뷰 수')
    plt.savefig(os.path.join(IMAGE_DIR, 'review_count_dist.png'))
    plt.close()
    write_report("\n![Review Count Distribution](images/review_count_dist.png)")

    # Event Count
    write_report("\n### Event Count (이벤트 수)")
    try:
        write_report(df['event_count'].describe().to_markdown())
    except:
        write_report(str(df['event_count'].describe()))
    
    plt.figure(figsize=(10, 5))
    sns.histplot(df['event_count'], bins=30, kde=True)
    plt.title('이벤트 수 분포')
    plt.savefig(os.path.join(IMAGE_DIR, 'event_count_dist.png'))
    plt.close()
    write_report("\n![Event Count Distribution](images/event_count_dist.png)")

    # District Code
    write_report("\n### District Code (지역 코드)")
    district_counts = df['district_code'].value_counts()
    try:
        write_report(district_counts.head(10).to_markdown())
    except:
        write_report(str(district_counts.head(10)))

    plt.figure(figsize=(12, 6))
    sns.barplot(x=district_counts.index[:20], y=district_counts.values[:20]) # Top 20
    plt.xticks(rotation=45)
    plt.title('지역 코드 빈도 (Top 20)')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'district_count.png'))
    plt.close()
    write_report("\n![District Count](images/district_count.png)")

    # Treatment Tags (간단 분석)
    write_report("\n### Treatment Tags (진료 태그)")
    tags_list = []
    for tags in df['treatment_tags'].dropna():
        if isinstance(tags, str):
            # 문자열 정리 및 분리
            cleaned_tags = tags.replace("'", "").replace("[", "").replace("]", "").replace('"', "")
            splitted = [t.strip() for t in cleaned_tags.split(",")]
            tags_list.extend([t for t in splitted if t]) # 빈 문자열 제외
    
    if tags_list:
        tags_series = pd.Series(tags_list)
        top_tags = tags_series.value_counts().head(20)
        try:
            write_report(f"Top 20 Tags:\n{top_tags.to_markdown()}")
        except:
            write_report(f"Top 20 Tags:\n{str(top_tags)}")

        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_tags.index, y=top_tags.values)
        plt.xticks(rotation=45)
        plt.title('진료 태그 빈도 (Top 20)')
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_DIR, 'tags_count.png'))
        plt.close()
        write_report("\n![Tags Count](images/tags_count.png)")
    else:
        write_report("태그 데이터를 분석할 수 없습니다.")

    # Doctors
    write_report("\n### Doctors (의사)")
    write_report(f"Doctors 컬럼 결측치 수: {df['doctors'].isnull().sum()}")
    try:
        write_report(f"Doctors 데이터 샘플 (Top 5):\n{df['doctors'].dropna().head(5).to_markdown()}")
    except:
        write_report(f"Doctors 데이터 샘플 (Top 5):\n{str(df['doctors'].dropna().head(5))}")

    # Address
    write_report("\n### Address (주소)")
    # 주소에서 '구' 단위 추출 시도
    def extract_gu(addr):
        if isinstance(addr, str):
            parts = addr.split()
            for part in parts:
                if part.endswith('구') and len(part) > 1:
                    return part
            if len(parts) > 1:
                 return parts[1]
        return "Unknown"

    df['gu'] = df['address'].apply(extract_gu)
    gu_counts = df['gu'].value_counts()
    try:
        write_report(gu_counts.head(20).to_markdown())
    except:
        write_report(str(gu_counts.head(20)))
    
    plt.figure(figsize=(12, 6))
    if len(gu_counts) > 0:
        sns.barplot(x=gu_counts.index[:20], y=gu_counts.values[:20])
        plt.title('지역구 분포 (주소 기반)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_DIR, 'address_gu_dist.png'))
    plt.close()
    write_report("\n![Address Gu Distribution](images/address_gu_dist.png)")

print("EDA Step 1 Complete.")
