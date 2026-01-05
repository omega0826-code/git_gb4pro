import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import re
from collections import Counter
from wordcloud import WordCloud

# 한글 폰트 설정
if os.name == 'nt':
    plt.rc('font', family='Malgun Gothic')
    FONT_PATH = r'C:/Windows/Fonts/malgun.ttf'
elif sys.platform == 'darwin':
    plt.rc('font', family='AppleGothic')
    FONT_PATH = r'/System/Library/Fonts/AppleGothic.ttf'
else:
    plt.rc('font', family='NanumGothic')
    FONT_PATH = r'/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

plt.rc('axes', unicode_minus=False)

# 경로 설정
DATA_PATH = r'crawling/gangnam/data/gangnam_hospitals_final_20260105_065921.csv'
REPORT_PATH = r'eda/eda_step2_report.md'
IMAGE_DIR = r'eda/images'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

f = open(REPORT_PATH, 'w', encoding='utf-8')

def write_report(text):
    f.write(text + '\n')
    f.flush()

write_report("# 2차 EDA: 병원 소개글(Introduction) 심층 분석")
write_report("## 1. 데이터 로드 및 전처리")

# 데이터 로드
try:
    df = pd.read_csv(DATA_PATH, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(DATA_PATH, encoding='cp949')
    except Exception as e:
        write_report(f"데이터 로드 실패: {e}")
        f.close()
        sys.exit()
except Exception as e:
    write_report(f"데이터 로드 에러: {e}")
    f.close()
    sys.exit()

# Introduction 컬럼만 추출 및 결측치 제거
intro_df = df[['hospital_name', 'introduction']].dropna()
write_report(f"- 전체 데이터 수: {len(df)}")
write_report(f"- 소개글이 있는 병원 수: {len(intro_df)}")

# 중복 소개글 확인
dup_count = intro_df.duplicated(subset=['introduction']).sum()
write_report(f"- 중복된 소개글 수: {dup_count} (프랜차이즈 또는 동일 병원의 중복 등록 가능성)")

write_report("\n## 2. 정량적 구조 분석")

# 파생 변수 생성
intro_df['char_len'] = intro_df['introduction'].apply(len)
intro_df['word_count'] = intro_df['introduction'].apply(lambda x: len(x.split()))
intro_df['newline_count'] = intro_df['introduction'].apply(lambda x: x.count('\n'))

# 통계 요약
try:
    write_report(intro_df[['char_len', 'word_count', 'newline_count']].describe().to_markdown())
except:
    write_report(str(intro_df[['char_len', 'word_count', 'newline_count']].describe()))

# 시각화: 글자 수 분포
plt.figure(figsize=(10, 5))
sns.histplot(intro_df['char_len'], bins=50, kde=True)
plt.title('소개글 글자 수 분포')
plt.xlabel('글자 수')
plt.savefig(os.path.join(IMAGE_DIR, 'intro_char_len.png'))
plt.close()
write_report("\n![Char Len Dist](images/intro_char_len.png)")

# 시각화: 줄바꿈 수 분포
plt.figure(figsize=(10, 5))
sns.histplot(intro_df['newline_count'], bins=30, kde=True)
plt.title('소개글 줄바꿈(가독성) 분포')
plt.xlabel('줄바꿈 수')
plt.savefig(os.path.join(IMAGE_DIR, 'intro_newline_count.png'))
plt.close()
write_report("\n![Newline Count Dist](images/intro_newline_count.png)")

write_report("\n## 3. 키워드 분석 (단순 빈도 분석)")
write_report("- 형태소 분석기(Kiwi) 호환성 문제로 정규식 기반 단순 분석 수행.")

# 불용어 설정
STOPWORDS = {'병원', '진료', '수술', '시술', '환자', '저희', '합니다', '있는', '안녕하세요', '생각', 
             '위해', '통해', '가능', '다양', '제공', '노력', '최선', '약속', '치료', '관리', '과정',
             '결과', '마음', '사람', '개인', '맞춤', '상담', '부분', '가지', '방법', '경우', '문제',
             '시간', '사용', '진행', '원장', '의원', '클리닉', '센터', '분들', '가지', '까지', '대한', '만큼',
             '고객', '준비', '도움', '방식', '만족', '여러분', '방문', '감사', '성형', '외과', '피부', '피부과',
             '그리고', '또는', '하지만', '또한', '바로', '가장', '모든', '많은', '항상', '오직', '함께'}

# 간단한 조사 제거 함수
def remove_josa(word):
    josas = ['은', '는', '이', '가', '을', '를', '의', '에', '로', '으로', '에서', '에게', '께', '와', '과']
    for josa in josas:
        if word.endswith(josa) and len(word) > len(josa) + 1:
            return word[:-len(josa)]
    return word

def extract_keywords(text):
    # 한글만 남기고 공백으로 변환
    text = re.sub(r'[^가-힣\s]', ' ', text)
    words = text.split()
    keywords = []
    for word in words:
        word = remove_josa(word)
        if len(word) > 1 and word not in STOPWORDS:
            keywords.append(word)
    return keywords

# 전체 텍스트 분석
write_report("키워드 분석 진행 중...")
all_keywords = []
for text in intro_df['introduction']:
    all_keywords.extend(extract_keywords(text))

# 빈도 분석
counter = Counter(all_keywords)
top_50 = counter.most_common(50)

write_report("\n### Top 50 키워드")
top_50_df = pd.DataFrame(top_50, columns=['Keyword', 'Frequency'])
try:
    write_report(top_50_df.to_markdown())
except:
    write_report(str(top_50_df))

# 워드클라우드
write_report("\n### 워드클라우드 생성")
try:
    wc = WordCloud(font_path=FONT_PATH, 
                   background_color='white', 
                   width=800, 
                   height=600, 
                   max_words=100)
    wc.generate_from_frequencies(counter)
    wc.to_file(os.path.join(IMAGE_DIR, 'intro_wordcloud.png'))
    write_report("\n![WordCloud](images/intro_wordcloud.png)")
except Exception as e:
    write_report(f"워드클라우드 생성 실패: {e}")

write_report("\n## 4. 인사이트 요약")
write_report("- 키워드 분석 결과, 의료 서비스의 본질(안전, 정확, 정직 등)과 관련된 단어들이 추출되었는지 확인 필요.")
write_report("- 정규식 기반 분석이므로 형태소 분석 대비 정확도는 낮을 수 있으나 전반적인 경향 파악 가능.")

f.close()
print("EDA Step 2 Complete.")
