# -*- coding: utf-8 -*-
"""
?섏썝湲??쇰?怨??낆? 遺꾩꽍 - 醫낇빀 ?됯?
?묒꽦?? 2026-02-03
踰꾩쟾: 1.0
?ㅻ챸: 紐⑤뱺 遺꾩꽍 寃곌낵瑜??듯빀?섏뿬 理쒖쟻 ?낆? TOP 5瑜?異붿쿇?⑸땲??
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path`r`nimport sys`r`n`r`n# 한글 폰트 설정`r`ncurrent_dir = Path(__file__).parent`r`nsys.path.insert(0, str(current_dir))`r`nfrom korean_font_setup import setup_korean_font`r`nsetup_korean_font()

# ?쒓? ?고듃 ?ㅼ젙


print("=" * 80)
print("醫낇빀 ?됯? 諛?理쒖쟻 ?낆? 異붿쿇")
print("=" * 80)

# ?곗씠??濡쒕뵫
print("\n[1/5] 遺꾩꽍 寃곌낵 濡쒕뵫 以?..", flush=True)

base_path = Path('d:/git_gb4pro/data/?쒖슱??二쇱슂 82?μ냼 ?곸뿭/REPORT/')
output_path = base_path / '05_醫낇빀?됯?'

# 媛?遺꾩꽍 寃곌낵 濡쒕뵫
try:
    df_competition = pd.read_csv(base_path / '01_寃쎌웳?섍꼍遺꾩꽍/?곴텒蹂??먰룷?꾪솴.csv', encoding='utf-8-sig')
    print("  ??寃쎌웳?섍꼍 遺꾩꽍 寃곌낵")
except:
    df_competition = None
    print("  ??寃쎌웳?섍꼍 遺꾩꽍 寃곌낵 ?놁쓬")

try:
    df_customer = pd.read_csv(base_path / '02_怨좉컼遺꾩꽍/?곴텒蹂?留ㅼ텧?꾪솴.csv', encoding='utf-8-sig')
    print("  ??怨좉컼遺꾩꽍 寃곌낵")
except:
    df_customer = None
    print("  ??怨좉컼遺꾩꽍 寃곌낵 ?놁쓬")

try:
    df_population = pd.read_csv(base_path / '03_?멸뎄?좊룞遺꾩꽍/?곴텒蹂??멸뎄?꾪솴.csv', encoding='utf-8-sig')
    print("  ???멸뎄?좊룞 遺꾩꽍 寃곌낵")
except:
    df_population = None
    print("  ???멸뎄?좊룞 遺꾩꽍 寃곌낵 ?놁쓬")

try:
    df_location = pd.read_csv(base_path / '04_?낆?議곌굔遺꾩꽍/?곴텒蹂??낆??됯?.csv', encoding='utf-8-sig')
    print("  ???낆?議곌굔 遺꾩꽍 寃곌낵")
except:
    df_location = None
    print("  ???낆?議곌굔 遺꾩꽍 寃곌낵 ?놁쓬")

# [2/5] ?곗씠???듯빀
print("\n[2/5] ?곗씠???듯빀 以?..", flush=True)

# 湲곗? ?곗씠?고봽?덉엫 ?앹꽦
if df_competition is not None:
    df_integrated = df_competition[['?곴텒紐?]].copy()
elif df_customer is not None:
    df_integrated = df_customer[['?곴텒紐?]].copy()
elif df_population is not None:
    df_integrated = df_population[['?곴텒紐?]].copy()
else:
    print("  ???듯빀???곗씠???놁쓬")
    df_integrated = pd.DataFrame({'?곴텒紐?: []})

# 媛?遺꾩꽍 寃곌낵 蹂묓빀
if df_competition is not None:
    df_integrated = df_integrated.merge(
        df_competition[['?곴텒紐?, '?먰룷??, '?쒖옣?먯쑀??]],
        on='?곴텒紐?, how='outer'
    )

if df_customer is not None:
    df_integrated = df_integrated.merge(
        df_customer[['?곴텒紐?, '留ㅼ텧???듭썝']],
        on='?곴텒紐?, how='outer'
    )

if df_population is not None:
    df_integrated = df_integrated.merge(
        df_population[['?곴텒紐?, '珥앹씤援?]],
        on='?곴텒紐?, how='outer'
    )

if df_location is not None:
    df_integrated = df_integrated.merge(
        df_location[['?곴텒紐?, '醫낇빀?먯닔']],
        on='?곴텒紐?, how='outer'
    )

print(f"  - ?듯빀 ?곴텒 ?? {len(df_integrated)}媛?)
print(f"  - ?듯빀 吏???? {len(df_integrated.columns)-1}媛?)

# [3/5] 醫낇빀 ?먯닔 怨꾩궛
print("\n[3/5] 醫낇빀 ?먯닔 怨꾩궛 以?..", flush=True)

# 寃곗륫移?泥섎━
df_integrated = df_integrated.fillna(0)

# 媛?吏???뺢퇋??(0~1)
score_df = df_integrated.copy()

# 寃쎌웳 媛뺣룄 (??쓣?섎줉 醫뗭쓬 - ??젙洹쒗솕)
if '?먰룷?? in score_df.columns:
    max_val = score_df['?먰룷??].max()
    if max_val > 0:
        score_df['寃쎌웳?먯닔'] = 1 - (score_df['?먰룷??] / max_val)
    else:
        score_df['寃쎌웳?먯닔'] = 0
else:
    score_df['寃쎌웳?먯닔'] = 0

# 留ㅼ텧 ?좎옱??(?믪쓣?섎줉 醫뗭쓬)
if '留ㅼ텧???듭썝' in score_df.columns:
    max_val = score_df['留ㅼ텧???듭썝'].max()
    if max_val > 0:
        score_df['留ㅼ텧?먯닔'] = score_df['留ㅼ텧???듭썝'] / max_val
    else:
        score_df['留ㅼ텧?먯닔'] = 0
else:
    score_df['留ㅼ텧?먯닔'] = 0

# ?멸뎄 洹쒕え (?믪쓣?섎줉 醫뗭쓬)
if '珥앹씤援? in score_df.columns:
    max_val = score_df['珥앹씤援?].max()
    if max_val > 0:
        score_df['?멸뎄?먯닔'] = score_df['珥앹씤援?] / max_val
    else:
        score_df['?멸뎄?먯닔'] = 0
else:
    score_df['?멸뎄?먯닔'] = 0

# ?낆? 議곌굔 (?대? ?뺢퇋?붾맖)
if '醫낇빀?먯닔' in score_df.columns:
    score_df['?낆??먯닔'] = score_df['醫낇빀?먯닔']
else:
    score_df['?낆??먯닔'] = 0

# 媛以묒튂 ?곸슜 醫낇빀 ?먯닔
weights = {
    '寃쎌웳?먯닔': 0.20,  # 寃쎌웳 ?섍꼍 20%
    '留ㅼ텧?먯닔': 0.30,  # 留ㅼ텧 ?좎옱??30%
    '?멸뎄?먯닔': 0.25,  # ?멸뎄 洹쒕え 25%
    '?낆??먯닔': 0.25   # ?낆? 議곌굔 25%
}

score_df['理쒖쥌?먯닔'] = (
    score_df['寃쎌웳?먯닔'] * weights['寃쎌웳?먯닔'] +
    score_df['留ㅼ텧?먯닔'] * weights['留ㅼ텧?먯닔'] +
    score_df['?멸뎄?먯닔'] * weights['?멸뎄?먯닔'] +
    score_df['?낆??먯닔'] * weights['?낆??먯닔']
) * 100  # 100??留뚯젏

# ?쒖쐞 ?곗젙
score_df = score_df.sort_values('理쒖쥌?먯닔', ascending=False).reset_index(drop=True)
score_df['?쒖쐞'] = range(1, len(score_df) + 1)

print(f"\n理쒖쟻 ?낆? TOP 5:")
for idx, row in score_df.head(5).iterrows():
    print(f"  {row['?쒖쐞']}?? {row['?곴텒紐?]}: {row['理쒖쥌?먯닔']:.1f}??)

# [4/5] ?쒓컖??
print("\n[4/5] ?쒓컖??諛?寃곌낵 ???以?..", flush=True)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('媛뺣궓援??쇰?怨??낆? 醫낇빀 ?됯?', fontsize=16, fontweight='bold')

# 1. TOP 5 醫낇빀 ?먯닔
ax1 = axes[0, 0]
top5 = score_df.head(5)
ax1.barh(range(len(top5)), top5['理쒖쥌?먯닔'], color='crimson')
ax1.set_yticks(range(len(top5)))
ax1.set_yticklabels([f"{row['?쒖쐞']}?? {row['?곴텒紐?]}" for _, row in top5.iterrows()])
ax1.set_xlabel('醫낇빀 ?먯닔')
ax1.set_title('理쒖쟻 ?낆? TOP 5', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)
ax1.invert_yaxis()

# 2. ?몃? ?먯닔 鍮꾧탳 (?덉씠??李⑦듃)
ax2 = axes[0, 1]
categories = ['寃쎌웳?섍꼍', '留ㅼ텧?좎옱??, '?멸뎄洹쒕え', '?낆?議곌굔']
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

for idx, row in top5.head(3).iterrows():
    values = [
        row['寃쎌웳?먯닔'] * 100,
        row['留ㅼ텧?먯닔'] * 100,
        row['?멸뎄?먯닔'] * 100,
        row['?낆??먯닔'] * 100
    ]
    values += values[:1]
    ax2.plot(angles, values, 'o-', linewidth=2, label=f"{row['?쒖쐞']}?? {row['?곴텒紐?]}")
    ax2.fill(angles, values, alpha=0.15)

ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories)
ax2.set_ylim(0, 100)
ax2.set_title('TOP 3 ?곴텒 ?몃? ?먯닔 鍮꾧탳', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax2.grid(True)

# 3. ?꾩껜 ?곴텒 ?먯닔 遺꾪룷
ax3 = axes[1, 0]
ax3.hist(score_df['理쒖쥌?먯닔'], bins=10, color='steelblue', edgecolor='black', alpha=0.7)
ax3.axvline(score_df['理쒖쥌?먯닔'].mean(), color='red', linestyle='--', linewidth=2, label=f'?됯퇏: {score_df["理쒖쥌?먯닔"].mean():.1f}??)
ax3.set_xlabel('醫낇빀 ?먯닔')
ax3.set_ylabel('?곴텒 ??)
ax3.set_title('?꾩껜 ?곴텒 ?먯닔 遺꾪룷', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# 4. 醫낇빀 ?됯? ?붿빟
ax4 = axes[1, 1]
ax4.axis('off')
top1 = score_df.iloc[0]
metrics_text = f"""
醫낇빀 ?됯? 寃곌낵

?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺

?룇 理쒖슦???낆?
  ???곴텒紐? {top1['?곴텒紐?]}
  ??醫낇빀 ?먯닔: {top1['理쒖쥌?먯닔']:.1f}??

?뱤 ?몃? ?먯닔
  ??寃쎌웳 ?섍꼍: {top1['寃쎌웳?먯닔']*100:.1f}??(媛以묒튂 20%)
  ??留ㅼ텧 ?좎옱?? {top1['留ㅼ텧?먯닔']*100:.1f}??(媛以묒튂 30%)
  ???멸뎄 洹쒕え: {top1['?멸뎄?먯닔']*100:.1f}??(媛以묒튂 25%)
  ???낆? 議곌굔: {top1['?낆??먯닔']*100:.1f}??(媛以묒튂 25%)

?렞 ?됯? 湲곗?
  ??遺꾩꽍 ?곴텒: {len(score_df)}媛?
  ???됯퇏 ?먯닔: {score_df['理쒖쥌?먯닔'].mean():.1f}??
  ???곗닔 ?곴텒 (70???댁긽): {(score_df['理쒖쥌?먯닔'] >= 70).sum()}媛?

?뮕 異붿쿇
  ??1?쒖쐞: {score_df.iloc[0]['?곴텒紐?]}
  ??2?쒖쐞: {score_df.iloc[1]['?곴텒紐?] if len(score_df) > 1 else 'N/A'}
  ??3?쒖쐞: {score_df.iloc[2]['?곴텒紐?] if len(score_df) > 2 else 'N/A'}
"""
ax4.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center', )

plt.tight_layout()

# ???
output_path.mkdir(parents=True, exist_ok=True)
fig.savefig(output_path / '醫낇빀?됯?_寃곌낵.png', dpi=300, bbox_inches='tight')
print(f"  ??洹몃옒????? {output_path / '醫낇빀?됯?_寃곌낵.png'}")

# [5/5] 寃곌낵 ???
print("\n[5/5] 理쒖쥌 寃곌낵 ???以?..", flush=True)

# ?꾩껜 寃곌낵 ???
score_df.to_csv(output_path / '?꾩껜_?곴텒_?됯?寃곌낵.csv', index=False, encoding='utf-8-sig')
print(f"  ???꾩껜 寃곌낵: {output_path / '?꾩껜_?곴텒_?됯?寃곌낵.csv'}")

# TOP 5 ???
top5_result = score_df.head(5)[['?쒖쐞', '?곴텒紐?, '理쒖쥌?먯닔', '寃쎌웳?먯닔', '留ㅼ텧?먯닔', '?멸뎄?먯닔', '?낆??먯닔']]
top5_result.to_csv(output_path / '理쒖쟻?낆?_TOP5.csv', index=False, encoding='utf-8-sig')
print(f"  ??TOP 5 寃곌낵: {output_path / '理쒖쟻?낆?_TOP5.csv'}")

print("\n" + "=" * 80)
print("??醫낇빀 ?됯? ?꾨즺!")
print("=" * 80)
print(f"\n?렞 理쒖쥌 異붿쿇 ?낆?:")
print(f"  1?쒖쐞: {score_df.iloc[0]['?곴텒紐?]} ({score_df.iloc[0]['理쒖쥌?먯닔']:.1f}??")
if len(score_df) > 1:
    print(f"  2?쒖쐞: {score_df.iloc[1]['?곴텒紐?]} ({score_df.iloc[1]['理쒖쥌?먯닔']:.1f}??")
if len(score_df) > 2:
    print(f"  3?쒖쐞: {score_df.iloc[2]['?곴텒紐?]} ({score_df.iloc[2]['理쒖쥌?먯닔']:.1f}??")
print(f"\n?뱚 寃곌낵 ?뚯씪:")
print(f"  - {output_path / '醫낇빀?됯?_寃곌낵.png'}")
print(f"  - {output_path / '理쒖쟻?낆?_TOP5.csv'}")
print(f"\n?ㅼ쓬 ?④퀎: 99_?꾩껜?ㅽ뻾.py濡??꾩껜 ?뚯씠?꾨씪???ㅽ뻾\n")
