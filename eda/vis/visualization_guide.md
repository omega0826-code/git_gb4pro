# 시각화 코드 모듈화 가이드

EDA에 사용된 주요 시각화 코드 패턴 및 재사용 가능한 함수 예시입니다.

## 1. 한글 폰트 설정
OS별로 한글 폰트를 자동으로 설정하여 그래프 깨짐을 방지합니다.

```python
import os
import sys
import matplotlib.pyplot as plt

def set_korean_font():
    """
    OS 환경에 맞는 한글 폰트를 설정합니다.
    Windows: Malgun Gothic
    Mac: AppleGothic
    Linux: NanumGothic
    """
    if os.name == 'nt':
        plt.rc('font', family='Malgun Gothic')
    elif sys.platform == 'darwin':
        plt.rc('font', family='AppleGothic')
    else:
        plt.rc('font', family='NanumGothic')
    
    # 마이너스 기호 깨짐 방지
    plt.rc('axes', unicode_minus=False)
```

## 2. 히스토그램 (Histogram)
수치형 데이터의 분포를 파악합니다.

```python
import seaborn as sns

def plot_histogram(data, column, title, save_path=None, bins=30):
    plt.figure(figsize=(10, 5))
    sns.histplot(data[column], bins=bins, kde=True)
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
```

## 3. 바 차트 (Bar Chart)
범주형 데이터의 빈도를 비교합니다.

```python
def plot_bar_chart(x_data, y_data, title, save_path=None):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_data, y=y_data)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
```

## 4. 워드클라우드 (WordCloud)
텍스트 키워드 빈도를 시각화합니다. 한글 폰트 경로(`font_path`) 지정이 필수입니다.

```python
from wordcloud import WordCloud

def generate_wordcloud(frequencies, font_path, save_path=None):
    """
    frequencies: Counter 객체 또는 {단어: 빈도} 딕셔너리
    font_path: 한글 폰트 파일 경로 (예: C:/Windows/Fonts/malgun.ttf)
    """
    wc = WordCloud(font_path=font_path, 
                   background_color='white', 
                   width=800, height=600,
                   max_words=100)
    wc.generate_from_frequencies(frequencies)
    
    if save_path:
        wc.to_file(save_path)
    else:
        return wc.to_image()
```
