# -*- coding: utf-8 -*-
"""
Missing Value Guideline MD to HTML Converter
"""

import os
from datetime import datetime

def create_html():
    """Generate HTML from missing value guideline"""
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>결측치 처리 가이드라인</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --text-primary: #333;
            --text-secondary: #666;
            --bg-light: #f8f9fa;
            --bg-highlight: #fff3cd;
            --bg-insight: #e7f3ff;
        }
        
        body {
            font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: var(--text-primary);
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.8em;
            font-weight: 700;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header .meta {
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .content {
            padding: 40px;
        }
        
        h2 {
            font-size: 2.0em;
            font-weight: 600;
            color: var(--primary-color);
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary-color);
        }
        
        h3 {
            font-size: 1.5em;
            font-weight: 600;
            color: var(--secondary-color);
            margin: 30px 0 15px 0;
        }
        
        h4 {
            font-size: 1.2em;
            font-weight: 600;
            color: var(--text-primary);
            margin: 20px 0 10px 0;
        }
        
        p { margin: 15px 0; line-height: 1.8; }
        ul, ol { margin: 15px 0; padding-left: 30px; }
        li { margin: 8px 0; line-height: 1.6; }
        
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
            color: #e83e8c;
        }
        
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            line-height: 1.5;
        }
        
        pre code {
            background: none;
            color: #f8f8f2;
            padding: 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        
        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        th {
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover {
            background: #f5f7fa;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        blockquote {
            background: var(--bg-insight);
            border-left: 5px solid var(--primary-color);
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 8px;
            font-style: italic;
        }
        
        .info-box {
            background: #e7f3ff;
            border-left: 5px solid #17a2b8;
            padding: 20px 25px;
            margin: 25px 0;
            border-radius: 8px;
        }
        
        .warning-box {
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px 25px;
            margin: 25px 0;
            border-radius: 8px;
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .toc {
            background: var(--bg-light);
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
        }
        
        .toc h3 {
            color: var(--primary-color);
            margin-bottom: 15px;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8px 0;
        }
        
        .toc a {
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .toc a:hover {
            color: var(--primary-color);
        }
        
        .footer {
            background: var(--bg-light);
            padding: 30px 40px;
            text-align: center;
            color: var(--text-secondary);
            border-top: 1px solid #e0e0e0;
        }
        
        .checklist {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .checklist li {
            list-style: none;
            padding: 8px 0;
        }
        
        .checklist li:before {
            content: "☐ ";
            color: var(--primary-color);
            font-weight: bold;
            margin-right: 8px;
        }
        
        hr {
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 40px 0;
        }
        
        @media (max-width: 768px) {
            body { padding: 10px; }
            .header { padding: 30px 20px; }
            .header h1 { font-size: 2em; }
            .content { padding: 20px; }
            h2 { font-size: 1.6em; }
            h3 { font-size: 1.3em; }
            table { font-size: 0.9em; }
            th, td { padding: 8px 10px; }
        }
        
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; }
            .header { background: white; color: black; border-bottom: 3px solid #333; }
            pre { background: #f4f4f4; color: #333; border: 1px solid #ddd; }
            .footer { border-top: 2px solid #333; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 결측치 처리 가이드라인</h1>
            <div class="meta">
                <p><strong>Missing Value Handling Guidelines</strong></p>
                <p>목적: 데이터 분석 및 처리 시 결측치를 체계적으로 다루기 위한 일반적인 방법론 제시</p>
                <p>적용 범위: 모든 데이터 분석 프로젝트</p>
                <p>작성일: 2026-01-19 | HTML 변환: """ + current_time + """</p>
            </div>
        </div>
        
        <div class="content">
            <div class="toc">
                <h3>📋 목차</h3>
                <ul>
                    <li><a href="#principles">1. 결측치 처리 기본 원칙</a></li>
                    <li><a href="#process">2. 결측치 분석 프로세스</a></li>
                    <li><a href="#patterns">3. 결측치 패턴 분류</a></li>
                    <li><a href="#methods">4. 결측치 처리 방법</a></li>
                    <li><a href="#decision">5. 컬럼별 처리 방법 결정 프로세스</a></li>
                    <li><a href="#documentation">6. 결측치 처리 문서화 템플릿</a></li>
                    <li><a href="#warnings">7. 주의사항</a></li>
                    <li><a href="#references">8. 참고 자료</a></li>
                    <li><a href="#checklist">9. 체크리스트</a></li>
                </ul>
            </div>
            
            <div class="section" id="principles">
                <h2>📌 1. 결측치 처리 기본 원칙</h2>
                
                <h3>1.1 핵심 원칙</h3>
                <table>
                    <thead>
                        <tr>
                            <th>원칙</th>
                            <th>설명</th>
                            <th>적용 예시</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>데이터 보존 우선</strong></td>
                            <td>가능한 한 원본 데이터를 유지하고, 삭제는 최소화</td>
                            <td>결측치가 있어도 다른 유용한 정보가 있다면 보존</td>
                        </tr>
                        <tr>
                            <td><strong>의미 기반 처리</strong></td>
                            <td>결측치의 의미(없음 vs 미제공)를 구분하여 처리</td>
                            <td>"장비 없음"과 "장비 정보 미제공"은 다르게 처리</td>
                        </tr>
                        <tr>
                            <td><strong>분석 목적 고려</strong></td>
                            <td>향후 분석 목적에 맞는 처리 방법 선택</td>
                            <td>통계 분석용과 머신러닝용은 다른 전략 필요</td>
                        </tr>
                        <tr>
                            <td><strong>투명성 확보</strong></td>
                            <td>모든 처리 내역을 문서화하고 추적 가능하게 관리</td>
                            <td>처리 로그, 버전 관리, 메타데이터 기록</td>
                        </tr>
                        <tr>
                            <td><strong>일관성 유지</strong></td>
                            <td>동일한 유형의 데이터는 동일한 방식으로 처리</td>
                            <td>프로젝트 전체에서 통일된 규칙 적용</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="section" id="process">
                <h2>📊 2. 결측치 분석 프로세스</h2>
                
                <h3>2.1 단계별 분석 절차</h3>
                <div class="info-box">
                    <ol>
                        <li><strong>데이터 로드</strong> &rarr; 원본 데이터 불러오기</li>
                        <li><strong>결측치 현황 파악</strong> &rarr; 기본 통계 수집</li>
                        <li><strong>결측치 패턴 분류</strong> &rarr; 비율 및 의미 분석</li>
                        <li><strong>결측치 원인 분석</strong> &rarr; MCAR, MAR, MNAR 판단</li>
                        <li><strong>처리 전략 수립</strong> &rarr; 컬럼별 처리 방법 결정</li>
                        <li><strong>처리 실행</strong> &rarr; 코드 작성 및 실행</li>
                        <li><strong>검증 및 문서화</strong> &rarr; 결과 확인 및 기록</li>
                    </ol>
                </div>

                <h3>2.2 결측치 현황 파악 - 기본 통계 수집</h3>
                <pre><code>import pandas as pd
import numpy as np

def analyze_missing_values(df):
    missing_stats = pd.DataFrame({
        '전체_건수': len(df),
        '결측치수': df.isnull().sum(),
        '결측_비율(%)': (df.isnull().sum() / len(df) * 100).round(2),
        '데이터타입': df.dtypes
    })
    
    missing_stats = missing_stats[missing_stats['결측치수'] > 0]
    missing_stats = missing_stats.sort_values('결측_비율(%)', ascending=False)
    
    return missing_stats</code></pre>
            </div>

            <div class="section" id="patterns">
                <h2>🔍 3. 결측치 패턴 분류</h2>
                
                <h3>3.1 결측 비율에 따른 분류</h3>
                <table>
                    <thead>
                        <tr>
                            <th>분류</th>
                            <th>결측 비율</th>
                            <th>처리 전략</th>
                            <th>예시</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>낮은 결측률</strong></td>
                            <td>0-10%</td>
                            <td>대체 또는 제거 가능</td>
                            <td>필수 정보 일부 누락</td>
                        </tr>
                        <tr>
                            <td><strong>중간 결측률</strong></td>
                            <td>10-50%</td>
                            <td>신중한 대체 또는 플래그 추가</td>
                            <td>선택적 정보</td>
                        </tr>
                        <tr>
                            <td><strong>높은 결측률</strong></td>
                            <td>50-80%</td>
                            <td>결측 유지 또는 별도 분석</td>
                            <td>특수 정보</td>
                        </tr>
                        <tr>
                            <td><strong>매우 높은 결측률</strong></td>
                            <td>80% 이상</td>
                            <td>컬럼 제거 고려 또는 결측 유지</td>
                            <td>거의 제공되지 않는 정보</td>
                        </tr>
                    </tbody>
                </table>

                <h3>3.2 결측치 의미에 따른 분류</h3>
                
                <h4>A. MCAR (Missing Completely At Random)</h4>
                <ul>
                    <li><strong>특징</strong>: 결측치가 완전히 무작위로 발생</li>
                    <li><strong>판단 기준</strong>: 결측 여부가 다른 변수와 무관</li>
                    <li><strong>처리 방법</strong>: 단순 삭제 또는 평균/중앙값 대체 가능</li>
                </ul>

                <h4>B. MAR (Missing At Random)</h4>
                <ul>
                    <li><strong>특징</strong>: 결측치가 관측된 다른 변수와 관련</li>
                    <li><strong>판단 기준</strong>: 특정 조건에서 결측이 더 많이 발생</li>
                    <li><strong>처리 방법</strong>: 조건부 대체, 회귀 대체</li>
                </ul>

                <h4>C. MNAR (Missing Not At Random)</h4>
                <ul>
                    <li><strong>특징</strong>: 결측치가 결측값 자체와 관련</li>
                    <li><strong>판단 기준</strong>: 값이 너무 크거나 작아서 누락</li>
                    <li><strong>처리 방법</strong>: 도메인 지식 기반 처리, 별도 플래그</li>
                </ul>
            </div>

            <div class="section" id="methods">
                <h2>🛠️ 4. 결측치 처리 방법</h2>
                
                <h3>4.1 삭제 (Deletion)</h3>
                <pre><code>def remove_rows_with_missing(df, columns=None, threshold=None):
    if columns:
        df_clean = df.dropna(subset=columns)
    elif threshold:
        df_clean = df.dropna(thresh=threshold)
    else:
        df_clean = df.dropna()
    
    print(f"원본: {len(df)}건 &rarr; 처리 후: {len(df_clean)}건")
    return df_clean</code></pre>

                <h3>4.2 대체 (Imputation)</h3>
                <pre><code>def simple_imputation(df, strategy='mean'):
    df_imputed = df.copy()
    
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if strategy == 'mean' and df[col].dtype in ['int64', 'float64']:
                df_imputed[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median' and df[col].dtype in ['int64', 'float64']:
                df_imputed[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'zero':
                df_imputed[col].fillna(0, inplace=True)
    
    return df_imputed</code></pre>
            </div>

            <div class="section" id="decision">
                <h2>📋 5. 컬럼별 처리 방법 결정 프로세스</h2>
                
                <h3>5.1 의사결정 플로우차트</h3>
                <div class="info-box">
                    <pre>1. 컬럼이 필수 정보인가?
   ├─ YES &rarr; 결측 시 행 삭제
   └─ NO &rarr; 2번으로

2. 결측 비율이 80% 이상인가?
   ├─ YES &rarr; 컬럼 삭제 고려 또는 결측 유지
   └─ NO &rarr; 3번으로

3. 결측의 의미가 "없음"인가?
   ├─ YES (예: 장비 없음, 직원 0명)
   │   └─ 수치형: 0으로 대체
   │   └─ 범주형: 'N' 또는 '해당없음'으로 대체
   └─ NO (정보 미제공) &rarr; 4번으로

4. 결측 비율이 10% 미만인가?
   ├─ YES &rarr; 평균/중앙값/최빈값으로 대체
   └─ NO &rarr; 결측 유지 (NULL) + 플래그 추가 고려</pre>
                </div>

                <h3>5.2 처리 방법 매트릭스</h3>
                <table>
                    <thead>
                        <tr>
                            <th>데이터 유형</th>
                            <th>결측 비율</th>
                            <th>결측 의미</th>
                            <th>권장 처리 방법</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>필수 정보</td>
                            <td>모든 비율</td>
                            <td>-</td>
                            <td><strong>행 삭제</strong></td>
                        </tr>
                        <tr>
                            <td>수치형</td>
                            <td>0-10%</td>
                            <td>없음</td>
                            <td><strong>0으로 대체</strong></td>
                        </tr>
                        <tr>
                            <td>수치형</td>
                            <td>10-50%</td>
                            <td>없음</td>
                            <td><strong>0으로 대체</strong></td>
                        </tr>
                        <tr>
                            <td>수치형</td>
                            <td>50% 이상</td>
                            <td>-</td>
                            <td><strong>결측 유지 (NULL)</strong></td>
                        </tr>
                        <tr>
                            <td>범주형</td>
                            <td>0-10%</td>
                            <td>없음</td>
                            <td><strong>'해당없음' 대체</strong></td>
                        </tr>
                        <tr>
                            <td>Y/N 플래그</td>
                            <td>모든 비율</td>
                            <td>없음</td>
                            <td><strong>'N'으로 대체</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="section" id="warnings">
                <h2>⚠️ 7. 주의사항</h2>
                
                <h3>7.1 일반적 주의사항</h3>
                
                <div class="warning-box">
                    <h4>1. 과도한 삭제 지양</h4>
                    <ul>
                        <li>행 삭제는 정보 손실을 초래하므로 신중하게 결정</li>
                        <li>가능하면 대체 방법 우선 고려</li>
                    </ul>
                </div>

                <div class="warning-box">
                    <h4>2. 대체값의 의미 명확화</h4>
                    <ul>
                        <li>0 대체: "없음"을 의미하는지 명확히 구분</li>
                        <li>NULL 유지: "정보 미제공"의 의미</li>
                    </ul>
                </div>

                <div class="warning-box">
                    <h4>3. 데이터 타입 일관성</h4>
                    <ul>
                        <li>대체 후에도 원래 데이터 타입 유지</li>
                        <li>수치형 컬럼에 문자열 대체 금지</li>
                    </ul>
                </div>
            </div>

            <div class="section" id="references">
                <h2>📚 8. 참고 자료</h2>
                
                <h3>8.1 추천 라이브러리</h3>
                <ul>
                    <li><strong>pandas</strong>: 기본 결측치 처리</li>
                    <li><strong>scikit-learn</strong>: SimpleImputer, KNNImputer</li>
                    <li><strong>missingno</strong>: 결측치 시각화</li>
                    <li><strong>fancyimpute</strong>: 고급 대체 알고리즘</li>
                </ul>
            </div>

            <div class="section" id="checklist">
                <h2>📌 9. 체크리스트</h2>
                
                <div class="checklist">
                    <p><strong>결측치 처리 완료 전 확인사항:</strong></p>
                    <ul>
                        <li>결측치 현황 파악 완료</li>
                        <li>결측치 패턴 분류 완료</li>
                        <li>컬럼별 처리 방법 결정</li>
                        <li>처리 코드 작성 및 테스트</li>
                        <li>처리 전후 비교 검증</li>
                        <li>처리 로그 기록</li>
                        <li>문서화 완료</li>
                        <li>원본 데이터 백업</li>
                        <li>처리된 데이터 저장</li>
                        <li>팀 리뷰 완료</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>문서 버전</strong>: 1.0 | <strong>최종 수정</strong>: 2026-01-19 | <strong>작성자</strong>: Data Analysis Team</p>
            <p>HTML 변환: """ + current_time + """</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    output_dir = r'd:\git_gb4pro\crawling\openapi\getHospDetailList\REPORT'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'missing_value_guideline_{timestamp}.html')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("=" * 60)
    print("Missing Value Guideline HTML Conversion Complete")
    print("=" * 60)
    print(f"\nHTML file created successfully!")
    print(f"Location: {output_file}")
    print(f"File size: {os.path.getsize(output_file):,} bytes")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    create_html()
