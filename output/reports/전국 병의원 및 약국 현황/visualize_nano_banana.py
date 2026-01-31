import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================================
# NANO BANANA BUSINESS COLOR PALETTE
# ============================================================================
BG_COLOR = '#0F0F0F'      # Deep Dark Background
PRIMARY_COLOR = '#DFFF00'   # Nano Banana (Neon Yellow)
SECONDARY_COLOR = '#FFFFFF' # White
ACCENT_COLOR = '#333333'    # Dark Grey for grid
TEXT_COLOR = '#EEEEEE'
BAR_COLORS = ['#DFFF00', '#C4E000', '#A9C100', '#8EA200', '#738300', '#586400']

# ============================================================================
# 1. 데이터 로드
# ============================================================================
file_path = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/강남구_병원_진료과목수_분석.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# ============================================================================
# 2. 분석 데이터 준비
# ============================================================================
# 인포카드를 위한 통계
total_hospitals = len(df)
multi_dept_hospitals = len(df[df['진료과목수'] >= 2])
multi_ratio = (multi_dept_hospitals / total_hospitals) * 100
avg_depts = df[df['진료과목수'] > 0]['진료과목수'].mean()

# 유형별 분포
type_order = ['단일 진료과목', '2-3개 진료과목', '4-5개 진료과목', '6-10개 진료과목', '11개 이상 진료과목']
type_dist = df['병원유형'].value_counts().reindex(type_order).fillna(0)

# 종별 평균
type_dept_avg = df.groupby('종별코드명')['진료과목수'].mean().sort_values(ascending=False).head(8)

# ============================================================================
# 3. 시각화 (Nano Banana Style)
# ============================================================================
fig = plt.figure(figsize=(20, 14), facecolor=BG_COLOR)
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.2])

# 타이틀 및 아시아틱 요소
plt.suptitle('GANGNAM MULTI-DEPARTMENT CLINIC ANALYSIS 2025', 
             color=PRIMARY_COLOR, fontsize=32, fontweight='black', y=0.96)
plt.figtext(0.5, 0.92, '강남구 병원 진료과목 집적도 및 다과목 의원 분포 프리미엄 리포트', 
            color=SECONDARY_COLOR, fontsize=16, ha='center', alpha=0.8)

# --- [상단: 인포그래픽 카드 스타일] ---
# 실제 그래프 대신 텍스트 카드로 핵심 지표 강조
ax_info = fig.add_subplot(gs[0, 0])
ax_info.set_facecolor(BG_COLOR)
ax_info.axis('off')

stats_data = [
    ("TOTAL HOSPITALS", f"{total_hospitals:,}", "강남구 병원 총계"),
    ("MULTI-DEPT RATIO", f"{multi_ratio:.1f}%", "다과목 병원 비중"),
    ("AVG DEPARTMENTS", f"{avg_depts:.1f}", "병원당 평균 과목수")
]

for i, (label, val, desc) in enumerate(stats_data):
    y_pos = 0.8 - i*0.3
    ax_info.text(0, y_pos, label, color=PRIMARY_COLOR, fontsize=14, fontweight='bold')
    ax_info.text(0, y_pos - 0.08, val, color=SECONDARY_COLOR, fontsize=36, fontweight='black')
    ax_info.text(0, y_pos - 0.15, desc, color=SECONDARY_COLOR, fontsize=11, alpha=0.6)

# --- [상단 중앙: 유형별 도넛 차트] ---
ax_pie = fig.add_subplot(gs[0, 1])
ax_pie.set_facecolor(BG_COLOR)
wedges, texts, autotexts = ax_pie.pie(type_dist.values, labels=type_dist.index, 
                                      autopct='%1.1f%%', startangle=140, 
                                      colors=BAR_COLORS, 
                                      wedgeprops={'width': 0.4, 'edgecolor': BG_COLOR, 'linewidth': 3},
                                      textprops={'color': SECONDARY_COLOR, 'fontsize': 10})
plt.setp(autotexts, size=10, weight="bold", color=BG_COLOR)
ax_pie.set_title('CLINIC TYPE COMPOSITION', color=PRIMARY_COLOR, fontsize=18, fontweight='bold', pad=20)

# --- [상단 우측: 종별 평균 바 차트] ---
ax_type = fig.add_subplot(gs[0, 2])
ax_type.set_facecolor(BG_COLOR)
bars = ax_type.barh(type_dept_avg.index, type_dept_avg.values, color=PRIMARY_COLOR, alpha=0.8)
ax_type.tick_params(colors=SECONDARY_COLOR, labelsize=10)
ax_type.spines['bottom'].set_color(ACCENT_COLOR)
ax_type.spines['left'].set_color(ACCENT_COLOR)
ax_type.spines['top'].set_visible(False)
ax_type.spines['right'].set_visible(False)
ax_type.grid(axis='x', color=ACCENT_COLOR, linestyle='--', alpha=0.3)
ax_type.set_title('AVG DEPT BY CATEGORY', color=PRIMARY_COLOR, fontsize=18, fontweight='bold', pad=20)
for bar in bars:
    ax_type.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                 f"{bar.get_width():.1f}", color=PRIMARY_COLOR, va='center', fontweight='bold')

# --- [하단: 진료과목수 상세 분포 (전체 점유)] ---
ax_main = fig.add_subplot(gs[1, :])
ax_main.set_facecolor(BG_COLOR)
dept_counts = df['진료과목수'].value_counts().sort_index().head(21) # 20개까지
bars = ax_main.bar(dept_counts.index, dept_counts.values, color=PRIMARY_COLOR, width=0.7, edgecolor=BG_COLOR)

# 디자인 디테일: 바 상단 값 표시
for bar in bars:
    height = bar.get_height()
    ax_main.text(bar.get_x() + bar.get_width()/2., height + 10,
                 f'{int(height)}', ha='center', va='bottom', 
                 color=SECONDARY_COLOR, fontsize=10, fontweight='bold')

ax_main.set_xticks(range(21))
ax_main.tick_params(colors=SECONDARY_COLOR, labelsize=11)
ax_main.set_xlabel('NUMBER OF DEPARTMENTS', color=SECONDARY_COLOR, fontsize=12, labelpad=15)
ax_main.set_ylabel('HOSPITAL COUNT', color=SECONDARY_COLOR, fontsize=12, labelpad=15)
ax_main.spines['bottom'].set_color(ACCENT_COLOR)
ax_main.spines['left'].set_color(ACCENT_COLOR)
ax_main.spines['top'].set_visible(False)
ax_main.spines['right'].set_visible(False)
ax_main.grid(axis='y', color=ACCENT_COLOR, linestyle='--', alpha=0.2)
ax_main.set_title('DETAILED DISTRIBUTION OF DEPARTMENTS (GANGNAM-GU)', 
                  color=PRIMARY_COLOR, fontsize=20, fontweight='bold', pad=30)

# 워터마크 및 푸터
plt.figtext(0.95, 0.05, 'ANTIGRAVITY BUSINESS INTELLIGENCE | DATA SOURCE: HIRA 2025.12', 
            color=PRIMARY_COLOR, fontsize=10, ha='right', alpha=0.5)

plt.subplots_adjust(left=0.08, right=0.95, top=0.88, bottom=0.1, hspace=0.4, wspace=0.3)
output_path = 'd:/git_gb4pro/output/reports/전국 병의원 및 약국 현황/강남구_다과목의원_분포분석_나노바나나.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
print(f"Visualized chart saved to: {output_path}")
