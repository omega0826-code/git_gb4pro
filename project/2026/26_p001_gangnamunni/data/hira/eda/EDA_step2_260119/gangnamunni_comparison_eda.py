"""
강남언니 입점 업체 vs 미입점 업체 비교 분석 EDA
작성 일시: 2026-01-20 00:24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("=" * 80)
print("강남언니 입점 업체 vs 미입점 업체 비교 분석 EDA")
print("=" * 80)

# ============================================================================
# Step 1: 데이터 로드
# ============================================================================
print("\n[Step 1] 데이터 로드 중...")

# 결합된 데이터 로드
data_path = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\data\병원데이터_결합완료_20260120_000249.csv'
df = pd.read_csv(data_path, encoding='utf-8-sig')

print(f"  - 총 데이터: {len(df):,}건")
print(f"  - 총 컬럼: {len(df.columns)}개")

# ============================================================================
# Step 2: 입점 여부 식별
# ============================================================================
print("\n[Step 2] 입점 여부 식별 중...")

# _merge 컬럼으로 입점 여부 판단
df['입점여부'] = df['_merge'].apply(
    lambda x: '입점' if x == 'both' else '미입점'
)

입점_count = (df['입점여부'] == '입점').sum()
미입점_count = (df['입점여부'] == '미입점').sum()

print(f"  - 입점 업체: {입점_count:,}건 ({입점_count/len(df)*100:.1f}%)")
print(f"  - 미입점 업체: {미입점_count:,}건 ({미입점_count/len(df)*100:.1f}%)")

# 그룹 분리
입점_df = df[df['입점여부'] == '입점'].copy()
미입점_df = df[df['입점여부'] == '미입점'].copy()

# ============================================================================
# Step 3: 파생 변수 생성
# ============================================================================
print("\n[Step 3] 파생 변수 생성 중...")

for data in [df, 입점_df, 미입점_df]:
    # 의사 유형
    data['의사유형'] = data['dgsbjt_dgsbjtPrSdrCnt'].apply(
        lambda x: '전문의' if x > 0 else '일반의'
    )
    
    # 병원 규모
    data['총의사수'] = data['dgsbjt_cdiagDrCnt'] + data['dgsbjt_dgsbjtPrSdrCnt']
    data['병원규모'] = data['총의사수'].apply(
        lambda x: 'Type A (대형)' if x >= 5 
        else ('Type B (중형)' if x >= 2 else 'Type C (1인)')
    )
    
    # 수술 가능 여부
    data['수술가능'] = data['eqp_soprmCnt'].apply(
        lambda x: '수술가능' if x >= 1 else '시술중심'
    )

print("  - 파생 변수 생성 완료")

# ============================================================================
# Step 4: Part 1 - 입점 업체 특징 분석
# ============================================================================
print("\n[Step 4] Part 1 - 입점 업체 특징 분석 중...")

output_dir = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\EDA\EDA_step2_260119'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 4-1. 입점 업체 기본 프로필
입점_통계 = {
    '총_병원수': int(len(입점_df)),
    '평균_병상수': float(입점_df['eqp_stdSickbdCnt'].mean()),
    '평균_의사수': float(입점_df['총의사수'].mean()),
    '평균_직원수': float(입점_df['eqp_emymCnt'].mean()),
    '평균_수술실수': float(입점_df['eqp_soprmCnt'].mean())
}

print(f"\n  [입점 업체 기본 통계]")
for key, value in 입점_통계.items():
    if isinstance(value, float):
        print(f"    - {key}: {value:.2f}")
    else:
        print(f"    - {key}: {value:,}")

# 4-2. 입점 업체 유형 분포
입점_의사유형 = 입점_df['의사유형'].value_counts()
입점_병원규모 = 입점_df['병원규모'].value_counts()
입점_수술가능 = 입점_df['수술가능'].value_counts()

print(f"\n  [입점 업체 유형 분포]")
print(f"    전문의: {입점_의사유형.get('전문의', 0)}건 ({입점_의사유형.get('전문의', 0)/len(입점_df)*100:.1f}%)")
print(f"    일반의: {입점_의사유형.get('일반의', 0)}건 ({입점_의사유형.get('일반의', 0)/len(입점_df)*100:.1f}%)")

# 4-3. 입점 업체 지역 분포
입점_지역분포 = 입점_df.groupby('eqp_emdongNm').size().sort_values(ascending=False)
print(f"\n  [입점 업체 지역 분포 TOP 5]")
for i, (dong, count) in enumerate(입점_지역분포.head(5).items(), 1):
    print(f"    {i}. {dong}: {count}건 ({count/len(입점_df)*100:.1f}%)")

# ============================================================================
# Step 5: Part 2 - 비교 분석
# ============================================================================
print("\n[Step 5] Part 2 - 입점 vs 미입점 비교 분석 중...")

# 5-1. 규모 비교
비교_통계 = pd.DataFrame({
    '입점': [
        입점_df['eqp_stdSickbdCnt'].mean(),
        입점_df['총의사수'].mean(),
        입점_df['eqp_emymCnt'].mean(),
        입점_df['eqp_soprmCnt'].mean()
    ],
    '미입점': [
        미입점_df['eqp_stdSickbdCnt'].mean(),
        미입점_df['총의사수'].mean(),
        미입점_df['eqp_emymCnt'].mean(),
        미입점_df['eqp_soprmCnt'].mean()
    ]
}, index=['평균_병상수', '평균_의사수', '평균_직원수', '평균_수술실수'])

print(f"\n  [규모 비교]")
print(비교_통계.to_string())

# 5-2. 전문의 비율 비교
입점_전문의비율 = (입점_df['의사유형'] == '전문의').sum() / len(입점_df) * 100
미입점_전문의비율 = (미입점_df['의사유형'] == '전문의').sum() / len(미입점_df) * 100

print(f"\n  [전문의 비율 비교]")
print(f"    입점: {입점_전문의비율:.1f}%")
print(f"    미입점: {미입점_전문의비율:.1f}%")
print(f"    차이: {입점_전문의비율 - 미입점_전문의비율:+.1f}%p")

# 5-3. 수술실 보유율 비교
입점_수술실보유율 = (입점_df['수술가능'] == '수술가능').sum() / len(입점_df) * 100
미입점_수술실보유율 = (미입점_df['수술가능'] == '수술가능').sum() / len(미입점_df) * 100

print(f"\n  [수술실 보유율 비교]")
print(f"    입점: {입점_수술실보유율:.1f}%")
print(f"    미입점: {미입점_수술실보유율:.1f}%")
print(f"    차이: {입점_수술실보유율 - 미입점_수술실보유율:+.1f}%p")

# 5-4. 행정동별 입점률
행정동별_입점률 = df.groupby('eqp_emdongNm').apply(
    lambda x: (x['입점여부'] == '입점').sum() / len(x) * 100
).sort_values(ascending=False)

print(f"\n  [행정동별 입점률 TOP 5]")
for i, (dong, rate) in enumerate(행정동별_입점률.head(5).items(), 1):
    total = len(df[df['eqp_emdongNm'] == dong])
    입점 = (df[df['eqp_emdongNm'] == dong]['입점여부'] == '입점').sum()
    print(f"    {i}. {dong}: {rate:.1f}% ({입점}/{total})")

# ============================================================================
# Step 6: 통계적 비교
# ============================================================================
print("\n[Step 6] 통계적 비교 수행 중...")

# 병상 수 평균 차이
입점_병상평균 = 입점_df['eqp_stdSickbdCnt'].mean()
미입점_병상평균 = 미입점_df['eqp_stdSickbdCnt'].mean()
병상차이 = 입점_병상평균 - 미입점_병상평균

print(f"\n  [병상 수 평균 비교]")
print(f"    입점: {입점_병상평균:.2f}개")
print(f"    미입점: {미입점_병상평균:.2f}개")
print(f"    차이: {병상차이:+.2f}개 ({abs(병상차이)/미입점_병상평균*100:+.1f}%)")

# 의사 수 평균 차이
입점_의사평균 = 입점_df['총의사수'].mean()
미입점_의사평균 = 미입점_df['총의사수'].mean()
의사차이 = 입점_의사평균 - 미입점_의사평균

print(f"\n  [의사 수 평균 비교]")
print(f"    입점: {입점_의사평균:.2f}명")
print(f"    미입점: {미입점_의사평균:.2f}명")
print(f"    차이: {의사차이:+.2f}명 ({abs(의사차이)/미입점_의사평균*100:+.1f}%)")

# ============================================================================
# Step 7: 시각화
# ============================================================================
print("\n[Step 7] 시각화 생성 중...")

# 7-1. 입점 vs 미입점 규모 비교
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 병원 규모 분포
ax1 = axes[0, 0]
x = np.arange(len(입점_병원규모.index))
width = 0.35
입점_values = [입점_병원규모.get(cat, 0) for cat in ['Type C (1인)', 'Type B (중형)', 'Type A (대형)']]
미입점_values = [미입점_병원규모.get(cat, 0) for cat in ['Type C (1인)', 'Type B (중형)', 'Type A (대형)']]
ax1.bar(x - width/2, 입점_values, width, label='입점', color='#4A90E2')
ax1.bar(x + width/2, 미입점_values, width, label='미입점', color='#E74C3C')
ax1.set_xlabel('병원 규모', fontsize=12)
ax1.set_ylabel('병원 수', fontsize=12)
ax1.set_title('병원 규모 분포 비교', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(['Type C (1인)', 'Type B (중형)', 'Type A (대형)'])
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 전문의 비율
ax2 = axes[0, 1]
categories = ['전문의', '일반의']
입점_전문의_dist = [입점_의사유형.get('전문의', 0), 입점_의사유형.get('일반의', 0)]
미입점_전문의_dist = [미입점_df['의사유형'].value_counts().get('전문의', 0), 
                     미입점_df['의사유형'].value_counts().get('일반의', 0)]
x2 = np.arange(len(categories))
ax2.bar(x2 - width/2, 입점_전문의_dist, width, label='입점', color='#4A90E2')
ax2.bar(x2 + width/2, 미입점_전문의_dist, width, label='미입점', color='#E74C3C')
ax2.set_xlabel('의사 유형', fontsize=12)
ax2.set_ylabel('병원 수', fontsize=12)
ax2.set_title('전문의 vs 일반의 분포 비교', fontsize=14, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(categories)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 평균 지표 비교
ax3 = axes[1, 0]
metrics = ['병상수', '의사수', '직원수', '수술실수']
입점_metrics = [입점_df['eqp_stdSickbdCnt'].mean(), 입점_df['총의사수'].mean(),
               입점_df['eqp_emymCnt'].mean(), 입점_df['eqp_soprmCnt'].mean()]
미입점_metrics = [미입점_df['eqp_stdSickbdCnt'].mean(), 미입점_df['총의사수'].mean(),
                 미입점_df['eqp_emymCnt'].mean(), 미입점_df['eqp_soprmCnt'].mean()]
x3 = np.arange(len(metrics))
ax3.bar(x3 - width/2, 입점_metrics, width, label='입점', color='#4A90E2')
ax3.bar(x3 + width/2, 미입점_metrics, width, label='미입점', color='#E74C3C')
ax3.set_xlabel('지표', fontsize=12)
ax3.set_ylabel('평균값', fontsize=12)
ax3.set_title('평균 지표 비교', fontsize=14, fontweight='bold')
ax3.set_xticks(x3)
ax3.set_xticklabels(metrics)
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# 수술실 보유 비교
ax4 = axes[1, 1]
surgery_categories = ['수술가능', '시술중심']
입점_surgery = [입점_수술가능.get('수술가능', 0), 입점_수술가능.get('시술중심', 0)]
미입점_surgery = [미입점_df['수술가능'].value_counts().get('수술가능', 0),
                 미입점_df['수술가능'].value_counts().get('시술중심', 0)]
x4 = np.arange(len(surgery_categories))
ax4.bar(x4 - width/2, 입점_surgery, width, label='입점', color='#4A90E2')
ax4.bar(x4 + width/2, 미입점_surgery, width, label='미입점', color='#E74C3C')
ax4.set_xlabel('수술 인프라', fontsize=12)
ax4.set_ylabel('병원 수', fontsize=12)
ax4.set_title('수술 인프라 보유 비교', fontsize=14, fontweight='bold')
ax4.set_xticks(x4)
ax4.set_xticklabels(surgery_categories)
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/comparison_overview_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: comparison_overview_{timestamp}.png")
plt.close()

# 7-2. 행정동별 입점률
fig, ax = plt.subplots(figsize=(14, 10))
행정동별_입점률.plot(kind='barh', ax=ax, color='#2ECC71')
ax.set_title('행정동별 입점률', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('입점률 (%)', fontsize=13)
ax.set_ylabel('행정동', fontsize=13)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# 값 표시
for i, v in enumerate(행정동별_입점률):
    ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/district_penetration_rate_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"  - 저장: district_penetration_rate_{timestamp}.png")
plt.close()

# ============================================================================
# Step 8: 결과 저장
# ============================================================================
print("\n[Step 8] 결과 저장 중...")

# 분석 결과 요약
analysis_summary = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'data_overview': {
        '총_병원수': int(len(df)),
        '입점_업체수': int(입점_count),
        '미입점_업체수': int(미입점_count),
        '입점률': float(입점_count / len(df) * 100)
    },
    'part1_입점업체특징': {
        '기본_통계': 입점_통계,
        '전문의_비율': float(입점_전문의비율),
        '수술실_보유율': float(입점_수술실보유율),
        '상위5개_지역': {k: int(v) for k, v in 입점_지역분포.head(5).items()}
    },
    'part2_비교분석': {
        '평균_지표_비교': {
            '입점': {
                '병상수': float(입점_df['eqp_stdSickbdCnt'].mean()),
                '의사수': float(입점_df['총의사수'].mean()),
                '직원수': float(입점_df['eqp_emymCnt'].mean()),
                '수술실수': float(입점_df['eqp_soprmCnt'].mean())
            },
            '미입점': {
                '병상수': float(미입점_df['eqp_stdSickbdCnt'].mean()),
                '의사수': float(미입점_df['총의사수'].mean()),
                '직원수': float(미입점_df['eqp_emymCnt'].mean()),
                '수술실수': float(미입점_df['eqp_soprmCnt'].mean())
            }
        },
        '전문의_비율_비교': {
            '입점': float(입점_전문의비율),
            '미입점': float(미입점_전문의비율),
            '차이': float(입점_전문의비율 - 미입점_전문의비율)
        },
        '수술실_보유율_비교': {
            '입점': float(입점_수술실보유율),
            '미입점': float(미입점_수술실보유율),
            '차이': float(입점_수술실보유율 - 미입점_수술실보유율)
        },
        '통계적_비교': {
            '병상수_비교': {
                '입점_평균': float(입점_병상평균),
                '미입점_평균': float(미입점_병상평균),
                '차이': float(병상차이),
                '차이_비율': float(abs(병상차이)/미입점_병상평균*100)
            },
            '의사수_비교': {
                '입점_평균': float(입점_의사평균),
                '미입점_평균': float(미입점_의사평균),
                '차이': float(의사차이),
                '차이_비율': float(abs(의사차이)/미입점_의사평균*100)
            }
        }
    }
}

# JSON 저장
summary_file = f'{output_dir}/analysis_summary_{timestamp}.json'
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_summary, f, ensure_ascii=False, indent=2)
print(f"  - 저장: analysis_summary_{timestamp}.json")

# ============================================================================
# 완료
# ============================================================================
print("\n" + "=" * 80)
print("[완료] 강남언니 입점 비교 분석 완료!")
print("=" * 80)
print(f"\n생성된 파일:")
print(f"  1. comparison_overview_{timestamp}.png")
print(f"  2. district_penetration_rate_{timestamp}.png")
print(f"  3. analysis_summary_{timestamp}.json")
print(f"\n저장 위치: {output_dir}")
