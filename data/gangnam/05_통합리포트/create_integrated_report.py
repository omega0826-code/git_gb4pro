# -*- coding: utf-8 -*-
"""
피부과 입지선정 통합 분석 리포트 생성
5개 챕터, 30개 시각화 통합
"""

import base64
from pathlib import Path
from datetime import datetime

# 경로 설정
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M')
BASE_DIR = Path(r'D:\git_gb4pro\data\gangnam')

# 각 챕터별 소스 폴더
CH1_DIR = BASE_DIR / '01_공급분석'
CH2_DIR = BASE_DIR / '02_경쟁분석'
CH3_DIR = BASE_DIR / '03_수요분석'
CH4_DIR = BASE_DIR / '04_입지선정'
OUTPUT_DIR = BASE_DIR / '05_통합리포트'
OUTPUT_FILE = OUTPUT_DIR / f'피부과_입지선정_통합리포트_{TIMESTAMP}.html'

def encode_img(path):
    """이미지를 Base64로 인코딩"""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def img_section(title, img_path, insight=""):
    """이미지 섹션 HTML 생성"""
    if not img_path.exists():
        return f"<p>⚠️ 이미지 없음: {img_path.name}</p>"
    return f"""
    <div class="chart-box">
        <h3>{title}</h3>
        <img src="data:image/png;base64,{encode_img(img_path)}" alt="{title}">
        {f'<p class="insight">{insight}</p>' if insight else ''}
    </div>
    """

# HTML 템플릿 시작
print(f"통합 리포트 생성 시작: {TIMESTAMP}")

html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>피부과 입지선정 통합 분석 리포트</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Malgun Gothic', sans-serif; 
            margin: 0; 
            padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 30px auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{ margin: 0; font-size: 2.5em; }}
        header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        nav {{
            background: #2c3e50;
            padding: 15px 40px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        nav a {{
            color: white;
            text-decoration: none;
            margin-right: 25px;
            font-weight: bold;
            opacity: 0.8;
            transition: opacity 0.3s;
        }}
        nav a:hover {{ opacity: 1; }}
        .chapter {{
            padding: 40px;
            border-bottom: 1px solid #eee;
        }}
        .chapter h2 {{
            color: #e74c3c;
            border-left: 5px solid #e74c3c;
            padding-left: 15px;
            margin-bottom: 30px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
        }}
        .chart-box {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .chart-box h3 {{
            color: #2c3e50;
            margin: 0 0 15px 0;
            font-size: 1.1em;
        }}
        .chart-box img {{
            width: 100%;
            border-radius: 10px;
        }}
        .insight {{
            background: #e8f4fd;
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 0.9em;
            color: #2980b9;
            border-left: 4px solid #3498db;
        }}
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .comparison-table th, .comparison-table td {{
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }}
        .comparison-table th {{
            background: #2c3e50;
            color: white;
        }}
        .comparison-table tr:nth-child(even) {{ background: #f8f9fa; }}
        .pro {{ color: #27ae60; }}
        .con {{ color: #e74c3c; }}
        .recommendation {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        .mice-box {{
            background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 피부과 입지선정 통합 분석 리포트</h1>
            <p>강남구 피부과 개원을 위한 최적 입지 도출 | 생성일: {TIMESTAMP}</p>
        </header>
        
        <nav>
            <a href="#ch1">Ch1. 공급분석</a>
            <a href="#ch2">Ch2. 경쟁분석</a>
            <a href="#ch3">Ch3. 수요분석</a>
            <a href="#ch4">Ch4. 입지선정</a>
            <a href="#ch5">Ch5. 결론</a>
        </nav>
"""

# Chapter 1: 공급 분석
print("Ch1. 공급 분석 추가 중...")
ch1_charts = [
    ('01_type_distribution.png', '종별 분포', '의원급 98.5%로 소규모 전문 클리닉 중심'),
    ('02_district_distribution.png', '자치구별 분포', '강남구 23.7%로 압도적 1위'),
    ('03_establish_distribution.png', '설립구분 분포', '개인 설립이 대다수'),
    ('04_year_distribution.png', '개설연도 추이', '2010년대 개원 러시'),
    ('05_specialist_analysis.png', '전문의 분포', '기관당 평균 1.3명'),
    ('06_bed_analysis.png', '병상 현황', '외래 중심 운영'),
    ('06b_bed_per_hospital.png', '병원당 평균 병상', '의원급은 대부분 무병상'),
    ('07_department_analysis.png', '병행 진료과목', '성형외과 병행 최다'),
    ('08_age_size_analysis.png', '병원 연령대', '중견(10-20년) 기관 최다'),
]

html += """
        <div class="chapter" id="ch1">
            <h2>Chapter 1: 공급 분석 (서울 피부과 현황)</h2>
            <p>서울시 피부과 4,853개 기관의 현황을 분석합니다.</p>
            <div class="chart-grid">
"""
for img, title, insight in ch1_charts:
    html += img_section(title, CH1_DIR / img, insight)
html += "</div></div>"

# Chapter 2: 경쟁 분석
print("Ch2. 경쟁 분석 추가 중...")
ch2_charts = [
    ('01_institution_scale.png', '기관 수 비교', '강남구 1,150개로 서울의 23.7%'),
    ('02_type_composition.png', '종별 구성비', '의원급 비중 유사'),
    ('03_specialist_comparison.png', '전문의 비교', '강남구 전문의 밀도 최고'),
    ('04_bed_comparison.png', '병상 비교', '종합병원급만 유의미한 병상'),
    ('05_establishment_trend.png', '설립연도 분포', '강남구 개원 활발'),
    ('06_new_clinic_ratio.png', '신규개원 비율', '최근 5년 개원 증가'),
    ('07_department_heatmap.png', '진료과목 히트맵', '성형외과 병행 비율 최다'),
]

html += """
        <div class="chapter" id="ch2">
            <h2>Chapter 2: 경쟁 분석 (강남 vs 서울)</h2>
            <p>강남구와 서초구, 송파구, 서울 평균을 비교합니다.</p>
            <div class="chart-grid">
"""
for img, title, insight in ch2_charts:
    html += img_section(title, CH2_DIR / img, insight)
html += "</div></div>"

# Chapter 3: 수요 분석
print("Ch3. 수요 분석 추가 중...")
ch3_charts = [
    ('A1_경쟁_점포수.png', 'A1. 경쟁 강도', '상권별 피부과 밀집도'),
    ('B1_타겟_매출.png', 'B1. 타겟 매출', '20-40대 매출 분석'),
    ('B2_성별_매출.png', 'B2. 성별 매출', '여성 vs 남성'),
    ('B3_연령대별_매출.png', 'B3. 연령대별 매출', '세부 연령대 분포'),
    ('C1_유동인구.png', 'C1. 유동인구', '상권별 유동인구 규모'),
    ('C2_타겟_유동인구.png', 'C2. 타겟 유동인구', '20-40대 유동인구'),
    ('C3_직장인구.png', 'C3. 직장인구', '주간 직장인구'),
    ('C4_상주인구.png', 'C4. 상주인구', '거주 인구'),
    ('D1_집객시설.png', 'D1. 집객시설', '상권별 집객시설 현황'),
    ('D2_평균소득.png', 'D2. 평균소득', '소득 수준'),
    ('D3_의료비지출.png', 'D3. 의료비지출', '의료비 지출 현황'),
    ('E1_종합점수_순위.png', 'E1. 종합점수 순위', '가중치 기반 순위'),
    ('E2_레이더_TOP3.png', 'E2. TOP3 레이더', '상위 3개 상권 비교'),
    ('E3_세부지표_히트맵.png', 'E3. 세부지표 히트맵', '전체 지표 비교'),
]

html += """
        <div class="chapter" id="ch3">
            <h2>Chapter 3: 수요 분석 (강남 9개 상권)</h2>
            <p>강남구 9개 주요 상권의 수요 환경을 분석합니다.</p>
            <div class="chart-grid">
"""
for img, title, insight in ch3_charts:
    html += img_section(title, CH3_DIR / 'charts' / img, insight)
html += "</div></div>"

# Chapter 4: 입지 선정
print("Ch4. 입지 선정 추가 중...")
html += """
        <div class="chapter" id="ch4">
            <h2>Chapter 4: 입지 선정</h2>
            <p>Ch3. 강남 9개 상권 분석 결과를 바탕으로 최적 입지를 선정합니다.</p>
            
            <h3>4.1 TOP 3 상권 장단점 비교</h3>
            <p><em>※ Ch3 종합 평가 결과 기반 (가중치: 경쟁 20% + 고객 40% + 인구 20% + 입지 20%)</em></p>
            <table class="comparison-table">
                <tr>
                    <th>순위</th>
                    <th>상권</th>
                    <th>종합점수</th>
                    <th>장점</th>
                    <th>단점</th>
                    <th>적합 전략</th>
                </tr>
                <tr>
                    <td><strong>🥇 1위</strong></td>
                    <td><strong>강남역</strong></td>
                    <td><strong style="color:#e74c3c;">75.8점</strong></td>
                    <td class="pro">• 고객 수요 최고 (타겟 매출 2,764억)<br>• 유동인구 815만 압도적<br>• 집객시설 389개 인프라 최고</td>
                    <td class="con">• 경쟁 최고 (684개소)<br>• 임대료 최고 수준</td>
                    <td>고객 수요 극대화 + 차별화 필수</td>
                </tr>
                <tr>
                    <td><strong>🥈 2위</strong></td>
                    <td><strong>선릉역</strong></td>
                    <td><strong style="color:#3498db;">45.4점</strong></td>
                    <td class="pro">• 균형 잡힌 지표<br>• 의료비 지출 4.5억 높음<br>• 직장인 수요 안정적</td>
                    <td class="con">• 중간 경쟁 강도<br>• 강남역 대비 고객 수요 25%</td>
                    <td>직장인 타겟 안정 운영</td>
                </tr>
                <tr>
                    <td><strong>🥉 3위</strong></td>
                    <td><strong>강남 마이스</strong></td>
                    <td><strong style="color:#27ae60;">39.3점</strong></td>
                    <td class="pro">• 저경쟁 블루오션 (10개소)<br>• 평균 소득 701만원 최고<br>• 직장인구 10.2만 1위</td>
                    <td class="con">• 유동인구 11만 최하위<br>• 집객시설 부족</td>
                    <td>저경쟁 + 고소득 직장인 타겟<br>+ MICE 특구 외국인 의료관광</td>
                </tr>
            </table>
            
            <h3>4.2 최적 입지 추천</h3>
            <div class="recommendation">
                <h3>🎯 1순위 추천: 강남역 상권 (75.8점)</h3>
                <p><strong>Ch3 분석 결과 기반 추천 근거:</strong></p>
                <ul>
                    <li><strong>고객 수요 점수 1.00 (만점)</strong> → 타겟 매출 2,764억으로 압도적 1위</li>
                    <li><strong>인구 유동 점수 0.97</strong> → 유동인구 815만, 타겟(20-40대) 586만 최다</li>
                    <li><strong>입지 조건 점수 0.82</strong> → 집객시설 389개, 의료비 지출 4.7억</li>
                    <li>경쟁 점수 0.00 (684개소 최다) → <strong>차별화 전략 필수</strong></li>
                </ul>
                <p><strong>권장 전략:</strong> 프리미엄 피부미용 전문 + 강력한 마케팅으로 경쟁 돌파</p>
            </div>
            
            <h3>4.3 마이스특구 추가 후보지</h3>
            <div class="mice-box">
                <h3>🌏 외국인 의료관광 고려: 강남 마이스 상권 (39.3점 / 3위)</h3>
                <p><strong>강남 마이스(MICE) 특구 지정</strong>으로 인한 외국인 유입 증가 예상:</p>
                <ul>
                    <li><strong>경쟁 점수 0.99 (10개소)</strong> → 신규 진입 시 저경쟁 블루오션</li>
                    <li><strong>평균 소득 701만원</strong>으로 소득 수준 1위</li>
                    <li><strong>직장인구 10.2만</strong>으로 직장인 타겟 유리</li>
                    <li>코엑스/현대백화점 인접 → 외국인 관광객 접근성 우수</li>
                </ul>
                <p><strong>권장 전략:</strong> 외국어 대응 + 의료관광 패키지 연계 → 중장기 성장 포텐셜 높음</p>
            </div>
        </div>
"""


# Chapter 5: 최종 결론
print("Ch5. 결론 추가 중...")
html += """
        <div class="chapter" id="ch5">
            <h2>Chapter 5: 최종 결론</h2>
            
            <div class="recommendation" style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);">
                <h3>📋 실행 권고안 (Ch3 9개 상권 분석 결과 기반)</h3>
                <table class="comparison-table" style="background: white; color: #2c3e50;">
                    <tr>
                        <th>우선순위</th>
                        <th>상권</th>
                        <th>종합점수</th>
                        <th>전략</th>
                    </tr>
                    <tr>
                        <td><strong>1순위</strong></td>
                        <td>강남역</td>
                        <td><strong>75.8점</strong></td>
                        <td>고객 수요 최고 + 프리미엄 차별화 전략</td>
                    </tr>
                    <tr>
                        <td><strong>2순위</strong></td>
                        <td>선릉역</td>
                        <td><strong>45.4점</strong></td>
                        <td>직장인 타겟 안정적 운영</td>
                    </tr>
                    <tr>
                        <td><strong>3순위</strong></td>
                        <td>강남 마이스</td>
                        <td><strong>39.3점</strong></td>
                        <td>저경쟁 블루오션 + 외국인 의료관광</td>
                    </tr>
                </table>
            </div>
            
            <h3>핵심 인사이트 요약</h3>
            <ul>
                <li>✅ <strong>Ch1 공급 분석:</strong> 서울 피부과 시장은 의원급 98.5%로 소규모 클리닉 중심</li>
                <li>✅ <strong>Ch2 경쟁 분석:</strong> 강남구에 23.7% 집중 → 경쟁 치열하나 수요도 풍부</li>
                <li>✅ <strong>Ch3 수요 분석:</strong> 강남역(75.8점)이 종합 1위, 타겟 매출 2,764억</li>
                <li>✅ <strong>Ch4 입지 선정:</strong> 강남역 1순위 추천, 마이스특구 강남마이스 차선 고려</li>
            </ul>
            
            <div class="mice-box" style="background: linear-gradient(135deg, #16a085 0%, #1abc9c 100%);">
                <h3>🎯 최종 결론</h3>
                <p>강남 9개 상권 종합 분석 결과, <strong>강남역</strong>이 고객 수요, 유동인구, 인프라 모든 면에서 최적 입지로 평가됩니다.</p>
                <p>다만 경쟁이 최고 수준이므로 <strong>프리미엄 피부미용 전문 + 강력한 마케팅</strong>을 통한 차별화가 필수입니다.</p>
                <p>중장기적 외국인 의료관광 수요 대비 시 <strong>강남 마이스</strong> 상권이 저경쟁 블루오션으로 고려 가치가 있습니다.</p>
            </div>
        </div>
        
        <footer>
            <p>피부과 입지선정 통합 분석 리포트 | 데이터 기준: 2025.12 | Ch3 강남 9개 상권 분석 결과 반영</p>
        </footer>
    </div>
</body>
</html>
"""

# 저장
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("통합 리포트 생성 완료:", OUTPUT_FILE)
