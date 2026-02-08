# -*- coding: utf-8 -*-
"""
폰트 개선 사항 적용 테스트 - 간단한 분석 예제
V4.01 가이드라인 기반
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

print("=" * 80)
print("[테스트] 폰트 개선 사항 적용 분석")
print("=" * 80)
print()

# ============================================================================
# 1. 한글 폰트 설정 (V4.01 개선 방법)
# ============================================================================
print("[1/5] 한글 폰트 설정...")

try:
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    korean_fonts = ['Malgun Gothic', 'NanumGothic', 'Gulim', 'Batang']
    
    selected_font = None
    for font in korean_fonts:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False
        print(f"  [OK] 한글 폰트 설정: {selected_font}")
    else:
        print("  [WARNING] 한글 폰트를 찾을 수 없습니다.")
        plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    print(f"  [WARNING] 폰트 설정 중 오류: {e}")
    plt.rcParams['axes.unicode_minus'] = False

print()

# ============================================================================
# 2. 샘플 데이터 생성
# ============================================================================
print("[2/5] 샘플 데이터 생성...")

# 강남구 주요 상권 샘플 데이터
data = {
    '상권명': ['강남역', '역삼역', '가로수길', '강남구청', '양재역'],
    '경쟁강도': [0.85, 0.72, 0.68, 0.55, 0.45],
    '고객수요': [0.92, 0.78, 0.85, 0.65, 0.58],
    '인구유동': [0.88, 0.75, 0.70, 0.60, 0.52],
    '입지조건': [0.90, 0.80, 0.75, 0.70, 0.65],
    '종합점수': [88.8, 76.3, 74.5, 62.5, 55.0]
}

df = pd.DataFrame(data)
print(f"  [OK] 샘플 데이터 생성 완료 ({len(df)}개 상권)")
print()

# ============================================================================
# 3. 그래프 생성 (한글 표시 테스트)
# ============================================================================
print("[3/5] 그래프 생성 중...")

output_dir = Path('d:/git_gb4pro/data/서울시 주요 82장소 영역/REPORT/TEST_OUTPUT')
output_dir.mkdir(parents=True, exist_ok=True)

# 그래프 1: 종합점수 막대 그래프
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1-1. 종합점수 막대 그래프
ax1 = axes[0, 0]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
ax1.barh(df['상권명'], df['종합점수'], color=colors)
ax1.set_xlabel('종합점수')
ax1.set_title('상권별 종합평가 점수', fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# 1-2. 경쟁강도 vs 고객수요 산점도
ax2 = axes[0, 1]
scatter = ax2.scatter(df['경쟁강도'], df['고객수요'], 
                     s=df['종합점수']*10, c=df['종합점수'], 
                     cmap='viridis', alpha=0.6, edgecolors='black')
for idx, row in df.iterrows():
    ax2.annotate(row['상권명'], (row['경쟁강도'], row['고객수요']),
                xytext=(5, 5), textcoords='offset points', fontsize=9)
ax2.set_xlabel('경쟁강도')
ax2.set_ylabel('고객수요')
ax2.set_title('경쟁강도 vs 고객수요', fontsize=14, fontweight='bold')
ax2.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax2, label='종합점수')

# 1-3. 레이더 차트 (상위 3개 상권)
ax3 = axes[1, 0]
categories = ['경쟁강도', '고객수요', '인구유동', '입지조건']
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

for idx in range(3):
    values = df.iloc[idx][['경쟁강도', '고객수요', '인구유동', '입지조건']].tolist()
    values += values[:1]
    ax3.plot(angles, values, 'o-', linewidth=2, label=df.iloc[idx]['상권명'])
    ax3.fill(angles, values, alpha=0.15)

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(categories)
ax3.set_ylim(0, 1)
ax3.set_title('상위 3개 상권 비교 (레이더 차트)', fontsize=14, fontweight='bold')
ax3.legend(loc='upper right')
ax3.grid(True)

# 1-4. 지표별 평균 비교
ax4 = axes[1, 1]
metrics = ['경쟁강도', '고객수요', '인구유동', '입지조건']
means = [df[m].mean() for m in metrics]
bars = ax4.bar(metrics, means, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax4.set_ylabel('평균값')
ax4.set_title('지표별 평균 비교', fontsize=14, fontweight='bold')
ax4.set_ylim(0, 1)
ax4.grid(axis='y', alpha=0.3)

# 막대 위에 값 표시
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}', ha='center', va='bottom')

plt.tight_layout()
output_path = output_dir / '폰트_테스트_종합분석.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"  [OK] 그래프 저장: {output_path.name}")
plt.close()

print()

# ============================================================================
# 4. 결과 요약 테이블 생성
# ============================================================================
print("[4/5] 결과 요약 테이블 생성...")

fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('tight')
ax.axis('off')

# 테이블 데이터
table_data = []
table_data.append(['순위', '상권명', '경쟁강도', '고객수요', '인구유동', '입지조건', '종합점수'])
for idx, row in df.iterrows():
    table_data.append([
        idx + 1,
        row['상권명'],
        f"{row['경쟁강도']:.2f}",
        f"{row['고객수요']:.2f}",
        f"{row['인구유동']:.2f}",
        f"{row['입지조건']:.2f}",
        f"{row['종합점수']:.1f}"
    ])

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.08, 0.15, 0.12, 0.12, 0.12, 0.12, 0.12])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# 헤더 스타일
for i in range(7):
    table[(0, i)].set_facecolor('#4ECDC4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# 순위별 색상
colors_rank = ['#FFD93D', '#C8E6C9', '#BBDEFB', '#F8BBD0', '#E1BEE7']
for i in range(1, 6):
    table[(i, 0)].set_facecolor(colors_rank[i-1])

plt.title('상권별 종합평가 결과 요약', fontsize=16, fontweight='bold', pad=20)
output_path = output_dir / '폰트_테스트_결과표.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"  [OK] 결과표 저장: {output_path.name}")
plt.close()

print()

# ============================================================================
# 5. 검증 및 완료
# ============================================================================
print("[5/5] 검증 완료")
print()
print("=" * 80)
print("[완료] 폰트 개선 사항 적용 테스트 완료!")
print("=" * 80)
print()
print(f"생성된 파일:")
print(f"  - {output_dir / '폰트_테스트_종합분석.png'}")
print(f"  - {output_dir / '폰트_테스트_결과표.png'}")
print()
print("결과 확인:")
print("  1. 생성된 이미지 파일을 열어 한글이 정상 표시되는지 확인하세요")
print("  2. 네모 박스(□) 없이 한글이 표시되면 성공입니다")
print()
