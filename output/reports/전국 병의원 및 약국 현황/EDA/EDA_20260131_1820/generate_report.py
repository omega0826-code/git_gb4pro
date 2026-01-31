# -*- coding: utf-8 -*-
"""
서울 병원 통합 데이터 EDA 분석 리포트 생성기
작성일: 2026-01-31
"""

import base64
import os
from pathlib import Path
from datetime import datetime

# 경로 설정
OUTPUT_DIR = Path(r'd:\git_gb4pro\output\reports\전국 병의원 및 약국 현황\EDA\EDA_20260131_1820')
LOG_FILE = OUTPUT_DIR / 'analysis_log.txt'
HTML_FILE = OUTPUT_DIR / 'EDA_분석리포트_서울병원통합_20260131.html'

# 로그 파일 읽기
with open(LOG_FILE, 'r', encoding='utf-8') as f:
    log_content = f.read()

# 이미지 파일 목록
images = [
    ('01_type_distribution.png', '의료기관 유형 분포'),
    ('02_district_distribution.png', '자치구별 분포 (상위 10개)'),
    ('03_establish_distribution.png', '설립구분 분포'),
    ('04_year_distribution.png', '연도별 개원 추이'),
    ('05_specialist_analysis.png', '의과전문의 보유 현황'),
    ('06_bed_analysis.png', '병상 규모 분석'),
    ('07_department_analysis.png', '주요 진료과목 TOP 10'),
    ('08_age_size_analysis.png', '병원 연령대 및 규모 분석')
]

# 이미지를 Base64로 인코딩
def encode_image(img_path):
    with open(img_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# HTML 생성
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>서울 병원 통합 데이터 EDA 분석 리포트</title>
    <style>
        :root {{
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --text-primary: #2d3436;
            --text-secondary: #636e72;
            --bg-light: #f9f9f9;
            --card-bg: #ffffff;
            --accent: #ff7675;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Malgun Gothic', sans-serif;
            background: var(--bg-light);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .report-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: var(--bg-gradient);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .meta {{
            font-size: 0.95em;
            opacity: 0.9;
        }}
        
        .summary-box {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            border-left: 4px solid var(--primary-color);
        }}
        
        .summary-box h2 {{
            color: var(--primary-color);
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.12);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: var(--primary-color);
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.95em;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}
        
        .section h2 {{
            color: var(--primary-color);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--bg-light);
            font-size: 1.8em;
        }}
        
        .section h3 {{
            color: var(--text-primary);
            margin: 25px 0 15px 0;
            font-size: 1.4em;
        }}
        
        .image-container {{
            margin: 30px 0;
            text-align: center;
        }}
        
        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .image-caption {{
            margin-top: 10px;
            color: var(--text-secondary);
            font-size: 0.95em;
            font-style: italic;
        }}
        
        .insight-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid var(--accent);
        }}
        
        .insight-box::before {{
            content: "&#128161; ";
            font-size: 1.2em;
        }}
        
        ul {{
            margin: 15px 0 15px 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: bold;
        }}
        
        @media print {{
            .report-container {{
                max-width: 100%;
            }}
            .stat-card {{
                break-inside: avoid;
            }}
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <header>
            <h1>&#128202; 서울 병원 통합 데이터 EDA 분석 리포트</h1>
            <div class="meta">
                분석 기준일: 2026년 1월 31일<br>
                데이터: 전국 병의원 및 약국 현황 (2025.12 기준)<br>
                분석 가이드라인: EDA_서울병원통합_분석_가이드라인_V2.00.md
            </div>
        </header>
        
        <div class="summary-box">
            <h2>&#128204; Executive Summary</h2>
            <p>본 리포트는 서울시 소재 병의원 및 약국 <span class="highlight">19,641개</span> 기관에 대한 종합 탐색적 데이터 분석(EDA) 결과를 담고 있습니다. 
            의료기관 유형, 지역 분포, 설립 현황, 인력 규모, 진료과목 특성 등 6개 주요 영역에 걸친 분석을 수행하였습니다.</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">총 분석 기관 수</div>
                <div class="stat-value">19,641</div>
                <div class="stat-label">개</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">총 컬럼 수</div>
                <div class="stat-value">150</div>
                <div class="stat-label">개</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">데이터 크기</div>
                <div class="stat-value">52.45</div>
                <div class="stat-label">MB</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">자치구 수</div>
                <div class="stat-value">25</div>
                <div class="stat-label">개</div>
            </div>
        </div>
        
        <div class="section">
            <h2>1. 의료기관 유형 분포</h2>
            <div class="insight-box">
                의원급 의료기관(의원, 치과의원, 한의원)이 전체의 <strong>97.0%</strong>를 차지하며, 
                병원급 이상은 <strong>3.0%</strong>에 불과합니다.
            </div>
            <ul>
                <li><strong>의원</strong>: 10,491개 (53.4%) - 가장 많은 비중</li>
                <li><strong>치과의원</strong>: 4,868개 (24.8%)</li>
                <li><strong>한의원</strong>: 3,684개 (18.8%)</li>
                <li><strong>병원급 이상</strong>: 598개 (3.0%)</li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '01_type_distribution.png')}" alt="의료기관 유형 분포">
                <div class="image-caption">그림 1. 의료기관 유형별 분포</div>
            </div>
        </div>
        
        <div class="section">
            <h2>2. 지역별 분포 특성</h2>
            <div class="insight-box">
                <strong>강남구</strong>가 3,099개 기관으로 압도적 1위를 차지하며, 
                이는 2위 서초구(1,564개)의 약 <strong>2배</strong> 규모입니다.
            </div>
            <h3>상위 10개 자치구</h3>
            <ul>
                <li>1위: <strong>강남구</strong> - 3,099개 (15.8%)</li>
                <li>2위: <strong>서초구</strong> - 1,564개 (8.0%)</li>
                <li>3위: <strong>송파구</strong> - 1,304개 (6.6%)</li>
                <li>4위: <strong>강서구</strong> - 978개 (5.0%)</li>
                <li>5위: <strong>강동구</strong> - 958개 (4.9%)</li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '02_district_distribution.png')}" alt="자치구별 분포">
                <div class="image-caption">그림 2. 자치구별 의료기관 분포 (상위 10개)</div>
            </div>
        </div>
        
        <div class="section">
            <h2>3. 설립 및 개원 현황</h2>
            <div class="insight-box">
                <strong>개인 운영</strong> 의료기관이 98.1%로 절대 다수를 차지하며, 
                법인 형태는 극히 소수입니다.
            </div>
            <h3>설립구분</h3>
            <ul>
                <li><strong>개인</strong>: 19,264개 (98.1%)</li>
                <li><strong>의료법인</strong>: 116개 (0.6%)</li>
                <li><strong>공립/국립</strong>: 84개 (0.4%)</li>
                <li><strong>기타 법인</strong>: 177개 (0.9%)</li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '03_establish_distribution.png')}" alt="설립구분 분포">
                <div class="image-caption">그림 3. 설립구분별 분포</div>
            </div>
            
            <h3>개원 연도 분석</h3>
            <div class="insight-box">
                평균 개설연도는 <strong>2010년</strong>이며, 2010년대 개원한 기관이 
                <strong>31.2%</strong>로 가장 많습니다.
            </div>
            <ul>
                <li><strong>2020년대</strong>: 4,618개 (23.5%) - 최근 5년간 급증</li>
                <li><strong>2010년대</strong>: 6,125개 (31.2%) - 최다</li>
                <li><strong>2000년대</strong>: 5,387개 (27.4%)</li>
                <li><strong>1990년대 이전</strong>: 3,511개 (17.9%)</li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '04_year_distribution.png')}" alt="연도별 개원 추이">
                <div class="image-caption">그림 4. 연도별 개원 추이</div>
            </div>
        </div>
        
        <div class="section">
            <h2>4. 인력 현황 분석</h2>
            <div class="insight-box">
                의과전문의를 보유하지 않은 기관이 <strong>48.0%</strong>이며, 
                <strong>1인 의원</strong> 형태가 39.0%로 일반적입니다.
            </div>
            <h3>의과전문의 보유 현황</h3>
            <ul>
                <li><strong>0명</strong> (치과/한의원 등): 9,427개 (48.0%)</li>
                <li><strong>1명</strong> (1인 의원): 7,651개 (39.0%)</li>
                <li><strong>2명 이상</strong>: 2,563개 (13.0%)</li>
                <li>평균: <strong>1.38명</strong> / 최대: <strong>1,022명</strong></li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '05_specialist_analysis.png')}" alt="전문의 현황">
                <div class="image-caption">그림 5. 의과전문의 보유 현황</div>
            </div>
        </div>
        
        <div class="section">
            <h2>5. 병상 규모 분석</h2>
            <div class="insight-box">
                대부분의 의료기관(<strong>94.7%</strong>)은 일반병상을 보유하지 않으며, 
                이는 의원급 중심 구조를 반영합니다.
            </div>
            <h3>일반병상</h3>
            <ul>
                <li><strong>보유</strong>: 1,042개 (5.3%)</li>
                <li><strong>미보유</strong>: 18,599개 (94.7%)</li>
                <li>평균 병상수: <strong>68.0개</strong></li>
            </ul>
            <h3>상급병상</h3>
            <ul>
                <li><strong>보유</strong>: 1,482개 (7.5%)</li>
                <li><strong>미보유</strong>: 18,159개 (92.5%)</li>
                <li>평균 병상수: <strong>6.3개</strong></li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '06_bed_analysis.png')}" alt="병상 규모">
                <div class="image-caption">그림 6. 병상 규모 분석</div>
            </div>
        </div>
        
        <div class="section">
            <h2>6. 진료과목 특성</h2>
            <div class="insight-box">
                <strong>다과목 운영</strong> 기관이 77.0%로 대다수이며, 
                평균 <strong>5.48개</strong>의 진료과목을 운영합니다.
            </div>
            <h3>진료과목 개수</h3>
            <ul>
                <li><strong>단일 과목</strong>: 4,477개 (22.8%)</li>
                <li><strong>다과목 운영</strong>: 15,122개 (77.0%)</li>
                <li>평균: <strong>5.48개</strong> / 최대: <strong>36개</strong></li>
            </ul>
            <h3>주요 진료과목 TOP 10</h3>
            <ul>
                <li>1위: <strong>내과계</strong> - 5,874개 (29.9%)</li>
                <li>2위: <strong>미용계</strong> - 5,424개 (27.6%)</li>
                <li>3위: <strong>내과</strong> - 5,127개 (26.1%)</li>
                <li>4위: <strong>외과계</strong> - 4,998개 (25.4%)</li>
                <li>5위: <strong>피부과</strong> - 4,874개 (24.8%)</li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '07_department_analysis.png')}" alt="진료과목 분석">
                <div class="image-caption">그림 7. 주요 진료과목 TOP 10</div>
            </div>
        </div>
        
        <div class="section">
            <h2>7. 병원 연령대 분석</h2>
            <div class="insight-box">
                <strong>중견 병원</strong>(10-20년)이 29.2%로 가장 많으며, 
                신규 개원(5년 미만)도 19.2%로 활발한 시장 진입을 보입니다.
            </div>
            <h3>연령대별 분포</h3>
            <ul>
                <li><strong>신규</strong> (5년 미만): 3,780개 (19.2%)</li>
                <li><strong>성장기</strong> (5-10년): 3,453개 (17.6%)</li>
                <li><strong>중견</strong> (10-20년): 5,744개 (29.2%) - 최다</li>
                <li><strong>성숙</strong> (20-30년): 4,182개 (21.3%)</li>
                <li><strong>노포</strong> (30년 이상): 2,482개 (12.6%)</li>
            </ul>
            <div class="image-container">
                <img src="data:image/png;base64,{encode_image(OUTPUT_DIR / '08_age_size_analysis.png')}" alt="병원 연령대">
                <div class="image-caption">그림 8. 병원 연령대 및 규모 분석</div>
            </div>
        </div>
        
        <div class="section">
            <h2>8. 결측치 현황</h2>
            <p>총 <strong>27개</strong> 컬럼에서 결측치가 발견되었으며, 주요 결측치는 다음과 같습니다:</p>
            <ul>
                <li><strong>전문병원지정분야</strong>: 99.85% - 대부분 미지정</li>
                <li><strong>응급실 전화번호</strong>: 99.5% 이상 - 의원급 중심 구조 반영</li>
                <li>기타 결측치는 분석에 영향을 미치지 않는 수준</li>
            </ul>
        </div>
        
        <div class="summary-box">
            <h2>&#128200; 주요 발견사항 (Key Findings)</h2>
            <ul>
                <li><strong>의원급 중심 구조</strong>: 전체의 97%가 의원급 의료기관으로, 1차 의료 중심</li>
                <li><strong>강남 집중 현상</strong>: 강남구가 전체의 15.8%를 차지하며 압도적 1위</li>
                <li><strong>개인 운영 우세</strong>: 98.1%가 개인 운영으로 법인화 비율 극히 낮음</li>
                <li><strong>다과목 운영 일반화</strong>: 77%가 복수 진료과목 운영으로 경쟁력 확보</li>
                <li><strong>최근 개원 증가</strong>: 2020년대 들어 4,618개 신규 개원으로 시장 활성화</li>
                <li><strong>미용/피부과 강세</strong>: 미용계(27.6%), 피부과(24.8%)가 상위권 차지</li>
            </ul>
        </div>
        
        <footer style="text-align: center; padding: 30px; color: var(--text-secondary); border-top: 1px solid var(--bg-light); margin-top: 40px;">
            <p>본 리포트는 EDA 가이드라인 V2.00에 따라 자동 생성되었습니다.</p>
            <p>생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
        </footer>
    </div>
</body>
</html>
"""

# HTML 파일 저장
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[SUCCESS] HTML 리포트 생성 완료!")
print(f"파일 위치: {HTML_FILE}")
print(f"포함된 시각화: {len(images)}개")
print(f"파일 크기: {HTML_FILE.stat().st_size / 1024:.1f} KB")
