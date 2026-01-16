# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import base64
from io import BytesIO

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
df = pd.read_csv(r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원전체정보_20260115_235745.csv', encoding='utf-8-sig')

# 지역별 분포 계산 (시도별)
region_counts = df['eqp_sidoCdNm'].value_counts()


# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))
region_counts.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('지역별 의료기관 분포', fontproperties=font_prop, fontsize=16, pad=20)
ax.set_xlabel('지역', fontproperties=font_prop, fontsize=12)
ax.set_ylabel('의료기관 수', fontproperties=font_prop, fontsize=12)
ax.tick_params(axis='x', rotation=45)

# x축 레이블에 한글 폰트 적용
for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Base64로 인코딩
buffer = BytesIO()
plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
buffer.seek(0)
img_base64 = base64.b64encode(buffer.read()).decode()

# 결과 출력
print(img_base64)
