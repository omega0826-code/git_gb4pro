# -*- coding: utf-8 -*-
"""비중 + 집계(3년평균) 통합 CSV 생성"""
import pandas as pd, os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
df = pd.read_csv(os.path.join(BASE_DIR, 'output', 'preprocessed_supply_up.csv'), encoding='utf-8-sig')
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 업종 코드 순서
order = [
    '농업, 임업 및 어업(01~03)', '광업(05~08)', '제조업(10~34)',
    '전기, 가스, 증기 및 공기조절 공급업(35)', '수도, 하수 및 폐기물 처리, 원료 재생업(36~39)',
    '건설업(41~42)', '도매 및 소매업(45~47)', '운수 및 창고업(49~52)',
    '숙박 및 음식점업(55~56)', '정보통신업(58~63)', '금융 및 보험업(64~66)',
    '부동산업(68)', '전문, 과학 및 기술 서비스업(70~73)',
    '사업시설 관리, 사업 지원 및 임대 서비스업(74~76)',
    '공공행정, 국방 및 사회보장 행정(84)', '교육 서비스업(85)',
    '보건업 및 사회복지 서비스업(86~87)', '예술, 스포츠 및 여가관련 서비스업(90~91)',
    '협회 및 단체, 수리 및 기타 개인 서비스업(94~96)', '가구 내 고용활동(10차 전용)',
]

years = [2022, 2023, 2024]
groups = ['학력무관', '고졸이하', '전문대졸', '대졸', '대학원졸']

# 전체 구인
total = df.groupby(['통합_산업명','연도'])['구인인원'].sum().unstack(fill_value=0).reindex(order, fill_value=0)

# 학력그룹별
grp = {}
for g in groups:
    grp[g] = df[df['학력_그룹']==g].groupby(['통합_산업명','연도'])['구인인원'].sum().unstack(fill_value=0).reindex(order, fill_value=0)

jun = grp['전문대졸']; dae = grp['대졸']
comb = jun + dae

# 비중 계산
comb_r = (comb / total * 100).round(1).fillna(0)
jun_r = (jun / total * 100).round(1).fillna(0)
dae_r = (dae / total * 100).round(1).fillna(0)
comb_r['3년평균'] = comb_r.mean(axis=1).round(1)
jun_r['3년평균'] = jun_r.mean(axis=1).round(1)
dae_r['3년평균'] = dae_r.mean(axis=1).round(1)

# ===== 비중 CSV =====
ratio_df = pd.DataFrame()
ratio_df['순번'] = range(1, len(order)+1)
ratio_df['통합_산업명'] = order
for y in years:
    ratio_df[f'전문대+대졸_{y}(%)'] = comb_r[y].values
ratio_df['전문대+대졸_3년평균(%)'] = comb_r['3년평균'].values
for y in years:
    ratio_df[f'전문대졸_{y}(%)'] = jun_r[y].values
ratio_df['전문대졸_3년평균(%)'] = jun_r['3년평균'].values
for y in years:
    ratio_df[f'대졸_{y}(%)'] = dae_r[y].values
ratio_df['대졸_3년평균(%)'] = dae_r['3년평균'].values

p1 = os.path.join(OUTPUT_DIR, 'ratio_by_industry.csv')
ratio_df.to_csv(p1, index=False, encoding='utf-8-sig')
print(f"[저장] {p1}")

# ===== 집계 CSV (3년평균) =====
count_df = pd.DataFrame()
count_df['순번'] = range(1, len(order)+1)
count_df['통합_산업명'] = order

# 전체구인
for y in years:
    count_df[f'전체구인_{y}'] = total[y].values.astype(int)
count_df['전체구인_3년평균'] = total.mean(axis=1).round(0).astype(int).values

# 학력별
for g in groups:
    for y in years:
        count_df[f'{g}_{y}'] = grp[g][y].values.astype(int)
    count_df[f'{g}_3년평균'] = grp[g].mean(axis=1).round(0).astype(int).values

p2 = os.path.join(OUTPUT_DIR, 'count_by_industry.csv')
count_df.to_csv(p2, index=False, encoding='utf-8-sig')
print(f"[저장] {p2}")

# 콘솔 요약
print(f"\n비중 CSV: {ratio_df.shape}")
print(f"집계 CSV: {count_df.shape}")
print(f"\n컬럼 (비중): {ratio_df.columns.tolist()}")
print(f"컬럼 (집계): {count_df.columns.tolist()}")
